def concat(lst: list[str], separator=""):
    if len(lst) == 0:
        return ""
    return "".join([s + separator for s in lst[:-1]]) + lst[-1]
