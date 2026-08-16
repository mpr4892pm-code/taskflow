const API_BASE_URL =  "https://taskflow-4hhe.onrender.com";

const taskForm = document.getElementById("taskForm");

const titleInput = document.getElementById("title");

const projectIdInput = document.getElementById("projectId");

const dueDateInput = document.getElementById("dueDate");

const priorityInput = document.getElementById("priority");

const titleError = document.getElementById("titleError");

const taskList = document.getElementById("taskList");


// --------------------------------------------------
// Local Storage Cache
// --------------------------------------------------

let tasks = JSON.parse(
    localStorage.getItem("tasks")
) || [];


// --------------------------------------------------
// Render cached data immediately
// --------------------------------------------------

renderTasks(tasks);


// --------------------------------------------------
// Save backend data to localStorage
// --------------------------------------------------

function saveTasksToCache(taskData) {

    localStorage.setItem(
        "tasks",
        JSON.stringify(taskData)
    );
}


// --------------------------------------------------
// Load tasks from REAL BACKEND
// --------------------------------------------------

async function loadTasks() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/tasks`
        );


        if (!response.ok) {

            throw new Error(
                "Failed to load tasks"
            );
        }


        const backendTasks =
            await response.json();


        // Backend is the source of truth
        tasks = backendTasks;


        // Update cache with real backend data
        saveTasksToCache(tasks);


        // Render real backend data
        renderTasks(tasks);

    }

    catch (error) {

        console.error(
            "Error loading tasks:",
            error
        );

        // Cached tasks remain visible
        // if backend is temporarily unavailable
    }
}


// --------------------------------------------------
// Render Tasks
// --------------------------------------------------

function renderTasks(taskData) {

    taskList.textContent = "";


    if (taskData.length === 0) {

        const emptyMessage =
            document.createElement("p");

        emptyMessage.textContent =
            "No tasks found.";

        taskList.appendChild(emptyMessage);

        return;
    }


    taskData.forEach(function(task) {

        const taskItem =
            document.createElement("div");

        taskItem.classList.add("task-item");


        // ------------------------------------------
        // Title
        // ------------------------------------------

        const taskTitle =
            document.createElement("h3");

        taskTitle.textContent =
            task.title;


        // ------------------------------------------
        // Project ID
        // ------------------------------------------

        const project =
            document.createElement("p");

        project.textContent =
            `Project ID: ${task.project_id}`;


        // ------------------------------------------
        // Due Date
        // ------------------------------------------

        const dueDate =
            document.createElement("p");

        dueDate.textContent =
            `Due Date: ${
                task.due_date || "Not set"
            }`;


        // ------------------------------------------
        // Priority
        // ------------------------------------------

        const priority =
            document.createElement("p");

        priority.textContent =
            `Priority: ${
                task.priority || "Not set"
            }`;


        // ------------------------------------------
        // Buttons container
        // ------------------------------------------

        const actions =
            document.createElement("div");

        actions.classList.add(
            "task-actions"
        );


        // ------------------------------------------
        // Edit button
        // ------------------------------------------

        const editButton =
            document.createElement("button");

        editButton.textContent = "Edit";

        editButton.classList.add(
            "edit-btn"
        );


        editButton.addEventListener(
            "click",
            function() {

                editTask(task);

            }
        );


        // ------------------------------------------
        // Delete button
        // ------------------------------------------

        const deleteButton =
            document.createElement("button");

        deleteButton.textContent = "Delete";

        deleteButton.classList.add(
            "delete-btn"
        );


        deleteButton.addEventListener(
            "click",
            function() {

                deleteTask(task.task_id);

            }
        );


        // ------------------------------------------
        // Append elements
        // ------------------------------------------

        actions.appendChild(editButton);

        actions.appendChild(deleteButton);


        taskItem.appendChild(taskTitle);

        taskItem.appendChild(project);

        taskItem.appendChild(dueDate);

        taskItem.appendChild(priority);

        taskItem.appendChild(actions);


        taskList.appendChild(taskItem);

    });
}


// --------------------------------------------------
// ADD TASK
// --------------------------------------------------

taskForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const title =
            titleInput.value.trim();


        // ------------------------------------------
        // Client-side validation
        // ------------------------------------------

        if (title === "") {

            titleError.textContent =
                "Task title is required.";

            titleInput.focus();

            return;
        }


        titleError.textContent = "";


        const projectId =
            Number(projectIdInput.value);


        if (!projectId) {

            alert(
                "Please enter a valid Project ID."
            );

            return;
        }


        const priority =
            priorityInput.value.trim();


        // ------------------------------------------
        // Data sent to FastAPI
        // ------------------------------------------

        const newTask = {

            project_id: projectId,

            title: title,

            description: "",

            priority:
                priority || "medium",

            due_date:
                dueDateInput.value || null

        };


        try {

            const response =
                await fetch(
                    `${API_BASE_URL}/tasks`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(newTask)
                    }
                );


            if (!response.ok) {

                const errorData =
                    await response.json();

                console.error(
                    "Backend error:",
                    errorData
                );

                alert(
                    "Task could not be created."
                );

                return;
            }


            // Backend-created task
            const createdTask =
                await response.json();


            // Add returned backend object
            tasks.push(createdTask);


            // Update cache
            saveTasksToCache(tasks);


            // Update UI
            renderTasks(tasks);


            // Clear form
            taskForm.reset();

        }

        catch (error) {

            console.error(
                "Error creating task:",
                error
            );

            alert(
                "Backend server is not running."
            );
        }

    }
);


// --------------------------------------------------
// EDIT TASK
// --------------------------------------------------

async function editTask(task) {

    const newTitle =
        prompt(
            "Enter new task title:",
            task.title
        );


    if (
        newTitle === null ||
        newTitle.trim() === ""
    ) {

        return;
    }


    const updatedTask = {

        title: newTitle.trim(),

        description:
            task.description || "",

        priority:
            task.priority || "medium",

        due_date:
            task.due_date || null,

        project_id:
            task.project_id

    };


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/tasks/${task.task_id}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(updatedTask)
                }
            );


        if (!response.ok) {

            alert(
                "Task could not be updated."
            );

            return;
        }


        const updatedBackendTask =
            await response.json();


        // Replace old task
        tasks =
            tasks.map(function(item) {

                if (
                    item.task_id ===
                    updatedBackendTask.task_id
                ) {

                    return updatedBackendTask;
                }

                return item;

            });


        // Cache real backend data
        saveTasksToCache(tasks);


        // Update UI
        renderTasks(tasks);

    }

    catch (error) {

        console.error(
            "Error updating task:",
            error
        );
    }
}


// --------------------------------------------------
// DELETE TASK
// --------------------------------------------------

async function deleteTask(taskId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this task?"
        );


    if (!confirmed) {

        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/tasks/${taskId}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            alert(
                "Task could not be deleted."
            );

            return;
        }


        // Remove from frontend state
        tasks =
            tasks.filter(function(task) {

                return task.task_id !== taskId;

            });


        // Update cache
        saveTasksToCache(tasks);


        // Update UI
        renderTasks(tasks);

    }

    catch (error) {

        console.error(
            "Error deleting task:",
            error
        );
    }
}


// --------------------------------------------------
// Remove validation error when user types
// --------------------------------------------------

titleInput.addEventListener(
    "input",
    function() {

        if (
            titleInput.value.trim() !== ""
        ) {

            titleError.textContent = "";
        }

    }
);


// --------------------------------------------------
// Load REAL backend data on page load
// --------------------------------------------------

loadTasks();