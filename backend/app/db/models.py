from sqlalchemy import Column,Integer,String,Text,Boolean,ForeignKey,Date,Enum,DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    name = Column(String(50), nullable=False)
    family_name = Column(String(50), nullable=False)
    is_confirmed = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    program_id = Column(Integer, ForeignKey('programs.id', ondelete='SET NULL'), nullable=True)
    program = relationship('Program', back_populates='users')
    gender = Column(String(10), nullable=False)
    remarks = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    expire_date = Column(Date, nullable=True)
    photo = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<User {self.name}>'

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    number_of_instances = Column(Integer, default=0)
    icone_path=Column(String(255), nullable=False)
    icone_path_female=Column(String(255), nullable=False)
    exercises = relationship('Exercise', back_populates='category')


    def __repr__(self):
        return f'<Category {self.name}>'

class Exercise(Base):
    __tablename__ = 'exercises'
    code = Column(String(255), primary_key=True)
    name = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    description = Column(Text, nullable=False)
    video_path = Column(Text, nullable=False)
    video_path_female = Column(Text, nullable=False)
    category = relationship('Category', back_populates='exercises')
    program_details = relationship('ProgramDetail', back_populates='exercise')


    def __repr__(self):
        return f'<Exercise {self.name}, vids : {self.video_path} and {self.video_path_female} >'

class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    creator = Column(String(255), nullable=False)
    users = relationship('User', back_populates='program')
    created_at = Column(DateTime, default=datetime.utcnow)
    details = relationship('ProgramDetail', back_populates='program')

    def __repr__(self):
        return f'<Program {self.name}>'

class ProgramDetail(Base):
    __tablename__ = "program_details"
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    exercise_code = Column(String(255), ForeignKey('exercises.code'), nullable=True)
    sequence = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    type = Column(Enum('exercise', name='detail_type'), nullable=False)
    program = relationship('Program', back_populates='details')
    exercise = relationship('Exercise', back_populates='program_details')


    def __repr__(self):
        return f'<ProgramDetails Program {self.program_id} Item {self.id}>'