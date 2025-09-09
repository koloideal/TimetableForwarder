import os


def make_dirs() -> None:
    paths = (
        "database",
        "local_data/images",
        "local_data/products_data",
    )

    for path in paths:
        os.makedirs(path, exist_ok=True)
