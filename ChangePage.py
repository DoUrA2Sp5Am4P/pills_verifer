import serial
import time

# Настройки порта (укажите ваш порт, например, 'COM3' для Windows или '/dev/ttyUSB0' для Linux)
PORT = 'COM11'  # Замените на свой порт
BAUD_RATE = 9600  # Скорость порта для Nextion, обычно 9600

# Инициализация последовательного соединения
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

def send_command(command):
    """
    Функция для отправки команды на Nextion.
    Команда должна быть в виде строки, например 'page 1'
    """
    # Преобразуем команду в байты и добавляем завершающие символы 0xFF 0xFF 0xFF
    command_bytes = command.encode('utf-8') + b'\xff\xff\xff'
    ser.write(command_bytes)
    time.sleep(0.1)  # Задержка для стабильности

def change_page(page_number):
    """
    Функция для смены страницы на Nextion.
    page_number - номер страницы (например, 1, 2, 3 и т.д.)
    """
    command = f"page {page_number}"
    send_command(command)
    print(f"Переход на страницу {page_number}")

# Пример смены страницы
try:
    change_page(1)  # Переход на страницу 1
finally:
    ser.close()  # Закрытие порта
