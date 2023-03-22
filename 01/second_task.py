def gen(filename: str, words: list):
    with open(filename, "r", encoding="utf8") as text_file:
        for string in text_file:
            for word in words:
                if word.lower() in string.lower():
                    yield string
