from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import ProgrammingError
import llm
import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectRequest(BaseModel):
    db_url: str

class AskRequest(BaseModel):
    question: str

current_db = None

@app.post("/connect")
def connect(req: ConnectRequest):
    global current_db
    current_db = req.db_url
    return {"status": "connected"}

@app.post("/ask")
def ask(req: AskRequest):
    global current_db
    if not current_db:
        raise HTTPException(status_code=400, detail="Database not connected")

    try:
        sql = llm.nl_to_sql(req.question, current_db)

        if sql == "CANNOT_ANSWER":
            return {"sql": "--", "result": [], "explanation": "No data found."}

        try:
            rows, cols = db.run_query(current_db, sql)
            result = [dict(zip(cols, row)) for row in rows]
        except Exception as db_err:
            raise HTTPException(status_code=400, detail=f"SQL Error: {str(db_err)}")

        explanation = llm.explain(req.question, result)

        return {
            "sql": sql,
            "result": result,
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
