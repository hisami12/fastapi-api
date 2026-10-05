from fastapi import APIRouter
from app.majors.schemas import MajorsAdd, MajorsUpdate
from app.majors.dao import MajorDao

router = APIRouter(prefix="/majors", tags=["majors"])



@router.post("/")
async def add(data: MajorsAdd)->dict:
    major = await MajorDao.add(**data.model_dump())
    
    if major:
        return {"message": "Факультет успешно добавлен!", "major": data.model_dump()}
    else:
        return {"message": "Ошибка при добавлении факультета!"}
    return {"message": "user has been added"}



@router.put("/update_description/")
async def update(data: MajorsUpdate):
    major = await MajorDao.update(filter_by={"major_name": data.major_name}, major_description=data.major_description)

    
    if major:
        return {"message": "Описание факультета успешно обновлено!", "major": major}
    else: 
        return {"message": "Ошибка при обновлении описания факультета!"}


@router.delete("/delete/{major_id}")
async def delete(major_id: int):
    major = await MajorDao.delete(id=major_id)
    if major:
        return {"message": f"Факультет с ID {major_id} удален!"}
    else:
        return {"message": "Ошибка при удалении факультета!"}