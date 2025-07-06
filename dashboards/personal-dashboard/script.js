(function () {
  const taskInput = document.getElementById('new-task');
  const addTaskBtn = document.getElementById('add-task');
  const taskListEl = document.getElementById('task-list');

  const tasks = JSON.parse(localStorage.getItem('tasks') || '[]');

  function renderTasks() {
    taskListEl.innerHTML = '';
    tasks.forEach((task, index) => {
      const li = document.createElement('li');
      const span = document.createElement('span');
      span.textContent = task;
      const delBtn = document.createElement('button');
      delBtn.textContent = 'Delete';
      delBtn.className = 'delete-btn';
      delBtn.addEventListener('click', () => deleteTask(index));
      li.appendChild(span);
      li.appendChild(delBtn);
      taskListEl.appendChild(li);
    });
  }

  function addTask() {
    const value = taskInput.value.trim();
    if (!value) return;
    tasks.push(value);
    taskInput.value = '';
    saveTasks();
    renderTasks();
  }

  function deleteTask(index) {
    tasks.splice(index, 1);
    saveTasks();
    renderTasks();
  }

  function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }

  addTaskBtn.addEventListener('click', addTask);
  renderTasks();
})();
