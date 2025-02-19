class NodoExperimento:
    def __init__(self, id, nombre, descripcion):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.siguiente = None

class ListaExperimentos:
    def __init__(self):
        self.cabeza = None
    
    def agregar_experimento(self, id, nombre, descripcion):
        nuevo_nodo = NodoExperimento(id, nombre, descripcion)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        print(f"Experimento '{nombre}' cargado con éxito.")
    
    def mostrar_experimentos(self):
        actual = self.cabeza
        if not actual:
            print("No hay experimentos cargados.")
            return
        while actual:
            print(f"ID: {actual.id}, Nombre: {actual.nombre}, Descripción: {actual.descripcion}")
            actual = actual.siguiente

class Sistema:
    def __init__(self):
        self.catalogo = ListaExperimentos()
    
    def cargar_experimentos(self):
        ruta = input("Ingrese la ruta del archivo XML: ")
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(ruta)
            root = tree.getroot()
            for idx, exp in enumerate(root.findall('experimento')):
                id = exp.find('id').text
                nombre = exp.find('nombre').text
                descripcion = exp.find('descripcion').text
                self.catalogo.agregar_experimento(id, nombre, descripcion)
            print("Experimentos cargados con éxito.")
        except Exception as e:
            print(f"Error al cargar el archivo XML: {e}")
    
    def desarrollar_experimento(self):
        while True:
            print("\n----------------- DESARROLLAR EXPERIMENTO -----------------")
            print("1. Crear manualmente")
            print("2. Cargar desde el catálogo")
            print("3. Regresar al menú principal")
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                id = input("Ingrese el ID del experimento: ")
                nombre = input("Ingrese el nombre del experimento: ")
                descripcion = input("Ingrese la descripción: ")
                self.catalogo.agregar_experimento(id, nombre, descripcion)
            elif opcion == "2":
                self.catalogo.mostrar_experimentos()
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Intente nuevamente.")
    
    def menu_principal(self):
        while True:
            print("\n----------------- MENÚ PRINCIPAL -----------------")
            print("1. Inicializar el sistema")
            print("2. Cargar a Catálogo de experimentos")
            print("3. Desarrollar Experimento")
            print("4. Mostrar Datos del Estudiante")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                print("Sistema inicializado.")
            elif opcion == "2":
                self.cargar_experimentos()
            elif opcion == "3":
                self.desarrollar_experimento()
            elif opcion == "4":
                print("Mostrando datos del estudiante...")
            elif opcion == "5":
                print("Saliendo del sistema.")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    sistema = Sistema()
    sistema.menu_principal()
