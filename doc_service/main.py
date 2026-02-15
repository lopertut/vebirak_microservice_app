from fastapi import FastAPI
from types import Optional
import uvicorn 
import db
import os


app = FastAPI()


@app.get("/get_doc")
def get_doc(doc_id):
    return db.get_doc(doc_id)


@app.post("/create_doc")
def create_doc(doc: Optional[dict], doc_path: Optional[str]):
    return db.create_doc(doc, doc_path)


@app.put("/update_doc")
def update_doc(doc_id, key: str, new_value):
    return db.update_doc(doc_id, key: str, new_value)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="localhost", port=os.environ.get("port"), reload=True
    )
