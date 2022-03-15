# Check if a dict contains all of the desired keys.
def dictContains(keys: tuple, check_dict: dict) -> bool:
    for key in keys:
        if not key in check_dict:
            return False
    return True

# Try to convert dict values to desired types.
def convertDictTypes(types: tuple, res_dict: dict) -> bool:
    for index, key in enumerate(res_dict.keys()):
        try:
            res_dict[key] = types[index](res_dict[key])
        except (TypeError, ValueError):
            return False
    return True

# Order a dictionary based on given key order.
def orderDict(keys: tuple, res_dict: dict) -> None:
    new_dict = {}
    for key in keys:
        new_dict[key] = res_dict[key]
    res_dict.clear()
    res_dict.update(new_dict)