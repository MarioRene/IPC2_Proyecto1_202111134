import xml.etree.ElementTree as ET #import XML library
from graphviz import Digraph #import graph visualization library

# Estructuras de datos personalizadas
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

# Estructuras de datos personalizadas para el proyecto
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    # Métodos de la clase Matriz
    # Agregar valores a la matriz en la posición indicada
    def agregar(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            
    # Dibujar la matriz en forma de grafo
    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual.valor, end=" -> ")
            actual = actual.siguiente
        print("None")

# Clase para manejar las matrices
class Matriz:
    # Métodos de la clase Matriz
    # Constructor para inicializar una matriz de tamaño filas x columnas
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.datos = ListaEnlazada()  # Lista enlazada de filas
        for _ in range(filas):
            fila = ListaEnlazada()  # Cada fila es una lista enlazada de columnas
            for _ in range(columnas):
                fila.agregar("")  # Inicializar con valores vacíos
            self.datos.agregar(fila)

    # Obtener el valor en la posición indicada
    def obtener(self, fila, columna):
        fila_actual = self.datos.cabeza
        for _ in range(fila):
            fila_actual = fila_actual.siguiente
        nodo_columna = fila_actual.valor.cabeza
        for _ in range(columna):
            nodo_columna = nodo_columna.siguiente
        return nodo_columna.valor
    
    # Asignar el valor en la posición indicada
    def asignar(self, fila, columna, valor):
        fila_actual = self.datos.cabeza
        for _ in range(fila):
            fila_actual = fila_actual.siguiente
        nodo_columna = fila_actual.valor.cabeza
        for _ in range(columna):
            nodo_columna = nodo_columna.siguiente
        nodo_columna.valor = valor

    # Mostrar la matriz en forma de tabla
    def mostrar(self):
        fila_actual = self.datos.cabeza
        while fila_actual:
            columna_actual = fila_actual.valor.cabeza
            while columna_actual:
                print(columna_actual.valor, end=" ")
                columna_actual = columna_actual.siguiente
            print()
            fila_actual = fila_actual.siguiente

# Clase para manejar las parejas de proteínas
class Pareja:
    # Metodos de la clase Pareja
    # Constructor para inicializar una pareja con dos proteínas
    def __init__(self, proteina1, proteina2):
        self.proteina1 = proteina1
        self.proteina2 = proteina2
    
    # Método para mostrar la pareja de proteínas
    def __str__(self):
        return f"{self.proteina1} - {self.proteina2}"

# Clase para manejar los experimentos
class Experimento:
    # Métodos de la clase Experimento
    # Constructor para inicializar un experimento con una rejilla de proteínas y una lista enlazada de parejas
    def __init__(self, nombre, filas, columnas):
        self.nombre = nombre
        self.tejido = Matriz(filas, columnas)  # Usar la clase Matriz
        self.parejas = ListaEnlazada()  # Usar una lista enlazada para las parejas
    
    # Agregar una pareja a la lista enlazada de parejas
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
    # Métodos de la clase SistemaExperimentos
    # Constructor para inicializar el sistema con una lista enlazada para los experimentos
    def __init__(self):
        self.catalogo = ListaEnlazada()
    
    # Método para mostrar el catálogo de experimentos
    def inicializar_sistema(self):
        self.catalogo = ListaEnlazada()
        print("Sistema inicializado correctamente.")
    
    # Método para cargar el catálogo de experimentos desde un archivo XML
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
    
    # Método para agregar un nuevo experimento al catálogo
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
    
    # Método para agregar un nuevo experimento al catálogo de forma manual
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
    
    # Método para modificar un experimento existente en el catálogo
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
    
    # Método para ejecutar un experimento
    def ejecutar_experimento(self, experimento):
        print("\n--- EJECUTAR EXPERIMENTO ---")
        print("1. Modificar")
        print("2. Ejecutar Paso a Paso")
        print("3. Ejecutar directamente para obtener el resultado final")
        print("4. Resultados con Graphviz")
        print("5. Regresar al menú desarrollar experimento")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.modificar_experimento(experimento)
        elif opcion == "2":
            self.ejecutar_paso_a_paso(experimento)
        elif opcion == "3":
            self.ejecutar_directamente(experimento)
        elif opcion == "4":
            self.mostrar_resultados_con_graphviz(experimento)
        elif opcion == "5":
            return
        else:
            print("Opción inválida.")
    
    # Método para modificar un experimento existente en el catálogo
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

    # Método para ejecutar un experimento directamente
    def ejecutar_paso_a_paso(self, experimento):
        print("\n--- EJECUCIÓN PASO A PASO ---")
        rejilla = Matriz(experimento.tejido.filas, experimento.tejido.columnas)
        for i in range(experimento.tejido.filas):
            for j in range(experimento.tejido.columnas):
                rejilla.asignar(i, j, experimento.tejido.obtener(i, j))

        parejas = experimento.parejas

        # Método para verificar si dos proteínas forman una pareja reactiva
        def es_pareja_reactiva(proteina1, proteina2):
            actual = parejas.cabeza
            while actual:
                if (proteina1 == actual.valor.proteina1 and proteina2 == actual.valor.proteina2) or \
                   (proteina1 == actual.valor.proteina2 and proteina2 == actual.valor.proteina1):
                    return True
                actual = actual.siguiente
            return False

        # Método para mostrar la rejilla con el título indicado
        def mostrar_rejilla(rejilla, titulo):
            print(f"\n--- {titulo} ---")
            rejilla.mostrar()
            print("-------------------")

        paso = 0 # para mostrar la rejilla con el título indicado para cada paso de la ejecución
        cambios = True # para verificar si hay cambios en la rejilla

        mostrar_rejilla(rejilla, f"Paso {paso}")

        # Mientras haya cambios en la rejilla, se ejecuta el algoritmo de la reactividad de proteínas
        while cambios:
            cambios = False
            paso += 1

            # Crear una nueva matriz para almacenar los cambios
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
        
        # Calcular el porcentaje de las células inertes
        porcentaje_inertes = (celdas_inertes / total_celdas) * 100

        # Determinar el resultado final del experimento
        if 30 <= porcentaje_inertes <= 60: # Medicamento exitoso
            resultado = "Medicamento exitoso"
        elif porcentaje_inertes < 30: # Medicamento no efectivo
            resultado = "Medicamento no efectivo"
        else: # Medicamento fatal
            resultado = "Medicamento fatal"

        # Mostrar el resultado final del experimento
        print(f"\n--- RESULTADO FINAL ---")
        print(f"Porcentaje de células inertes: {porcentaje_inertes:.2f}%")
        print(f"Resultado: {resultado}")
    
    # Método para ejecutar un experimento directamente
    def ejecutar_directamente(self, experimento):
        print("\n--- EJECUTAR DIRECTAMENTE ---")
        rejilla = Matriz(experimento.tejido.filas, experimento.tejido.columnas)
        for i in range(experimento.tejido.filas):
            for j in range(experimento.tejido.columnas):
                rejilla.asignar(i, j, experimento.tejido.obtener(i, j))

        parejas = experimento.parejas

        # Método para verificar si dos proteínas forman una pareja reactiva
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

    # Método para mostrar los resultados de un experimento con Graphviz
    def mostrar_resultados_con_graphviz(self, experimento):
        print("\n--- RESULTADOS CON GRAPHVIZ ---")
        
        # Crear gráfico para el estado inicial
        dot_inicial = Digraph(comment='Estado Inicial')
        dot_inicial.attr('node', shape='square')
        
        # Añadir nodos y arcos para el estado inicial
        for i in range(experimento.tejido.filas):
            for j in range(experimento.tejido.columnas):
                valor = experimento.tejido.obtener(i, j)
                dot_inicial.node(f'{i}_{j}', label=valor)
        
        # Añadir arcos para las parejas reactivas
        for i in range(experimento.tejido.filas):
            for j in range(experimento.tejido.columnas):
                if j < experimento.tejido.columnas - 1:
                    dot_inicial.edge(f'{i}_{j}', f'{i}_{j+1}')
                if i < experimento.tejido.filas - 1:
                    dot_inicial.edge(f'{i}_{j}', f'{i+1}_{j}')
        
        # Generar y mostrar el gráfico del estado inicial
        dot_inicial.render('estado_inicial.gv', view=True)
        print("Gráfico del estado inicial generado y mostrado.")

        # Crear gráfico para el estado final
        rejilla_final = Matriz(experimento.tejido.filas, experimento.tejido.columnas)
        for i in range(experimento.tejido.filas):
            for j in range(experimento.tejido.columnas):
                rejilla_final.asignar(i, j, experimento.tejido.obtener(i, j))

        parejas = experimento.parejas

        # Método para verificar si dos proteínas forman una pareja reactiva
        def es_pareja_reactiva(proteina1, proteina2):
            actual = parejas.cabeza
            while actual:
                if (proteina1 == actual.valor.proteina1 and proteina2 == actual.valor.proteina2) or \
                   (proteina1 == actual.valor.proteina2 and proteina2 == actual.valor.proteina1):
                    return True
                actual = actual.siguiente
            return False

        cambios = True

        # Ejecutar el algoritmo de la reactividad de proteínas
        while cambios:
            cambios = False

            nueva_rejilla = Matriz(rejilla_final.filas, rejilla_final.columnas)
            for i in range(rejilla_final.filas):
                for j in range(rejilla_final.columnas):
                    nueva_rejilla.asignar(i, j, rejilla_final.obtener(i, j))

            for i in range(rejilla_final.filas):
                for j in range(rejilla_final.columnas):
                    if j < rejilla_final.columnas - 1 and es_pareja_reactiva(rejilla_final.obtener(i, j), rejilla_final.obtener(i, j + 1)):
                        if rejilla_final.obtener(i, j) != "INERTE" and rejilla_final.obtener(i, j + 1) != "INERTE":
                            nueva_rejilla.asignar(i, j, "INERTE")
                            nueva_rejilla.asignar(i, j + 1, "INERTE")
                            cambios = True

                    if i < rejilla_final.filas - 1 and es_pareja_reactiva(rejilla_final.obtener(i, j), rejilla_final.obtener(i + 1, j)):
                        if rejilla_final.obtener(i, j) != "INERTE" and rejilla_final.obtener(i + 1, j) != "INERTE":
                            nueva_rejilla.asignar(i, j, "INERTE")
                            nueva_rejilla.asignar(i + 1, j, "INERTE")
                            cambios = True

            rejilla_final = nueva_rejilla

        dot_final = Digraph(comment='Estado Final')
        dot_final.attr('node', shape='square')
        
        for i in range(rejilla_final.filas):
            for j in range(rejilla_final.columnas):
                valor = rejilla_final.obtener(i, j)
                dot_final.node(f'{i}_{j}', label=valor)
        
        for i in range(rejilla_final.filas):
            for j in range(rejilla_final.columnas):
                if j < rejilla_final.columnas - 1:
                    dot_final.edge(f'{i}_{j}', f'{i}_{j+1}')
                if i < rejilla_final.filas - 1:
                    dot_final.edge(f'{i}_{j}', f'{i+1}_{j}')
        
        dot_final.render('estado_final.gv', view=True)
        print("Gráfico del estado final generado y mostrado.")

    # Método para mostrar mi información
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
        print("5. Resultados con Graphviz")
        print("6. Salir")
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
            if sistema.catalogo.cabeza is None:
                print("No hay experimentos en el catálogo.")
            else:
                print("Experimentos disponibles:")
                actual = sistema.catalogo.cabeza
                while actual:
                    print(f"- {actual.valor.nombre}")
                    actual = actual.siguiente
                nombre_experimento = input("Seleccione el nombre del experimento: ")
                actual = sistema.catalogo.cabeza
                while actual:
                    if actual.valor.nombre == nombre_experimento:
                        sistema.mostrar_resultados_con_graphviz(actual.valor)
                        return
                    actual = actual.siguiente
                print("Experimento no encontrado.")
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

# Ejecutar el programa principal
if __name__ == "__main__":
    menu_principal()

