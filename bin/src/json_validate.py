
def json_validate(data, required_keys, err_prefix):
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise ValueError(f"{err_prefix} Missing required keys: {', '.join(missing_keys)}")

    none_values = [key for key in required_keys if data.get(key) is None]
    if none_values:
        raise ValueError(f"{err_prefix} None values for keys: {', '.join(none_values)}")