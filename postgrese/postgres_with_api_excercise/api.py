from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from db import create_table, add_password, get_password, update_password
from typing import Optional

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
    email: Optional[EmailStr] = Field(None, example="user@gmail.com")

    @validator("site")
    def validate_site(cls, value):
        allowed_suffixes = [".com", ".org", ".net", ".edu", ".io", ".gov", ".co", ".info", ".us", ".uk"]

        if not any(value.endswith(suffix) for suffix in allowed_suffixes):
            raise ValueError(
                f"Invalid site name '{value}'. It must end with one of: {', '.join(allowed_suffixes)}"
            )

        # Disallow spaces or uppercase letters
        if " " in value or value != value.lower():
            raise ValueError("Site name must be lowercase and contain no spaces")

        return value

    @validator("email", pre=True)
    def empty_to_none(cls, value):
        if value == "":
            return None
        return value

    @validator("email")
    def validate_email(cls, value):
        allowed_domains = [
            "@gmail.com",
            "@outlook.com",
            "@yahoo.com",
            "@icloud.com",
            "@hotmail.com",
            "@protonmail.com",
            "@aol.com",
            "@zoho.com",
            "@live.com",
            "@mail.com"
        ]

        if value and not any(value.endswith(domain) for domain in allowed_domains):
            raise ValueError(
                f"{value} is not allowed. Must end with one of: {', '.join(allowed_domains)}"
            )
        return value



class PasswordUpdate(BaseModel):
    new_password: str = Field(..., min_length=3, example="new_secure_password")

@app.post("/add")
def add_entry(entry: PasswordEntry):
    try:
        new_id = add_password(entry.site, entry.username, entry.password)
        return {"message": "Password added!", "id": new_id}
    except Exception as e:
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
