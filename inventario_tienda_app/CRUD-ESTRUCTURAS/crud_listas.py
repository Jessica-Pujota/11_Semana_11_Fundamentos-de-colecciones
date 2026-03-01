"""CRUD con LISTAS (LIST) Implementación de inventario utilizando listas como estructura principal"""

import sys
import os
# Ajustar path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Inventario.modelos.producto import Producto
class CrudListas:
    """
    Implementación CRUD usando LISTAS.
    Los productos se almacenan como objetos Producto en una lista.
    """
    
    def __init__(self, archivo_datos="inventario.txt"): #Inicializa el CRUD con listas
        self.archivo = archivo_datos
        self.productos = []  # Lista de objetos Producto
        self.nombre = "LISTAS"
        self.cargar_desde_archivo()
    
    def cargar_desde_archivo(self): #Carga los productos desde el archivo
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        producto = Producto.from_file_string(linea)
                        if producto:
                            self.productos.append(producto)
            print(f"📋 [{self.nombre}] {len(self.productos)} productos cargados")
        except FileNotFoundError:
            print(f"📄 [{self.nombre}] Archivo no encontrado, se creará nuevo")
        except Exception as e:
            print(f"✗ Error cargando: {e}")
    
    def guardar_en_archivo(self): #Guarda los productos en el archivo
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                for producto in self.productos:
                    f.write(producto.to_file_string())
            return True
        except Exception as e:
            print(f"✗ Error guardando: {e}")
            return False
    
    def buscar_indice_por_id(self, id_buscar): #Busca el índice de un producto por su ID
        for i, producto in enumerate(self.productos):
            if producto.id == id_buscar:
                return i
        return None
    
    def buscar_por_id(self, id_buscar): #Busca un producto por su ID
        indice = self.buscar_indice_por_id(id_buscar)
        if indice is not None:
            return self.productos[indice]
        return None
    
    # ===== OPERACIONES CRUD =====
    def create(self, id_producto, nombre, cantidad, precio): #Crea un nuevo producto
        print(f"\n🆕 [{self.nombre}] CREATE - Crear producto")
        
        # Verificar ID único
        if self.buscar_por_id(id_producto):
            print(f"  ✗ Error: Ya existe producto con ID {id_producto}")
            return False
        
        # Validar datos
        if cantidad < 0 or precio < 0:
            print(f"  ✗ Error: Cantidad y precio no pueden ser negativos")
            return False
        
        # Crear producto y añadir a la lista
        nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
        self.productos.append(nuevo_producto)
        posicion = len(self.productos) - 1
        
        # Guardar en archivo
        if self.guardar_en_archivo():
            print(f"  ✓ Producto '{nombre}' creado correctamente en posición {posicion}")
            print(f"  📊 Total en lista: {len(self.productos)} productos")
            return True
        else:
            self.productos.pop()
            print(f"  ✗ Error al guardar en archivo")
            return False
    
    def read(self, id_buscar=None): #Lee producto(s) del inventario
        if id_buscar:
            print(f"\n🔍 [{self.nombre}] READ - Buscar ID {id_buscar}")
            producto = self.buscar_por_id(id_buscar)
            if producto:
                print(f"  ✓ Encontrado: {producto}")
                return [producto]
            else:
                print(f"  ✗ No se encontró producto con ID {id_buscar}")
                return []
        else:
            print(f"\n📋 [{self.nombre}] READ - Listar todos")
            return self.productos.copy()
    
    def update(self, id_producto, cantidad=None, precio=None): #Actualiza un producto existente.
        print(f"\n📝 [{self.nombre}] UPDATE - Producto ID {id_producto}")
        
        indice = self.buscar_indice_por_id(id_producto)
        if indice is None:
            print(f"  ✗ No existe producto con ID {id_producto}")
            return False
        
        producto = self.productos[indice]
        
        # Mostrar valores actuales
        print(f"  📌 Valores actuales: Cant={producto.cantidad}, Precio=${producto.precio:.2f}")
        try:
            # Actualizar valores
            if cantidad is not None:
                if cantidad < 0:
                    raise ValueError("La cantidad no puede ser negativa")
                producto.cantidad = cantidad
            
            if precio is not None:
                if precio < 0:
                    raise ValueError("El precio no puede ser negativo")
                producto.precio = precio
            
            print(f"  📌 Nuevos valores: Cant={producto.cantidad}, Precio=${producto.precio:.2f}")
            
            # Guardar en archivo
            if self.guardar_en_archivo():
                print(f"  ✓ Producto ID {id_producto} actualizado correctamente")
                return True
            else:
                print(f"  ✗ Error al guardar en archivo")
                return False
        except ValueError as e:
            print(f"  ✗ Error: {e}")
            return False
    def delete(self, id_producto): #Elimina un producto del inventario
        print(f"\n🗑️ [{self.nombre}] DELETE - Producto ID {id_producto}")
        indice = self.buscar_indice_por_id(id_producto)
        if indice is None:
            print(f"  ✗ No existe producto con ID {id_producto}")
            return False
        producto_eliminado = self.productos.pop(indice)
        print(f"  📌 Eliminando: {producto_eliminado.nombre}")
        
        if self.guardar_en_archivo():
            print(f"  ✓ Producto ID {id_producto} eliminado correctamente")
            return True
        else:
            self.productos.insert(indice, producto_eliminado)
            print(f"  ✗ Error al guardar - producto restaurado")
            return False
    
    # ===== OPERACIONES ESPECÍFICAS DE LISTAS =====
    def ordenar_por_precio(self, descendente=False): #Ordena los productos por precio
        self.productos.sort(key=lambda p: p.precio, reverse=descendente)
        self.guardar_en_archivo()
        print(f"\n📊 [{self.nombre}] Lista ordenada por precio")
        return self.productos
    def ordenar_por_cantidad(self, descendente=False): #Ordena los productos por cantidad
        self.productos.sort(key=lambda p: p.cantidad, reverse=descendente)
        self.guardar_en_archivo()
        print(f"\n📊 [{self.nombre}] Lista ordenada por cantidad")
        return self.productos
    def obtener_primeros_n(self, n): #Obtiene los primeros n productos
        return self.productos[:n]
    def obtener_ultimos_n(self, n): #Obtiene los últimos n productos
        return self.productos[-n:] if n > 0 else []
    def buscar_por_rango_precio(self, min_precio, max_precio): #Busca productos en un rango de precio
        resultados = [p for p in self.productos if min_precio <= p.precio <= max_precio]
        print(f"\n🔍 [{self.nombre}] Productos entre ${min_precio} y ${max_precio}: {len(resultados)}")
        return resultados
    def __str__(self):
        return f"CrudListas({len(self.productos)} productos)"
# Función de prueba
def test_crud_listas(): #Prueba básica del CRUD con listas
    print("\n" + "="*60)
    print("🧪 PRUEBA CRUD CON LISTAS")
    print("="*60)
    # Crear instancia
    crud = CrudListas("test_listas.txt")
    # CREATE
    print("\n📝 Creando productos...")
    crud.create(1, "Laptop Gamer", 10, 1200.00)
    crud.create(2, "Mouse RGB", 50, 35.50)
    crud.create(3, "Teclado Mecánico", 30, 89.99)
    crud.create(4, "Monitor 4K", 15, 450.00)
    # READ
    print("\n📋 Listando productos...")
    for p in crud.read():
        print(f"  {p}")
    # UPDATE
    print("\n📝 Actualizando producto...")
    crud.update(2, cantidad=45, precio=29.99)
    # Operaciones de lista
    print("\n📊 Probando operaciones de lista...")
    crud.ordenar_por_precio()
    print("  Productos ordenados por precio:")
    for p in crud.obtener_primeros_n(3):
        print(f"    {p}")
    # Búsqueda por rango
    crud.buscar_por_rango_precio(50, 500)
    # DELETE
    print("\n🗑️ Eliminando producto...")
    crud.delete(4)
    # READ final
    print("\n📋 Productos finales:")
    for p in crud.read():
        print(f"  {p}")
    print("\n" + "="*60)
    print("✅ PRUEBA COMPLETADA")
    print("="*60)
if __name__ == "__main__":
    test_crud_listas()