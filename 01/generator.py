import _io


def gen(name, words):
    found_atleast_once = False
    if isinstance(name, _io.TextIOWrapper):
        text_file = name
    else:
        text_file = open(name, "r", encoding="utf8")
    for string in text_file:
        found = False
        for word in words:
            if word.lower() + " " in string.lower() in string.lower():
                found = True
                break
            if " " + word.lower() + " " in string.lower() in string.lower():
                found = True
                break
            if " " + word.lower() + "\n" in string.lower():
                found = True
                break
        if found:
            found_atleast_once = True
            yield string
    try:
        name.close()
    except AttributeError:
        text_file.close()
    if not found_atleast_once:
        yield None
