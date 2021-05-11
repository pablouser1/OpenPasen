import requests

# Session
s = requests.Session()

BASE_URL = "https://seneca.juntadeandalucia.es/seneca/jsp/pasendroid" # Este es el comienzo de todas las URLs de PASEN

# HEADERS
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "OpenPasen"
}
HEADERS_POST = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "OpenPasen"
}


def sendReq(endpoint: str, method: str, data = None, response = 'json'):
    try:
        send_headers = HEADERS if "GET" in method else HEADERS_POST
        res = s.request(method, BASE_URL + endpoint, headers=send_headers, data=data, verify="assets/juntadeandalucia-es-chain.pem", timeout=5)
        if 'json' in response:
            # El encoding del servidor es ISO-8859-1
            res.encoding = 'ISO-8859-1'
            # Si el servidor devuelve un error hacer una exception
            if (res.json()['ESTADO']['CODIGO'] == "E"):
                raise Exception(res.json()['ESTADO']['DESCRIPCION'])
            return res.json()
        elif 'img' in response:
            return res
    
    # Timeout
    except requests.exceptions.RequestException as e:
        print(f'Error de conexión, {e}')
    
    return False
