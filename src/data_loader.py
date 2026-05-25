"""
Módulo de carga de datos desde la API Spring Boot
Maneja conexiones, errores y conversión a DataFrames
"""
import requests
import pandas as pd
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    """Carga datos desde la API de donantes y donaciones"""
    
    def __init__(self, timeout: int = config.API_TIMEOUT):
        self.timeout = timeout
        self.session = requests.Session()
    
    def _make_request(self, url: str, metodo: str = 'GET') -> Optional[List[Dict]]:
        """
        Realiza request a la API con manejo de errores
        
        Args:
            url: URL del endpoint
            metodo: GET, POST, etc.
        
        Returns:
            Lista de diccionarios o None si hay error
        """
        try:
            logger.info(f"Solicitando: {url}")
            
            if metodo == 'GET':
                response = self.session.get(url, timeout=self.timeout)
            else:
                raise ValueError(f"Método {metodo} no implementado")
            
            response.raise_for_status()  # Lanza excepción si status != 2xx
            
            datos = response.json()
            logger.info(f"✓ Datos obtenidos: {len(datos) if isinstance(datos, list) else 'sin lista'}")
            
            # Si la respuesta es un diccionario, convertir a lista
            if isinstance(datos, dict):
                datos = [datos]
            
            return datos if isinstance(datos, list) else []
        
        except requests.exceptions.Timeout:
            logger.error(f"❌ Timeout: API no responde en {self.timeout}s")
            logger.error(f"   Verifica que la API esté corriendo en: {config.API_BASE_URL}")
            return None
        
        except requests.exceptions.ConnectionError:
            logger.error(f"❌ Error de conexión: No se puede conectar a {config.API_BASE_URL}")
            logger.error(f"   Asegúrate de que la API Spring Boot está corriendo")
            return None
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ Error HTTP {response.status_code}: {response.text}")
            return None
        
        except ValueError as e:
            logger.error(f"❌ Error al parsear JSON: {str(e)}")
            return None
        
        except Exception as e:
            logger.error(f"❌ Error inesperado: {str(e)}")
            return None
    
    def cargar_donantes(self) -> Optional[pd.DataFrame]:
        """
        Carga todos los donantes
        
        Returns:
            DataFrame con donantes o None si hay error
        """
        datos = self._make_request(config.ENDPOINTS['donantes'])
        
        if datos is None:
            return None
        
        try:
            df = pd.DataFrame(datos)
            logger.info(f"✓ DataFrame de donantes: {len(df)} registros, {len(df.columns)} columnas")
            return df
        except Exception as e:
            logger.error(f"❌ Error al crear DataFrame: {str(e)}")
            return None
    
    def cargar_donaciones(self) -> Optional[pd.DataFrame]:
        """
        Carga todas las donaciones
        
        Returns:
            DataFrame con donaciones o None si hay error
        """
        datos = self._make_request(config.ENDPOINTS['donaciones'])
        
        if datos is None:
            return None
        
        try:
            df = pd.DataFrame(datos)
            logger.info(f"✓ DataFrame de donaciones: {len(df)} registros, {len(df.columns)} columnas")
            return df
        except Exception as e:
            logger.error(f"❌ Error al crear DataFrame: {str(e)}")
            return None
    
    def cargar_donantes_activos(self) -> Optional[pd.DataFrame]:
        """
        Carga solo donantes activos
        
        Returns:
            DataFrame con donantes activos
        """
        datos = self._make_request(config.ENDPOINTS['donantes_activos'])
        
        if datos is None:
            return None
        
        try:
            df = pd.DataFrame(datos)
            logger.info(f"✓ Donantes activos: {len(df)} registros")
            return df
        except Exception as e:
            logger.error(f"❌ Error al crear DataFrame: {str(e)}")
            return None
    
    def cargar_donantes_por_sangre(self, tipo_sangre: str) -> Optional[pd.DataFrame]:
        """
        Carga donantes por tipo de sangre
        
        Args:
            tipo_sangre: Ej: 'O+', 'A-', etc.
        
        Returns:
            DataFrame con donantes del tipo de sangre especificado
        """
        url = config.ENDPOINTS['donantes_por_sangre'](tipo_sangre)
        datos = self._make_request(url)
        
        if datos is None:
            return None
        
        try:
            df = pd.DataFrame(datos)
            logger.info(f"✓ Donantes tipo {tipo_sangre}: {len(df)} registros")
            return df
        except Exception as e:
            logger.error(f"❌ Error al crear DataFrame: {str(e)}")
            return None
    
    def cargar_donaciones_donante(self, id_donante: int) -> Optional[pd.DataFrame]:
        """
        Carga todas las donaciones de un donante específico
        
        Args:
            id_donante: ID del donante
        
        Returns:
            DataFrame con donaciones del donante
        """
        url = config.ENDPOINTS['donaciones_donante'](id_donante)
        datos = self._make_request(url)
        
        if datos is None:
            return None
        
        try:
            df = pd.DataFrame(datos)
            logger.info(f"✓ Donaciones del donante {id_donante}: {len(df)} registros")
            return df
        except Exception as e:
            logger.error(f"❌ Error al crear DataFrame: {str(e)}")
            return None


def cargar_todos_datos() -> tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Carga donantes y donaciones en paralelo
    
    Returns:
        Tupla (df_donantes, df_donaciones)
    """
    loader = DataLoader()
    
    logger.info("=" * 60)
    logger.info("INICIANDO CARGA DE DATOS")
    logger.info("=" * 60)
    
    df_donantes = loader.cargar_donantes()
    df_donaciones = loader.cargar_donaciones()
    
    logger.info("=" * 60)
    logger.info("CARGA COMPLETADA")
    logger.info("=" * 60)
    
    return df_donantes, df_donaciones


if __name__ == "__main__":
    # Test: cargar datos
    df_donantes, df_donaciones = cargar_todos_datos()
    
    if df_donantes is not None:
        print("\nPrimeros donantes:")
        print(df_donantes.head())
    
    if df_donaciones is not None:
        print("\nPrimeras donaciones:")
        print(df_donaciones.head())
