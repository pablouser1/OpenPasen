from openpasen.api.handler import sendReq
class PasenAPI:
    @staticmethod
    def login(username, password):
        res = sendReq('/login', 'POST', {
            "USUARIO": username,
            "CLAVE": password,
            "p": '{"version":"11.10.5"}'
        })
        return res
    # User
    @staticmethod
    def infoSesion():
        res = sendReq("/infoSesion", "GET")
        return res
    
    # Photo
    @staticmethod
    def photo(matricula):
        res = sendReq("/imageAlumno", "POST", {
            "X_MATRICULA": matricula,
            "ALTO": 128,
            "ANCHO": 128
        }, "photo")
        return res
    
    # Convocatorias
    @staticmethod
    def convocatorias(matricula):
        convocatorias = []
        res = sendReq("/getConvocatorias", "POST", {
            "X_MATRICULA": matricula
        })
        if res:
            for convocatoria in res["RESULTADO"]:
                convocatorias.append({
                    "id": convocatoria["X_CONVCENTRO"],
                    "name": convocatoria["D_CONVOCATORIA"],
                    "active": convocatoria["L_ACTIVA"]
                })
            return convocatorias
        return []
    # Notas
    @staticmethod
    def notas(matricula, convcentro):
        notas = []
        res = sendReq("/getNotas", "POST", {
            "X_MATRICULA": matricula,
            "X_CONVCENTRO": convcentro
        })
        if res:
            for nota in res["RESULTADO"]:
                notas.append({
                    "nombre": nota["D_MATERIA"],
                    "nota": nota["NOTA"]
                })
            return notas
        return []
