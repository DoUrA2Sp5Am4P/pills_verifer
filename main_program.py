import os
import time
import pygame
import sounddevice as sd
from scipy.io.wavfile import write
import cv2
import serial
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
import wave
import json
from qreader import QReader
import argparse
import numpy as np
from difflib import SequenceMatcher
parser = argparse.ArgumentParser(
                    prog='Medicine',
                    description='Medicine',
                    epilog='Medicine')
parser.add_argument('-p', '--port') #Важно указывать аргументы
args = parser.parse_args()
# Настройки порта (укажите ваш порт, например, 'COM3' для Windows или '/dev/ttyUSB0' для Linux)
PORT = args.port  # Замените на свой порт
BAUD_RATE = 9600  # Скорость порта для Nextion, обычно 9600
# Инициализация последовательного соединения
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
# Инициализация pygame для воспроизведения звуков
cam = cv2.VideoCapture(0)
pygame.init()
pygame.mixer.init()
def is_similar_to_contraindication(word, target_word="противопоказания", threshold=0.5):
    # Рассчитываем коэффициент схожести
    similarity = SequenceMatcher(None, word, target_word).ratio()
    return similarity >= threshold
def is_similar_to_instruction(word, target_word="инструкция", threshold=0.5):
    # Рассчитываем коэффициент схожести
    similarity = SequenceMatcher(None, word, target_word).ratio()
    return similarity >= threshold
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
def play_music(src):
    pygame.mixer.music.load(src)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

# Функция для записи голоса и распознавания команд
def listen_for_voice_or_button():
    # Читаем сигнал из Serial или слушаем микрофон
    duration = 5  # Длительность записи, секунд
    fs = 44100  # Частота дискретизации
    
    print("Запись звука...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1,dtype=np.int16)
    sd.wait()  # Ожидание завершения записи
    
    # Сохраняем временный файл записи
    temp_audio_path = './temp_python_files/temp_audio.wav'
    write(temp_audio_path, fs, audio_data)
    
    # Отправляем файл в recognite() и удаляем временный файл
    command_text = recognite(temp_audio_path)
    os.remove(temp_audio_path)
    com=read_nextion_button()
    if len(com)>0:
        command_text=com
    return command_text
def insert_r(text, chunk_size=20):
    # Создаем пустой список для хранения частей текста
    chunks = []
    
    # Проходим по тексту с шагом chunk_size
    for i in range(0, len(text), chunk_size):
        # Добавляем подстроку длиной chunk_size в список
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks
def convert_to_nextion_encoding(text):
    conversion_map = {
        'а': b'\xD0', 'б': b'\xD1', 'в': b'\xD2', 'г': b'\xD3', 'д': b'\xD4', 'е': b'\xD5', 'ё': b'\xF1',
        'ж': b'\xD6', 'з': b'\xD7', 'и': b'\xD8', 'й': b'\xD9', 'к': b'\xDA', 'л': b'\xDB', 'м': b'\xDC',
        'н': b'\xDD', 'о': b'\xDE', 'п': b'\xDF', 'р': b'\xE0', 'с': b'\xE1', 'т': b'\xE2', 'у': b'\xE3',
        'ф': b'\xE4', 'х': b'\xE5', 'ц': b'\xE6', 'ч': b'\xE7', 'ш': b'\xE8', 'щ': b'\xE9', 'ъ': b'\xEA',
        'ы': b'\xEB', 'ь': b'\xEC', 'э': b'\xED', 'ю': b'\xEE', 'я': b'\xEF'
    }
    converted_bytes = b""
    for char in text:
        converted_bytes += conversion_map.get(char.lower(), char.encode('utf-8'))
    return converted_bytes

# Функция отправки команды на Nextion
def send_command(command):
    # Добавляем завершающие байты для Nextion
    if isinstance(command, str):
        command = command.encode('utf-8')
    command += b'\xff\xff\xff'
    ser.write(command)
    time.sleep(0.1)  # Задержка для стабильности соединения

# Основная функция для отправки текста на Nextion
def send_text_to_nextion(text, field_name,znak):
    # Конвертируем текст в байт-коды Nextion
    encoded_text = convert_to_nextion_encoding(text)
    
    # Формируем команду для отправки текста в нужное текстовое поле на экране
    command = f'{field_name}.txt{znak}"{encoded_text.decode("latin1")}"'.encode("latin1")
    send_command(command)
    ser.write(b'\x74\x31\x2E\x74\x78\x74\x3D\x74\x31\x2E\x74\x78\x74\x2B\x22\x5C\x72\x22\xff\xff\xff')
    time.sleep(0.1)
def change_page(page_number):
    """
    Функция для смены страницы на Nextion.
    page_number - номер страницы (например, 1, 2, 3 и т.д.)
    """
    command = f"page {page_number}"
    send_command(command)
    print(f"Переход на страницу {page_number}")
def convert_to_wav(input_file, output_file):
    try:
        sound = AudioSegment.from_mp3(input_file)
        sound.set_channels(1)
        sound = sound.set_frame_rate(16000)                
        sound = sound.set_channels(1)    
        sound.export(output_file, format="wav")
    except:
        print("Error")
def recognite(input_audio): # Пример использования
    output_audio = "./temp_python_files/output.wav"
    convert_to_wav(input_audio, output_audio)
    # Путь к скачанной модели
    MODEL_PATH = "./vosk-model-small-ru-0.22/"  # Замените на путь к вашей модели
    AUDIO_PATH = input_audio  # Замените на путь к вашему аудиофайлу

    # Загрузка модели
    print("Загрузка модели...")
    model = Model(MODEL_PATH)

    # Открытие аудиофайла
    with wave.open(AUDIO_PATH, "rb") as wf:
        # Проверка параметров аудиофайла (моно, 16 kHz)
        #if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        #    raise ValueError("Аудиофайл должен быть WAV, 16 kHz, моно.")

        # Создаем распознаватель
        recognizer = KaldiRecognizer(model, wf.getframerate())

        # Переменная для хранения результата
        result_text = ""

        print("Распознавание началось...")
        # Чтение аудиофайла блоками и распознавание
        while True:
            data = wf.readframes(4000)  # Чтение фреймов
            if len(data) == 0:  # Если файл дочитан
                break
            if recognizer.AcceptWaveform(data):  # Промежуточные результаты
                result = json.loads(recognizer.Result())
                result_text += result.get("text", "") + " "

        # Получение финального результата
        final_result = json.loads(recognizer.FinalResult())
        result_text += final_result.get("text", "")

        print("Распознанный текст:")
        print("'",result_text,"'")
        return result_text
# Основной цикл программы
var_stop_m=0
change_page("scan")
play_music('./main/hello.wav')
try:
    # Открываем файл в режиме чтения
    with open('./first_start/first_start.txt', 'r') as file:
        # Читаем первую строку
        first_line = file.readline().strip()  # Удаляем пробелы по краям
        # Проверяем, равна ли первая строка '1'
        if first_line == '1':
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            time.sleep(0.5)
            play_music('./main/first_start.wav')
        with open('./first_start/first_start.txt', 'w') as file_write:
                file_write.write('0')   
except FileNotFoundError:
    print("Файл не найден.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
previous_qr_code = None
while True:
    # Шаг 2. Сканирование QR-кода
    qr_code = ""  # Получаем QR-код (например, "123")
    if var_stop_m==1:
        # Шаг 3. Остановка музыки
        stop_music()
    var_stop_m=1
    # Шаг 4. Смена экрана на "scan"
    start = time.time()
    # Create a QReader instance
    qreader = QReader()
    # Open the default camera
    while True:
        ret, frame = cam.read()
        while ret!=True:
            print("Ошибка")
            ret, frame = cam.read()
        #cv2.imwrite('./temp_python_files/captured_frame.png', frame)
        # Write the frame to the output file
        # Get the image that contains the QR code
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Use the detect_and_decode function to get the decoded QR data
        qr_code = qreader.detect_and_decode(image=image)   
        if len(qr_code)!=0:
            stop_music
            qr_code=qr_code[0]
            break

    # Шаг 5. Проверка результата сканирования
    if qr_code:
        # Шаг 5.1. Проверка существования файла
        name_file = f'./medicines_text/names/name_{qr_code}.txt'
        dosage_file = f'./medicines_text/dosages/dosage_{qr_code}.txt'
        print(name_file)
        
        if os.path.exists(name_file) and os.path.exists(dosage_file):
            # Если файл существует, смена экрана на "information"
            change_page("information")
            
            # Шаг 5.2. Отправка текста на дисплей
            with open(name_file, 'r') as file:
                name_text = file.read().strip()
            with open(dosage_file, 'r') as file:
                dosage_text = file.read().strip()
                
            # Отправляем текст на дисплей
            send_text_to_nextion(name_text.encode('cp1251').decode('utf-8'),"t0","=")
            for chunk in insert_r(dosage_text.encode('cp1251').decode('utf-8')):
                send_text_to_nextion(chunk,"t1.txt=t1","+")
            # Шаг 5.4. Воспроизведение звуков по очереди
            play_music('./main/name.wav')
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            time.sleep(0.5)
            play_music(f'./medicines_audio/names/name_{qr_code}.wav')
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            time.sleep(1)
            play_music('./main/dosage.wav')
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            time.sleep(0.5)
            play_music(f'./medicines_audio/dosages/dosage_{qr_code}.wav')
            # Шаг 5.5. Проверка событий
            while True:
                qreader = QReader()
                # Open the default camera
                ret, frame = cam.read()
                cv2.imwrite('./temp_python_files/captured_frame.png', frame)
                # Write the frame to the output file
                # Get the image that contains the QR code
                image = cv2.cvtColor(cv2.imread("./temp_python_files/captured_frame.png"), cv2.COLOR_BGR2RGB)
                # Use the detect_and_decode function to get the decoded QR data
                new_qr_code = qreader.detect_and_decode(image=image)
                # Проверка на новый QR-код
                if new_qr_code!=():
                    if new_qr_code[0] != qr_code:
                        previous_qr_code = qr_code
                        break
                # Проверка на нажатие кнопки или голосовую команду
                command = listen_for_voice_or_button().replace(" ", "")
                print("'"+command+"'")
                if command == "button_instruction_pressed" or is_similar_to_instruction(command) or command == "Инструкция" or str(command).startswith("Ин") or str(command).endswith("ция"):
                    print("OK")
                    stop_music()
                    play_music(f'./medicines_audio/instructions/instruction_{qr_code}.wav')
                elif command == "button_contraindication_pressed" or is_similar_to_contraindication(command) or command == "Противопоказания" or str(command).startswith("Пр") or str(command).endswith("ния"):
                    stop_music()
                    play_music(f'./medicines_audio/contraindications/contraindication_{qr_code}.wav')
        
        else:
            # Если файл не найден, смена экрана на "error" и воспроизведение ошибки
            change_page("error")
            play_music('./main/not_found.wav')
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
