from fastapi import FastAPI 
from app.students.router import router as router_students
from app.majors.router import router as router_majors
app = FastAPI()

@app.get("/")
async def home_page():
    return {"message": "this`s home page"}

app.include_router(router_students)
app.include_router(router_majors)






