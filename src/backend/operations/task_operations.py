from src.backend.tertiary.validation import (
    raise_forbidden_error,
    raise_no_content,
)
from src.backend.database.models import Task
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update

#TODO: find out how to stop declaring "With Session(engine)" everytime

def get_task_data(
    task_id: int, 
    owner_user_id: int,
    session: Session # Session here is just a type hint, the important thing is = Depends(get_session)
    # Depends(get_session): FastAPI runs the function and yields session to the endpoint, after finishing the function it closes the session
    # if get_session() was return instead of yield, the with statement would close when  the return is reached
):
    stmt = select(Task).where((Task.id==task_id) & (Task.owner_user_id == owner_user_id))
    # This is the SQL statement
    # Hence the "&"
    rows_tuple = session.execute(stmt)
    # acts like [(Task(id, title, ...),),] (this is a result object though, not indexable)
    # print would result <sqlalchemy.engine.result.Result object at 0x...>
    
    # Each row becomes a tuple item
    # and the entire tuple item is a single row, but each tuple item is a column of this row
    # Example:
    # [("A", "B", "C"), ]
    # "A", "B", "C" would be a row and "A" would be a column (1st) as well as "B" and "C" (3rd)

    rows_scalared = rows_tuple.scalars()
    # scalars turn the tuple of rows into iterator (ScalarResult object) of the first column
    # of each row, not a list nor a dict, but an iterator
    # acts like [ Task(id, title, ...), ]
    task_data = rows_scalared.first()
    # First item of the iteration. Since there is only one, it will give that. (None if not)
    return task_data


def operation_create_task(
    task,
    decoded_token_data: dict,
    session: Session
):
    task_info = Task(
        title = task.title,
        description = task.description,
        is_checked = task.is_checked,
        owner_user_id = decoded_token_data["sub"]
    )
    session.add(task_info)
    session.commit()

    return {
        "id": task_info.id,
        "title": task_info.title,
        "description": task_info.description,
        "is_checked": task_info.is_checked,
        "owner_user_id": task_info.owner_user_id
    }


def operation_get_task_list(
    decoded_token_data: dict,
    page: int, 
    limit: int,
    session: Session
):
    
    stmt = select(Task).where(Task.owner_user_id == decoded_token_data["sub"])
    task_list = session.execute(stmt).scalars().all()
    # we already know what .scalars() does, so we are with something that behaves like this:
    # [ Task(...), Task(...), Task(...),] after .scalars()
    # So what the .all() do?
    # It makes the ScalarResult object actually indexable. It returns a list.

    if limit and page:
        return {
            "Data": task_list[limit * page - limit : limit * page],
            "page": page,
            "limit": limit,
            "total": len(task_list),
        }
    return {
        "Data": task_list,
        "page": None,
        "limit": None,
        "total": len(task_list),
    }
    # Page 1, Limit 10:
    #          (0)         -     )10(
    # (limit*page - limit) - (limit*page)
    # Page 2, Limit 10:
    #         (10)        -     )20(
    # (limit*page -limit) - (limit*page)


def operation_get_single_task(
    task_id: int,
    decoded_token_data: dict,
    session
):

    task_data = get_task_data(task_id, decoded_token_data["sub"], session)
    if task_data is None:
        raise_forbidden_error()

    return task_data


def operation_update_task(
    task_id: int,
    task: object,
    decoded_token_data: dict,
    session: Session
):
    stmt = update(Task).where(
        (Task.id == task_id) & (Task.owner_user_id == decoded_token_data["sub"])
        ).values(
            title=task.title,
            description = task.description,
            is_checked=task.is_checked)
    
    session.execute(stmt)
    session.commit()

    task_data = get_task_data(task_id, decoded_token_data["sub"], session)
    if task_data is None:
        raise_forbidden_error()

    return task_data


def operation_delete_task(
    task_id: int,
    decoded_token_data: dict,
    session: Session
):
    
    stmt = select(Task).where(
        (Task.id == task_id) & (Task.owner_user_id == decoded_token_data["sub"])
        )
    task_data = session.execute(stmt).scalars().first()
    # .first(): Returns the task object if found, None if not.
    if task_data is None:
        # PEP 8 recommends using is for None instead of == because it is a singleton
        # As a singletone, there in only one "None" in the universe of python.
        # This is called identity comparison
        raise_forbidden_error()
    stmt = delete(Task).where(
        (Task.id == task_id) & (Task.owner_user_id == decoded_token_data["sub"])
        )
    session.execute(stmt)
    session.commit()
    raise_no_content()
