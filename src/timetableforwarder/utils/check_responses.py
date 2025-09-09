import json
import os
import shutil
import typing

if typing.TYPE_CHECKING:
    from _typeshed import SupportsWrite, SupportsRead


async def check_responses(username: str) -> bool:
    if os.path.exists(f"local_data/images/{username}/responses.json"):
        with open(f"local_data/images/{username}/responses.json", "r") as file: # type: SupportsRead[str | bytes]
            responses: list[dict[str]] = json.load(file)["responses"]
    else:
        return False

    if len(responses) < 5:
        return False
    else:
        oldest_response = min(responses, key=lambda x: x["date"])
        data = json.load(open(f"local_data/images/{username}/responses.json", "r"))
        data["responses"].remove(oldest_response)

        with open(f"local_data/images/{username}/responses.json", "w") as file: # type: SupportsWrite[str]
            json.dump(data, file, indent=4)

        shutil.rmtree(f'local_data/images/{username}/{oldest_response['name']}', ignore_errors=True)
        os.remove(f'local_data/products_data/{username}/{oldest_response["name"]}.json')

        return True
