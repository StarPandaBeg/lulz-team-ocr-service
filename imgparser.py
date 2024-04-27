import cv2
import sys
import json
import pyocr
import enhance
from PIL import Image
from pymystem3 import Mystem
from g4f.client import Client



def gettext(image, tool_number = 0):

    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("OCR не найден. Убедитесь что он указан в перменной PATH")
        sys.exit(1)

    return tools[tool_number].image_to_string(
        image, lang='rus', builder=pyocr.builders.TextBuilder()
    )

def process_image(image_path):
    input_image = cv2.imread(enhance.set_image_dpi(image_path))
    input_image = enhance.remove_noise(input_image)
    adjusted_image = enhance.increase_contrast(input_image)
    adjusted_image = enhance.get_grayscale(input_image)
    return adjusted_image


def fix_spelling(text):
    # Создаем экземпляр Mystem
    mystem = Mystem()
    # Лемматизируем текст с помощью Mystem
    lemmas = mystem.lemmatize(text)
    # Собираем леммы обратно в текст
    corrected_text = ''.join(lemmas)
    return corrected_text

def parse_image(image_path):
    image = process_image(image_path)
    pil_image = Image.fromarray(image)
    text = gettext(pil_image, 0)
    return (text, fix_spelling(text))


def trim_json(s):
    brace_index = s.find('{')
    bracket_index = s.find('[')
    if brace_index == -1:
        brace_index = len(s)
    if bracket_index == -1:
        bracket_index = len(s)
    index = min(brace_index, bracket_index)
    s = s[index:]
    brace_end_index = s.rfind('}')
    bracket_end_index = s.rfind(']')
    if brace_end_index == -1:
        brace_end_index = len(s) + 1
    if bracket_end_index == -1:
        bracket_end_index = len(s) + 1
    index = max(brace_end_index, bracket_end_index)
    s = s[:index + 1]
    return s


client = Client()
def systemize(text, corrected_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""Hello!) I have ticket and scan it with two ocr tools.
                I have 2 different text but i need one for get parameters.
                Can you fix it please? text writed on russian language.
                First text: {text} and Second text: {corrected_text}
                write all parameters in JSON style ONLY only json object without ```.
                Адрес, Название организации, ИНН (контрагента), Приход/расход, ФН (фискальный номер),
                ФД (фискальный документ), ФП (фискальный признак), Дата, Сумма, Номер карты.
                Missing text set to null
                Example: 
                {{
                    "address": "",
                    "organisation_name": "",
                    "tin": "",
                    "income_expense": "",
                    "fn": "",
                    "fd": "",
                    "fp": "",
                    "date": "01.01.01 12:34:56",
                    "sum": "0.0",
                    "card_number": "0000 0000 0000 0000"
                }}. Response MUST have all fields (that may be null)."""
            }
        ],
    )
    return response.choices[0].message.content


def process(image_path):
    text, corrected_text = parse_image(image_path)
    return json.loads(systemize(text, corrected_text))