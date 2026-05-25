"""
Configuración centralizada del proyecto de analítica
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ====== CONFIGURACIÓN DE API ======
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8080')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '10'))

# Endpoints principales
ENDPOINTS = {
    'donantes': f'{API_BASE_URL}/donante',
    'donantes_activos': f'{API_BASE_URL}/donante/activos',
    'donantes_por_sangre': lambda tipo: f'{API_BASE_URL}/donante/sangre/{tipo}',
    'donante_id': lambda id: f'{API_BASE_URL}/donante/{id}',
    'donaciones': f'{API_BASE_URL}/donacion',
    'donaciones_donante': lambda id: f'{API_BASE_URL}/donacion/donante/{id}',
    'donacion_id': lambda id: f'{API_BASE_URL}/donacion/{id}',
}

# ====== CONSTANTES DE NEGOCIO ======
TIPOS_SANGRE = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
ESTADOS_DONACION = ['completada', 'pendiente', 'cancelada', 'rechazada']

# ====== CONFIGURACIÓN DE STREAMLIT ======
PAGINA_TITULO = "Analítica Donación de Sangre 🩸"
PAGINA_ICONO = "🏥"

# ====== COLORES Y ESTILOS ======
COLORES = {
    'primario': '#FF6B6B',      # Rojo (sangre)
    'secundario': '#4ECDC4',    # Turquesa (salud)
    'exitoso': '#51CF66',       # Verde
    'advertencia': '#FFD93D',   # Amarillo
    'peligro': '#C92A2A',       # Rojo oscuro
    'neutro': '#6C757D'         # Gris
}

# ====== CACHE Y PERFORMANCE ======
CACHE_TTL = 300  # 5 minutos en segundos

# ====== RUTAS DE DATOS ======
DATA_DIR = 'data'
RAW_DATA_DIR = f'{DATA_DIR}/raw'
PROCESSED_DATA_DIR = f'{DATA_DIR}/processed'
