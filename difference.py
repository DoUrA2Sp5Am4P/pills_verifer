from difflib import SequenceMatcher

def is_similar_to_instruction(word, target_word="инструкция", threshold=0.5):
    # Рассчитываем коэффициент схожести
    similarity = SequenceMatcher(None, word, target_word).ratio()
    return similarity >= threshold

# Примеры сокращенных слов
words_to_check = ["инстр", "нстр", "кция", "инстукция", "инструкци"]

for word in words_to_check:
    if is_similar_to_instruction(word):
        print(f"'{word}' -> похоже на 'инструкция'")
    else:
        print(f"'{word}' -> не похоже на 'инструкция'")