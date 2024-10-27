import wave
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
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
    AUDIO_PATH = "./temp_python_files/output.wav"  # Замените на путь к вашему аудиофайлу

    # Загрузка модели
    print("Загрузка модели...")
    model = Model(MODEL_PATH)

    # Открытие аудиофайла
    with wave.open(AUDIO_PATH, "rb") as wf:
        # Проверка параметров аудиофайла (моно, 16 kHz)
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("Аудиофайл должен быть WAV, 16 kHz, моно.")

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
        print(result_text)
        return result_text
print(recognite("medicines_audio\names\name_1.wav"))