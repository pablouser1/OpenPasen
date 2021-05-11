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

    # Asignaturas
    @staticmethod
    def asignaturas(matricula):
        asignaturas = []
        res = sendReq("/getMateriasMatricula", "POST", {
            "X_MATRICULA": matricula
        })
        if res:
            for asignatura in res["RESULTADO"]:
                asignaturas.append({
                    "id": asignatura["X_MATERIAOMG"],
                    "name": asignatura["D_MATERIAC"]
                })
            return asignaturas
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
    # Actividades evaluables
    @staticmethod
    def actividades(matricula, convcentro, asignatura = None):
        actividades = []
        data = {
            "X_MATRICULA": matricula,
            "X_CONVCENTRO": convcentro
        }
        if asignatura:
            data["X_MATERIAOMG"] = asignatura

        res = sendReq("/getActividadesEvaluables", "POST", data)
        if res:
            for actividad in res["RESULTADO"]:
                actividades.append({
                    "id": actividad["X_ACTEVA"],
                    "nombre": actividad["D_ACTEVA"],
                    "nota": actividad["N_NOTA"]
                })
            return actividades
        return []
    # Centro
    @staticmethod
    def centro(xcentro):
        res = sendReq("/datosCentro", "POST", {
            "X_CENTRO": xcentro
        })
        if res:
            return res["RESULTADO"]
        return res

    # Horario
    @staticmethod
    def horario(matricula):
        res = sendReq("/getHorario", "POST", {
            "X_MATRICULA": matricula
        })
        return res
