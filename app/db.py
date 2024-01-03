from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

from app.models import FunctionSubmission

Base = declarative_base()


from sqlalchemy import JSON


from sqlalchemy import JSON, PickleType


class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    code = Column(String)
    description = Column(String)
    dependencies = Column(String, nullable=True)
    args = Column(PickleType, nullable=True)  # Use PickleType instead of JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def dependencies_list(self):
        if self.dependencies:
            return self.dependencies.split(",")
        return []

    @dependencies_list.setter
    def dependencies_list(self, dependencies):
        if dependencies:
            self.dependencies = ",".join(dependencies)
        else:
            self.dependencies = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "dependencies": self.dependencies_list,
            "args": dict(self.args),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def add_function(db: Session, function: FunctionSubmission) -> Function:
    function_dict = function.model_dump()
    function_dict["dependencies_list"] = function_dict.pop("dependencies")
    existing_function = (
        db.query(Function).filter(Function.name == function_dict["name"]).first()
    )
    if existing_function:
        for key, value in function_dict.items():
            setattr(existing_function, key, value)
        db.commit()
        db.refresh(existing_function)
        return existing_function
    else:
        function = Function(**function_dict)

        db.add(function)
        db.commit()
        db.refresh(function)
        return function


def get_function(db: Session, name: str):
    function = db.query(Function).where(Function.name == name).first()
    return function


def get_all_functions(db: Session):
    functions = db.query(Function).all()
    return functions
