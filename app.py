"""
Esta aplicación de Streamlit proporciona un análisis de datos económicos,
que incluye proyecciones y tasas de crecimiento de diferentes sectores y entidades.
"""

import re
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

img = Image.open('inegi.png')

st.set_page_config(page_title='Demografía de Negocios', page_icon=img, layout='wide')

st.title('Simulador de los Resultados de los Indicadores Demográficos Económicos de México')


# --- CARGA Y PROCESAMIENTO DE DATOS PRINCIPALES ---
@st.cache_data
def cargar_datos():
    """Carga y unifica todos los archivos CSV de censos con su censo correspondiente."""

    # Mapeo de archivos a años de censo
    mapeo_archivos = {
        'NAC_UE_POT_SEC_1.csv': 1988, 'NAC_UE_POT_SEC_2.csv': 1993,
        'NAC_UE_POT_SEC_3.csv': 1998, 'NAC_UE_POT_SEC_4.csv': 2003,
        'NAC_UE_POT_SEC_5.csv': 2008, 'NAC_UE_POT_SEC_6.csv': 2013,
        'NAC_UE_POT_SEC_7.csv': 2018, 'NAC_UE_POT_SEC_8.csv': 2023
    }

    lista_df = []

    for archivo, anio_censo in mapeo_archivos.items():
        try:
            # Detectar el separador y la codificación
            with open(archivo, 'r', encoding='latin1') as f:
                header = f.readline()
                if ',' in header:
                    separator = ','
                elif ';' in header:
                    separator = ';'
                else:
                    separator = ','
            
            df_temp = pd.read_csv(archivo, encoding='latin1', sep=separator, low_memory=False)
            
            df_temp.columns = [col.upper().strip().replace(' ', '_') for col in df_temp.columns]
            
            df_temp.rename(columns={
                'ENTIDAD': 'entidad', 'SECTOR': 'sector',
                'TAMAÑO': 'personal_ocupado_estrato', 'UNIDADES_ECONÓMICAS': 'ue',
                'AÑO': 'generacion','PERSONAL_OCUPADO': 'po'
            }, inplace=True)
            
            df_temp['censo'] = anio_censo
            df_temp.columns = [col.lower() for col in df_temp.columns]
            
            if 'sector' in df_temp.columns:
                df_temp['sector'] = df_temp['sector'].str.upper().str.strip()

            lista_df.append(df_temp)
        except FileNotFoundError:
            st.warning(f"Archivo no encontrado: {archivo}")
        except Exception as e:
            st.error(f"Error al leer el archivo {archivo}: {e}")
            continue
    
    if not lista_df:
        st.error("No se encontraron archivos de datos. Asegúrate de que los archivos estén en la misma carpeta.")
        return pd.DataFrame()

    df_unificado = pd.concat(lista_df, ignore_index=True)
    df_unificado['ue'] = pd.to_numeric(df_unificado['ue'], errors='coerce').fillna(0)
    df_unificado['personal_ocupado_estrato'] = pd.to_numeric(df_unificado['personal_ocupado_estrato'], errors='coerce')
    df_unificado['generacion'] = pd.to_numeric(df_unificado['generacion'], errors='coerce').fillna(0).astype(int)
    df_unificado['po'] = pd.to_numeric(df_unificado['po'], errors='coerce').fillna(0)
    

    # Eliminar filas con valores nulos en las columnas clave para evitar el TypeError
    df_unificado.dropna(subset=['entidad', 'sector', 'personal_ocupado_estrato'], inplace=True)

    df_unificado['sector'] = df_unificado['sector'].replace({
        'SERVICIOS_PRIVADOS_NO_FINANCIEROS': 'SERVICIOS',
        'OTROS_SECTORES': 'OTROS SEC'
    })

    return df_unificado

# Cargar datos al inicio
df = cargar_datos()

if df.empty:
    st.stop()

# --- SELECTBOXES CON CÓDIGO FIJO ---
# Inicializa la variable personal_seleccionado para evitar errores
personal_seleccionado = None

with st.sidebar:
    entidad = st.selectbox(
        'ENTIDAD FEDERATIVA:',
        ['NACIONAL','AGUASCALIENTES','BAJA CALIFORNIA','BAJA CALIFORNIA SUR','CAMPECHE','COAHUILA DE ZARAGOZA','COLIMA','CHIAPAS','CHIHUAHUA','CIUDAD DE MEXICO','DURANGO','GUANAJUATO','GUERRERO','HIDALGO','JALISCO','MEXICO','MICHOACAN DE OCAMPO','MORELOS','NAYARIT','NUEVO LEON','OAXACA','PUEBLA','QUERETARO','QUINTANA ROO','SAN LUIS POTOSI','SINALOA','SONORA','TABASCO','TAMAULIPAS','TLAXCALA','VERACRUZ DE IGNACIO DE LA LLAVE','YUCATAN','ZACATECAS']
    )

    sector = st.selectbox(
        'SECTOR:',
        ['TODOS LOS SECTORES','COMERCIO','MANUFACTURAS','OTROS SECTORES','SERVICIOS PRIVADOS NO FINANCIEROS']
    )

    if entidad == 'NACIONAL' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101-250 Personas ocupadas','251 y más Personas ocupadas']
        )

    elif entidad == 'NACIONAL' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51 y más Personas ocupadas']
        )

    elif entidad == 'NACIONAL' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31 y más Personas ocupadas']
        )

    elif entidad == 'NACIONAL' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31 y más Personas ocupadas']
        )
        
    elif entidad == 'NACIONAL' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101 y más Personas ocupadas']
        )

    #AGUASCALIENTES
    
    elif entidad == 'AGUASCALIENTES' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'AGUASCALIENTES' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'AGUASCALIENTES' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'AGUASCALIENTES' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )
        
    elif entidad == 'AGUASCALIENTES' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS']
        )

    #BAJA CALIFORNIA

    elif entidad == 'BAJA CALIFORNIA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101 y más Personas ocupadas']
        )

    elif entidad == 'BAJA CALIFORNIA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'BAJA CALIFORNIA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'BAJA CALIFORNIA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'BAJA CALIFORNIA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    #BAJA CALIFORNIA SUR

    elif entidad == 'BAJA CALIFORNIA SUR' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'BAJA CALIFORNIA SUR' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS']
        )

    elif entidad == 'BAJA CALIFORNIA SUR' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'BAJA CALIFORNIA SUR' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )
        
    elif entidad == 'BAJA CALIFORNIA SUR' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS']
        )

    #CAMPECHE

    elif entidad == 'CAMPECHE' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'CAMPECHE' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'CAMPECHE' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'CAMPECHE' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )
        
    elif entidad == 'CAMPECHE' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )
        
    #COAHUILA DE ZARAGOZA

    elif entidad == 'COAHUILA DE ZARAGOZA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51 y más Personas ocupadas']
        )

    elif entidad == 'COAHUILA DE ZARAGOZA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'COAHUILA DE ZARAGOZA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'COAHUILA DE ZARAGOZA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'COAHUILA DE ZARAGOZA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #COLIMA

    elif entidad == 'COLIMA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'COLIMA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    elif entidad == 'COLIMA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'COLIMA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )
        
    elif entidad == 'COLIMA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS']
        )
        
    #CHIAPAS

    elif entidad == 'CHIAPAS' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'CHIAPAS' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    elif entidad == 'CHIAPAS' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'CHIAPAS' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'CHIAPAS' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #CHIHUAHUA

    elif entidad == 'CHIHUAHUA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21 y más Personas ocupadas']
        )

    elif entidad == 'CHIHUAHUA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'CHIHUAHUA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'CHIHUAHUA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'CHIHUAHUA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )
        
    #CIUDAD DE MEXICO

    elif entidad == 'CIUDAD DE MEXICO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101-250 Personas ocupadas','251 y más Personas ocupadas']
        )

    elif entidad == 'CIUDAD DE MEXICO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51 y más Personas ocupadas']
        )

    elif entidad == 'CIUDAD DE MEXICO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101 y más Personas ocupadas']
        )

    elif entidad == 'CIUDAD DE MEXICO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101 y más Personas ocupadas']
        )
        
    elif entidad == 'CIUDAD DE MEXICO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #DURANGO

    elif entidad == 'DURANGO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'DURANGO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'DURANGO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'DURANGO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'DURANGO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #GUANAJUATO

    elif entidad == 'GUANAJUATO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101 y más Personas ocupadas']
        )

    elif entidad == 'GUANAJUATO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'GUANAJUATO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'GUANAJUATO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'GUANAJUATO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #GUERRERO

    elif entidad == 'GUERRERO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'GUERRERO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'GUERRERO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'GUERRERO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'GUERRERO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #GUANAJUATO

    elif entidad == 'GUANAJUATO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101 y más Personas ocupadas']
        )

    elif entidad == 'GUANAJUATO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'GUANAJUATO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'GUANAJUATO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'GUANAJUATO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #HIDALGO

    elif entidad == 'HIDALGO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'HIDALGO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'HIDALGO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'HIDALGO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'HIDALGO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #JALISCO

    elif entidad == 'JALISCO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101-250 Personas ocupadas','251 y más Personas ocupadas']
        )

    elif entidad == 'JALISCO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31 y más Personas ocupadas']
        )

    elif entidad == 'JALISCO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51 y más Personas ocupadas']
        )

    elif entidad == 'JALISCO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31 y más Personas ocupadas']
        )
        
    elif entidad == 'JALISCO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    #MEXICO

    elif entidad == 'MEXICO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101-250 Personas ocupadas','251 y más Personas ocupadas']
        )

    elif entidad == 'MEXICO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101 y más Personas ocupadas']
        )

    elif entidad == 'MEXICO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31 y más Personas ocupadas']
        )

    elif entidad == 'MEXICO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31 y más Personas ocupadas']
        )
        
    elif entidad == 'MEXICO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    #MICHOACAN DE OCAMPO

    elif entidad == 'MICHOACAN DE OCAMPO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31 y más Personas ocupadas']
        )

    elif entidad == 'MICHOACAN DE OCAMPO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'MICHOACAN DE OCAMPO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'MICHOACAN DE OCAMPO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'MICHOACAN DE OCAMPO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    #MORELOS

    elif entidad == 'MORELOS' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'MORELOS' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    elif entidad == 'MORELOS' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'MORELOS' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'MORELOS' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #NAYARIT

    elif entidad == 'NAYARIT' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'NAYARIT' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'NAYARIT' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'NAYARIT' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'NAYARIT' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #NUEVO LEON

    elif entidad == 'NUEVO LEON' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101-250 Personas ocupadas','251 y más Personas ocupadas']
        )

    elif entidad == 'NUEVO LEON' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101 y más Personas ocupadas']
        )

    elif entidad == 'NUEVO LEON' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51 y más Personas ocupadas']
        )

    elif entidad == 'NUEVO LEON' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51 y más Personas ocupadas']
        )
        
    elif entidad == 'NUEVO LEON' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    #OAXACA

    elif entidad == 'OAXACA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21 y más Personas ocupadas']
        )

    elif entidad == 'OAXACA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'OAXACA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'OAXACA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'OAXACA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    #PUEBLA

    elif entidad == 'PUEBLA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31 y más Personas ocupadas']
        )

    elif entidad == 'PUEBLA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'PUEBLA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'PUEBLA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21 y más Personas ocupadas']
        )
        
    elif entidad == 'PUEBLA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    #QUERÉTARO

    elif entidad == 'QUERÉTARO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'QUERÉTARO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'QUERÉTARO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'QUERÉTARO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'QUERÉTARO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #QUINTANA ROO

    elif entidad == 'QUINTANA ROO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'QUINTANA ROO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'QUINTANA ROO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'QUINTANA ROO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'QUINTANA ROO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS']
        )

    #SAN LUIS POTOSI

    elif entidad == 'SAN LUIS POTOSI' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'SAN LUIS POTOSI' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'SAN LUIS POTOSI' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'SAN LUIS POTOSI' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'SAN LUIS POTOSI' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #SINALOA

    elif entidad == 'SINALOA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21 y más Personas ocupadas']
        )

    elif entidad == 'SINALOA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'SINALOA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'SINALOA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'SINALOA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    #SONORA

    elif entidad == 'SONORA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21 y más Personas ocupadas']
        )

    elif entidad == 'SONORA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'SONORA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'SONORA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'SONORA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    #TABASCO

    elif entidad == 'TABASCO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21 y más Personas ocupadas']
        )

    elif entidad == 'TABASCO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'TABASCO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'TABASCO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'TABASCO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    #TAMAULIPAS

    elif entidad == 'TAMAULIPAS' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21 y más Personas ocupadas']
        )

    elif entidad == 'TAMAULIPAS' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'TAMAULIPAS' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'TAMAULIPAS' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'TAMAULIPAS' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    #TLAXCALA

    elif entidad == 'TLAXCALA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'TLAXCALA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'TLAXCALA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'TLAXCALA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'TLAXCALA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    #VERACRUZ DE IGNACIO DE LA LLAVE

    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21-30 Personas ocupadas','31-50 Personas ocupadas','51-100 Personas ocupadas','101 y más Personas ocupadas']
        )

    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21 y más Personas ocupadas']
        )
        
    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    #YUCATAN

    elif entidad == 'YUCATAN' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16-20 Personas ocupadas','21 y más Personas ocupadas']
        )

    elif entidad == 'YUCATAN' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'YUCATAN' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )

    elif entidad == 'YUCATAN' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11-15 Personas ocupadas','16 y más Personas ocupadas']
        )
        
    elif entidad == 'YUCATAN' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    #ZACATECAS

    elif entidad == 'ZACATECAS' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
        ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'ZACATECAS' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6 y más Personas ocupadas']
        )

    elif entidad == 'ZACATECAS' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )

    elif entidad == 'ZACATECAS' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3-5 Personas ocupadas','6-10 Personas ocupadas','11 y más Personas ocupadas']
        )
        
    elif entidad == 'ZACATECAS' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'TAMAÑO:',
            ['CONCENTRADOS','0-2 Personas ocupadas','3 y más Personas ocupadas']
        )

    
    #--- SELECCIÓN DE VARIABLES DE ANÁLISIS ---

    st.write('FENÓMENO DEMOGRÁFICO')
    fenomeno_demografico = st.radio('Seleccionar:', ['Población activa', 'Natalidad', 'Supervivencia','Mortalidad'],label_visibility='visible')
    st.write('VARIABLE DE ANÁLISIS:')
    mostrar_unidades = st.checkbox("Negocios", value=True)
    mostrar_personal = st.checkbox("Empleos", value=False)

    
    options = ["Mostrar Matriz"]
    selection = st.segmented_control(
        "MATRIZ DE DATOS", options, selection_mode="single"
    )

mapa_estratos = {
    '0-2 Personas ocupadas': 1,
    '3-5 Personas ocupadas': 2,
    '6-10 Personas ocupadas': 3,
    '11-15 Personas ocupadas': 4,
    '16-20 Personas ocupadas': 5,
    '21-30 Personas ocupadas': 6,
    '31-50 Personas ocupadas': 7,
    '51-100 Personas ocupadas': 8,
    '101-250 Personas ocupadas': 9,    
    '3 y más Personas ocupadas': 2,
    '6 y más Personas ocupadas': 3,
    '11 y más Personas ocupadas': 4,
    '16 y más Personas ocupadas': 5,
    '21 y más Personas ocupadas': 6,    
    '31 y más Personas ocupadas': 7,
    '51 y más Personas ocupadas': 8,
    '101 y más Personas ocupadas': 9,
    '251 y más Personas ocupadas': 10
}
# --- FIN DE SELECTBOXES ---



# --- LÓGICA DE FILTROS Y VISUALIZACIÓN ---

df_final_filtrado = df.copy()

# Filtro por entidad
if entidad != 'NACIONAL':
    df_final_filtrado = df_final_filtrado[df_final_filtrado['entidad'] == entidad]

# Filtro por sector
if sector != 'TODOS LOS SECTORES':
    df_final_filtrado = df_final_filtrado[df_final_filtrado['sector'].str.upper().str.strip() == sector]

# Nuevo filtro por estrato de personal ocupado
if personal_seleccionado and personal_seleccionado != 'CONCENTRADOS':
    estrato_seleccionado = mapa_estratos.get(personal_seleccionado)
    
    if estrato_seleccionado:
        if 'y más Personas ocupadas' in personal_seleccionado:
            # Filtrar por el estrato y todos los mayores
            df_final_filtrado = df_final_filtrado[df_final_filtrado['personal_ocupado_estrato'] >= estrato_seleccionado]
        else:
            # Filtrar solo por el estrato exacto
            df_final_filtrado = df_final_filtrado[df_final_filtrado['personal_ocupado_estrato'] == estrato_seleccionado]
    else:
        st.warning("No se pudo interpretar el formato del rango de personal ocupado. El filtro no se aplicará.")
    

# --- VISUALIZACIÓN DE LA TABLA SOLICITADA ---

if df_final_filtrado.empty:
    st.warning("No se encontraron datos para la combinación de filtros seleccionada. Intenta con otras opciones.")
else:
    df_final_filtrado = df_final_filtrado[df_final_filtrado['generacion'] >= 1983]
    df_final_filtrado['generacion'] = pd.to_numeric(df_final_filtrado['generacion'], errors='coerce')
    df_final_filtrado.dropna(subset=['generacion'], inplace=True)
    df_final_filtrado['generacion'] = df_final_filtrado['generacion'].astype(int)

    if mostrar_personal or mostrar_unidades:
        # Crear tabla pivote con múltiples valores
        valores = []
        if mostrar_personal:
            valores.append('po')
        if mostrar_unidades:
            valores.append('ue')

        tabla_pivote = pd.pivot_table(
            df_final_filtrado,
            values=valores,
            index='generacion',
            columns='censo',
            aggfunc='sum',
            fill_value=0
        )

        # Asegurar que el índice tenga nombre
        tabla_pivote.index.name = 'Año'

        # Aplanar columnas para que queden como: "Censo 2008 - Unidades Económicas"
        tabla_pivote.columns = [f"CE {col} - {metrica.upper()}" for metrica, col in tabla_pivote.columns]

        # Ordenar columnas por censo y tipo de métrica
        tabla_pivote = tabla_pivote.reindex(sorted(tabla_pivote.columns), axis=1)

        # Agregar fila de totales
        tabla_pivote.loc[0] = tabla_pivote.sum(axis=0)

        # Formatear tabla
        tabla_formato = tabla_pivote.replace(0, '')
        tabla_formato = tabla_formato.map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        
        #st.dataframe(tabla_formato, use_container_width=True)
    else:
        st.info("Selecciona al menos una casilla para mostrar la información.")

matriz_principal = tabla_formato.copy()


if selection == 'Mostrar Matriz':
    st.markdown('---')
    st.dataframe(matriz_principal, use_container_width=True)
else:
    st.empty()
    
        






# --- CÁLCULO Y VISUALIZACIÓN DEL CRECIMIENTO DINÁMICO ---
#st.subheader("Índice de Crecimiento por Censo")

# Obtener la fila de totales
totales_numericos = tabla_pivote.loc[0]

# Inicializar diccionario para guardar resultados por métrica
crecimientos = {}

# Función para calcular crecimiento
def calcular_crecimiento(columnas):
    resultados = []
    etiquetas = []
    for i in range(1, len(columnas)):
        col_actual = columnas[i]
        col_anterior = columnas[i - 1]

        try:
            anio_actual = int(col_actual.split(' ')[-1])
            anio_anterior = int(col_anterior.split(' ')[-1])
        except:
            anio_actual = col_actual
            anio_anterior = col_anterior

        total_actual = totales_numericos[col_actual]
        total_anterior = totales_numericos[col_anterior]

        if total_anterior > 0:
            crecimiento = (total_actual / total_anterior) ** 0.2
            resultados.append(round(crecimiento, 14))
        else:
            resultados.append(None)
        etiquetas.append(f'{anio_anterior.replace('PO','').replace('UE','')}{anio_actual.replace('PO','').replace('UE','').replace('-','')}'.replace(' ',''))

    return resultados, etiquetas

# Detectar columnas por métrica
columnas_ue = [col for col in totales_numericos.index if 'UE' in col]
columnas_po = [col for col in totales_numericos.index if 'PO' in col]

# Calcular según selección
filas = []
nombres_filas = []

if mostrar_unidades and columnas_ue:
    resultados, etiquetas = calcular_crecimiento(columnas_ue)
    filas.append(resultados)
    nombres_filas.append("Unidades Económicas")

if mostrar_personal and columnas_po:
    resultados, etiquetas = calcular_crecimiento(columnas_po)
    filas.append(resultados)
    nombres_filas.append("Personal Ocupado")

# Mostrar tabla combinada
if filas:
    df_crecimiento = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
    #st.dataframe(df_crecimiento, use_container_width=True)
else:
    st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")

#Tratando nueva tabla para cálculos posteriores
datos_totales = tabla_pivote.loc[0]
nombres_columnas = tabla_pivote.columns
df_totales = pd.DataFrame([datos_totales], columns=nombres_columnas)
df_transpuesto = df_totales.T.reset_index()
df_transpuesto.columns = ['Columna_Original','Total']
df_transpuesto[['Año','Unidad']] = df_transpuesto['Columna_Original'].str.split(' - ', expand=True)
df_final = df_transpuesto.pivot(index='Unidad', columns='Año', values='Total')
#st.dataframe(df_final, use_container_width=True) #QUITAR NUMERAL CUANDO SEA NECESARIO VER

# --- CARGA Y PROCESAMIENTO DE DATOS DE PROBABILIDADES ---
@st.cache_data
def cargar_probabilidades():
        """Carga y procesa el archivo de probabilidades."""
        try:
            df_prob = pd.read_csv('PROBABILIDADES.csv')
            df_prob.columns = [col.upper().strip().replace(' ', '_') for col in df_prob.columns]            
            df_prob['ENTIDAD'] = df_prob['ENTIDAD'].str.upper().str.strip()
            df_prob['SECTOR'] = df_prob['SECTOR'].str.upper().str.strip()
            df_prob['TAMAÑO'] = df_prob['TAMAÑO']
            return df_prob
        except FileNotFoundError:
            st.error("Archivo 'PROBABILIDADES.csv' no encontrado.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error al leer 'PROBABILIDADES.csv': {e}")
            return pd.DataFrame()

# --- PROYECCIÓN DE UNIDADES ECONÓMICAS ---

        
# Obtener la lista de censos y valores
censos_str = df_crecimiento.columns.tolist()

# Inicializar DataFrame con columnas dinámicas según selección
columnas = ['Año']
if mostrar_unidades:
    columnas += ('Número de Negocios','Tasa Crecimiento UE (%)')    
if mostrar_personal:
    columnas += ('Personal Ocupado','Tasa Crecimiento PO (%)')    

df_proyeccion = pd.DataFrame(columns=columnas)

# Iterar sobre los periodos censales
for i in range(len(df_crecimiento.columns)):
    periodo = df_crecimiento.columns[i]
    partes = periodo.split('-')

    anio_inicio_completo = partes[0].strip()
    anio_fin_completo = partes[1].strip()

    anio_inicio_str = anio_inicio_completo.replace('CE','')
    anio_fin_str = anio_fin_completo.replace('CE','')
    
    anio_inicio = int(anio_inicio_str)
    anio_fin = int(anio_fin_str)

    fila_inicial = {'Año': anio_inicio}


    etiqueta_columna = f'CE {anio_inicio}'
        

    if mostrar_unidades: 
        valor_actual_ue = df_final.loc['UE',etiqueta_columna]
        tasa_ue = df_crecimiento.loc['Unidades Económicas', periodo]
        fila_inicial['Número de Negocios'] = valor_actual_ue

    if mostrar_personal:
        valor_actual_po = df_final.loc['PO',etiqueta_columna]
        tasa_po = df_crecimiento.loc['Personal Ocupado', periodo]
        fila_inicial['Personal Ocupado'] = valor_actual_po

    
    df_proyeccion.loc[len(df_proyeccion)] = fila_inicial

    # Proyección intermedia
    for anio in range(anio_inicio + 1, anio_fin):
        if anio_fin > 2019:
            break  # No proyectar más allá de 2019
        fila = {'Año': anio}
        if mostrar_unidades:
            valor_actual_ue *= tasa_ue
            fila['Número de Negocios'] = valor_actual_ue
        if mostrar_personal:
            valor_actual_po *= tasa_po
            fila['Personal Ocupado'] = valor_actual_po
        df_proyeccion.loc[len(df_proyeccion)] = fila

#TASAS IMSS
tasas_imss = {
    'Año': [2019, 2020, 2021, 2022],
    'Tasas': [1.0184,0.9681,1.0558,1.0319]
}


# --- CÁLCULO DE TASAS QUINQUENALES (Solo para UE, pero se ejecuta el bucle) ---

# 1. Inicializar variables de proyección ANTES de cualquier condicional

valor_2019_proyectado_ue = None
valor_2019_proyectado_po = None
if mostrar_unidades:
    tasas_quinquenales_ue = []
    # Ya no necesitamos tasas_quinquenales_po

    # Este bucle solo es necesario para acumular tasas_quinquenales_ue
    for i in range(len(df_final.columns) - 1): 
        censo_actual_str = df_final.columns[i]
        censo_siguiente_str = df_final.columns[i + 1]

        # Usamos try/except para el caso de etiquetas sin 'CE '
        try:
            anio_siguiente = int(censo_siguiente_str.replace('CE ', ''))
        except:
            anio_siguiente = 9999 

        if anio_siguiente > 2023:
            break

        # Acumulación de Tasas (Unidades Económicas)
        
        valor_actual_ue = df_final.loc['UE', censo_actual_str]
        valor_siguiente_ue = df_final.loc['UE', censo_siguiente_str]
        
        if valor_actual_ue > 0:
            tasa_quinquenal_ue = (valor_siguiente_ue / valor_actual_ue)
            tasas_quinquenales_ue.append(tasa_quinquenal_ue)


    # --- CÁLCULO DE PROMEDIOS Y PROYECCIÓN A 2019 (FUERA DEL BUCLE) ---

    # Proyección UE (Utiliza el promedio quinquenal de los censos)

    if tasas_quinquenales_ue:
        promedio_quinquenal_ue = sum(tasas_quinquenales_ue) / len(tasas_quinquenales_ue)
        tasa_anual_promedio_ue = promedio_quinquenal_ue**(1/6)
    else:
        tasa_anual_promedio_ue = 1 

    # Buscar el valor final proyectado de 2018
    valor_2018_ue = df_proyeccion.loc[df_proyeccion['Año'] == 2018, 'Número de Negocios'].iloc[0]
    
    # Calcular el valor proyectado para 2019
    valor_2019_proyectado_ue = valor_2018_ue * tasa_anual_promedio_ue



# 🌟 PROYECCIÓN PO (Utiliza solo la Tasa IMSS de 2019) 🌟
if mostrar_personal:
    
    # 1. Obtener la tasa IMSS para el primer año de proyección (2019)
    # Tasas es la lista [1.0184, 0.9681, 1.0558, 1.0319]
    tasa_imss_2019 = tasas_imss['Tasas'][0] 

    # 2. Obtener el valor de Personal Ocupado de 2018 de la tabla proyectada
    valor_2018_po = df_proyeccion.loc[df_proyeccion['Año'] == 2018, 'Personal Ocupado'].iloc[0]
    
    # 3. Cálculo directo: Valor 2018 * Tasa IMSS
    valor_2019_proyectado_po = valor_2018_po * tasa_imss_2019

# --- AÑADIR FILA A LA TABLA ---
fila_2019 = {'Año': 2019}

if valor_2019_proyectado_ue is not None:
    fila_2019['Número de Negocios'] = valor_2019_proyectado_ue
    
if valor_2019_proyectado_po is not None:
    fila_2019['Personal Ocupado'] = valor_2019_proyectado_po
    
df_proyeccion.loc[len(df_proyeccion)] = fila_2019
#st.write(f"Tasa anual de crecimiento promedio calculada: {tasa_anual_promedio:.4f}")

# --- PROCESAMIENTO DE DATOS DE PROBABILIDADES ---

if mostrar_unidades:
    
    df_probabilidades = cargar_probabilidades()

        # Si el DataFrame de probabilidades está vacío, detenemos la ejecución
    if df_probabilidades.empty:
        st.stop()

        # --- Proyección de los años 2020, 2021 y 2022 UNIDADES ECONÓMICAS ---

        # Obtener el valor más reciente para la proyección (2019)
    # Preparamos el nombre del sector para el filtro
    sector_filtrado_prob = sector.upper().strip()
    if sector_filtrado_prob == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        sector_filtrado_prob = 'SERVICIOS PRIVADOS NO FINANCIEROS'

    # Bucle para proyectar los años 2020, 2021 y 2022
    proyecciones_futuras = {}
    
    for anio_futuro in range(2020, 2023):
            # Encontrar las tasas correspondientes en el DataFrame de probabilidades
            try:
                tasas = df_probabilidades[
                    (df_probabilidades['ENTIDAD'] == entidad.upper()) &
                    (df_probabilidades['SECTOR'] == sector_filtrado_prob) &
                    (df_probabilidades['TAMAÑO'] == personal_seleccionado) &
                    (df_probabilidades['AÑO'] == anio_futuro)
                ]

                if not tasas.empty:
                    tasa_supervivencia = tasas['SOBREVIVIENTES'].iloc[0]
                    tasa_nacimientos = tasas['NACIMIENTOS'].iloc[0]
                        
                    # Calcular el factor de crecimiento (supervivencia + nacimientos)
                    factor_crecimiento = tasa_supervivencia + tasa_nacimientos
                        
                    # Proyectar el valor del año anterior
                    valor_2019_ue = df_proyeccion.loc[df_proyeccion['Año'] == 2019, 'Número de Negocios'].iloc[0]
                    if anio_futuro == 2020:
                        proyected_value = valor_2019_ue * factor_crecimiento
                    elif anio_futuro == 2021:
                        proyected_value = valor_2019_ue * factor_crecimiento
                    else:
                        proyected_value = valor_2019_ue * factor_crecimiento

                    proyecciones_futuras[anio_futuro] = proyected_value
                    
                else:
                    st.warning(f"No se encontraron datos en 'PROBABILIDADES.csv' para {entidad}, {sector}, {personal_seleccionado} en el año {anio_futuro}.")
                    proyecciones_futuras[anio_futuro] = None
                    
            except IndexError:
                st.error(f"Error al obtener tasas para el año {anio_futuro}. Revisa que las columnas 'SOBREVIVIENTES' y 'NACIMIENTOS' existan y contengan valores válidos.")
                proyecciones_futuras[anio_futuro] = None

# Agregar PO si está seleccionado

if mostrar_personal:
    proyecciones_futuras_po = {}
    for anio in range(2020, 2023):                
        valor_2019_po = df_proyeccion.loc[df_proyeccion['Año'] == 2019, 'Personal Ocupado'].iloc[0]
        if anio == 2020:            
            tasa_imss_2020 = tasas_imss['Tasas'][1]
            valor_proyectado = valor_2019_po * tasa_imss_2020
        if anio == 2021:
            tasa_imss_2021 = tasas_imss['Tasas'][2]
            valor_proyectado = valor_proyectado * tasa_imss_2021
        if anio == 2022:
            tasa_imss_2022 = tasas_imss['Tasas'][3]
            valor_proyectado = valor_proyectado * tasa_imss_2022
        proyecciones_futuras_po[anio] = valor_proyectado

# Añadir filas 2020-2022 UE-PO

for anio in range(2020, 2023):    
    fila3anios = {'Año': anio}
    if mostrar_unidades:        
        fila3anios['Número de Negocios'] = proyecciones_futuras[anio]
    if mostrar_personal:        
        fila3anios['Personal Ocupado'] = proyecciones_futuras_po[anio]
    df_proyeccion.loc[len(df_proyeccion)] = fila3anios

# Añadir fila 2023

fila_2023 = {'Año': 2023}
if mostrar_unidades:
    fila_2023['Número de Negocios'] = tabla_pivote.loc[0, 'CE 2023 - UE']
if mostrar_personal:
    fila_2023['Personal Ocupado'] = tabla_pivote.loc[0, 'CE 2023 - PO']   
df_proyeccion.loc[len(df_proyeccion)] = fila_2023

    
if fenomeno_demografico == 'Población activa':

    st.markdown("---")
    st.subheader('Población Activa')
    st.markdown('---')
  

    # --- CÁLCULO DE TASAS DE CRECIMIENTO ANUAL ---
    # Tasa de crecimiento anual

    for i in range(1, len(df_proyeccion)):
        # Unidades Económicas
        if mostrar_unidades:
            ue_actual = df_proyeccion.loc[i, 'Número de Negocios']
            ue_anterior = df_proyeccion.loc[i - 1, 'Número de Negocios']
            if ue_anterior > 0:
                tasa_ue = ((ue_actual / ue_anterior) - 1) * 100
                df_proyeccion.loc[i, 'Tasa Crecimiento UE (%)'] = tasa_ue

        # Personal Ocupado
        if mostrar_personal:
            po_actual = df_proyeccion.loc[i, 'Personal Ocupado']
            po_anterior = df_proyeccion.loc[i - 1, 'Personal Ocupado']
            if po_anterior > 0:
                tasa_po = ((po_actual / po_anterior) - 1) * 100
                df_proyeccion.loc[i, 'Tasa Crecimiento PO (%)'] = tasa_po


    # Formatear las columnas a dos decimales con símbolo %
    if mostrar_unidades:
        df_proyeccion['Tasa Crecimiento UE (%)'] = df_proyeccion['Tasa Crecimiento UE (%)'].apply(
            lambda x: f"{x:,.2f}" if pd.notna(x) else None
        )
    if mostrar_personal:
        df_proyeccion['Tasa Crecimiento PO (%)'] = df_proyeccion['Tasa Crecimiento PO (%)'].apply(
            lambda x: f"{x:,.2f}" if pd.notna(x) else None
        )

    # --- VISUALIZACIÓN DE LA TABLA Y GRÁFICOS INTERACTIVOS ---

    df_proyeccion_formato = df_proyeccion.copy()
    
    
    if mostrar_unidades:
        df_proyeccion_formato.sort_values(by='Año', inplace=True)
        df_proyeccion_formato.drop_duplicates(subset='Año', keep='last', inplace=True)
        df_proyeccion_formato['Número de Negocios'] = round(df_proyeccion_formato['Número de Negocios'].astype(float),0)    
        df_proyeccion_formato['Número de Negocios'] = df_proyeccion_formato['Número de Negocios'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_formato.reset_index(drop=True, inplace=True)
    
    if mostrar_personal:
        df_proyeccion_formato.sort_values(by='Año', inplace=True)
        df_proyeccion_formato.drop_duplicates(subset='Año', keep='last', inplace=True)
        df_proyeccion_formato['Personal Ocupado'] = round(df_proyeccion_formato['Personal Ocupado'].astype(float),0)
        df_proyeccion_formato['Personal Ocupado'] = df_proyeccion_formato['Personal Ocupado'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_formato.reset_index(drop=True, inplace=True)

    col1, col2 = st.columns([40, 60])
    with col1:
        # Mostrar el DataFrame final con la nueva columna
        st.write(f"Comportamiento anual de población activa en {entidad.capitalize()}, pertenecientes al sector {sector.replace('TP', '').capitalize()} con {personal_seleccionado}")
        st.dataframe(df_proyeccion_formato, use_container_width=True, height=950)
        


    with col2:
    # --- VISUALIZACIÓN DE GRÁFICOS INTERACTIVOS CON PLOTLY ---
        st.write("Visualización de Comportamiento Anual")

        # 1. Gráfico de Número de Negocios
        columnas = []
        if mostrar_unidades:
            columnas.append('Número de Negocios')
        if mostrar_personal:
            columnas.append('Personal Ocupado')

        if columnas:
            fig_negocios = make_subplots(specs=[[{"secondary_y": True}]])
            for i, col in enumerate(columnas):
                es_secundario = i > 0  # La segunda métrica (si existe) va en el eje secundario
                color_trazado = '#08989C' if col == 'Número de Negocios' else '#003057'
                fig_negocios.add_trace(
                    go.Scatter(
                        x=df_proyeccion['Año'],
                        y=df_proyeccion[col],                        
                        name=col,
                        mode='lines+markers',
                        line=dict(color=color_trazado),
                        marker=dict(color=color_trazado),
                        hovertemplate='%{y:,.0f}<br>Año: %{x}'
                    ),
                    secondary_y=es_secundario
                )
            fig_negocios.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Comportamiento anual de población activa en la entidad de {entidad.title()}, pertenecientes al sector<br>{sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                    x=0.5,
                    xanchor='center',
                    y=-0.2,
                    yanchor='top',
                    orientation='h'
                ),
                xaxis_title = 'Año',
                margin={'t': 110}
            )
            if mostrar_unidades:
                fig_negocios.update_yaxes(title_text='<b>UNIDADES ECONÓMICAS</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>PERSONAL OCUPADO TOTAL</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_unidades and mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>UNIDADES ECONÓMICAS</b>', title_font=dict(size=13), secondary_y=False)
                fig_negocios.update_yaxes(title_text='<b>PERSONAL OCUPADO TOTAL</b>', title_font=dict(size=13), secondary_y=True)
            with st.container(border=True):
                st.plotly_chart(fig_negocios, use_container_width=True)
        
                    
        # 2. Gráfico de Tasas de Crecimiento   
        columnas = []
        if mostrar_unidades:
            columnas.append('Tasa Crecimiento UE (%)')
        if mostrar_personal:
            columnas.append('Tasa Crecimiento PO (%)')

        if columnas:
            fig_negocios_tasas = make_subplots()
            for i, col in enumerate(columnas):                
                color_trazado = '#08989C' if col == 'Tasa Crecimiento UE (%)' else '#003057'
                fig_negocios_tasas.add_trace(
                    go.Scatter(
                        x=df_proyeccion['Año'],
                        y=df_proyeccion[col],                        
                        name=col,
                        mode='lines+markers',
                        line=dict(color=color_trazado),
                        marker=dict(color=color_trazado),
                        hovertemplate='%{y:,.0f}<br>Año: %{x}'
                    )
                )
                      
        fig_negocios_tasas.update_layout(
            hovermode="x unified",
            title={
                'text': f"Tasa de crecimiento anual de población activa en la entidad de {entidad.title()}, pertenecientes al sector<br>{sector.title()}, con {personal_seleccionado.lower()}",
                'font': {'size': 14},
                'automargin': False
            },
            legend=dict(
                    x=0.5,
                    xanchor='center',
                    y=-0.2,
                    yanchor='top',
                    orientation='h'
                ),
            xaxis_title = 'Año',
            margin={'t': 110}
        )
        fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE CRECIMIENTO</b>', title_font=dict(size=13))    
        with st.container(border=True):
            st.plotly_chart(fig_negocios_tasas, use_container_width=True)
        st.markdown('<small>Fuente: Censos Económicos 1989-2024<small>', unsafe_allow_html=True)


#----NACIMIENTO DE UNIDADES ECONÓMICAS Y NACIMIENTO DE EMPLEOS ----

# Copiar tabla pivote
df_natalidad = tabla_pivote.copy()
df_natalidad.columns = [col.strip() for col in df_natalidad.columns]

# Extraer censos únicos en orden original
censos_unicos = []
for col in df_natalidad.columns:
    if col.startswith('CE'):
        censo = col.split(' - ')[0]
        if censo not in censos_unicos:
            censos_unicos.append(censo)

# Crear estructura para la nueva tabla
nueva_tabla = {'UE': {}, 'PO': {}}

# Aplicar lógica: fila 5 para primer censo, 10 para segundo, etc.
for i, censo in enumerate(censos_unicos):
    fila = (i + 1) * 5  # 5, 10, 15, 20...
    columnas_censo = [col for col in df_natalidad.columns if col.startswith(censo)]

    # Inicializar valores
    valor_ue = ''
    valor_po = ''

    for col in columnas_censo:
        if fila < len(df_natalidad):  # Validar que la fila exista
            if 'UE' in col.upper():
                valor_ue = df_natalidad.iloc[fila, df_natalidad.columns.get_loc(col)]
            elif 'PO' in col.upper():
                valor_po = df_natalidad.iloc[fila, df_natalidad.columns.get_loc(col)]

    nueva_tabla['UE'][censo] = valor_ue
    nueva_tabla['PO'][censo] = valor_po

# Convertir a DataFrame con censos como columnas
tabla_natalidad = pd.DataFrame(nueva_tabla).T


#Tabla Natalidad
#st.dataframe(tabla_natalidad, use_container_width=True)

# --- CÁLCULO Y VISUALIZACIÓN DEL CRECIMIENTO DINÁMICO ---
# Inicializar lista para resultados
filas = []
nombres_filas = []
etiquetas = []

# Función para calcular crecimiento porcentual entre censos
def calcular_crecimiento_natalidad(valores):
    resultados = []
    for i in range(1, len(valores)):
        anterior = valores[i - 1]
        actual = valores[i]
        if anterior and actual and anterior != '' and actual != '':
            anterior_num = float(str(anterior).replace(',', ''))
            actual_num = float(str(actual).replace(',', ''))
            if anterior_num > 0:
                crecimiento = ((actual_num) / anterior_num) ** 0.2
                resultados.append(crecimiento)
            else:
                resultados.append(None)
        else:
            resultados.append(None)
    return resultados

# Etiquetas para columnas (pares de censos)
etiquetas = [f"{tabla_natalidad.columns[i-1]}-{tabla_natalidad.columns[i]}" for i in range(1, len(tabla_natalidad.columns))]

# Calcular según selección
if mostrar_unidades:
    valores_ue = tabla_natalidad.loc['UE'].tolist()
    filas.append(calcular_crecimiento_natalidad(valores_ue))
    nombres_filas.append("Unidades Económicas")

if mostrar_personal:
    valores_po = tabla_natalidad.loc['PO'].tolist()
    filas.append(calcular_crecimiento_natalidad(valores_po))
    nombres_filas.append("Personal Ocupado")

# Mostrar tabla combinada
if filas:
    df_crecimiento_natalidad = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
    #st.dataframe(df_crecimiento_natalidad, use_container_width=True)
else:
    st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")


# --- PROYECCIÓN DE UNIDADES ECONÓMICAS Y PERSONAL OCUPADO ---
# Inicializar DataFrame con columnas dinámicas según selección
columnas = ['Año']
if mostrar_unidades:
    columnas += ('Número de Nacimientos','Tasa de Natalidad UE (%)','Tasa Crecimiento Anual de la Natalidad (%)')    
if mostrar_personal:
    columnas += ('Nacimiento de Empleos','Tasa de Natalidad PO (%)','Tasa Crecimiento Anual de Empleos (%)')    

df_proyeccion_nat = pd.DataFrame(columns=columnas)

# Iterar sobre los periodos censales
for i in range(len(df_crecimiento_natalidad.columns)):
    periodo = df_crecimiento_natalidad.columns[i]
    partes = periodo.split('-')

    anio_inicio_completo = partes[0].strip()
    anio_fin_completo = partes[1].strip()

    anio_inicio_str = anio_inicio_completo.replace('CE','')
    anio_fin_str = anio_fin_completo.replace('CE','')
    
    anio_inicio = int(anio_inicio_str)
    anio_fin = int(anio_fin_str)

    fila_inicial = {'Año': anio_inicio}
    etiqueta_columna = f'CE {anio_inicio}'

    if mostrar_unidades: 
        valor_actual_ue = float(tabla_natalidad.loc['UE',etiqueta_columna])
        tasa_ue = df_crecimiento_natalidad.loc['Unidades Económicas', periodo]
        fila_inicial['Número de Nacimientos'] = valor_actual_ue

    if mostrar_personal:
        valor_actual_po = float(tabla_natalidad.loc['PO',etiqueta_columna])
        tasa_po = df_crecimiento_natalidad.loc['Personal Ocupado', periodo]
        fila_inicial['Nacimiento de Empleos'] = valor_actual_po        
    
    df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila_inicial

    # Proyección intermedia
    for anio in range(anio_inicio + 1, anio_fin):
        if anio_fin > 2019:
            break  # No proyectar más allá de 2019
        fila = {'Año': anio}
        if mostrar_unidades:
            valor_actual_ue *= tasa_ue
            fila['Número de Nacimientos'] = valor_actual_ue
        if mostrar_personal:
            valor_actual_po *= tasa_po
            fila['Nacimiento de Empleos'] = valor_actual_po
        df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila
    
#TASAS IMSS
tasas_imss = {
    'Año': [2019, 2020, 2021, 2022],
    'Tasas': [1.0184,0.9681,1.0558,1.0319]
}

# --- CÁLCULO DE TASAS QUINQUENALES (Solo para UE, pero se ejecuta el bucle) ---

# 1. Inicializar variables de proyección ANTES de cualquier condicional

valor_2019_proyectado_ue = None
valor_2019_proyectado_po = None
if mostrar_unidades:
    tasas_quinquenales_ue = []
    
    # Este bucle solo es necesario para acumular tasas_quinquenales_ue
    for i in range(len(tabla_natalidad.columns) - 1): 
        censo_actual_str = tabla_natalidad.columns[i]
        censo_siguiente_str = tabla_natalidad.columns[i + 1]

        # Usamos try/except para el caso de etiquetas sin 'CE '
        try:
            anio_siguiente = int(censo_siguiente_str.replace('CE ', ''))
        except:
            anio_siguiente = 9999 

        if anio_siguiente > 2023:
            break

        # Acumulación de Tasas (Unidades Económicas)
        
        valor_actual_ue = float(tabla_natalidad.loc['UE', censo_actual_str])
        valor_siguiente_ue = float(tabla_natalidad.loc['UE', censo_siguiente_str])
        
        if valor_actual_ue > 0:
            tasa_quinquenal_ue = (valor_siguiente_ue / valor_actual_ue)
            tasas_quinquenales_ue.append(tasa_quinquenal_ue)


    # --- CÁLCULO DE PROMEDIOS Y PROYECCIÓN A 2019 (FUERA DEL BUCLE) ---

    # Proyección UE (Utiliza el promedio quinquenal de los censos)

    if tasas_quinquenales_ue:
        promedio_quinquenal_ue = sum(tasas_quinquenales_ue) / len(tasas_quinquenales_ue)
        tasa_anual_promedio_ue = promedio_quinquenal_ue**(1/6)
    else:
        tasa_anual_promedio_ue = 1 

    # Buscar el valor final proyectado de 2018
    valor_2018_ue = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 2018, 'Número de Nacimientos'].iloc[0]
    
    # Calcular el valor proyectado para 2019
    valor_2019_proyectado_ue = valor_2018_ue * tasa_anual_promedio_ue

# PROYECCIÓN PO (Utiliza solo la Tasa IMSS de 2019)
if mostrar_personal:
    
    # 1. Obtener la tasa IMSS para el primer año de proyección (2019)
    # Tasas es la lista [1.0184, 0.9681, 1.0558, 1.0319]
    tasa_imss_2019 = tasas_imss['Tasas'][0] 

    # 2. Obtener el valor de Personal Ocupado de 2018 de la tabla proyectada
    valor_2018_po = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 2018, 'Nacimiento de Empleos'].iloc[0]
    
    # 3. Cálculo directo: Valor 2018 * Tasa IMSS
    valor_2019_proyectado_po = valor_2018_po * tasa_imss_2019

# --- AÑADIR FILA A LA TABLA ---
fila_2019_nat = {'Año': 2019}

if valor_2019_proyectado_ue is not None:
    fila_2019_nat['Número de Nacimientos'] = valor_2019_proyectado_ue
    
if valor_2019_proyectado_po is not None:
    fila_2019_nat['Nacimiento de Empleos'] = valor_2019_proyectado_po
    
df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila_2019_nat
#st.write(f"Tasa anual de crecimiento promedio calculada: {tasa_anual_promedio:.4f}")

#----DATOS AÑOS 2020,2021,2022 NATALIDAD

if mostrar_unidades:
        
    df_probabilidades = cargar_probabilidades()

        # Si el DataFrame de probabilidades está vacío, detenemos la ejecución
    if df_probabilidades.empty:
        st.stop()

        # --- Proyección de los años 2020, 2021 y 2022 UNIDADES ECONÓMICAS ---

        # Obtener el valor más reciente para la proyección (2019)
    # Preparamos el nombre del sector para el filtro
    sector_filtrado_prob = sector.upper().strip()
    if sector_filtrado_prob == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        sector_filtrado_prob = 'SERVICIOS PRIVADOS NO FINANCIEROS'

    # Bucle para proyectar los años 2020, 2021 y 2022
    proyecciones_futuras = {}
    
    for anio_futuro in range(2020, 2023):
        # Encontrar las tasas correspondientes en el DataFrame de probabilidades
        try:
            tasas = df_probabilidades[
                (df_probabilidades['ENTIDAD'] == entidad.upper()) &
                (df_probabilidades['SECTOR'] == sector_filtrado_prob) &
                (df_probabilidades['TAMAÑO'] == personal_seleccionado) &
                (df_probabilidades['AÑO'] == anio_futuro)
            ]

            if not tasas.empty:
                tasa_supervivencia = tasas['SOBREVIVIENTES'].iloc[0]
                tasa_nacimientos = tasas['NACIMIENTOS'].iloc[0]
                    
                # Calcular el factor de crecimiento (supervivencia + nacimientos)
                factor_crecimiento = tasa_supervivencia + tasa_nacimientos
                    
                # Proyectar el valor del año anterior
                valor_2019_ue = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 2019, 'Número de Nacimientos'].iloc[0]
                
                if anio_futuro == 2020:
                    proyected_value = valor_2019_ue * factor_crecimiento
                if anio_futuro == 2021:
                    proyected_value = valor_2019_ue * factor_crecimiento
                if anio_futuro == 2022:
                    proyected_value = valor_2019_ue * factor_crecimiento

                proyecciones_futuras[anio_futuro] = proyected_value
                    

            else:
                st.warning(f"No se encontraron datos en 'PROBABILIDADES.csv' para {entidad}, {sector}, {personal_seleccionado} en el año {anio_futuro}.")
                proyecciones_futuras[anio_futuro] = None

        except IndexError:
            st.error(f"Error al obtener tasas para el año {anio_futuro}. Revisa que las columnas 'SOBREVIVIENTES' y 'NACIMIENTOS' existan y contengan valores válidos.")
            proyecciones_futuras[anio_futuro] = None
    
# Agregar PO si está seleccionado

if mostrar_personal:
    proyecciones_futuras_po = {}
    for anio in range(2020, 2023):                
        valor_2019_po = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 2019, 'Nacimiento de Empleos'].iloc[0]
        if anio == 2020:            
            tasa_imss_2020 = tasas_imss['Tasas'][1]
            valor_proyectado = valor_2019_po * tasa_imss_2020
        if anio == 2021:
            tasa_imss_2021 = tasas_imss['Tasas'][2]
            valor_proyectado = valor_proyectado * tasa_imss_2021
        if anio == 2022:
            tasa_imss_2022 = tasas_imss['Tasas'][3]
            valor_proyectado = valor_proyectado * tasa_imss_2022
        proyecciones_futuras_po[anio] = valor_proyectado

# Añadir filas 2020-2022 UE-PO

for anio in range(2020, 2023):    
    fila3anios = {'Año': anio}
    if mostrar_unidades:        
        fila3anios['Número de Nacimientos'] = proyecciones_futuras[anio]
    if mostrar_personal:        
        fila3anios['Nacimiento de Empleos'] = proyecciones_futuras_po[anio]
    df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila3anios

# Añadir fila 2023
fila_2023 = {'Año': 2023}
if mostrar_unidades:
    fila_2023['Número de Nacimientos'] = tabla_natalidad.loc['UE', 'CE 2023']
if mostrar_personal:
    fila_2023['Nacimiento de Empleos'] = tabla_natalidad.loc['PO', 'CE 2023']   
df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila_2023    

# Ordenar y limpiar
df_proyeccion_nat.sort_values(by='Año', inplace=True)
df_proyeccion_nat.drop_duplicates(subset='Año', keep='last', inplace=True)
df_proyeccion_nat.reset_index(drop=True, inplace=True)

# Formatear columnas
if mostrar_unidades and 'Número de Nacimientos' in df_proyeccion_nat.columns:
    df_proyeccion_nat['Número de Nacimientos'] = df_proyeccion_nat['Número de Nacimientos'].astype(float)
if mostrar_personal and 'Nacimiento de Empleos' in df_proyeccion_nat.columns:
    df_proyeccion_nat['Nacimiento de Empleos'] = df_proyeccion_nat['Nacimiento de Empleos'].astype(float)


# --- CÁLCULO DE TASAS DE NATALIDAD (%) ---    
# Asegurar que las columnas existan
if mostrar_unidades and 'Tasa de Natalidad UE (%)' not in df_proyeccion_nat.columns:
    df_proyeccion_nat['Tasa de Natalidad UE (%)'] = None
if mostrar_personal and 'Tasa de Natalidad PO (%)' not in df_proyeccion_nat.columns:
    df_proyeccion_nat['Tasa de Natalidad PO (%)'] = None

# Calcular tasas para cada año
for idx, row in df_proyeccion_nat.iterrows():
    anio = row['Año']

    # Buscar el número de negocios y personal ocupado en df_proyeccion
    if anio in df_proyeccion['Año'].values:
        datos_base = df_proyeccion[df_proyeccion['Año'] == anio].iloc[0]

        # Calcular tasa UE
        if mostrar_unidades and pd.notnull(row.get('Número de Nacimientos')) and 'Número de Negocios' in datos_base:
            numero_negocios = datos_base['Número de Negocios']
            if numero_negocios > 0:
                tasa_ue = (row['Número de Nacimientos'] / numero_negocios) * 100
                df_proyeccion_nat.at[idx, 'Tasa de Natalidad UE (%)'] = round(tasa_ue, 2)                    
    
        # Calcular tasa PO
        if mostrar_personal and pd.notnull(row.get('Nacimiento de Empleos')) and 'Personal Ocupado' in datos_base:
            personal_ocupado = datos_base['Personal Ocupado']
            if personal_ocupado > 0:
                tasa_po = (row['Nacimiento de Empleos'] / personal_ocupado) * 100
                df_proyeccion_nat.at[idx, 'Tasa de Natalidad PO (%)'] = round(tasa_po, 2)


if mostrar_unidades:
    tasanat1998 = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 1998, 'Tasa de Natalidad UE (%)'].iloc[0]
    tasanat1993 = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 1993, 'Tasa de Natalidad UE (%)'].iloc[0]    


#----DATOS AÑOS 2020,2021,2022 NATALIDAD 2a VEZ


# Copiar tabla pivote
df_natalidad = tabla_pivote.copy()
df_natalidad.columns = [col.strip() for col in df_natalidad.columns]

# Extraer censos únicos en orden original
censos_unicos = []
for col in df_natalidad.columns:
    if col.startswith('CE'):
        censo = col.split(' - ')[0]
        if censo not in censos_unicos:
            censos_unicos.append(censo)

# Crear estructura para la nueva tabla
nueva_tabla = {'UE': {}, 'PO': {}}

# Aplicar lógica: fila 5 para primer censo, 10 para segundo, etc.
for i, censo in enumerate(censos_unicos):
    fila = (i + 1) * 5  # 5, 10, 15, 20...
    columnas_censo = [col for col in df_natalidad.columns if col.startswith(censo)]

    # Inicializar valores
    valor_ue = ''
    valor_po = ''

    for col in columnas_censo:
        if fila < len(df_natalidad):  # Validar que la fila exista
            if 'UE' in col.upper():
                valor_ue = df_natalidad.iloc[fila, df_natalidad.columns.get_loc(col)]
            elif 'PO' in col.upper():
                valor_po = df_natalidad.iloc[fila, df_natalidad.columns.get_loc(col)]

    nueva_tabla['UE'][censo] = valor_ue
    nueva_tabla['PO'][censo] = valor_po

# Convertir a DataFrame con censos como columnas
tabla_natalidad = pd.DataFrame(nueva_tabla).T


#---TABLA NATALIDAD---
#st.dataframe(tabla_natalidad, use_container_width=True)

# --- CÁLCULO Y VISUALIZACIÓN DEL CRECIMIENTO DINÁMICO ---
# Inicializar lista para resultados
filas = []
nombres_filas = []
etiquetas = []

# Función para calcular crecimiento porcentual entre censos
def calcular_crecimiento_natalidad(valores):
    resultados = []
    for i in range(1, len(valores)):
        anterior = valores[i - 1]
        actual = valores[i]
        if anterior and actual and anterior != '' and actual != '':
            anterior_num = float(str(anterior).replace(',', ''))
            actual_num = float(str(actual).replace(',', ''))
            if anterior_num > 0:
                crecimiento = ((actual_num) / anterior_num) ** 0.2
                resultados.append(crecimiento)
            else:
                resultados.append(None)
        else:
            resultados.append(None)
    return resultados

# Etiquetas para columnas (pares de censos)
etiquetas = [f"{tabla_natalidad.columns[i-1]}-{tabla_natalidad.columns[i]}" for i in range(1, len(tabla_natalidad.columns))]

# Calcular según selección
if mostrar_unidades:
    valores_ue = tabla_natalidad.loc['UE'].tolist()
    filas.append(calcular_crecimiento_natalidad(valores_ue))
    nombres_filas.append("Unidades Económicas")

if mostrar_personal:
    valores_po = tabla_natalidad.loc['PO'].tolist()
    filas.append(calcular_crecimiento_natalidad(valores_po))
    nombres_filas.append("Personal Ocupado")

# Mostrar tabla combinada
if filas:
    df_crecimiento_natalidad = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
#   st.dataframe(df_crecimiento_natalidad, use_container_width=True)
else:
    st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")


# --- PROYECCIÓN DE UNIDADES ECONÓMICAS Y PERSONAL OCUPADO ---
# Inicializar DataFrame con columnas dinámicas según selección
columnas = ['Año']
if mostrar_unidades:
    columnas += ('Número de Nacimientos','Tasa de Natalidad UE (%)','Tasa Crecimiento Anual de la Natalidad (%)')    
if mostrar_personal:
    columnas += ('Nacimiento de Empleos','Tasa de Natalidad PO (%)','Tasa Crecimiento Anual de Empleos (%)')    

df_proyeccion_nat = pd.DataFrame(columns=columnas)

# Iterar sobre los periodos censales
for i in range(len(df_crecimiento_natalidad.columns)):
    periodo = df_crecimiento_natalidad.columns[i]
    partes = periodo.split('-')

    anio_inicio_completo = partes[0].strip()
    anio_fin_completo = partes[1].strip()

    anio_inicio_str = anio_inicio_completo.replace('CE','')
    anio_fin_str = anio_fin_completo.replace('CE','')
    
    anio_inicio = int(anio_inicio_str)
    anio_fin = int(anio_fin_str)

    fila_inicial = {'Año': anio_inicio}
    etiqueta_columna = f'CE {anio_inicio}'

    if mostrar_unidades: 
        valor_actual_ue = float(tabla_natalidad.loc['UE',etiqueta_columna])
        tasa_ue = df_crecimiento_natalidad.loc['Unidades Económicas', periodo]
        fila_inicial['Número de Nacimientos'] = valor_actual_ue

    if mostrar_personal:
        valor_actual_po = float(tabla_natalidad.loc['PO',etiqueta_columna])
        tasa_po = df_crecimiento_natalidad.loc['Personal Ocupado', periodo]
        fila_inicial['Nacimiento de Empleos'] = valor_actual_po        
    
    df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila_inicial

    # Proyección intermedia
    for anio in range(anio_inicio + 1, anio_fin):
        if anio_fin > 2019:
            break  # No proyectar más allá de 2019
        fila = {'Año': anio}
        if mostrar_unidades:
            valor_actual_ue *= tasa_ue
            fila['Número de Nacimientos'] = valor_actual_ue
        if mostrar_personal:
            valor_actual_po *= tasa_po
            fila['Nacimiento de Empleos'] = valor_actual_po
        df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila
    
#TASAS IMSS
tasas_imss = {
    'Año': [2019, 2020, 2021, 2022],
    'Tasas': [1.0184,0.9681,1.0558,1.0319]
}

# --- CÁLCULO DE TASAS QUINQUENALES (Solo para UE, pero se ejecuta el bucle) ---

# 1. Inicializar variables de proyección ANTES de cualquier condicional

valor_2019_proyectado_ue = None
valor_2019_proyectado_po = None
if mostrar_unidades:
    tasas_quinquenales_ue = []
    
    # Este bucle solo es necesario para acumular tasas_quinquenales_ue
    for i in range(len(tabla_natalidad.columns) - 1): 
        censo_actual_str = tabla_natalidad.columns[i]
        censo_siguiente_str = tabla_natalidad.columns[i + 1]

        # Usamos try/except para el caso de etiquetas sin 'CE '
        try:
            anio_siguiente = int(censo_siguiente_str.replace('CE ', ''))
        except:
            anio_siguiente = 9999 

        if anio_siguiente > 2023:
            break

        # Acumulación de Tasas (Unidades Económicas)
        
        valor_actual_ue = float(tabla_natalidad.loc['UE', censo_actual_str])
        valor_siguiente_ue = float(tabla_natalidad.loc['UE', censo_siguiente_str])
        
        if valor_actual_ue > 0:
            tasa_quinquenal_ue = (valor_siguiente_ue / valor_actual_ue)
            tasas_quinquenales_ue.append(tasa_quinquenal_ue)


    # --- CÁLCULO DE PROMEDIOS Y PROYECCIÓN A 2019 (FUERA DEL BUCLE) ---

    # Proyección UE (Utiliza el promedio quinquenal de los censos)

    if tasas_quinquenales_ue:
        promedio_quinquenal_ue = sum(tasas_quinquenales_ue) / len(tasas_quinquenales_ue)
        tasa_anual_promedio_ue = promedio_quinquenal_ue**(1/6)
    else:
        tasa_anual_promedio_ue = 1 

    # Buscar el valor final proyectado de 2018
    valor_2018_ue = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 2018, 'Número de Nacimientos'].iloc[0]
    
    # Calcular el valor proyectado para 2019
    valor_2019_proyectado_ue = valor_2018_ue * tasa_anual_promedio_ue

# PROYECCIÓN PO (Utiliza solo la Tasa IMSS de 2019)
if mostrar_personal:
    
    # 1. Obtener la tasa IMSS para el primer año de proyección (2019)
    # Tasas es la lista [1.0184, 0.9681, 1.0558, 1.0319]
    tasa_imss_2019 = tasas_imss['Tasas'][0] 

    # 2. Obtener el valor de Personal Ocupado de 2018 de la tabla proyectada
    valor_2018_po = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 2018, 'Nacimiento de Empleos'].iloc[0]
    
    # 3. Cálculo directo: Valor 2018 * Tasa IMSS
    valor_2019_proyectado_po = valor_2018_po * tasa_imss_2019

# --- AÑADIR FILA A LA TABLA ---
fila_2019_nat = {'Año': 2019}

if valor_2019_proyectado_ue is not None:
    fila_2019_nat['Número de Nacimientos'] = valor_2019_proyectado_ue
    
if valor_2019_proyectado_po is not None:
    fila_2019_nat['Nacimiento de Empleos'] = valor_2019_proyectado_po
    
df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila_2019_nat
#st.write(f"Tasa anual de crecimiento promedio calculada: {tasa_anual_promedio:.4f}")

#----DATOS AÑOS 2020,2021,2022 NATALIDAD

if mostrar_unidades:
        
    df_probabilidades = cargar_probabilidades()

        # Si el DataFrame de probabilidades está vacío, detenemos la ejecución
    if df_probabilidades.empty:
        st.stop()

        # --- Proyección de los años 2020, 2021 y 2022 UNIDADES ECONÓMICAS ---

        # Obtener el valor más reciente para la proyección (2019)
    # Preparamos el nombre del sector para el filtro
    sector_filtrado_prob = sector.upper().strip()
    if sector_filtrado_prob == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        sector_filtrado_prob = 'SERVICIOS PRIVADOS NO FINANCIEROS'

    # Bucle para proyectar los años 2020, 2021 y 2022
    proyecciones_futuras = {}
    
    for anio_futuro in range(2020, 2023):
        anio_anterior = anio_futuro - 1
        if anio_anterior < 2020:
            anio_anterior = 2020
        try:
            tasas = df_probabilidades[
                (df_probabilidades['ENTIDAD'] == entidad.upper()) &
                (df_probabilidades['SECTOR'] == sector_filtrado_prob) &
                (df_probabilidades['TAMAÑO'] == personal_seleccionado) &
                (df_probabilidades['AÑO'] == anio_futuro)                    
            ]
        
            tasas_anterior = df_probabilidades[
                (df_probabilidades['ENTIDAD'] == entidad.upper()) &
                (df_probabilidades['SECTOR'] == sector_filtrado_prob) &
                (df_probabilidades['TAMAÑO'] == personal_seleccionado) &
                (df_probabilidades['AÑO'] == anio_anterior)                    
            ]
                    
            if not tasas.empty and not tasas_anterior.empty:                    
                tasa_nacimientos_anterior = tasas_anterior['NACIMIENTOS'].iloc[0]
                tasa_nacimientos_actual = tasas['NACIMIENTOS'].iloc[0]
                    
                # Calcular el factor de crecimiento (supervivencia + nacimientos)
                factor_crecimiento = tasa_nacimientos_actual/tasa_nacimientos_anterior
                    
                # Proyectar el valor del año anterior
                valor_2019_ue = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 2019, 'Número de Nacimientos'].iloc[0]
                if anio_futuro == 2020:
                    proyected_value = valor_2019_ue * (tasanat1998/tasanat1993)
                if anio_futuro == 2021:
                    proyected_value = proyected_value * factor_crecimiento
                if anio_futuro == 2022:
                    proyected_value = proyected_value * factor_crecimiento

                proyecciones_futuras[anio_futuro] = proyected_value
                    

            else:
                st.warning(f"No se encontraron datos en 'PROBABILIDADES.csv' para {entidad}, {sector}, {personal_seleccionado} en el año {anio_futuro}.")
                proyecciones_futuras[anio_futuro] = None

        except IndexError:
            st.error(f"Error al obtener tasas para el año {anio_futuro}. Revisa que las columnas 'SOBREVIVIENTES' y 'NACIMIENTOS' existan y contengan valores válidos.")
            proyecciones_futuras[anio_futuro] = None
        
    
# Agregar PO si está seleccionado

if mostrar_personal:
    proyecciones_futuras_po = {}
    for anio in range(2020, 2023):                
        valor_2019_po = df_proyeccion_nat.loc[df_proyeccion_nat['Año'] == 2019, 'Nacimiento de Empleos'].iloc[0]
        if anio == 2020:            
            tasa_imss_2020 = tasas_imss['Tasas'][1]
            valor_proyectado = valor_2019_po * tasa_imss_2020
        if anio == 2021:
            tasa_imss_2021 = tasas_imss['Tasas'][2]
            valor_proyectado = valor_proyectado * tasa_imss_2021
        if anio == 2022:
            tasa_imss_2022 = tasas_imss['Tasas'][3]
            valor_proyectado = valor_proyectado * tasa_imss_2022
        proyecciones_futuras_po[anio] = valor_proyectado

# Añadir filas 2020-2022 UE-PO

for anio in range(2020, 2023):    
    fila3anios = {'Año': anio}
    if mostrar_unidades:        
        fila3anios['Número de Nacimientos'] = proyecciones_futuras[anio]
    if mostrar_personal:        
        fila3anios['Nacimiento de Empleos'] = proyecciones_futuras_po[anio]
    df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila3anios



# Añadir fila 2023

fila_2023 = {'Año': 2023}
if mostrar_unidades:
    fila_2023['Número de Nacimientos'] = tabla_natalidad.loc['UE', 'CE 2023']
if mostrar_personal:
    fila_2023['Nacimiento de Empleos'] = tabla_natalidad.loc['PO', 'CE 2023']   
df_proyeccion_nat.loc[len(df_proyeccion_nat)] = fila_2023    

# Ordenar y limpiar
df_proyeccion_nat.sort_values(by='Año', inplace=True)
df_proyeccion_nat.drop_duplicates(subset='Año', keep='last', inplace=True)
df_proyeccion_nat.reset_index(drop=True, inplace=True)

# Formatear columnas
if mostrar_unidades and 'Número de Nacimientos' in df_proyeccion_nat.columns:
    df_proyeccion_nat['Número de Nacimientos'] = df_proyeccion_nat['Número de Nacimientos'].astype(float)
if mostrar_personal and 'Nacimiento de Empleos' in df_proyeccion_nat.columns:
    df_proyeccion_nat['Nacimiento de Empleos'] = df_proyeccion_nat['Nacimiento de Empleos'].astype(float)


# --- CÁLCULO DE TASAS DE NATALIDAD (%) ---    
# Asegurar que las columnas existan
if mostrar_unidades and 'Tasa de Natalidad UE (%)' not in df_proyeccion_nat.columns:
    df_proyeccion_nat['Tasa de Natalidad UE (%)'] = None
if mostrar_personal and 'Tasa de Natalidad PO (%)' not in df_proyeccion_nat.columns:
    df_proyeccion_nat['Tasa de Natalidad PO (%)'] = None

# Calcular tasas para cada año
for idx, row in df_proyeccion_nat.iterrows():
    anio = row['Año']

    # Buscar el número de negocios y personal ocupado en df_proyeccion
    if anio in df_proyeccion['Año'].values:
        datos_base = df_proyeccion[df_proyeccion['Año'] == anio].iloc[0]

        # Calcular tasa UE
        if mostrar_unidades and pd.notnull(row.get('Número de Nacimientos')) and 'Número de Negocios' in datos_base:
            numero_negocios = datos_base['Número de Negocios']
            if numero_negocios > 0:
                tasa_ue = (row['Número de Nacimientos'] / numero_negocios) * 100
                df_proyeccion_nat.at[idx, 'Tasa de Natalidad UE (%)'] = round(tasa_ue, 2)                    
    
        # Calcular tasa PO
        if mostrar_personal and pd.notnull(row.get('Nacimiento de Empleos')) and 'Personal Ocupado' in datos_base:
            personal_ocupado = datos_base['Personal Ocupado']
            if personal_ocupado > 0:
                tasa_po = (row['Nacimiento de Empleos'] / personal_ocupado) * 100
                df_proyeccion_nat.at[idx, 'Tasa de Natalidad PO (%)'] = round(tasa_po, 2)

#st.dataframe(df_proyeccion_nat, use_container_width = True)

    # --- CÁLCULO DE TASAS DE CRECIMIENTO ANUAL DE LA NATALIDAD ---
# Tasa de crecimiento anual

if mostrar_unidades and 'Tasa Crecimiento Anual de la Natalidad (%)' not in df_proyeccion_nat.columns:
    df_proyeccion_nat['Tasa Crecimiento Anual de la Natalidad (%)'] = None
if mostrar_personal and 'Tasa Crecimiento Anual de Empleos (%)' not in df_proyeccion_nat.columns:
    df_proyeccion_nat['Tasa Crecimiento Anual de Empleos (%)'] = None

for i in range(1, len(df_proyeccion_nat)):        
    if mostrar_unidades:
        ue_actual = df_proyeccion_nat.loc[i, 'Número de Nacimientos']
        ue_anterior = df_proyeccion_nat.loc[i - 1, 'Número de Nacimientos']
        if ue_anterior > 0:
            tasa_ue = ((ue_actual / ue_anterior) - 1) * 100
            df_proyeccion_nat.loc[i, 'Tasa Crecimiento Anual de la Natalidad (%)'] = tasa_ue

    # Personal Ocupado
    if mostrar_personal:
        po_actual = df_proyeccion_nat.loc[i, 'Nacimiento de Empleos']
        po_anterior = df_proyeccion_nat.loc[i - 1, 'Nacimiento de Empleos']
        if po_anterior > 0:
            tasa_po = ((po_actual / po_anterior) - 1) * 100
            df_proyeccion_nat.loc[i, 'Tasa Crecimiento Anual de Empleos (%)'] = tasa_po


# Formatear las columnas a dos decimales con símbolo %
if mostrar_unidades:
    df_proyeccion_nat['Tasa de Natalidad UE (%)'] = df_proyeccion_nat['Tasa de Natalidad UE (%)'].apply(
        lambda x: f"{x:,.2f}" if pd.notna(x) else None
    )
    df_proyeccion_nat['Tasa Crecimiento Anual de la Natalidad (%)'] = df_proyeccion_nat['Tasa Crecimiento Anual de la Natalidad (%)'].apply(
        lambda x: f"{x:,.2f}" if pd.notna(x) else None
    )
if mostrar_personal:
    df_proyeccion_nat['Tasa de Natalidad PO (%)'] = df_proyeccion_nat['Tasa de Natalidad PO (%)'].apply(
        lambda x: f"{x:,.2f}" if pd.notna(x) else None
    )
    df_proyeccion_nat['Tasa Crecimiento Anual de Empleos (%)'] = df_proyeccion_nat['Tasa Crecimiento Anual de Empleos (%)'].apply(
        lambda x: f"{x:,.2f}" if pd.notna(x) else None
    )


#----VISUALIZACIÓN NATALIDAD---

if fenomeno_demografico == 'Natalidad':

    st.markdown("---")
    st.subheader("Natalidad")
    st.markdown('---')

    #Formato de valores
    df_proyeccion_nat_formato = df_proyeccion_nat.copy()
        
    if mostrar_unidades:
        df_proyeccion_nat_formato.sort_values(by='Año', inplace=True)
        df_proyeccion_nat_formato.drop_duplicates(subset='Año', keep='last', inplace=True)
        df_proyeccion_nat_formato['Número de Nacimientos'] = round(df_proyeccion_nat_formato['Número de Nacimientos'].astype(float),0)        
        df_proyeccion_nat_formato['Número de Nacimientos'] = df_proyeccion_nat_formato['Número de Nacimientos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_nat_formato.reset_index(drop=True, inplace=True)
    
    if mostrar_personal:
        df_proyeccion_nat_formato.sort_values(by='Año', inplace=True)
        df_proyeccion_nat_formato.drop_duplicates(subset='Año', keep='last', inplace=True)
        df_proyeccion_nat_formato['Nacimiento de Empleos'] = round(df_proyeccion_nat_formato['Nacimiento de Empleos'].astype(float),0)
        df_proyeccion_nat_formato['Nacimiento de Empleos'] = df_proyeccion_nat_formato['Nacimiento de Empleos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_nat_formato.reset_index(drop=True, inplace=True)

    #---Información en columnas y las gráficas
    col1, col2 = st.columns([40, 60])
    with col1:
        st.write(f"Comportamiento anual de Natalidad en {entidad.capitalize()}, pertenecientes al sector {sector.replace('TP', '').capitalize()} con {personal_seleccionado}")
        st.dataframe(df_proyeccion_nat_formato, use_container_width=False, height=1300)



    with col2:
    # --- VISUALIZACIÓN DE GRÁFICOS INTERACTIVOS CON PLOTLY ---
        st.write("Visualización de Comportamiento Anual")

        # 1. Gráfico de Número de Negocios
        columnas = []
        if mostrar_unidades:
            columnas.append('Número de Nacimientos')
        if mostrar_personal:
            columnas.append('Nacimiento de Empleos')

        if columnas:
            fig_negocios = make_subplots(specs=[[{"secondary_y": True}]])
            for i, col in enumerate(columnas):
                es_secundario = i > 0  # La segunda métrica (si existe) va en el eje secundario
                color_trazado = '#08989C' if col == 'Número de Nacimientos' else '#003057'
                fig_negocios.add_trace(
                    go.Scatter(
                        x=df_proyeccion_nat['Año'],
                        y=df_proyeccion_nat[col],                        
                        name=col,
                        mode='lines+markers',
                        line=dict(color=color_trazado),
                        marker=dict(color=color_trazado),
                        hovertemplate='%{y:,.0f}<br>Año: %{x}'
                    ),
                    secondary_y=es_secundario
                )
            fig_negocios.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Comportamiento anual de nacimientos en la entidad de {entidad.title()}, pertenecientes al sector<br>{sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                    x=0.5,
                    xanchor='center',
                    y=-0.2,
                    yanchor='top',
                    orientation='h'
                ),
                xaxis_title='Año',
                margin={'t': 110}
            )
            if mostrar_unidades:
                fig_negocios.update_yaxes(title_text='<b>NACIMIENTOS DE NEGOCIOS</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>NACIMIENTOS DE NEGOCIOS</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_unidades and mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>NACIMIENTOS DE NEGOCIOS</b>', title_font=dict(size=13), secondary_y=False)
                fig_negocios.update_yaxes(title_text='<b>NACIMIENTOS DE EMPLEOS</b>', title_font=dict(size=13), secondary_y=True)
            with st.container(border=True):
                st.plotly_chart(fig_negocios, use_container_width=True)
        
                    
        # 2. Gráfico de Tasas de Crecimiento   
        columnas = []
        if mostrar_unidades:
            columnas.append('Tasa de Natalidad UE (%)')
        if mostrar_personal:
            columnas.append('Tasa de Natalidad PO (%)')

        if columnas:
            fig_negocios_tasas = make_subplots()
            for i, col in enumerate(columnas):                
                color_trazado = '#08989C' if col == 'Tasa de Natalidad UE (%)' else '#003057'
                fig_negocios_tasas.add_trace(
                    go.Scatter(
                        x=df_proyeccion_nat['Año'],
                        y=df_proyeccion_nat[col],                        
                        name=col,
                        mode='lines+markers',
                        line=dict(color=color_trazado),
                        marker=dict(color=color_trazado),
                        hovertemplate='%{y:,.0f}<br>Año: %{x}'
                    )
                )
                      
        fig_negocios_tasas.update_layout(
            hovermode="x unified",
            title={
                'text': f"Tasa de natalidad en la entidad de {entidad.title()}, pertenecientes al sector<br>{sector.title()}, con {personal_seleccionado.lower()}",
                'font': {'size': 14},
                'automargin': False
            },
            legend=dict(
                    x=0.5,
                    xanchor='center',
                    y=-0.2,
                    yanchor='top',
                    orientation='h'
                ),
            xaxis_title='Año',
            margin={'t': 110}
        )
        fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE NATALIDAD</b>', title_font=dict(size=13))    
        with st.container(border=True):
            st.plotly_chart(fig_negocios_tasas, use_container_width=True)


        # 3. Gráfico de Tasas de Crecimiento
        columnas = []
        if mostrar_unidades:
            columnas.append('Tasa Crecimiento Anual de la Natalidad (%)')
        if mostrar_personal:
            columnas.append('Tasa Crecimiento Anual de Empleos (%)')

        if columnas:
            fig_negocios_tasas = make_subplots()
            for i, col in enumerate(columnas):                
                color_trazado = '#08989C' if col == 'Tasa Crecimiento Anual de la Natalidad (%)' else '#003057'
                fig_negocios_tasas.add_trace(
                    go.Scatter(
                        x=df_proyeccion_nat['Año'],
                        y=df_proyeccion_nat[col],                        
                        name=col,
                        mode='lines+markers',
                        line=dict(color=color_trazado),
                        marker=dict(color=color_trazado),
                        hovertemplate='%{y:,.0f}<br>Año: %{x}'
                    )
                )
                      
        fig_negocios_tasas.update_layout(
            hovermode="x unified",
            title={
                'text': f"Tasa de crecimiento de natalidad en la entidad de {entidad.title()}, pertenecientes al sector<br>{sector.title()}, con {personal_seleccionado.lower()}",
                'font': {'size': 14},
                'automargin': False
            },
            legend=dict(
                    x=0.5,
                    xanchor='center',
                    y=-0.2,
                    yanchor='top',
                    orientation='h'
                ),
            xaxis_title='Año',
            margin={'t': 110}
        )
        fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE CRECIMIENTO</b>', title_font=dict(size=13))    
        with st.container(border=True):
            st.plotly_chart(fig_negocios_tasas, use_container_width=True)
        st.markdown('<small>Fuente: Censos Económicos 1989-2024<small>', unsafe_allow_html=True)


#----SUPERVIVENCIA DE UNIDADES ECONÓMICAS Y SUPERVIVENCIA DE EMPLEOS ----

if fenomeno_demografico == 'Supervivencia':
    st.markdown("---")
    st.subheader("Supervivencia")
    st.markdown('---')
    
    rango_sprv = st.slider('Selecciona el rango de supervivencia:',min_value=5,max_value=25,value=5,step=5,width=600)

    # Copiar tabla pivote
    df_sprv = tabla_pivote.copy()
    df_sprv.columns = [col.strip() for col in df_sprv.columns]
    
    if rango_sprv == 5:

        # Extraer censos únicos en orden original
        censos_unicos = []
        for col in df_sprv.columns:
            if col.startswith('CE'):
                censo = col.split(' - ')[0]
                if int(censo.replace('CE ', '')) >= 1993 and censo not in censos_unicos:  # Filtrar censos desde 1993 en adelante                
                    censos_unicos.append(censo)
        
        # Crear estructura para la nueva tabla
        nueva_tabla = {'UE': {}, 'PO': {}}

        # Aplicar lógica: fila 5 para primer censo, 10 para segundo, etc.
        for i, censo in enumerate(censos_unicos):
            fila = (i + 1) * 5   # 5, 10, 15, 20...
            columnas_censo = [col for col in df_sprv.columns if col.startswith(censo)]

            # Inicializar valores
            valor_ue = ''
            valor_po = ''

            for col in columnas_censo:
                if fila < len(df_sprv):  # Validar que la fila exista
                    if 'UE' in col.upper():
                        valor_ue = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]
                    elif 'PO' in col.upper():
                        valor_po = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]

            nueva_tabla['UE'][censo] = valor_ue
            nueva_tabla['PO'][censo] = valor_po

        # Convertir a DataFrame con censos como columnas
        tabla_sprv5 = pd.DataFrame(nueva_tabla).T
        
        #st.dataframe(tabla_sprv5, use_container_width=True)   #Ocultar tabla de supervivencia

        #Calcular crecimiento
        filas = []
        nombres_filas = []
        etiquetas = []

        # Función para calcular crecimiento porcentual entre censos
        def calcular_crecimiento_natalidad(valores):
            resultados = []
            for i in range(1, len(valores)):
                anterior = valores[i - 1]
                actual = valores[i]
                if anterior and actual and anterior != '' and actual != '':
                    anterior_num = float(str(anterior).replace(',', ''))
                    actual_num = float(str(actual).replace(',', ''))
                    if anterior_num > 0:
                        crecimiento = ((actual_num) / anterior_num) ** 0.2
                        resultados.append(crecimiento)
                    else:
                        resultados.append(None)
                else:
                    resultados.append(None)
            return resultados

        # Etiquetas para columnas (pares de censos)
        etiquetas = [f"{tabla_sprv5.columns[i-1]}-{tabla_sprv5.columns[i]}" for i in range(1, len(tabla_sprv5.columns))]

        # Calcular según selección
        if mostrar_unidades:
            valores_ue = tabla_sprv5.loc['UE'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_ue))
            nombres_filas.append("Unidades Económicas")

        if mostrar_personal:
            valores_po = tabla_sprv5.loc['PO'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_po))
            nombres_filas.append("Personal Ocupado")

        # Mostrar tabla combinada
        if filas:
            df_crecimiento_sprv5 = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
            #st.dataframe(df_crecimiento_sprv5, use_container_width=True)
        else:
            st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")


        columnas = ['Año (t)']
        if mostrar_unidades:
            columnas += ('Número de Nacimientos','Supervivientes después de 5 años UE','Probabilidad de Supervivencia UE (%)', 'Tasa de Crecimiento Anual de la Supervivencia UE (%)')    
        if mostrar_personal:
            columnas += ('Nacimiento de Empleos','Supervivientes después de 5 años PO','Probabilidad de Supervivencia PO', 'Tasa de Crecimiento Anual de la Supervivencia PO (%)')    

        df_proyeccion_sprv5 = pd.DataFrame(columns=columnas)

        # Iterar sobre los periodos censales
        for i in range(len(df_crecimiento_sprv5.columns)):
            periodo = df_crecimiento_sprv5.columns[i]
            partes = periodo.split('-')

            anio_inicio_completo = partes[0].strip()
            anio_fin_completo = partes[1].strip()

            anio_inicio_str = anio_inicio_completo.replace('CE','')
            anio_fin_str = anio_fin_completo.replace('CE','')
            
            anio_inicio = int(anio_inicio_str)
            anio_fin = int(anio_fin_str)

            fila_inicial = {'Año (t)': anio_inicio}
            etiqueta_columna = f'CE {anio_inicio}'

            if mostrar_unidades: 
                valor_actual_ue = float(tabla_sprv5.loc['UE',etiqueta_columna])
                tasa_ue = df_crecimiento_sprv5.loc['Unidades Económicas', periodo]
                fila_inicial['Supervivientes después de 5 años UE'] = valor_actual_ue

            if mostrar_personal:
                valor_actual_po = float(tabla_sprv5.loc['PO',etiqueta_columna])
                tasa_po = df_crecimiento_sprv5.loc['Personal Ocupado', periodo]
                fila_inicial['Supervivientes después de 5 años PO'] = valor_actual_po        
            
            df_proyeccion_sprv5.loc[len(df_proyeccion_sprv5)] = fila_inicial

            # Proyección intermedia
            for anio in range(anio_inicio + 1, anio_fin):
                if anio_fin > 2019:
                    break  # No proyectar más allá de 2019
                fila = {'Año (t)': anio}
                if mostrar_unidades:
                    valor_actual_ue *= tasa_ue
                    fila['Supervivientes después de 5 años UE'] = valor_actual_ue
                if mostrar_personal:
                    valor_actual_po *= tasa_po
                    fila['Supervivientes después de 5 años PO'] = valor_actual_po
                df_proyeccion_sprv5.loc[len(df_proyeccion_sprv5)] = fila

        
       
        # --- CÁLCULO DE TASAS QUINQUENALES (Solo para UE, pero se ejecuta el bucle) ---

        # 1. Inicializar variables de proyección ANTES de cualquier condicional

        valor_2019_proyectado_ue = None
        valor_2019_proyectado_po = None
        
        if mostrar_unidades:
            tasas_quinquenales_ue = []
            
            # Este bucle solo es necesario para acumular tasas_quinquenales_ue
            for i in range(len(tabla_sprv5.columns) - 1): 
                censo_actual_str = tabla_sprv5.columns[i]
                censo_siguiente_str = tabla_sprv5.columns[i + 1]

                # Usamos try/except para el caso de etiquetas sin 'CE '
                try:
                    anio_siguiente = int(censo_siguiente_str.replace('CE ', ''))
                except:
                    anio_siguiente = 9999 

                if anio_siguiente > 2023:
                    break

                # Acumulación de Tasas (Unidades Económicas)
                
                valor_actual_ue = float(tabla_sprv5.loc['UE', censo_actual_str])
                valor_siguiente_ue = float(tabla_sprv5.loc['UE', censo_siguiente_str])
                
                if valor_actual_ue > 0:
                    tasa_quinquenal_ue = (valor_siguiente_ue / valor_actual_ue)
                    tasas_quinquenales_ue.append(tasa_quinquenal_ue)
            
            

            # --- CÁLCULO DE PROMEDIOS Y PROYECCIÓN A 2019 (FUERA DEL BUCLE) ---

            # Proyección UE (Utiliza el promedio quinquenal de los censos)
            
            if tasas_quinquenales_ue:
                promedio_quinquenal_ue = sum(tasas_quinquenales_ue) / len(tasas_quinquenales_ue)
                tasa_anual_promedio_ue = promedio_quinquenal_ue**(1/5)
            else:
                tasa_anual_promedio_ue = 1
            
            # Valores a la tabla 2019-2022 UE            
            valor_actual_ue = df_proyeccion_sprv5.loc[df_proyeccion_sprv5['Año (t)'] == 2018, 'Supervivientes después de 5 años UE'].iloc[0]            
            proyecciones_ue = {}
            for anio in range(2019, 2023):
                proyecciones_ue[anio] = None
                valor_actual_ue *= tasa_anual_promedio_ue
                proyecciones_ue[anio] = valor_actual_ue
        
        if mostrar_personal:
            valor_actual_po = df_proyeccion_sprv5.loc[df_proyeccion_sprv5['Año (t)'] == 2018, 'Supervivientes después de 5 años PO'].iloc[0]
            proyecciones_po = {}
            for anio in range(2019, 2023):
                proyecciones_po[anio] = None
                tasa_imss_anio = tasas_imss['Tasas'][anio - 2019]  # Ajuste para obtener la tasa correcta
                valor_actual_po *= tasa_imss_anio
                proyecciones_po[anio] = valor_actual_po
        
        # Añadir filas 2019-2022 UE-PO
        for anio in range (2019, 2023):    
            fila3anios = {'Año (t)': anio}
            if mostrar_unidades:        
                fila3anios['Supervivientes después de 5 años UE'] = proyecciones_ue[anio]
            if mostrar_personal:        
                fila3anios['Supervivientes después de 5 años PO'] = proyecciones_po[anio]
            df_proyeccion_sprv5.loc[len(df_proyeccion_sprv5)] = fila3anios

        # Añadir fila 2023

        fila_2023 = {'Año (t)': 2023}
        if mostrar_unidades:
            fila_2023['Supervivientes después de 5 años UE'] = tabla_sprv5.loc['UE', 'CE 2023']
        if mostrar_personal:
            fila_2023['Supervivientes después de 5 años PO'] = tabla_sprv5.loc['PO', 'CE 2023']   
        df_proyeccion_sprv5.loc[len(df_proyeccion_sprv5)] = fila_2023    

        
        # Columna Número de Nacimientos y Nacimiento de Empleos desde df_proyeccion_nat
        if mostrar_unidades:
            df_proyeccion_sprv5['Número de Nacimientos'] = df_proyeccion_nat['Número de Nacimientos']
        
        if mostrar_personal:
            df_proyeccion_sprv5['Nacimiento de Empleos'] = df_proyeccion_nat['Nacimiento de Empleos']
        
        # Calculo de probabilidades
        for anio in range(len(df_proyeccion_sprv5)):
            if mostrar_unidades:
                supervivientes_ue = df_proyeccion_sprv5.loc[anio, 'Supervivientes después de 5 años UE']
                valor_inicial_ue = df_proyeccion_sprv5.loc[anio, 'Número de Nacimientos']
                if valor_inicial_ue and valor_inicial_ue != '' and supervivientes_ue and supervivientes_ue != '':
                    probabilidad_ue = supervivientes_ue / valor_inicial_ue
                    if probabilidad_ue > 1:
                        probabilidad_ue = 1
                    else:
                        pass
                    df_proyeccion_sprv5.loc[anio, 'Probabilidad de Supervivencia UE (%)'] = round(probabilidad_ue, 4)
                    

            if mostrar_personal:
                supervivientes_po = df_proyeccion_sprv5.loc[anio, 'Supervivientes después de 5 años PO']
                valor_inicial_po = df_proyeccion_sprv5.loc[anio, 'Nacimiento de Empleos']
                if valor_inicial_po and valor_inicial_po != '' and supervivientes_po and supervivientes_po != '':
                    probabilidad_po = supervivientes_po / valor_inicial_po
                    if probabilidad_po > 1:
                        probabilidad_po = 1
                    else:
                        pass
                    df_proyeccion_sprv5.loc[anio, 'Probabilidad de Supervivencia PO'] = round(probabilidad_po, 4)
        
        # Calculo de tasa de crecimiento anual de la supervivencia
        for i in range(1, len(df_proyeccion_sprv5)):        
            if mostrar_unidades:
                supervivientes_actual_ue = df_proyeccion_sprv5.loc[i, 'Supervivientes después de 5 años UE']
                supervivientes_anterior_ue = df_proyeccion_sprv5.loc[i - 1, 'Supervivientes después de 5 años UE']
                if supervivientes_anterior_ue and supervivientes_anterior_ue != 0:
                    tasa_ue = ((supervivientes_actual_ue / supervivientes_anterior_ue) - 1) * 100
                    df_proyeccion_sprv5.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia UE (%)'] = round(tasa_ue, 2)

            if mostrar_personal:
                supervivientes_actual_po = df_proyeccion_sprv5.loc[i, 'Supervivientes después de 5 años PO']
                supervivientes_anterior_po = df_proyeccion_sprv5.loc[i - 1, 'Supervivientes después de 5 años PO']
                if supervivientes_anterior_po and supervivientes_anterior_po != 0:
                    tasa_po = ((supervivientes_actual_po / supervivientes_anterior_po) - 1) * 100
                    df_proyeccion_sprv5.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia PO (%)'] = round(tasa_po, 2)
                    
         # Añadir columna Año(-t)
        df_proyeccion_sprv5['Año(-t)'] = df_proyeccion_sprv5['Año (t)'] - 5
       
       # Reordenar columnas para que Año(-t) sea la primera y Año (t) la tercera
        cols = df_proyeccion_sprv5.columns.tolist()
        
        if 'Año(-t)' in cols and 'Año (t)' in cols:
            
            cols.remove('Año(-t)')
            cols.remove('Año (t)')
                            
            cols.insert(0, 'Año(-t)')
            cols.insert(2, 'Año (t)')
                    
        if mostrar_unidades and mostrar_personal:
            if 'Año(-t)' in cols and 'Año (t)' in cols:
                
                cols.remove('Año(-t)')
                cols.remove('Año (t)')
                cols.remove('Nacimiento de Empleos')
                    
                cols.insert(0, 'Año(-t)')
                cols.insert(2, 'Año (t)')
                cols.insert(2, 'Nacimiento de Empleos')

            # Reordenar el DataFrame
        df_proyeccion_sprv5 = df_proyeccion_sprv5[cols]

        # --- Visualización de tabla y gráficos interactivos ---

        df_proyeccion_sprv5_formato = df_proyeccion_sprv5.copy()
        
        if mostrar_unidades:
            df_proyeccion_sprv5_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv5_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv5_formato['Número de Nacimientos'] = round(df_proyeccion_sprv5_formato['Número de Nacimientos'].astype(float),0)
            df_proyeccion_sprv5_formato['Número de Nacimientos'] = df_proyeccion_sprv5_formato['Número de Nacimientos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv5_formato['Supervivientes después de 5 años UE'] = round(df_proyeccion_sprv5_formato['Supervivientes después de 5 años UE'].astype(float),0)
            df_proyeccion_sprv5_formato['Supervivientes después de 5 años UE'] = df_proyeccion_sprv5_formato['Supervivientes después de 5 años UE'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv5_formato.reset_index(drop=True, inplace=True)

        if mostrar_personal:
            df_proyeccion_sprv5_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv5_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv5_formato['Nacimiento de Empleos'] = round(df_proyeccion_sprv5_formato['Nacimiento de Empleos'].astype(float),0)        
            df_proyeccion_sprv5_formato['Nacimiento de Empleos'] = df_proyeccion_sprv5_formato['Nacimiento de Empleos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv5_formato['Supervivientes después de 5 años PO'] = round(df_proyeccion_sprv5_formato['Supervivientes después de 5 años PO'].astype(float),0)
            df_proyeccion_sprv5_formato['Supervivientes después de 5 años PO'] = df_proyeccion_sprv5_formato['Supervivientes después de 5 años PO'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv5_formato.reset_index(drop=True, inplace=True)

        col1, col2 = st.columns([40, 60])
        with col1:
            # Mostrar el DataFrame final con la nueva columna
            st.write(f"Supervivientes 5 años después de haber nacido en {entidad.capitalize()}, pertenecientes al sector {sector.capitalize()} con {personal_seleccionado}")
            st.dataframe(df_proyeccion_sprv5_formato, use_container_width=True, height=1140)

        with col2:
            st.write("Visualización de Comportamiento Anual")

            # 1. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Supervivientes después de 5 años UE')
            if mostrar_personal:
                columnas.append('Supervivientes después de 5 años PO')

            if columnas:
                fig_negocios = make_subplots(specs=[[{"secondary_y": True}]])
                for i, col in enumerate(columnas):
                    es_secundario = i > 0  # La segunda métrica (si existe) va en el eje secundario
                    color_trazado = '#08989C' if col == 'Supervivientes después de 5 años UE' else '#003057'
                    fig_negocios.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv5['Año (t)'],
                            y=df_proyeccion_sprv5[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.0f}<br>Año: %{x}'
                        ),
                        secondary_y=es_secundario
                    )
                fig_negocios.update_layout(
                    hovermode="x unified",
                    title={
                        'text': f"Número de unidades económicas supervivientes al año t, nacidas 5 años antes en la entidad de<br>{entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                        'font': {'size': 14},
                        'automargin': False
                    },
                    legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                    xaxis_title = 'Año (t)',
                    margin={'t': 110}
                )
            if mostrar_unidades:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_unidades and mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=True)
            with st.container(border=True):
                st.plotly_chart(fig_negocios, use_container_width=True)
                    

            # 2. Gráfico               
            columnas = []
            if mostrar_unidades:
                columnas.append('Probabilidad de Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Probabilidad de Supervivencia PO')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Probabilidad de Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv5['Año (t)'],
                            y=df_proyeccion_sprv5[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.4f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Probabilidad de superviviencia al año t de las unidades económicas que nacieron 5 años antes en la entidad de<br>{entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>PROBABILIDAD</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)
         
                     
            # 3. Gráfico    
            columnas = []
            if mostrar_unidades:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia PO (%)')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Tasa de Crecimiento Anual de la Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv5['Año (t)'],
                            y=df_proyeccion_sprv5[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.2f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Tasa de crecimiento anual de la supervivencia al año t de las unidades económicas que nacieron 5 año antes en<br>la entidad de {entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE CRECIMIENTO</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)            
          
            st.markdown('<small>Fuente: Censos Económicos 1989-2024<small>', unsafe_allow_html=True) 
    
    
    if rango_sprv == 10:
         # Extraer censos únicos en orden original
        censos_unicos = []
        for col in df_sprv.columns:
            if col.startswith('CE'):
                censo = col.split(' - ')[0]
                if int(censo.replace('CE ', '')) >= 1998 and censo not in censos_unicos:  # Filtrar censos desde 1998 en adelante                
                    censos_unicos.append(censo)
        
        # Crear estructura para la nueva tabla
        nueva_tabla = {'UE': {}, 'PO': {}}

        # Aplicar lógica: fila 5 para primer censo, 10 para segundo, etc.
        for i, censo in enumerate(censos_unicos):
            fila = (i + 1) * 5   # 5, 10, 15, 20...
            columnas_censo = [col for col in df_sprv.columns if col.startswith(censo)]

            # Inicializar valores
            valor_ue = ''
            valor_po = ''

            for col in columnas_censo:
                if fila < len(df_sprv):  # Validar que la fila exista
                    if 'UE' in col.upper():
                        valor_ue = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]
                    elif 'PO' in col.upper():
                        valor_po = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]

            nueva_tabla['UE'][censo] = valor_ue
            nueva_tabla['PO'][censo] = valor_po

        # Convertir a DataFrame con censos como columnas
        tabla_sprv10 = pd.DataFrame(nueva_tabla).T
        
        #st.dataframe(tabla_sprv10, use_container_width=True)

        #Calcular crecimiento
        filas = []
        nombres_filas = []
        etiquetas = []

        # Función para calcular crecimiento porcentual entre censos
        def calcular_crecimiento_natalidad(valores):
            resultados = []
            for i in range(1, len(valores)):
                anterior = valores[i - 1]
                actual = valores[i]
                if anterior and actual and anterior != '' and actual != '':
                    anterior_num = float(str(anterior).replace(',', ''))
                    actual_num = float(str(actual).replace(',', ''))
                    if anterior_num > 0:
                        crecimiento = ((actual_num) / anterior_num) ** 0.2
                        resultados.append(crecimiento)
                    else:
                        resultados.append(None)
                else:
                    resultados.append(None)
            return resultados

        # Etiquetas para columnas (pares de censos)
        etiquetas = [f"{tabla_sprv10.columns[i-1]}-{tabla_sprv10.columns[i]}" for i in range(1, len(tabla_sprv10.columns))]

        # Calcular según selección
        if mostrar_unidades:
            valores_ue = tabla_sprv10.loc['UE'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_ue))
            nombres_filas.append("Unidades Económicas")

        if mostrar_personal:
            valores_po = tabla_sprv10.loc['PO'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_po))
            nombres_filas.append("Personal Ocupado")

        # Mostrar tabla combinada
        if filas:
            df_crecimiento_sprv10 = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
            #st.dataframe(df_crecimiento_sprv10, use_container_width=True)
        else:
            st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")


        columnas = ['Año (t)']
        if mostrar_unidades:
            columnas += ('Número de Nacimientos','Supervivientes después de 10 años UE','Probabilidad de Supervivencia UE (%)', 'Tasa de Crecimiento Anual de la Supervivencia UE (%)')    
        if mostrar_personal:
            columnas += ('Nacimiento de Empleos','Supervivientes después de 10 años PO','Probabilidad de Supervivencia PO', 'Tasa de Crecimiento Anual de la Supervivencia PO (%)')    

        df_proyeccion_sprv10 = pd.DataFrame(columns=columnas)

        # Iterar sobre los periodos censales
        for i in range(len(df_crecimiento_sprv10.columns)):
            periodo = df_crecimiento_sprv10.columns[i]
            partes = periodo.split('-')

            anio_inicio_completo = partes[0].strip()
            anio_fin_completo = partes[1].strip()

            anio_inicio_str = anio_inicio_completo.replace('CE','')
            anio_fin_str = anio_fin_completo.replace('CE','')
            
            anio_inicio = int(anio_inicio_str)
            anio_fin = int(anio_fin_str)

            fila_inicial = {'Año (t)': anio_inicio}
            etiqueta_columna = f'CE {anio_inicio}'

            if mostrar_unidades: 
                valor_actual_ue = float(tabla_sprv10.loc['UE',etiqueta_columna])
                tasa_ue = df_crecimiento_sprv10.loc['Unidades Económicas', periodo]
                fila_inicial['Supervivientes después de 10 años UE'] = valor_actual_ue

            if mostrar_personal:
                valor_actual_po = float(tabla_sprv10.loc['PO',etiqueta_columna])
                tasa_po = df_crecimiento_sprv10.loc['Personal Ocupado', periodo]
                fila_inicial['Supervivientes después de 10 años PO'] = valor_actual_po        
            
            df_proyeccion_sprv10.loc[len(df_proyeccion_sprv10)] = fila_inicial

            # Proyección intermedia
            for anio in range(anio_inicio + 1, anio_fin):
                if anio_fin > 2019:
                    break  # No proyectar más allá de 2019
                fila = {'Año (t)': anio}
                if mostrar_unidades:
                    valor_actual_ue *= tasa_ue
                    fila['Supervivientes después de 10 años UE'] = valor_actual_ue
                if mostrar_personal:
                    valor_actual_po *= tasa_po
                    fila['Supervivientes después de 10 años PO'] = valor_actual_po
                df_proyeccion_sprv10.loc[len(df_proyeccion_sprv10)] = fila
 
       
        # --- CÁLCULO DE TASAS QUINQUENALES (Solo para UE, pero se ejecuta el bucle) ---

        # 1. Inicializar variables de proyección ANTES de cualquier condicional

        valor_2019_proyectado_ue = None
        valor_2019_proyectado_po = None
        
        if mostrar_unidades:
            tasas_quinquenales_ue = []
            
            # Este bucle solo es necesario para acumular tasas_quinquenales_ue
            for i in range(len(tabla_sprv10.columns) - 1): 
                censo_actual_str = tabla_sprv10.columns[i]
                censo_siguiente_str = tabla_sprv10.columns[i + 1]

                # Usamos try/except para el caso de etiquetas sin 'CE '
                try:
                    anio_siguiente = int(censo_siguiente_str.replace('CE ', ''))
                except:
                    anio_siguiente = 9999 

                if anio_siguiente > 2023:
                    break

                # Acumulación de Tasas (Unidades Económicas)
                
                valor_actual_ue = float(tabla_sprv10.loc['UE', censo_actual_str])
                valor_siguiente_ue = float(tabla_sprv10.loc['UE', censo_siguiente_str])
                
                if valor_actual_ue > 0:
                    tasa_quinquenal_ue = (valor_siguiente_ue / valor_actual_ue)
                    tasas_quinquenales_ue.append(tasa_quinquenal_ue)
            
            

            # --- CÁLCULO DE PROMEDIOS Y PROYECCIÓN A 2019 (FUERA DEL BUCLE) ---

            # Proyección UE (Utiliza el promedio quinquenal de los censos)
            
            if tasas_quinquenales_ue:
                promedio_quinquenal_ue = sum(tasas_quinquenales_ue) / len(tasas_quinquenales_ue)
                tasa_anual_promedio_ue = promedio_quinquenal_ue**(1/5)
            else:
                tasa_anual_promedio_ue = 1
            #st.write('Tasa_anual_promedio_ue:', tasa_anual_promedio_ue)
           
            # Valores a la tabla 2019-2022 UE            
            valor_actual_ue = df_proyeccion_sprv10.loc[df_proyeccion_sprv10['Año (t)'] == 2018, 'Supervivientes después de 10 años UE'].iloc[0]            
            proyecciones_ue = {}
            for anio in range(2019, 2023):
                proyecciones_ue[anio] = None
                valor_actual_ue *= tasa_anual_promedio_ue
                proyecciones_ue[anio] = valor_actual_ue
        
        if mostrar_personal:
            valor_actual_po = df_proyeccion_sprv10.loc[df_proyeccion_sprv10['Año (t)'] == 2018, 'Supervivientes después de 10 años PO'].iloc[0]
            proyecciones_po = {}
            for anio in range(2019, 2023):
                proyecciones_po[anio] = None
                tasa_imss_anio = tasas_imss['Tasas'][anio - 2019]  # Ajuste para obtener la tasa correcta
                valor_actual_po *= tasa_imss_anio
                proyecciones_po[anio] = valor_actual_po
        
        # Añadir filas 2019-2022 UE-PO
        for anio in range (2019, 2023):    
            fila3anios = {'Año (t)': anio}
            if mostrar_unidades:        
                fila3anios['Supervivientes después de 10 años UE'] = proyecciones_ue[anio]
            if mostrar_personal:        
                fila3anios['Supervivientes después de 10 años PO'] = proyecciones_po[anio]
            df_proyeccion_sprv10.loc[len(df_proyeccion_sprv10)] = fila3anios

        # Añadir fila 2023

        fila_2023 = {'Año (t)': 2023}
        if mostrar_unidades:
            fila_2023['Supervivientes después de 10 años UE'] = tabla_sprv10.loc['UE', 'CE 2023']
        if mostrar_personal:
            fila_2023['Supervivientes después de 10 años PO'] = tabla_sprv10.loc['PO', 'CE 2023']   
        df_proyeccion_sprv10.loc[len(df_proyeccion_sprv10)] = fila_2023    

        
        # Columna Número de Nacimientos y Nacimiento de Empleos desde df_proyeccion_nat
        if mostrar_unidades:
            df_proyeccion_sprv10['Número de Nacimientos'] = df_proyeccion_nat['Número de Nacimientos']
        
        if mostrar_personal:
            df_proyeccion_sprv10['Nacimiento de Empleos'] = df_proyeccion_nat['Nacimiento de Empleos']
        
        # Calculo de probabilidades
        for anio in range(len(df_proyeccion_sprv10)):
            if mostrar_unidades:
                supervivientes_ue = df_proyeccion_sprv10.loc[anio, 'Supervivientes después de 10 años UE']
                valor_inicial_ue = df_proyeccion_sprv10.loc[anio, 'Número de Nacimientos']
                if valor_inicial_ue and valor_inicial_ue != '' and supervivientes_ue and supervivientes_ue != '':
                    probabilidad_ue = supervivientes_ue / valor_inicial_ue
                    if probabilidad_ue > 1:
                        probabilidad_ue = 1
                    else:
                        pass
                    df_proyeccion_sprv10.loc[anio, 'Probabilidad de Supervivencia UE (%)'] = round(probabilidad_ue, 4)
                    

            if mostrar_personal:
                supervivientes_po = df_proyeccion_sprv10.loc[anio, 'Supervivientes después de 10 años PO']
                valor_inicial_po = df_proyeccion_sprv10.loc[anio, 'Nacimiento de Empleos']
                if valor_inicial_po and valor_inicial_po != '' and supervivientes_po and supervivientes_po != '':
                    probabilidad_po = supervivientes_po / valor_inicial_po
                    if probabilidad_po > 1:
                        probabilidad_po = 1
                    else:
                        pass
                    df_proyeccion_sprv10.loc[anio, 'Probabilidad de Supervivencia PO'] = round(probabilidad_po, 4)
        
        # Calculo de tasa de crecimiento anual de la supervivencia
        for i in range(1, len(df_proyeccion_sprv10)):        
            if mostrar_unidades:
                supervivientes_actual_ue = df_proyeccion_sprv10.loc[i, 'Supervivientes después de 10 años UE']
                supervivientes_anterior_ue = df_proyeccion_sprv10.loc[i - 1, 'Supervivientes después de 10 años UE']
                if supervivientes_anterior_ue and supervivientes_anterior_ue != 0:
                    tasa_ue = ((supervivientes_actual_ue / supervivientes_anterior_ue) - 1) * 100
                    df_proyeccion_sprv10.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia UE (%)'] = round(tasa_ue, 2)

            if mostrar_personal:
                supervivientes_actual_po = df_proyeccion_sprv10.loc[i, 'Supervivientes después de 10 años PO']
                supervivientes_anterior_po = df_proyeccion_sprv10.loc[i - 1, 'Supervivientes después de 10 años PO']
                if supervivientes_anterior_po and supervivientes_anterior_po != 0:
                    tasa_po = ((supervivientes_actual_po / supervivientes_anterior_po) - 1) * 100
                    df_proyeccion_sprv10.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia PO (%)'] = round(tasa_po, 2)
                    
         # Añadir columna Año(-t)
        df_proyeccion_sprv10['Año(-t)'] = df_proyeccion_sprv10['Año (t)'] - 10
       
       # Reordenar columnas para que Año(-t) sea la primera y Año (t) la tercera
        cols = df_proyeccion_sprv10.columns.tolist()
        
        if 'Año(-t)' in cols and 'Año (t)' in cols:
            
            cols.remove('Año(-t)')
            cols.remove('Año (t)')
            
                
            cols.insert(0, 'Año(-t)')
            cols.insert(2, 'Año (t)')
            
        
        if mostrar_unidades and mostrar_personal:
            if 'Año(-t)' in cols and 'Año (t)' in cols:
                
                cols.remove('Año(-t)')
                cols.remove('Año (t)')
                cols.remove('Nacimiento de Empleos')
                    
                cols.insert(0, 'Año(-t)')
                cols.insert(2, 'Año (t)')
                cols.insert(2, 'Nacimiento de Empleos')

            # Reordenar el DataFrame
        df_proyeccion_sprv10 = df_proyeccion_sprv10[cols]

        # --- Visualización de tabla y gráficos interactivos ---

        df_proyeccion_sprv10_formato = df_proyeccion_sprv10.copy()
        
        if mostrar_unidades:
            df_proyeccion_sprv10_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv10_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv10_formato['Número de Nacimientos'] = round(df_proyeccion_sprv10_formato['Número de Nacimientos'].astype(float),0)
            df_proyeccion_sprv10_formato['Número de Nacimientos'] = df_proyeccion_sprv10_formato['Número de Nacimientos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv10_formato['Supervivientes después de 10 años UE'] = round(df_proyeccion_sprv10_formato['Supervivientes después de 10 años UE'].astype(float),0)
            df_proyeccion_sprv10_formato['Supervivientes después de 10 años UE'] = df_proyeccion_sprv10_formato['Supervivientes después de 10 años UE'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv10_formato.reset_index(drop=True, inplace=True)

        if mostrar_personal:
            df_proyeccion_sprv10_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv10_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv10_formato['Nacimiento de Empleos'] = round(df_proyeccion_sprv10_formato['Nacimiento de Empleos'].astype(float),0)        
            df_proyeccion_sprv10_formato['Nacimiento de Empleos'] = df_proyeccion_sprv10_formato['Nacimiento de Empleos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv10_formato['Supervivientes después de 10 años PO'] = round(df_proyeccion_sprv10_formato['Supervivientes después de 10 años PO'].astype(float),0)
            df_proyeccion_sprv10_formato['Supervivientes después de 10 años PO'] = df_proyeccion_sprv10_formato['Supervivientes después de 10 años PO'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv10_formato.reset_index(drop=True, inplace=True)

        col1, col2 = st.columns([40, 60])
        with col1:
            # Mostrar el DataFrame final con la nueva columna
            st.write(f"Supervivientes 10 años después de haber nacido en {entidad.capitalize()}, pertenecientes al sector {sector.capitalize()} con {personal_seleccionado}")
            st.dataframe(df_proyeccion_sprv10_formato, use_container_width=True, height=950)

        with col2:
            st.write("Visualización de Comportamiento Anual")

            
            # 1. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Supervivientes después de 10 años UE')
            if mostrar_personal:
                columnas.append('Supervivientes después de 10 años PO')

            if columnas:
                fig_negocios = make_subplots(specs=[[{"secondary_y": True}]])
                for i, col in enumerate(columnas):
                    es_secundario = i > 0  # La segunda métrica (si existe) va en el eje secundario
                    color_trazado = '#08989C' if col == 'Supervivientes después de 10 años UE' else '#003057'
                    fig_negocios.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv10['Año (t)'],
                            y=df_proyeccion_sprv10[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.0f}<br>Año: %{x}'
                        ),
                        secondary_y=es_secundario
                    )
                fig_negocios.update_layout(
                    hovermode="x unified",
                    title={
                        'text': f"Número de unidades económicas supervivientes al año t, nacidas 10 años antes<br>en la entidad de {entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                        'font': {'size': 14},
                        'automargin': False
                    },
                    legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                    xaxis_title = 'Año (t)',
                    margin={'t': 110}
                )
            if mostrar_unidades:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_unidades and mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=True)
            with st.container(border=True):
                st.plotly_chart(fig_negocios, use_container_width=True)


            # 2. Gráfico 
            columnas = []
            if mostrar_unidades:
                columnas.append('Probabilidad de Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Probabilidad de Supervivencia PO')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Probabilidad de Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv10['Año (t)'],
                            y=df_proyeccion_sprv10[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.4f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Probabilidad de superviviencia al año t de las unidades económicas que nacieron 10 años antes en la entidad de<br>{entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>PROBABILIDAD</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)  
            

            # 3. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia PO (%)')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Tasa de Crecimiento Anual de la Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv10['Año (t)'],
                            y=df_proyeccion_sprv10[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.2f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Tasa de crecimiento anual de la supervivencia al año t de las unidades económicas que nacieron 10 año antes en<br>la entidad de {entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE CRECIMIENTO</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)            
          
            st.markdown('<small>Fuente: Censos Económicos 1989-2024<small>', unsafe_allow_html=True) 
    

    
    if rango_sprv == 15:
         # Extraer censos únicos en orden original
        censos_unicos = []
        for col in df_sprv.columns:
            if col.startswith('CE'):
                censo = col.split(' - ')[0]
                if int(censo.replace('CE ', '')) >= 2003 and censo not in censos_unicos:  # Filtrar censos desde 2003 en adelante                
                    censos_unicos.append(censo)
        
        # Crear estructura para la nueva tabla
        nueva_tabla = {'UE': {}, 'PO': {}}

        # Aplicar lógica: fila 5 para primer censo, 10 para segundo, etc.
        for i, censo in enumerate(censos_unicos):
            fila = (i + 1) * 5   # 5, 10, 15, 20...
            columnas_censo = [col for col in df_sprv.columns if col.startswith(censo)]

            # Inicializar valores
            valor_ue = ''
            valor_po = ''

            for col in columnas_censo:
                if fila < len(df_sprv):  # Validar que la fila exista
                    if 'UE' in col.upper():
                        valor_ue = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]
                    elif 'PO' in col.upper():
                        valor_po = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]

            nueva_tabla['UE'][censo] = valor_ue
            nueva_tabla['PO'][censo] = valor_po

        # Convertir a DataFrame con censos como columnas
        tabla_sprv15 = pd.DataFrame(nueva_tabla).T
        
        #st.dataframe(tabla_sprv15, use_container_width=True)

        #Calcular crecimiento
        filas = []
        nombres_filas = []
        etiquetas = []

        # Función para calcular crecimiento porcentual entre censos
        def calcular_crecimiento_natalidad(valores):
            resultados = []
            for i in range(1, len(valores)):
                anterior = valores[i - 1]
                actual = valores[i]
                if anterior and actual and anterior != '' and actual != '':
                    anterior_num = float(str(anterior).replace(',', ''))
                    actual_num = float(str(actual).replace(',', ''))
                    if anterior_num > 0:
                        crecimiento = ((actual_num) / anterior_num) ** 0.2
                        resultados.append(crecimiento)
                    else:
                        resultados.append(None)
                else:
                    resultados.append(None)
            return resultados

        # Etiquetas para columnas (pares de censos)
        etiquetas = [f"{tabla_sprv15.columns[i-1]}-{tabla_sprv15.columns[i]}" for i in range(1, len(tabla_sprv15.columns))]

        # Calcular según selección
        if mostrar_unidades:
            valores_ue = tabla_sprv15.loc['UE'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_ue))
            nombres_filas.append("Unidades Económicas")

        if mostrar_personal:
            valores_po = tabla_sprv15.loc['PO'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_po))
            nombres_filas.append("Personal Ocupado")

        # Mostrar tabla combinada
        if filas:
            df_crecimiento_sprv15 = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
            #st.dataframe(df_crecimiento_sprv15, use_container_width=True)
        else:
            st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")


        columnas = ['Año (t)']
        if mostrar_unidades:
            columnas += ('Número de Nacimientos','Supervivientes después de 15 años UE','Probabilidad de Supervivencia UE (%)', 'Tasa de Crecimiento Anual de la Supervivencia UE (%)')    
        if mostrar_personal:
            columnas += ('Nacimiento de Empleos','Supervivientes después de 15 años PO','Probabilidad de Supervivencia PO', 'Tasa de Crecimiento Anual de la Supervivencia PO (%)')    

        df_proyeccion_sprv15 = pd.DataFrame(columns=columnas)

        # Iterar sobre los periodos censales
        for i in range(len(df_crecimiento_sprv15.columns)):
            periodo = df_crecimiento_sprv15.columns[i]
            partes = periodo.split('-')

            anio_inicio_completo = partes[0].strip()
            anio_fin_completo = partes[1].strip()

            anio_inicio_str = anio_inicio_completo.replace('CE','')
            anio_fin_str = anio_fin_completo.replace('CE','')
            
            anio_inicio = int(anio_inicio_str)
            anio_fin = int(anio_fin_str)

            fila_inicial = {'Año (t)': anio_inicio}
            etiqueta_columna = f'CE {anio_inicio}'

            if mostrar_unidades: 
                valor_actual_ue = float(tabla_sprv15.loc['UE',etiqueta_columna])
                tasa_ue = df_crecimiento_sprv15.loc['Unidades Económicas', periodo]
                fila_inicial['Supervivientes después de 15 años UE'] = valor_actual_ue

            if mostrar_personal:
                valor_actual_po = float(tabla_sprv15.loc['PO',etiqueta_columna])
                tasa_po = df_crecimiento_sprv15.loc['Personal Ocupado', periodo]
                fila_inicial['Supervivientes después de 15 años PO'] = valor_actual_po        
            
            df_proyeccion_sprv15.loc[len(df_proyeccion_sprv15)] = fila_inicial

            # Proyección intermedia
            for anio in range(anio_inicio + 1, anio_fin):
                if anio_fin > 2019:
                    break  # No proyectar más allá de 2019
                fila = {'Año (t)': anio}
                if mostrar_unidades:
                    valor_actual_ue *= tasa_ue
                    fila['Supervivientes después de 15 años UE'] = valor_actual_ue
                if mostrar_personal:
                    valor_actual_po *= tasa_po
                    fila['Supervivientes después de 15 años PO'] = valor_actual_po
                df_proyeccion_sprv15.loc[len(df_proyeccion_sprv15)] = fila
 
       
        # --- CÁLCULO DE TASAS QUINQUENALES (Solo para UE, pero se ejecuta el bucle) ---

        # 1. Inicializar variables de proyección ANTES de cualquier condicional

        valor_2019_proyectado_ue = None
        valor_2019_proyectado_po = None
        
        if mostrar_unidades:
            tasas_quinquenales_ue = []
            
            # Este bucle solo es necesario para acumular tasas_quinquenales_ue
            for i in range(len(tabla_sprv15.columns) - 1): 
                censo_actual_str = tabla_sprv15.columns[i]
                censo_siguiente_str = tabla_sprv15.columns[i + 1]

                # Usamos try/except para el caso de etiquetas sin 'CE '
                try:
                    anio_siguiente = int(censo_siguiente_str.replace('CE ', ''))
                except:
                    anio_siguiente = 9999 

                if anio_siguiente > 2023:
                    break

                # Acumulación de Tasas (Unidades Económicas)
                
                valor_actual_ue = float(tabla_sprv15.loc['UE', censo_actual_str])
                valor_siguiente_ue = float(tabla_sprv15.loc['UE', censo_siguiente_str])
                
                if valor_actual_ue > 0:
                    tasa_quinquenal_ue = (valor_siguiente_ue / valor_actual_ue)
                    tasas_quinquenales_ue.append(tasa_quinquenal_ue)
            
            

            # --- CÁLCULO DE PROMEDIOS Y PROYECCIÓN A 2019 (FUERA DEL BUCLE) ---

            # Proyección UE (Utiliza el promedio quinquenal de los censos)
            
            if tasas_quinquenales_ue:
                promedio_quinquenal_ue = sum(tasas_quinquenales_ue) / len(tasas_quinquenales_ue)
                tasa_anual_promedio_ue = promedio_quinquenal_ue**(1/5)
            else:
                tasa_anual_promedio_ue = 1
            #st.write('Tasa_anual_promedio_ue:', tasa_anual_promedio_ue)
            # Valores a la tabla 2019-2022 UE            
            valor_actual_ue = df_proyeccion_sprv15.loc[df_proyeccion_sprv15['Año (t)'] == 2018, 'Supervivientes después de 15 años UE'].iloc[0]            
            proyecciones_ue = {}
            for anio in range(2019, 2023):
                proyecciones_ue[anio] = None
                valor_actual_ue *= tasa_anual_promedio_ue
                proyecciones_ue[anio] = valor_actual_ue
        
        if mostrar_personal:
            valor_actual_po = df_proyeccion_sprv15.loc[df_proyeccion_sprv15['Año (t)'] == 2018, 'Supervivientes después de 15 años PO'].iloc[0]
            proyecciones_po = {}
            for anio in range(2019, 2023):
                proyecciones_po[anio] = None
                tasa_imss_anio = tasas_imss['Tasas'][anio - 2019]  # Ajuste para obtener la tasa correcta
                valor_actual_po *= tasa_imss_anio
                proyecciones_po[anio] = valor_actual_po
        
        # Añadir filas 2019-2022 UE-PO
        for anio in range (2019, 2023):    
            fila3anios = {'Año (t)': anio}
            if mostrar_unidades:        
                fila3anios['Supervivientes después de 15 años UE'] = proyecciones_ue[anio]
            if mostrar_personal:        
                fila3anios['Supervivientes después de 15 años PO'] = proyecciones_po[anio]
            df_proyeccion_sprv15.loc[len(df_proyeccion_sprv15)] = fila3anios

        # Añadir fila 2023

        fila_2023 = {'Año (t)': 2023}
        if mostrar_unidades:
            fila_2023['Supervivientes después de 15 años UE'] = tabla_sprv15.loc['UE', 'CE 2023']
        if mostrar_personal:
            fila_2023['Supervivientes después de 15 años PO'] = tabla_sprv15.loc['PO', 'CE 2023']   
        df_proyeccion_sprv15.loc[len(df_proyeccion_sprv15)] = fila_2023    

        
        # Columna Número de Nacimientos y Nacimiento de Empleos desde df_proyeccion_nat
        if mostrar_unidades:
            df_proyeccion_sprv15['Número de Nacimientos'] = df_proyeccion_nat['Número de Nacimientos']
        
        if mostrar_personal:
            df_proyeccion_sprv15['Nacimiento de Empleos'] = df_proyeccion_nat['Nacimiento de Empleos']
        
        # Calculo de probabilidades
        for anio in range(len(df_proyeccion_sprv15)):
            if mostrar_unidades:
                supervivientes_ue = df_proyeccion_sprv15.loc[anio, 'Supervivientes después de 15 años UE']
                valor_inicial_ue = df_proyeccion_sprv15.loc[anio, 'Número de Nacimientos']
                if valor_inicial_ue and valor_inicial_ue != '' and supervivientes_ue and supervivientes_ue != '':
                    probabilidad_ue = supervivientes_ue / valor_inicial_ue
                    if probabilidad_ue > 1:
                        probabilidad_ue = 1
                    else:
                        pass
                    df_proyeccion_sprv15.loc[anio, 'Probabilidad de Supervivencia UE (%)'] = round(probabilidad_ue, 4)
                    

            if mostrar_personal:
                supervivientes_po = df_proyeccion_sprv15.loc[anio, 'Supervivientes después de 15 años PO']
                valor_inicial_po = df_proyeccion_sprv15.loc[anio, 'Nacimiento de Empleos']
                if valor_inicial_po and valor_inicial_po != '' and supervivientes_po and supervivientes_po != '':
                    probabilidad_po = supervivientes_po / valor_inicial_po
                    if probabilidad_po > 1:
                        probabilidad_po = 1
                    else:
                        pass
                    df_proyeccion_sprv15.loc[anio, 'Probabilidad de Supervivencia PO'] = round(probabilidad_po, 4)
        
        # Calculo de tasa de crecimiento anual de la supervivencia
        for i in range(1, len(df_proyeccion_sprv15)):        
            if mostrar_unidades:
                supervivientes_actual_ue = df_proyeccion_sprv15.loc[i, 'Supervivientes después de 15 años UE']
                supervivientes_anterior_ue = df_proyeccion_sprv15.loc[i - 1, 'Supervivientes después de 15 años UE']
                if supervivientes_anterior_ue and supervivientes_anterior_ue != 0:
                    tasa_ue = ((supervivientes_actual_ue / supervivientes_anterior_ue) - 1) * 100
                    df_proyeccion_sprv15.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia UE (%)'] = round(tasa_ue, 2)

            if mostrar_personal:
                supervivientes_actual_po = df_proyeccion_sprv15.loc[i, 'Supervivientes después de 15 años PO']
                supervivientes_anterior_po = df_proyeccion_sprv15.loc[i - 1, 'Supervivientes después de 15 años PO']
                if supervivientes_anterior_po and supervivientes_anterior_po != 0:
                    tasa_po = ((supervivientes_actual_po / supervivientes_anterior_po) - 1) * 100
                    df_proyeccion_sprv15.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia PO (%)'] = round(tasa_po, 2)
                    
         # Añadir columna Año(-t)
        df_proyeccion_sprv15['Año(-t)'] = df_proyeccion_sprv15['Año (t)'] - 15
       
       # Reordenar columnas para que Año(-t) sea la primera y Año (t) la tercera
        cols = df_proyeccion_sprv15.columns.tolist()
        
        if 'Año(-t)' in cols and 'Año (t)' in cols:
            
            cols.remove('Año(-t)')
            cols.remove('Año (t)')
            
                
            cols.insert(0, 'Año(-t)')
            cols.insert(2, 'Año (t)')
            
        
        if mostrar_unidades and mostrar_personal:
            if 'Año(-t)' in cols and 'Año (t)' in cols:
                
                cols.remove('Año(-t)')
                cols.remove('Año (t)')
                cols.remove('Nacimiento de Empleos')
                    
                cols.insert(0, 'Año(-t)')
                cols.insert(2, 'Año (t)')
                cols.insert(2, 'Nacimiento de Empleos')

            # Reordenar el DataFrame
        df_proyeccion_sprv15 = df_proyeccion_sprv15[cols]

        # --- Visualización de tabla y gráficos interactivos ---

        df_proyeccion_sprv15_formato = df_proyeccion_sprv15.copy()
        
        if mostrar_unidades:
            df_proyeccion_sprv15_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv15_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv15_formato['Número de Nacimientos'] = round(df_proyeccion_sprv15_formato['Número de Nacimientos'].astype(float),0)
            df_proyeccion_sprv15_formato['Número de Nacimientos'] = df_proyeccion_sprv15_formato['Número de Nacimientos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv15_formato['Supervivientes después de 15 años UE'] = round(df_proyeccion_sprv15_formato['Supervivientes después de 15 años UE'].astype(float),0)
            df_proyeccion_sprv15_formato['Supervivientes después de 15 años UE'] = df_proyeccion_sprv15_formato['Supervivientes después de 15 años UE'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv15_formato.reset_index(drop=True, inplace=True)

        if mostrar_personal:
            df_proyeccion_sprv15_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv15_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv15_formato['Nacimiento de Empleos'] = round(df_proyeccion_sprv15_formato['Nacimiento de Empleos'].astype(float),0)        
            df_proyeccion_sprv15_formato['Nacimiento de Empleos'] = df_proyeccion_sprv15_formato['Nacimiento de Empleos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv15_formato['Supervivientes después de 15 años PO'] = round(df_proyeccion_sprv15_formato['Supervivientes después de 15 años PO'].astype(float),0)
            df_proyeccion_sprv15_formato['Supervivientes después de 15 años PO'] = df_proyeccion_sprv15_formato['Supervivientes después de 15 años PO'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv15_formato.reset_index(drop=True, inplace=True)

        col1, col2 = st.columns([40, 60])
        with col1:
            # Mostrar el DataFrame final con la nueva columna
            st.write(f"Supervivientes 15 años después de haber nacido en {entidad.capitalize()}, pertenecientes al sector {sector.capitalize()} con {personal_seleccionado}")
            st.dataframe(df_proyeccion_sprv15_formato, use_container_width=True, height=780)

        with col2:
            st.write("Visualización de Comportamiento Anual")

            # 1. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Supervivientes después de 15 años UE')
            if mostrar_personal:
                columnas.append('Supervivientes después de 15 años PO')

            if columnas:
                fig_negocios = make_subplots(specs=[[{"secondary_y": True}]])
                for i, col in enumerate(columnas):
                    es_secundario = i > 0  # La segunda métrica (si existe) va en el eje secundario
                    color_trazado = '#08989C' if col == 'Supervivientes después de 15 años UE' else '#003057'
                    fig_negocios.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv15['Año (t)'],
                            y=df_proyeccion_sprv15[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.0f}<br>Año: %{x}'
                        ),
                        secondary_y=es_secundario
                    )
                fig_negocios.update_layout(
                    hovermode="x unified",
                    title={
                        'text': f"Número de unidades económicas supervivientes al año t, nacidas 15 años antes en la entidad de<br>{entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                        'font': {'size': 14},
                        'automargin': False
                    },
                    legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                    xaxis_title = 'Año (t)',
                    margin={'t': 110}
                )
            if mostrar_unidades:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_unidades and mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=True)
            with st.container(border=True):
                st.plotly_chart(fig_negocios, use_container_width=True)


            # 2. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Probabilidad de Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Probabilidad de Supervivencia PO')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Probabilidad de Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv15['Año (t)'],
                            y=df_proyeccion_sprv15[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.4f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Probabilidad de superviviencia al año t de las unidades económicas que nacieron 15 años antes en la entidad de<br>{entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>PROBABILIDAD</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)  
            

            # 3. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia PO (%)')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Tasa de Crecimiento Anual de la Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv15['Año (t)'],
                            y=df_proyeccion_sprv15[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.2f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Tasa de crecimiento anual de la supervivencia al año t de las unidades económicas que nacieron 15 años antes en<br>la entidad de {entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE CRECIMIENTO</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)            
          
            st.markdown('<small>Fuente: Censos Económicos 1989-2024<small>', unsafe_allow_html=True) 

    
    if rango_sprv == 20:
         # Extraer censos únicos en orden original
        censos_unicos = []
        for col in df_sprv.columns:
            if col.startswith('CE'):
                censo = col.split(' - ')[0]
                if int(censo.replace('CE ', '')) >= 2008 and censo not in censos_unicos:  # Filtrar censos desde 2008 en adelante                
                    censos_unicos.append(censo)
        
        # Crear estructura para la nueva tabla
        nueva_tabla = {'UE': {}, 'PO': {}}

        # Aplicar lógica: fila 5 para primer censo, 10 para segundo, etc.
        for i, censo in enumerate(censos_unicos):
            fila = (i + 1) * 5   # 5, 10, 15, 20...
            columnas_censo = [col for col in df_sprv.columns if col.startswith(censo)]

            # Inicializar valores
            valor_ue = ''
            valor_po = ''

            for col in columnas_censo:
                if fila < len(df_sprv):  # Validar que la fila exista
                    if 'UE' in col.upper():
                        valor_ue = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]
                    elif 'PO' in col.upper():
                        valor_po = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]

            nueva_tabla['UE'][censo] = valor_ue
            nueva_tabla['PO'][censo] = valor_po

        # Convertir a DataFrame con censos como columnas
        tabla_sprv20 = pd.DataFrame(nueva_tabla).T
        
        #st.dataframe(tabla_sprv20, use_container_width=True)

        #Calcular crecimiento
        filas = []
        nombres_filas = []
        etiquetas = []

        # Función para calcular crecimiento porcentual entre censos
        def calcular_crecimiento_natalidad(valores):
            resultados = []
            for i in range(1, len(valores)):
                anterior = valores[i - 1]
                actual = valores[i]
                if anterior and actual and anterior != '' and actual != '':
                    anterior_num = float(str(anterior).replace(',', ''))
                    actual_num = float(str(actual).replace(',', ''))
                    if anterior_num > 0:
                        crecimiento = ((actual_num) / anterior_num) ** 0.2
                        resultados.append(crecimiento)
                    else:
                        resultados.append(None)
                else:
                    resultados.append(None)
            return resultados

        # Etiquetas para columnas (pares de censos)
        etiquetas = [f"{tabla_sprv20.columns[i-1]}-{tabla_sprv20.columns[i]}" for i in range(1, len(tabla_sprv20.columns))]

        # Calcular según selección
        if mostrar_unidades:
            valores_ue = tabla_sprv20.loc['UE'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_ue))
            nombres_filas.append("Unidades Económicas")

        if mostrar_personal:
            valores_po = tabla_sprv20.loc['PO'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_po))
            nombres_filas.append("Personal Ocupado")

        # Mostrar tabla combinada
        if filas:
            df_crecimiento_sprv20 = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
            #st.dataframe(df_crecimiento_sprv20, use_container_width=True)
        else:
            st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")


        columnas = ['Año (t)']
        if mostrar_unidades:
            columnas += ('Número de Nacimientos','Supervivientes después de 20 años UE','Probabilidad de Supervivencia UE (%)', 'Tasa de Crecimiento Anual de la Supervivencia UE (%)')    
        if mostrar_personal:
            columnas += ('Nacimiento de Empleos','Supervivientes después de 20 años PO','Probabilidad de Supervivencia PO', 'Tasa de Crecimiento Anual de la Supervivencia PO (%)')    

        df_proyeccion_sprv20 = pd.DataFrame(columns=columnas)

        # Iterar sobre los periodos censales
        for i in range(len(df_crecimiento_sprv20.columns)):
            periodo = df_crecimiento_sprv20.columns[i]
            partes = periodo.split('-')

            anio_inicio_completo = partes[0].strip()
            anio_fin_completo = partes[1].strip()

            anio_inicio_str = anio_inicio_completo.replace('CE','')
            anio_fin_str = anio_fin_completo.replace('CE','')
            
            anio_inicio = int(anio_inicio_str)
            anio_fin = int(anio_fin_str)

            fila_inicial = {'Año (t)': anio_inicio}
            etiqueta_columna = f'CE {anio_inicio}'

            if mostrar_unidades: 
                valor_actual_ue = float(tabla_sprv20.loc['UE',etiqueta_columna])
                tasa_ue = df_crecimiento_sprv20.loc['Unidades Económicas', periodo]
                fila_inicial['Supervivientes después de 20 años UE'] = valor_actual_ue

            if mostrar_personal:
                valor_actual_po = float(tabla_sprv20.loc['PO',etiqueta_columna])
                tasa_po = df_crecimiento_sprv20.loc['Personal Ocupado', periodo]
                fila_inicial['Supervivientes después de 20 años PO'] = valor_actual_po        
            
            df_proyeccion_sprv20.loc[len(df_proyeccion_sprv20)] = fila_inicial

            # Proyección intermedia
            for anio in range(anio_inicio + 1, anio_fin):
                if anio_fin > 2019:
                    break  # No proyectar más allá de 2019
                fila = {'Año (t)': anio}
                if mostrar_unidades:
                    valor_actual_ue *= tasa_ue
                    fila['Supervivientes después de 20 años UE'] = valor_actual_ue
                if mostrar_personal:
                    valor_actual_po *= tasa_po
                    fila['Supervivientes después de 20 años PO'] = valor_actual_po
                df_proyeccion_sprv20.loc[len(df_proyeccion_sprv20)] = fila
 
       
        # --- CÁLCULO DE TASAS QUINQUENALES (Solo para UE, pero se ejecuta el bucle) ---

        # 1. Inicializar variables de proyección ANTES de cualquier condicional

        valor_2019_proyectado_ue = None
        valor_2019_proyectado_po = None
        
        if mostrar_unidades:
            tasas_quinquenales_ue = []
            
            # Este bucle solo es necesario para acumular tasas_quinquenales_ue
            for i in range(len(tabla_sprv20.columns) - 1): 
                censo_actual_str = tabla_sprv20.columns[i]
                censo_siguiente_str = tabla_sprv20.columns[i + 1]

                # Usamos try/except para el caso de etiquetas sin 'CE '
                try:
                    anio_siguiente = int(censo_siguiente_str.replace('CE ', ''))
                except:
                    anio_siguiente = 9999 

                if anio_siguiente > 2023:
                    break

                # Acumulación de Tasas (Unidades Económicas)
                
                valor_actual_ue = float(tabla_sprv20.loc['UE', censo_actual_str])
                valor_siguiente_ue = float(tabla_sprv20.loc['UE', censo_siguiente_str])
                
                if valor_actual_ue > 0:
                    tasa_quinquenal_ue = (valor_siguiente_ue / valor_actual_ue)
                    tasas_quinquenales_ue.append(tasa_quinquenal_ue)
            
            

            # --- CÁLCULO DE PROMEDIOS Y PROYECCIÓN A 2019 (FUERA DEL BUCLE) ---

            # Proyección UE (Utiliza el promedio quinquenal de los censos)
            
            if tasas_quinquenales_ue:
                promedio_quinquenal_ue = sum(tasas_quinquenales_ue) / len(tasas_quinquenales_ue)
                tasa_anual_promedio_ue = promedio_quinquenal_ue**(1/5)
            else:
                tasa_anual_promedio_ue = 1
            #st.write('Tasa_anual_promedio_ue:', tasa_anual_promedio_ue)
            # Valores a la tabla 2019-2022 UE            
            valor_actual_ue = df_proyeccion_sprv20.loc[df_proyeccion_sprv20['Año (t)'] == 2018, 'Supervivientes después de 20 años UE'].iloc[0]            
            proyecciones_ue = {}
            for anio in range(2019, 2023):
                proyecciones_ue[anio] = None
                valor_actual_ue *= tasa_anual_promedio_ue
                proyecciones_ue[anio] = valor_actual_ue
        
        if mostrar_personal:
            valor_actual_po = df_proyeccion_sprv20.loc[df_proyeccion_sprv20['Año (t)'] == 2018, 'Supervivientes después de 20 años PO'].iloc[0]
            proyecciones_po = {}
            for anio in range(2019, 2023):
                proyecciones_po[anio] = None
                tasa_imss_anio = tasas_imss['Tasas'][anio - 2019]  # Ajuste para obtener la tasa correcta
                valor_actual_po *= tasa_imss_anio
                proyecciones_po[anio] = valor_actual_po
        
        # Añadir filas 2019-2022 UE-PO
        for anio in range (2019, 2023):    
            fila3anios = {'Año (t)': anio}
            if mostrar_unidades:        
                fila3anios['Supervivientes después de 20 años UE'] = proyecciones_ue[anio]
            if mostrar_personal:        
                fila3anios['Supervivientes después de 20 años PO'] = proyecciones_po[anio]
            df_proyeccion_sprv20.loc[len(df_proyeccion_sprv20)] = fila3anios

        # Añadir fila 2023

        fila_2023 = {'Año (t)': 2023}
        if mostrar_unidades:
            fila_2023['Supervivientes después de 20 años UE'] = tabla_sprv20.loc['UE', 'CE 2023']
        if mostrar_personal:
            fila_2023['Supervivientes después de 20 años PO'] = tabla_sprv20.loc['PO', 'CE 2023']   
        df_proyeccion_sprv20.loc[len(df_proyeccion_sprv20)] = fila_2023    

        
        # Columna Número de Nacimientos y Nacimiento de Empleos desde df_proyeccion_nat
        if mostrar_unidades:
            df_proyeccion_sprv20['Número de Nacimientos'] = df_proyeccion_nat['Número de Nacimientos']
        
        if mostrar_personal:
            df_proyeccion_sprv20['Nacimiento de Empleos'] = df_proyeccion_nat['Nacimiento de Empleos']
        
        # Calculo de probabilidades
        for anio in range(len(df_proyeccion_sprv20)):
            if mostrar_unidades:
                supervivientes_ue = df_proyeccion_sprv20.loc[anio, 'Supervivientes después de 20 años UE']
                valor_inicial_ue = df_proyeccion_sprv20.loc[anio, 'Número de Nacimientos']
                if valor_inicial_ue and valor_inicial_ue != '' and supervivientes_ue and supervivientes_ue != '':
                    probabilidad_ue = supervivientes_ue / valor_inicial_ue
                    if probabilidad_ue > 1:
                        probabilidad_ue = 1
                    else:
                        pass
                    df_proyeccion_sprv20.loc[anio, 'Probabilidad de Supervivencia UE (%)'] = round(probabilidad_ue, 4)
                    

            if mostrar_personal:
                supervivientes_po = df_proyeccion_sprv20.loc[anio, 'Supervivientes después de 20 años PO']
                valor_inicial_po = df_proyeccion_sprv20.loc[anio, 'Nacimiento de Empleos']
                if valor_inicial_po and valor_inicial_po != '' and supervivientes_po and supervivientes_po != '':
                    probabilidad_po = supervivientes_po / valor_inicial_po
                    if probabilidad_po > 1:
                        probabilidad_po = 1
                    else:
                        pass
                    df_proyeccion_sprv20.loc[anio, 'Probabilidad de Supervivencia PO'] = round(probabilidad_po, 4)
        
        # Calculo de tasa de crecimiento anual de la supervivencia
        for i in range(1, len(df_proyeccion_sprv20)):        
            if mostrar_unidades:
                supervivientes_actual_ue = df_proyeccion_sprv20.loc[i, 'Supervivientes después de 20 años UE']
                supervivientes_anterior_ue = df_proyeccion_sprv20.loc[i - 1, 'Supervivientes después de 20 años UE']
                if supervivientes_anterior_ue and supervivientes_anterior_ue != 0:
                    tasa_ue = ((supervivientes_actual_ue / supervivientes_anterior_ue) - 1) * 100
                    df_proyeccion_sprv20.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia UE (%)'] = round(tasa_ue, 2)

            if mostrar_personal:
                supervivientes_actual_po = df_proyeccion_sprv20.loc[i, 'Supervivientes después de 20 años PO']
                supervivientes_anterior_po = df_proyeccion_sprv20.loc[i - 1, 'Supervivientes después de 20 años PO']
                if supervivientes_anterior_po and supervivientes_anterior_po != 0:
                    tasa_po = ((supervivientes_actual_po / supervivientes_anterior_po) - 1) * 100
                    df_proyeccion_sprv20.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia PO (%)'] = round(tasa_po, 2)
                    
         # Añadir columna Año(-t)
        df_proyeccion_sprv20['Año(-t)'] = df_proyeccion_sprv20['Año (t)'] - 20
       
       # Reordenar columnas para que Año(-t) sea la primera y Año (t) la tercera
        cols = df_proyeccion_sprv20.columns.tolist()
        
        if 'Año(-t)' in cols and 'Año (t)' in cols:
            
            cols.remove('Año(-t)')
            cols.remove('Año (t)')
            
                
            cols.insert(0, 'Año(-t)')
            cols.insert(2, 'Año (t)')
            
        
        if mostrar_unidades and mostrar_personal:
            if 'Año(-t)' in cols and 'Año (t)' in cols:
                
                cols.remove('Año(-t)')
                cols.remove('Año (t)')
                cols.remove('Nacimiento de Empleos')
                    
                cols.insert(0, 'Año(-t)')
                cols.insert(2, 'Año (t)')
                cols.insert(2, 'Nacimiento de Empleos')

            # Reordenar el DataFrame
        df_proyeccion_sprv20 = df_proyeccion_sprv20[cols]

        # --- Visualización de tabla y gráficos interactivos ---

        df_proyeccion_sprv20_formato = df_proyeccion_sprv20.copy()
        
        if mostrar_unidades:
            df_proyeccion_sprv20_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv20_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv20_formato['Número de Nacimientos'] = round(df_proyeccion_sprv20_formato['Número de Nacimientos'].astype(float),0)
            df_proyeccion_sprv20_formato['Número de Nacimientos'] = df_proyeccion_sprv20_formato['Número de Nacimientos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv20_formato['Supervivientes después de 20 años UE'] = round(df_proyeccion_sprv20_formato['Supervivientes después de 20 años UE'].astype(float),0)
            df_proyeccion_sprv20_formato['Supervivientes después de 20 años UE'] = df_proyeccion_sprv20_formato['Supervivientes después de 20 años UE'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv20_formato.reset_index(drop=True, inplace=True)

        if mostrar_personal:
            df_proyeccion_sprv20_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv20_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv20_formato['Nacimiento de Empleos'] = round(df_proyeccion_sprv20_formato['Nacimiento de Empleos'].astype(float),0)        
            df_proyeccion_sprv20_formato['Nacimiento de Empleos'] = df_proyeccion_sprv20_formato['Nacimiento de Empleos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv20_formato['Supervivientes después de 20 años PO'] = round(df_proyeccion_sprv20_formato['Supervivientes después de 20 años PO'].astype(float),0)
            df_proyeccion_sprv20_formato['Supervivientes después de 20 años PO'] = df_proyeccion_sprv20_formato['Supervivientes después de 20 años PO'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv20_formato.reset_index(drop=True, inplace=True)

        col1, col2 = st.columns([40, 60])
        with col1:
            # Mostrar el DataFrame final con la nueva columna
            st.write(f"Supervivientes 20 años después de haber nacido en {entidad.capitalize()}, pertenecientes al sector {sector.capitalize()} con {personal_seleccionado}")
            st.dataframe(df_proyeccion_sprv20_formato, use_container_width=True, height=595)

        with col2:
            st.write("Visualización de Comportamiento Anual")

            # 1. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Supervivientes después de 20 años UE')
            if mostrar_personal:
                columnas.append('Supervivientes después de 20 años PO')

            if columnas:
                fig_negocios = make_subplots(specs=[[{"secondary_y": True}]])
                for i, col in enumerate(columnas):
                    es_secundario = i > 0  # La segunda métrica (si existe) va en el eje secundario
                    color_trazado = '#08989C' if col == 'Supervivientes después de 20 años UE' else '#003057'
                    fig_negocios.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv20['Año (t)'],
                            y=df_proyeccion_sprv20[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.0f}<br>Año: %{x}'
                        ),
                        secondary_y=es_secundario
                    )
                fig_negocios.update_layout(
                    hovermode="x unified",
                    title={
                        'text': f"Número de unidades económicas supervivientes al año t, nacidas 20 años antes en la entidad de<br>{entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                        'font': {'size': 14},
                        'automargin': False
                    },
                    legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                    xaxis_title = 'Año (t)',
                    margin={'t': 110}
                )
            if mostrar_unidades:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_unidades and mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=True)
            with st.container(border=True):
                st.plotly_chart(fig_negocios, use_container_width=True)


            # 2. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Probabilidad de Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Probabilidad de Supervivencia PO')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Probabilidad de Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv20['Año (t)'],
                            y=df_proyeccion_sprv20[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.4f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Probabilidad de superviviencia al año t de las unidades económicas que nacieron 20 años antes en la entidad de<br>{entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>PROBABILIDAD</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)  
            

            # 3. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia PO (%)')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Tasa de Crecimiento Anual de la Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv20['Año (t)'],
                            y=df_proyeccion_sprv20[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.2f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Tasa de crecimiento anual de la supervivencia al año t de las unidades económicas que nacieron 20 años antes en<br>la entidad de {entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE CRECIMIENTO</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)            
          
            st.markdown('<small>Fuente: Censos Económicos 1989-2024<small>', unsafe_allow_html=True) 
    

    if rango_sprv == 25:
         # Extraer censos únicos en orden original
        censos_unicos = []
        for col in df_sprv.columns:
            if col.startswith('CE'):
                censo = col.split(' - ')[0]
                if int(censo.replace('CE ', '')) >= 2013 and censo not in censos_unicos:  # Filtrar censos desde 2013 en adelante                
                    censos_unicos.append(censo)
        
        # Crear estructura para la nueva tabla
        nueva_tabla = {'UE': {}, 'PO': {}}

        # Aplicar lógica: fila 5 para primer censo, 10 para segundo, etc.
        for i, censo in enumerate(censos_unicos):
            fila = (i + 1) * 5   # 5, 10, 15, 20...
            columnas_censo = [col for col in df_sprv.columns if col.startswith(censo)]

            # Inicializar valores
            valor_ue = ''
            valor_po = ''

            for col in columnas_censo:
                if fila < len(df_sprv):  # Validar que la fila exista
                    if 'UE' in col.upper():
                        valor_ue = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]
                    elif 'PO' in col.upper():
                        valor_po = df_sprv.iloc[fila, df_sprv.columns.get_loc(col)]

            nueva_tabla['UE'][censo] = valor_ue
            nueva_tabla['PO'][censo] = valor_po

        # Convertir a DataFrame con censos como columnas
        tabla_sprv25 = pd.DataFrame(nueva_tabla).T
       
        #st.dataframe(tabla_sprv25, use_container_width=True)

        #Calcular crecimiento
        filas = []
        nombres_filas = []
        etiquetas = []

        # Función para calcular crecimiento porcentual entre censos
        def calcular_crecimiento_natalidad(valores):
            resultados = []
            for i in range(1, len(valores)):
                anterior = valores[i - 1]
                actual = valores[i]
                if anterior and actual and anterior != '' and actual != '':
                    anterior_num = float(str(anterior).replace(',', ''))
                    actual_num = float(str(actual).replace(',', ''))
                    if anterior_num > 0:
                        crecimiento = ((actual_num) / anterior_num) ** 0.2
                        resultados.append(crecimiento)
                    else:
                        resultados.append(None)
                else:
                    resultados.append(None)
            return resultados

        # Etiquetas para columnas (pares de censos)
        etiquetas = [f"{tabla_sprv25.columns[i-1]}-{tabla_sprv25.columns[i]}" for i in range(1, len(tabla_sprv25.columns))]

        # Calcular según selección
        if mostrar_unidades:
            valores_ue = tabla_sprv25.loc['UE'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_ue))
            nombres_filas.append("Unidades Económicas")

        if mostrar_personal:
            valores_po = tabla_sprv25.loc['PO'].tolist()
            filas.append(calcular_crecimiento_natalidad(valores_po))
            nombres_filas.append("Personal Ocupado")

        # Mostrar tabla combinada
        if filas:
            df_crecimiento_sprv25 = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
            #st.dataframe(df_crecimiento_sprv25, use_container_width=True)
        else:
            st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")


        columnas = ['Año (t)']
        if mostrar_unidades:
            columnas += ('Número de Nacimientos','Supervivientes después de 25 años UE','Probabilidad de Supervivencia UE (%)', 'Tasa de Crecimiento Anual de la Supervivencia UE (%)')    
        if mostrar_personal:
            columnas += ('Nacimiento de Empleos','Supervivientes después de 25 años PO','Probabilidad de Supervivencia PO', 'Tasa de Crecimiento Anual de la Supervivencia PO (%)')    

        df_proyeccion_sprv25 = pd.DataFrame(columns=columnas)

        # Iterar sobre los periodos censales
        for i in range(len(df_crecimiento_sprv25.columns)):
            periodo = df_crecimiento_sprv25.columns[i]
            partes = periodo.split('-')

            anio_inicio_completo = partes[0].strip()
            anio_fin_completo = partes[1].strip()

            anio_inicio_str = anio_inicio_completo.replace('CE','')
            anio_fin_str = anio_fin_completo.replace('CE','')
            
            anio_inicio = int(anio_inicio_str)
            anio_fin = int(anio_fin_str)

            fila_inicial = {'Año (t)': anio_inicio}
            etiqueta_columna = f'CE {anio_inicio}'

            if mostrar_unidades: 
                valor_actual_ue = float(tabla_sprv25.loc['UE',etiqueta_columna])
                tasa_ue = df_crecimiento_sprv25.loc['Unidades Económicas', periodo]
                fila_inicial['Supervivientes después de 25 años UE'] = valor_actual_ue

            if mostrar_personal:
                valor_actual_po = float(tabla_sprv25.loc['PO',etiqueta_columna])
                tasa_po = df_crecimiento_sprv25.loc['Personal Ocupado', periodo]
                fila_inicial['Supervivientes después de 25 años PO'] = valor_actual_po        
            
            df_proyeccion_sprv25.loc[len(df_proyeccion_sprv25)] = fila_inicial

            # Proyección intermedia
            for anio in range(anio_inicio + 1, anio_fin):
                if anio_fin > 2019:
                    break  # No proyectar más allá de 2019
                fila = {'Año (t)': anio}
                if mostrar_unidades:
                    valor_actual_ue *= tasa_ue
                    fila['Supervivientes después de 25 años UE'] = valor_actual_ue
                if mostrar_personal:
                    valor_actual_po *= tasa_po
                    fila['Supervivientes después de 25 años PO'] = valor_actual_po
                df_proyeccion_sprv25.loc[len(df_proyeccion_sprv25)] = fila
 
       
        # --- CÁLCULO DE TASAS QUINQUENALES (Solo para UE, pero se ejecuta el bucle) ---

        # 1. Inicializar variables de proyección ANTES de cualquier condicional

        valor_2019_proyectado_ue = None
        valor_2019_proyectado_po = None
        
        if mostrar_unidades:
            tasas_quinquenales_ue = []
            
            # Este bucle solo es necesario para acumular tasas_quinquenales_ue
            for i in range(len(tabla_sprv25.columns) - 1): 
                censo_actual_str = tabla_sprv25.columns[i]
                censo_siguiente_str = tabla_sprv25.columns[i + 1]

                # Usamos try/except para el caso de etiquetas sin 'CE '
                try:
                    anio_siguiente = int(censo_siguiente_str.replace('CE ', ''))
                except:
                    anio_siguiente = 9999 

                if anio_siguiente > 2023:
                    break

                # Acumulación de Tasas (Unidades Económicas)
                
                valor_actual_ue = float(tabla_sprv25.loc['UE', censo_actual_str])
                valor_siguiente_ue = float(tabla_sprv25.loc['UE', censo_siguiente_str])
                
                if valor_actual_ue > 0:
                    tasa_quinquenal_ue = (valor_siguiente_ue / valor_actual_ue)
                    tasas_quinquenales_ue.append(tasa_quinquenal_ue)
            
            

            # --- CÁLCULO DE PROMEDIOS Y PROYECCIÓN A 2019 (FUERA DEL BUCLE) ---

            # Proyección UE (Utiliza el promedio quinquenal de los censos)
            
            if tasas_quinquenales_ue:
                promedio_quinquenal_ue = sum(tasas_quinquenales_ue) / len(tasas_quinquenales_ue)
                tasa_anual_promedio_ue = promedio_quinquenal_ue**(1/5)
            else:
                tasa_anual_promedio_ue = 1
            #st.write('Tasa_anual_promedio_ue:', tasa_anual_promedio_ue)
            
            # Valores a la tabla 2019-2022 UE            
            valor_actual_ue = df_proyeccion_sprv25.loc[df_proyeccion_sprv25['Año (t)'] == 2018, 'Supervivientes después de 25 años UE'].iloc[0]            
            proyecciones_ue = {}
            for anio in range(2019, 2023):
                proyecciones_ue[anio] = None
                valor_actual_ue *= tasa_anual_promedio_ue
                proyecciones_ue[anio] = valor_actual_ue
        
        if mostrar_personal:
            valor_actual_po = df_proyeccion_sprv25.loc[df_proyeccion_sprv25['Año (t)'] == 2018, 'Supervivientes después de 25 años PO'].iloc[0]
            proyecciones_po = {}
            for anio in range(2019, 2023):
                proyecciones_po[anio] = None
                tasa_imss_anio = tasas_imss['Tasas'][anio - 2019]  # Ajuste para obtener la tasa correcta
                valor_actual_po *= tasa_imss_anio
                proyecciones_po[anio] = valor_actual_po
        
        # Añadir filas 2019-2022 UE-PO
        for anio in range (2019, 2023):    
            fila3anios = {'Año (t)': anio}
            if mostrar_unidades:        
                fila3anios['Supervivientes después de 25 años UE'] = proyecciones_ue[anio]
            if mostrar_personal:        
                fila3anios['Supervivientes después de 25 años PO'] = proyecciones_po[anio]
            df_proyeccion_sprv25.loc[len(df_proyeccion_sprv25)] = fila3anios

        # Añadir fila 2023

        fila_2023 = {'Año (t)': 2023}
        if mostrar_unidades:
            fila_2023['Supervivientes después de 25 años UE'] = tabla_sprv25.loc['UE', 'CE 2023']
        if mostrar_personal:
            fila_2023['Supervivientes después de 25 años PO'] = tabla_sprv25.loc['PO', 'CE 2023']   
        df_proyeccion_sprv25.loc[len(df_proyeccion_sprv25)] = fila_2023    

        
        # Columna Número de Nacimientos y Nacimiento de Empleos desde df_proyeccion_nat
        if mostrar_unidades:
            df_proyeccion_sprv25['Número de Nacimientos'] = df_proyeccion_nat['Número de Nacimientos']
        
        if mostrar_personal:
            df_proyeccion_sprv25['Nacimiento de Empleos'] = df_proyeccion_nat['Nacimiento de Empleos']
        
        # Calculo de probabilidades
        for anio in range(len(df_proyeccion_sprv25)):
            if mostrar_unidades:
                supervivientes_ue = df_proyeccion_sprv25.loc[anio, 'Supervivientes después de 25 años UE']
                valor_inicial_ue = df_proyeccion_sprv25.loc[anio, 'Número de Nacimientos']
                if valor_inicial_ue and valor_inicial_ue != '' and supervivientes_ue and supervivientes_ue != '':
                    probabilidad_ue = supervivientes_ue / valor_inicial_ue
                    if probabilidad_ue > 1:
                        probabilidad_ue = 1
                    else:
                        pass
                    df_proyeccion_sprv25.loc[anio, 'Probabilidad de Supervivencia UE (%)'] = round(probabilidad_ue, 4)
                    

            if mostrar_personal:
                supervivientes_po = df_proyeccion_sprv25.loc[anio, 'Supervivientes después de 25 años PO']
                valor_inicial_po = df_proyeccion_sprv25.loc[anio, 'Nacimiento de Empleos']
                if valor_inicial_po and valor_inicial_po != '' and supervivientes_po and supervivientes_po != '':
                    probabilidad_po = supervivientes_po / valor_inicial_po
                    if probabilidad_po > 1:
                        probabilidad_po = 1
                    else:
                        pass
                    df_proyeccion_sprv25.loc[anio, 'Probabilidad de Supervivencia PO'] = round(probabilidad_po, 4)
        
        # Calculo de tasa de crecimiento anual de la supervivencia
        for i in range(1, len(df_proyeccion_sprv25)):        
            if mostrar_unidades:
                supervivientes_actual_ue = df_proyeccion_sprv25.loc[i, 'Supervivientes después de 25 años UE']
                supervivientes_anterior_ue = df_proyeccion_sprv25.loc[i - 1, 'Supervivientes después de 25 años UE']
                if supervivientes_anterior_ue and supervivientes_anterior_ue != 0:
                    tasa_ue = ((supervivientes_actual_ue / supervivientes_anterior_ue) - 1) * 100
                    df_proyeccion_sprv25.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia UE (%)'] = round(tasa_ue, 2)

            if mostrar_personal:
                supervivientes_actual_po = df_proyeccion_sprv25.loc[i, 'Supervivientes después de 25 años PO']
                supervivientes_anterior_po = df_proyeccion_sprv25.loc[i - 1, 'Supervivientes después de 25 años PO']
                if supervivientes_anterior_po and supervivientes_anterior_po != 0:
                    tasa_po = ((supervivientes_actual_po / supervivientes_anterior_po) - 1) * 100
                    df_proyeccion_sprv25.loc[i, 'Tasa de Crecimiento Anual de la Supervivencia PO (%)'] = round(tasa_po, 2)
                    
         # Añadir columna Año(-t)
        df_proyeccion_sprv25['Año(-t)'] = df_proyeccion_sprv25['Año (t)'] - 25
       
       # Reordenar columnas para que Año(-t) sea la primera y Año (t) la tercera
        cols = df_proyeccion_sprv25.columns.tolist()
        
        if 'Año(-t)' in cols and 'Año (t)' in cols:
            
            cols.remove('Año(-t)')
            cols.remove('Año (t)')
            
                
            cols.insert(0, 'Año(-t)')
            cols.insert(2, 'Año (t)')
            
        
        if mostrar_unidades and mostrar_personal:
            if 'Año(-t)' in cols and 'Año (t)' in cols:
                
                cols.remove('Año(-t)')
                cols.remove('Año (t)')
                cols.remove('Nacimiento de Empleos')
                    
                cols.insert(0, 'Año(-t)')
                cols.insert(2, 'Año (t)')
                cols.insert(2, 'Nacimiento de Empleos')

            # Reordenar el DataFrame
        df_proyeccion_sprv25 = df_proyeccion_sprv25[cols]

        # --- Visualización de tabla y gráficos interactivos ---

        df_proyeccion_sprv25_formato = df_proyeccion_sprv25.copy()
        
        if mostrar_unidades:
            df_proyeccion_sprv25_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv25_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv25_formato['Número de Nacimientos'] = round(df_proyeccion_sprv25_formato['Número de Nacimientos'].astype(float),0)
            df_proyeccion_sprv25_formato['Número de Nacimientos'] = df_proyeccion_sprv25_formato['Número de Nacimientos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv25_formato['Supervivientes después de 25 años UE'] = round(df_proyeccion_sprv25_formato['Supervivientes después de 25 años UE'].astype(float),0)
            df_proyeccion_sprv25_formato['Supervivientes después de 25 años UE'] = df_proyeccion_sprv25_formato['Supervivientes después de 25 años UE'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv25_formato.reset_index(drop=True, inplace=True)

        if mostrar_personal:
            df_proyeccion_sprv25_formato.sort_values(by='Año (t)', inplace=True)
            df_proyeccion_sprv25_formato.drop_duplicates(subset='Año (t)', keep='last', inplace=True)
            df_proyeccion_sprv25_formato['Nacimiento de Empleos'] = round(df_proyeccion_sprv25_formato['Nacimiento de Empleos'].astype(float),0)        
            df_proyeccion_sprv25_formato['Nacimiento de Empleos'] = df_proyeccion_sprv25_formato['Nacimiento de Empleos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv25_formato['Supervivientes después de 25 años PO'] = round(df_proyeccion_sprv25_formato['Supervivientes después de 25 años PO'].astype(float),0)
            df_proyeccion_sprv25_formato['Supervivientes después de 25 años PO'] = df_proyeccion_sprv25_formato['Supervivientes después de 25 años PO'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
            df_proyeccion_sprv25_formato.reset_index(drop=True, inplace=True)

        col1, col2 = st.columns([40, 60])
        with col1:
            # Mostrar el DataFrame final con la nueva columna
            st.write(f"Supervivientes 25 años después de haber nacido en {entidad.capitalize()}, pertenecientes al sector {sector.capitalize()} con {personal_seleccionado}")
            st.dataframe(df_proyeccion_sprv25_formato, use_container_width=True, height=420)

        with col2:
            st.write("Visualización de Comportamiento Anual")

            # 1. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Supervivientes después de 25 años UE')
            if mostrar_personal:
                columnas.append('Supervivientes después de 25 años PO')

            if columnas:
                fig_negocios = make_subplots(specs=[[{"secondary_y": True}]])
                for i, col in enumerate(columnas):
                    es_secundario = i > 0  # La segunda métrica (si existe) va en el eje secundario
                    color_trazado = '#08989C' if col == 'Supervivientes después de 25 años UE' else '#003057'
                    fig_negocios.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv25_formato['Año (t)'],
                            y=df_proyeccion_sprv25_formato[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.0f}<br>Año: %{x}'
                        ),
                        secondary_y=es_secundario
                    )
                fig_negocios.update_layout(
                    hovermode="x unified",
                    title={
                        'text': f"Número de unidades económicas supervivientes al año t, nacidas 25 años antes en la entidad de<br>{entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                        'font': {'size': 14},
                        'automargin': False
                    },
                    legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                    xaxis_title = 'Año (t)',
                    margin={'t': 110}
                )
            if mostrar_unidades:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=False)
            if mostrar_unidades and mostrar_personal:
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES UE</b>', title_font=dict(size=13), secondary_y=False)
                fig_negocios.update_yaxes(title_text='<b>SUPERVIVIENTES PO</b>', title_font=dict(size=13), secondary_y=True)
            with st.container(border=True):
                st.plotly_chart(fig_negocios, use_container_width=True)


            # 2. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Probabilidad de Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Probabilidad de Supervivencia PO')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Probabilidad de Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv25['Año (t)'],
                            y=df_proyeccion_sprv25[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.4f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Probabilidad de superviviencia al año t de las unidades económicas que nacieron 25 años antes en la entidad de<br>{entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>PROBABILIDAD</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)  
            

            # 3. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia UE (%)')
            if mostrar_personal:
                columnas.append('Tasa de Crecimiento Anual de la Supervivencia PO (%)')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Tasa de Crecimiento Anual de la Supervivencia UE (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_sprv25['Año (t)'],
                            y=df_proyeccion_sprv25[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.2f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Tasa de crecimiento anual de la supervivencia al año t de las unidades económicas que nacieron 25 años antes en<br>la entidad de {entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año (t)',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE CRECIMIENTO</b>', title_font=dict(size=13))    
            with st.container(border=True):
                st.plotly_chart(fig_negocios_tasas, use_container_width=True)            
          
            st.markdown('<small>Fuente: Censos Económicos 1989-2024<small>', unsafe_allow_html=True) 

        

#----MORTALIDAD DE UNIDADES ECONÓMICAS Y MORTALIDAD DE EMPLEOS ----    
if fenomeno_demografico == 'Mortalidad':
    st.markdown("---")
    st.subheader("Mortalidad")
    st.markdown('---')
    
    if mostrar_unidades:
        df_activos = df_proyeccion[['Año', 'Número de Negocios']].iloc[5:].copy()
        df_activos_completo = df_proyeccion[['Año', 'Número de Negocios']].copy()
        df_activos.reset_index(drop=True, inplace=True)
        
    if mostrar_personal:
        df_activos = df_proyeccion[['Año', 'Personal Ocupado']].iloc[5:].copy()
        df_activos_completo = df_proyeccion[['Año', 'Personal Ocupado']].copy()
        df_activos.reset_index(drop=True, inplace=True)

    if mostrar_unidades and mostrar_personal:
        df_activos = df_proyeccion[['Año', 'Número de Negocios', 'Personal Ocupado']].iloc[5:].copy()
        df_activos_completo = df_proyeccion[['Año', 'Número de Negocios', 'Personal Ocupado']].copy()
        df_activos.reset_index(drop=True, inplace=True)
    

    #st.dataframe(df_activos_completo)
    #st.dataframe(df_activos)


    df_mrt = tabla_pivote.copy()
           
    df_mrt.columns = [col.strip() for col in df_mrt.columns]
    
    # Extraer censos únicos en orden original
    censos_unicos = []
    for col in df_mrt.columns:
        if col.startswith('CE'):
            partes = col.split(' - ')
            if len(partes) > 0:
                censo = partes[0]
                try:
                    anio_censo = int(censo.replace('CE ', ''))
                    if anio_censo >= 1993 and censo not in censos_unicos:  # Filtrar censos desde 1993 en adelante                
                        censos_unicos.append(censo)
                except ValueError:
                    continue  # Saltar si no se puede convertir a entero
    
    # Crear estructura para la nueva tabla
    nueva_tabla = {'UE': {}, 'PO': {}}
    
    for i, censo in enumerate(censos_unicos):
        limite_superior = ((i + 1) * 5)+1   # 5, 10, 15, 20...
        columnas_censo = [col for col in df_mrt.columns if col.startswith(censo)]
    
        # Inicializar valores
        suma_ue = 0
        suma_po = 0

        for col in columnas_censo:
            segmento_filas = df_mrt[col].iloc[0 : limite_superior]
            if 'UE' in col.upper():
                suma_ue = segmento_filas.sum()
            elif 'PO' in col.upper():
                suma_po = segmento_filas.sum()
        nueva_tabla['UE'][censo] = suma_ue
        nueva_tabla['PO'][censo] = suma_po
    
    # Convertir a DataFrame con censos como columnas
    tabla_sprv_t = pd.DataFrame(nueva_tabla).T
    #st.write('tabla_sprv_t')
    #st.dataframe(tabla_sprv_t, use_container_width=True)


    #Calcular crecimiento
    filas = []
    nombres_filas = []
    etiquetas = []

    # Función para calcular crecimiento porcentual entre censos
    def calcular_crecimiento_sprv_t(valores):
        resultados = []
        for i in range(1, len(valores)):
            anterior = valores[i - 1]
            actual = valores[i]
            if anterior and actual and anterior != '' and actual != '':
                anterior_num = float(str(anterior).replace(',', ''))
                actual_num = float(str(actual).replace(',', ''))
                if anterior_num > 0:
                    crecimiento = ((actual_num) / anterior_num) ** 0.2
                    resultados.append(crecimiento)
                else:
                    resultados.append(None)
            else:
                resultados.append(None)
        return resultados

    # Etiquetas para columnas (pares de censos)
    etiquetas = [f"{tabla_sprv_t.columns[i-1]}-{tabla_sprv_t.columns[i]}" for i in range(1, len(tabla_sprv_t.columns))]

    # Calcular según selección
    if mostrar_unidades:
        valores_ue = tabla_sprv_t.loc['UE'].tolist()
        filas.append(calcular_crecimiento_sprv_t(valores_ue))
        nombres_filas.append("Unidades Económicas")

    if mostrar_personal:
        valores_po = tabla_sprv_t.loc['PO'].tolist()
        filas.append(calcular_crecimiento_sprv_t(valores_po))
        nombres_filas.append("Personal Ocupado")

    # Mostrar tabla combinada
    if filas:
        df_crecimiento_sprv_t = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
        #st.write('df_crecimiento_sprv_t')
        #st.dataframe(df_crecimiento_sprv_t, use_container_width=True)
    else:
        st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")


   
    # Calculo de número de muertos x≥0
    resultados_finales = {'UE': {}, 'PO': {}}

    for i, censo in enumerate(tabla_sprv_t.columns):
        idx_fila = i * 5
        if mostrar_unidades:
            if idx_fila < len(df_activos_completo):
                val_activos_ue = df_activos_completo.iloc[idx_fila, 1]
                val_mrt_ue = tabla_sprv_t.iloc[0, i]
                resultados_finales['UE'][censo] = val_activos_ue - val_mrt_ue
                if resultados_finales['UE'][censo] < 0:
                    resultados_finales['UE'][censo] = 0
        
        if mostrar_personal:
            if idx_fila < len(df_activos_completo):
                val_activos_po = df_activos_completo.iloc[idx_fila, 1]
                val_mrt_po = tabla_sprv_t.iloc[1, i]
                resultados_finales['PO'][censo] = val_activos_po - val_mrt_po
                if resultados_finales['PO'][censo] < 0:
                    resultados_finales['PO'][censo] = 0

        if mostrar_unidades and mostrar_personal:
            if idx_fila < len(df_activos_completo):
                val_activos_ue = df_activos_completo.iloc[idx_fila, 1]
                val_mrt_ue = tabla_sprv_t.iloc[0, i]
                resultados_finales['UE'][censo] = val_activos_ue - val_mrt_ue
                if resultados_finales['UE'][censo] < 0:
                    resultados_finales['UE'][censo] = 0

                val_activos_po = df_activos_completo.iloc[idx_fila, 2]
                val_mrt_po = tabla_sprv_t.iloc[1, i]
                resultados_finales['PO'][censo] = val_activos_po - val_mrt_po
                if resultados_finales['PO'][censo] < 0:
                    resultados_finales['PO'][censo] = 0


    tabla_mrt = pd.DataFrame(resultados_finales).T
    #st.write('tabla_mrt')
    #st.dataframe(tabla_mrt, use_container_width=True)


    #Calcular crecimiento
    filas = []
    nombres_filas = []
    etiquetas = []

    # Función para calcular crecimiento porcentual entre censos
    def df_crecimiento_mrt(valores):
        resultados = []
        for i in range(1, len(valores)):
            anterior = valores[i - 1]
            actual = valores[i]
            if anterior and actual and anterior != '' and actual != '':
                anterior_num = float(str(anterior).replace(',', ''))
                actual_num = float(str(actual).replace(',', ''))
                if anterior_num > 0:
                    crecimiento = ((actual_num) / anterior_num) ** 0.2
                    resultados.append(crecimiento)
                else:
                    resultados.append(None)
            else:
                resultados.append(None)
        return resultados

    # Etiquetas para columnas (pares de censos)
    etiquetas = [f"{tabla_mrt.columns[i-1]}-{tabla_mrt.columns[i]}" for i in range(1, len(tabla_mrt.columns))]

    # Calcular según selección
    if mostrar_unidades:
        valores_ue = tabla_mrt.loc['UE'].tolist()
        filas.append(df_crecimiento_mrt(valores_ue))
        nombres_filas.append("Unidades Económicas")

    if mostrar_personal:
        valores_po = tabla_mrt.loc['PO'].tolist()
        filas.append(df_crecimiento_mrt(valores_po))
        nombres_filas.append("Personal Ocupado")

    # Mostrar tabla combinada
    #st.write('df_crecimiento_mrt')
    if filas:
        df_crecimiento_mrt = pd.DataFrame(filas, columns=etiquetas, index=nombres_filas)
        #st.dataframe(df_crecimiento_mrt, use_container_width=True)
    else:
        st.info("Selecciona al menos una métrica para calcular el índice de crecimiento.")

    
    # TABLA DE PROYECCION DE MORTALIDAD
    
    columnas = ['Año']
    if mostrar_unidades:
        columnas += ['Activos', 'Sobrevivientes ≥5 en el año t', 'Número de negocios muertos x≥0','Tasa de mortalidad (%)','Tasa de crecimiento anual de la mortalidad (%)']
    if mostrar_personal:
        columnas += ['Empleos activos', 'Empleos sobrevivientes ≥5 en el año t', 'Número de empleos muertos x≥0','Tasa de mortalidad de los empleos (%)','Tasa de crecimiento anual de la mortalidad de los empleos (%)']

    

    df_proyeccion_mrt = pd.DataFrame()

    for i in range(len(df_crecimiento_sprv_t.columns)):
        periodo = df_crecimiento_sprv_t.columns[i]
        partes = periodo.split('-')

        anio_inicio_completo = partes[0].strip()
        anio_fin_completo = partes[1].strip()

        anio_inicio_str = anio_inicio_completo.replace('CE', '')
        anio_fin_str = anio_fin_completo.replace('CE', '')
        
        anio_inicio = int(anio_inicio_str)
        anio_fin = int(anio_fin_str)

        etiqueta_columna = f'CE {anio_inicio}'

        if mostrar_unidades:
            valor_actual_ue = float(tabla_sprv_t.loc['UE', etiqueta_columna])
            tasa_ue = float(df_crecimiento_sprv_t.loc['Unidades Económicas', periodo])
            df_proyeccion_mrt.loc[anio_inicio, 'Sobrevivientes ≥5 en el año t'] = valor_actual_ue

        if mostrar_personal:
            valor_actual_po = float(tabla_sprv_t.loc['PO', etiqueta_columna])
            tasa_po = float(df_crecimiento_sprv_t.loc['Personal Ocupado', periodo])
            df_proyeccion_mrt.loc[anio_inicio, 'Empleos sobrevivientes ≥5 en el año t'] = valor_actual_po        


        for anio in range(anio_inicio + 1, anio_fin):
            if anio_fin > 2019:
                break  # No proyectar internamente en este periodo

            if mostrar_unidades:
                valor_actual_ue *= tasa_ue
                df_proyeccion_mrt.loc[anio, 'Sobrevivientes ≥5 en el año t'] = valor_actual_ue

            if mostrar_personal:
                valor_actual_po *= tasa_po
                df_proyeccion_mrt.loc[anio, 'Empleos sobrevivientes ≥5 en el año t'] = valor_actual_po

    # 2.2) CÁLCULO DE TASAS QUINQUENALES (UE) y proyección a 2019
    valor_2019_proyectado_ue = None
    valor_2019_proyectado_po = None

    if mostrar_unidades:
        tasas_quinquenales_ue = []
        for i in range(len(tabla_sprv_t.columns) - 1):
            censo_actual_str = tabla_sprv_t.columns[i]
            censo_siguiente_str = tabla_sprv_t.columns[i + 1]

            try:
                anio_siguiente = int(censo_siguiente_str.replace('CE ', ''))
            except Exception:
                anio_siguiente = 9999

            if anio_siguiente > 2023:
                break

            valor_actual_ue = float(tabla_sprv_t.loc['UE', censo_actual_str])
            valor_siguiente_ue = float(tabla_sprv_t.loc['UE', censo_siguiente_str])

            if valor_actual_ue > 0:
                tasa_quinquenal_ue = (valor_siguiente_ue / valor_actual_ue)
                tasas_quinquenales_ue.append(tasa_quinquenal_ue)

        if tasas_quinquenales_ue:
            promedio_quinquenal_ue = sum(tasas_quinquenales_ue) / len(tasas_quinquenales_ue)
            tasa_anual_promedio_ue = promedio_quinquenal_ue ** (1/5)
        else:
            tasa_anual_promedio_ue = 1.0

        # Buscar el valor 2018 sobrevivientes UE
        try:
            valor_2018_ue = df_proyeccion_mrt.loc[2018, 'Sobrevivientes ≥5 en el año t']
        except KeyError:
            st.warning("No se encontró el año 2018 en 'Sobrevivientes ≥5 en el año t'. Verifica el armado previo.")
            valor_2018_ue = None

        if valor_2018_ue is not None:
            valor_2019_proyectado_ue = float(valor_2018_ue) * float(tasa_anual_promedio_ue)

    # 2.3) PROYECCIÓN PO 2019 con tasa IMSS
    if mostrar_personal:
        try:
            tasa_imss_2019 = float(tasas_imss['Tasas'][0])  # ej. [1.0184, 0.9681, 1.0558, 1.0319]
        except Exception:
            st.error("No se pudo leer 'tasa_imss_2019' de tasas_imss['Tasas'][0].")
            tasa_imss_2019 = None

        try:
            valor_2018_po = df_proyeccion_mrt.loc[2018, 'Empleos sobrevivientes ≥5 en el año t']
        except KeyError:
            st.warning("No se encontró el año 2018 en 'Empleos sobrevivientes ≥5 en el año t'. Verifica el armado previo.")
            valor_2018_po = None

        if tasa_imss_2019 is not None and valor_2018_po is not None:
            valor_2019_proyectado_po = float(valor_2018_po) * float(tasa_imss_2019)

    # Añadir fila 2019 (escribiendo por índice)
    if valor_2019_proyectado_ue is not None:
        df_proyeccion_mrt.loc[2019, 'Sobrevivientes ≥5 en el año t'] = valor_2019_proyectado_ue

    if valor_2019_proyectado_po is not None:
        df_proyeccion_mrt.loc[2019, 'Empleos sobrevivientes ≥5 en el año t'] = valor_2019_proyectado_po

   
    # PROBABILIDADES 2020–2022 (UE) y Tasas IMSS 2020–2022 (PO)
   
    if mostrar_unidades:
        df_probabilidades = cargar_probabilidades()
        if df_probabilidades.empty:
            st.stop()

        # Normalizar filtros
        sector_filtrado_prob = sector.upper().strip()
        if sector_filtrado_prob == 'SERVICIOS PRIVADOS NO FINANCIEROS':
            sector_filtrado_prob = 'SERVICIOS PRIVADOS NO FINANCIEROS'

        # Obtener base 2019 UE
        try:
            valor_base_ue = df_proyeccion_mrt.loc[2019, 'Sobrevivientes ≥5 en el año t']
        except KeyError:
            valor_base_ue = None
            st.warning("No hay valor 2019 para UE. Se omite proyección 2020–2022 de UE.")

        if valor_base_ue is not None:
            proyected_value_ue = float(valor_base_ue)
            for anio_futuro in range(2020, 2023):
                try:
                    tasas = df_probabilidades[
                        (df_probabilidades['ENTIDAD'] == entidad.upper()) &
                        (df_probabilidades['SECTOR'] == sector_filtrado_prob) &
                        (df_probabilidades['TAMAÑO'] == personal_seleccionado) &
                        (df_probabilidades['AÑO'] == anio_futuro)
                    ]
                    if not tasas.empty:
                        tasa_supervivencia = float(tasas['SOBREVIVIENTES'].iloc[0])
                        proyected_value_ue *= tasa_supervivencia
                        df_proyeccion_mrt.loc[anio_futuro, 'Sobrevivientes ≥5 en el año t'] = proyected_value_ue
                    else:
                        st.warning(f"No hay probabilidades para {entidad}, {sector}, {personal_seleccionado}, {anio_futuro}.")
                except Exception as e:
                    st.error(f"Error al obtener tasas para {anio_futuro}: {e}")

    # PO 2020–2022 por IMSS
    if mostrar_personal:
        try:
            valor_base_po = df_proyeccion_mrt.loc[2019, 'Empleos sobrevivientes ≥5 en el año t']
        except KeyError:
            valor_base_po = None
            st.warning("No hay valor 2019 para PO. Se omite proyección 2020–2022 de PO.")

        if valor_base_po is not None:
            proyected_value_po = float(valor_base_po)
            # esperamos tasas_imss['Tasas'][1:4]
            try:
                tasas_2020_2022 = [
                    float(tasas_imss['Tasas'][1]),
                    float(tasas_imss['Tasas'][2]),
                    float(tasas_imss['Tasas'][3]),
                ]
            except Exception:
                st.error("No se pudieron leer tasas IMSS 2020–2022 de 'tasas_imss['Tasas']'.")
                tasas_2020_2022 = None

            if tasas_2020_2022:
                for offset, anio in enumerate(range(2020, 2023)):
                    proyected_value_po *= tasas_2020_2022[offset]
                    df_proyeccion_mrt.loc[anio, 'Empleos sobrevivientes ≥5 en el año t'] = proyected_value_po

    
    # Añadir 2023 desde tabla_sprv_t
    
    if mostrar_unidades:
        try:
            df_proyeccion_mrt.loc[2023, 'Sobrevivientes ≥5 en el año t'] = float(tabla_sprv_t.loc['UE', 'CE 2023'])
        except Exception:
            st.warning("No se pudo asignar UE 2023 desde 'tabla_sprv_t'.")

    if mostrar_personal:
        try:
            df_proyeccion_mrt.loc[2023, 'Empleos sobrevivientes ≥5 en el año t'] = float(tabla_sprv_t.loc['PO', 'CE 2023'])
        except Exception:
            st.warning("No se pudo asignar PO 2023 desde 'tabla_sprv_t'.")

   
    # ACTIVOS y EMPLEOS ACTIVOS (mapeo por Año, no por índice posicional)
   
    def _map_by_year(df_base, df_origen, col_origen, col_destino):
        """Mapea col_origen de df_origen -> df_base[col_destino] por Año."""
        if 'Año' in df_origen.columns:
            serie_origen = df_origen.set_index('Año')[col_origen]
        else:
            # Si df_activos ya trae el índice por Año
            serie_origen = df_origen[col_origen]
            serie_origen.index = serie_origen.index.astype(int)
        df_base[col_destino] = df_base.index.map(serie_origen)

    if mostrar_unidades:
        try:
            _map_by_year(df_proyeccion_mrt, df_activos, 'Número de Negocios', 'Activos')
        except Exception as e:
            st.warning(f"No se pudo mapear 'Activos' desde df_activos: {e}")

    if mostrar_personal:
        try:
            _map_by_year(df_proyeccion_mrt, df_activos, 'Personal Ocupado', 'Empleos activos')
        except Exception as e:
            st.warning(f"No se pudo mapear 'Empleos activos' desde df_activos: {e}")


    # MUERTOS (UE/PO) hasta 2019 — 

    for i in range(len(df_crecimiento_mrt.columns)):
        periodo = df_crecimiento_mrt.columns[i]
        partes = periodo.split('-')

        anio_inicio_completo = partes[0].strip()
        anio_fin_completo = partes[1].strip()

        anio_inicio_str = anio_inicio_completo.replace('CE', '')
        anio_fin_str = anio_fin_completo.replace('CE', '')
        
        anio_inicio = int(anio_inicio_str)
        anio_fin = int(anio_fin_str)

        etiqueta_columna = f'CE {anio_inicio}'

        
        if mostrar_unidades:
            valor_actual_ue = float(tabla_mrt.loc['UE', etiqueta_columna])
            tasa_ue = df_crecimiento_mrt.loc['Unidades Económicas', periodo]
            tasa_ue = 0 if pd.isna(tasa_ue) else float(tasa_ue)
            df_proyeccion_mrt.loc[anio_inicio, 'Número de negocios muertos x≥0'] = valor_actual_ue

        if mostrar_personal:
            valor_actual_po = float(tabla_mrt.loc['PO', etiqueta_columna])
            tasa_po = df_crecimiento_mrt.loc['Personal Ocupado', periodo]
            tasa_po = 0 if pd.isna(tasa_po) else float(tasa_po)
            df_proyeccion_mrt.loc[anio_inicio, 'Número de empleos muertos x≥0'] = valor_actual_po
        

        # Intermedio (sin pasar de 2019 en este tramo)
        for anio in range(anio_inicio + 1, anio_fin):
            if anio_fin > 2019:
                break  # 2019 o superiores se manejan fuera (o no se proyectan aquí)

            base_activos = (df_activos_completo.set_index('Año')
                            if 'Año' in df_activos_completo.columns
                            else df_activos_completo)

            if mostrar_unidades:
                if tasa_ue == 0:
                    
                    activos_5 = (float(base_activos.loc[anio - 5, 'Número de Negocios'])
                                if (anio - 5) in base_activos.index else np.nan)
                    
                    sobrev = (float(df_proyeccion_mrt.loc[anio, 'Sobrevivientes ≥5 en el año t'])
                            if ('Sobrevivientes ≥5 en el año t' in df_proyeccion_mrt.columns and anio in df_proyeccion_mrt.index)
                            else np.nan)

                    
                    if pd.isna(activos_5) or pd.isna(sobrev):
                        valor_actual_ue = np.nan
                    else:
                        valor_actual_ue = activos_5 - sobrev
                        if valor_actual_ue < 0:
                            valor_actual_ue = 0.0
                else:
                    valor_actual_ue *= tasa_ue

                df_proyeccion_mrt.loc[anio, 'Número de negocios muertos x≥0'] = valor_actual_ue

            
            if mostrar_personal:
                if tasa_po == 0:
                    empleos_activos_5 = (float(base_activos.loc[anio - 5, 'Personal Ocupado'])
                                        if (anio - 5) in base_activos.index else np.nan)
                    sobrev_po = (float(df_proyeccion_mrt.loc[anio, 'Empleos sobrevivientes ≥5 en el año t'])
                                if ('Empleos sobrevivientes ≥5 en el año t' in df_proyeccion_mrt.columns and anio in df_proyeccion_mrt.index)
                                else np.nan)

                    if pd.isna(empleos_activos_5) or pd.isna(sobrev_po):
                        valor_actual_po = np.nan
                    else:
                        valor_actual_po = empleos_activos_5 - sobrev_po
                        if valor_actual_po < 0:
                            valor_actual_po = 0.0
                else:
                    valor_actual_po *= tasa_po

                df_proyeccion_mrt.loc[anio, 'Número de empleos muertos x≥0'] = valor_actual_po

        
        base_activos = (df_activos_completo.set_index('Año')
                            if 'Año' in df_activos_completo.columns
                            else df_activos_completo)

        for anio in range(2019, 2023):
            if mostrar_unidades:
                activos_1 = (float(base_activos.loc[anio - 1, 'Número de Negocios'])
                            if (anio - 1) in base_activos.index else np.nan)
                
                sobrev = (float(df_proyeccion_mrt.loc[anio, 'Sobrevivientes ≥5 en el año t'])
                        if ('Sobrevivientes ≥5 en el año t' in df_proyeccion_mrt.columns and anio in df_proyeccion_mrt.index)
                        else np.nan)
                if pd.isna(activos_1) or pd.isna(sobrev):
                    valor_actual_ue = np.nan
                else:
                    valor_actual_ue = activos_1 - sobrev
                    if valor_actual_ue < 0:
                        valor_actual_ue = 0.0
                df_proyeccion_mrt.loc[anio, 'Número de negocios muertos x≥0'] = valor_actual_ue

            if mostrar_personal:
                empleos_activos_1 = (float(base_activos.loc[anio - 1, 'Personal Ocupado'])
                                    if (anio - 1) in base_activos.index else np.nan)
                sobrev_po = (float(df_proyeccion_mrt.loc[anio, 'Empleos sobrevivientes ≥5 en el año t'])
                            if ('Empleos sobrevivientes ≥5 en el año t' in df_proyeccion_mrt.columns and anio in df_proyeccion_mrt.index)
                            else np.nan)

                if pd.isna(empleos_activos_1) or pd.isna(sobrev_po):
                    valor_actual_po = np.nan
                else:
                    valor_actual_po = empleos_activos_1 - sobrev_po
                    if valor_actual_po < 0:
                        valor_actual_po = 0.0
                df_proyeccion_mrt.loc[anio, 'Número de empleos muertos x≥0'] = valor_actual_po

    # Añadir 2023 muertos desde tabla_mrt
    if mostrar_unidades:
        try:
            df_proyeccion_mrt.loc[2023, 'Número de negocios muertos x≥0'] = float(
                tabla_mrt.loc['UE', 'CE 2023']
            )
        except Exception as e:
            st.warning(f"No se pudo asignar UE muertos 2023 desde 'tabla_mrt': {e}")

    if mostrar_personal:
        try:
            df_proyeccion_mrt.loc[2023, 'Número de empleos muertos x≥0'] = float(
                tabla_mrt.loc['PO', 'CE 2023']
            )
        except Exception as e:
            st.warning(f"No se pudo asignar PO muertos 2023 desde 'tabla_mrt': {e}")



    # --- CÁLCULO DE TASAS DE MORTALIDAD (%) ---    
    
    # Asegura índice Año
    if 'Año' in df_proyeccion_mrt.columns and df_proyeccion_mrt.index.name != 'Año':
        df_proyeccion_mrt = df_proyeccion_mrt.set_index('Año')

    for anio in df_proyeccion_mrt.index:
        if mostrar_unidades and 'Número de negocios muertos x≥0' in df_proyeccion_mrt.columns:
            s_activos = df_activos_completo.set_index('Año')['Número de Negocios']
            muertos_ue = df_proyeccion_mrt.at[anio, 'Número de negocios muertos x≥0']
            activos = s_activos.get(anio-1, np.nan)
            if pd.notna(muertos_ue) and pd.notna(activos) and activos > 0:
                df_proyeccion_mrt.at[anio, 'Tasa de mortalidad (%)'] = round((muertos_ue / activos) * 100, 2)

        if mostrar_personal and 'Número de empleos muertos x≥0' in df_proyeccion_mrt.columns:
            s_empleos = df_activos_completo.set_index('Año')['Personal Ocupado']
            muertos_po = df_proyeccion_mrt.at[anio, 'Número de empleos muertos x≥0']
            empleos = s_empleos.get(anio-1, np.nan)
            if pd.notna(muertos_po) and pd.notna(empleos) and empleos > 0:
                df_proyeccion_mrt.at[anio, 'Tasa de mortalidad de los empleos (%)'] = round((muertos_po / empleos) * 100, 2)
    

    # --- CÁLCULO DE TASAS DE CRECIMIENTO ANUAL DE LA NATALIDAD ---

    if mostrar_unidades and 'Tasa de crecimiento anual de la mortalidad (%)' not in df_proyeccion_mrt.columns:
        df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad (%)'] = None
    if mostrar_personal and 'Tasa de crecimiento anual de la mortalidad de los empleos (%)' not in df_proyeccion_mrt.columns:
        df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad de los empleos (%)'] = None

    
    if 'Año' in df_proyeccion_mrt.columns:
        df_proyeccion_mrt = df_proyeccion_mrt.sort_values('Año').reset_index(drop=True)


    for i in range(1, len(df_proyeccion_mrt)):
        if mostrar_unidades:
            ue_actual = df_proyeccion_mrt.iloc[i][ 'Número de negocios muertos x≥0']
            ue_anterior = df_proyeccion_mrt.iloc[i-1]['Número de negocios muertos x≥0']
            if pd.notna(ue_anterior) and ue_anterior > 0:
                tasa_ue = ((ue_actual / ue_anterior) - 1) * 100
                if pd.isna(tasa_ue):
                    tasa_ue = 0.0
                df_proyeccion_mrt.iloc[i, df_proyeccion_mrt.columns.get_loc('Tasa de crecimiento anual de la mortalidad (%)')] = tasa_ue
            df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad (%)'] = \
            df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad (%)'].fillna(0)


        if mostrar_personal:
            po_actual = df_proyeccion_mrt.iloc[i]['Número de empleos muertos x≥0']
            po_anterior = df_proyeccion_mrt.iloc[i-1]['Número de empleos muertos x≥0']
            if pd.notna(po_anterior) and po_anterior > 0:
                tasa_po = ((po_actual / po_anterior) - 1) * 100
                df_proyeccion_mrt.iloc[i, df_proyeccion_mrt.columns.get_loc('Tasa de crecimiento anual de la mortalidad de los empleos (%)')] = tasa_po
            df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad de los empleos (%)'] = \
            df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad de los empleos (%)'].fillna(0)


    # Formatear las columnas a dos decimales con símbolo %
    if mostrar_unidades:
        df_proyeccion_mrt['Tasa de mortalidad (%)'] = df_proyeccion_mrt['Tasa de mortalidad (%)'].apply(
            lambda x: f"{x:,.2f}" if pd.notna(x) else None
        )
        df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad (%)'] = df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad (%)'].apply(
            lambda x: f"{x:,.2f}" if pd.notna(x) else None
        )
    if mostrar_personal:
        df_proyeccion_mrt['Tasa de mortalidad de los empleos (%)'] = df_proyeccion_mrt['Tasa de mortalidad de los empleos (%)'].apply(
            lambda x: f"{x:,.2f}" if pd.notna(x) else None
        )
        df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad de los empleos (%)'] = df_proyeccion_mrt['Tasa de crecimiento anual de la mortalidad de los empleos (%)'].apply(
            lambda x: f"{x:,.2f}" if pd.notna(x) else None
        )

    # Formato final para visualización
   
    # Ordenar por Año y restaurar como columna
    df_proyeccion_mrt = (
        df_proyeccion_mrt
        .sort_index()          # ordena por Año (índice)
        .reset_index()         # devuelve 'Año' como columna
        .rename(columns={'index': 'Año'})
    )

    # Asegurar tipos
    if 'Año' in df_proyeccion_mrt.columns:
        df_proyeccion_mrt['Año'] = df_proyeccion_mrt['Año'].astype(int)
    
    orden_columnas = [
        'Activos',
        'Sobrevivientes ≥5 en el año t',
        'Número de negocios muertos x≥0',
        'Tasa de mortalidad (%)',
        'Tasa de crecimiento anual de la mortalidad (%)',
        'Empleos activos',
        'Empleos sobrevivientes ≥5 en el año t',
        'Número de empleos muertos x≥0',
        'Tasa de mortalidad de los empleos (%)',
        'Tasa de crecimiento anual de la mortalidad de los empleos (%)'
    ]
    orden_columnas_ue = [
        'Activos',
        'Sobrevivientes ≥5 en el año t',
        'Número de negocios muertos x≥0',
        'Tasa de mortalidad (%)',
        'Tasa de crecimiento anual de la mortalidad (%)'        
    ]
    orden_columnas_po = [
        'Empleos activos',
        'Empleos sobrevivientes ≥5 en el año t',
        'Número de empleos muertos x≥0',
        'Tasa de mortalidad de los empleos (%)',
        'Tasa de crecimiento anual de la mortalidad de los empleos (%)'
    ]
    
    for col in orden_columnas:
        if col not in df_proyeccion_mrt.columns:
            df_proyeccion_mrt[col] = pd.NA

    if mostrar_unidades and mostrar_personal:
        columnas_finales = ['Año'] + [c for c in orden_columnas if c in df_proyeccion_mrt.columns]
    elif mostrar_unidades:
            columnas_finales = ['Año'] + [c for c in orden_columnas_ue if c in df_proyeccion_mrt.columns]
    elif mostrar_personal:
            columnas_finales = ['Año'] + [c for c in orden_columnas_po if c in df_proyeccion_mrt.columns]

    df_proyeccion_mrt = df_proyeccion_mrt[columnas_finales]
    
    
    df_proyeccion_mrt_formato = df_proyeccion_mrt.copy()
        
    if mostrar_unidades:
        df_proyeccion_mrt_formato.sort_values(by='Año', inplace=True)
        df_proyeccion_mrt_formato.drop_duplicates(subset='Año', keep='last', inplace=True)
        df_proyeccion_mrt_formato['Activos'] = round(df_proyeccion_mrt_formato['Activos'].astype(float),0)
        df_proyeccion_mrt_formato['Activos'] = df_proyeccion_mrt_formato['Activos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_mrt_formato['Sobrevivientes ≥5 en el año t'] = round(df_proyeccion_mrt_formato['Sobrevivientes ≥5 en el año t'].astype(float),0)
        df_proyeccion_mrt_formato['Sobrevivientes ≥5 en el año t'] = df_proyeccion_mrt_formato['Sobrevivientes ≥5 en el año t'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_mrt_formato['Número de negocios muertos x≥0'] = round(df_proyeccion_mrt_formato['Número de negocios muertos x≥0'].astype(float),0)
        df_proyeccion_mrt_formato['Número de negocios muertos x≥0'] = df_proyeccion_mrt_formato['Número de negocios muertos x≥0'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_mrt_formato.reset_index(drop=True, inplace=True)

    if mostrar_personal:
        df_proyeccion_mrt_formato.sort_values(by='Año', inplace=True)
        df_proyeccion_mrt_formato.drop_duplicates(subset='Año', keep='last', inplace=True)
        df_proyeccion_mrt_formato['Empleos activos'] = round(df_proyeccion_mrt_formato['Empleos activos'].astype(float),0)
        df_proyeccion_mrt_formato['Empleos activos'] = df_proyeccion_mrt_formato['Empleos activos'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_mrt_formato['Empleos sobrevivientes ≥5 en el año t'] = round(df_proyeccion_mrt_formato['Empleos sobrevivientes ≥5 en el año t'].astype(float),0)
        df_proyeccion_mrt_formato['Empleos sobrevivientes ≥5 en el año t'] = df_proyeccion_mrt_formato['Empleos sobrevivientes ≥5 en el año t'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_mrt_formato['Número de empleos muertos x≥0'] = round(df_proyeccion_mrt_formato['Número de empleos muertos x≥0'].astype(float),0)
        df_proyeccion_mrt_formato['Número de empleos muertos x≥0'] = df_proyeccion_mrt_formato['Número de empleos muertos x≥0'].map(lambda x: f"{int(x):,}" if isinstance(x, (int, float)) and x != '' else '')
        df_proyeccion_mrt_formato.reset_index(drop=True, inplace=True)
   
     
    col1, col2 = st.columns([40, 60])
    with col1:
        # Mostrar el DataFrame final con la nueva columna
        st.write(f"Muertes en {entidad.capitalize()}, pertenecientes al sector {sector.capitalize()} con {personal_seleccionado}")
        st.dataframe(df_proyeccion_mrt_formato, use_container_width=True, height=1130)

    with col2:
        st.write("Visualización de Comportamiento Anual")

        # 1. Gráfico
        columnas = []
        if mostrar_unidades:
            columnas.append('Número de negocios muertos x≥0')
        if mostrar_personal:
            columnas.append('Número de empleos muertos x≥0')

        if columnas:
            fig_negocios = make_subplots(specs=[[{"secondary_y": True}]])
            for i, col in enumerate(columnas):
                es_secundario = i > 0  # La segunda métrica (si existe) va en el eje secundario
                color_trazado = '#08989C' if col == 'Número de negocios muertos x≥0' else '#003057'
                fig_negocios.add_trace(
                    go.Scatter(
                        x=df_proyeccion_mrt_formato['Año'],
                        y=df_proyeccion_mrt_formato[col],                        
                        name=col,
                        mode='lines+markers',
                        line=dict(color=color_trazado),
                        marker=dict(color=color_trazado),
                        hovertemplate='%{y:,.0f}<br>Año: %{x}'
                    ),
                    secondary_y=es_secundario
                )
            fig_negocios.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Número de muertes en la entidad {entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                    x=0.5,
                    xanchor='center',
                    y=-0.2,
                    yanchor='top',
                    orientation='h'
                ),
                xaxis_title = 'Año',
                margin={'t': 110}
            )
        if mostrar_unidades:
            fig_negocios.update_yaxes(title_text='<b>UNIDADES ECONÓMICAS</b>', title_font=dict(size=13), secondary_y=False)
        if mostrar_personal:
            fig_negocios.update_yaxes(title_text='<b>EMPLEOS</b>', title_font=dict(size=13), secondary_y=False)
        if mostrar_unidades and mostrar_personal:
            fig_negocios.update_yaxes(title_text='<b>UNIDADES ECONÓMICAS</b>', title_font=dict(size=13), secondary_y=False)
            fig_negocios.update_yaxes(title_text='<b>EMPLEOS</b>', title_font=dict(size=13), secondary_y=True)
        with st.container(border=True):
            st.plotly_chart(fig_negocios, use_container_width=True)

        # 2. Gráfico
            columnas = []
            if mostrar_unidades:
                columnas.append('Tasa de mortalidad (%)')
            if mostrar_personal:
                columnas.append('Tasa de mortalidad de los empleos (%)')

            if columnas:
                fig_negocios_tasas = make_subplots()
                for i, col in enumerate(columnas):                
                    color_trazado = '#08989C' if col == 'Tasa de mortalidad (%)' else '#003057'
                    fig_negocios_tasas.add_trace(
                        go.Scatter(
                            x=df_proyeccion_mrt['Año'],
                            y=df_proyeccion_mrt[col],                        
                            name=col,
                            mode='lines+markers',
                            line=dict(color=color_trazado),
                            marker=dict(color=color_trazado),
                            hovertemplate='%{y:,.2f}<br>Año: %{x}'
                        )
                    )
                        
            fig_negocios_tasas.update_layout(
                hovermode="x unified",
                title={
                    'text': f"Tasa de mortalidad anual en la entidad de {entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                    'font': {'size': 14},
                    'automargin': False
                },
                legend=dict(
                        x=0.5,
                        xanchor='center',
                        y=-0.2,
                        yanchor='top',
                        orientation='h'
                    ),
                xaxis_title = 'Año',
                margin={'t': 110}
            )
            fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE MORTALIDAD</b>', title_font=dict(size=13))    
        with st.container(border=True):
            st.plotly_chart(fig_negocios_tasas, use_container_width=True)            


        # 3. Gráfico
        columnas = []
        if mostrar_unidades:
            columnas.append('Tasa de crecimiento anual de la mortalidad (%)')
        if mostrar_personal:
            columnas.append('Tasa de crecimiento anual de la mortalidad de los empleos (%)')

        if columnas:
            fig_negocios_tasas = make_subplots()
            for i, col in enumerate(columnas):                
                color_trazado = '#08989C' if col == 'Tasa de crecimiento anual de la mortalidad (%)' else '#003057'
                fig_negocios_tasas.add_trace(
                    go.Scatter(
                        x=df_proyeccion_mrt['Año'],
                        y=df_proyeccion_mrt[col],                        
                        name=col,
                        mode='lines+markers',
                        line=dict(color=color_trazado),
                        marker=dict(color=color_trazado),
                        hovertemplate='%{y:,.2f}<br>Año: %{x}'
                    )
                )
                    
        fig_negocios_tasas.update_layout(
            hovermode="x unified",
            title={
                'text': f"Tasa de crecimiento anual de la mortalidad en la entidad de {entidad.title()}, pertenecientes al sector {sector.title()}, con {personal_seleccionado.lower()}",
                'font': {'size': 14},
                'automargin': False
            },
            legend=dict(
                    x=0.5,
                    xanchor='center',
                    y=-0.2,
                    yanchor='top',
                    orientation='h'
                ),
            xaxis_title = 'Año',
            margin={'t': 110}
        )
        fig_negocios_tasas.update_yaxes(title_text='<b>TASA DE CRECIMIENTO</b>', title_font=dict(size=13))    
        with st.container(border=True):
            st.plotly_chart(fig_negocios_tasas, use_container_width=True)         

        st.markdown('<small>Fuente: Censos Económicos 1989-2024<small>', unsafe_allow_html=True) 
