from timetableforwarder.database.connect_to_database import DatabaseConnection
from timetableforwarder.database.database_models import User


class UsersDAO:
    def __init__(self):
        self.database: DatabaseConnection = DatabaseConnection()

    def user_to_database(self, user: User) -> None:
        query: str = '''INSERT IGNORE INTO users(user_id, first_name, username) VALUES(%s, %s, %s)'''
        with self.database as cursor:
            cursor.execute(query, (user.user_id, user.first_name, user.username))

        return
