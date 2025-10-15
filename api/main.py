from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

#python -m venv venv
#.\venv\Scripts\activate  
#python -m pip install requests
#python .\testing_endpoint.py

#To call: fastapi dev .\main.py
app = FastAPI(title="Todo API", version="1.0")

class Todo(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, Eggs, Bread")
    completed: bool = Field(False, example=False)

# In-memory storage (mock DB)
todos: List[Todo] = []

@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo):
    for existing in todos:
        if existing.id == todo.id:
            raise HTTPException(status_code=400, detail="Todo ID already exists.")
    todos.append(todo)
    return todo

@app.get("/todos/", response_model=List[Todo])
def get_all_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found.")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found for update.")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[index]
    raise HTTPException(status_code=404, detail="Todo not found for deletion.")
