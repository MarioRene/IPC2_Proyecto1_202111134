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

class Matriz:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.datos = ListaEnlazada()  # Lista enlazada de filas
        for _ in range(filas):
            fila = ListaEnlazada()  # Cada fila es una lista enlazada de columnas
            for _ in range(columnas):
                fila.agregar("")  # Inicializar con valores vacíos
            self.datos.agregar(fila)

    def obtener(self, fila, columna):
        fila_actual = self.datos.cabeza
        for _ in range(fila):
            fila_actual = fila_actual.siguiente
        nodo_columna = fila_actual.valor.cabeza
        for _ in range(columna):
            nodo_columna = nodo_columna.siguiente
        return nodo_columna.valor

    def asignar(self, fila, columna, valor):
        fila_actual = self.datos.cabeza
        for _ in range(fila):
            fila_actual = fila_actual.siguiente
        nodo_columna = fila_actual.valor.cabeza
        for _ in range(columna):
            nodo_columna = nodo_columna.siguiente
        nodo_columna.valor = valor

    def mostrar(self):
        fila_actual = self.datos.cabeza
        while fila_actual:
            columna_actual = fila_actual.valor.cabeza
            while columna_actual:
                print(columna_actual.valor, end=" ")
                columna_actual = columna_actual.siguiente
            print()
            fila_actual = fila_actual.siguiente

class Pareja:
    def __init__(self, proteina1, proteina2):
        self.proteina1 = proteina1
        self.proteina2 = proteina2

    def __str__(self):
        return f"{self.proteina1} - {self.proteina2}"

# Clase para manejar los experimentos
class Experimento:
    def __init__(self, nombre, filas, columnas):
        self.nombre = nombre
        self.tejido = Matriz(filas, columnas)  # Usar la clase Matriz
        self.parejas = ListaEnlazada()  # Usar una lista enlazada para las parejas

    def mostrar(self):
        print(f"Experimento: {self.nombre}")
        print("Rejilla de proteínas:")
        self.tejido.mostrar()
        print("Parejas de proteínas:")
        actual = self.parejas.cabeza
        while actual:
            print(actual.valor)
            actual = actual.siguiente

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
                nuevo_experimento = Experimento(nombre, filas, columnas)

                # Cargar la rejilla de proteínas
                rejilla = tejido.find('rejilla').text.strip().split('\n')
                for i in range(filas):
                    fila = rejilla[i].strip().split()
                    for j in range(columnas):
                        nuevo_experimento.tejido.asignar(i, j, fila[j])

                # Cargar las parejas de proteínas
                proteinas = experimento.find('proteinas')
                for pareja in proteinas.findall('pareja'):
                    proteina1, proteina2 = pareja.text.strip().split()
                    nuevo_experimento.parejas.agregar(Pareja(proteina1, proteina2))

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
        nuevo_experimento = Experimento(nombre, filas, columnas)

        print("Ingrese la rejilla de proteínas (separadas por espacios):")
        for i in range(filas):
            fila = input(f"Ingrese la fila {i + 1}: ").strip().split()
            for j in range(columnas):
                nuevo_experimento.tejido.asignar(i, j, fila[j])

        print("Ingrese las parejas de proteínas (separadas por espacios, una por línea, 'fin' para terminar):")
        while True:
            pareja = input().strip()
            if pareja.lower() == 'fin':
                break
            proteina1, proteina2 = pareja.split()
            nuevo_experimento.parejas.agregar(Pareja(proteina1, proteina2))

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
            for i in range(experimento.tejido.filas):
                fila = input(f"Ingrese la fila {i + 1} (separada por espacios): ").strip().split()
                for j in range(experimento.tejido.columnas):
                    experimento.tejido.asignar(i, j, fila[j])
            print("Rejilla de proteínas actualizada.")

        elif opcion == "3":
            print("Ingrese las nuevas parejas de proteínas (separadas por espacios, una por línea, 'fin' para terminar):")
            experimento.parejas = ListaEnlazada()  # Reiniciar la lista de parejas
            while True:
                pareja = input().strip()
                if pareja.lower() == 'fin':
                    break
                proteina1, proteina2 = pareja.split()
                experimento.parejas.agregar(Pareja(proteina1, proteina2))
            print("Parejas de proteínas actualizadas.")

        elif opcion == "4":
            return  # Regresar al menú anterior

        else:
            print("Opción inválida.")

    def ejecutar_paso_a_paso(self, experimento):
        print("\n--- EJECUCIÓN PASO A PASO ---")
        rejilla = Matriz(experimento.tejido.filas, experimento.tejido.columnas)
        for i in range(experimento.tejido.filas):
            for j in range(experimento.tejido.columnas):
                rejilla.asignar(i, j, experimento.tejido.obtener(i, j))

        parejas = experimento.parejas

        def es_pareja_reactiva(proteina1, proteina2):
            actual = parejas.cabeza
            while actual:
                if (proteina1 == actual.valor.proteina1 and proteina2 == actual.valor.proteina2) or \
                   (proteina1 == actual.valor.proteina2 and proteina2 == actual.valor.proteina1):
                    return True
                actual = actual.siguiente
            return False

        def mostrar_rejilla(rejilla, titulo):
            print(f"\n--- {titulo} ---")
            rejilla.mostrar()
            print("-------------------")

        paso = 0
        cambios = True

        mostrar_rejilla(rejilla, f"Paso {paso}")

        while cambios:
            cambios = False
            paso += 1

            nueva_rejilla = Matriz(rejilla.filas, rejilla.columnas)
            for i in range(rejilla.filas):
                for j in range(rejilla.columnas):
                    nueva_rejilla.asignar(i, j, rejilla.obtener(i, j))

            for i in range(rejilla.filas):
                for j in range(rejilla.columnas):
                    if j < rejilla.columnas - 1 and es_pareja_reactiva(rejilla.obtener(i, j), rejilla.obtener(i, j + 1)):
                        if rejilla.obtener(i, j) != "INERTE" and rejilla.obtener(i, j + 1) != "INERTE":
                            nueva_rejilla.asignar(i, j, "INERTE")
                            nueva_rejilla.asignar(i, j + 1, "INERTE")
                            cambios = True

                    if i < rejilla.filas - 1 and es_pareja_reactiva(rejilla.obtener(i, j), rejilla.obtener(i + 1, j)):
                        if rejilla.obtener(i, j) != "INERTE" and rejilla.obtener(i + 1, j) != "INERTE":
                            nueva_rejilla.asignar(i, j, "INERTE")
                            nueva_rejilla.asignar(i + 1, j, "INERTE")
                            cambios = True

            rejilla = nueva_rejilla

            if cambios:
                mostrar_rejilla(rejilla, f"Paso {paso}")

        total_celdas = rejilla.filas * rejilla.columnas
        celdas_inertes = 0
        for i in range(rejilla.filas):
            for j in range(rejilla.columnas):
                if rejilla.obtener(i, j) == "INERTE":
                    celdas_inertes += 1

        porcentaje_inertes = (celdas_inertes / total_celdas) * 100

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
        rejilla = Matriz(experimento.tejido.filas, experimento.tejido.columnas)
        for i in range(experimento.tejido.filas):
            for j in range(experimento.tejido.columnas):
                rejilla.asignar(i, j, experimento.tejido.obtener(i, j))

        parejas = experimento.parejas

        def es_pareja_reactiva(proteina1, proteina2):
            actual = parejas.cabeza
            while actual:
                if (proteina1 == actual.valor.proteina1 and proteina2 == actual.valor.proteina2) or \
                   (proteina1 == actual.valor.proteina2 and proteina2 == actual.valor.proteina1):
                    return True
                actual = actual.siguiente
            return False

        cambios = True

        while cambios:
            cambios = False

            nueva_rejilla = Matriz(rejilla.filas, rejilla.columnas)
            for i in range(rejilla.filas):
                for j in range(rejilla.columnas):
                    nueva_rejilla.asignar(i, j, rejilla.obtener(i, j))

            for i in range(rejilla.filas):
                for j in range(rejilla.columnas):
                    if j < rejilla.columnas - 1 and es_pareja_reactiva(rejilla.obtener(i, j), rejilla.obtener(i, j + 1)):
                        if rejilla.obtener(i, j) != "INERTE" and rejilla.obtener(i, j + 1) != "INERTE":
                            nueva_rejilla.asignar(i, j, "INERTE")
                            nueva_rejilla.asignar(i, j + 1, "INERTE")
                            cambios = True

                    if i < rejilla.filas - 1 and es_pareja_reactiva(rejilla.obtener(i, j), rejilla.obtener(i + 1, j)):
                        if rejilla.obtener(i, j) != "INERTE" and rejilla.obtener(i + 1, j) != "INERTE":
                            nueva_rejilla.asignar(i, j, "INERTE")
                            nueva_rejilla.asignar(i + 1, j, "INERTE")
                            cambios = True

            rejilla = nueva_rejilla

        total_celdas = rejilla.filas * rejilla.columnas
        celdas_inertes = 0
        for i in range(rejilla.filas):
            for j in range(rejilla.columnas):
                if rejilla.obtener(i, j) == "INERTE":
                    celdas_inertes += 1

        porcentaje_inertes = (celdas_inertes / total_celdas) * 100

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
        print("Nombre:                                                   Mario Rene Merida Taracena")
        print("Carné:                                                                     202111134")
        print("Curso:                                Introducción a la Programación y Computación 2")
        print("Carrera:                                           Ingeniería en Ciencias y Sistemas")
        print("Semestre:                                                        1er semestre - 2025")
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
    
