import ipaddress
import math

def calcular_mascara(total_equipos):
    """Calcula la máscara de subred mínima necesaria para acomodar el número total de equipos."""
    bits_necesarios = math.ceil(math.log2(total_equipos))
    bits_red = 32 - bits_necesarios
    return f"/{bits_red}"

def imprimir_titulo_color(titulo, color_code):
    """Imprime el título con el color especificado."""
    colores = {
        'rojo': '\033[91m',
        'verde': '\033[92m',
        'amarillo': '\033[93m',
        'azul': '\033[94m',
        'morado': '\033[95m',
        'cyan': '\033[96m',
        'blanco': '\033[97m',
        'reset': '\033[0m'
    }
    color = colores.get(color_code, '\033[0m')
    print(f"{color}{titulo}{colores['reset']}")

def obtener_numero_equipos():
    """Solicita el número de equipos y asegura que sea mayor que 2."""
    while True:
        try:
            equipos = int(input("¿Cuántos equipos necesitas? "))
            if equipos <= 2:
                imprimir_titulo_color("¡Error! El número de equipos debe ser mayor que 2.", 'rojo')
            else:
                return equipos
        except ValueError:
            imprimir_titulo_color("¡Error! Debes ingresar un número entero.", 'rojo')

def sumarizar_redes(redes_objetos):
    """Dada una lista de objetos ip_network, devuelve una superred que las cubra."""
    try:
        # Ordenar las redes por dirección de red
        redes_objetos = sorted(redes_objetos, key=lambda r: int(r.network_address))
        
        # Calcular la superred que cubre todas las redes
        superred = redes_objetos[0]
        for red in redes_objetos[1:]:
            superred = superred.supernet(new_prefix=superred.prefixlen - 1)
            # Verificar si la superred cubre todas las redes seleccionadas
            if not all(r.subnet_of(superred) for r in redes_objetos):
                raise ValueError("No se puede sumarizar las redes seleccionadas en una superred única.")
        
        return superred
    except ValueError as e:
        imprimir_titulo_color(f"Error al sumarizar las redes: {e}", 'rojo')
        return None

def validar_redes_contiguas(redes_objetos):
    """Valida que las redes seleccionadas sean contiguas."""
    try:
        redes_objetos = sorted(redes_objetos, key=lambda r: int(r.network_address))
        for i in range(1, len(redes_objetos)):
            prev = redes_objetos[i-1]
            curr = redes_objetos[i]
            # Verificar si la dirección de broadcast de la red anterior + 1 es igual a la dirección de red de la actual
            if int(prev.broadcast_address) + 1 != int(curr.network_address):
                raise ValueError(f"Las redes {prev} y {curr} no son contiguas.")
        return True
    except ValueError as e:
        imprimir_titulo_color(f"Error al validar las redes: {e}", 'rojo')
        return False

def main():
    try:
        imprimir_titulo_color("CÁLCULO DE REDES", 'morado')

        # Paso 1: Preguntar cuántas redes se necesitan
        num_redes = int(input("¿Cuántas redes necesitas? "))

        # Inicializamos una lista para guardar las redes y sus equipos
        redes = []

        # Paso 1a: Preguntar información de cada red
        for i in range(1, num_redes + 1):
            imprimir_titulo_color(f"\nConfiguración de la Red {i}:", 'cyan')
            nombre_red = input(f"Nombre para la Red {i}: ")
            equipos = obtener_numero_equipos()  # Usamos la nueva función de validación
            total_equipos = math.ceil(equipos * 1.2) + 2  # Sumar el 20% + 2
            total_hosts = 2 ** math.ceil(math.log2(total_equipos))  # Ajustar al número de hosts posible
            mascara = calcular_mascara(total_hosts)
            redes.append({
                "nombre": nombre_red,
                "equipos": equipos,
                "total_equipos": total_equipos,
                "mascara": mascara,
                "total_hosts": total_hosts,
                "subred": None  # Placeholder para almacenar el objeto ip_network
            })
            imprimir_titulo_color(f"Para la Red {i}, necesitas al menos la máscara {mascara} con {total_hosts} direcciones.", 'verde')

        # Ordenar redes de mayor a menor por el total de equipos
        redes.sort(key=lambda x: x["total_equipos"], reverse=True)

        # Mostrar el resumen de las redes
        imprimir_titulo_color("\nRESUMEN DE LAS REDES (ORDENADAS POR NÚMERO DE EQUIPOS):", 'morado')
        for i, red in enumerate(redes, start=1):
            print(f"Red {i} ({red['nombre']}): {red['equipos']} equipos, total con margen: {red['total_equipos']}, máscara: {red['mascara']}")

        # Paso 2: Preguntar en qué red quiere empezar
        red_inicio = int(input("\n¿Con qué red quieres empezar (1 al {}): ".format(num_redes))) - 1
        if red_inicio < 0 or red_inicio >= num_redes:
            imprimir_titulo_color("Selección de red inválida. Comenzando con la red de mayor tamaño.", 'rojo')
            red_inicio = 0

        # Paso 3: Solicitar la dirección IP base y asignar subredes
        direccion_base = input("\nIntroduce la dirección IP base para las redes (por ejemplo, 192.168.4.0): ")

        try:
            # Usamos la dirección IP base proporcionada para la red
            red_actual = ipaddress.ip_network(f"{direccion_base}/{redes[red_inicio]['mascara'].strip('/')}", strict=False)
        except ValueError as e:
            imprimir_titulo_color(f"Dirección IP base no válida: {e}", 'rojo')
            return

        # Paso 4: Asignar subredes
        imprimir_titulo_color("\nAsignación de subredes:", 'azul')
        for i in range(num_redes):
            # Determinar el índice de la red actual
            red_idx = (red_inicio + i) % num_redes
            red = redes[red_idx]

            # Crear subred para esta red usando la máscara calculada
            subred = ipaddress.ip_network(f"{red_actual.network_address}/{red['mascara'].strip('/')}", strict=False)
            red["subred"] = subred  # Asignar la subred al diccionario de la red

            # Imprimir título de la red con color
            colores = ['rojo', 'verde', 'amarillo', 'azul', 'morado', 'cyan']
            color = colores[i % len(colores)]
            imprimir_titulo_color(f"\nDetalles de la Red {red['nombre']}:", color)

            print(f"Dirección de red: {subred.network_address}")
            print(f"Broadcast: {subred.broadcast_address}")
            print(f"Máscara: {subred.netmask}")
            # Puerta de enlace válida: primera dirección utilizable
            gateway = next(subred.hosts())
            print(f"Puerta de enlace válida: {gateway}")

            # Mostrar el rango de IPs disponibles
            hosts = list(subred.hosts())
            if hosts:
                ip_inicio = hosts[0]  # Primera IP utilizable
                ip_fin = hosts[-1]    # Última IP utilizable
                print(f"Rango de IPs disponibles: {ip_inicio} hasta {ip_fin}")
            else:
                print("No hay IPs disponibles en esta subred.")

            # Calcular la siguiente subred avanzando el número de direcciones necesarias
            siguiente_red_int = int(subred.network_address) + subred.num_addresses
            siguiente_red_ip = ipaddress.ip_address(siguiente_red_int)
            try:
                # Crear una red a partir de la siguiente dirección con la misma prefixlen
                red_actual = ipaddress.ip_network(f"{siguiente_red_ip}/{subred.prefixlen}", strict=False)
            except ValueError as e:
                imprimir_titulo_color(f"Error al calcular la siguiente subred: {e}", 'rojo')
                break

        # Menú para sumarizar redes
        while True:
            imprimir_titulo_color("\nMenú:", 'amarillo')
            print("1. Sumarizar redes")
            print("2. Salir")
            opcion = input("Selecciona una opción (1 o 2): ")

            if opcion == "1":
                # Mostrar las redes disponibles para sumarizar
                imprimir_titulo_color("\nRedes disponibles para sumarizar:", 'morado')
                for i, red in enumerate(redes, start=1):
                    print(f"Red {i}: {red['nombre']} - Dirección de red: {red['subred'].network_address}")

                indices = input("\nIntroduce los números de las redes que deseas sumarizar (por ejemplo, 1, 2): ").split(",")
                redes_seleccionadas = []
                try:
                    for idx in indices:
                        idx = int(idx.strip()) - 1
                        if 0 <= idx < len(redes):
                            redes_seleccionadas.append(redes[idx]["subred"])
                        else:
                            imprimir_titulo_color(f"Red {idx + 1} no válida.", 'rojo')
                    if len(redes_seleccionadas) >= 2:
                        superred = sumarizar_redes(redes_seleccionadas)
                        if superred:
                            imprimir_titulo_color(f"Superred: {superred}", 'verde')
                    else:
                        imprimir_titulo_color("Debes seleccionar al menos dos redes para sumarizar.", 'rojo')
                except ValueError:
                    imprimir_titulo_color("Error al procesar la entrada. Asegúrate de ingresar números válidos.", 'rojo')

            elif opcion == "2":
                imprimir_titulo_color("Saliendo del programa...", 'cyan')
                break
            else:
                imprimir_titulo_color("Opción no válida. Por favor, selecciona 1 o 2.", 'rojo')

    except Exception as e:
        imprimir_titulo_color(f"Error en el programa: {e}", 'rojo')

if __name__ == "__main__":
    main()
