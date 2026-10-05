from sqlalchemy import select, update, delete
from app.database import async_session_maker


class BaseDao:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            students = await session.execute(select(cls.model).filter_by(**filter_by))
            return students.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id):
        async with async_session_maker() as session:
            student = await session.execute(select(cls.model).where(cls.model.id == data_id))
            
            return student.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            student = await session.execute(select(cls.model).filter_by(**filter_by))
            return student.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance


    @classmethod
    async def update(cls, filter_by, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model).where(
                        *[
                            getattr(cls.model, k) == v for k, v in filter_by.items()
                        ]
                    ).values(**values).execution_options(synchronize_session="fetch")
                ) 
                result = await session.execute(query)

                try: 
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

                return result.rowcount

    @classmethod
    async def delete(cls, delete_all: bool = False, **by_filter):#unpacking named arguments to dict
        if not delete_all and not by_filter:
            raise ValueError("t least one parameter is required for deletion")
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")


        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model).filter_by(**by_filter)

                result = await session.execute(query)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    