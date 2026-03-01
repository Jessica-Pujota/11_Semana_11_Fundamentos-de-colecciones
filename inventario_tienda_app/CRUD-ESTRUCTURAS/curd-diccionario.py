"""CRUD con DICCIONARIOS (DICT)
Implementación de inventario utilizando diccionarios como estructura principal.
"""
import sys
import os

# Ajustar path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Inventario.modelos.producto import Producto
class CrudDiccionario: #Implementación CRUD usando DICCIONARIOS. Los productos se almacenan en un dict con ID como clave.
    def __init__(self, archivo_datos="inventario.txt"): #Inicializa el CRUD con diccionarios.
        self.archivo = archivo_datos
        self.productos = {}  # Diccionario {id: Producto}
        self.nombre = "DICCIONARIOS"
        self.cargar_desde_archivo()
    
    def cargar_desde_archivo(self): #Carga los productos desde el archivo al diccionario
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        producto = Producto.from_file_string(linea)
                        if producto:
                            self.productos[producto.id] = producto
            print(f"📖 [{self.nombre}] {len(self.productos)} productos cargados")
        except FileNotFoundError:
            print(f"📄 [{self.nombre}] Archivo no encontrado, se creará nuevo")
        except Exception as e:
            print(f"✗ Error cargando: {e}")
    
    def guardar_en_archivo(self): #Guarda los productos en el archivo
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                # Ordenar por ID para consistencia
                for id_producto in sorted(self.productos.keys()):
                    f.write(self.productos[id_producto].to_file_string())
            return True
        except Exception as e:
            print(f"✗ Error guardando: {e}")
            return False
    
    # ===== OPERACIONES CRUD =====
    def create(self, id_producto, nombre, cantidad, precio): #Crear un nuevo producto en el diccionario
        print(f"\n🆕 [{self.nombre}] CREATE - Crear producto")
        
        # Verificar ID único
        if id_producto in self.productos:
            print(f"  ✗ Error: Ya existe producto con ID {id_producto}")
            return False
        # Validar datos
        if cantidad < 0 or precio < 0:
            print(f"  ✗ Error: Cantidad y precio no pueden ser negativos")
            return False
        
        # Crear producto y añadir al diccionario
        nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
        self.productos[id_producto] = nuevo_producto
        
        # Guardar en archivo
        if self.guardar_en_archivo():
            print(f"  ✓ Producto '{nombre}' creado correctamente con clave {id_producto}")
            print(f"  📊 Total en diccionario: {len(self.productos)} productos")
            return True
        else:
            del self.productos[id_producto]
            print(f"  ✗ Error al guardar en archivo")
            return False
    
    def read(self, id_buscar=None): #Leer productos del diccionario, opcionalmente por ID
        if id_buscar:
            print(f"\n🔍 [{self.nombre}] READ - Buscar ID {id_buscar}")
            producto = self.productos.get(id_buscar)
            if producto:
                print(f"  ✓ Encontrado: {producto}")
                return [producto]
            else:
                print(f"  ✗ No se encontró producto con ID {id_buscar}")
                return []
        else:
            print(f"\n📋 [{self.nombre}] READ - Listar todos")
            # Ordenar por ID para mostrarlos ordenados
            return [self.productos[id] for id in sorted(self.productos.keys())]
    
    def update(self, id_producto, cantidad=None, precio=None): #Actualizar un producto existente en el diccionario
        print(f"\n📝 [{self.nombre}] UPDATE - Producto ID {id_producto}")
        
        if id_producto not in self.productos:
            print(f"  ✗ No existe producto con ID {id_producto}")
            return False
        
        producto = self.productos[id_producto]
        
        # Guardar valores originales por si hay error
        cant_original = producto.cantidad
        prec_original = producto.precio
        
        # Mostrar valores actuales
        print(f"  📌 Valores actuales: Cant={cant_original}, Precio=${prec_original:.2f}")
        
        try:
            # Actualizar valores
            cambios = False
            if cantidad is not None:
                if cantidad < 0:
                    raise ValueError("La cantidad no puede ser negativa")
                producto.cantidad = cantidad
                cambios = True
            
            if precio is not None:
                if precio < 0:
                    raise ValueError("El precio no puede ser negativo")
                producto.precio = precio
                cambios = True
            
            if not cambios:
                print(f"  ⚠ No se especificaron cambios")
                return True
            
            print(f"  📌 Nuevos valores: Cant={producto.cantidad}, Precio=${producto.precio:.2f}")
            
            # Guardar en archivo
            if self.guardar_en_archivo():
                print(f"  ✓ Producto ID {id_producto} actualizado correctamente")
                return True
            else:
                # Revertir cambios
                producto.cantidad = cant_original
                producto.precio = prec_original
                print(f"  ✗ Error al guardar - cambios revertidos")
                return False
                
        except ValueError as e:
            print(f"  ✗ Error: {e}")
            return False
    
    def delete(self, id_producto): #Eliminar un producto del diccionario por ID
        print(f"\n🗑️ [{self.nombre}] DELETE - Producto ID {id_producto}")
        
        if id_producto not in self.productos:
            print(f"  ✗ No existe producto con ID {id_producto}")
            return False
        
        producto_eliminado = self.productos.pop(id_producto)
        print(f"  📌 Eliminando: {producto_eliminado.nombre}")
        
        if self.guardar_en_archivo():
            print(f"  ✓ Producto ID {id_producto} eliminado correctamente")
            return True
        else:
            self.productos[id_producto] = producto_eliminado
            print(f"  ✗ Error al guardar - producto restaurado")
            return False
    
    # ===== OPERACIONES ESPECÍFICAS DE DICCIONARIOS =====
    
    def filtrar_por_condicion(self, **condiciones): #Filtra productos por condiciones específicas (precio, cantidad, nombre)
        print(f"\n🔍 [{self.nombre}] Filtrando productos...")
        
        resultado = self.productos.copy()
        
        if 'precio_min' in condiciones:
            resultado = {k: v for k, v in resultado.items() 
                        if v.precio >= condiciones['precio_min']}
        if 'precio_max' in condiciones:
            resultado = {k: v for k, v in resultado.items() 
                        if v.precio <= condiciones['precio_max']}
        if 'cantidad_min' in condiciones:
            resultado = {k: v for k, v in resultado.items() 
                        if v.cantidad >= condiciones['cantidad_min']}
        if 'nombre_contiene' in condiciones:
            texto = condiciones['nombre_contiene'].lower()
            resultado = {k: v for k, v in resultado.items() 
                        if texto in v.nombre.lower()}
        print(f"  ✓ {len(resultado)} productos encontrados")
        return resultado
    
    def agrupar_por_rango_precio(self): #Agrupa productos por rangos de precio (económico, medio, caro)
        grupos = {
            'económico (< $50)': [],
            'medio ($50-$200)': [],
            'caro (> $200)': []
        }
        
        for producto in self.productos.values():
            if producto.precio < 50:
                grupos['económico (< $50)'].append(producto)
            elif producto.precio <= 200:
                grupos['medio ($50-$200)'].append(producto)
            else:
                grupos['caro (> $200)'].append(producto)
        
        return grupos
    def estadisticas_por_categoria(self):  #Calcula estadísticas por categoría de precio.
        grupos = self.agrupar_por_rango_precio()
        estadisticas = {}
        
        for categoria, productos in grupos.items():
            if productos:
                cantidades = [p.cantidad for p in productos]
                precios = [p.precio for p in productos]
                estadisticas[categoria] = {
                    'cantidad_productos': len(productos),
                    'total_unidades': sum(cantidades),
                    'precio_promedio': sum(precios) / len(precios),
                    'precio_maximo': max(precios),
                    'precio_minimo': min(precios),
                    'productos': [p.nombre for p in productos]
                }
            else:
                estadisticas[categoria] = {'cantidad_productos': 0}
        
        return estadisticas
    
    def buscar_por_nombre(self, texto): # Buscar productos por nombre (coincidencia parcial)
        texto = texto.lower()
        resultados = [p for p in self.productos.values() 
                     if texto in p.nombre.lower()]
        
        print(f"\n🔍 [{self.nombre}] Búsqueda por nombre '{texto}': {len(resultados)} resultados")
        return resultados
    
    def __str__(self):
        return f"CrudDiccionario({len(self.productos)} productos)"

# Función de prueba
def test_crud_diccionario(): #Prueba básica del CRUD con diccionarios
    print("\n" + "="*60)
    print("🧪 PRUEBA CRUD CON DICCIONARIOS")
    print("="*60)
    
    # Crear instancia
    crud = CrudDiccionario("test_diccionario.txt")
    # CREATE
    print("\n📝 Creando productos...")
    crud.create(1, "Laptop Gamer", 10, 1200.00)
    crud.create(2, "Mouse RGB", 50, 35.50)
    crud.create(3, "Teclado Mecánico", 30, 89.99)
    crud.create(4, "Monitor 4K", 15, 450.00)
    crud.create(5, "Audífonos", 25, 45.00)
    
    # READ
    print("\n📋 Listando productos...")
    for p in crud.read():
        print(f"  {p}")
    
    # UPDATE
    print("\n📝 Actualizando producto...")
    crud.update(2, cantidad=45, precio=29.99)
    
    # Operaciones de diccionario
    print("\n📊 Probando operaciones de diccionario...")
    
    # Filtrar
    filtrados = crud.filtrar_por_condicion(precio_max=100, cantidad_min=20)
    print(f"\n  Productos con precio < $100 y cantidad >= 20:")
    for p in filtrados.values():
        print(f"    {p}")
    
    # Agrupar
    print("\n  Agrupación por rango de precio:")
    grupos = crud.agrupar_por_rango_precio()
    for rango, prods in grupos.items():
        print(f"    {rango}: {len(prods)} productos")
    
    # Estadísticas
    print("\n  Estadísticas por categoría:")
    stats = crud.estadisticas_por_categoria()
    for cat, datos in stats.items():
        if datos['cantidad_productos'] > 0:
            print(f"    {cat}: {datos['cantidad_productos']} prod, "
                  f"precio prom ${datos['precio_promedio']:.2f}")
    
    # DELETE
    print("\n🗑️ Eliminando producto...")
    crud.delete(5)
    
    # READ final
    print("\n📋 Productos finales:")
    for p in crud.read():
        print(f"  {p}")
    
    print("\n" + "="*60)
    print("✅ PRUEBA COMPLETADA")
    print("=" *60)
    
if __name__ == "__main__":
    test_crud_diccionario()