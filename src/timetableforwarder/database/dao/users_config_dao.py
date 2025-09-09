from findlybot.database.connect_to_database import DatabaseConnection
from findlybot.database.database_models import UserConfig
from findlybot.database.dto.users_config_dto import UsersConfigDTO


class UsersConfigDAO:
    def __init__(self):
        self.database: DatabaseConnection = DatabaseConnection()

    def config_user_to_database(self, params: tuple) -> None:
        query: str = '''INSERT IGNORE INTO users_config(username, only_new, max_size, language, price_filter, name_filter) VALUES(%s, %s, %s, %s, %s, %s)'''
        with self.database as cursor:
            cursor.execute(query, params)

        return

    def change_only_new_config(self, only_new: str, username: str) -> None:
        query: str = '''UPDATE users_config SET only_new = %s WHERE username = %s'''
        with self.database as cursor:
            cursor.execute(query, (only_new, username))

    def change_name_filter_config(self, name_filter: str, username: str) -> None:
        query: str = '''UPDATE users_config SET name_filter = %s WHERE username = %s'''
        with self.database as cursor:
            cursor.execute(query, (name_filter, username))

        return

    def change_price_filter_config(self, price_filter: str, username: str) -> None:
        query: str = '''UPDATE users_config SET price_filter = %s WHERE username = %s'''
        with self.database as cursor:
            cursor.execute(query, (price_filter, username))

        return

    def change_lang_config(self, language: str, username: str) -> None:
        query: str = '''UPDATE users_config SET language = %s WHERE username = %s'''
        with self.database as cursor:
            cursor.execute(query, (language, username))

        return

    def get_all_configs(self, username: str) -> UserConfig:
        query: str = '''SELECT only_new, max_size, language, price_filter, name_filter FROM users_config WHERE username = %s'''
        with self.database as cursor:
            cursor.execute(query, (username,))
            config = cursor.fetchone()

        return UsersConfigDTO.get_all_configs(config=config, username=username)

    def change_max_size_config(self, username: str, max_size: int) -> None:
        query: str = '''UPDATE users_config SET max_size = %s WHERE username = %s'''
        with self.database as cursor:
            cursor.execute(query, (max_size, username))

        return
