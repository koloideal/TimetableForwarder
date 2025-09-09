from findlybot.database.connect_to_database import DatabaseConnection


class InitializeDatabaseDAO:
    def __init__(self):
        self.database: DatabaseConnection = DatabaseConnection()

    def create_tables(self) -> None:
        table_create_queries: list[str] = ['''CREATE TABLE IF NOT EXISTS users_config(username VARCHAR(50) NOT NULL UNIQUE, only_new VARCHAR(3), max_size INTEGER, name_filter VARCHAR(3), price_filter VARCHAR(3), language VARCHAR(2))''',
                                           '''CREATE TABLE IF NOT EXISTS users(user_id INTEGER NOT NULL UNIQUE, first_name VARCHAR(50), username VARCHAR(50))''',
                                           '''CREATE TABLE IF NOT EXISTS banned_users(username VARCHAR(50) NOT NULL)''',
                                           '''CREATE TABLE IF NOT EXISTS admins(username VARCHAR(50) NOT NULL)''']
        with self.database as cursor:
            for table_create_query in table_create_queries:
                cursor.execute(table_create_query)

        return

