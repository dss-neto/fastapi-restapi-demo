# models is the file where tables are created
# TODO: figure out how to make this sqlalchemy work
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

# TODO: relationship Task(owner_user_id) and User(id)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    tasks: Mapped[list["Task"]] = mapped_column(relationship(back_populates="owner"))
    # User.tasks will return a list of the tasks attached to this user
    # But it would return in a unreadable format like:
    #   [ <Book at 0x...> , <Book at 0x...>, ... ]
    # back populates mean that changes on one side changes the other and vice-versa
    
    # this is called one-to-many:
    #   Task.owner = user (one object)
    #   User.tasks = list of tasks objects (many objects)
    
    def __repr__(self):
        task_ids = [task.id for task in self.tasks]
        return f"User (id={self.id!r}, name={self.name!r}, email={self.email!r}, hashed_password={self.hashed_password!r}, tasks={task_ids!r})"

# TODO: User.tasks, Task.owner and owner_user_id foreign was added, get an idea of how they work

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    is_checked: Mapped[int] = mapped_column(default=0)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # ForeignKey ensures that the owner_user_id is the same as the id of the user tho created
    #   this task
    owner: Mapped[User] = mapped_column(relationship(back_populates="tasks"))
    # Task.owner will return the user object attached to the task

    def __repr__(self) -> str:
        return f"Task (id={self.id!r}, title={self.title!r}, description={self.description!r}, is_checked={self.is_checked!r}), owner_user_id={self.owner_user_id!r}, owner={self.owner}"