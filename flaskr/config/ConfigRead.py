import yaml
class ConfigReader:
    def __init__(self):
        f = open("config.yml", 'r', encoding='utf-8')
        self.__config__ = yaml.load(f, Loader=yaml.FullLoader)
    def property(self, key: str):
        return self.__config__[key]