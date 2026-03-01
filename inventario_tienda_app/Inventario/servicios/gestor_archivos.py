"""
Gestor de archivos para todas las implementaciones.
"""
import os
from datetime import datetime
from typing import List, Dict, Set, Tuple
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Inventario.modelos.producto import Producto

class GestorArchivos:
    """
    Clase para manejo de archivos con diferentes estructuras.
    """
    
    def __init__(self, archivo_base: str = "inventario.txt"):
        """
        Inicializa el gestor de archivos.
        """
        self.archivo_base = archivo_base
        self.directorio_base = os.path.dirname(archivo_base) or "."
        
        # Crear directorio si no existe
        if self.directorio_base and not os.path.exists(self.directorio_base):
            try:
                os.makedirs(self.directorio_base)
            except:
                pass
    
    # ===== MÉTODOS DE GUARDADO =====
    def guardar_desde_lista(self, productos: List[Producto]) -> bool: #Guarda una lista de objetos Producto
        try:
            with open(self.archivo_base, 'w', encoding='utf-8') as f:
                for producto in productos:
                    f.write(producto.to_file_string())
            return True
        except Exception as e:
            print(f"✗ Error guardando: {e}")
            return False
    
    def guardar_desde_diccionario(self, productos: Dict[int, Producto]) -> bool: #Guarda un diccionario de productos
        return self.guardar_desde_lista(list(productos.values()))
    
    def guardar_desde_conjunto(self, productos: Set[Tuple]) -> bool: #Guarda un conjunto de tuplas
        try:
            with open(self.archivo_base, 'w', encoding='utf-8') as f:
                for elemento in productos:
                    f.write(f"{elemento[0]},{elemento[1]},{elemento[2]},{elemento[3]:.2f}\n")
            return True
        except Exception as e:
            print(f"✗ Error guardando: {e}")
            return False
    
    def guardar_desde_tuplas(self, productos: List[Tuple]) -> bool: #Guarda una lista de tuplas
        try:
            with open(self.archivo_base, 'w', encoding='utf-8') as f:
                for tupla in productos:
                    f.write(f"{tupla[0]},{tupla[1]},{tupla[2]},{tupla[3]:.2f}\n")
            return True
        except Exception as e:
            print(f"✗ Error guardando: {e}")
            return False
    
    # ===== MÉTODOS DE CARGA =====
    
    def cargar_como_lista(self) -> List[Producto]: #Carga productos como lista de objetos Producto
        productos = []
        try:
            with open(self.archivo_base, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        producto = Producto.from_file_string(linea)
                        if producto:
                            productos.append(producto)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"✗ Error cargando: {e}")
        return productos
    
    def cargar_como_diccionario(self) -> Dict[int, Producto]: #Carga productos como diccionario
        productos = {}
        lista = self.cargar_como_lista()
        for producto in lista:
            productos[producto.id] = producto
        return productos
    
    def cargar_como_conjunto(self) -> Set[Tuple]: #Carga productos como conjunto de tuplas
        conjunto = set()
        try:
            with open(self.archivo_base, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        partes = linea.strip().split(',')
                        if len(partes) == 4:
                            elemento = (int(partes[0]), partes[1], int(partes[2]), float(partes[3]))
                            conjunto.add(elemento)
        except:
            pass
        return conjunto
    
    def cargar_como_tuplas(self) -> List[Tuple]: #Carga productos como lista de tuplas
        tuplas = []
        try:
            with open(self.archivo_base, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        partes = linea.strip().split(',')
                        if len(partes) == 4:
                            tupla = (int(partes[0]), partes[1], int(partes[2]), float(partes[3]))
                            tuplas.append(tupla)
        except:
            pass
        return tuplas