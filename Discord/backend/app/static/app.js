document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("check-health");
  const out = document.getElementById("health-output");
  const form = document.getElementById("todo-form");
  const titleInput = document.getElementById("todo-title");
  const list = document.getElementById("todo-list");
  const userIdInput = document.getElementById("user-id");
  const saveUserBtn = document.getElementById("save-user");

  function getUserId() {
    return localStorage.getItem("dod_user_id") || "";
  }

  function setUserId(value) {
    localStorage.setItem("dod_user_id", value);
  }

  function authHeaders() {
    const userId = getUserId();
    return userId ? { "X-User-Id": userId } : {};
  }

  function ensureUserId() {
    const id = getUserId();
    if (!id) {
      list.innerHTML =
        "<li>Vælg et Bruger-id (demo) ovenfor, så du får din egen todo-liste.</li>";
      return false;
    }
    return true;
  }

  // Health check
  btn?.addEventListener("click", async () => {
    out.textContent = "Henter...";
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      out.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      out.textContent = "Fejl ved kald til API'et";
    }
  });

  // Helpers til todos
  async function fetchTodos() {
    const res = await fetch("/api/todos", { headers: authHeaders() });
    if (!res.ok) {
      throw new Error("Kunne ikke hente todos");
    }
    return await res.json();
  }

  async function createTodo(title) {
    const res = await fetch("/api/todos", {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify({ title, completed: false }),
    });
    if (!res.ok) throw new Error("Kunne ikke oprette todo");
    return await res.json();
  }

  async function toggleTodo(todo) {
    const res = await fetch(`/api/todos/${todo.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify({ title: todo.title, completed: !todo.completed }),
    });
    if (!res.ok) throw new Error("Kunne ikke opdatere todo");
    return await res.json();
  }

  async function deleteTodo(id) {
    const res = await fetch(`/api/todos/${id}`, {
      method: "DELETE",
      headers: authHeaders(),
    });
    if (!res.ok) throw new Error("Kunne ikke slette todo");
  }

  function renderTodos(todos) {
    list.innerHTML = "";
    if (!todos.length) {
      const li = document.createElement("li");
      li.textContent = "Ingen todos endnu.";
      list.appendChild(li);
      return;
    }

    for (const todo of todos) {
      const li = document.createElement("li");
      li.className = "todo-item";

      const title = document.createElement("span");
      title.className = "todo-title" + (todo.completed ? " completed" : "");
      title.textContent = `${todo.id}. ${todo.title}`;

      const actions = document.createElement("span");
      actions.className = "todo-actions";

      const toggleBtn = document.createElement("button");
      toggleBtn.textContent = todo.completed ? "Markér som ikke færdig" : "Markér som færdig";
      toggleBtn.addEventListener("click", async () => {
        try {
          const updated = await toggleTodo(todo);
          todo.completed = updated.completed;
          loadTodos();
        } catch (err) {
          alert("Fejl ved opdatering af todo");
        }
      });

      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "Slet";
      deleteBtn.className = "delete";
      deleteBtn.addEventListener("click", async () => {
        if (!confirm("Slet denne todo?")) return;
        try {
          await deleteTodo(todo.id);
          loadTodos();
        } catch (err) {
          alert("Fejl ved sletning af todo");
        }
      });

      actions.appendChild(toggleBtn);
      actions.appendChild(deleteBtn);

      li.appendChild(title);
      li.appendChild(actions);
      list.appendChild(li);
    }
  }

  async function loadTodos() {
    if (!ensureUserId()) return;
    try {
      const todos = await fetchTodos();
      renderTodos(todos);
    } catch (err) {
      list.innerHTML = "<li>Kunne ikke hente todos fra API'et.</li>";
    }
  }

  saveUserBtn?.addEventListener("click", () => {
    const val = userIdInput.value.trim();
    if (!val) {
      alert("Indtast et Bruger-id (demo).");
      return;
    }
    setUserId(val);
    loadTodos();
  });

  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = titleInput.value.trim();
    if (!title) return;
    try {
      await createTodo(title);
      titleInput.value = "";
      loadTodos();
    } catch (err) {
      alert("Fejl ved oprettelse af todo");
    }
  });

  // Initial load
  const existingUserId = getUserId();
  if (existingUserId) userIdInput.value = existingUserId;
  loadTodos();
});
