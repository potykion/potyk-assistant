def escape(text):
    to_escape = ".()-!+"
    for ch in to_escape:
        text = text.replace(ch, rf"\{ch}")
    return text


class AskForData(Exception):
    def __init__(self, question, field=None):
        self.question = question
        self.field = field
