import json

def dict_contains(keys: tuple, check_dict: dict) -> bool:
    """
    Check if a dictionary contains all of the desired keys.
    """
    for key in keys:
        if not key in check_dict:
            return False
    return True


def convert_dict_types(types: tuple, res_dict: dict) -> bool:
    """
    Convert dictionary values to desired types.
    """
    for index, key in enumerate(res_dict.keys()):
        try:
            res_dict[key] = types[index](res_dict[key])
        except (TypeError, ValueError, json.decoder.JSONDecodeError):
            return False
    return True


def order_dict(keys: tuple, res_dict: dict) -> None:
    """
    Order a dictionary based on a given key order.
    """
    new_dict = {}
    for key in keys:
        new_dict[key] = res_dict[key]
    res_dict.clear()
    res_dict.update(new_dict)