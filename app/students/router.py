from fastapi import APIRouter
from app.students.dao import StudentDao
from app.students.schemas import SStudent, StudentIn
from app.students.rb import RBStudent
from fastapi import Depends

router = APIRouter(prefix="/students", tags=["working with students"])


@router.get("/", summary="get all students", response_model=list[SStudent])
async def get_all_students(request_body: RBStudent = Depends()):
    return await StudentDao.find_all(**request_body.to_dict())



@router.get('/byfilter', summary="get a student by filter")
async def get_student_or_none(request_body: RBStudent = Depends()):
    student = await StudentDao.find_one_or_none(**request_body.to_dict())
    if student is None:
        return {"message": f'student with the specified details not found'}
    return student 
            
@router.get("/{student_id}", summary="Получить одного студента по id")
async def get_student_by_id(student_id: int) -> SStudent | dict:
    rez = await StudentDao.find_full_data(student_id)
    if rez is None:
        return {'message': f'Студент с ID {student_id} не найден!'}
    return rez

@router.post("/add", summary="add a new student")
async def add_student(student_data: StudentIn):
    res = await StudentDao.add_student(student_data.model_dump())
    if res:
        return {"message": "student has been added successfuly", "student": res}
    else:
        return {"message": "failed to added the student"}

@router.delete("/del/{student_id}")
async def dell_student_by_id(student_id: int) -> dict:
    check = await StudentDao.delete_student_by_id(student_id=student_id)
    if check:
        return {"message": f"Student with ID {student_id} has been deleted!"}
    else:
        return {"message": "Ошибка при удалении студента!"}

@router.put("/update")
async def update(filter_by: SStudent):
    student = await StudentDao.update({"id": filter_by.id}, first_name=filter_by.first_name)
    if student:
        return {"message":"The student data has been updated", "student": student}
    else: return {"message":"Failed to update the student data"}