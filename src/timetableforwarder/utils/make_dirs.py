import os


def make_dirs() -> None:
    paths = (
        "local_data",
        "local_data/images",
        "secret_data"
    )

    for path in paths:
        os.makedirs(path, exist_ok=True)
        