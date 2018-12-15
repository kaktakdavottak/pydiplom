import configparser


def get_config(path):
    """
    Returns the config object
    """
    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    """
    Get out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    return value
