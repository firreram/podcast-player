from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, is_creator, userimg):
        self.id = id
        self.username= username
        self.password = password
        self.is_creator = is_creator
        self.userimg = userimg