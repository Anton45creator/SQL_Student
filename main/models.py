from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import DATABASE


Base = declarative_base()


association_table = Table(
    'association',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('course_id', Integer, ForeignKey('course.id')),
)


class GroupModel(Base):
    bind = 'students'
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self) -> str:
        return self.name


class StudentModel(Base):

    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    group_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    courses = relationship(
        'CourseModel',
        secondary=association_table,
        backref="students",
        )

    def __repr__(self) -> str:
        return f'\n{self.first_name} {self.last_name}: {self.group_id}'


class CourseModel(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self) -> str:
        return self.name


engine = create_engine(f'postgresql+psycopg2://{DATABASE}')
Base.metadata.create_all(engine)
