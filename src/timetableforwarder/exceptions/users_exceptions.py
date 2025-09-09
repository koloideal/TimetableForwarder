class InvalidUsernameForBan(Exception):
    def __init__(self, invalid_username: str) -> None:
        self.__invalid_username: str = invalid_username

    def __str__(self) -> str:
        return f"Invalid username for ban: {self.__invalid_username}"


class AttemptToBanAdminOrCreator(Exception):
    def __init__(self, invalid_username: str) -> None:
        self.__invalid_username: str = invalid_username

    def __str__(self) -> str:
        return f"You can't ban a '{self.__invalid_username}' since he is an admin or creator"


class InvalidUsernameForAddAdmin(Exception):
    def __init__(self, invalid_username: str) -> None:
        self.__invalid_username: str = invalid_username

    def __str__(self) -> str:
        return f"Invalid username for add admin: {self.__invalid_username}"
