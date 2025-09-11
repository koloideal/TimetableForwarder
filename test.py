import asyncio
from pprint import pprint
from timetableforwarder.services.image_to_text import ImageToTextService

image_to_text_service = ImageToTextService(api_key="")

pprint(asyncio.run(image_to_text_service.converting_image_to_text("test.jpg")))