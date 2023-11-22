!sudo apt install tesseract-ocr
!sudo apt-get install tesseract-ocr-all
!pip install PyPDF2
!pip install pytesseract
!pip install pdf2image
!pip install aiohttp
!sudo apt-get install -y poppler-utils

import aiohttp
import asyncio
import PyPDF2
import pytesseract
from PIL import Image
from io import BytesIO
from pdf2image import convert_from_path
import nest_asyncio
nest_asyncio.apply()
import json

async def fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

async def ocr_from_url(url, lang='eng'):
    response = await fetch_content(url)
    try:
        img = Image.open(BytesIO(response))
        config = f'-l {lang}'
        text = pytesseract.image_to_string(img, config=config)
        return json.dumps({'text': text})
    except:
        with open('temp.pdf', 'wb') as f:
            f.write(response)
        images = convert_from_path('temp.pdf')
        text = ''
        for i in range(len(images)):
            text += pytesseract.image_to_string(images[i], lang=lang)
        return json.dumps({'text': text})

response = asyncio.get_event_loop().run_until_complete(ocr_from_url('Image/PDF URL Here', 'eng'))
response_dict = json.loads(response)
print(response_dict['text'])
