from database.db import get_connection
from tertiary.formatter import format_task_data, format_task_list
from tertiary.validation import raise_forbidden_error, raise_no_content


def get_task_data(cursor: object, task_id: int, owner_user_id: int):
    cursor.execute(
        "SELECT * FROM task_list WHERE id = ? AND owner_user_id = ?",
        (task_id, owner_user_id),
    )
    task_data = cursor.fetchall()
    return task_data


def operation_create_task(task: object, decoded_token_data: dict):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
            INSERT INTO task_list
            (title, description, is_checked, owner_user_id)
            VALUES (?, ?, ?, ?)
        """,
        (
            task.title,
            task.description,
            task.is_checked,
            decoded_token_data["sub"],
        ),
    )
    connection.commit()
    cursor.execute(
        """
            SELECT id FROM task_list
            WHERE title = ? AND description = ? AND is_checked = ? AND owner_user_id = ?
        """,
        (
            task.title,
            task.description,
            task.is_checked,
            decoded_token_data["sub"],
        ),
    )
    task_id = cursor.fetchall()[-1][-1]
    # first [-1]:
    #   some tasks may be the exact same,
    #   so their ids would also appear in the list
    # second [-1]:
    #   cursor.fetchall() returns a list (with all the columns that matched) of lists (all the
    #   fields that I asked it to select from the columns)
    # so with [-1][-1] I can get the last ID from the last column that matched
    #   (the one created recently)

    connection.close()

    return {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "is_checked": task.is_checked,
        "owner_user_id": decoded_token_data["sub"],
    }


def operation_get_task_list(decoded_token_data: dict, page: int, limit: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """SELECT * FROM task_list
        WHERE owner_user_id = ?""",
        (decoded_token_data["sub"],),
    )
    task_list = cursor.fetchall()
    connection.close()
    formatted_list = format_task_list(task_list)
    if limit and page:
        return {
            "Data": formatted_list[limit * page - limit : limit * page],
            "page": page,
            "limit": limit,
            "total": len(formatted_list),
        }
    return {
        "Data": formatted_list,
        "page": None,
        "limit": None,
        "total": len(formatted_list),
    }
    # Page 1, Limit 10:
    #          (0)         -     )10(
    # (limit*page - limit) - (limit*page)
    # Page 2, Limit 10:
    #         (10)        -     )20(
    # (limit*page -limit) - (limit*page)


def operation_get_single_task(task_id: int, decoded_token_data: dict):
    connection = get_connection()
    cursor = connection.cursor()

    task_data = get_task_data(cursor, task_id, decoded_token_data["sub"])
    connection.close()
    if len(task_data) == 0:
        raise_forbidden_error()

    return format_task_data(task_data[0])


def operation_update_task(task_id: int, task: object, decoded_token_data: dict):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
            UPDATE task_list
            SET title = ?, description = ?, is_checked = ?
            WHERE id = ? AND owner_user_id = ?
        """,
        (
            task.title,
            task.description,
            task.is_checked,
            task_id,
            decoded_token_data["sub"],
        ),
    )
    connection.commit()

    task_data = get_task_data(cursor, task_id, decoded_token_data["sub"])
    connection.close()
    if len(task_data) == 0:
        raise_forbidden_error()

    return format_task_data(task_data[0])


def operation_delete_task(task_id: int, decoded_token_data: dict):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
            SELECT * FROM task_list
            WHERE id = ? AND owner_user_id = ?
        """,
        (task_id, decoded_token_data["sub"]),
    )
    task_data = cursor.fetchall()
    if len(task_data) == 0:
        raise_forbidden_error()
    cursor.execute(
        "DELETE FROM task_list WHERE id = ? AND owner_user_id = ?",
        (task_id, decoded_token_data["sub"]),
    )
    connection.commit()
    connection.close()
    raise_no_content()
