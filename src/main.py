from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Task Management API")


class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    description: str
    status: str
    priority: int = Field(..., ge=1, le=5)


tasks = [
    Task(
        id=1,
        title="Learn FastAPI",
        description="Study FastAPI REST API",
        status="Pending",
        priority=1
    ),
    Task(
        id=2,
        title="Write Tests",
        description="Create pytest test cases",
        status="Completed",
        priority=2
    )
]


# GET - Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# GET - Get task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# POST - Create a new task
@app.post("/tasks", status_code=201)
def create_task(task: Task):

    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(
                status_code=400,
                detail="Task ID already exists"
            )

    tasks.append(task)

    return task


# PUT - Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):

    for index, task in enumerate(tasks):

        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# DELETE - Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):

        if task.id == task_id:
            deleted_task = tasks.pop(index)
            return deleted_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )