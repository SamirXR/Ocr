# OCR


Join [Discord Server](https://discord.gg/P9gGZaXWGR) for any Assist/Issues or Testing it!

If You like My OpenSource Work you can Support : https://www.buymeacoffee.com/samir.xr

This will be Solely used for Hosting and Future Improvements.


# Prerequisites

- A Google Colab Account : [Click here](https://colab.google/)

# Install These Requirements

```python
!sudo apt-get update
!sudo apt install tesseract-ocr
!sudo apt-get install tesseract-ocr-all
!pip install PyPDF2
!pip install pytesseract
!pip install pdf2image
!pip install fpdf
!pip install aiohttp
!sudo apt-get install -y poppler-utils
```

# After sucessfully executing Paste this in the Cell


```python
import os
import aiohttp
import asyncio
import PyPDF2
import pytesseract
from PIL import Image
from io import BytesIO
from pdf2image import convert_from_path
import nest_asyncio
import json

nest_asyncio.apply()

async def fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

async def ocr_from_file(file_path, lang='eng'):
    if os.path.exists(file_path):
        if file_path.endswith('.pdf'):
            images = convert_from_path(file_path)
            text = ''
            for i in range(len(images)):
                text += pytesseract.image_to_string(images[i], lang=lang)
            return json.dumps({'text': text})
        else:
            img = Image.open(file_path)
            config = f'-l {lang}'
            text = pytesseract.image_to_string(img, config=config)
            return json.dumps({'text': text})
    else:
        return json.dumps({'error': 'File does not exist'})

async def ocr_from_url_or_file(input, lang='eng'):
    if input.startswith('http://') or input.startswith('https://'):
        response = await fetch_content(input)
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
    else:
        return await ocr_from_file(input, lang)

response = asyncio.get_event_loop().run_until_complete(ocr_from_url_or_file('/content/social.webp', 'eng'))
response_dict = json.loads(response)
if 'text' in response_dict:
    print(response_dict['text'])
else:
    print(response_dict['error'])
```



# Usage

```python
response = asyncio.get_event_loop().run_until_complete(ocr_from_url_or_file('/content/social.webp', 'eng'))
response_dict = json.loads(response)
if 'text' in response_dict:
    print(response_dict['text'])
else:
    print(response_dict['error'])
```


# Usage (Output in PDF Format)
```python
from fpdf import FPDF
from google.colab import files

# For URL
response = asyncio.get_event_loop().run_until_complete(ocr_from_url_or_file('https://cdn.discordapp.com/attachments/1095065755017552096/1176800366973689866/image.png', 'eng'))
response_dict = json.loads(response)
if 'text' in response_dict:
    print(response_dict['text'])
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=response_dict['text'])
    pdf.output("output.pdf")
    files.download('output.pdf')
else:
    print(response_dict['error'])
```

# Supported Languages

| Code          | Language                                |
|---------------|-----------------------------------------|
| afr           | Afrikaans                               |
| amh           | Amharic                                 |
| ara           | Arabic                                  |
| asm           | Assamese                                |
| aze           | Azerbaijani                             |
| aze_cyrl      | Azerbaijani - Cyrillic                  |
| bel           | Belarusian                              |
| ben           | Bengali                                 |
| bod           | Tibetan                                 |
| bos           | Bosnian                                 |
| bul           | Bulgarian                               |
| cat           | Catalan; Valencian                      |
| ceb           | Cebuano                                 |
| ces           | Czech                                   |
| chi_sim       | Chinese - Simplified                    |
| chi_tra       | Chinese - Traditional                   |
| chr           | Cherokee                                |
| cos           | Corsican                                |
| cym           | Welsh                                   |
| dan           | Danish                                  |
| deu           | German                                  |
| div           | Divehi; Dhivehi; Maldivian;             |
| dzo           | Dzongkha                                |
| ell           | Greek, Modern (1453-)                   |
| eng           | English                                 |
| enm           | English, Middle (1100-1500)             |
| epo           | Esperanto                               |
| est           | Estonian                                |
| eus           | Basque                                  |
| fas           | Persian                                 |
| fin           | Finnish                                 |
| fra           | French                                  |
| frk           | Frankish                                |
| frm           | French, Middle (ca.1400-1600)           |
| gle           | Irish                                   |
| glg           | Galician                                |
| grc           | Greek, Ancient (-1453)                  |
| guj           | Gujarati                                |
| hat           | Haitian; Haitian Creole                 |
| heb           | Hebrew (modern)                         |
| hin           | Hindi                                   |
| hrv           | Croatian                                |
| hun           | Hungarian                               |
| hye           | Armenian                                |
| iku           | Inuktitut                               |
| ind           | Indonesian                              |
| isl           | Icelandic                               |
| ita           | Italian                                 |
| ita_old       | Italian - Old                           |
| jav           | Javanese                                |
| jpn           | Japanese                                |
| kan           | Kannada                                 |
| kat           | Georgian                                |
| kat_old       | Georgian - Old                          |
| kaz           | Kazakh                                  |
| khm           | Central Khmer                           |
| kir           | Kirghiz, Kyrgyz                         |
| kor           | Korean                                  |
| kur           | Kurdish                                 |
| lao           | Lao                                     |
| lat           | Latin                                   |
| lav           | Latvian                                 |
| lit           | Lithuanian                              |
| mal           | Malayalam                               |
| mar           | Marathi                                 |
| mkd           | Macedonian                              |
| mlt           | Maltese                                 |
| msa           | Malay                                   |
| mya           | Burmese                                 |
| nep           | Nepali                                  |
| nld           | Dutch                                   |
| nor           | Norwegian                               |
| ori           | Oriya                                   |
| pan           | Panjabi, Punjabi                        |
| pol           | Polish                                  |
| por           | Portuguese                              |
| pus           | Pushto, Pashto                          |
| ron           | Moldavian, Moldovan                     |
| rus           | Russian                                 |
| san           | Sanskrit (Saṁskṛta)                    |
| sin           | Sinhala, Sinhalese                      |
| slk           | Slovak                                  |
| slv           | Slovene                                 |
| spa           | Spanish; Castilian                      |
| spa_old       | Spanish; Castilian - Old                |
| sqi           | Albanian                                |
| srp           | Serbian                                 |
| srp_latn      | Serbian - Latin                         |
| swa           | Swahili                                 |
| swe           | Swedish                                 |
| syr           | Syriac                                  |
| tam           | Tamil                                   |
| tel           | Telugu                                  |
| tgk           | Tajik                                  |
| tgl           | Tagalog                                |
| tha           | Thai                                   |
| tir           | Tigrinya                               |
| tur           | Turkish                                |
| uig           | Uighur, Uyghur                         |
| ukr           | Ukrainian                              |
| urd           | Urdu                                   |
| uzb           | Uzbek                                  |
| uzb_cyrl      | Uzbek - Cyrillic                        |
| vie           | Vietnamese                             |
| yid           | Yiddish                                |
