from findlybot.database.connect_to_database import DatabaseConnection
from findlybot.database.database_models import Admin
from findlybot.database.dto.admins_dto import AdminsDTO


class AdminsDAO:
    def __init__(self):
        self.database: DatabaseConnection = DatabaseConnection()

    def add_admin(self, admin: Admin) -> None:
        query: str = '''INSERT IGNORE INTO admins(username) VALUES(%s)'''
        with self.database as cursor:
            cursor.execute(query, (admin.username,))

        return

    def del_admin(self, username: str) -> None:
        query: str = '''DELETE FROM admins WHERE username = %s'''
        with self.database as cursor:
            cursor.execute(query, (username,))

        return

    def get_admins(self) -> list[Admin]:
        query: str = '''SELECT username FROM admins'''
        with self.database as cursor:
            cursor.execute(query)
            admins_data: list[tuple] = cursor.fetchall()

        return AdminsDTO.get_admins(admins_data=admins_data)
