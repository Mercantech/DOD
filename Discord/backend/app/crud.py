from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Todo, User
from schemas import TodoCreate, TodoUpdate


async def get_or_create_user(db: AsyncSession, *, provider: str, external_id: str) -> User:
    result = await db.execute(
        select(User).where(User.provider == provider, User.external_id == external_id)
    )
    user = result.scalar_one_or_none()
    if user:
        return user
    user = User(provider=provider, external_id=external_id)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_todos(db: AsyncSession, *, owner_id: int) -> List[Todo]:
    result = await db.execute(
        select(Todo).where(Todo.owner_id == owner_id).order_by(Todo.id)
    )
    return list(result.scalars().all())


async def create_todo(db: AsyncSession, *, owner_id: int, data: TodoCreate) -> Todo:
    todo = Todo(title=data.title, completed=data.completed, owner_id=owner_id)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def get_todo(db: AsyncSession, *, owner_id: int, todo_id: int) -> Optional[Todo]:
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id, Todo.owner_id == owner_id)
    )
    return result.scalar_one_or_none()


async def update_todo(
    db: AsyncSession, *, owner_id: int, todo_id: int, data: TodoUpdate
) -> Optional[Todo]:
    todo = await get_todo(db, owner_id=owner_id, todo_id=todo_id)
    if not todo:
        return None
    todo.title = data.title
    todo.completed = data.completed
    await db.commit()
    await db.refresh(todo)
    return todo


async def delete_todo(db: AsyncSession, *, owner_id: int, todo_id: int) -> bool:
    todo = await get_todo(db, owner_id=owner_id, todo_id=todo_id)
    if not todo:
        return False
    await db.delete(todo)
    await db.commit()
    return True

