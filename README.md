# 🩸 Analítica de Donación de Sangre

Dashboard interactivo para análisis y visualización de datos de donación de sangre en hospitales. Sistema integrado con API REST (Spring Boot) para obtener datos en tiempo real.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Documentación Técnica](#documentación-técnica)
- [Despliegue](#despliegue)
- [Solución de Problemas](#solución-de-problemas)

---

## ✨ Características

### Momento 1: DevOps y Colaboración ⚙️
- ✅ Entorno virtual Python (.venv) completamente aislado
- ✅ requirements.txt actualizado con todas las dependencias
- ✅ README profesional con instrucciones completas
- ✅ Archivo .env.example para configuración

### Momento 2: Ingeniería de Datos 🛠️
- ✅ **Carga de Datos**: Consumo de API REST (Spring Boot)
- ✅ **Limpieza ETL**: Manejo de nulos, tipos de datos, duplicados
- ✅ **Pandas Pro**: Uso avanzado de groupby, filtros booleanos, transformaciones
- ✅ **API Ready**: Integración fluida con contrato JSON del Backend

### Momento 3: Visualización e Integración 📊
- ✅ **Dashboard Interactivo**: Streamlit con filtros dinámicos
- ✅ **Gráficos Profesionales**: Plotly y Seaborn de alta calidad
- ✅ **Conexión en Vivo**: Sincronización automática con API
- ✅ **UI/UX Profesional**: Diseño moderno y accesible

---

## 🔧 Requisitos

### Sistema
- Python 3.8+ (se recomienda 3.10+)
- pip (gestor de paquetes de Python)
- Git (para control de versiones)
- API Spring Boot en ejecución

### Software Recomendado
- Visual Studio Code o PyCharm
- Postman (para testing de API)
- Docker (opcional, para contenerizar)

---

## 📦 Instalación

### 1️⃣ Clonar el Repositorio

```bash
# Con HTTPS
git clone https://github.com/tu-usuario/analytics-donantes.git
cd analytics-donantes


```

### 2️⃣ Crear Entorno Virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu línea de comandos.

### 3️⃣ Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Para verificar que todo se instaló correctamente:
```bash
pip list
```

### 4️⃣ Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores
# Por defecto:
# API_BASE_URL=http://localhost:8080
# API_TIMEOUT=10
```

---

## ⚙️ Configuración

### Configurar la URL de la API

El archivo `config.py` contiene la configuración centralizada. Las variables se cargan desde `.env`:

```python
# config.py
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8080')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '10'))
```

**Ejemplos de URLs:**

```env
# Desarrollo local
API_BASE_URL=http://localhost:8080

# Docker local
API_BASE_URL=http://host.docker.internal:8080

# Servidor remoto
API_BASE_URL=https://api.hospital.com
```

### Estructura de Carpetas

```
analytics-donantes/
├── app.py                    # Dashboard principal (Streamlit)
├── config.py                 # Configuración centralizada
├── requirements.txt          # Dependencias
├── .env                      # Variables de entorno (NO COMMITEAR)
├── .env.example              # Plantilla de .env
├── README.md                 # Esta documentación
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # Consume API
│   ├── data_cleaning.py      # ETL con Pandas
│   └── data_processor.py     # Análisis y KPIs
└── data/
    ├── raw/                  # Datos crudos (opcional)
    └── processed/            # Datos procesados (generado)
```

---

## 🚀 Uso

### Ejecutar el Dashboard

```bash
# Asegúrate de que el entorno virtual está activado
# (venv) debe aparecer en tu línea de comandos

streamlit run app.py
```

El dashboard se abrirá automáticamente en: `http://localhost:8501`

### Uso del Dashboard

#### Filtros Disponibles
- **Rango de Fechas**: Selecciona el período de análisis
- **Tipos de Sangre**: Filtra por tipo O+, A-, etc.
- **Estado de Donaciones**: Completadas, pendientes, canceladas

#### Secciones Principales
1. **Métricas Principales**: KPIs en tiempo real
2. **Distribución por Tipo de Sangre**: Gráficos de composición
3. **Tendencias Temporales**: Análisis de donaciones por mes
4. **Estado de Donaciones**: Distribución por estado
5. **Top Donadores**: Ranking de donantes más activos
6. **Análisis de Frecuencia**: Patrón de donaciones por donante

### Testing Manual de la API

Puedes verificar que la API funciona antes de ejecutar el dashboard:

```bash
# Test básico
curl http://localhost:8080/donante

# Test por tipo de sangre
curl http://localhost:8080/donante/sangre/O+

# Test de donantes activos
curl http://localhost:8080/donante/activos
```

---

## 📚 Documentación Técnica

### Módulo: data_loader.py

Consume datos desde la API Spring Boot con manejo robusto de errores.

**Clase Principal: `DataLoader`**

```python
from src.data_loader import DataLoader

loader = DataLoader()

# Cargar todos los donantes
df_donantes = loader.cargar_donantes()

# Cargar solo activos
df_activos = loader.cargar_donantes_activos()

# Cargar por tipo de sangre
df_o_plus = loader.cargar_donantes_por_sangre('O+')

# Cargar todas las donaciones
df_donaciones = loader.cargar_donaciones()

# Cargar donaciones de un donante específico
df_historial = loader.cargar_donaciones_donante(id_donante=5)
```

**Manejo de Errores:**
- Timeout de conexión
- Errores de HTTP
- Fallos de parseo JSON
- Conexiones perdidas

### Módulo: data_cleaning.py

Limpieza ETL con Pandas avanzado.

**Clase Principal: `DataCleaner`**

```python
from src.data_cleaning import DataCleaner, procesar_datos_completos

# Limpiar donantes
df_donantes_limpio = DataCleaner.limpiar_donantes(df_donantes_crudo)

# Limpiar donaciones
df_donaciones_limpio = DataCleaner.limpiar_donaciones(df_donaciones_crudo)

# Pipeline completo ETL
donantes, donaciones = procesar_datos_completos(
    df_donantes_crudo,
    df_donaciones_crudo
)
```

**Transformaciones Aplicadas:**

**Donantes:**
- Conversión de tipos (int, string, datetime, bool)
- Validación de tipos de sangre
- Cálculo de edad
- Limpieza de nombres (trim, title case)
- Eliminación de duplicados
- Manejo de nulos

**Donaciones:**
- Validación de cantidades (100-1000 ml)
- Conversión de fechas
- Validación de estados
- Limpieza de datos
- Enriquecimiento con información del donante

### Módulo: data_processor.py

Análisis de datos y cálculo de KPIs.

**Clase Principal: `DataProcessor`**

```python
from src.data_processor import DataProcessor

processor = DataProcessor()

# Métricas generales
metricas = processor.metricas_generales(donantes, donaciones)
# Retorna: {total_donantes, donantes_activos, total_donaciones, volumen_total_ml, ...}

# Donantes por tipo de sangre
sangre_df = processor.donantes_por_tipo_sangre(donantes)

# Donaciones por mes
mes_df = processor.donaciones_por_mes(donaciones)

# Top donadores
top_df = processor.donantes_top_donadores(donantes, donaciones, top=10)

# Análisis de frecuencia
frecuencia = processor.analisis_frecuencia_donacion(donantes, donaciones)

# Reporte ejecutivo
reporte = processor.reporte_ejecutivo(donantes, donaciones)
```

---

## ☁️ Despliegue

### Opción 1: Streamlit Cloud (Recomendado)

#### Paso 1: Preparar repositorio en GitHub

```bash
# Agregar archivos
git add .
git commit -m "Primer commit: proyecto completo"

# Push a GitHub (requiere crear repo primero)
git push origin main
```

**Asegúrate de NO incluir:**
- `.env` (usa `.env.example`)
- `__pycache__/`
- `.venv/`

#### Paso 2: Desplegar en Streamlit Cloud

1. Ir a [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click en "New app"
3. Seleccionar tu repositorio
4. Configurar variables de entorno en Streamlit Cloud:
   - Ir a "Advanced Settings"
   - Agregar: `API_BASE_URL = https://tu-api-produccion.com`

### Opción 2: Render

```bash
# Crear archivo Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Push a GitHub
git add Procfile
git commit -m "Add Procfile para Render"
git push origin main
```

Luego desplegar desde Render.com

### Opción 3: Docker

```dockerfile
# Crear Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
```

```bash
# Build y run
docker build -t analytics-donantes .
docker run -p 8501:8501 -e API_BASE_URL=http://api:8080 analytics-donantes
```

---

## 🔍 Solución de Problemas

### ❌ "Error de conexión: No se puede conectar a la API"

**Causa:** La API Spring Boot no está corriendo o la URL es incorrecta

**Solución:**
```bash
# Verificar que la API está corriendo
curl http://localhost:8080/donante

# Si no funciona, revisar:
# 1. El puerto de la API (¿es realmente 8080?)
# 2. La URL en .env
# 3. Logs de la API Java
```

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

**Causa:** Las dependencias no se instalaron correctamente

**Solución:**
```bash
# Activar el entorno virtual
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstalar
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ "Timeout: API no responde"

**Causa:** La API es lenta o no responde

**Solución:**
```bash
# Aumentar timeout en .env
API_TIMEOUT=30

# O revisar performance de la API
```

### ❌ "TypeError: unhashable type: 'dict'"

**Causa:** Estructura de datos anidada en la API

**Solución:**
```python
# En data_cleaning.py, la función procesa objetos anidados
# Esto ya está manejado automáticamente
```

### ❌ El dashboard no se abre

**Causa:** Streamlit no está escuchando en el puerto correcto

**Solución:**
```bash
# Ejecutar con puerto específico
streamlit run app.py --server.port 8501 --server.address localhost
```

---

## 📊 Estructura de Datos de la API

### Endpoint: GET /donante

```json
{
  "idDonante": 1,
  "nombre": "Juan",
  "apellido": "Pérez",
  "fechaNacimiento": "1990-05-15",
  "tipoSangre": "O+",
  "telefono": "3001234567",
  "email": "juan@example.com",
  "activo": true
}
```

### Endpoint: GET /donacion

```json
{
  "idDonacion": 1,
  "fechaDonacion": "2024-01-15",
  "cantidadMl": 450,
  "estado": "completada",
  "donante": {
    "idDonante": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "tipoSangre": "O+"
  },
  "solicitud": {
    "idSolicitud": 1,
    "tipo": "Hospital"
  }
}
```

---

## 👥 Equipo

Proyecto analítico e integración de datos desarrollado en colaboración por:
- **Anderson Vanegas** - *Ingeniería de Datos y Dashboard (Python)*
- **Samuel Ceballos** - *Desarrollo de Backend (Spring Boot & MySQL)*
- **Darwin Cardenas** - *Desarrollo Front-End (React, Vite & Tailwind)*

**Institución:** CESDE  
**Curso:** 
**Año:** 2026

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver LICENSE para detalles.

---

## 🙋 Soporte

¿Preguntas o problemas?

1. Revisa esta documentación
2. Consulta los logs: `streamlit run app.py --logger.level=debug`
3. Abre un issue en GitHub
4. Contacta al equipo de desarrollo

---
