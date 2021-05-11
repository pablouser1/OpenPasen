from openpasen.common import config
from openpasen.api.handler import sendReq
class Auth:
    @staticmethod
    def checkSession():
        creds = config.getConfig("Login")
        if creds:
            Auth.login(creds["username"], creds["password"])
            return True

        return False
    
    @staticmethod
    def login(username, password):
        res = sendReq('/login', 'POST', {
            "USUARIO": username,
            "CLAVE": password,
            "p": '{"version":"11.10.5"}'
        })
        return res
