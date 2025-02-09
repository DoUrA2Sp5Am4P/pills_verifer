import os
from deep_translator import GoogleTranslator

def translate_text(text):
    res=GoogleTranslator(source='en', target='ru').translate(text) 
    return res

def translate_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()
    
    translated_text = translate_text(original_text)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(translated_text))

    return file_path

def translate_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            try:
                result=translate_file(file_path)
                print(f"Переведенный текст сохранен в {result}")
            except Exception as e:
                print(f"Ошибка при обработке файла: {e}")


# Укажите путь к директории с файлами
directory_path = './names'
translate_files_in_directory(directory_path)