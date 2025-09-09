from timetableforwarder.database.database_models import BannedUser


class BannedUsersDTO:
    @staticmethod
    def get_admins(banned_users_data: list[tuple]) -> list[BannedUser]:
        banned_users: list[BannedUser] = [
            BannedUser(username=banned_user[0]) for banned_user in banned_users_data
        ]

        return banned_users
