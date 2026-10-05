
from app.students.models import Student
from app.dao.base import BaseDao
from app.database import async_session_maker
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from app.majors.models import Major
class StudentDao(BaseDao):
    model = Student


    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_session_maker() as session:
            query_student = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result_student = await session.execute(query_student)
            student_info = result_student.scalar_one_or_none()

            if not student_info:
                return None
            student_data = student_info.to_dict()
            student_data["major"] = student_info.major.major_name
            return student_data


    @classmethod
    async def add_student(cls, data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)

            student = await session.execute(query)
            new_instance = student.scalar_one()

            update_major = update(Major).where(Major.id==new_instance.major_id).values(count_students=Major.count_students+1)

            await session.execute(update_major)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance
    @classmethod
    async def delete_student_by_id(cls, student_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=student_id)
                result = await session.execute(query)
                student_to_delete = result.scalar_one_or_none()

                if not student_to_delete:
                    return None

                # Удаляем студента
                await session.execute(
                    delete(cls.model).filter_by(id=student_id)
                )

                await session.commit()
                return student_id