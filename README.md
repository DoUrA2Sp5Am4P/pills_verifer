# Верификатор таблеток

## Установка

1. Установите Python 3.11.9.
2. Клонируйте репозиторий.
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Установите **Распространяемые пакеты Visual C++ для Visual Studio 2013** (библиотеки `libconv.dll`) (только для Windows) по ссылке: [скачать здесь](https://www.microsoft.com/ru-ru/download/details.aspx?id=40784).
5. Клонируйте в папку с `main_program.py` репозиторий XTTS:
   ```bash
   git clone https://huggingface.co/coqui/XTTS-v2
   ```
6. Скачайте и распакуйте в папку с `main_program.py` VOSK (vosk-model-small-ru-0.22) по ссылке: [скачать здесь](https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip).
7. Скачайте и распакуйте в папку с `main_program.py` FFmpeg (ffmpeg-master-latest-win64-gpl) по ссылке: [скачать здесь](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip).
8. Запустите программу:
   ```bash
   python main_program.py
   ```
9. Скопируйте файл `./nextion/nextion_1.tft` на экран Nextion (карта памяти должна быть в формате FAT32).

## Как использовать

### Для генерации голоса

Планируется, что голос будет генерироваться не на Raspberry (так как он это делает долго), а на компьютере. Записи с названиями таблеток, инструкциями и противопоказаниями будут заранее храниться на Raspberry. 

1. Установите дополнительные зависимости:
   ```bash
   pip install -r requirements_for_tts.txt
   ```
2. Для генерации голоса используйте:
   ```bash
   generator.py --text "Таблетка" --output ./folder/name.wav
   ```

### Для распознавания таблеток

Если вы хотите тестировать на Windows, потребуется камера, микрофон, IDE Nextion, а также виртуальные Serial-порты (например, com0com). 

1. Запустите эмулятор (файл проекта `.hmi` хранится в папке `nextion`), затем подключите его к виртуальному порту.
2. Запустите программу:
   ```bash
   python main_program.py --port COM11
   ```
   На Raspberry используйте порт `/dev/Serial0`.

Если что-то не работает, попробуйте выполнить отдельные тесты:
- `ChangePage.py`
- `play.py`
- `qr.py`

Для установки на Raspberry изменения в программе не требуются, кроме указания порта. Используемые библиотеки:
- Для изображений: `cv2`
- Для вывода аудио: `pygame`
- Для микрофона: `pydub`
