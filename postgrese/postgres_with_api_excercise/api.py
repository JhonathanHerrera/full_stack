from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from db import create_table, add_password, get_password, update_password

app = FastAPI(title="Password Manager API")
#fastapi dev main.py     
# Create the table when the server starts (init)
@app.on_event("startup")
def init_db():
    create_table()

# Pydantic model
class PasswordEntry(BaseModel):
    site: str = Field(..., example="gmail.com")
    username: str = Field(..., example="user@gmail.com")
    password: str = Field(..., min_length=3, example="abc123")

class PasswordUpdate(BaseModel):
    new_password: str = Field(..., min_length=3, example="new_secure_password")

@app.post("/add")
def add_entry(entry: PasswordEntry):
    try:
        print("3")
        new_id = add_password(entry.site, entry.username, entry.password)
        return {"message": "Password added!", "id": new_id}
    except Exception as e:
        print("1")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get/{site}")
def get_entry(site: str):
    result = get_password(site)
    if not result:
        raise HTTPException(status_code=404, detail="Site not found")
    return result

@app.put("/update/{site}")
def update_entry(site: str, payload: PasswordUpdate):
    updated = update_password(site, payload.new_password)
    if not updated:
        raise HTTPException(status_code=404, detail="Site not found or not updated")
    return {"message": "Password updated!", "site": site}
