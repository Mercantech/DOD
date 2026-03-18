import os
import asyncio
from typing import List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import discord
from discord.ext import commands
from discord import app_commands

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from db import get_session, engine, Base, DATABASE_URL, AsyncSessionLocal
import crud
import schemas


DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "CHANGE_ME")


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
app = FastAPI(title="Discord Bot Skeleton")

_tree_synced = False


async def _format_todo_line(todo) -> str:
    return f"{todo.id}. [{'x' if todo.completed else ' '}] {todo.title}"


async def _fetch_todos() -> list:
    raise RuntimeError("Use _fetch_todos_for_user(external_id) instead")


async def _create_todo(title: str) -> object:
    raise RuntimeError("Use _create_todo_for_user(external_id, title) instead")


async def _toggle_todo(todo_id: int) -> Optional[object]:
    raise RuntimeError("Use _toggle_todo_for_user(external_id, todo_id) instead")


async def _delete_todo(todo_id: int) -> bool:
    raise RuntimeError("Use _delete_todo_for_user(external_id, todo_id) instead")


async def _get_user_id(*, provider: str, external_id: str) -> int:
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider=provider, external_id=external_id)
        return user.id


async def _fetch_todos_for_user(*, provider: str, external_id: str) -> list:
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider=provider, external_id=external_id)
        return await crud.get_todos(session, owner_id=user.id)


async def _create_todo_for_user(*, provider: str, external_id: str, title: str) -> object:
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider=provider, external_id=external_id)
        return await crud.create_todo(session, owner_id=user.id, data=schemas.TodoCreate(title=title))


async def _toggle_todo_for_user(*, provider: str, external_id: str, todo_id: int) -> Optional[object]:
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider=provider, external_id=external_id)
        todo = await crud.get_todo(session, owner_id=user.id, todo_id=todo_id)
        if not todo:
            return None
        todo.completed = not todo.completed
        await session.commit()
        await session.refresh(todo)
        return todo


async def _delete_todo_for_user(*, provider: str, external_id: str, todo_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider=provider, external_id=external_id)
        return await crud.delete_todo(session, owner_id=user.id, todo_id=todo_id)


def _todos_embed(todos: list) -> discord.Embed:
    embed = discord.Embed(title="Todos", color=discord.Color.blurple())
    if not todos:
        embed.description = "Ingen todos endnu."
        return embed
    embed.description = "\n".join([f"- {t.id}. {'✅' if t.completed else '⬜'} {t.title}" for t in todos[:20]])
    if len(todos) > 20:
        embed.set_footer(text=f"Viser 20 af {len(todos)} todos")
    return embed


class TodoAddModal(discord.ui.Modal, title="Tilføj todo"):
    todo_title = discord.ui.TextInput(
        label="Titel",
        placeholder="Fx: Lær Docker",
        max_length=255,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        title = str(self.todo_title.value).strip()
        if not title:
            await interaction.followup.send("Titel må ikke være tom.", ephemeral=True)
            return
        external_id = str(interaction.user.id)
        todo = await _create_todo_for_user(provider="discord", external_id=external_id, title=title)
        await interaction.followup.send(
            f"Oprettet todo #{todo.id}: {todo.title}",
            ephemeral=True,
        )


class TodoSelect(discord.ui.Select):
    def __init__(self, *, todos: list, placeholder: str, action: str, external_id: str):
        options = [
            discord.SelectOption(
                label=f"#{t.id} {'(færdig)' if t.completed else ''}".strip(),
                description=(t.title[:90] + "…") if len(t.title) > 90 else t.title,
                value=str(t.id),
            )
            for t in todos[:25]
        ]
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)
        self.action = action
        self.external_id = external_id

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        todo_id = int(self.values[0])

        if self.action == "toggle":
            todo = await _toggle_todo_for_user(provider="discord", external_id=self.external_id, todo_id=todo_id)
            if not todo:
                await interaction.followup.send("Todo findes ikke længere.", ephemeral=True)
                return
            await interaction.followup.send(
                f"Todo #{todo.id} er nu {'færdig' if todo.completed else 'ikke færdig'}.",
                ephemeral=True,
            )
            return

        if self.action == "delete":
            ok = await _delete_todo_for_user(provider="discord", external_id=self.external_id, todo_id=todo_id)
            if not ok:
                await interaction.followup.send("Todo findes ikke længere.", ephemeral=True)
                return
            await interaction.followup.send(f"Slettede todo #{todo_id}.", ephemeral=True)
            return

        await interaction.followup.send("Ukendt handling.", ephemeral=True)


class TodoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="Opdater", style=discord.ButtonStyle.secondary)
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True, thinking=True)
        external_id = str(interaction.user.id)
        todos = await _fetch_todos_for_user(provider="discord", external_id=external_id)
        await interaction.edit_original_response(embed=_todos_embed(todos), view=self)

    @discord.ui.button(label="Tilføj", style=discord.ButtonStyle.primary)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TodoAddModal())

    @discord.ui.button(label="Toggle", style=discord.ButtonStyle.success)
    async def toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True, thinking=True)
        external_id = str(interaction.user.id)
        todos = await _fetch_todos_for_user(provider="discord", external_id=external_id)
        if not todos:
            await interaction.followup.send("Ingen todos at toggle.", ephemeral=True)
            return
        view = discord.ui.View(timeout=60)
        view.add_item(TodoSelect(todos=todos, placeholder="Vælg todo at toggle…", action="toggle", external_id=external_id))
        await interaction.followup.send("Vælg en todo:", view=view, ephemeral=True)

    @discord.ui.button(label="Slet", style=discord.ButtonStyle.danger)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True, thinking=True)
        external_id = str(interaction.user.id)
        todos = await _fetch_todos_for_user(provider="discord", external_id=external_id)
        if not todos:
            await interaction.followup.send("Ingen todos at slette.", ephemeral=True)
            return
        view = discord.ui.View(timeout=60)
        view.add_item(TodoSelect(todos=todos, placeholder="Vælg todo at slette…", action="delete", external_id=external_id))
        await interaction.followup.send("Vælg en todo:", view=view, ephemeral=True)


@bot.event
async def on_ready():
    global _tree_synced
    if not _tree_synced:
        try:
            await bot.tree.sync()
            _tree_synced = True
            print("Slash commands synced.")
        except Exception as e:
            print(f"Failed to sync slash commands: {e}")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    msg = "Der opstod en fejl i kommandoen. Prøv igen om lidt."
    try:
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
    except Exception:
        pass


@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")


@bot.command(name="todo_add")
async def todo_add(ctx: commands.Context, *, title: str):
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider="discord", external_id=str(ctx.author.id))
        todo = await crud.create_todo(session, owner_id=user.id, data=schemas.TodoCreate(title=title))
    await ctx.send(f"Oprettet todo #{todo.id}: {todo.title}")


@bot.command(name="todo_list")
async def todo_list(ctx: commands.Context):
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider="discord", external_id=str(ctx.author.id))
        todos = await crud.get_todos(session, owner_id=user.id)
    if not todos:
        await ctx.send("Ingen todos endnu.")
        return
    lines = [
        f"{t.id}. [{'x' if t.completed else ' '}] {t.title}"
        for t in todos
    ]
    await ctx.send("\n".join(lines))


@bot.command(name="todo_toggle")
async def todo_toggle(ctx: commands.Context, todo_id: int):
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider="discord", external_id=str(ctx.author.id))
        todo = await crud.get_todo(session, owner_id=user.id, todo_id=todo_id)
        if not todo:
            await ctx.send(f"Todo #{todo_id} findes ikke.")
            return
        todo.completed = not todo.completed
        await session.commit()
        await session.refresh(todo)
    await ctx.send(
        f"Todo #{todo.id} er nu {'færdig' if todo.completed else 'ikke færdig'}."
    )


@bot.command(name="todo_delete")
async def todo_delete(ctx: commands.Context, todo_id: int):
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider="discord", external_id=str(ctx.author.id))
        ok = await crud.delete_todo(session, owner_id=user.id, todo_id=todo_id)
    if not ok:
        await ctx.send(f"Todo #{todo_id} findes ikke.")
        return
    await ctx.send(f"Slettede todo #{todo_id}.")


# Slash commands (interaktivt)
todo_group = app_commands.Group(name="todo", description="Administrér todos")


@todo_group.command(name="list", description="Vis todos (med interaktive knapper)")
async def todo_list_slash(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)
    external_id = str(interaction.user.id)
    todos = await _fetch_todos_for_user(provider="discord", external_id=external_id)
    await interaction.followup.send(
        embed=_todos_embed(todos),
        view=TodoView(),
        ephemeral=True,
    )


@todo_group.command(name="add", description="Opret en todo")
@app_commands.describe(title="Titel på todo")
async def todo_add_slash(interaction: discord.Interaction, title: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    title = title.strip()
    if not title:
        await interaction.followup.send("Titel må ikke være tom.", ephemeral=True)
        return
    external_id = str(interaction.user.id)
    todo = await _create_todo_for_user(provider="discord", external_id=external_id, title=title)
    await interaction.followup.send(f"Oprettet todo #{todo.id}: {todo.title}", ephemeral=True)


@todo_group.command(name="toggle", description="Toggle completed på en todo")
@app_commands.describe(todo_id="Id på todo")
async def todo_toggle_slash(interaction: discord.Interaction, todo_id: int):
    await interaction.response.defer(ephemeral=True, thinking=True)
    external_id = str(interaction.user.id)
    todo = await _toggle_todo_for_user(provider="discord", external_id=external_id, todo_id=todo_id)
    if not todo:
        await interaction.followup.send("Todo findes ikke.", ephemeral=True)
        return
    await interaction.followup.send(
        f"Todo #{todo.id} er nu {'færdig' if todo.completed else 'ikke færdig'}.",
        ephemeral=True,
    )


@todo_group.command(name="delete", description="Slet en todo")
@app_commands.describe(todo_id="Id på todo")
async def todo_delete_slash(interaction: discord.Interaction, todo_id: int):
    await interaction.response.defer(ephemeral=True, thinking=True)
    external_id = str(interaction.user.id)
    ok = await _delete_todo_for_user(provider="discord", external_id=external_id, todo_id=todo_id)
    if not ok:
        await interaction.followup.send("Todo findes ikke.", ephemeral=True)
        return
    await interaction.followup.send(f"Slettede todo #{todo_id}.", ephemeral=True)


bot.tree.add_command(todo_group)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/info")
async def info():
    return {
        "bot": str(bot.user) if bot.user else None,
        "database_url": DATABASE_URL,
    }


async def _require_user_id(x_user_id: Optional[str] = Header(default=None)) -> int:
    """
    Midlertidig "auth" til WebUI: klienten sender X-User-Id header.
    Senere kan vi skifte til rigtig auth og mappe til samme User-tabel.
    """
    if not x_user_id or not str(x_user_id).strip():
        raise HTTPException(status_code=401, detail="Missing X-User-Id header")
    external_id = str(x_user_id).strip()
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, provider="web", external_id=external_id)
        return user.id


@app.get("/api/todos", response_model=List[schemas.TodoRead])
async def list_todos(
    user_id: int = Depends(_require_user_id),
    db: AsyncSession = Depends(get_session),
):
    todos = await crud.get_todos(db, owner_id=user_id)
    return todos


@app.post("/api/todos", response_model=schemas.TodoRead)
async def create_todo(
    todo: schemas.TodoCreate,
    user_id: int = Depends(_require_user_id),
    db: AsyncSession = Depends(get_session),
):
    return await crud.create_todo(db, owner_id=user_id, data=todo)


@app.get("/api/todos/{todo_id}", response_model=schemas.TodoRead)
async def get_todo(
    todo_id: int,
    user_id: int = Depends(_require_user_id),
    db: AsyncSession = Depends(get_session),
):
    todo = await crud.get_todo(db, owner_id=user_id, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/api/todos/{todo_id}", response_model=schemas.TodoRead)
async def update_todo(
    todo_id: int,
    data: schemas.TodoUpdate,
    user_id: int = Depends(_require_user_id),
    db: AsyncSession = Depends(get_session),
):
    todo = await crud.update_todo(db, owner_id=user_id, todo_id=todo_id, data=data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.delete("/api/todos/{todo_id}")
async def delete_todo(
    todo_id: int,
    user_id: int = Depends(_require_user_id),
    db: AsyncSession = Depends(get_session),
):
    ok = await crud.delete_todo(db, owner_id=user_id, todo_id=todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"status": "deleted", "id": todo_id}


@app.get("/")
async def index():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")


def start_bot():
    asyncio.run(bot.start(DISCORD_BOT_TOKEN))


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Minimal "migration" for demo, så eksisterende DB kan opgraderes uden Alembic.
        await conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS users (
                  id SERIAL PRIMARY KEY,
                  external_id VARCHAR(64) NOT NULL,
                  provider VARCHAR(32) NOT NULL DEFAULT 'discord',
                  CONSTRAINT users_provider_external_id_key UNIQUE (provider, external_id)
                );
                """
            )
        )
        # Tidlige versioner havde (forkert) unique på kun external_id, hvilket blokerer for samme id i flere providers.
        # Dropper de kendte navne hvis de findes, og sikrer derefter korrekt unikhed på (provider, external_id).
        await conn.execute(text("DROP INDEX IF EXISTS ix_users_external_id;"))
        await conn.execute(text("DROP INDEX IF EXISTS users_external_id_key;"))
        await conn.execute(text("DROP INDEX IF EXISTS ux_users_external_id;"))

        # Hvis tabellen allerede fandtes uden constraint, så sørg mindst for en unik index.
        await conn.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS ux_users_provider_external_id ON users (provider, external_id);"
            )
        )

        # Sørg for at todos har owner_id (create_all ændrer ikke eksisterende tabeller).
        await conn.execute(text("ALTER TABLE todos ADD COLUMN IF NOT EXISTS owner_id INTEGER;"))

        # Backfill legacy todos (fra før brugersystemet) til en default user.
        await conn.execute(
            text(
                """
                INSERT INTO users (provider, external_id)
                SELECT 'legacy', 'legacy'
                WHERE NOT EXISTS (
                  SELECT 1 FROM users WHERE provider='legacy' AND external_id='legacy'
                );
                """
            )
        )
        await conn.execute(
            text(
                """
                UPDATE todos
                SET owner_id = (
                  SELECT id FROM users WHERE provider='legacy' AND external_id='legacy'
                )
                WHERE owner_id IS NULL;
                """
            )
        )

        # Index + FK (IF NOT EXISTS hvor muligt)
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_todos_owner_id ON todos (owner_id);"))
        await conn.execute(
            text(
                """
                DO $$
                BEGIN
                  IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint WHERE conname = 'todos_owner_id_fkey'
                  ) THEN
                    ALTER TABLE todos
                    ADD CONSTRAINT todos_owner_id_fkey
                    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE;
                  END IF;
                END
                $$;
                """
            )
        )
        await conn.execute(text("ALTER TABLE todos ALTER COLUMN owner_id SET NOT NULL;"))

        await conn.run_sync(Base.metadata.create_all)

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(DISCORD_BOT_TOKEN))

