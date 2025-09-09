from findlybot.database.connect_to_database import DatabaseConnection
from findlybot.database.database_models import BannedUser
from findlybot.database.dto.banned_users_dto import BannedUsersDTO


class BannedUsersDAO:
    def __init__(self):
        self.database: DatabaseConnection = DatabaseConnection()

    def get_banned_users(self) -> list[BannedUser]:
        query: str = '''SELECT username FROM banned_users'''
        with self.database as cursor:
            cursor.execute(query)
            banned_users_data: list[tuple] = cursor.fetchall()

        return BannedUsersDTO.get_admins(banned_users_data=banned_users_data)

    def ban_user(self, banned_user: BannedUser) -> None:
        query: str = '''INSERT IGNORE INTO banned_users(username) VALUES(%s)'''
        with self.database as cursor:
            cursor.execute(query, (banned_user.username,))
        return

    def unban_user(self, username: str) -> None:
        query: str = '''DELETE FROM banned_users WHERE username = %s'''
        with self.database as cursor:
            cursor.execute(query, (username,))

        return
