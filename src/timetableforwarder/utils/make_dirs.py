import os


def make_dirs() -> None:
    paths = (
        "local_data/images",
    )

    for path in paths:
        os.makedirs(path, exist_ok=True)
