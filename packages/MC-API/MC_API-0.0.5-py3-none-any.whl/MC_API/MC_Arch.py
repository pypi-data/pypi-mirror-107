import requests
from simple_colors import *
from base64 import b64decode


class MC:

    class User_MC:
        #Obtener el UUID del Perfil
        def get_UUID(nombre_Usuario):
            request = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{nombre_Usuario}')
            if request.ok:
                try:
                    datos_usuario: str = request.json()['id']
                    return datos_usuario
                except Exception:
                    return print('Error al intentar convetir el request a JSON')
            else:
                print(f'La respuesta no es la esperada {request}, debe de ser 200')

        #Obtener el historial de los nombres
        def get_History_Names(nombre_Usuario):
            uuid = MC.User_MC.get_UUID(nombre_Usuario)
            request = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names')
            if request.ok:
                datos_usuario = request.json()
                vec_Datos = []
                for dato in datos_usuario:
                    vec_Datos.append(dato.get('name'))
                return vec_Datos
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
            uuid = MC.User_MC.get_UUID(nombre_Usuario)
            request = requests.get(f'https://visage.surgeplay.com/full/512/{uuid}')
            if request.ok:
                return f'https://visage.surgeplay.com/full/512/{uuid}'
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

    class Servicios_MCC:
        def services_Check():
            request = requests.get(f'https://status.mojang.com/check')
            if request.ok:
                datos_Service = request.json()

                sericios = '\n\nLista de sericios\n1: Minecraft.net ---------------- Estado: '

                if datos_Service[0].get("minecraft.net").upper() == 'GREEN':
                    sericios+= green(datos_Service[0].get("minecraft.net").upper())
                elif datos_Service[0].get("minecraft.net").upper() == 'YELLOW':
                    sericios+= yellow(datos_Service[0].get("minecraft.net").upper())
                elif datos_Service[0].get("minecraft.net").upper() == 'RED':
                    sericios+= red(datos_Service[0].get("minecraft.net").upper())
            
                sericios+='\n2: Sesion en Minecraft.net ------ Estado: '

                if datos_Service[1].get("session.minecraft.net").upper() == 'GREEN':
                    sericios+= green(datos_Service[1].get("session.minecraft.net").upper())
                elif datos_Service[1].get("session.minecraft.net").upper() == 'YELLOW':
                    sericios+= yellow(datos_Service[1].get("session.minecraft.net").upper())
                elif datos_Service[1].get("session.minecraft.net").upper() == 'RED':
                    sericios+= red(datos_Service[1].get("session.minecraft.net").upper())
            
                sericios+='\n3: Cuenta en Mojan.com ---------- Estado: '

                if datos_Service[2].get("account.mojang.com").upper() == 'GREEN':
                    sericios+= green(datos_Service[2].get("account.mojang.com").upper().upper())
                elif datos_Service[2].get("account.mojang.com").upper() == 'YELLOW':
                    sericios+= yellow(datos_Service[2].get("account.mojang.com").upper().upper())
                elif datos_Service[2].get("account.mojang.com").upper() == 'RED':
                    sericios+= red(datos_Service[2].get("account.mojang.com").upper())

                sericios+='\n4: Autentificacion en Mojan.com - Estado: '

                if datos_Service[3].get("authserver.mojang.com").upper() == 'GREEN':
                    sericios+= green(datos_Service[3].get("authserver.mojang.com").upper())
                elif datos_Service[3].get("authserver.mojang.com").upper() == 'YELLOW':
                    sericios+= yellow(datos_Service[3].get("authserver.mojang.com").upper())
                elif datos_Service[3].get("authserver.mojang.com").upper() == 'RED':
                    sericios+= red(datos_Service[3].get("authserver.mojang.com").upper())

                sericios+='\n5: Sesion en Mojan.com ---------- Estado: '

                if datos_Service[4].get("sessionserver.mojang.com").upper() == 'GREEN':
                    sericios+= green(datos_Service[4].get("sessionserver.mojang.com").upper())
                elif datos_Service[4].get("sessionserver.mojang.com").upper() == 'YELLOW':
                    sericios+= yellow(datos_Service[4].get("sessionserver.mojang.com").upper())
                elif datos_Service[4].get("sessionserver.mojang.com").upper() == 'RED':
                    sericios+= red(datos_Service[4].get("sessionserver.mojang.com").upper())

                sericios+='\n6: Mojan APIs ------------------- Estado: '

                if datos_Service[5].get("api.mojang.com").upper() == 'GREEN':
                    sericios+= green(datos_Service[5].get("api.mojang.com").upper())
                elif datos_Service[5].get("api.mojang.com").upper() == 'YELLOW':
                    sericios+= yellow(datos_Service[5].get("api.mojang.com").upper())
                elif datos_Service[5].get("api.mojang.com").upper() == 'RED':
                    sericios+= red(datos_Service[5].get("api.mojang.com").upper())

                sericios+='\n7: Texturas en Minecraft -------- Estado: '

                if datos_Service[6].get("textures.minecraft.net").upper() == 'GREEN':
                    sericios+= green(datos_Service[6].get("textures.minecraft.net").upper())
                elif datos_Service[6].get("textures.minecraft.net").upper() == 'YELLOW':
                    sericios+= yellow(datos_Service[6].get("textures.minecraft.net").upper())
                elif datos_Service[6].get("textures.minecraft.net").upper() == 'RED':
                    sericios+= red(datos_Service[6].get("textures.minecraft.net").upper())

                sericios+='\n8: Mojan.com -------------------- Estado: '

                if datos_Service[7].get("mojang.com").upper() == 'GREEN':
                    sericios+= green(datos_Service[7].get("mojang.com").upper())
                elif datos_Service[7].get("mojang.com").upper() == 'YELLOW':
                    sericios+= yellow(datos_Service[7].get("mojang.com").upper())
                elif datos_Service[7].get("mojang.com").upper() == 'RED':
                    sericios+= red(datos_Service[7].get("mojang.com").upper())

                print(sericios)   



