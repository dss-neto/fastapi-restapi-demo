def format_task_data(task_data: list):
    id, title, description, is_checked, _ = task_data
    if is_checked == 0:
        is_checked = "No"
    else:
        is_checked = "Yes"
    return {
        "id": id,
        "title": title,
        "description": description,
        "finished": is_checked,
    }


def format_task_list(task_list: list):
    formatted_task_list = []
    for task in task_list:
        formatted_task = format_task_data(task)
        formatted_task_list.append(
            {
                "id": formatted_task["id"],
                "title": formatted_task["title"],
                "description": formatted_task["description"],
                "finished": formatted_task["finished"],
            }
        )

    return formatted_task_list


def format_user_data(user_data: list):
    id, name, email, _ = user_data
    formatted_user_data = {
        "id": id,
        "name": name,
        "email": email,
    }

    return formatted_user_data


def format_user_list(user_list: list):
    formatted_user_list = []
    for user in user_list:
        formatted_user_list.append(format_user_data(user))

    return formatted_user_list
