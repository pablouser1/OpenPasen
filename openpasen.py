import requests, pickle
import os
import json
#Initial variables
headers = {
    "Content-Type": "application/json; charset=UTF-8"
}

headerslogin = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

#Facilitar las requests
def req(method, url):
    if (method == "GET"):
        data = requests.get(url, headers=headers, cookies=jar)
        return data
    if (method == "POST"):
        data = requests.post(url, headers=headers, cookies=jar)
        return data

#Hacer login, conseguir cookies para iniciar sesión
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    body = 'p={ "version":"11.9.1" }&USUARIO=' + username + '&CLAVE=' + password
    login = requests.post("https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/login", headers=headerslogin, data=body)
    if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
        print("Error al iniciar sesión, ¿ha escrito la contraseña correcta?")
        quit(1)
    global jar
    jar = requests.cookies.RequestsCookieJar()
    jar.set('SenecaP', login.cookies['SenecaP'], domain='www.juntadeandalucia.es', path='/')
    jar.set('JSESSIONID', login.cookies['JSESSIONID'], domain='www.juntadeandalucia.es', path='/')
    print("Las cookies usadas son: " + str(jar))
    mainmenu()


#Menú prinicipal
def mainmenu():
    main = req("GET", "https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/infoSesion")

    os.system('clear')
    print ("Bienvenido, " + main.json()['RESULTADO'][0]['USUARIO'])
    print ("\t1 - Actividades evaluables")
    print ("\t2 - segunda opción")
    print ("\t3 - Información")
    print ("\t9 - salir")
    while True:
        menuoption = input("inserta un numero valor >> ")
        if menuoption=="1":
            acteval()
        elif menuoption=="2":
            print ("")
            input("Has pulsado la opción 2...\npulsa una tecla para continuar")
        elif menuoption=="3":
            info()
        elif menuoption=="9":
            break
        else:
            print ("")
            input("No has pulsado ninguna opción correcta...\nPulsa una tecla para continuar")

def acteval():
    os.system('clear')
    print ("\t1 - Test")
    print ("\t2 - Test2")
    print ("\t3 - Test3")
    print ("\t9 - salir")
    while True:
        menuoption = input("inserta un numero valor >> ")
        if menuoption=="1":
            acteval()
        elif menuoption=="2":
            print ("")
            input("Has pulsado la opción 2...\npulsa una tecla para continuar")
        elif menuoption=="3":
            info()
        elif menuoption=="9":
            break
        else:
            print ("")
            input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")

def info():
    print("WIP")
login()