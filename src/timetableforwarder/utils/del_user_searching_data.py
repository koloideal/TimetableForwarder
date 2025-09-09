import shutil
import os


async def del_user_searching_data(username: str) -> None:
    images_path = f"local_data/images/{username}"
    if os.path.isdir(images_path):
        shutil.rmtree(images_path, ignore_errors=True)

    products_data_path = f"local_data/products_data/{username}"
    if os.path.isdir(products_data_path):
        shutil.rmtree(products_data_path, ignore_errors=True)
