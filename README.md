# Верификатор таблеток
## Установка
1. Сначала установите Python 3.11.9
2. Затем клонируйте репозиторий
3. Установите зависимости `pip install -r requirements.txt`
4. Установите `Распространяемые пакеты Visual C++ для Visual Studio 2013` (библиотеки `libconv.dll`) https://www.microsoft.com/ru-ru/download/details.aspx?id=40784
5. Клонируйте в папку с `main_program.py` XTTS `git clone https://huggingface.co/coqui/XTTS-v2`
6. Клонируйте в папку с `main_program.py` VOSK (vosk-model-small-ru-0.22) https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
7. Клонируйте в папку с `main_program.py` FFmpeg (ffmpeg-master-latest-win64-gpl) https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
8. Запустите `python main_program.py`
9. Скопируйте из папки ./nextion/nextion_1.tft в экран Nextion (формат sd карты FAT32)
