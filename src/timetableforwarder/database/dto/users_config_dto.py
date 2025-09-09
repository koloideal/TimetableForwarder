from timetableforwarder.database.database_models import UserConfig


class UsersConfigDTO:
    @staticmethod
    def get_all_configs(config: tuple, username: str) -> UserConfig:
        user_config = UserConfig(
            username=username,
            only_new=config[0],
            max_size=config[1],
            language=config[2],
            price_filter=config[3],
            name_filter=config[4]
        )

        return user_config
