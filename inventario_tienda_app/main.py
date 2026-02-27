"""
Sistema de Gestión de Inventarios para Tienda
Autor: Sistema desarrollado para tarea de POO
Descripción: Programa principal con menú interactivo para gestionar inventario
"""
from servicios.inventario import Inventario

class MenuInventario: #clase que maneja la interfaz de usuario del sistema de inventario    
    def __init__(self): #Inicializa el menú con una instancia del inventario
        self.inventario = Inventario()
        self.opciones = {
            '1': self.añadir_producto,
            '2': self.eliminar_producto,
            '3': self.actualizar_producto,
            '4': self.buscar_producto,
            '5': self.mostrar_todos,
            '6': self.salir
        }
    def mostrar_menu(self): #Muestra el menú principal al usuario
        print("\n" + "="*50)
        print("SISTEMA DE GESTIÓN DE INVENTARIOS")
        print("="*50)
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")
        print("="*50)
    
    def ejecutar(self): #Ejecuta el bucle principal del programa
        while True:
            try:
                self.mostrar_menu()
                opcion = input("Seleccione una opción (1-6): ").strip() 
                if opcion in self.opciones:
                    self.opciones[opcion]()
                else:
                    print("Opción no válida. Por favor, seleccione 1-6.")     
            except KeyboardInterrupt:
                print("\n\nSaliendo del sistema...")
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
    def añadir_producto(self): #Añade un nuevo producto al inventario
        print("\n--- AÑADIR NUEVO PRODUCTO ---")
        try:
            nombre = input("Nombre del producto: ").strip()
            if not nombre:
                print("Error: El nombre no puede estar vacío")
                return
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: $"))
            producto = self.inventario.añadir_producto(nombre, cantidad, precio)
            print(f"Producto añadido exitosamente: {producto}")
        except ValueError as e:
            print(f" Error: {e}")
        except Exception as e:
            print(f" Error inesperado: {e}")
    
    def eliminar_producto(self): #Elimina un producto por su ID
        print("\n--- ELIMINAR PRODUCTO ---")
        try:
            id_producto = int(input("ID del producto a eliminar: "))
            if self.inventario.eliminar_producto(id_producto):
                print(f"Producto con ID {id_producto} eliminado exitosamente")
            else:
                print(f"No se encontró producto con ID {id_producto}")      
        except ValueError:
            print("Error: El ID debe ser un número entero") 
    def actualizar_producto(self): #Actualiza la cantidad y/o precio de un producto
        print("\n--- ACTUALIZAR PRODUCTO ---")
        try:
            id_producto = int(input("ID del producto a actualizar: "))
            producto = self.inventario.obtener_producto(id_producto)
            if not producto:
                print(f"No se encontró producto con ID {id_producto}")
                return
            print(f"Producto actual: {producto}")
            print("(Deje en blanco para no modificar)")
            cantidad_str = input("Nueva cantidad: ").strip()
            precio_str = input("Nuevo precio: $").strip()
            cantidad = int(cantidad_str) if cantidad_str else None
            precio = float(precio_str) if precio_str else None
            if self.inventario.actualizar_producto(id_producto, cantidad, precio):
                print(f"Producto actualizado: {self.inventario.obtener_producto(id_producto)}")
            else:
                print("Error al actualizar el producto")       
        except ValueError as e:
            print(f"Error: {e}")
    def buscar_producto(self): #Busca productos por nombre
        print("\n--- BUSCAR PRODUCTO ---")
        nombre = input("Ingrese el nombre o parte del nombre a buscar: ").strip()
        if not nombre:
            print("Error: Debe ingresar un término de búsqueda")
            return
        resultados = self.inventario.buscar_por_nombre(nombre)
        if resultados:
            print(f"\n📦 Se encontraron {len(resultados)} producto(s):")
            print("-" * 50)
            for producto in sorted(resultados, key=lambda p: p.nombre):
                print(producto)
        else:
            print("No se encontraron productos con ese nombre")
    def mostrar_todos(self): #Muestra todos los productos del inventario
        print("\n--- INVENTARIO COMPLETO ---")
        productos = self.inventario.mostrar_todos()
        if productos:
            print(f"📊 Total de productos: {len(productos)}")
            print("-" * 50)
            for producto in productos:
                print(producto)
            # Mostrar estadísticas usando tuplas para datos inmutables
            if productos:
                total_valor = sum(p.cantidad * p.precio for p in productos)
                producto_mas_caro = max(productos, key=lambda p: p.precio)
                producto_mas_stock = max(productos, key=lambda p: p.cantidad)
                
                print("\n📈 Estadísticas:")
                print(f"Valor total del inventario: ${total_valor:.2f}")
                print(f"Producto más caro: {producto_mas_caro.nombre} (${producto_mas_caro.precio:.2f})")
                print(f"Producto con más stock: {producto_mas_stock.nombre} ({producto_mas_stock.cantidad} unidades)")
        else:
            print("📭 El inventario está vacío")
    def salir(self):
        """Sale del programa"""
        print("\n👋 ¡Gracias por usar el sistema de inventarios!")
        exit()
if __name__ == "__main__":
    # Crear y ejecutar el menú
    menu = MenuInventario()
    menu.ejecutar()