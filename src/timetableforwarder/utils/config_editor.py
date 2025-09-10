from pathlib import Path
import tomli
import tomli_w


CONFIG_PATH = Path("secret_data/config.toml")


def read_config() -> dict:
    with open(CONFIG_PATH, "rb") as f:
        return tomli.load(f)


def write_config(data: dict) -> None:
    with open(CONFIG_PATH, "wb") as f:
        tomli_w.dump(data, f)


def remove_group(group_id: int) -> bool:
    data = read_config()
    groups = data.get("groups", {}).get("list", [])
    if group_id not in groups:
        return False
    groups = [g for g in groups if g != group_id]
    data["groups"]["list"] = groups
    write_config(data)
    return True


def add_group(group_id: int) -> bool:
    data = read_config()
    groups = data.setdefault("groups", {}).setdefault("list", [])
    if group_id in groups:
        return False
    groups.append(group_id)
    groups.sort()
    write_config(data)
    return True


