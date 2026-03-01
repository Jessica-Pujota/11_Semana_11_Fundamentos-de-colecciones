""" Servicio principal que coordina todas las implementaciones CRUD"""
import os
import sys
from typing import List, Dict, Any, Union

# Ajustar path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Inventario.cli.modelos.producto import Producto
from Estructuras.listas import ListaInventario
from Estructuras.diccionarios import DiccionarioInventario
from Estructuras.conjunto import ConjuntoInventario
from Estructuras.tuplas import TuplaInventario

class InventarioServicio:
    """
    Servicio que unifica todas las implementaciones de inventario.
    Permite trabajar con diferentes estructuras de datos.
    """
    def __init__(self, archivo_base: str = "inventario.txt"): #Inicializa el servicio con todas las implementaciones.
        
        self.archivo = archivo_base
        self.implementaciones = {}
        self.activa = "listas"  # Implementación por defecto
        
        # Inicializar todas las implementaciones
        self._inicializar_implementaciones()
    
    def _inicializar_implementaciones(self): #Inicializa todas las implementaciones de inventario
        try:
            from servicios.Registros.gestor_archivos import GestorArchivos
            gestor = GestorArchivos(self.archivo)
        except ImportError:
            # Gestor simple si no existe
            gestor = None
        
        self.implementaciones = {
            "listas": ListaInventario(gestor),
            "diccionarios": DiccionarioInventario(gestor),
            "conjuntos": ConjuntoInventario(gestor),
            "tuplas": TuplaInventario(gestor)
        }
    
    def cambiar_implementacion(self, nombre: str) -> bool:
        """
        Cambia la implementación activa.
        
        Args:
            nombre: "listas", "diccionarios", "conjuntos", "tuplas"
        """
        if nombre in self.implementaciones:
            self.activa = nombre
            print(f"\n🔄 Implementación cambiada a: {self.implementaciones[nombre].nombre_implementacion}")
            return True
        else:
            print(f"✗ Implementación '{nombre}' no válida")
            return False
    
    def get_activa(self): #Obtiene la implementación activa
        return self.implementaciones[self.activa]
    
    # ===== MÉTODOS CRUD DELEGADOS =====
    
    def create(self, producto: Producto) -> bool: #Añade producto usando implementación activa
        return self.get_activa().create(producto)
    
    def read(self, id_buscar: int = None) -> list: #Lee producto(s) usando implementación activa
        return self.get_activa().read(id_buscar)
    
    def update(self, id_producto: int, cantidad: int = None, precio: float = None) -> bool: #Actualiza producto usando implementación activa
        return self.get_activa().update(id_producto, cantidad, precio)
    
    def delete(self, id_producto: int) -> bool: #Elimina producto usando implementación activa
        return self.get_activa().delete(id_producto)
    
    # ===== OPERACIONES ESPECÍFICAS =====
    def ejecutar_operacion_especifica(self): #Ejecuta operación específica de la implementación activa
        activa = self.get_activa()
        
        if self.activa == "conjuntos":
            activa.demostrar_operaciones_conjuntos()
        elif self.activa == "listas":
            self._menu_listas(activa)
        elif self.activa == "diccionarios":
            self._menu_diccionarios(activa)
        elif self.activa == "tuplas":
            activa.demostrar_inmutabilidad()
    
    def _menu_listas(self, lista_impl): #Menú para operaciones específicas de listas
        print("\n📋 OPERACIONES DE LISTAS:")
        print("1. Ordenar por precio")
        print("2. Ordenar por cantidad")
        print("3. Ver primeros 3 productos")
        print("4. Ver últimos 3 productos")
        
        opcion = input("Seleccione opción: ")
        if opcion == "1":
            lista_impl.ordenar_por_precio()
        elif opcion == "2":
            lista_impl.ordenar_por_cantidad()
        elif opcion == "3":
            primeros = lista_impl.obtener_primeros_n(3)
            for p in primeros:
                print(f"  {p}")
        elif opcion == "4":
            ultimos = lista_impl.obtener_ultimos_n(3)
            for p in ultimos:
                print(f"  {p}")
    def _menu_diccionarios(self, dict_impl): #Menú para operaciones específicas de diccionarios
        print("\n📖 OPERACIONES DE DICCIONARIOS:")
        print("1. Ver estadísticas por categoría")
        print("2. Filtrar productos (precio < 100)")
        print("3. Agrupar por rango de precio")
        
        opcion = input("Seleccione opción: ")
        if opcion == "1":
            stats = dict_impl.estadisticas_por_categoria()
            for cat, datos in stats.items():
                print(f"\n  {cat.upper()}: {datos}")
        elif opcion == "2":
            filtrados = dict_impl.filtrar_por_condicion(precio_max=100)
            print(f"\n  Productos con precio < $100: {len(filtrados)}")
            for p in filtrados.values():
                print(f"    {p}")
        elif opcion == "3":
            grupos = dict_impl.agrupar_por_rango_precio()
            for rango, productos in grupos.items():
                print(f"\n  {rango}: {len(productos)} productos")
    
    def comparar_rendimiento(self): #Compara el rendimiento de todas las implementaciones
        print("\n⚡ COMPARACIÓN DE RENDIMIENTO")
        print("="*60)
        import time
        for nombre, impl in self.implementaciones.items():
            inicio = time.time()
            
            # Operación de lectura
            datos = impl.read()
            
            # Operación de búsqueda (si existe)
            if hasattr(impl, '_buscar_por_id') and datos:
                if nombre == "listas":
                    # En listas, buscar el último elemento
                    ultimo_id = datos[-1].id if datos else 1
                    impl._buscar_indice_por_id(ultimo_id)
                elif datos:
                    ultimo_id = datos[-1][0] if nombre == "tuplas" else datos[-1].id
                    impl._buscar_por_id(ultimo_id)
            
            fin = time.time()
            print(f"  {impl.nombre_implementacion:15s}: {(fin-inicio)*1000:.3f} ms")
        
        print("="*60)
    def __str__(self) -> str: #Representación del servicio
        return f"ServicioInventario(activa={self.activa}, implementaciones={len(self.implementaciones)})"