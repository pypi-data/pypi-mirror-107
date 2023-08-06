import requests
import json
from base64 import b64decode


class MC:

    #Obtener el UUID del Perfil
    def get_UUID(nombre_Usuario):
        request = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{nombre_Usuario}')
        if request.ok:
            try:
                datos_usuario: str = request.json()['id']
                return datos_usuario
            except json.decoder.JSONDecodeError:
                return None
        else:
            print(f'La respuesta no es la esperada {request}, debe de ser 200')

    #Obtener el historial de los nombres
    def get_History_Names(nombre_Usuario):
        uuid = MC.get_UUID(nombre_Usuario)
        request = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names')
        if request.ok:
            datos_usuario = request.json()
            vec_Datos = []
            for dato in datos_usuario:
                vec_Datos.append(dato)
            print(vec_Datos)
        else:
            print(f'No se encontro el perfil')

    #Saber si el nombre esta disponible
    def get_Name_Free(nombre_Usuario):
        request = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{nombre_Usuario}')
        if request.status_code != 200:
            print(f'El nombre de Usuario {nombre_Usuario} esta Disponible')
        else:
            print(f'El nombre de Usuario {nombre_Usuario} no esta Disponible')

    #Renderizar Skin en 3D
    def get_Render_Skin(nombre_Usuario):
        uuid = MC.get_UUID(nombre_Usuario)
        request = requests.get(f'https://visage.surgeplay.com/full/512/{uuid}')
        if request.ok:
            return request
        else:
            print('No se puedo renderizar')


    # Metodo incompleto, solo carga la skin en su formato base
    # def get_Render_Skin_Oficial(nombre_Usuario):
    #     uuid = MC.get_UUID(nombre_Usuario)
    #     request = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}')
    #     if request.ok:
    #         vec_Datos = request.json()['properties']
    #         datos = vec_Datos[0].get('value')
    #         vec_Decodificado = b64decode(datos)
    #         print(vec_Decodificado)
