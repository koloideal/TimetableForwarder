import os
import re
from os import path
import aiohttp
from aiocache import cached
from aiocache.serializers import PickleSerializer

from findlybot.database.database_models import UserConfig
from findlybot.database.dao.users_config_dao import UsersConfigDAO


@cached(ttl=5 * 60, serializer=PickleSerializer())
async def api_data_to_dump(api_json_data: dict,
                           requestor_username: str,
                           query_path_hash: str) -> dict:
    to_dump_data: dict = {}
    all_configs: UserConfig = UsersConfigDAO().get_all_configs(requestor_username)
    max_size: int = all_configs.max_size

    os.makedirs(f"local_data/images/{requestor_username}", exist_ok=True)

    for marketplace in api_json_data:
        marketplace_path = f"local_data/images/{requestor_username}/{query_path_hash}/{marketplace}"
        os.makedirs(marketplace_path, exist_ok=True)
        items: list = []
        for k, item in enumerate(api_json_data[marketplace]):
            if k <= int(max_size):
                res_item = item
                res_item["id"] = k
                res_item["name"] = re.sub(r"[ /\\]", "_", item["name"])
                items.append(res_item)

                if res_item["image"] != "images/placeholder.png" and not path.isfile(f"{marketplace_path}/{res_item['name']}.jpg"):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(item['image']) as response:
                            with open(f"{marketplace_path}/{res_item['name']}.jpg", "wb") as f:
                                f.write(await response.read())
            else:
                break
        to_dump_data[marketplace] = items

    return to_dump_data
