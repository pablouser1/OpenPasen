import configparser
from pathlib import Path
from os import mkdir
import platform

class Config:
    config = configparser.ConfigParser()

    def __init__(self):
        self.configPath = self.getPath()
        self.importConfig()

    def getPath(self):
        config_path = None
        homepath = str(Path.home())
        if platform.system() in "Linux":
            config_path = homepath + "/.config/OpenPasen/" # Localización en linux
        elif platform.system() in "Windows":
            config_path = homepath + "/AppData/Roaming/OpenPasen/" # Localización en Windows
        elif platform.system() in "Darwin":
            config_path = homepath + "/Library/OpenPasen" # Localización en Mac

        if config_path and not Path(config_path).is_dir():
            mkdir(config_path)
        return config_path

    def importConfig(self):
        config_file = self.configPath + "config.ini"
        if Path(config_file).is_file():
            print("Configuración encontrada")
            self.config.read(config_file)
            return True
        print("Configuración no encontrada")
        return False

    def getConfig(self, section):
        if self.config.has_section(section):
            return self.config[section]
        return None

    def saveLogin(self, username, password):
        self.config["Login"] = {
            "username": username,
            "password": password
        }
        with open(self.configPath + "config.ini", 'w') as configfile:
            self.config.write(configfile)
