from fastapi import FastAPI, Request
import uvicorn 
import db
import os
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()


@app.get("/get_doc")
def get_doc(doc_id):
    doc = db.get_doc(doc_id)
    if doc:
        return {"status": "success", "doc": doc}
    else:
        return {"satus": "fail"}


@app.post("/create_doc")
async def create_doc(request: Request): 
    doc = await request.json() 
    try:
        db.create_doc(doc)
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"satus": "fail"}
        

@app.put("/update_doc")
def update_doc(doc_id, key: str, new_value):
        update_doc = db.update_doc(doc_id, key, new_value)
        if update_doc:
            return {"status": "success"}
        else:
            return {"status": "fail"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=os.environ.get("host"), port=int(os.environ.get("port")), reload=True
    )
