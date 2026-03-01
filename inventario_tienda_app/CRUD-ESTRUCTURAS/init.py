"""
Paquete CRUD-ESTRUCTURAS 
Contiene implementaciones de inventario usando diferentes estructuras de datos.
"""

from .crud_conjuntos import CrudConjuntos
from .crud_listas import CrudListas
from .crud_upload import CrudUpload
from .curd_diccionario import CrudDiccionario

__all__ = [
    'CrudConjuntos',
    'CrudListas',
    'CrudUpload',
    'CrudDiccionario'
]