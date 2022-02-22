

def is_number(number: str) -> bool:

    try:
        float(number)
        return True
    except ValueError:
        return False
