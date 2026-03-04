import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json

app = FastAPI()




@app.get("/")
async def main():
    return FileResponse("public/index.html")
@app.get("/find")
async def main():
    return FileResponse("public/find.html")

@app.get("/add")
async def add_page():
    return FileResponse("public/add.html")

@app.get("/result")
async def result_page():
    return FileResponse("public/result.html")



def save_notes():
    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

try:
    with open('db.json', 'r', encoding='utf-8') as f:
        notes = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    notes = []





@app.get(
    "/notes",
    tags=["Заметки"],
    summary="Список заметок"

)
def read_notes():
    return notes

@app.get(
    "/notes/{id}",
    tags=["Выбор заметок"],
    summary="Напишите 'id' вашей книге",
)
def read_notes(id: int):
    for note in notes:
        if note["id"] == id:
            return note
    raise HTTPException(status_code=404, detail="note not found")

class Newnote(BaseModel):
    title: str
    content: str

@app.put(
    "/notes/{id}",
    tags=["Изменить"], )

@app.put("/notes/{id}", tags=["Изменить"])
def update_note(id: int, updated_note: Newnote):
    for note in notes:
        if note["id"] == id:
            note["title"] = updated_note.title
            note["content"] = updated_note.content
            save_notes()
            return {"success": True}

    raise HTTPException(status_code=404, detail="note not found")


@app.delete("/notes/{id}")
def delete_note(id: int):
    for note in notes:
        if note["id"] == id:
            notes.remove(note)
            save_notes()
            return {"success": True}
    raise HTTPException(status_code=404, detail="note not found")


@app.post("/notes")
def create_note(note: Newnote):

    if notes:
        new_id = max(n["id"] for n in notes) + 1
    else:
        new_id = 1

    new_note = {
        "id": new_id,
        "title": note.title,
        "content": note.content,
    }

    notes.append(new_note)
    save_notes()
    return {"success": True}

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)