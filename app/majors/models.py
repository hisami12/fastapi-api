from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base



class Major(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    major_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    major_description: Mapped[str] = mapped_column(nullable=True)
    count_students: Mapped[int] = mapped_column(server_default=text("0")) 
    students = relationship("Student", back_populates="major")
    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, major_name={self.major_name!r})'

    def __repr__(self):
        return str(self)   