# models is the file where tables are created
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    role: Mapped[str]
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    
    tasks: Mapped[list["Task"]] = relationship(
            back_populates="owner",
    )
    # tasks: Mapped[list["Task"]] = mapped_column(relationship(default=[]))
    
    # User.tasks will return a list of the tasks attached to this user
    # But it would return in a unreadable format like:
    #   [ <Book at 0x...> , <Book at 0x...>, ... ]
    # back populates mean that changes on one side changes the other and vice-versa
    
    # this is called one-to-many:
    #   Task.owner = user (one object)
    #   User.tasks = list of tasks objects (many objects)
    
    def __repr__(self):
        #task_ids = [task.id for task in self.tasks]
        #return f"User (id={self.id!r}, name={self.name!r}, email={self.email!r}, hashed_password={self.hashed_password!r}, tasks={task_ids!r})"
        return f"User (id={self.id!r}, role={self.role!r}, name={self.name!r}, email={self.email!r}, hashed_password={self.hashed_password!r})"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )
    is_checked: Mapped[int] = mapped_column(default=0)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # ForeignKey ensures that the owner_user_id is the same as the id of the user tho created
    #   this task (links two tables)
    
    owner: Mapped["User"] = relationship(
            back_populates="tasks"
    )
    
    # Task.owner will return the user object attached to the task
    # But it's computed by ORM at runtime, not a column in the database
    
    def __repr__(self) -> str:
        return f"Task (id={self.id!r}, title={self.title!r}, description={self.description!r}, is_checked={self.is_checked!r}), owner_user_id={self.owner_user_id!r}, owner={self.owner}"
