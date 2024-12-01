import ipaddress
import math
from colorama import Fore, Style, init

# Inicializar colores para diferentes sistemas operativos
init(autoreset=True)

def calcular_bloques(ip_inicio, ip_fin, bloques):
    try:
        ip_inicio = ipaddress.IPv4Address(ip_inicio)
        ip_fin = ipaddress.IPv4Address(ip_fin)

        total_ips = int(ip_fin) - int(ip_inicio) + 1
        tamaño_bloque = 2 ** math.floor(math.log2(total_ips // bloques))

        if tamaño_bloque < 4:
            raise ValueError("El rango de IPs no permite dividir en subredes válidas.")

        máscara = 32 - math.ceil(math.log2(tamaño_bloque))

        subredes = []
        ip_actual = ip_inicio
        while ip_actual <= ip_fin:
            red = ipaddress.IPv4Network((ip_actual, máscara), strict=False)
            subredes.append(red)
            ip_actual = red[-1] + 1

            if len(subredes) == bloques:
                break

        return subredes, tamaño_bloque, máscara
    except Exception as e:
        return f"Error: {str(e)}"

def resumen_subred(subred):
    """Devuelve un resumen detallado de una subred."""
    ip_inicio = subred[0]
    ip_final = subred[-1]
    broadcast = subred.broadcast_address
    máscara = subred.prefixlen
    rango_ips = f"{list(subred.hosts())[0]} - {list(subred.hosts())[-1]}"
    return ip_inicio, ip_final, broadcast, máscara, rango_ips

def color_para_red(i):
    """Devuelve un color distinto para cada red."""
    colores = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]
    return colores[i % len(colores)]  # Rota entre los colores disponibles

# Solicitar datos al usuario
print(Fore.YELLOW + "=== Calculadora de Subredes con Resumen Detallado ===" + Style.RESET_ALL)
try:
    ip_inicio = input(Fore.CYAN + "Introduce la IP inicial (ejemplo: 200.200.100.0): " + Style.RESET_ALL)
    ip_fin = input(Fore.CYAN + "Introduce la IP final (ejemplo: 200.200.101.255): " + Style.RESET_ALL)
    bloques = int(input(Fore.CYAN + "Introduce el número de bloques deseados: " + Style.RESET_ALL))
    
    resultado = calcular_bloques(ip_inicio, ip_fin, bloques)
    if isinstance(resultado, str):
        print(Fore.RED + resultado)
    else:
        subredes, tamaño_bloque, máscara = resultado
        print(Fore.GREEN + f"\nRango IP inicial: {ip_inicio} | Rango IP final: {ip_fin}")
        print(Fore.GREEN + f"Bloques solicitados: {bloques} | Tamaño ajustado de cada bloque: {tamaño_bloque} IPs | Máscara: /{máscara}\n")

        for i, subred in enumerate(subredes, 1):
            ip_inicio, ip_final, broadcast, máscara, rango_ips = resumen_subred(subred)
            color_red = color_para_red(i-1)  # Obtiene un color distinto para cada red

            print(color_red + f"=== Bloque {i} ===")
            print(color_red + f"  Subred: {subred}")
            print(color_red + f"  IP de inicio: {ip_inicio}")
            print(color_red + f"  IP de final: {ip_final}")
            print(color_red + f"  Broadcast: {broadcast}")
            print(color_red + f"  Máscara: /{máscara}")
            print(color_red + f"  Rango de IPs disponibles: {rango_ips}")
            print(Style.RESET_ALL)

except ValueError:
    print(Fore.RED + "Error: Por favor, introduce valores válidos.")

# Pausar antes de salir
input(Fore.YELLOW + "\nPresiona Enter para salir..." + Style.RESET_ALL)
