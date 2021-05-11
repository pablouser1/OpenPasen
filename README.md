# OpenPasen

### <span style="background-color:red;">AVISO</span>
La versión estable y usable está [aquí](https://github.com/pablouser1/OpenPasen/tree/legacy)

Esta versión está todavía en desarrollo.

## Qué es OpenPasen
Esta es una implementación open-source distribuida bajo la licencia GPLv3 del programa de seguimiento escolar PASEN hecha en Python.

Actualmente testeado usando una cuenta de PASEN de alumno usando Linux, de momento no funciona con cuentas de tutores legales.

## Cómo usar

#### Linux:

Necesitas instalar las dependencias: Python 3, Glade, y las librerías requests, configparser y GTK 3.

Opcionalmente requiere BeautifulSoup para generar los reportes y openpyxl para generar los horarios fotocopiables.

Cuando tengas las dependencias puedes empezar ejecutando el script "run.sh".

## TODO

#### General:

https://seneca.juntadeandalucia.es/seneca/jsp/pasendroid/getComunicaciones (Comunicaciones profe <-> alumno) | GET

https://seneca.juntadeandalucia.es/seneca/jsp/pasendroid/avisos (Avisos) | GET (Está implementada pero a veces falla)

https://seneca.juntadeandalucia.es/seneca/jsp/pasendroid/getConductasContrarias (Conductas contrarias) | POST (Incompleta)

Tutores legales

Bug: Al generar más de un informe en una sesión comienza a duplicar entradas

## Cómo contribuir

Este programa utiliza la API de iPASEN, las solicitudes al servidor necesarias se pueden obtener a través de logcat. Cualquiera contribución es bienvenida.
