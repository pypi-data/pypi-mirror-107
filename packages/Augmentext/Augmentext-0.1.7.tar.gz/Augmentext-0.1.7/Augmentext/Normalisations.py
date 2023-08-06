# Module for normalisation functions.
# Normalisation procedures do not have a probability associated with them.

class NormaliseCase():
    def __init__(self):
        pass

    def perform_operation(text, case):

        if case == "UPPER":
            return text.upper()
        elif case == "LOWER":
            return text.lower()

