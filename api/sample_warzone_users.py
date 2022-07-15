real_users = [
    ("clutchbelk#3571595", "acti"),
    ("truegamedata#1375", "battle"),
    ("Bojo704", "psn"),
]


def get_users_list():
    return [{"username": uname, "platform": plat} for (uname, plat) in real_users]


def get_a_user():
    user = {"username": "", "platform": ""}
    user["username"], user["platform"] = real_users[0]
    return user
