import serial
import time

# Установите параметры порта
PORT = 'COM11'  # Замените на ваш порт, например 'COM3' для Windows или '/dev/ttyUSB0' для Linux
BAUD_RATE = 9600  # Скорость соединения (обычно 9600 для Nextion)
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

# Функция конвертации текста в байт-коды Nextion
def convert_to_nextion_encoding(text):
    conversion_map = {
        'а': b'\xD0', 'б': b'\xD1', 'в': b'\xD2', 'г': b'\xD3', 'д': b'\xD4', 'е': b'\xD5', 'ё': b'\xF1',
        'ж': b'\xD6', 'з': b'\xD7', 'и': b'\xD8', 'й': b'\xD9', 'к': b'\xDA', 'л': b'\xDB', 'м': b'\xDC',
        'н': b'\xDD', 'о': b'\xDE', 'п': b'\xDF', 'р': b'\xE0', 'с': b'\xE1', 'т': b'\xE2', 'у': b'\xE3',
        'ф': b'\xE4', 'х': b'\xDA', 'ц': b'\xE6', 'ч': b'\xE7', 'ш': b'\xE8', 'щ': b'\xE9', 'ъ': b'\xEA',
        'ы': b'\xEB', 'ь': b'\xEC', 'э': b'\xED', 'ю': b'\xEE', 'я': b'\xEF'
    }
    converted_bytes = b""
    for char in text:
        converted_bytes += conversion_map.get(char.lower(), char.encode('utf-8'))
    return converted_bytes

# Функция отправки команды на Nextion
def send_command(command):
    # Преобразуем команду в байты, если это строка, и добавляем завершающие байты для Nextion
    if isinstance(command, str):
        command = command.encode('latin1')
    command += b'\xff\xff\xff'
    ser.write(command)
    time.sleep(0.1)  # Задержка для стабильности соединения

# Основная функция для отправки текста на Nextion
def send_text_to_nextion(text, field_name="t0"):
    # Конвертируем текст в байт-коды Nextion
    encoded_text = convert_to_nextion_encoding(text)
    
    # Формируем команду для отправки текста в нужное текстовое поле на экране
    command = f'{field_name}.txt="{encoded_text.decode("latin1")}"'.encode("latin1")
    send_command(command)

# Пример использования
text_to_send = "Пример текста2"
send_text_to_nextion(text_to_send, "t0")
print("Текст отправлен на Nextion.")
