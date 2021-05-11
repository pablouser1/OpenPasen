from openpasen.api.handler import sendReq
class UserAPI:
    @staticmethod
    def infoSesion():
        res = sendReq("/infoSesion", "GET")
        return res
    
    @staticmethod
    def photo(matricula):
        res = sendReq("/imageAlumno", "POST", {
            "X_MATRICULA": matricula,
            "ALTO": 128,
            "ANCHO": 128
        }, "photo")
        return res