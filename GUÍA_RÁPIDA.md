# ⚡ Guía Rápida - Empezar en 5 Minutos

## 🎯 Objetivo
Tener el dashboard corriendo en tu computadora en **menos de 5 minutos**.

---

## 📋 Pasos

### ✅ Paso 1: Preparar la API (1 minuto)

Asegúrate de que la API Spring Boot esté corriendo:

```bash
# En tu terminal de la API
cd Donantes-final-clean-main
mvn spring-boot:run

# Deberías ver:
# Tomcat started on port 8080
```

Si la API no funciona, revisa estos puertos:
- Puerto 8080 (por defecto)
- Puerto 8000
- Puerto 3000

### ✅ Paso 2: Clonar este proyecto (1 minuto)

```bash
git clone <URL-DEL-REPOSITORIO>
cd analytics-donantes
```

### ✅ Paso 3: Configurar entorno (2 minutos)

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

⏳ Espera mientras se instalan las librerías (puede tomar 1-2 minutos)

### ✅ Paso 4: Ejecutar (1 minuto)

```bash
streamlit run app.py
```

🎉 **¡Listo!** El dashboard debería abrirse automáticamente en:
```
http://localhost:8501
```

---

## 🔧 Si Algo Sale Mal

### Error: "No puede conectar a la API"

```bash
# Verifica que la API funciona:
curl http://localhost:8080/donante

# Si no funciona, edita .env
nano .env  # (o usa tu editor favorito)

# Cambia:
API_BASE_URL=http://localhost:8080
# A lo que sea que uses

# Luego reinicia Streamlit (Ctrl+C y streamlit run app.py)
```

### Error: "ModuleNotFoundError: streamlit"

```bash
# Asegúrate de activar el entorno virtual:

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Verifica que ves (venv) al inicio de tu línea

# Reinstala:
pip install -r requirements.txt
```

### Error: "Address already in use"

```bash
# El puerto 8501 está siendo usado. Elige otro:
streamlit run app.py --server.port 8502
```

---

## 📱 Usando el Dashboard

### Una vez que esté corriendo:

1. **Filtra por fechas**: Usa el calendario en la barra izquierda
2. **Filtra por tipo de sangre**: Selecciona los tipos que quieres ver
3. **Filtra por estado**: Elige qué estados de donación ver
4. **Explora gráficos**: Haz click para ampliar, descarga PNG

### Secciones del Dashboard

| Sección | Qué hace |
|---------|----------|
| 📊 **Métricas Principales** | KPIs en números grandes |
| 🩸 **Distribución Sangre** | Gráfico de pastel por tipo |
| 📈 **Tendencias** | Línea de donaciones por mes |
| 📋 **Estado** | Barras de completadas/pendientes/etc |
| ⭐ **Top Donadores** | Ranking de más activos |
| 📊 **Frecuencia** | Cuántas donaciones por donante |

---

## 🔄 Actualizar Datos

El dashboard **se actualiza automáticamente** cada 5 minutos.

Para actualizar manualmente, haz click en el botón **🔄 Actualizar** en la parte superior.

---

## 💾 Próximos Pasos

Una vez funcione localmente:

1. **Crear repositorio en GitHub**
   ```bash
   git init
   git add .
   git commit -m "Primer commit"
   git remote add origin https://github.com/tu-usuario/analytics-donantes
   git push -u origin main
   ```

2. **Desplegar en Streamlit Cloud** (gratis)
   - Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
   - Conecta tu GitHub
   - Deploy en 2 clics

---

## 📚 Para Aprender Más

- **Dashboard completo**: Lee `README.md`
- **Código**: Revisa los archivos en `src/`
- **Configuración**: Edita `config.py`

---

## ❓ ¿Preguntas?

- ¿API no funciona? Verifica que está corriendo en el puerto correcto
- ¿Dashboard no se ve? Verifica que Python 3.8+ está instalado
- ¿Datos vacíos? Verifica que la API tiene donantes/donaciones en la BD

---

**¡Listo! Ahora tienes un dashboard profesional de analítica en tu máquina local.** 🚀

Próximo paso: Configurar Git/GitHub (si aún no lo hiciste) y preparar para despliegue.
