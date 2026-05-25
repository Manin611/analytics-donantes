"""
Módulo de limpieza y transformación de datos (ETL)
Maneja: tipos de datos, nulos, duplicados, validaciones
"""
import pandas as pd
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    """Limpia y transforma datos de donantes y donaciones"""
    
    @staticmethod
    def limpiar_donantes(df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia DataFrame de donantes
        
        Args:
            df: DataFrame de donantes
        
        Returns:
            DataFrame limpio
        """
        df = df.copy()
        
        # 🔄 MAPEO: Traducir nombres de la API/Base de datos al formato esperado por el script
        columnas_map = {
            'id_donante': 'idDonante',
            'fecha_nacimiento': 'fechaNacimiento',
            'tipo_sangre': 'tipoSangre'
        }
        df = df.rename(columns=columnas_map)
        
        logger.info(f"Limpiando donantes: {len(df)} registros")
        
        # Blindaje por si la API viene totalmente vacía
        if df.empty:
            logger.warning("⚠️ El DataFrame de donantes está vacío.")
            return pd.DataFrame(columns=['idDonante', 'nombre', 'apellido', 'tipoSangre', 'activo', 'edad'])
        
        # 1. Eliminar duplicados por ID
        n_antes = len(df)
        df = df.drop_duplicates(subset=['idDonante'], keep='first')
        n_dups = n_antes - len(df)
        if n_dups > 0:
            logger.warning(f"  ⚠️  {n_dups} donantes duplicados eliminados")
        
        # 2. Validar campos obligatorios
        campos_obligatorios = ['idDonante', 'nombre', 'apellido', 'tipoSangre']
        for campo in campos_obligatorios:
            if campo not in df.columns:
                logger.error(f"  ❌ Campo obligatorio faltante: {campo}")
                return pd.DataFrame()
            
            nulos = df[campo].isnull().sum()
            if nulos > 0:
                logger.warning(f"  ⚠️  {nulos} nulos en {campo} - eliminando filas")
                df = df.dropna(subset=[campo])
        
        # 3. Convertir tipos de datos
        df['idDonante'] = df['idDonante'].astype('int32')
        df['nombre'] = df['nombre'].astype('string').str.strip().str.title()
        df['apellido'] = df['apellido'].astype('string').str.strip().str.title()
        df['tipoSangre'] = df['tipoSangre'].astype('string').str.strip().str.upper()
        
        if 'email' in df.columns:
            df['email'] = df['email'].astype('string').str.strip().str.lower()
        
        if 'telefono' in df.columns:
            df['telefono'] = df['telefono'].astype('string').str.strip()
        
        # 4. Convertir fechaNacimiento
        if 'fechaNacimiento' in df.columns:
            try:
                df['fechaNacimiento'] = pd.to_datetime(df['fechaNacimiento'])
                # Calcular edad
                df['edad'] = (datetime.now() - df['fechaNacimiento']).dt.days // 365
            except Exception as e:
                logger.warning(f"  ⚠️  Error al convertir fechaNacimiento: {e}")
                df['edad'] = None
        else:
            df['edad'] = None
        
        # 5. Convertir activo a boolean
        if 'activo' in df.columns:
            df['activo'] = df['activo'].astype('bool')
        
        # 6. Validar tipos de sangre
        tipos_validos = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        tipos_invalidos = df[~df['tipoSangre'].isin(tipos_validos)]
        if len(tipos_invalidos) > 0:
            logger.warning(f"  ⚠️  {len(tipos_invalidos)} tipos de sangre inválidos encontrados")
            logger.info(f"     Tipos inválidos: {tipos_invalidos['tipoSangre'].unique()}")
        
        logger.info(f"✓ Donantes limpios: {len(df)} registros")
        return df
    
    @staticmethod
    def limpiar_donaciones(df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia DataFrame de donaciones
        
        Args:
            df: DataFrame de donaciones
        
        Returns:
            DataFrame limpio
        """
        df = df.copy()
        
        # 🔄 MAPEO: Traducir nombres de la tabla donaciones al formato del script
        columnas_map = {
            'id_donacion': 'idDonacion',
            'fecha_donacion': 'fechaDonacion',
            'cantidad_ml': 'cantidadMl',
            'id_donante': 'idDonante'
        }
        df = df.rename(columns=columnas_map)
        
        logger.info(f"Limpiando donaciones: {len(df)} registros")
        
        # Blindaje por si la API viene vacía
        if df.empty:
            logger.warning("⚠️ El DataFrame de donaciones está vacío.")
            return pd.DataFrame(columns=['idDonacion', 'fechaDonacion', 'cantidadMl', 'estado', 'idDonante'])
        
        # 1. Eliminar duplicados por ID
        n_antes = len(df)
        df = df.drop_duplicates(subset=['idDonacion'], keep='first')
        n_dups = n_antes - len(df)
        if n_dups > 0:
            logger.warning(f"  ⚠️  {n_dups} donaciones duplicadas eliminadas")
        
        # 2. Validar campos obligatorios
        campos_obligatorios = ['idDonacion', 'fechaDonacion', 'cantidadMl', 'estado']
        for campo in campos_obligatorios:
            if campo not in df.columns:
                logger.error(f"  ❌ Campo obligatorio faltante: {campo}")
                return pd.DataFrame()
            
            nulos = df[campo].isnull().sum()
            if nulos > 0:
                logger.warning(f"  ⚠️  {nulos} nulos en {campo} - eliminando filas")
                df = df.dropna(subset=[campo])
        
        # 3. Convertir tipos de datos
        df['idDonacion'] = df['idDonacion'].astype('int32')
        
        # Convertir fechaDonacion
        try:
            df['fechaDonacion'] = pd.to_datetime(df['fechaDonacion'])
        except Exception as e:
            logger.warning(f"  ⚠️  Error al convertir fechaDonacion: {e}")
        
        # Convertir cantidadMl
        df['cantidadMl'] = pd.to_numeric(df['cantidadMl'], errors='coerce').astype('int32')
        
        # Convertir estado
        df['estado'] = df['estado'].astype('string').str.strip().str.lower()
        
        # 4. Validar estados
        estados_validos = ['completada', 'pendiente', 'cancelada', 'rechazada']
        estados_invalidos = df[~df['estado'].isin(estados_validos)]
        if len(estados_invalidos) > 0:
            logger.warning(f"  ⚠️  {len(estados_invalidos)} estados inválidos encontrados")
        
        # 5. Validar cantidad de sangre (450-500 ml es estándar)
        donaciones_anomalas = df[(df['cantidadMl'] < 100) | (df['cantidadMl'] > 1000)]
        if len(donaciones_anomalas) > 0:
            logger.warning(f"  ⚠️  {len(donaciones_anomalas)} donaciones con cantidad anómala")
        
        logger.info(f"✓ Donaciones limpias: {len(df)} registros")
        return df
    
    @staticmethod
    def enriquecer_donantes(df_donantes: pd.DataFrame) -> pd.DataFrame:
        """
        Enriquece datos de donantes con columnas calculadas
        """
        df = df_donantes.copy()
        
        # Blindaje preventivo contra dataframes vacíos
        if df.empty or 'tipoSangre' not in df.columns:
            df['nombre_completo'] = pd.Series(dtype='string')
            df['grupo_edad'] = pd.Series(dtype='category')
            df['sangre_rara'] = pd.Series(dtype='bool')
            return df
        
        # Nombre completo
        if 'nombre' in df.columns and 'apellido' in df.columns:
            df['nombre_completo'] = df['nombre'] + ' ' + df['apellido']
        
        # Riesgo de edad (si tenemos edad)
        if 'edad' in df.columns and df['edad'].notnull().any():
            df['grupo_edad'] = pd.cut(
                df['edad'],
                bins=[0, 18, 25, 35, 50, 65, 120],
                labels=['<18', '18-25', '25-35', '35-50', '50-65', '>65']
            )
        else:
            df['grupo_edad'] = np.nan
        
        # Riesgo de tipo de sangre (raro vs común)
        df['sangre_rara'] = df['tipoSangre'].isin(['AB-', 'AB+', 'B-'])
                
        return df
    
    @staticmethod
    def enriquecer_donaciones(df_donaciones: pd.DataFrame, df_donantes: pd.DataFrame = None) -> pd.DataFrame:
        """
        Enriquece datos de donaciones con columnas calculadas
        """
        df = df_donaciones.copy()
        
        if df.empty:
            df['mes_donacion'] = pd.Series(dtype='period[M]')
            df['ano_donacion'] = pd.Series(dtype='int32')
            df['mes_nombre'] = pd.Series(dtype='string')
            df['categoria_cantidad'] = pd.Series(dtype='category')
            return df
        
        # Agregar información del donante si está disponible
        if df_donantes is not None and not df_donantes.empty and 'idDonante' in df.columns:
            try:
                # Merge directo usando la columna homologada idDonante
                df = df.merge(
                    df_donantes[['idDonante', 'tipoSangre', 'nombre_completo']],
                    on='idDonante',
                    how='left'
                )
            except Exception as e:
                logger.warning(f"  ⚠️  No se pudo enriquecer con datos de donante: {e}")
        
        # Extraer mes y año
        if 'fechaDonacion' in df.columns:
            df['fechaDonacion'] = pd.to_datetime(df['fechaDonacion'])
            df['mes_donacion'] = df['fechaDonacion'].dt.to_period('M')
            df['ano_donacion'] = df['fechaDonacion'].dt.year
            df['mes_nombre'] = df['fechaDonacion'].dt.strftime('%B')
        
        # Clasificar cantidad
        if 'cantidadMl' in df.columns:
            df['categoria_cantidad'] = pd.cut(
                df['cantidadMl'],
                bins=[0, 250, 450, 500, 1000],
                labels=['Bajo (<250ml)', 'Normal (250-450ml)', 'Alto (450-500ml)', 'Muy Alto (>500ml)']
            )
        
        return df


def procesar_datos_completos(df_donantes: pd.DataFrame, df_donaciones: pd.DataFrame) -> tuple:
    """
    Pipeline completo de limpieza y enriquecimiento
    """
    logger.info("\n" + "="*60)
    logger.info("INICIANDO PIPELINE ETL")
    logger.info("="*60 + "\n")
    
    # Limpiar
    donantes = DataCleaner.limpiar_donantes(df_donantes)
    donaciones = DataCleaner.limpiar_donaciones(df_donaciones)
    
    # Enriquecer
    donantes = DataCleaner.enriquecer_donantes(donantes)
    donaciones = DataCleaner.enriquecer_donaciones(donaciones, donantes)
    
    logger.info("\n" + "="*60)
    logger.info("PIPELINE ETL COMPLETADO")
    logger.info("="*60 + "\n")
    
    return donantes, donaciones


if __name__ == "__main__":
    from data_loader import cargar_todos_datos
    
    df_donantes, df_donaciones = cargar_todos_datos()
    
    if df_donantes is not None and df_donaciones is not None:
        donantes, donaciones = procesar_datos_completos(df_donantes, df_donaciones)
        
        print("\nDonantes limpios:")
        print(donantes.info())
        print(donantes.head())
        
        print("\nDonaciones limpias:")
        print(donaciones.info())
        print(donaciones.head())