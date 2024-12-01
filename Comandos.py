import re

# Validaciones
def validar_ip(ip):
    """Valida si una dirección IP es válida."""
    patron = r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'
    if re.match(patron, ip):
        partes = ip.split('.')
        if all(0 <= int(parte) <= 255 for parte in partes):
            return True
    return False

def pedir_dato(prompt, tipo):
    """
    Solicita un dato al usuario y valida su formato según el tipo.
    - tipo: "ip" para direcciones IP, "interfaz" para nombres de interfaces.
    """
    while True:
        dato = input(prompt)
        if tipo == "ip" and validar_ip(dato):
            return dato
        elif tipo == "interfaz" and ('Fa' in dato or 'Gig' in dato or 'S' in dato):
            return dato
        else:
            print("\033[91mError: Entrada no válida. Inténtalo de nuevo.\033[0m")

# Configuración del Router
def configurar_router():
    print("\n--- Configuración de Router ---")
    
    # Submenú para elegir tipo de interfaz
    while True:
        print("\nElige el tipo de interfaz que deseas configurar:")
        print("1. FastEthernet")
        print("2. Serial")
        print("3. Volver al menú principal")
        
        opcion_interfaz = input("Elige una opción (1-3): ")
        
        if opcion_interfaz == '1':
            tipo_interfaz = "FastEthernet"
            prefijo = "Fa"
            break
        elif opcion_interfaz == '2':
            tipo_interfaz = "Serial"
            prefijo = "S"
            break
        elif opcion_interfaz == '3':
            return
        else:
            print("\033[91mOpción no válida. Intenta de nuevo.\033[0m")
    
    # Solicitar y validar el puerto de la interfaz
    puerto = pedir_dato(f"Introduce el puerto de {tipo_interfaz} que deseas configurar (ejemplo: {prefijo}0/0): ", "interfaz")
    print(f"\033[92mHas seleccionado la interfaz {puerto}.\033[0m")
    
    # Solicitar y validar la IP y la máscara de subred
    ip = pedir_dato("Introduce la dirección IP para la interfaz (ejemplo: 192.168.1.1): ", "ip")
    mascara = pedir_dato("Introduce la máscara de subred para la interfaz (ejemplo: 255.255.255.0): ", "ip")
    
    # Comandos para configurar en el router
    comandos_cli = [
        "enable",
        "configure terminal",
        f"interface {puerto}",
        f"ip address {ip} {mascara}",
        "no shutdown",
        "exit",
        "copy running-config startup-config"
    ]
    
    print("\n--- Comandos para configurar el Router en CLI ---")
    print("1. Ve a la pestaña CLI del Router en Packet Tracer.")
    print("2. Introduce los comandos en el siguiente orden:\n")
    for comando in comandos_cli:
        print(comando)

    # Opción para agregar rutas estáticas
    while True:
        print("\n¿Deseas configurar enrutamiento estático?")
        print("1. Sí")
        print("2. No")
        opcion_enrutamiento = input("Elige una opción (1-2): ")
        
        if opcion_enrutamiento == '1':
            agregar_ruta_estatica()
            break
        elif opcion_enrutamiento == '2':
            print("\033[92mEnrutamiento estático no configurado.\033[0m")
            break
        else:
            print("\033[91mOpción no válida. Intenta de nuevo.\033[0m")

    print("\n--- Nota ---")
    print("Asegúrate de guardar la configuración con el comando 'copy running-config startup-config'.")

# Función para configurar una ruta estática
def agregar_ruta_estatica():
    print("\n--- Configuración de Ruta Estática ---")
    
    # Solicitar red de destino, máscara de subred y puerta de enlace
    red_destino = pedir_dato("Introduce la red de destino (ejemplo: 192.168.2.0): ", "ip")
    mascara_destino = pedir_dato("Introduce la máscara de subred de la red de destino (ejemplo: 255.255.255.0): ", "ip")
    puerta_enlace = pedir_dato("Introduce la puerta de enlace de la ruta estática (ejemplo: 192.168.1.1): ", "ip")
    
    # Comando para agregar la ruta estática
    comando_ruta_estatica = f"ip route {red_destino} {mascara_destino} {puerta_enlace}"
    
    print("\n--- Comandos para configurar la ruta estática en el Router ---")
    print("1. Ve a la pestaña CLI del Router en Packet Tracer.")
    print("2. Introduce el siguiente comando:\n")
    print(comando_ruta_estatica)
    
    # Verifica si se desea agregar más rutas estáticas
    while True:
        print("\n¿Deseas agregar otra ruta estática?")
        print("1. Sí")
        print("2. No")
        opcion_ruta = input("Elige una opción (1-2): ")
        
        if opcion_ruta == '1':
            agregar_ruta_estatica()
            break
        elif opcion_ruta == '2':
            print("\033[92mEnrutamiento estático configurado.\033[0m")
            break
        else:
            print("\033[91mOpción no válida. Intenta de nuevo.\033[0m")

# Configuración del PC
def configurar_pc():
    print("\n--- Configuración de PC ---")
    
    # Solicitar y validar la IP del PC, máscara y puerta de enlace
    ip = pedir_dato("Introduce la dirección IP del PC (ejemplo: 192.168.1.10): ", "ip")
    mascara = pedir_dato("Introduce la máscara de subred del PC (ejemplo: 255.255.255.0): ", "ip")
    puerta_enlace = pedir_dato("Introduce la puerta de enlace del PC (ejemplo: 192.168.1.1): ", "ip")
    
    print("\n--- Pasos para configurar el PC en Packet Tracer ---")
    print("1. Haz clic en el PC y abre la pestaña *Desktop*.")
    print("2. Selecciona *IP Configuration*.")
    print(f"3. Introduce los siguientes datos:\n   - Dirección IP: {ip}\n   - Máscara de subred: {mascara}\n   - Puerta de enlace: {puerta_enlace}")
    print("4. Guarda los cambios y verifica la conectividad con un *ping*.")

# Menú principal
def main():
    while True:
        print("\n--- Menú de Configuración en Packet Tracer ---")
        print("1. Configurar Router")
        print("2. Configurar PC")
        print("3. Salir")
        
        opcion = input("Elige una opción (1-3): ")
        
        if opcion == '1':
            configurar_router()
        elif opcion == '2':
            configurar_pc()
        elif opcion == '3':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("\033[91mOpción no válida. Intenta de nuevo.\033[0m")

# Llamada a la función principal para ejecutar el programa
if __name__ == "__main__":
    main()
