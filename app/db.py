from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

from app.models import FunctionBase

Base = declarative_base()


class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    code = Column(String)
    description = Column(String)
    dependencies = Column(String, nullable=True)
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


DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def add_function(db: Session, function: FunctionBase) -> Function:
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


if __name__ == "__main__":
    from pydantic import BaseModel

    class FunctionModel(BaseModel):
        name: str
        code: str
        description: str
        dependencies: list[str]

    # Create a Pydantic model instance
    function_model = FunctionModel(
        name="my_function",
        code="""
    import numpy as np
    import pandas as pd

    def calculate_mean(dataframe, column):
        return np.mean(dataframe[column])

    data = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
    mean = calculate_mean(data, 'A')
    print('Mean of column A:', mean)
    """,
        description="A function that calculates the mean of a column in a pandas DataFrame using numpy",
        dependencies=["numpy", "pandas"],
    )

    add_function(SessionLocal(), function_model)
