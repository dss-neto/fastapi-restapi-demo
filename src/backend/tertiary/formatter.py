def format_user_data(user_data: list):
    formatted_user_data = {
        "id": user_data.id,
        "name": user_data.name,
        "email": user_data.email,
        "tasks": user_data.tasks
    }

    return formatted_user_data


def format_user_list(user_list: list):
    formatted_user_list = [format_user_data(user) for user in user_list]
    return formatted_user_list
