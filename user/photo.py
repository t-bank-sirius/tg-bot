import base64
from PIL import Image
from io import BytesIO


async def decode(base64_string: str):
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",", 1)[1]

    image_data = base64.b64decode(base64_string)
    buffer = BytesIO(image_data)
    buffer.name = "image.jpg"
    buffer.seek(0)
    
    return buffer


def encode_image_from_bytesio(buffer: BytesIO, format: str = 'JPEG') -> str:
    buffer.seek(0)
    image = Image.open(buffer)

    if image.mode in ("RGBA", "LA"):
        image = image.convert("RGB")

    encoded_io = BytesIO()
    image.save(encoded_io, format=format, quality=100, subsampling=0)
    encoded_io.seek(0)

    return f"data:image/{format.lower()};base64,{base64.b64encode(encoded_io.read()).decode('utf-8')}"
