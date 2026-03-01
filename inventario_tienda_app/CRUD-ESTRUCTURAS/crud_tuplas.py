""" CRUD con TUPLAS (TUPLE) Implementación de inventario utilizando tuplas como estructura principal."""

import sys
import os

# Ajustar path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
class CrudTuplas:
    """
    Implementación CRUD usando TUPLAS.
    Las tuplas son INMUTABLES, por lo que cada modificación crea una nueva lista.
    """
    
    def __init__(self, archivo_datos="inventario.txt"): #Inicializa el CRUD con tuplas.
        self.archivo = archivo_datos
        self.productos = []  # Lista de tuplas (id, nombre, cantidad, precio)
        self.nombre = "TUPLAS"
        self.cargar_desde_archivo()
    
    def cargar_desde_archivo(self):
        """Carga los productos desde el archivo"""
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        partes = linea.strip().split(',')
                        if len(partes) == 4:
                            tupla = (int(partes[0]), partes[1], int(partes[2]), float(partes[3]))
                            self.productos.append(tupla)
            print(f"🔷 [{self.nombre}] {len(self.productos)} productos cargados")
        except FileNotFoundError:
            print(f"📄 [{self.nombre}] Archivo no encontrado")
        except Exception as e:
            print(f"✗ Error cargando: {e}")
    
    def guardar_en_archivo(self):
        """Guarda los productos en el archivo"""
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                for tupla in sorted(self.productos, key=lambda x: x[0]):
                    f.write(f"{tupla[0]},{tupla[1]},{tupla[2]},{tupla[3]:.2f}\n")
            return True
        except Exception as e:
            print(f"✗ Error guardando: {e}")
            return False
    
    def buscar_por_id(self, id_buscar):
        """Busca un producto por su ID"""
        for producto in self.productos:
            if producto[0] == id_buscar:
                return producto
        return None
    
    # ===== OPERACIONES CRUD =====
    
    def create(self, id_producto, nombre, cantidad, precio):
        """
        Crea un nuevo producto.
        Las tuplas son INMUTABLES, pero podemos añadir a la lista.
        """
        print(f"\n🆕 [{self.nombre}] CREATE - Crear producto")
        
        # Verificar ID único
        if self.buscar_por_id(id_producto):
            print(f"  ✗ Error: Ya existe producto con ID {id_producto}")
            return False
        
        # Validar datos
        if cantidad < 0 or precio < 0:
            print(f"  ✗ Error: Cantidad y precio no pueden ser negativos")
            return False
        
        # Crear nueva tupla (INMUTABLE)
        nuevo_producto = (id_producto, nombre, cantidad, precio)
        
        # Añadir a la lista
        self.productos.append(nuevo_producto)
        
        # Guardar
        if self.guardar_en_archivo():
            print(f"  ✓ Producto '{nombre}' creado correctamente (tupla inmutable)")
            return True
        else:
            self.productos.remove(nuevo_producto)
            return False
    
    def read(self, id_buscar=None):
        """
        Lee producto(s) del inventario.
        """
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
            return sorted(self.productos, key=lambda x: x[0])
    
    def update(self, id_producto, cantidad=None, precio=None):
        """Actualiza un producto existente.
        Como las tuplas son INMUTABLES, creamos una nueva.
        """
        print(f"\n📝 [{self.nombre}] UPDATE - Producto ID {id_producto}")
        
        # Buscar producto
        indice = None
        producto_viejo = None
        for i, p in enumerate(self.productos):
            if p[0] == id_producto:
                indice = i
                producto_viejo = p
                break
        
        if producto_viejo is None:
            print(f"  ✗ No existe producto con ID {id_producto}")
            return False
        
        # Preparar nuevos valores
        id_val, nombre, cant_old, prec_old = producto_viejo
        nueva_cant = cantidad if cantidad is not None else cant_old
        nuevo_precio = precio if precio is not None else prec_old
        
        # Validaciones
        if nueva_cant < 0 or nuevo_precio < 0:
            print(f"  ✗ Error: Valores negativos no permitidos")
            return False
        
        # Crear NUEVA tupla (INMUTABLE)
        producto_nuevo = (id_val, nombre, nueva_cant, nuevo_precio)
        
        print(f"  📌 Valores actuales: Cant={cant_old}, Precio=${prec_old:.2f}")
        print(f"  📌 Nuevos valores: Cant={nueva_cant}, Precio=${nuevo_precio:.2f}")
        print(f"  📌 Nota: Se creará una NUEVA tupla (inmutabilidad)")
        
        # Reemplazar (creando nueva lista)
        self.productos[indice] = producto_nuevo
        
        # Guardar
        if self.guardar_en_archivo():
            print(f"  ✓ Producto ID {id_producto} actualizado (nueva tupla creada)")
            return True
        else:
            self.productos[indice] = producto_viejo
            return False
    
    def delete(self, id_producto):
        """
        Elimina un producto del inventario.
        """
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
            self.productos.append(producto)
            return False
    
    def demostrar_inmutabilidad(self):
        """Demuestra que las tuplas son inmutables"""
        print(f"\n🔒 [{self.nombre}] DEMOSTRACIÓN DE INMUTABILIDAD:")
        
        if not self.productos:
            print("  No hay productos para demostrar")
            return
        
        # Tomar el primer producto como ejemplo
        ejemplo = self.productos[0]
        print(f"\n  Producto de ejemplo: {ejemplo}")
        print(f"  Tipo: {type(ejemplo)}")
        print("\n  Intentos de modificación:")
        print("  ❌ ejemplo[2] = 100  # Esto daría ERROR")
        print("  ✅ Para modificar, creamos una nueva tupla:")
        
        # Crear nueva tupla
        nueva = (ejemplo[0], ejemplo[1], 100, ejemplo[3])
        print(f"  ✅ Nueva tupla creada: {nueva}")
        print(f"  ✅ Original intacta: {ejemplo}")