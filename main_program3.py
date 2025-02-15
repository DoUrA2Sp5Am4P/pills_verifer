import os
import time
import pygame
import serial
import json
import argparse
import numpy as np
import pygame.camera
from pyzbar.pyzbar import decode
from PIL import Image
import atexit
pygame.init()
pygame.camera.init()

camera_list = pygame.camera.list_cameras()
camera = pygame.camera.Camera(camera_list[0])
camera.start()
BAUD_RATE = 9600
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
#ser = serial.Serial('COM11', 9600, timeout=1)
ser.read(ser.in_waiting)
def close_port():
    ser.close()
    pass

atexit.register(close_port)
pygame.init()
pygame.mixer.init()
def read_nextion_button():
    """
    Считывает данные с дисплея Nextion и определяет, была ли нажата кнопка.
    
    Аргументы:
    - serial_port: объект serial.Serial, настроенный для связи с Nextion.

    Возвращает:
    - Идентификатор нажатой кнопки (если кнопка нажата), иначе None.
    """
    # Ожидание данных от дисплея
    if ser.in_waiting > 0:
        # Считываем все доступные байты
        data = ser.read(ser.in_waiting)
        # Удаляем байты конца и декодируем данные
        command = data.decode('latin1')
        return command
    return ""
def insert_r(text, chunk_size=20):
    # Разбиваем текст на строки
    lines_of_text = text.split("\n")
    lines = []
    for line_of_text in lines_of_text:
        current_line = []
        words = line_of_text.split()  # Разбиваем каждую строку на слова
        for word in words:
            # Проверяем, если добавление слова превышает максимальную длину,
            # сохранение текущей строки и сброс текущей линии
            if sum(len(w) for w in current_line) + len(word) + len(current_line) > chunk_size:
                lines.append(' '.join(current_line))  # Добавляем текущую строку в результат
                current_line = [word]  # Начинаем новую строку с текущим словом
            else:
                current_line.append(word)  # Добавляем слово в текущую строку

        # Добавляем оставшиеся слова после обработки строки
        if current_line:
            lines.append(' '.join(current_line))  # Сохраняем последнюю строку
    return lines
    
def convert_to_nextion_encoding(text):
    conversion_map = {
        'а': b'\xD0', 'б': b'\xD1', 'в': b'\xD2', 'г': b'\xD3', 'д': b'\xD4', 'е': b'\xD5', 'ё': b'\xF1',
        'ж': b'\xD6', 'з': b'\xD7', 'и': b'\xD8', 'й': b'\xD9', 'к': b'\xDA', 'л': b'\xDB', 'м': b'\xDC',
        'н': b'\xDD', 'о': b'\xDE', 'п': b'\xDF', 'р': b'\xE0', 'с': b'\xE1', 'т': b'\xE2', 'у': b'\xE3',
        'ф': b'\xE4', 'х': b'\xE5', 'ц': b'\xE6', 'ч': b'\xE7', 'ш': b'\xE8', 'щ': b'\xE9', 'ъ': b'\xEA',
        'ы': b'\xEB', 'ь': b'\xEC', 'э': b'\xED', 'ю': b'\xEE', 'я': b'\xEF',
    }
    converted_bytes = b""
    for char in text:
        try:
            converted_bytes += conversion_map.get(char.lower(), char.encode('utf-8'))
        except:
            converted_bytes+=str.encode(char)
    return converted_bytes
def send_command(command):
    if isinstance(command, str):
        command = command.encode('utf-8')
    command += b'\xff\xff\xff'
    ser.write(command)
def send_text_to_nextion(text, field_name,znak):
    encoded_text = convert_to_nextion_encoding(text)
    command = f'{field_name}.txt{znak}"{encoded_text.decode("latin1")}"'.encode("latin1")
    send_command(command)
    ser.write(b'\x74\x31\x2E\x74\x78\x74\x3D\x74\x31\x2E\x74\x78\x74\x2B\x22\x5C\x72\x22\xff\xff\xff')
    time.sleep(0.1)
def send_font_to_nextion():
    command = f't0.font=2'.encode("latin1")
    send_command(command)
    time.sleep(0.1)
def change_page(page_number):
    """
    Функция для смены страницы на Nextion.
    page_number - номер страницы (например, 1, 2, 3 и т.д.)
    """
    command = f"page {page_number}"
    send_command(command)
    print(f"Переход на страницу {page_number}")
while True:
    # Основной цикл программы
    previous_qr_code = ""
    button_qr_code=""         
    change_page("language")
    lang=""
    while True:
        command = read_nextion_button().replace(" ", "")
        if len(command)>0:
            lang=command
            break
    print(lang)
    if lang=="english":
        change_page("scan_e")
    else:
        change_page("scan_r")
    while True:
        restart=False
        while True:
            instruction_file = f"./medicines_text/{lang}/instructions/instruction_"+button_qr_code+".txt"
            contraindication_file = f"./medicines_text/{lang}/contraindications/contraindication_"+button_qr_code+".txt"
            if os.path.exists(instruction_file) and os.path.exists(contraindication_file):
                command = read_nextion_button().replace(" ", "")
                if len(command)>0:
                    empty_string=""
                    print("'"+command+"'")
                    if command == "button_instruction_pressed":
                        with open(instruction_file, 'r',encoding='utf-8') as file:
                            instruction_text = file.read().strip()
                        send_text_to_nextion(empty_string.encode('utf-8').decode('utf-8'),"t1","=")
                        for chunk in insert_r(instruction_text.encode('utf-8').decode('utf-8')):
                            send_text_to_nextion(chunk,"t1.txt=t1","+") 
                    if command == "button_contraindication_pressed":   
                        with open(contraindication_file, 'r',encoding='utf-8') as file:
                            contraindication_text = file.read().strip()
                        send_text_to_nextion(empty_string.encode('utf-8').decode('utf-8'),"t1","=")
                        for chunk in insert_r(contraindication_text.encode('utf-8').decode('utf-8')):
                            send_text_to_nextion(chunk,"t1.txt=t1","+")
                    if command=="restart":
                        restart=True
            camera_frame = camera.get_image()
            strFormat = 'RGBA'
            raw_str = pygame.image.tostring(camera_frame, strFormat, False)
            image = Image.frombytes(strFormat, camera_frame.get_size(), raw_str)
            clean_im = cv2.medianBlur(image, 25)
            small_clean_im = cv2.resize(clean_im, (512, 512), interpolation=cv2.INTER_AREA)
            qr_code = decode(small_clean_im, symbols=[ZBarSymbol.QRCODE])
            if len(qr_code)!=0:
                break
        if restart:
            break
        if previous_qr_code==qr_code[0].data.decode('ascii'):
            continue
        previous_qr_code=qr_code[0].data.decode('ascii')
        if qr_code:
            button_qr_code=qr_code[0].data.decode('ascii')
            name_file = f"./medicines_text/{lang}/names/name_"+qr_code[0].data.decode('ascii')+".txt"
            dosage_file = f"./medicines_text/{lang}/dosages/dosage_"+qr_code[0].data.decode('ascii')+".txt"
            print(name_file)
            if os.path.exists(name_file) and os.path.exists(dosage_file):
                if lang=="english":
                    change_page("information_e")
                else:
                    change_page("information_r")
                with open(name_file, 'r',encoding='utf-8') as file:
                    name_text = file.read().strip()
                with open(dosage_file, 'r',encoding='utf-8') as file:
                    dosage_text = file.read().strip()
                if len(name_text)>20:
                    send_font_to_nextion()
                send_text_to_nextion(name_text.encode('utf-8').decode('utf-8'),"t0","=")
                for chunk in insert_r(dosage_text.encode('utf-8').decode('utf-8')):
                    send_text_to_nextion(chunk,"t1.txt=t1","+")
            else:
                if lang=="english":
                    change_page("error_e")
                else:
                    change_page("error_r")
