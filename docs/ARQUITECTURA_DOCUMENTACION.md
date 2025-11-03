# 4. Arquitectura y Diseño del Sistema

## 4.1. Estructura de Carpetas y Archivos

El código fuente se organiza de manera modular, siguiendo un diseño multicapa donde cada carpeta representa una capa funcional del flujo ETL. La estructura principal del proyecto `etl_randomuser/` se divide en las siguientes secciones:

**Capa de código fuente (`src/`)**: Contiene `main.py` como punto de entrada único, junto con `config.py` para la configuración centralizada. Las subcarpetas organizan los componentes por responsabilidad: `controller/` para la orquestación del flujo, `services/` para la lógica de negocio (extracción, transformación y visualización), `models/` para la definición de estructuras de datos, `loaders/` para la persistencia de información, y `utils/` para utilidades transversales como el sistema de logging.

**Carpetas generadas durante la ejecución**: `data/` almacena los archivos CSV y la base de datos SQLite resultantes del proceso, `plots/` contiene los 8 gráficos estadísticos generados en formato PNG, y `logs/` mantiene el registro de ejecución con timestamps.

**Carpetas de soporte**: `dashboard/` incluye el informe HTML interactivo final, `scripts_project/` agrupa los scripts de ejecución automatizada y tests, y `docs/` centraliza toda la documentación del proyecto.

Esta organización jerárquica facilita la navegación del código, la localización de componentes específicos y el mantenimiento del sistema, reflejando principios de ingeniería de software modernos.

---

## 4.2. Componentes Principales

### a) main.py - Punto de Entrada del Sistema

El archivo `main.py` actúa como interfaz de orquestación y punto único de acceso al sistema. Su función principal es ejecutar el pipeline completo mediante una única llamada, garantizando la reproducibilidad y el registro del proceso.

Entre sus responsabilidades técnicas se encuentran la carga dinámica de parámetros desde `config.py`, donde se definen valores como el número de usuarios a extraer (1000 por defecto) y la semilla de reproducibilidad. También inicializa el sistema de logging global mediante `utils/logger.py`, que genera mensajes con formato estandarizado incluyendo timestamp y nivel de severidad.

La ejecución del flujo ETL se delega en el controlador, quien coordina las fases de extracción, transformación, carga y visualización de forma secuencial. De este modo, el archivo principal actúa como punto de entrada limpio y desacoplado de la lógica interna del sistema.

---

### b) Configuración Centralizada (config.py)

El módulo `config.py` centraliza todos los parámetros generales del sistema, permitiendo adaptar el comportamiento sin modificar el código fuente. Esta capa de configuración promueve la flexibilidad y reutilización del proyecto.

**Parámetros de extracción**: Se define `DEFAULT_N_USERS` con valor 1000, indicando el número de usuarios a extraer de la API RandomUser por defecto. `MAX_USERS_PER_REQUEST` establece el límite máximo en 5000 usuarios que permite la API en una sola petición. `API_TIMEOUT` configura un timeout de 30 segundos para todas las peticiones HTTP, garantizando que el sistema no se quede bloqueado indefinidamente.

**URLs de APIs**: `RANDOMUSER_API_URL` almacena la dirección base `"https://randomuser.me/api/"`, mientras que `RESTCOUNTRIES_API_URL` contiene el endpoint `"https://restcountries.com/v3.1/name/{country}"` utilizado para enriquecer los datos de usuarios con información geográfica adicional.

**Archivos y directorios**: Se establecen nombres de archivos como `"usuarios.csv"` y `"usuarios.db"` para las exportaciones, junto con rutas de directorios `"data"`, `"plots"` y `"dashboard"` donde se almacenan los resultados.

**Funciones helper**: El módulo incluye funciones como `build_randomuser_url()` que construye dinámicamente las URLs de petición incorporando parámetros como el número de usuarios y la semilla de reproducibilidad. Por ejemplo, para 1000 usuarios con semilla `"proyecto2025"`, la función genera: `"https://randomuser.me/api/?results=1000&seed=proyecto2025"`.

Esta centralización facilita la gestión de credenciales, el cambio de endpoints en diferentes entornos (desarrollo, producción) y la configuración de límites y timeouts según las necesidades específicas del despliegue.

---

### c) Controller - Capa de Orquestación

El controlador (`controller/etl_controller.py`) coordina la ejecución completa del pipeline ETL, implementando el flujo secuencial de las tres fases principales: extracción, transformación y carga, gestionando además la generación del dashboard final.

Sus responsabilidades incluyen invocar los servicios en el orden correcto, iniciando con la extracción de usuarios mediante `ETLService.extract_users()`, seguida de la validación y limpieza con `clean_users()`. Posteriormente, invoca `TransformerService` para realizar enriquecimientos, detección de outliers y cálculo de estadísticas avanzadas.

El controlador también gestiona los directorios de salida, creando automáticamente las carpetas `data/` y `plots/` si no existen, y coordina la carga de datos mediante instancias de `CSVLoader` y `SQLLoader` que persisten los resultados en formatos CSV y SQLite respectivamente.

La generación de visualizaciones se delega a `VisualizationService`, que produce 8 gráficos estadísticos: distribución de edades, género, top países, edad por país, matriz de correlación, distribución por regiones, grupos de edad, y género por país.

El controlador actúa como capa de gestión aplicando el principio de abstracción, ya que conoce las interfaces de los servicios pero no sus detalles internos de implementación. Esto facilita el mantenimiento, permite sustituir implementaciones sin afectar el flujo general, y asegura la coherencia entre las diferentes fases del proceso ETL.

---

### d) Services - Lógica de Negocio

La carpeta `services/` implementa la lógica funcional principal del sistema. Cada servicio encapsula un conjunto de operaciones específicas y expone métodos claros para interactuar con el resto del pipeline.

**ETLService**: Gestiona la conexión con la API RandomUser mediante peticiones HTTP, descarga los datos en formato JSON y los convierte en objetos `User` estructurados. Por ejemplo, un usuario JSON típico contiene campos como `gender: "male"`, `name.first: "John"`, `location.country: "Spain"`, `dob.age: 35`, y `email: "john.doe@example.com"`. Tras la conversión, realiza validaciones eliminando registros con email vacío, edad inválida o país no especificado.

**TransformerService**: Realiza transformaciones avanzadas sobre los datos. La función `enrich_data()` clasifica usuarios en grupos de edad: menores de 18 como "Adolescente", entre 18-30 como "Joven Adulto", 31-45 como "Adulto Joven", 46-60 como "Adulto Maduro", 61-80 como "Senior", y mayores de 80 como "Longevo". Además, extrae dominios de email (por ejemplo, `"gmail.com"` de `"user@gmail.com"`) y clasifica dominios populares para análisis de preferencias.

La detección de outliers utiliza el método IQR (Interquartile Range), calculando manualmente los cuartiles Q1 y Q3 de las edades. Si un usuario tiene edad fuera del rango `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`, se marca con `is_outlier: True`. Por ejemplo, en un dataset con edades 25-80, un usuario de 18 años sería marcado como outlier.

El enriquecimiento con RestCountries API agrega información geográfica: `region: "Europe"` para España, o `population: 47519628` para usuarios españoles. Esto permite análisis continentales o por tamaño poblacional.

Las estadísticas calculadas manualmente incluyen media de edad (por ejemplo, 51.97 años), mediana (53 años), desviación estándar (16.48), coeficiente de variación (30.9%), y distribuciones como género (male: 509, female: 491) o países más representados (Norway: 62 usuarios, Spain: 57 usuarios).

**VisualizationService**: Genera gráficos y reportes visuales en formato PNG con resoluciones de 300 DPI. Crea histogramas de edades con 15 bins, gráficos de barras horizontales para top países, boxplots agrupados por país mostrando la distribución de edades, diagramas de sectores para grupos de edad, y matrices de correlación con anotaciones de valores. Todos los gráficos se guardan en `plots/` con nombres descriptivos como `distribucion_edades.png` o `matriz_correlacion.png`.

Este diseño aplica los principios de encapsulación y reutilización, donde cada servicio gestiona su propia lógica y estado interno, facilitando el mantenimiento y la ampliación del sistema. Por ejemplo, agregar una nueva transformación solo requiere modificar `TransformerService`, sin afectar otros componentes.

---

### e) Loaders - Patrón de Herencia y Polimorfismo

La carpeta `loaders/` contiene los módulos responsables de la fase de carga, siguiendo un modelo basado en herencia y polimorfismo donde todas las clases derivan de una clase abstracta común `BaseLoader`.

**BaseLoader**: Define la interfaz genérica mediante el método abstracto `load(data, output_dir)`, estableciendo el contrato que deben cumplir todas las implementaciones. Utiliza el módulo `abc` de Python para garantizar que no se pueda instanciar directamente y que las clases hijas deben implementar el método.

**CSVLoader**: Implementa la persistencia en formato CSV usando `csv.DictWriter`, generando archivos con encoding UTF-8 para soportar caracteres internacionales. Por ejemplo, escribe filas como: `gender,first_name,country,age,email` en la primera línea, seguida de `male,John,Spain,35,john@example.com` en cada fila de datos. Añade automáticamente encabezados basados en las claves del primer registro.

**SQLLoader**: Almacena registros en una base de datos SQLite mediante sentencias preparadas para evitar inyección SQL. Crea la tabla `users` con columnas `first_name TEXT, last_name TEXT, gender TEXT, country TEXT, age INTEGER, email TEXT` si no existe. Realiza inserciones individuales para cada usuario, asegurando integridad transaccional mediante `commit()` al finalizar.

Este diseño permite añadir nuevos tipos de carga sin modificar la arquitectura existente. Por ejemplo, se podría crear `JSONLoader` o `XMLLoader` heredando de `BaseLoader` e implementando solo el método `load()`. Esto aplica el principio de abstracción y extensibilidad, permitiendo que el controlador trabaje con cualquier loader mediante polimorfismo.

La flexibilidad se demuestra cuando el controlador invoca `loader.load(data_dicts, output_dir)` sin conocer si `loader` es una instancia de `CSVLoader` o `SQLLoader`. Esta abstracción simplifica el código y facilita la expansión futura del sistema.

---

### f) Models - Definición de Estructuras de Datos

La carpeta `models/` define la estructura de los datos manejados por el sistema. El módulo `user_model.py` implementa la clase `User` mediante el decorador `@dataclass` de Python.

**Atributos principales**: La clase define atributos tipados como `gender: str` (valores "male" o "female"), `first_name: str` (por ejemplo "John"), `last_name: str` (por ejemplo "Doe"), `country: str` (por ejemplo "Spain"), `age: int` (por ejemplo 35), y `email: str` (por ejemplo "john.doe@example.com").

**Atributos derivados**: Durante la transformación se agregan campos calculados como `age_group: str` con valores "18-30", "31-45", etc., `age_category: str` con categorías "Joven Adulto", "Adulto Maduro", etc., `email_domain: str` extrayendo "gmail.com" del email completo, `email_preference: str` marcando "Popular" o "Otro" según el dominio, `is_outlier: bool` indicando si la edad es atípica, `region: str` con valores continentales como "Europe", y `population: int` con la población del país.

El método `from_api()` transforma directamente los datos JSON recibidos desde la API RandomUser en instancias de esta clase. Por ejemplo, un JSON con `{"gender":"male","name":{"first":"John","last":"Doe"},"location":{"country":"Spain"},"dob":{"age":35},"email":"john@example.com"}` se convierte en un objeto `User` con atributos accesibles mediante notación punto: `user.first_name`, `user.age`, etc.

El decorador `@dataclass` genera automáticamente métodos como `__init__()`, `__repr__()`, y `__eq__()`, eliminando código repetitivo. La representación de un objeto incluye todos los campos: `User(gender='male', first_name='John', last_name='Doe', country='Spain', age=35, email='john@example.com', ...)`.

Esta abstracción garantiza consistencia tipada, facilita la manipulación durante transformaciones, y proporciona una interfaz clara para acceder a los datos de usuarios a lo largo de todo el pipeline ETL.

---

### g) Utils - Utilidades Transversales

El módulo `utils/` reúne las funciones de apoyo al sistema. Entre ellas destaca `logger.py`, que configura un sistema de registro unificado para todo el proyecto utilizando el módulo estándar `logging` de Python.

**Configuración de logging**: Establece el nivel de severidad en `INFO`, registrando mensajes informativos, advertencias y errores. Configura un formateador que incluye timestamp con formato `'2025-11-03 20:47:10'`, nivel del mensaje (`INFO`, `WARNING`, `ERROR`), y el texto descriptivo.

**Handlers**: Crea un handler de archivo que escribe en `src/logs/etl.log` con encoding UTF-8, garantizando que no haya problemas con caracteres especiales. Los mensajes se acumulan en el archivo durante toda la ejecución, proporcionando un historial completo del proceso.

Ejemplos de mensajes registrados incluyen: `"2025-11-03 20:47:10 - INFO - Iniciando extracción de 1000 usuarios..."`, `"2025-11-03 20:47:11 - INFO - Extracción completada: 1000 usuarios."`, o `"2025-11-03 20:47:11 - INFO - Detectados 25 outliers de edad (método IQR)."`.

Este sistema de logging facilita el seguimiento y la depuración, permitiendo identificar en qué fase ocurre un error, analizar los tiempos de ejecución de cada etapa, y mantener un registro histórico de las ejecuciones del sistema. La configuración centralizada permite cambiar el nivel de verbosidad (por ejemplo, a `DEBUG` durante desarrollo) sin modificar el código de negocio.

---

## 4.3. Pipeline ETL y Flujo de Ejecución

El sistema sigue un flujo de ejecución automatizado y secuencial que refleja la naturaleza de un pipeline de datos.

**Fase 1 - Inicialización**: El archivo `main.py` carga la configuración desde `config.py`, donde se establece el número de usuarios (1000), la semilla de reproducibilidad (opcional), y los timeouts de peticiones HTTP. Inicializa el sistema de logging global y lanza el controlador.

**Fase 2 - Extracción**: Se solicitan datos a la API RandomUser mediante una petición HTTP GET a `"https://randomuser.me/api/?results=1000"`. La respuesta JSON contiene un array de 1000 objetos usuario, cada uno con campos como nombre, género, país, edad y email. La conversión a objetos `User` se realiza mediante el método `from_api()`, generando una lista de 1000 instancias tipadas.

**Fase 3 - Limpieza**: Se aplican validaciones eliminando registros con campos vacíos o inválidos. Por ejemplo, si 15 usuarios tienen email vacío o edad menor a 18, se descartan, resultando en 985 usuarios válidos. Los registros filtrados se registran en el log para trazabilidad.

**Fase 4 - Transformación**: Se ejecutan transformaciones básicas calculando estadísticas descriptivas: media de edad 51.97 años, mediana 53, desviación estándar 16.48. Las transformaciones avanzadas enriquecen los datos agregando grupos de edad, categorías, dominios de email, y marcas de outliers. Se enriquece con información geográfica de RestCountries, agregando regiones como "Europe" para usuarios de España, Francia o Alemania.

**Fase 5 - Carga**: Los 985 usuarios transformados se exportan en dos formatos. `CSVLoader` genera `usuarios.csv` con 986 líneas (1 header + 985 datos), donde cada línea contiene valores separados por comas: `"male,John,Doe,Spain,35,john@example.com,31-45,..."`. `SQLLoader` crea `usuarios.db` e inserta 985 filas en la tabla `users`, utilizando sentencias preparadas para garantizar integridad.

**Fase 6 - Visualización**: Se generan 8 gráficos PNG en la carpeta `plots/`. Por ejemplo, `distribucion_edades.png` muestra un histograma con 15 barras representando rangos de edad, `top_paises.png` presenta barras horizontales ordenadas por cantidad de usuarios (Norway: 62, Spain: 57, United Kingdom: 55), y `distribucion_genero.png` muestra proporciones aproximadas 50/50 entre géneros.

**Fase 7 - Dashboard**: Se genera `stats.json` con estadísticas agregadas: total 985 usuarios, edad promedio 51.97, y top países con sus conteos. El dashboard HTML lee este archivo y embebe las imágenes PNG, presentando un informe interactivo accesible vía navegador web.

El uso de un pipeline controlado garantiza la reproducibilidad del proceso. Por ejemplo, utilizando el mismo seed `"proyecto2025"` en ejecuciones diferentes, se obtienen exactamente los mismos 1000 usuarios, facilitando el testing, la depuración y la presentación de resultados consistentes. Esta estructura facilita también la integración de nuevas fuentes de datos o etapas adicionales sin modificar el flujo principal.

---

## 4.4. Dashboard HTML

Como etapa final, el sistema genera un dashboard HTML que sintetiza los resultados del proceso ETL. Este archivo combina texto, tablas y gráficos de análisis, presentando de forma accesible la información procesada.

El dashboard incluye secciones como estadísticas generales mostrando total de usuarios (985), edad promedio (51.97 años), y distribución por género (male: 491, female: 494). Presenta enlaces directos descargables a `usuarios.csv`, `usuarios.db`, y a cada uno de los 8 gráficos PNG almacenados en `plots/`.

Las visualizaciones se embeben directamente en la página mediante etiquetas `<img src="../plots/distribucion_edades.png">`, permitiendo visualización inmediata sin necesidad de abrir archivos externos. El diseño responsive se adapta a diferentes tamaños de pantalla mediante CSS Grid, facilitando la visualización en escritorio, tablet o móvil.

El dashboard actúa como interfaz de visualización y documentación automática del proceso ejecutado, proporcionando una representación consolidada que permite a usuarios no técnicos entender los resultados del análisis sin necesidad de acceder directamente a archivos CSV o bases de datos.

---

## 4.5. Consideraciones de Diseño

El sistema se ha diseñado aplicando principios de la Programación Orientada a Objetos (OOP) y las buenas prácticas de ingeniería del software.

**Modularidad**: La separación clara por capas funcionales facilita la navegación, localización de componentes y mantenimiento. Por ejemplo, modificar la lógica de extracción solo afecta a `ETLService`, sin impactar transformaciones o visualizaciones.

**Encapsulación**: Cada módulo gestiona su propia lógica y estado interno. Por ejemplo, `TransformerService` mantiene la lista de usuarios en `self.users` y solo expone métodos públicos como `enrich_data()` o `compute_statistics()`, ocultando implementaciones internas de cálculo de percentiles o contadores.

**Abstracción**: El controlador y los servicios interactúan mediante interfaces bien definidas. Por ejemplo, el controlador invoca `loader.load(data, output_dir)` sin conocer si internamente escribe CSV o SQL, aplicando el principio de inversión de dependencias.

**Herencia y polimorfismo**: Permiten extender funcionalidades, como en el caso de los loaders. La clase abstracta `BaseLoader` define el contrato mediante `load()`, mientras que `CSVLoader` y `SQLLoader` implementan los detalles específicos. Esto permite agregar `JSONLoader` o `XMLLoader` sin modificar el código existente.

**Reutilización y mantenibilidad**: Los módulos pueden integrarse en otros proyectos con mínimas modificaciones. Por ejemplo, `config.py` es independiente de la lógica de negocio, `BaseLoader` elimina duplicación de código, y los servicios son intercambiables.

En conjunto, la arquitectura proporciona una base sólida, escalable y fácilmente integrable, adecuada tanto para proyectos educativos como para entornos reales de análisis y automatización de datos.

---

## Conclusión

La arquitectura implementada combina separación de responsabilidades, configuración centralizada y principios OOP modernos, resultando en un código mantenible, extensible y testeable. El diseño multicapa facilita la comprensión del flujo de datos desde la extracción hasta la visualización, mientras que la modularidad permite adaptaciones y mejoras sin comprometer la estabilidad del sistema.

