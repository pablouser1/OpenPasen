# OpenPasen

Esta es una implementación open-source distribuida bajo la licencia GPLv3 del programa de seguimiento escolar PASEN.

Utiliza Python 3, Glade, y las librerías requests, configparser y GTK 3.

Actualmente testeado usando una cuenta de PASEN de alumno y usando el sistema operativo GNU/Linux.

# Cómo usar

Una vez instaladas todas las librerías necesarias, inicia el programa openpython.py.

# TODO

Queda por implementar las siguientes funciones:

https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/getComunicaciones (Comunicaciones profe <-> alumno) | GET

https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/getActividadesEvaluables (Actividades evaluables) | POST

https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/avisos (Avisos) | GET (Está implementada pero a veces falla)

Fallback para fallos de conexión

setup.py / Instalador

Comprobar compatibilidad con Windows y Mac

# Cómo contribuir

Este programa utiliza el sistema de APIs de la aplicación de móvil de iPasen de Android. Para poder ver lo que está haciendo puedes conectar tu teléfono al ordenador y usando adb logcat puedes ver las conexiones que hace tu teléfono a los servidores de la Junta de Andalucía. Con esta información te será más fácil contribuir al código.
