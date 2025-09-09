from timetableforwarder.database.database_models import Admin


class AdminsDTO:
    @staticmethod
    def get_admins(admins_data: list[tuple]) -> list[Admin]:
        admins: list[Admin] = [
            Admin(username=admin[0]) for admin in admins_data
        ]

        return admins
