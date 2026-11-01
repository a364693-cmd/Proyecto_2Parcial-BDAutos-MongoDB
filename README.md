# BDAutos - Sistema de Gestión y Analytics NoSQL en MongoDB

Este proyecto realiza la transformación, modelado e inicialización de la base de datos relacional `BDAutos` hacia un modelo orientado a documentos en **MongoDB**. Incluye una arquitectura de 3 capas con interfaz gráfica (Tkinter), un motor de consultas analíticas avanzadas y un gestor CRUD por terminal con borrado lógico.

---

## Requisitos Previos

- **Python 3.8+**
- **MongoDB Community Server (v4.4+)**
- Dependencia de Python: `pymongo`

---

## 1. Inicio del Servicio de MongoDB

Antes de ejecutar los scripts en Python, asegúrate de que el motor de MongoDB esté escuchando en el puerto local predeterminado (`localhost:27017`).

- **Linux (Kubuntu / Debian / Ubuntu):**  
  En sistemas con restricciones de sockets o configuraciones locales manuales, ejecuta MongoDB en una ventana de terminal independiente y mantenla activa durante el uso del sistema:
  ```bash
  sudo mongod --config /etc/mongod.conf
  ```

- **Windows:**  
  Inicia el servicio desde el administrador de servicios (`services.msc`) o desde CMD/PowerShell como administrador:
  ```cmd
  net start MongoDB
  ```

- **macOS:**  
  Inicia el servicio mediante Homebrew:
  ```bash
  brew services start mongodb-community
  ```

---

## 2. Configuración del Entorno Virtual (`venv`)

Para evitar conflictos de paquetes del sistema (cumpliendo con PEP 668 en Linux), configura un entorno virtual aislado:

### Linux / macOS
```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Instalar la librería requerida
pip install pymongo
```

### Windows
```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual (PowerShell)
.\venv\Scripts\Activate.ps1
# Si usas CMD: .\venv\Scripts\activate.bat

# 3. Instalar la librería requerida
pip install pymongo
```

---

## 3. Flujo de Ejecución del Sistema

Sigue este orden para poner en marcha la aplicación:

### Paso 1: Inicializar la Base de Datos
Ejecuta el script semillero **una sola vez al inicio** para crear la base de datos `BDAutos` y migrar los datos relacionales hacia las 4 colecciones NoSQL (`continents`, `countries`, `makers`, `cars`):
```bash
python init_db.py
```

### Paso 2: Ejecutar la Aplicación Gráfica (GUI)
Lanza la interfaz gráfica principal en Tkinter. Permite seleccionar y ejecutar las **25 consultas analíticas predefinidas**, así como escribir y ejecutar consultas libres en tiempo real (modo consola estilo MongoDB Compass):
```bash
python gui.py
```

### Paso 3: Gestor de Datos por Terminal (Opcional / Auxiliar)
Si necesitas insertar nuevos vehículos, consultar el inventario completo, aplicar **borrado lógico** (`"activo": false`) o restaurar registros sin pasar por la GUI, ejecuta el gestor interactivo de consola:
```bash
python crud_manager.py
```

---

## 4. Estructura del Proyecto

```text
Proyecto_2_Parcial_364693/
├── init_db.py          # Script semillero: Carga y transformación de datos relacionales a NoSQL.
├── mongo_bridge.py     # Controlador de DB: Puente de comunicación PyMongo y agregaciones.
├── queries_catalog.py  # Catálogo BSON: 25 canalizaciones de agregación + Req 0 (Consola Libre).
├── gui.py              # Aplicación gráfica principal (Tkinter) con visor de código y resultados.
└── crud_manager.py     # Herramienta auxiliar de terminal para gestión CRUD y borrado lógico.
```