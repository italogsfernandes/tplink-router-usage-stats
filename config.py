import configparser
from contants import CONFIG_PATH

def load_config(namespace):
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH)
    return (
        cfg[namespace]['ROUTER_IP'],
        cfg[namespace]['AUTH_TOKEN'],
        cfg[namespace]['OUTPUT_FILE'],
        cfg[namespace]['OUTPUT_FILE_COMPLETO']
    )

def get_apelidos_mac():
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH)
    apelidos_mac = {
        key.upper(): value for key, value in cfg['APELIDOS_MAC'].items()
    }
    return apelidos_mac
