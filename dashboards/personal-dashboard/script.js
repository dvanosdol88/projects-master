const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');
const taskList = document.getElementById('task-list');
const notesArea = document.getElementById('notes-area');
const sidebar = document.getElementById('sidebar');
const toggleMenu = document.getElementById('toggle-menu');

function loadTasks() {
  const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
  tasks.forEach((task) => addTaskToDOM(task));
}

function saveTasks() {
  const tasks = Array.from(taskList.children).map((li) => li.textContent);
  localStorage.setItem('tasks', JSON.stringify(tasks));
}

function addTaskToDOM(task) {
  const li = document.createElement('li');
  li.textContent = task;
  li.addEventListener('click', () => {
    li.remove();
    saveTasks();
  });
  taskList.appendChild(li);
}

taskForm.addEventListener('submit', (e) => {
  e.preventDefault();
  addTaskToDOM(taskInput.value);
  saveTasks();
  taskInput.value = '';
});

notesArea.addEventListener('input', () => {
  localStorage.setItem('notes', notesArea.value);
});

function loadNotes() {
  notesArea.value = localStorage.getItem('notes') || '';
}

toggleMenu.addEventListener('click', () => {
  sidebar.classList.toggle('visible');
});

loadTasks();
loadNotes();
