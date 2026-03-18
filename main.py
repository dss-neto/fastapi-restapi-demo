from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.params import Body
from random import randint

app = FastAPI()


class Task(BaseModel):
    name: str
    check: bool


taskDict = {}


@app.post("/tasks")
def create_task(task: Task = Body(...)):
    tasksLimit = 9999  # Max amount of tasks

    if len(taskDict) == tasksLimit:  # Checks if the limit has been reached
        return f"{tasksLimit} tasks limit reached. Delete a task to add more."
    taskId = randint(1, tasksLimit)  # ID: a number between the task limit and 1

    while taskId in taskDict:
        taskId = randint(1, tasksLimit)  # RNG ID until different than existent
    taskDict[taskId] = task
    return task


@app.get("/tasks")
def read_task_list():
    return taskDict


@app.get("/tasks/{key}")
def read_task(key: int):
    return taskDict[key]


@app.put("/tasks/{key}")
def update_task(key: int, task: Task = Body(...)):
    taskDict[key] = task
    return task


@app.delete("/tasks/{key}")
def delete_task(key: int):
    del taskDict[key]
    return taskDict
