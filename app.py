import pandas as pd
import streamlit as st
from PIL import Image
import re
import plotly.express as px

img = Image.open('inegi.png')

st.set_page_config(page_title='Demografía de Negocios', page_icon=img, layout='wide')

st.title('Análisis Interactivo Censos Económicos')

# --- CARGA Y PROCESAMIENTO DE DATOS PRINCIPALES ---
@st.cache_data
def cargar_datos():
    """Carga y unifica todos los archivos CSV de censos con su censo correspondiente."""
    
    # Mapeo de archivos a años de censo
    mapeo_archivos = {
        'NAC_UE_POT_SEC_1.csv': 1989, 'NAC_UE_POT_SEC_2.csv': 1994,
        'NAC_UE_POT_SEC_3.csv': 1999, 'NAC_UE_POT_SEC_4.csv': 2004,
        'NAC_UE_POT_SEC_5.csv': 2009, 'NAC_UE_POT_SEC_6.csv': 2014,
        'NAC_UE_POT_SEC_7.csv': 2019,
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
            
            df_temp = pd.read_csv(archivo, encoding='latin1', sep=separator)
            
            df_temp.columns = [col.upper().strip().replace(' ', '_') for col in df_temp.columns]
            
            df_temp.rename(columns={
                'ENTIDAD': 'entidad', 'SECTOR': 'sector',
                'TAMAÑO': 'personal_ocupado_estrato', 'UNIDADES_ECONÓMICAS': 'unidades_economicas',
                'CONTEO_E17': 'unidades_economicas', 'AÑO': 'generacion',
                'G111A': 'generacion', 'DESC_SEC': 'sector'
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
    df_unificado['unidades_economicas'] = pd.to_numeric(df_unificado['unidades_economicas'], errors='coerce').fillna(0)
    df_unificado['personal_ocupado_estrato'] = pd.to_numeric(df_unificado['personal_ocupado_estrato'], errors='coerce')
    df_unificado['generacion'] = pd.to_numeric(df_unificado['generacion'], errors='coerce').fillna(0).astype(int)

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
st.header("Filtros")

col1, col2, col3 = st.columns(3)

# Inicializa la variable personal_seleccionado para evitar errores
personal_seleccionado = None

with col1:
    entidad = st.selectbox(
        'Selecciona la Entidad Federativa',
        ['NACIONAL','AGUASCALIENTES','BAJA CALIFORNIA','BAJA CALIFORNIA SUR','CAMPECHE','COAHUILA DE ZARAGOZA','COLIMA','CHIAPAS','CHIHUAHUA','CIUDAD DE MEXICO','DURANGO','GUANAJUATO','GUERRERO','HIDALGO','JALISCO','MEXICO','MICHOACAN DE OCAMPO','MORELOS','NAYARIT','NUEVO LEON','OAXACA','PUEBLA','QUERETARO','QUINTANA ROO','SAN LUIS POTOSI','SINALOA','SONORA','TABASCO','TAMAULIPAS','TLAXCALA','VERACRUZ DE IGNACIO DE LA LLAVE','YUCATAN','ZACATECAS']
    )

with col2:
    sector = st.selectbox(
        'Selecciona el Sector',
        ['TODOS LOS SECTORES','COMERCIO','MANUFACTURAS','OTROS SECTORES','SERVICIOS PRIVADOS NO FINANCIEROS']
    )

with col3:
    if entidad == 'NACIONAL' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101-250 Personas ocupadas)','TP10(251 y más Personas ocupadas)']
        )

    elif entidad == 'NACIONAL' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51 y más Personas ocupadas)']
        )

    elif entidad == 'NACIONAL' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31 y más Personas ocupadas)']
        )

    elif entidad == 'NACIONAL' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31 y más Personas ocupadas)']
        )
        
    elif entidad == 'NACIONAL' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101 y más Personas ocupadas)']
        )

    #AGUASCALIENTES
    
    elif entidad == 'AGUASCALIENTES' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'AGUASCALIENTES' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'AGUASCALIENTES' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'AGUASCALIENTES' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )
        
    elif entidad == 'AGUASCALIENTES' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS']
        )

    #BAJA CALIFORNIA

    elif entidad == 'BAJA CALIFORNIA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101 y más Personas ocupadas)']
        )

    elif entidad == 'BAJA CALIFORNIA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'BAJA CALIFORNIA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'BAJA CALIFORNIA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'BAJA CALIFORNIA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    #BAJA CALIFORNIA SUR

    elif entidad == 'BAJA CALIFORNIA SUR' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'BAJA CALIFORNIA SUR' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS']
        )

    elif entidad == 'BAJA CALIFORNIA SUR' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'BAJA CALIFORNIA SUR' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )
        
    elif entidad == 'BAJA CALIFORNIA SUR' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS']
        )

    #CAMPECHE

    elif entidad == 'CAMPECHE' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'CAMPECHE' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'CAMPECHE' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'CAMPECHE' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )
        
    elif entidad == 'CAMPECHE' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )
        
    #COAHUILA DE ZARAGOZA

    elif entidad == 'COAHUILA DE ZARAGOZA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51 y más Personas ocupadas)']
        )

    elif entidad == 'COAHUILA DE ZARAGOZA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'COAHUILA DE ZARAGOZA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'COAHUILA DE ZARAGOZA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'COAHUILA DE ZARAGOZA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #COLIMA

    elif entidad == 'COLIMA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'COLIMA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    elif entidad == 'COLIMA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'COLIMA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )
        
    elif entidad == 'COLIMA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS']
        )
        
    #CHIAPAS

    elif entidad == 'CHIAPAS' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'CHIAPAS' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    elif entidad == 'CHIAPAS' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'CHIAPAS' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'CHIAPAS' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #CHIHUAHUA

    elif entidad == 'CHIHUAHUA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21 y más Personas ocupadas)']
        )

    elif entidad == 'CHIHUAHUA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'CHIHUAHUA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'CHIHUAHUA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'CHIHUAHUA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )
        
    #CIUDAD DE MEXICO

    elif entidad == 'CIUDAD DE MEXICO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101-250 Personas ocupadas)','TP10(251 y más Personas ocupadas)']
        )

    elif entidad == 'CIUDAD DE MEXICO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51 y más Personas ocupadas)']
        )

    elif entidad == 'CIUDAD DE MEXICO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101 y más Personas ocupadas)']
        )

    elif entidad == 'CIUDAD DE MEXICO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101 y más Personas ocupadas)']
        )
        
    elif entidad == 'CIUDAD DE MEXICO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #DURANGO

    elif entidad == 'DURANGO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'DURANGO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'DURANGO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'DURANGO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'DURANGO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #GUANAJUATO

    elif entidad == 'GUANAJUATO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101 y más Personas ocupadas)']
        )

    elif entidad == 'GUANAJUATO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'GUANAJUATO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'GUANAJUATO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'GUANAJUATO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #GUERRERO

    elif entidad == 'GUERRERO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'GUERRERO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'GUERRERO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'GUERRERO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'GUERRERO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #GUANAJUATO

    elif entidad == 'GUANAJUATO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101 y más Personas ocupadas)']
        )

    elif entidad == 'GUANAJUATO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'GUANAJUATO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'GUANAJUATO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'GUANAJUATO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #HIDALGO

    elif entidad == 'HIDALGO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'HIDALGO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'HIDALGO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'HIDALGO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'HIDALGO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #JALISCO

    elif entidad == 'JALISCO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101-250 Personas ocupadas)','TP10(251 y más Personas ocupadas)']
        )

    elif entidad == 'JALISCO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31 y más Personas ocupadas)']
        )

    elif entidad == 'JALISCO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51 y más Personas ocupadas)']
        )

    elif entidad == 'JALISCO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31 y más Personas ocupadas)']
        )
        
    elif entidad == 'JALISCO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    #MEXICO

    elif entidad == 'MEXICO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101-250 Personas ocupadas)','TP10(251 y más Personas ocupadas)']
        )

    elif entidad == 'MEXICO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101 y más Personas ocupadas)']
        )

    elif entidad == 'MEXICO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31 y más Personas ocupadas)']
        )

    elif entidad == 'MEXICO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31 y más Personas ocupadas)']
        )
        
    elif entidad == 'MEXICO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    #MICHOACAN DE OCAMPO

    elif entidad == 'MICHOACAN DE OCAMPO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31 y más Personas ocupadas)']
        )

    elif entidad == 'MICHOACAN DE OCAMPO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'MICHOACAN DE OCAMPO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'MICHOACAN DE OCAMPO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'MICHOACAN DE OCAMPO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    #MORELOS

    elif entidad == 'MORELOS' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'MORELOS' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    elif entidad == 'MORELOS' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'MORELOS' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'MORELOS' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #NAYARIT

    elif entidad == 'NAYARIT' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'NAYARIT' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'NAYARIT' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'NAYARIT' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'NAYARIT' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #NUEVO LEON

    elif entidad == 'NUEVO LEON' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101-250 Personas ocupadas)','TP10(251 y más Personas ocupadas)']
        )

    elif entidad == 'NUEVO LEON' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101 y más Personas ocupadas)']
        )

    elif entidad == 'NUEVO LEON' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51 y más Personas ocupadas)']
        )

    elif entidad == 'NUEVO LEON' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51 y más Personas ocupadas)']
        )
        
    elif entidad == 'NUEVO LEON' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    #OAXACA

    elif entidad == 'OAXACA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21 y más Personas ocupadas)']
        )

    elif entidad == 'OAXACA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'OAXACA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'OAXACA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'OAXACA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    #PUEBLA

    elif entidad == 'PUEBLA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31 y más Personas ocupadas)']
        )

    elif entidad == 'PUEBLA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'PUEBLA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'PUEBLA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21 y más Personas ocupadas)']
        )
        
    elif entidad == 'PUEBLA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    #QUERÉTARO

    elif entidad == 'QUERÉTARO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'QUERÉTARO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'QUERÉTARO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'QUERÉTARO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'QUERÉTARO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #QUINTANA ROO

    elif entidad == 'QUINTANA ROO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'QUINTANA ROO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'QUINTANA ROO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'QUINTANA ROO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'QUINTANA ROO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS']
        )

    #SAN LUIS POTOSI

    elif entidad == 'SAN LUIS POTOSI' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'SAN LUIS POTOSI' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'SAN LUIS POTOSI' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'SAN LUIS POTOSI' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'SAN LUIS POTOSI' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #SINALOA

    elif entidad == 'SINALOA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21 y más Personas ocupadas)']
        )

    elif entidad == 'SINALOA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'SINALOA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'SINALOA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'SINALOA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    #SONORA

    elif entidad == 'SONORA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21 y más Personas ocupadas)']
        )

    elif entidad == 'SONORA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'SONORA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'SONORA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'SONORA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    #TABASCO

    elif entidad == 'TABASCO' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21 y más Personas ocupadas)']
        )

    elif entidad == 'TABASCO' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'TABASCO' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'TABASCO' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'TABASCO' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    #TAMAULIPAS

    elif entidad == 'TAMAULIPAS' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21 y más Personas ocupadas)']
        )

    elif entidad == 'TAMAULIPAS' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'TAMAULIPAS' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'TAMAULIPAS' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'TAMAULIPAS' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    #TLAXCALA

    elif entidad == 'TLAXCALA' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'TLAXCALA' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'TLAXCALA' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'TLAXCALA' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'TLAXCALA' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )

    #VERACRUZ DE IGNACIO DE LA LLAVE

    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21-30 Personas ocupadas)','TP07(31-50 Personas ocupadas)','TP08(51-100 Personas ocupadas)','TP09(101 y más Personas ocupadas)']
        )

    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21 y más Personas ocupadas)']
        )
        
    elif entidad == 'VERACRUZ DE IGNACIO DE LA LLAVE' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    #YUCATAN

    elif entidad == 'YUCATAN' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16-20 Personas ocupadas)','TP06(21 y más Personas ocupadas)']
        )

    elif entidad == 'YUCATAN' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'YUCATAN' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )

    elif entidad == 'YUCATAN' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11-15 Personas ocupadas)','TP05(16 y más Personas ocupadas)']
        )
        
    elif entidad == 'YUCATAN' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    #ZACATECAS

    elif entidad == 'ZACATECAS' and sector =='TODOS LOS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
        ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'ZACATECAS' and sector == 'MANUFACTURAS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6 y más Personas ocupadas)']
        )

    elif entidad == 'ZACATECAS' and sector == 'COMERCIO':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )

    elif entidad == 'ZACATECAS' and sector == 'SERVICIOS PRIVADOS NO FINANCIEROS':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3-5 Personas ocupadas)','TP03(6-10 Personas ocupadas)','TP04(11 y más Personas ocupadas)']
        )
        
    elif entidad == 'ZACATECAS' and sector == 'OTROS SECTORES':
        personal_seleccionado = st.selectbox(
            'Selecciona el tamaño de personal ocupado',
            ['CONCENTRADOS','TP01(0-2 Personas ocupadas)','TP02(3 y más Personas ocupadas)']
        )



# --- FIN DE SELECTBOXES ---

st.markdown("---")

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
    # Extraer el número del estrato TP
    match = re.search(r'TP(\d+)', personal_seleccionado)
    if match:
        estrato_seleccionado = int(match.group(1))

        if 'y más Personas ocupadas' in personal_seleccionado:
            # Filtrar por el estrato y todos los mayores
            df_final_filtrado = df_final_filtrado[df_final_filtrado['personal_ocupado_estrato'] >= estrato_seleccionado]
        else:
            # Filtrar solo por el estrato exacto
            df_final_filtrado = df_final_filtrado[df_final_filtrado['personal_ocupado_estrato'] == estrato_seleccionado]
    else:
        st.warning("No se pudo interpretar el formato del rango de personal ocupado. El filtro no se aplicará.")

# --- VISUALIZACIÓN DE LA TABLA SOLICITADA ---
st.subheader("Matriz de Unidades Económicas")

if df_final_filtrado.empty:
    st.warning("No se encontraron datos para la combinación de filtros seleccionada. Intenta con otras opciones.")
else:
    df_final_filtrado = df_final_filtrado[df_final_filtrado['generacion'] >= 1983]
    
    df_final_filtrado['generacion'] = pd.to_numeric(df_final_filtrado['generacion'], errors='coerce')
    df_final_filtrado.dropna(subset=['generacion'], inplace=True)
    df_final_filtrado['generacion'] = df_final_filtrado['generacion'].astype(int)

    tabla_pivote = pd.pivot_table(
        df_final_filtrado,
        values='unidades_economicas',
        index='generacion',
        columns='censo',
        aggfunc='sum',
        fill_value=0
    )

    tabla_pivote.index.name = 'Año de generación'
    tabla_pivote.columns = [f'Censo {col}' for col in tabla_pivote.columns]
    
    # Calcular el total antes de formatear
    tabla_pivote.loc[0000] = tabla_pivote.sum(axis=0)

    # Crear una copia para el formateo
    tabla_pivote_formato = tabla_pivote.copy()

    # Remplazar los ceros con una cadena vacía para que se vean en blanco
    tabla_pivote_formato = tabla_pivote_formato.replace(0, '')
    
    # Formatear los números con separadores de miles
    for col in tabla_pivote_formato.columns:
        # Formatear la fila 'TOTAL' primero
        #if 0000 in tabla_pivote_formato.index and tabla_pivote_formato.loc[0000, col] != '':
        #    tabla_pivote_formato.loc[0000, col] = f"{int(tabla_pivote_formato.loc[0000, col]):,.0f}"
        
        # Formatear el resto de las celdas
        #tabla_pivote_formato[col] = tabla_pivote_formato[col].apply(
        #   lambda x: f"{int(x):,.0f}" if isinstance(x, (int, float)) else x
        #)
        pass

    def format_numbers(x):
        if pd.isna(x) or x == '':
            return ''
        return f"{int(x):,.0f}"

    tabla_pivote_formato = tabla_pivote_formato.applymap(format_numbers)
    
    st.dataframe(tabla_pivote_formato, use_container_width=True)
    
  
    # --- CÁLCULO Y VISUALIZACIÓN DEL CRECIMIENTO DE UNIDADES ECONÓMICAS ---
    #st.subheader("Crecimiento de Unidades Económicas")

   # Obtener la fila de totales numéricos de la tabla original
    totales_numericos = tabla_pivote.loc[0000]
        
    # Inicializar la lista para los resultados
    resultados_crecimiento = []
    indices_crecimiento = []

    # Calcular el crecimiento para cada par de censos consecutivos
    for i in range(1, len(totales_numericos)):
        # Obtener los nombres completos de las columnas del Censo (Ej. 'Censo 1989')
        censo_actual_str = totales_numericos.index[i]
        censo_anterior_str = totales_numericos.index[i-1]
        
        # Extraer solo el año de las cadenas de texto 'Censo XXXX'
        try:
            anio_actual = int(censo_actual_str.split(' ')[-1])
            anio_anterior = int(censo_anterior_str.split(' ')[-1])
        except (ValueError, IndexError):
            # En caso de que el formato no sea el esperado, se usa el valor original
            # Esto maneja el caso de que la columna sea el año puro (1989, 1994...)
            anio_actual = int(censo_actual_str)
            anio_anterior = int(censo_anterior_str)

        total_actual = totales_numericos.iloc[i]
        total_anterior = totales_numericos.iloc[i-1]
        
        if total_anterior > 0:
            crecimiento = (total_actual / total_anterior)**0.2
            resultados_crecimiento.append(crecimiento)
            indices_crecimiento.append(f'{anio_anterior}-{anio_actual}')
        else:
            resultados_crecimiento.append(None)
            indices_crecimiento.append(f'{anio_anterior}-{anio_actual}')
    
    # Crear un DataFrame para la tabla de crecimiento
    df_crecimiento = pd.DataFrame(
        [resultados_crecimiento], 
        columns=indices_crecimiento, 
        index=['Índice de crecimiento']
    )
    
    # Formatear la tabla de crecimiento a 4 decimales
    df_crecimiento = df_crecimiento.apply(lambda x: pd.to_numeric(x, errors='coerce').round(14))
    
    # Mostrar la nueva tabla
    #st.dataframe(df_crecimiento, use_container_width=True)



# --- PROYECCIÓN DE UNIDADES ECONÓMICAS ---
    st.markdown("---")
    st.subheader(f"Comportamiento anual del numero de unidades económicas activas en {entidad}, pertenecientes al sector {sector} con {personal_seleccionado}")
    
    
    # Obtener la lista de censos y valores
    censos_str = totales_numericos.index.tolist()
    
    # DataFrame para los resultados de la proyección
    df_proyeccion = pd.DataFrame(columns=['Año', 'Número de Negocios'])

    # Iterar sobre los periodos censales para la proyección
    for i in range(len(censos_str) - 1):
        censo_actual_str = censos_str[i]
        censo_siguiente_str = censos_str[i+1]
        
        # Extraer el año y el valor del censo
        anio_actual = int(censo_actual_str.split(' ')[-1])
        valor_actual = totales_numericos.loc[censo_actual_str]
        
        anio_siguiente = int(censo_siguiente_str.split(' ')[-1])
        valor_siguiente = totales_numericos.loc[censo_siguiente_str]
        
        # Obtener la tasa de crecimiento para el período
        tasa_anual = df_crecimiento.loc['Índice de crecimiento', f'{anio_actual}-{anio_siguiente}']

        # Si es el primer periodo, el año de inicio es el anterior al censo actual
        if i == 0:
            anio_inicio_proyeccion = anio_actual - 1
            valor_base = valor_actual
        else:
            # Para los demás periodos, el año de inicio es el anterior al siguiente censo
            anio_inicio_proyeccion = anio_actual - 1
            valor_base = valor_actual # El valor base para el inicio del periodo es el valor del Censo anterior
        
        # Agregar el año de inicio de la proyección con su valor base
        df_proyeccion.loc[len(df_proyeccion)] = [anio_inicio_proyeccion, valor_base]

        # Proyectar los años intermedios hasta el siguiente censo
        valor_proyectado = valor_base
        for anio in range(anio_inicio_proyeccion + 1, anio_siguiente):
            valor_proyectado *= tasa_anual
            df_proyeccion.loc[len(df_proyeccion)] = [anio, valor_proyectado]

    # Añadir el último año del censo (2019) y el año anterior (2018) con el mismo valor
    valor_ultimo_censo = totales_numericos.loc[censos_str[-1]]
    df_proyeccion.loc[len(df_proyeccion)] = [2018, valor_ultimo_censo]
    df_proyeccion.loc[len(df_proyeccion)] = [2019, valor_ultimo_censo]
    
    
    # --- Cálculo y adición de la proyección para 2019 ---
    
    # Obtener el valor de 2018 de la tabla de proyecciones
    valor_2018 = df_proyeccion.loc[df_proyeccion['Año'] == 2018, 'Número de Negocios'].iloc[0]
    
    # Calcular las tasas de crecimiento quinquenal
    tasas_quinquenales = []
    for i in range(len(censos_str) - 1):
        censo_actual_str = censos_str[i]
        censo_siguiente_str = censos_str[i+1]
        
        valor_actual = totales_numericos.loc[censo_actual_str]
        valor_siguiente = totales_numericos.loc[censo_siguiente_str]
        
        if valor_actual > 0:
            tasa_quinquenal = (valor_siguiente / valor_actual)
            tasas_quinquenales.append(tasa_quinquenal)
    
    # Calcular el promedio de las tasas quinquenales y elevarlo a 1/5
    if tasas_quinquenales:
        promedio_quinquenal = sum(tasas_quinquenales) / len(tasas_quinquenales)
        tasa_anual_promedio = promedio_quinquenal**(1/(6-1))
    else:
        tasa_anual_promedio = 1 # Valor por defecto si no hay tasas

#    st.write(f"Tasa anual de crecimiento promedio calculada: {tasa_anual_promedio:.4f}")

    # Obtener el valor de 2018 de la tabla de proyecciones
    valor_2018 = df_proyeccion.loc[df_proyeccion['Año'] == 2018, 'Número de Negocios'].iloc[0]
    
    # Calcular el valor proyectado para 2019
    valor_2019_proyectado = valor_2018 * tasa_anual_promedio
    
    # Añadir la fila de 2019 a la tabla
    df_proyeccion.loc[len(df_proyeccion)] = [2019, valor_2019_proyectado]

  # Limpiar y formatear el DataFrame de proyecciones
    df_proyeccion.sort_values(by='Año', inplace=True)
    df_proyeccion.drop_duplicates(subset='Año', keep='last', inplace=True)
    df_proyeccion['Año'] = df_proyeccion['Año'].astype(int)
    df_proyeccion['Número de Negocios'] = df_proyeccion['Número de Negocios'].round(0).astype(int)
    df_proyeccion.reset_index(drop=True, inplace=True)
   

# --- Carga y Procesamiento de Datos de Probabilidades ---
@st.cache_data
def cargar_probabilidades():
    """Carga y procesa el archivo de probabilidades."""
    try:
        df_prob = pd.read_csv('PROBABILIDADES.csv')
        df_prob.columns = [col.upper().strip().replace(' ', '_') for col in df_prob.columns]
        df_prob.rename(columns={'TAMAÑO': 'personal_ocupado_estrato'}, inplace=True)
        df_prob['ENTIDAD'] = df_prob['ENTIDAD'].str.upper().str.strip()
        df_prob['SECTOR'] = df_prob['SECTOR'].str.upper().str.strip()
        df_prob['personal_ocupado_estrato'] = df_prob['personal_ocupado_estrato'].str.upper().str.strip()
        return df_prob
    except FileNotFoundError:
        st.error("Archivo 'PROBABILIDADES.csv' no encontrado.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al leer 'PROBABILIDADES.csv': {e}")
        return pd.DataFrame()

df_probabilidades = cargar_probabilidades()

# Si el DataFrame de probabilidades está vacío, detenemos la ejecución
if df_probabilidades.empty:
    st.stop()

# --- Proyección de los años 2020, 2021 y 2022 ---

# Obtener el valor más reciente para la proyección (2019)
valor_2019 = df_proyeccion.loc[df_proyeccion['Año'] == 2019, 'Número de Negocios'].iloc[0]

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
            (df_probabilidades['personal_ocupado_estrato'] == personal_seleccionado.upper()) &
            (df_probabilidades['AÑO'] == anio_futuro)
        ]

        if not tasas.empty:
            tasa_supervivencia = tasas['SOBREVIVIENTES'].iloc[0]
            tasa_nacimientos = tasas['NACIMIENTOS'].iloc[0]
            
            # Calcular el factor de crecimiento (supervivencia + nacimientos)
            factor_crecimiento = tasa_supervivencia + tasa_nacimientos
            
            # Proyectar el valor del año anterior
            if anio_futuro == 2020:
                valor_proyectado = valor_2019 * factor_crecimiento
            elif anio_futuro == 2021:
                valor_proyectado = valor_2019 * factor_crecimiento
            else:
                valor_proyectado = valor_2019 * factor_crecimiento

            proyecciones_futuras[anio_futuro] = valor_proyectado

        else:
            st.warning(f"No se encontraron datos en 'PROBABILIDADES.csv' para {entidad}, {sector}, {personal_seleccionado} en el año {anio_futuro}.")
            proyecciones_futuras[anio_futuro] = None

    except IndexError:
        st.error(f"Error al obtener tasas para el año {anio_futuro}. Revisa que las columnas 'SOBREVIVIENTES' y 'NACIMIENTOS' existan y contengan valores válidos.")
        proyecciones_futuras[anio_futuro] = None

# Agregar las proyecciones al DataFrame principal
if proyecciones_futuras:
    df_proyeccion_futura = pd.DataFrame(proyecciones_futuras.items(), columns=['Año', 'Número de Negocios'])
    df_proyeccion = pd.concat([df_proyeccion, df_proyeccion_futura], ignore_index=True)

# Limpiar y formatear el DataFrame de proyecciones final
df_proyeccion.sort_values(by='Año', inplace=True)
df_proyeccion.drop_duplicates(subset='Año', keep='last', inplace=True)
df_proyeccion['Año'] = df_proyeccion['Año'].astype(int)
df_proyeccion['Número de Negocios'] = df_proyeccion['Número de Negocios'].round(0).astype(int)
df_proyeccion.reset_index(drop=True, inplace=True)

# Inicializar la columna para evitar errores
df_proyeccion['Tasa de crecimiento anual'] = None

# Calcular la tasa de crecimiento para cada año
for i in range(1, len(df_proyeccion)):
    ue_actual = df_proyeccion.loc[i, 'Número de Negocios']
    ue_anterior = df_proyeccion.loc[i - 1, 'Número de Negocios']
    
    if ue_anterior > 0:
        tasa = ((ue_actual / ue_anterior) - 1) * 100
        df_proyeccion.loc[i, 'Tasa de crecimiento anual'] = tasa

# Formatear la nueva columna a dos decimales, excepto la primera fila que no tiene tasa
df_proyeccion['Tasa de crecimiento anual'] = df_proyeccion['Tasa de crecimiento anual'].apply(
    lambda x: f"{x:,.2f}%" if pd.notna(x) else None
)

# Remplazar los ceros por guiones para una mejor visualización en la tabla
df_proyeccion.replace(0, '-')

# Mostrar el DataFrame final con la nueva columna
st.dataframe(df_proyeccion, use_container_width=True)







# --- VISUALIZACIÓN DE GRÁFICOS INTERACTIVOS CON PLOTLY ---
st.markdown("---")
st.subheader("Visualización de Comportamiento Anual")

col1, col2 = st.columns(2)

with col1:
# 1. Gráfico de Número de Negocios
    fig_negocios = px.line(
        df_proyeccion, 
        x='Año', 
        y='Número de Negocios', 
        title=f"Número de Unidades Económicas Activas: {entidad.title()}, {sector.title()}, {personal_seleccionado}",
        markers=True,
        labels={'Año': 'Año', 'Número de Negocios': 'Número de Negocios'}
    )
    fig_negocios.update_traces(hovertemplate='<b>Año:</b> %{x}<br><b>Negocios:</b> %{y:,.0f}')
    fig_negocios.update_layout(hovermode="x unified")
    st.plotly_chart(fig_negocios, use_container_width=True)

with col2:
# 2. Gráfico de Tasa de Crecimiento Anual
    df_crecimiento_plot = df_proyeccion.copy()
    df_crecimiento_plot['Tasa de crecimiento anual'] = pd.to_numeric(
        df_crecimiento_plot['Tasa de crecimiento anual'].str.rstrip('%').str.replace(',', ''), 
        errors='coerce'
    )
    
    fig_crecimiento = px.line(
        df_crecimiento_plot, 
        x='Año', 
        y='Tasa de crecimiento anual', 
        title=f"Tasa de Crecimiento Anual: {entidad.title()}, {sector.title()}, {personal_seleccionado}",
        markers=True,
        labels={'Año': 'Año', 'Tasa de crecimiento anual': 'Tasa de Crecimiento (%)'}
    )
    fig_crecimiento.update_traces(hovertemplate='<b>Año:</b> %{x}<br><b>Crecimiento:</b> %{y:.2f}%')
    fig_crecimiento.update_layout(hovermode="x unified")
    st.plotly_chart(fig_crecimiento, use_container_width=True)





