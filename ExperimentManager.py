import xml.etree.ElementTree as ET
import os

# Estructuras de datos personalizadas
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual.valor, end=" -> ")
            actual = actual.siguiente
        print("None")

# Clase para manejar los experimentos
class Experimento:
    def __init__(self, nombre, tejido, parejas):
        self.nombre = nombre
        self.tejido = tejido
        self.parejas = parejas

# Clase principal del sistema
class SistemaExperimentos:
    def __init__(self):
        self.catalogo = ListaEnlazada()

    def inicializar_sistema(self):
        self.catalogo = ListaEnlazada()
        print("Sistema inicializado correctamente.")

    def cargar_catalogo(self, ruta_archivo):
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            for experimento in root.findall('experimento'):
                nombre = experimento.get('nombre')
                tejido = experimento.find('tejido')
                filas = int(tejido.get('filas'))
                columnas = int(tejido.get('columnas'))
                rejilla = []
                for fila in tejido.find('rejilla').text.strip().split('\n'):
                    rejilla.append(fila.strip().split())
                parejas = []
                for pareja in experimento.find('proteinas').findall('pareja'):
                    parejas.append(pareja.text.strip().split())
                nuevo_experimento = Experimento(nombre, rejilla, parejas)
                self.catalogo.agregar(nuevo_experimento)
                print(f"Experimento '{nombre}' cargado con éxito.")
            print("Catálogo de experimentos cargado con éxito.")
        except Exception as e:
            print(f"Error al cargar el archivo XML: {e}")

    def desarrollar_experimento(self):
        print("\n--- DESARROLLAR EXPERIMENTO ---")
        print("1. Crear manualmente")
        print("2. Cargar desde el catálogo")
        print("3. Regresar al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.crear_experimento_manual()
        elif opcion == "2":
            self.cargar_desde_catalogo()
        elif opcion == "3":
            return
        else:
            print("Opción inválida.")

    def crear_experimento_manual(self):
        nombre = input("Ingrese el nombre del experimento: ")
        filas = int(input("Ingrese el número de filas: "))
        columnas = int(input("Ingrese el número de columnas: "))
        print("Ingrese la rejilla de proteínas (separadas por espacios):")
        rejilla = []
        for _ in range(filas):
            fila = input().strip().split()
            rejilla.append(fila)
        parejas = []
        print("Ingrese las parejas de proteínas (separadas por espacios, una por línea, 'fin' para terminar):")
        while True:
            pareja = input().strip()
            if pareja.lower() == 'fin':
                break
            parejas.append(pareja.split())
        nuevo_experimento = Experimento(nombre, rejilla, parejas)
        self.catalogo.agregar(nuevo_experimento)
        print(f"Experimento '{nombre}' creado y añadido al catálogo.")

    def cargar_desde_catalogo(self):
        if self.catalogo.cabeza is None:
            print("No hay experimentos en el catálogo.")
            return
        print("Experimentos disponibles:")
        actual = self.catalogo.cabeza
        while actual:
            print(f"- {actual.valor.nombre}")
            actual = actual.siguiente
        nombre_experimento = input("Seleccione el nombre del experimento: ")
        actual = self.catalogo.cabeza
        while actual:
            if actual.valor.nombre == nombre_experimento:
                self.ejecutar_experimento(actual.valor)
                return
            actual = actual.siguiente
        print("Experimento no encontrado.")

    def ejecutar_experimento(self, experimento):
        print("\n--- EJECUTAR EXPERIMENTO ---")
        print("1. Modificar")
        print("2. Ejecutar Paso a Paso")
        print("3. Ejecutar directamente para obtener el resultado final")
        print("4. Regresar al menú desarrollar experimento")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.modificar_experimento(experimento)
        elif opcion == "2":
            self.ejecutar_paso_a_paso(experimento)
        elif opcion == "3":
            self.ejecutar_directamente(experimento)
        elif opcion == "4":
            return
        else:
            print("Opción inválida.")

    def modificar_experimento(self, experimento):
        print("\n--- MODIFICAR EXPERIMENTO ---")
        print("1. Cambiar nombre del experimento")
        print("2. Modificar rejilla de proteínas")
        print("3. Modificar parejas de proteínas")
        print("4. Regresar al menú anterior")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nuevo_nombre = input("Ingrese el nuevo nombre del experimento: ")
            experimento.nombre = nuevo_nombre
            print(f"Nombre del experimento cambiado a '{nuevo_nombre}'.")

        elif opcion == "2":
            print("Ingrese la nueva rejilla de proteínas:")
            filas = int(input("Número de filas: "))
            columnas = int(input("Número de columnas: "))
            nueva_rejilla = []
            for i in range(filas):
                fila = input(f"Ingrese la fila {i + 1} (separada por espacios): ").strip().split()
                nueva_rejilla.append(fila)
            experimento.tejido = nueva_rejilla
            print("Rejilla de proteínas actualizada.")

        elif opcion == "3":
            print("Ingrese las nuevas parejas de proteínas (separadas por espacios, una por línea, 'fin' para terminar):")
            nuevas_parejas = []
            while True:
                pareja = input().strip()
                if pareja.lower() == 'fin':
                    break
                nuevas_parejas.append(pareja.split())
            experimento.parejas = nuevas_parejas
            print("Parejas de proteínas actualizadas.")

        elif opcion == "4":
            return  # Regresar al menú anterior

        else:
            print("Opción inválida.")

    def ejecutar_paso_a_paso(self, experimento):
        print("\n--- EJECUCIÓN PASO A PASO ---")
        rejilla = [fila.copy() for fila in experimento.tejido]  # Copia de la rejilla para no modificar la original
        parejas = experimento.parejas

        # Función para verificar si dos proteínas son una pareja que reacciona
        def es_pareja_reactiva(proteina1, proteina2):
            for pareja in parejas:
                if (proteina1 == pareja[0] and proteina2 == pareja[1]) or (proteina1 == pareja[1] and proteina2 == pareja[0]):
                    return True
            return False

        # Función para mostrar la rejilla
        def mostrar_rejilla(rejilla, titulo):
            print(f"\n--- {titulo} ---")
            for fila in rejilla:
                print(" ".join(fila))
            print("-------------------")

        paso = 0
        cambios = True

        # Mostrar el estado inicial de la rejilla
        mostrar_rejilla(rejilla, f"Paso {paso}")

        # Ejecutar pasos hasta que no haya más cambios
        while cambios:
            cambios = False
            paso += 1

            # Crear una copia de la rejilla para no modificar la original durante la iteración
            nueva_rejilla = [fila.copy() for fila in rejilla]

            # Recorrer la rejilla para buscar parejas reactivas
            for i in range(len(rejilla)):
                for j in range(len(rejilla[i])):
                    # Verificar la celda a la derecha (horizontal)
                    if j < len(rejilla[i]) - 1 and es_pareja_reactiva(rejilla[i][j], rejilla[i][j + 1]):
                        if rejilla[i][j] != "INERTE" and rejilla[i][j + 1] != "INERTE":
                            nueva_rejilla[i][j] = "INERTE"
                            nueva_rejilla[i][j + 1] = "INERTE"
                            cambios = True

                    # Verificar la celda abajo (vertical)
                    if i < len(rejilla) - 1 and es_pareja_reactiva(rejilla[i][j], rejilla[i + 1][j]):
                        if rejilla[i][j] != "INERTE" and rejilla[i + 1][j] != "INERTE":
                            nueva_rejilla[i][j] = "INERTE"
                            nueva_rejilla[i + 1][j] = "INERTE"
                            cambios = True

            # Actualizar la rejilla
            rejilla = nueva_rejilla

            # Mostrar el estado actual de la rejilla
            if cambios:
                mostrar_rejilla(rejilla, f"Paso {paso}")

        # Calcular el porcentaje de células inertes
        total_celdas = len(rejilla) * len(rejilla[0])
        celdas_inertes = sum(fila.count("INERTE") for fila in rejilla)
        porcentaje_inertes = (celdas_inertes / total_celdas) * 100

        # Determinar el resultado del medicamento
        if 30 <= porcentaje_inertes <= 60:
            resultado = "Medicamento exitoso"
        elif porcentaje_inertes < 30:
            resultado = "Medicamento no efectivo"
        else:
            resultado = "Medicamento fatal"

        print(f"\n--- RESULTADO FINAL ---")
        print(f"Porcentaje de células inertes: {porcentaje_inertes:.2f}%")
        print(f"Resultado: {resultado}")

    def ejecutar_directamente(self, experimento):
        print("\n--- EJECUTAR DIRECTAMENTE ---")
        rejilla = [fila.copy() for fila in experimento.tejido]  # Copia de la rejilla para no modificar la original
        parejas = experimento.parejas

        # Función para verificar si dos proteínas son una pareja que reacciona
        def es_pareja_reactiva(proteina1, proteina2):
            for pareja in parejas:
                if (proteina1 == pareja[0] and proteina2 == pareja[1]) or (proteina1 == pareja[1] and proteina2 == pareja[0]):
                    return True
            return False

        cambios = True

        # Ejecutar reacciones hasta que no haya más cambios
        while cambios:
            cambios = False

            # Crear una copia de la rejilla para no modificar la original durante la iteración
            nueva_rejilla = [fila.copy() for fila in rejilla]

            # Recorrer la rejilla para buscar parejas reactivas
            for i in range(len(rejilla)):
                for j in range(len(rejilla[i])):
                    # Verificar la celda a la derecha (horizontal)
                    if j < len(rejilla[i]) - 1 and es_pareja_reactiva(rejilla[i][j], rejilla[i][j + 1]):
                        if rejilla[i][j] != "INERTE" and rejilla[i][j + 1] != "INERTE":
                            nueva_rejilla[i][j] = "INERTE"
                            nueva_rejilla[i][j + 1] = "INERTE"
                            cambios = True

                    # Verificar la celda abajo (vertical)
                    if i < len(rejilla) - 1 and es_pareja_reactiva(rejilla[i][j], rejilla[i + 1][j]):
                        if rejilla[i][j] != "INERTE" and rejilla[i + 1][j] != "INERTE":
                            nueva_rejilla[i][j] = "INERTE"
                            nueva_rejilla[i + 1][j] = "INERTE"
                            cambios = True

            # Actualizar la rejilla
            rejilla = nueva_rejilla

        # Calcular el porcentaje de células inertes
        total_celdas = len(rejilla) * len(rejilla[0])
        celdas_inertes = sum(fila.count("INERTE") for fila in rejilla)
        porcentaje_inertes = (celdas_inertes / total_celdas) * 100

        # Determinar el resultado del medicamento
        if 30 <= porcentaje_inertes <= 60:
            resultado = "Medicamento exitoso"
        elif porcentaje_inertes < 30:
            resultado = "Medicamento no efectivo"
        else:
            resultado = "Medicamento fatal"

        print(f"\n--- RESULTADO FINAL ---")
        print(f"Porcentaje de células inertes: {porcentaje_inertes:.2f}%")
        print(f"Resultado: {resultado}")

    def mostrar_datos_estudiante(self):
        print("\n--- DATOS DEL ESTUDIANTE ---")
        print("Nombre: Mario Rene Merida Taracena")
        print("Carné: 202111134")
        print("Curso: Introducción a la Programación y Computación 2")
        print("Carrera: Ingeniería en Ciencias y Sistemas")
        print("Semestre: 7mo semestre - 2025")
        print("Enlace a la documentación: https://github.com/MarioRene/IPC2_Proyecto1_202111134.git")

# Menú principal
def menu_principal():
    sistema = SistemaExperimentos()
    while True:
        print("\n----------------- MENÚ PRINCIPAL -----------------")
        print("1. Inicializar el sistema")
        print("2. Cargar Catálogo de experimentos")
        print("3. Desarrollar Experimento")
        print("4. Mostrar Datos del Estudiante")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            sistema.inicializar_sistema()
        elif opcion == "2":
            ruta_archivo = input("Ingrese la ruta del archivo XML: ")
            sistema.cargar_catalogo(ruta_archivo)
        elif opcion == "3":
            sistema.desarrollar_experimento()
        elif opcion == "4":
            sistema.mostrar_datos_estudiante()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_principal()
