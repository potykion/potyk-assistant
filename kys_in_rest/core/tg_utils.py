def escape(text):
    to_escape = ".()-!+"
    for ch in to_escape:
        text = text.replace(ch, rf"\{ch}")
    return text


class AskForDataTg(Exception):
    ...
