# Documentación del uso de Colecciones
### Colecciones utilizadas:
1. Diccionario (_productos):
- Propósito: Almacenar productos con ID como clave
- Ventaja: Búsqueda O(1) por ID, ideal para acceso rápido
2. Uso: self._productos = {}
- Conjunto (_ids_disponibles):
- Propósito: Mantener IDs de productos eliminados para reutilización
- Ventaja: Búsqueda O(1) y sin duplicados
3. Uso: self._ids_disponibles = set()

- Listas:
- Propósito: Resultados de búsquedas y ordenamiento
- Uso: resultados = [] en búsqueda por nombre
- Tuplas:
- Propósito: Datos inmutables para estadísticas
4. Uso implícito: En funciones como max() y comprensiones
- Almacenamiento en Archivos:
Formato: JSON para serialización/deserialización
- Ubicación: datos/inventario.json
5. Proceso:
- to_dict(): Convierte Producto a diccionario
- from_dict(): Recrea Producto desde diccionario
- guardar_en_archivo(): Serializa y guarda
- cargar_desde_archivo(): Lee y deserializa

# Sistema de Gestión de Inventarios para Tienda
## 📋 Descripción
Sistema avanzado de gestión de inventarios desarrollado en Python que aplica conceptos de Programación Orientada a Objetos (POO), colecciones y persistencia de datos en archivos. Ideal para pequeñas y medianas tiendas que necesitan un control eficiente de su inventario.

## Características Principales
- **Gestión completa de productos**: Añadir, eliminar, actualizar y buscar productos
- **Búsqueda inteligente**: Búsqueda por nombre con coincidencias parciales
- **Persistencia de datos**: Guardado automático en archivo JSON
- **Interfaz intuitiva**: Menú interactivo por consola
- **Manejo de errores**: Validación de datos y gestión de excepciones
- **Estadísticas en tiempo real**: Cálculo automático de valor total del inventario
## Estructura del Proyecto