"""
Módulo de análisis y cálculo de métricas KPI
Genera insights y estadísticas a partir de datos limpios
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Calcula métricas y análisis de donantes y donaciones"""
    
    @staticmethod
    def metricas_generales(df_donantes: pd.DataFrame, df_donaciones: pd.DataFrame) -> dict:
        """
        Calcula métricas generales del sistema
        
        Args:
            df_donantes: DataFrame de donantes
            df_donaciones: DataFrame de donaciones
        
        Returns:
            Diccionario con métricas clave
        """
        metricas = {}
        
        # Donantes
        metricas['total_donantes'] = len(df_donantes)
        metricas['donantes_activos'] = df_donantes['activo'].sum() if 'activo' in df_donantes.columns else 0
        metricas['donantes_inactivos'] = metricas['total_donantes'] - metricas['donantes_activos']
        
        # Donaciones
        metricas['total_donaciones'] = len(df_donaciones)
        metricas['donaciones_completadas'] = len(df_donaciones[df_donaciones['estado'] == 'completada'])
        metricas['donaciones_pendientes'] = len(df_donaciones[df_donaciones['estado'] == 'pendiente'])
        
        # Volumen de sangre
        metricas['volumen_total_ml'] = df_donaciones['cantidadMl'].sum() if 'cantidadMl' in df_donaciones.columns else 0
        metricas['volumen_promedio_ml'] = df_donaciones['cantidadMl'].mean() if 'cantidadMl' in df_donaciones.columns else 0
        
        # Promedio de donaciones por donante
        if metricas['total_donantes'] > 0:
            metricas['donaciones_promedio_donante'] = metricas['total_donaciones'] / metricas['total_donantes']
        else:
            metricas['donaciones_promedio_donante'] = 0
        
        logger.info(f"✓ Métricas generales calculadas")
        return metricas
    
    @staticmethod
    def donantes_por_tipo_sangre(df_donantes: pd.DataFrame) -> pd.DataFrame:
        """
        Agrupa donantes por tipo de sangre
        
        Args:
            df_donantes: DataFrame de donantes
        
        Returns:
            DataFrame con conteo por tipo de sangre
        """
        resultado = df_donantes.groupby('tipoSangre').agg(
            cantidad=('idDonante', 'count'),
            activos=('activo', 'sum') if 'activo' in df_donantes.columns else ('idDonante', 'count')
        ).reset_index()
        
        resultado['porcentaje'] = (resultado['cantidad'] / resultado['cantidad'].sum() * 100).round(2)
        resultado = resultado.sort_values('cantidad', ascending=False)
        
        logger.info(f"✓ Donantes por tipo de sangre calculado")
        return resultado
    
    @staticmethod
    def donaciones_por_mes(df_donaciones: pd.DataFrame) -> pd.DataFrame:
        """
        Agrupa donaciones por mes
        
        Args:
            df_donaciones: DataFrame de donaciones
        
        Returns:
            DataFrame con donaciones por mes
        """
        if 'mes_donacion' not in df_donaciones.columns:
            if 'fechaDonacion' in df_donaciones.columns:
                df_donaciones = df_donaciones.copy()
                df_donaciones['mes_donacion'] = df_donaciones['fechaDonacion'].dt.to_period('M')
        
        resultado = df_donaciones.groupby('mes_donacion').agg(
            cantidad=('idDonacion', 'count'),
            volumen_ml=('cantidadMl', 'sum'),
            promedio_ml=('cantidadMl', 'mean')
        ).reset_index()
        
        resultado['mes_donacion'] = resultado['mes_donacion'].astype('string')
        resultado = resultado.sort_values('mes_donacion')
        
        logger.info(f"✓ Donaciones por mes calculado")
        return resultado
    
    @staticmethod
    def donaciones_por_estado(df_donaciones: pd.DataFrame) -> pd.DataFrame:
        """
        Agrupa donaciones por estado
        
        Args:
            df_donaciones: DataFrame de donaciones
        
        Returns:
            DataFrame con conteo por estado
        """
        resultado = df_donaciones.groupby('estado').agg(
            cantidad=('idDonacion', 'count'),
            volumen_ml=('cantidadMl', 'sum')
        ).reset_index()
        
        resultado['porcentaje'] = (resultado['cantidad'] / resultado['cantidad'].sum() * 100).round(2)
        resultado = resultado.sort_values('cantidad', ascending=False)
        
        logger.info(f"✓ Donaciones por estado calculado")
        return resultado
    
    @staticmethod
    def donantes_top_donadores(df_donantes: pd.DataFrame, df_donaciones: pd.DataFrame, top: int = 10) -> pd.DataFrame:
        """
        Identifica los donantes más activos
        
        Args:
            df_donantes: DataFrame de donantes
            df_donaciones: DataFrame de donaciones
            top: Número de donantes a retornar
        
        Returns:
            DataFrame con top donadores
        """
        # Contar donaciones por donante
        donaciones_por_donante = df_donaciones.groupby('idDonante').agg(
            numero_donaciones=('idDonacion', 'count'),
            volumen_total=('cantidadMl', 'sum'),
            fecha_ultima=('fechaDonacion', 'max')
        ).reset_index()
        
        # Merge con información del donante
        resultado = donaciones_por_donante.merge(
            df_donantes[['idDonante', 'nombre_completo', 'tipoSangre', 'activo']],
            on='idDonante',
            how='left'
        )
        
        resultado = resultado.sort_values('numero_donaciones', ascending=False).head(top)
        
        logger.info(f"✓ Top {top} donadores calculado")
        return resultado
    
    @staticmethod
    def analisis_frecuencia_donacion(df_donantes: pd.DataFrame, df_donaciones: pd.DataFrame) -> dict:
        """
        Analiza la frecuencia de donación por donante
        
        Args:
            df_donantes: DataFrame de donantes
            df_donaciones: DataFrame de donaciones
        
        Returns:
            Diccionario con análisis de frecuencia
        """
        donaciones_por_donante = df_donaciones.groupby('idDonante').size()
        
        analisis = {
            'donantes_sin_donacion': len(df_donantes) - len(donaciones_por_donante),
            'donantes_1_donacion': len(donaciones_por_donante[donaciones_por_donante == 1]),
            'donantes_2_5_donaciones': len(donaciones_por_donante[(donaciones_por_donante >= 2) & (donaciones_por_donante <= 5)]),
            'donantes_5_10_donaciones': len(donaciones_por_donante[(donaciones_por_donante > 5) & (donaciones_por_donante <= 10)]),
            'donantes_mas_10_donaciones': len(donaciones_por_donante[donaciones_por_donante > 10]),
            'promedio_donaciones_donante': donaciones_por_donante.mean()
        }
        
        logger.info(f"✓ Análisis de frecuencia calculado")
        return analisis
    
    @staticmethod
    def disponibilidad_sangre(df_donaciones: pd.DataFrame, df_donantes: pd.DataFrame) -> pd.DataFrame:
        """
        Estima disponibilidad de sangre por tipo (últimas donaciones)
        
        Args:
            df_donaciones: DataFrame de donaciones
            df_donantes: DataFrame de donantes
        
        Returns:
            DataFrame con disponibilidad estimada
        """
        # Última donación completada por tipo de sangre
        donaciones_completadas = df_donaciones[df_donaciones['estado'] == 'completada'].copy()
        
        resultado = donaciones_completadas.groupby('tipoSangre').agg(
            volumen_ultimo=('cantidadMl', 'last'),
            volumen_total_ultimo_mes=('cantidadMl', 'sum'),  # Simulado
            fecha_ultima_donacion=('fechaDonacion', 'max'),
            numero_donaciones_recientes=('idDonacion', 'count')
        ).reset_index()
        
        # Agregar disponibilidad por tipo de sangre
        donantes_por_tipo = df_donantes.groupby('tipoSangre').size().reset_index(name='donantes_disponibles')
        resultado = resultado.merge(donantes_por_tipo, on='tipoSangre', how='left')
        
        resultado = resultado.sort_values('tipoSangre')
        
        logger.info(f"✓ Disponibilidad de sangre calculado")
        return resultado
    
    @staticmethod
    def tendencias_temporales(df_donaciones: pd.DataFrame) -> pd.DataFrame:
        """
        Analiza tendencias de donación en el tiempo
        
        Args:
            df_donaciones: DataFrame de donaciones
        
        Returns:
            DataFrame con análisis temporal
        """
        if 'ano_donacion' not in df_donaciones.columns:
            df_donaciones = df_donaciones.copy()
            df_donaciones['ano_donacion'] = df_donaciones['fechaDonacion'].dt.year
        
        resultado = df_donaciones.groupby('ano_donacion').agg(
            total_donaciones=('idDonacion', 'count'),
            volumen_total=('cantidadMl', 'sum'),
            promedio_ml=('cantidadMl', 'mean')
        ).reset_index()
        
        # Calcular variación porcentual
        resultado['variacion_pct'] = resultado['total_donaciones'].pct_change() * 100
        
        logger.info(f"✓ Tendencias temporales calculado")
        return resultado
    
    @staticmethod
    def reporte_ejecutivo(df_donantes: pd.DataFrame, df_donaciones: pd.DataFrame) -> dict:
        """
        Genera un reporte ejecutivo con KPIs principales
        
        Args:
            df_donantes: DataFrame de donantes
            df_donaciones: DataFrame de donaciones
        
        Returns:
            Diccionario con reporte ejecutivo
        """
        processor = DataProcessor()
        
        # Calcular todas las métricas
        metricas = processor.metricas_generales(df_donantes, df_donaciones)
        frecuencia = processor.analisis_frecuencia_donacion(df_donantes, df_donaciones)
        
        # Composición por tipo de sangre
        composicion = processor.donantes_por_tipo_sangre(df_donantes)
        tipo_sangre_mas_comun = composicion.iloc[0]['tipoSangre'] if len(composicion) > 0 else 'N/A'
        tipo_sangre_mas_raro = composicion.iloc[-1]['tipoSangre'] if len(composicion) > 0 else 'N/A'
        
        # Tasa de éxito de donaciones
        tasa_exito = (metricas['donaciones_completadas'] / metricas['total_donaciones'] * 100) if metricas['total_donaciones'] > 0 else 0
        
        reporte = {
            'fecha_reporte': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'metricas_principales': {
                'total_donantes': metricas['total_donantes'],
                'donantes_activos': metricas['donantes_activos'],
                'tasa_actividad': (metricas['donantes_activos'] / metricas['total_donantes'] * 100) if metricas['total_donantes'] > 0 else 0,
                'total_donaciones': metricas['total_donaciones'],
                'donaciones_completadas': metricas['donaciones_completadas'],
                'tasa_exito_donaciones': tasa_exito,
                'volumen_total_ml': metricas['volumen_total_ml'],
                'volumen_promedio_ml': round(metricas['volumen_promedio_ml'], 2),
            },
            'distribucion_sangre': {
                'tipo_mas_comun': tipo_sangre_mas_comun,
                'tipo_mas_raro': tipo_sangre_mas_raro,
                'cantidad_tipos': len(composicion)
            },
            'patron_donacion': {
                'donantes_sin_historial': frecuencia['donantes_sin_donacion'],
                'donantes_muy_activos': frecuencia['donantes_mas_10_donaciones'],
                'promedio_donaciones_donante': round(frecuencia['promedio_donaciones_donante'], 2)
            }
        }
        
        logger.info(f"✓ Reporte ejecutivo generado")
        return reporte


if __name__ == "__main__":
    # Test: procesar datos
    from data_loader import cargar_todos_datos
    from data_cleaning import procesar_datos_completos
    
    df_donantes_raw, df_donaciones_raw = cargar_todos_datos()
    
    if df_donantes_raw is not None and df_donaciones_raw is not None:
        donantes, donaciones = procesar_datos_completos(df_donantes_raw, df_donaciones_raw)
        
        processor = DataProcessor()
        
        # Generar reportes
        reporte = processor.reporte_ejecutivo(donantes, donaciones)
        print("\nREPORTE EJECUTIVO:")
        print(f"Fecha: {reporte['fecha_reporte']}")
        print(f"Total Donantes: {reporte['metricas_principales']['total_donantes']}")
        print(f"Total Donaciones: {reporte['metricas_principales']['total_donaciones']}")
        print(f"Volumen Total: {reporte['metricas_principales']['volumen_total_ml']} ml")
