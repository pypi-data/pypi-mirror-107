import requests

class Servicios_MCC:
    def services_Check():
        request = requests.get(f'https://status.mojang.com/check')
        if request.ok:
            datos_Service = request.json()
            print(f'\n\nLista de sericios\n1: Minecraft.net ---------------- Estado: {datos_Service[0].get("minecraft.net").upper()}\n2: Sesion en Minecraft.net ------ Estado: {datos_Service[1].get("session.minecraft.net").upper()}\n3: Cuenta en Mojan.com ---------- Estado: {datos_Service[2].get("account.mojang.com").upper()}\n4: Autentificacion en Mojan.com - Estado: {datos_Service[3].get("authserver.mojang.com").upper()}\n5: Sesion en Mojan.com ---------- Estado: {datos_Service[4].get("sessionserver.mojang.com").upper()}\n6: Mojan APIs ------------------- Estado: {datos_Service[5].get("api.mojang.com").upper()}\n7: Texturas en Minecraft -------- Estado: {datos_Service[6].get("textures.minecraft.net").upper()}\n8: Mojan.com -------------------- Estado: {datos_Service[7].get("mojang.com").upper()}')