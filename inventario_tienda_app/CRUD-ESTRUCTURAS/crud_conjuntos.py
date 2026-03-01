""" CRUD con CONJUNTOS (SET) Implementación de inventario utilizando conjuntos como estructura principal"""
import sys
import os

# Ajustar path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Inventario.modelos.producto import Producto
class CrudConjuntos:
    """
    Implementación CRUD usando CONJUNTOS.
    Los productos se almacenan como tuplas inmutables en un set.
    """
    def __init__(self, archivo_datos="inventario.txt"): #Inicializa el CRUD con conjuntos.        
        self.archivo = archivo_datos
        self.productos = set()  # Set de tuplas (id, nombre, cantidad, precio)
        self.nombre = "CONJUNTOS"
        self.cargar_desde_archivo()
    
    def _producto_a_tupla(self, producto): #Convierte el producto a tupla para el set
        return (producto.id, producto.nombre, producto.cantidad, producto.precio)
    
    def _tupla_a_producto(self, tupla): #Convierte una tupla a objeto Producto
        return Producto(tupla[0], tupla[1], tupla[2], tupla[3])
    
    def cargar_desde_archivo(self): #Carga los productos desde el archivo
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        partes = linea.strip().split(',')
                        if len(partes) == 4:
                            tupla = (int(partes[0]), partes[1], int(partes[2]), float(partes[3]))
                            self.productos.add(tupla)
            print(f"📚 [{self.nombre}] {len(self.productos)} productos cargados")
        except FileNotFoundError:
            print(f"📄 [{self.nombre}] Archivo no encontrado, se creará nuevo")
        except Exception as e:
            print(f"✗ Error cargando: {e}")
    
    def guardar_en_archivo(self): #Guarda los productos en el archivo
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                for tupla in sorted(self.productos, key=lambda x: x[0]):
                    f.write(f"{tupla[0]},{tupla[1]},{tupla[2]},{tupla[3]:.2f}\n")
            return True
        except Exception as e:
            print(f"✗ Error guardando: {e}")
            return False
    
    def buscar_por_id(self, id_buscar): #Busca un producto por su ID
        for producto in self.productos:
            if producto[0] == id_buscar:
                return producto
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
        
        # Crear tupla y añadir al set
        nuevo_producto = (id_producto, nombre, cantidad, precio)
        self.productos.add(nuevo_producto)
        
        # Guardar en archivo
        if self.guardar_en_archivo():
            print(f"  ✓ Producto '{nombre}' creado correctamente")
            print(f"  📊 Total en conjunto: {len(self.productos)} productos")
            return True
        else:
            self.productos.remove(nuevo_producto)
            print(f"  ✗ Error al guardar en archivo")
            return False
    
    def read(self, id_buscar=None): #Lee producto(s) del inventario
        if id_buscar:
            print(f"\n🔍 [{self.nombre}] READ - Buscar ID {id_buscar}")
            producto = self.buscar_por_id(id_buscar)
            if producto:
                print(f"  ✓ Encontrado: ID:{producto[0]} | {producto[1]} | Cant:{producto[2]} | ${producto[3]:.2f}")
                return [producto]
            else:
                print(f"  ✗ No se encontró producto con ID {id_buscar}")
                return []
        else:
            print(f"\n📋 [{self.nombre}] READ - Listar todos")
            return sorted(list(self.productos), key=lambda x: x[0])
    
    def update(self, id_producto, cantidad=None, precio=None): #Actualiza un producto existente
        print(f"\n📝 [{self.nombre}] UPDATE - Producto ID {id_producto}")
        
        producto_viejo = self.buscar_por_id(id_producto)
        if not producto_viejo:
            print(f"  ✗ No existe producto con ID {id_producto}")
            return False
        
        # Preparar nuevos valores
        id_val, nombre, cant_old, prec_old = producto_viejo
        nueva_cant = cantidad if cantidad is not None else cant_old
        nuevo_precio = precio if precio is not None else prec_old
        
        # Validaciones
        if nueva_cant < 0 or nuevo_precio < 0:
            print(f"  ✗ Error: Cantidad y precio no pueden ser negativos")
            return False
        
        # Crear nuevo producto
        producto_nuevo = (id_val, nombre, nueva_cant, nuevo_precio)
        
        # Mostrar cambios
        print(f"  📌 Valores actuales: Cant={cant_old}, Precio=${prec_old:.2f}")
        print(f"  📌 Nuevos valores: Cant={nueva_cant}, Precio=${nuevo_precio:.2f}")
        
        # Reemplazar en el set
        self.productos.remove(producto_viejo)
        self.productos.add(producto_nuevo)
        # Guardar
        if self.guardar_en_archivo():
            print(f"  ✓ Producto ID {id_producto} actualizado correctamente")
            return True
        else:
            # Revertir cambios
            self.productos.add(producto_viejo)
            self.productos.remove(producto_nuevo)
            print(f"  ✗ Error al guardar - cambios revertidos")
            return False
    
    def delete(self, id_producto): #Elimina un producto del inventario
        print(f"\n🗑️ [{self.nombre}] DELETE - Producto ID {id_producto}")
        
        producto = self.buscar_por_id(id_producto)
        if not producto:
            print(f"  ✗ No existe producto con ID {id_producto}")
            return False
        print(f"  📌 Eliminando: {producto[1]}")
        self.productos.remove(producto)
        
        if self.guardar_en_archivo():
            print(f"  ✓ Producto ID {id_producto} eliminado correctamente")
            return True
        else:
            self.productos.add(producto)
            print(f"  ✗ Error al guardar - producto restaurado")
            return False
    
    # ===== OPERACIONES ESPECÍFICAS DE CONJUNTOS =====
    def operaciones_conjuntos(self): #Demuestra operaciones características de sets
        print(f"\n🔷 [{self.nombre}] OPERACIONES DE CONJUNTOS:")
        
        if len(self.productos) < 2:
            print("  ⚠ Se necesitan más productos para demostrar operaciones")
            return
        # Conjunto de productos con cantidad > 10
        conj_a = {p for p in self.productos if p[2] > 10}
        # Conjunto de productos con precio < 100
        conj_b = {p for p in self.productos if p[3] < 100}
        
        print(f"\n  📊 Conjunto A (cantidad > 10): {len(conj_a)} productos")
        print(f"  📊 Conjunto B (precio < $100): {len(conj_b)} productos")
        
        # UNIÓN
        union = conj_a | conj_b
        print(f"\n  🔗 UNIÓN (A ∪ B): {len(union)} productos")
        
        # INTERSECCIÓN
        interseccion = conj_a & conj_b
        print(f"  ⚡ INTERSECCIÓN (A ∩ B): {len(interseccion)} productos")
        if interseccion:
            print(f"     Productos que cumplen ambas condiciones:")
            for p in interseccion:
                print(f"     - {p[1]}: {p[2]} und, ${p[3]:.2f}")
        # DIFERENCIA
        diferencia = conj_a - conj_b
        print(f"  ➖ DIFERENCIA (A - B): {len(diferencia)} productos")
    
    def __str__(self):
        return f"CrudConjuntos({len(self.productos)} productos)"
    
# Función de prueba
def test_crud_conjuntos(): #Prueba básica del CRUD con conjuntos
    print("\n" + "="*60)
    print("🧪 PRUEBA CRUD CON CONJUNTOS")
    print("="*60)
    
    # Crear instancia
    crud = CrudConjuntos("test_conjuntos.txt")
    # CREATE
    print("\n📝 Creando productos...")
    crud.create(1, "Laptop Gamer", 10, 1200.00)
    crud.create(2, "Mouse RGB", 50, 35.50)
    crud.create(3, "Teclado Mecánico", 30, 89.99)
    
    # READ
    print("\n📋 Listando productos...")
    for p in crud.read():
        print(f"  {p}")
    # UPDATE
    print("\n📝 Actualizando producto...")
    crud.update(2, cantidad=45, precio=29.99)
    
    # DELETE
    print("\n🗑️ Eliminando producto...")
    crud.delete(3)
    
    # READ final
    print("\n📋 Productos finales:")
    for p in crud.read():
        print(f"  {p}")
    
    # Operaciones de conjuntos
    crud.operaciones_conjuntos()
    print("\n" + "="*60)
    print("✅ PRUEBA COMPLETADA")
    print("="*60)
if __name__ == "__main__":
    test_crud_conjuntos()