import pandas as pd
import os

# Загрузка Excel файла
excel_file = 'English.xlsx'  # Укажите путь к вашему файлу
data = pd.read_excel(excel_file)

# Создание необходимых папок, если они не существуют
folders = ['contraindications', 'dosages', 'instructions', 'names']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Итерация по строкам данных
for index, row in data.iterrows():
    name = row['name']
    name_file=f'names/name_{name}.txt'
    with open(name_file, 'w', encoding='utf-8') as f:
        f.write(name)
    # Создание файла contraindication_{name}.txt
    contraindications = row[['contraindication_1', 'contraindication_2']].dropna().tolist()
    contraindication_file = f'contraindications/contraindication_{name}.txt'
    with open(contraindication_file, 'w', encoding='utf-8') as f:
        for i, contraindication in enumerate(contraindications):
            if i == 0:
                f.write(f"Side effects: {contraindication}\n")
            else:
                f.write(f"Notes: {contraindication}\n")

    # Создание файла dosage_{name}.txt
    dosages = row[['dosage_1', 'dosage_2', 'dosage_3']].dropna().tolist()
    dosage_file = f'dosages/dosage_{name}.txt'

    with open(dosage_file, 'w', encoding='utf-8') as f:
        if len(dosages) > 0:
            f.write(f"Class: {dosages[0]}\n")
        if len(dosages) > 1:
            f.write(f"Form: {dosages[1]}\n")
        if len(dosages) > 2:
            f.write(f"Dosage: {dosages[2]}\n")

    # Создание файла instruction_{name}.txt
    instruction = row['instruction']
    instruction_file = f'instructions/instruction_{name}.txt'

    with open(instruction_file, 'w', encoding='utf-8') as f:
        f.write(f"Therapy: {instruction}")