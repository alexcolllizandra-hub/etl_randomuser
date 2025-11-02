# Guía de Virtualización para el Proyecto ETL

## Elección del Hypervisor: UTM vs VirtualBox

### **Recomendación: UTM + Debian 12**

**¿Por qué UTM para Apple Silicon (M1/M2/M3)?**
- ✅ Virtualización nativa optimizada
- ✅ Rendimiento superior
- ✅ Soporte oficial para ARM64
- ✅ Interfaz limpia y fácil de usar
- ✅ Sin problemas de compatibilidad

**VirtualBox es una buena opción si:**
- Usas Windows o Linux
- Necesitas la experiencia que ya tienes con VB
- No tienes problemas de rendimiento

## Pasos para Configurar UTM con Debian 12

### 1. Descargar e Instalar UTM

1. Ve a [UTM.app](https://mac.getutm.app/)
2. Descarga la versión para macOS
3. Arrastra UTM a Aplicaciones
4. Abre UTM desde Aplicaciones

### 2. Descargar Debian 12

1. Ve a [debian.org/downloads](https://www.debian.org/download)
2. Descarga **Debian 12 (ARM64)** para Apple Silicon
3. Guarda el archivo ISO (.iso) en una ubicación accesible

### 3. Crear la Máquina Virtual en UTM

1. Abre UTM y haz clic en **"+"** (Nueva VM)
2. Selecciona **"Virtualizar"**
3. Elige **"Linux"**
4. Configuración recomendada:
   - **CPU**: 2-4 cores
   - **RAM**: 2-4 GB (ajusta según tu Mac)
   - **Almacenamiento**: 20-30 GB
   - **Tipo de disco**: QCOW2 (recomendado)

### 4. Instalar Debian 12

1. Inserta la ISO descargada como CD
2. Inicia la VM
3. Sigue el instalador de Debian:
   - Idioma: Español o Inglés
   - Zona horaria: tu zona
   - Usuario y contraseña: anota los datos
   - Tipo de instalación: **Instalación normal** (ya incluye entorno gráfico)
   - Particionamiento: automático

### 5. Preparar el Sistema

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar herramientas esenciales
sudo apt install -y git curl wget vim
```

### 6. Instalar Python 3

```bash
# Verificar si Python ya está instalado
python3 --version

# Si no está, instalar Python 3
sudo apt install -y python3 python3-pip python3-venv

# Verificar instalación
python3 --version
pip3 --version
```

### 7. Clonar el Proyecto ETL

```bash
# Opción 1: Si tienes git configurado en la VM
git clone https://github.com/alexcolllizandra-hub/etl_randomuser.git
cd etl_randomuser

# Opción 2: Copiar desde el host Mac
# Crea una carpeta compartida o transfiere los archivos por SSH/SFTP
```

### 8. Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Verificar que estás en el entorno
which python
```

### 9. Instalar Dependencias

```bash
# Instalar desde requirements.txt
pip install -r requirements.txt

# Verificar instalación
pip list
```

### 10. Instalar Dependencias del Sistema (para gráficos)

```bash
# Debian necesita estas librerías para matplotlib
sudo apt install -y python3-tk
```

### 11. Ejecutar el ETL

**Opción A (recomendada): Usar el script de ejecución**
```bash
# Dar permisos de ejecución
chmod +x run_etl.sh

# Ejecutar el ETL
./run_etl.sh
```

**Opción B: Ejecutar manualmente con PYTHONPATH**
```bash
# Desde la raíz del proyecto
export PYTHONPATH=$(pwd)
python src/main.py

# O en una sola línea:
PYTHONPATH=$(pwd) python src/main.py
```

### 12. Verificar Resultados

```bash
# Ver archivos generados
ls -lh data/

# Ver logs
cat logs/etl.log
```

## Librerías Instaladas y Justificación

### **requests**
- **Función**: Comunicación HTTP con APIs
- **Justificación**: Necesaria para extraer datos de RandomUser API y RestCountries API
- **Uso en el proyecto**: `src/services/etl_service.py`, `src/services/transformer_service.py`

### **matplotlib**
- **Función**: Generación de gráficos
- **Justificación**: Visualizaciones (distribución de edad, género, países)
- **Uso en el proyecto**: `src/services/visualization_service.py`
- **Dependencia del sistema**: Requiere `python3-tk` en Debian/Linux

### **seaborn**
- **Función**: Estadísticas visuales avanzadas
- **Justificación**: Gráficos más atractivos y análisis estadístico visual
- **Uso en el proyecto**: `src/services/visualization_service.py`
- **Dependencia**: Requiere matplotlib instalado

## Estructura del Proyecto en la VM

```
etl_randomuser/
├── src/
│   ├── main.py                      # Punto de entrada
│   ├── controller/
│   │   └── etl_controller.py       # Orquesta el flujo ETL
│   ├── services/
│   │   ├── etl_service.py          # Extracción y limpieza
│   │   ├── transformer_service.py  # Transformaciones avanzadas
│   │   └── visualization_service.py # Gráficos
│   ├── loaders/
│   │   ├── csv_loader.py           # Carga CSV
│   │   └── sql_loader.py           # Carga SQLite
│   ├── models/
│   │   └── user_model.py           # Modelo de datos
│   └── utils/
│       └── logger.py               # Sistema de logs
├── data/                            # Outputs (CSV, DB)
├── logs/                            # Logs del sistema
├── venv/                            # Entorno virtual
├── requirements.txt                 # Dependencias
└── README.md                        # Documentación
```

## Verificación Final

### Check 1: Python está funcionando
```bash
python3 --version
# Debe mostrar: Python 3.11.x o superior
```

### Check 2: Dependencias instaladas
```bash
pip list
# Debe mostrar: requests, matplotlib, seaborn
```

### Check 3: El ETL ejecuta sin errores
```bash
python src/main.py
# Debe descargar usuarios, procesarlos y generar archivos
```

### Check 4: Archivos generados
```bash
ls -lh data/
# Debe mostrar: usuarios.csv y usuarios.db
```

## Troubleshooting Común

### Error: "No module named 'requests'"
```bash
pip install -r requirements.txt
```

### Error: "tkinter not found" (gráficos no se muestran)
```bash
sudo apt install -y python3-tk
```

### Error: "Permission denied" al ejecutar
```bash
chmod +x src/main.py
```

### La VM va lenta
- Asigna más RAM (4GB recomendado)
- Reduce el número de usuarios: `controller.run(n_users=50)`

### Red no funciona
- En UTM: Configuración → Red → Compartida (NAT)

## Capturas de Pantalla Sugeridas para el PDF

1. **VM corriendo en UTM** (pantalla completa)
2. **Debian Desktop** (en la VM)
3. **Terminal con `python3 --version`**
4. **Instalación de dependencias**: `pip install -r requirements.txt`
5. **Ejecución del ETL**: `python src/main.py`
6. **Salida del ETL** (logs en consola)
7. **Archivos generados**: `ls data/`
8. **Gráfico generado** (distribución de edad)
9. **Base de datos**: contenido de usuarios.db
10. **CSV abierto** (primeras líneas de usuarios.csv)

## Criterios de Éxito del Proyecto

✅ VM configurada y funcionando  
✅ Debian 12 instalado correctamente  
✅ Python 3 + pip funcionando  
✅ Proyecto clonado/transferido  
✅ Entorno virtual activo  
✅ Todas las dependencias instaladas  
✅ ETL ejecuta sin errores  
✅ Archivos CSV y DB generados  
✅ Gráficos se muestran correctamente  
✅ Logs generados sin errores  

## Referencias y Recursos

- [Documentación UTM](https://docs.getutm.app/)
- [Documentación Debian](https://www.debian.org/doc/)
- [RandomUser API](https://randomuser.me/documentation)
- [matplotlib Documentation](https://matplotlib.org/)
- [seaborn Documentation](https://seaborn.pydata.org/)

