def get_file_from_path(original_string: str, sepatator: str = "/"):
    return original_string[original_string.rfind("/") + 1 :]


def require_keys(d, keys):
    if type(keys) == str:
        keys = [keys]
    for k in keys:
        if k not in d:
            raise ValueError("'{}' must be set".format(k))

    return True
