(function () {
    const schedule = [
        { time: '9:00 AM', event: 'Morning Review' },
        { time: '12:00 PM', event: 'Lunch with Team' },
        { time: '3:00 PM', event: 'Project Update Meeting' },
    ];

    const scheduleList = document.getElementById('schedule-list');
    schedule.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.time} - ${item.event}`;
        scheduleList.appendChild(li);
    });

    const tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
    const taskList = document.getElementById('task-list');
    const taskInput = document.getElementById('task-input');
    const addTaskBtn = document.getElementById('add-task');

    function renderTasks() {
        taskList.innerHTML = '';
        tasks.forEach((task, index) => {
            const li = document.createElement('li');
            li.textContent = task;
            li.addEventListener('click', () => {
                tasks.splice(index, 1);
                localStorage.setItem('tasks', JSON.stringify(tasks));
                renderTasks();
            });
            taskList.appendChild(li);
        });
    }

    addTaskBtn.addEventListener('click', () => {
        if (taskInput.value.trim()) {
            tasks.push(taskInput.value.trim());
            taskInput.value = '';
            localStorage.setItem('tasks', JSON.stringify(tasks));
            renderTasks();
        }
    });

    renderTasks();

    const notesArea = document.getElementById('notes-area');
    notesArea.value = localStorage.getItem('notes') || '';
    notesArea.addEventListener('input', () => {
        localStorage.setItem('notes', notesArea.value);
    });
})();
