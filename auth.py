users = {}

def register(username, password):
    if username in users:
        return False
    users[username] = password
    return True

def login(username, password):
    return users.get(username) == password
