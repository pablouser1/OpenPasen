from openpasen.api.user import UserAPI
class User:
    def __init__(self):
        self.id = 0,
        self.nombre = ""
        self.unidad = ""
        self.curso = ""
        self.tutor = ""
        self.centro = {
            "id": 0,
            "nombre": ""
        }
        self.tipo = ""
        self.foto = None
    def getUser(self):
        res = UserAPI.infoSesion()
        if res:
            user = res["RESULTADO"][0]
            matricula = user["MATRICULAS"][0]
            self.id = matricula['X_MATRICULA']
            self.nombre = user["USUARIO"]
            self.unidad = matricula["UNIDAD"]
            self.curso = matricula["CURSO"]
            self.tutor = matricula["TUTOR"]
            self.centro = {
                "id": matricula["X_CENTRO"],
                "nombre": matricula["DENOMINACION"]
            }
            self.tipo = user["C_PERFIL"]
            # Foto
            self.foto = UserAPI.photo(self.id)


            return True
        
        return False
