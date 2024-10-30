# Верификатор таблеток
## Установка (для Windows)
1. Сначала установите Python 3.11.9
2. Затем клонируйте репозиторий
3. Установите зависимости `pip install -r requirements.txt`
4. Установите `Распространяемые пакеты Visual C++ для Visual Studio 2013` (библиотеки `libconv.dll`) https://www.microsoft.com/ru-ru/download/details.aspx?id=40784
5. Клонируйте в папку с `main_program.py` XTTS `git clone https://huggingface.co/coqui/XTTS-v2`
6. Клонируйте в папку с `main_program.py` VOSK (vosk-model-small-ru-0.22) https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
7. Клонируйте в папку с `main_program.py` FFmpeg (ffmpeg-master-latest-win64-gpl) https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
8. Запустите `python main_program.py`
9. Скопируйте из папки ./nextion/nextion_1.tft в экран Nextion (формат sd карты FAT32)
## Как использовать
# Для генерации голоса. 
Планируется, что голос будет генерироваться не на Raspberry (т. к. он очень долго это делает), а на компьютере. То есть записи с названиями всех таблеток, инструкциями к применению и противопоказаниями заренее будут храниться на Raspberry. Предварительно установите дополнительные зависимости из ``pip install -r requirements_for_tts.txt``
Итак для генерации голоса используйте ``generator.py --text Таблетка --output ./folder/name.wav``
# Для распознования таблеток
Если вы хотите тестировать на Windows, учтите, что у вас должены быть камера, микрофон и IDE Nextion, а также виртуальные Serial-порты (com0com например). Сначала запустите эмулятор (файл проекта .hmi хранится в папке nextion), затем подключите его к виртуальному порту. Запустите ``python main_program.py --port COM11``(На Raspberry ``/dev/Serial0``). Если что-то не работает сначала попробуйте выполнить отдельные тесты: ``ChangePage.py``,``play.py``,``qr.py``

Для установки на Raspberry ничего в программе кроме порта менять ненужно. Я использовал универсальные библеотеки: для изображений - ``cv2``, ``для вывода аудио - ``pygame``, для микрофона - ``pydub``
