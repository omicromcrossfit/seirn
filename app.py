
# -*- coding: utf-8 -*-
"""
App optimizada (FULL) para Demografía de Negocios en Streamlit.
- Carga única cacheada de censos y probabilidades
- Pivotes/crecimientos/proyecciones cacheados por filtros
- Sidebar y tamaños dinámicos (estratos)
- Sección Población activa: serie anual y gráficos ligeros
- Sección Natalidad: tabla y proyecciones con factores entre censos
- Sección Supervivencia: tablas y proyecciones para 5,10,15,20,25 años con funciones genéricas
- Tables resumidas + descarga CSV para evitar cuelgues por payload

Requisitos mínimos sugeridos en requirements.txt (compatibles con Streamlit Cloud / 1.50.0):
    streamlit==1.50.0
    pandas==2.2.3
    numpy==2.4.2
    pillow==11.1.0
    plotly==6.3.0
"""

import os
import math
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# Configuración de página e ícono
# -----------------------------------------------------------------------------
_IMG_ICON_PATH = "inegi.png"
_icon = None
if os.path.exists(_IMG_ICON_PATH):
    try:
        from PIL import Image
        _icon = Image.open(_IMG_ICON_PATH)
    except Exception:
        _icon = "📊"
else:
    _icon = "📊"

st.set_page_config(page_title="Demografía de Negocios — FULL", page_icon=_icon, layout="wide")
st.title("Simulador de Indicadores Demográficos Económicos de México — Versión FULL")

# -----------------------------------------------------------------------------
# Constantes y mapas
# -----------------------------------------------------------------------------
MAPEO_ARCHIVOS: Dict[str, int] = {
    "NAC_UE_POT_SEC_1.csv": 1988,
    "NAC_UE_POT_SEC_2.csv": 1993,
    "NAC_UE_POT_SEC_3.csv": 1998,
    "NAC_UE_POT_SEC_4.csv": 2003,
    "NAC_UE_POT_SEC_5.csv": 2008,
    "NAC_UE_POT_SEC_6.csv": 2013,
    "NAC_UE_POT_SEC_7.csv": 2018,
    "NAC_UE_POT_SEC_8.csv": 2023,
}
PROBABILIDADES_FILE = "PROBABILIDADES.csv"

# Mapa etiqueta ↔︎ estrato
ESTRATO_ETIQUETA_A_NUM = {
    "0-2 Personas ocupadas": 1,
    "3-5 Personas ocupadas": 2,
    "6-10 Personas ocupadas": 3,
    "11-15 Personas ocupadas": 4,
    "16-20 Personas ocupadas": 5,
    "21-30 Personas ocupadas": 6,
    "31-50 Personas ocupadas": 7,
    "51-100 Personas ocupadas": 8,
    "101 y más Personas ocupadas": 9,
}
NUM_A_ETIQUETA_ESTRATO = {v: k for k, v in ESTRATO_ETIQUETA_A_NUM.items()}

TASAS_IMSS = [1.0184, 0.9681, 1.0558, 1.0319]  # 2019..2022

# -----------------------------------------------------------------------------
# Utilidades E/S
# -----------------------------------------------------------------------------

def _auto_sep_read_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, sep=None, engine="python", encoding="latin1", low_memory=False)
        return df
    except Exception:
        return pd.read_csv(path, sep=",", encoding="latin1", low_memory=False)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.upper().strip().replace(" ", "_") for c in df.columns]
    ren = {
        "ENTIDAD": "entidad",
        "SECTOR": "sector",
        "TAMAÑO": "personal_ocupado_estrato",
        "UNIDADES_ECONÓMICAS": "ue",
        "AÑO": "generacion",
        "PERSONAL_OCUPADO": "po",
    }
    for k, v in ren.items():
        if k in df.columns:
            df.rename(columns={k: v}, inplace=True)
    if "entidad" in df.columns:
        df["entidad"] = df["entidad"].astype(str).str.upper().str.strip()
    if "sector" in df.columns:
        df["sector"] = df["sector"].astype(str).str.upper().str.strip()
    for col in ("ue", "po"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    if "personal_ocupado_estrato" in df.columns:
        df["personal_ocupado_estrato"] = pd.to_numeric(df["personal_ocupado_estrato"], errors="coerce")
    if "generacion" in df.columns:
        df["generacion"] = pd.to_numeric(df["generacion"], errors="coerce").fillna(0).astype("int32")
    # Filas clave no nulas
    claves = [c for c in ("entidad", "sector", "personal_ocupado_estrato") if c in df.columns]
    if claves:
        df.dropna(subset=claves, inplace=True)
    return df


@st.cache_data(show_spinner=False)
def cargar_censos_unificado() -> pd.DataFrame:
    dfs = []
    for archivo, anio_censo in MAPEO_ARCHIVOS.items():
        if not os.path.exists(archivo):
            st.warning(f"Archivo no encontrado: {archivo}")
            continue
        dfi = _auto_sep_read_csv(archivo)
        dfi = _normalize_columns(dfi)
        dfi["censo"] = int(anio_censo)
        dfs.append(dfi)
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)
    # dtypes compactos
    for col in ("entidad", "sector"):
        if col in df.columns:
            df[col] = df[col].astype("category")
    if "personal_ocupado_estrato" in df.columns:
        df["personal_ocupado_estrato"] = df["personal_ocupado_estrato"].astype("Int8")
    if "censo" in df.columns:
        df["censo"] = df["censo"].astype("Int16")
    return df


@st.cache_data(show_spinner=False)
def cargar_probabilidades() -> pd.DataFrame:
    if not os.path.exists(PROBABILIDADES_FILE):
        st.warning("'PROBABILIDADES.csv' no encontrado. Algunas proyecciones no estarán disponibles.")
        return pd.DataFrame()
    df = _auto_sep_read_csv(PROBABILIDADES_FILE)
    df.columns = [c.upper().strip().replace(" ", "_") for c in df.columns]
    for col in ("ENTIDAD", "SECTOR", "TAMAÑO"):
        if col in df.columns:
            df[col] = df[col].astype(str).upper().str.strip()
    # Mantener AÑO si existe
    return df

# -----------------------------------------------------------------------------
# Sidebar y filtros
# -----------------------------------------------------------------------------

def opciones_sidebar(df: pd.DataFrame) -> Tuple[str, str, Optional[str], str]:
    entidades = ["NACIONAL"] + sorted(df["entidad"].cat.categories.tolist())
    sectores = ["TODOS LOS SECTORES"] + sorted(df["sector"].cat.categories.tolist())

    with st.sidebar:
        st.subheader("Filtros")
        entidad = st.selectbox("ENTIDAD FEDERATIVA:", entidades)
        sector = st.selectbox("SECTOR:", sectores)
        # pre-filtrado para obtener estratos válidos
        dff = df
        if entidad != "NACIONAL":
            dff = dff[dff["entidad"] == entidad]
        if sector != "TODOS LOS SECTORES":
            dff = dff[dff["sector"] == sector]
        estratos_disponibles = sorted(dff["personal_ocupado_estrato"].dropna().unique().tolist())
        etiquetas = ["CONCENTRADOS"] + [NUM_A_ETIQUETA_ESTRATO.get(int(e), f"Estrato {int(e)}") for e in estratos_disponibles]
        tam = st.selectbox("TAMAÑO:", etiquetas)

        st.subheader("Métricas")
        mostrar_ue = st.checkbox("Negocios", value=True, key="chk_ue")
        mostrar_po = st.checkbox("Empleos", value=False, key="chk_po")

        fenomeno = st.radio("Fenómeno demográfico:", ["Población activa", "Natalidad", "Supervivencia"], horizontal=False)

    return entidad, sector, tam, fenomeno


def aplicar_filtros(df: pd.DataFrame, entidad: str, sector: str, tam: Optional[str]) -> pd.DataFrame:
    dff = df
    if entidad != "NACIONAL":
        dff = dff[dff["entidad"] == entidad]
    if sector != "TODOS LOS SECTORES":
        dff = dff[dff["sector"] == sector]
    if tam and tam != "CONCENTRADOS":
        estrato = ESTRATO_ETIQUETA_A_NUM.get(tam)
        if estrato is not None:
            if "y más" in tam:
                dff = dff[dff["personal_ocupado_estrato"] >= estrato]
            else:
                dff = dff[dff["personal_ocupado_estrato"] == estrato]
    return dff

# -----------------------------------------------------------------------------
# Pivotes / factores / series (comunes)
# -----------------------------------------------------------------------------

@st.cache_data(show_spinner=False, max_entries=64)
def pivot_demografia(dff: pd.DataFrame, incluir_ue: bool, incluir_po: bool) -> pd.DataFrame:
    valores = []
    if incluir_ue:
        valores.append("ue")
    if incluir_po:
        valores.append("po")
    if not valores:
        return pd.DataFrame()
    agg = dff.groupby(["generacion", "censo"], observed=True)[valores].sum().unstack("censo", fill_value=0)
    frames = []
    for metrica in valores:
        sub = agg[metrica]
        sub.columns = [f"CE {int(c)} - {metrica.upper()}" for c in sub.columns]
        frames.append(sub)
    tabla = pd.concat(frames, axis=1)
    tabla.index.name = "Año"
    # fila totales (índice 0)
    totales = pd.DataFrame([tabla.sum(axis=0)], index=[0])
    tabla = pd.concat([tabla, totales])
    return tabla


@st.cache_data(show_spinner=False, max_entries=256)
def factores_crecimiento_desde_totales(tabla: pd.DataFrame, raiz: float = 0.2) -> Tuple[pd.DataFrame, List[str]]:
    """Factores entre pares de censos consecutivos usando totales (índice 0).
    raiz=0.2 equivale ~5 años (compatible con tu código original).
    """
    if tabla.empty:
        return pd.DataFrame(), []
    totales = tabla.loc[0]
    col_ue = [c for c in totales.index if c.endswith("UE")]
    col_po = [c for c in totales.index if c.endswith("PO")]

    def _calc(cols: List[str]) -> Tuple[List[float], List[str]]:
        if not cols:
            return [], []
        pares = sorted(cols, key=lambda x: int(x.split(" ")[1]))
        vals = totales[pares].to_numpy(dtype=float)
        prev = vals[:-1]
        nxt = vals[1:]
        with np.errstate(divide='ignore', invalid='ignore'):
            factores = np.where(prev > 0, (nxt / prev) ** raiz, np.nan)
        etiquetas = [f"{pares[i]}-{pares[i+1]}" for i in range(len(pares)-1)]
        return factores.tolist(), etiquetas

    f_ue, etiquetas = _calc(col_ue)
    f_po, _ = _calc(col_po)

    filas, idx = [], []
    if f_ue:
        filas.append(f_ue); idx.append("Unidades Económicas")
    if f_po:
        filas.append(f_po); idx.append("Personal Ocupado")
    if not filas:
        return pd.DataFrame(), etiquetas
    df = pd.DataFrame(filas, index=idx, columns=[e.replace("CE ", "").replace(" - UE", "").replace(" - PO", "") for e in etiquetas])
    return df, etiquetas


@st.cache_data(show_spinner=False, max_entries=128)
def serie_anual_desde_factores(tabla: pd.DataFrame, factores: pd.DataFrame) -> pd.DataFrame:
    """Construye serie anual (Año, UE/PO) interpolando entre censos con factores anuales
    hasta 2019 y extendiendo PO con tasas IMSS 2020–2022; fija 2023 con el total observado.
    """
    if tabla.empty:
        return pd.DataFrame(columns=["Año", "Número de Negocios", "Personal Ocupado"])  

    cols_ue = sorted([c for c in tabla.columns if c.endswith("UE")], key=lambda x: int(x.split(" ")[1]))
    cols_po = sorted([c for c in tabla.columns if c.endswith("PO")], key=lambda x: int(x.split(" ")[1]))
    tot = tabla.loc[0]
    registros = []

    # UE
    for i in range(max(0, len(cols_ue)-1)):
        a_i = int(cols_ue[i].split(" ")[1]); a_f = int(cols_ue[i+1].split(" ")[1])
        val = float(tot[cols_ue[i]])
        etiqueta = f"{a_i}-{a_f}"
        f = float(factores.loc["Unidades Económicas", etiqueta]) if (not factores.empty and "Unidades Económicas" in factores.index and etiqueta in factores.columns) else 1.0
        registros.append({"Año": a_i, "Número de Negocios": val})
        for a in range(a_i+1, min(a_f, 2019)):
            val *= f; registros.append({"Año": a, "Número de Negocios": val})

    # PO
    for i in range(max(0, len(cols_po)-1)):
        a_i = int(cols_po[i].split(" ")[1]); a_f = int(cols_po[i+1].split(" ")[1])
        val = float(tot[cols_po[i]])
        etiqueta = f"{a_i}-{a_f}"
        f = float(factores.loc["Personal Ocupado", etiqueta]) if (not factores.empty and "Personal Ocupado" in factores.index and etiqueta in factores.columns) else 1.0
        registros.append({"Año": a_i, "Personal Ocupado": val})
        for a in range(a_i+1, min(a_f, 2019)):
            val *= f; registros.append({"Año": a, "Personal Ocupado": val})

    df = pd.DataFrame(registros).groupby("Año", as_index=False).sum(numeric_only=True)

    # 2019 a partir de 2018
    if not df.empty and (df["Año"] == 2018).any():
        base_ue_2018 = float(df.loc[df["Año"]==2018, "Número de Negocios"].fillna(0).values[0]) if "Número de Negocios" in df.columns else np.nan
        base_po_2018 = float(df.loc[df["Año"]==2018, "Personal Ocupado"].fillna(0).values[0]) if "Personal Ocupado" in df.columns else np.nan
        # tasa promedio UE desde factores
        if not factores.empty and "Unidades Económicas" in factores.index:
            medias = pd.to_numeric(factores.loc["Unidades Económicas"], errors="coerce").dropna()
            tasa_ue = float(medias.mean()) if not medias.empty else 1.0
        else:
            tasa_ue = 1.0
        if not math.isnan(base_ue_2018):
            df = pd.concat([df, pd.DataFrame([{"Año": 2019, "Número de Negocios": base_ue_2018*tasa_ue}])], ignore_index=True)
        if not math.isnan(base_po_2018):
            df = pd.concat([df, pd.DataFrame([{"Año": 2019, "Personal Ocupado": base_po_2018*TASAS_IMSS[0]}])], ignore_index=True)
        # 2020–2022 para PO
        for idx, anio in enumerate([2020, 2021, 2022], start=1):
            prev = df[df["Año"]==anio-1].iloc[:1]
            if not prev.empty and "Personal Ocupado" in df.columns and not pd.isna(prev["Personal Ocupado"].values[0]):
                po_val = float(prev["Personal Ocupado"].values[0]) * TASAS_IMSS[idx]
                df = pd.concat([df, pd.DataFrame([{"Año": anio, "Personal Ocupado": po_val}])], ignore_index=True)

    # 2023 observación
    for m, suf in (("Número de Negocios", "UE"), ("Personal Ocupado", "PO")):
        cols = [c for c in tabla.columns if c.startswith("CE 2023") and c.endswith(suf)]
        if cols:
            val = float(tabla.loc[0, cols[0]])
            df = df[df["Año"] != 2023]
            df = pd.concat([df, pd.DataFrame([{"Año": 2023, m: val}])], ignore_index=True)

    if not df.empty:
        df.sort_values("Año", inplace=True)
        df.drop_duplicates("Año", keep="last", inplace=True)
        for c in ("Número de Negocios", "Personal Ocupado"):
            if c in df.columns:
                df[c] = df[c].astype("float64")
    return df

# -----------------------------------------------------------------------------
# NATALIDAD (optimizada)
# -----------------------------------------------------------------------------

@st.cache_data(show_spinner=False, max_entries=64)
def tabla_natalidad_desde_pivote(tabla_pivote: pd.DataFrame, pasos_fila: int = 5) -> pd.DataFrame:
    """Replica la lógica original: para cada censo CE yyyy, toma la fila k*pasos_fila
    (k empieza en 1 → 5,10,15,...) y extrae UE/PO de ese censo.
    Devuelve DataFrame con índice ['UE','PO'] y columnas 'CE yyyy'.
    """
    if tabla_pivote.empty:
        return pd.DataFrame()
    # columnas CE yyyy - UE/PO existentes
    censos = sorted(list({c.split(" - ")[0] for c in tabla_pivote.columns if c.startswith("CE ")}))
    datos = {"UE": {}, "PO": {}}
    for i, censo in enumerate(censos):
        fila = (i+1)*pasos_fila  # 5,10,15...
        if fila < len(tabla_pivote):
            col_ue = f"{censo} - UE"
            col_po = f"{censo} - PO"
            if col_ue in tabla_pivote.columns:
                datos["UE"][censo] = float(tabla_pivote.iloc[fila][col_ue])
            if col_po in tabla_pivote.columns:
                datos["PO"][censo] = float(tabla_pivote.iloc[fila][col_po])
        else:
            datos["UE"][censo] = np.nan
            datos["PO"][censo] = np.nan
    df = pd.DataFrame(datos).T
    return df


@st.cache_data(show_spinner=False, max_entries=128)
def crecimiento_entre_censos_natalidad(tabla_np: pd.DataFrame, raiz: float = 0.2) -> Tuple[pd.DataFrame, List[str]]:
    """Calcula factores entre censos para la tabla de natalidad (UE/PO), similar a totales."""
    if tabla_np.empty:
        return pd.DataFrame(), []
    cols = sorted(tabla_np.columns, key=lambda x: int(x.split(" ")[1]))
    def _calc(row: pd.Series):
        vals = row[cols].to_numpy(dtype=float)
        prev = vals[:-1]; nxt = vals[1:]
        with np.errstate(divide='ignore', invalid='ignore'):
            f = np.where(prev>0, (nxt/prev)**raiz, np.nan)
        return f
    etiquetas = [f"{cols[i]}-{cols[i+1]}" for i in range(len(cols)-1)]
    out = {}
    for idx in tabla_np.index:
        out[idx] = _calc(tabla_np.loc[idx]).tolist()
    df = pd.DataFrame(out, index=etiquetas).T
    df.columns = etiquetas
    return df, etiquetas


@st.cache_data(show_spinner=False, max_entries=128)
def proyeccion_natalidad(tabla_np: pd.DataFrame, crecimientos: pd.DataFrame, anio_tope: int = 2019) -> pd.DataFrame:
    """Proyecta serie anual de natalidad (UE/PO) entre censos con factores, hasta anio_tope.
    Devuelve DataFrame con columnas: Año, Número de Nacimientos, Nacimiento de Empleos.
    """
    if tabla_np.empty:
        return pd.DataFrame(columns=["Año", "Número de Nacimientos", "Nacimiento de Empleos"])  
    cols = sorted(tabla_np.columns, key=lambda x: int(x.split(" ")[1]))
    registros = []
    # UE
    if "UE" in tabla_np.index:
        for i in range(max(0, len(cols)-1)):
            a_i = int(cols[i].split(" ")[1]); a_f = int(cols[i+1].split(" ")[1])
            val = float(tabla_np.loc["UE", cols[i]])
            etiqueta = f"{cols[i]}-{cols[i+1]}"
            f = float(crecimientos.loc["UE", etiqueta]) if (not crecimientos.empty and etiqueta in crecimientos.columns and "UE" in crecimientos.index) else 1.0
            registros.append({"Año": a_i, "Número de Nacimientos": val})
            for a in range(a_i+1, min(a_f, anio_tope)):
                val *= f; registros.append({"Año": a, "Número de Nacimientos": val})
    # PO
    if "PO" in tabla_np.index:
        for i in range(max(0, len(cols)-1)):
            a_i = int(cols[i].split(" ")[1]); a_f = int(cols[i+1].split(" ")[1])
            val = float(tabla_np.loc["PO", cols[i]])
            etiqueta = f"{cols[i]}-{cols[i+1]}"
            f = float(crecimientos.loc["PO", etiqueta]) if (not crecimientos.empty and etiqueta in crecimientos.columns and "PO" in crecimientos.index) else 1.0
            registros.append({"Año": a_i, "Nacimiento de Empleos": val})
            for a in range(a_i+1, min(a_f, anio_tope)):
                val *= f; registros.append({"Año": a, "Nacimiento de Empleos": val})

    df = pd.DataFrame(registros).groupby("Año", as_index=False).sum(numeric_only=True)
    # Insertar 2023 (observación) si existe
    for idx, col, target in (("UE", f"CE 2023", "Número de Nacimientos"), ("PO", f"CE 2023", "Nacimiento de Empleos")):
        if idx in tabla_np.index and col in tabla_np.columns:
            val = float(tabla_np.loc[idx, col])
            df = df[df["Año"] != 2023]
            df = pd.concat([df, pd.DataFrame([{"Año": 2023, target: val}])], ignore_index=True)

    if not df.empty:
        df.sort_values("Año", inplace=True)
        df.drop_duplicates("Año", keep="last", inplace=True)
    return df

# -----------------------------------------------------------------------------
# SUPERVIVENCIA (optimizada y genérica para 5,10,15,20,25)
# -----------------------------------------------------------------------------

@st.cache_data(show_spinner=False, max_entries=64)
def tabla_supervivencia_desde_pivote(tabla_pivote: pd.DataFrame, step: int) -> pd.DataFrame:
    """Construye tabla UE/PO con 'supervivientes después de <step> años' tomando fila k*5
    por censo (mismo patrón de tu app original) y devolviendo una tabla tipo natalidad.
    """
    return tabla_natalidad_desde_pivote(tabla_pivote, pasos_fila=5)  # misma extracción base


@st.cache_data(show_spinner=False, max_entries=128)
def proyeccion_supervivencia(tabla_sprv: pd.DataFrame, step: int, factores_ref: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Proyecta supervivencia anual UE/PO usando una tasa anual aproximada derivada del
    promedio de factores (si se provee), o 1.0 en su defecto. Similar a población activa, pero
    sobre la tabla de 'supervivientes después de X años'.
    """
    if tabla_sprv.empty:
        return pd.DataFrame(columns=["Año (t)", f"Supervivientes después de {step} años UE", f"Supervivientes después de {step} años PO"])  

    cols = sorted(tabla_sprv.columns, key=lambda x: int(x.split(" ")[1]))
    registros = []

    # UE
    if "UE" in tabla_sprv.index:
        for i in range(max(0, len(cols)-1)):
            a_i = int(cols[i].split(" ")[1]); a_f = int(cols[i+1].split(" ")[1])
            val = float(tabla_sprv.loc["UE", cols[i]])
            tasa = 1.0
            if factores_ref is not None and not factores_ref.empty and "Unidades Económicas" in factores_ref.index:
                medias = pd.to_numeric(factores_ref.loc["Unidades Económicas"], errors="coerce").dropna()
                if not medias.empty:
                    tasa = float(medias.mean())
            registros.append({"Año (t)": a_i, f"Supervivientes después de {step} años UE": val})
            for a in range(a_i+1, min(a_f, 2019)):
                val *= tasa; registros.append({"Año (t)": a, f"Supervivientes después de {step} años UE": val})

    # PO
    if "PO" in tabla_sprv.index:
        for i in range(max(0, len(cols)-1)):
            a_i = int(cols[i].split(" ")[1]); a_f = int(cols[i+1].split(" ")[1])
            val = float(tabla_sprv.loc["PO", cols[i]])
            registros.append({"Año (t)": a_i, f"Supervivientes después de {step} años PO": val})
            for a in range(a_i+1, min(a_f, 2019)):
                # Para PO usamos tasas IMSS año-a-año, aplicadas en cascada a partir del primer estimado
                # (Aproximación consistente con tu app: IMSS para PO post-2019, aquí usamos 2019..2022)
                # Entre censos previos a 2019 mantenemos val (o podríamos aplicar tasa UE ref si quieres).
                pass

    df = pd.DataFrame(registros).groupby("Año (t)", as_index=False).sum(numeric_only=True)
    # Extensión 2019..2022 para PO
    if not df.empty and (df["Año (t)"] == 2018).any() and f"Supervivientes después de {step} años PO" in df.columns:
        base_po_2018 = float(df.loc[df["Año (t)"]==2018, f"Supervivientes después de {step} años PO"].fillna(0).values[0])
        po_2019 = base_po_2018 * TASAS_IMSS[0]
        df = pd.concat([df, pd.DataFrame([{"Año (t)": 2019, f"Supervivientes después de {step} años PO": po_2019}])], ignore_index=True)
        prev = po_2019
        for idx, anio in enumerate([2020, 2021, 2022], start=1):
            prev = prev * TASAS_IMSS[idx]
            df = pd.concat([df, pd.DataFrame([{"Año (t)": anio, f"Supervivientes después de {step} años PO": prev}])], ignore_index=True)

    # Añadir 2023 observación si existe en tabla_sprv
    for idx, target in (("UE", f"Supervivientes después de {step} años UE"), ("PO", f"Supervivientes después de {step} años PO")):
        col = "CE 2023"
        if idx in tabla_sprv.index and col in tabla_sprv.columns:
            val = float(tabla_sprv.loc[idx, col])
            df = df[df["Año (t)"] != 2023]
            df = pd.concat([df, pd.DataFrame([{"Año (t)": 2023, target: val}])], ignore_index=True)

    if not df.empty:
        df.sort_values("Año (t)", inplace=True)
        df.drop_duplicates("Año (t)", keep="last", inplace=True)
    return df

# -----------------------------------------------------------------------------
# Helpers de UI
# -----------------------------------------------------------------------------

def _titulo(entidad: str, sector: str, tam: str) -> Tuple[str, str, str]:
    if entidad == "NACIONAL":
        t_ent = "a nivel Nacional"
    else:
        t_ent = f"en la entidad de {entidad.title().replace('De','de').replace('Del','del')}"
    if sector == "TODOS LOS SECTORES":
        t_sec = "pertenecientes a todos los sectores"
    elif sector == "OTROS SECTORES":
        t_sec = "pertenecientes a otros sectores"
    else:
        t_sec = f"pertenecientes al sector {sector.capitalize()}"
    if tam == "CONCENTRADOS":
        t_tam = "de todos los tamaños"
    else:
        t_tam = f"con {tam.lower()}"
    return t_ent, t_sec, t_tam


def _note():
    st.markdown("<small>Fuente: Censos Económicos 1989-2024</small>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

df_all = cargar_censos_unificado()
if df_all.empty:
    st.error("No se pudieron cargar los datos de censos. Asegúrate de subir los CSV al repositorio.")
    st.stop()

entidad, sector, tam, fenomeno = opciones_sidebar(df_all)
mostrar_ue = st.session_state.get("chk_ue", True)
mostrar_po = st.session_state.get("chk_po", False)

df_f = aplicar_filtros(df_all, entidad, sector, tam)
if df_f.empty:
    st.warning("No se encontraron datos para la combinación seleccionada.")
    st.stop()

t_ent, t_sec, t_tam = _titulo(entidad, sector, tam)

# PIVOTE BASE
tabla = pivot_demografia(df_f, mostrar_ue, mostrar_po)
if tabla.empty:
    st.info("Activa al menos una métrica (Negocios/Empleos) para ver resultados.")
    st.stop()

# ---------------------- POBLACIÓN ACTIVA ----------------------
if fenomeno == "Población activa":
    with st.expander("Ver tabla pivote (resumen)"):
        st.dataframe(tabla.head(100), width="stretch")
        st.download_button("Descargar pivote CSV", data=tabla.to_csv().encode("utf-8"), file_name="pivote_demografia.csv", mime="text/csv")

    factores, etiquetas = factores_crecimiento_desde_totales(tabla, raiz=0.2)
    serie = serie_anual_desde_factores(tabla, factores)

    if not serie.empty:
        serie_fmt = serie.copy()
        for c in ("Número de Negocios", "Personal Ocupado"):
            if c in serie_fmt.columns:
                serie_fmt[c] = serie_fmt[c].round(0).map(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
        st.write(f"Comportamiento anual de población activa {t_ent}, {t_sec} {t_tam}")
        st.dataframe(serie_fmt, width="stretch", height=600)
        _note()

    if not serie.empty:
        columnas = []
        if mostrar_ue and "Número de Negocios" in serie.columns:
            columnas.append("Número de Negocios")
        if mostrar_po and "Personal Ocupado" in serie.columns:
            columnas.append("Personal Ocupado")
        if columnas:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            for i, col in enumerate(columnas):
                sec = i > 0
                color = "#08989C" if col == "Número de Negocios" else "#003057"
                fig.add_trace(
                    go.Scatter(x=serie["Año"], y=serie[col], name=col, mode="lines+markers",
                               line=dict(color=color), marker=dict(color=color), hovertemplate="%{y:,.0f}<br>Año: %{x}"),
                    secondary_y=sec,
                )
            fig.update_layout(
                hovermode="x unified",
                title=dict(text=f"Comportamiento anual de población activa {t_ent},<br>{t_sec} {t_tam}", font=dict(size=15)),
                legend=dict(x=0.5, xanchor="center", y=-0.2, yanchor="top", orientation="h"),
                margin=dict(t=110),
            )
            fig.update_xaxes(title_text="Año")
            if mostrar_ue:
                fig.update_yaxes(title_text="<b>UNIDADES ECONÓMICAS</b>", secondary_y=False)
            if mostrar_po:
                fig.update_yaxes(title_text="<b>PERSONAL OCUPADO</b>", secondary_y=True)
            st.plotly_chart(fig, width="stretch")
            _note()

# ---------------------- NATALIDAD ----------------------
if fenomeno == "Natalidad":
    st.info("Los cálculos de natalidad se ejecutan de forma optimizada y cacheada.")
    # Construir tabla natalidad a partir del pivote base (5 en 5 filas como tu lógica original)
    tn = tabla_natalidad_desde_pivote(tabla, pasos_fila=5)
    if tn.empty:
        st.warning("No fue posible construir la tabla de natalidad con los datos actuales.")
        st.stop()
    # Factores entre censos
    crec_nat, etiquetas_nat = crecimiento_entre_censos_natalidad(tn, raiz=0.2)
    # Serie anual de natalidad
    nat = proyeccion_natalidad(tn, crec_nat, anio_tope=2019)

    with st.expander("Tabla de natalidad (resumen)"):
        st.dataframe(tn, width="stretch")
        st.download_button("Descargar natalidad CSV", data=tn.to_csv().encode("utf-8"), file_name="tabla_natalidad.csv", mime="text/csv")

    if not nat.empty:
        nat_fmt = nat.copy()
        for c in ("Número de Nacimientos", "Nacimiento de Empleos"):
            if c in nat_fmt.columns:
                nat_fmt[c] = nat_fmt[c].round(0).map(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
        st.write(f"Comportamiento anual de natalidad {t_ent}, {t_sec} {t_tam}")
        st.dataframe(nat_fmt, width="stretch", height=600)
        _note()

        columnas = []
        if mostrar_ue and "Número de Nacimientos" in nat.columns:
            columnas.append("Número de Nacimientos")
        if mostrar_po and "Nacimiento de Empleos" in nat.columns:
            columnas.append("Nacimiento de Empleos")
        if columnas:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            for i, col in enumerate(columnas):
                sec = i > 0
                color = "#08989C" if col == "Número de Nacimientos" else "#003057"
                fig.add_trace(
                    go.Scatter(x=nat["Año"], y=nat[col], name=col, mode="lines+markers",
                               line=dict(color=color), marker=dict(color=color), hovertemplate="%{y:,.0f}<br>Año: %{x}"),
                    secondary_y=sec,
                )
            fig.update_layout(
                hovermode="x unified",
                title=dict(text=f"Natalidad anual {t_ent},<br>{t_sec} {t_tam}", font=dict(size=15)),
                legend=dict(x=0.5, xanchor="center", y=-0.2, yanchor="top", orientation="h"),
                margin=dict(t=110),
            )
            fig.update_xaxes(title_text="Año")
            if mostrar_ue:
                fig.update_yaxes(title_text="<b>NACIMIENTOS DE NEGOCIOS</b>", secondary_y=False)
            if mostrar_po:
                fig.update_yaxes(title_text="<b>NACIMIENTOS DE EMPLEOS</b>", secondary_y=True)
            st.plotly_chart(fig, width="stretch")
            _note()

# ---------------------- SUPERVIVENCIA ----------------------
if fenomeno == "Supervivencia":
    st.info("Las tablas de supervivencia se construyen con funciones genéricas para 5, 10, 15, 20 y 25 años.")

    factores_ref, _ = factores_crecimiento_desde_totales(tabla, raiz=0.2)

    steps = [5, 10, 15, 20, 25]
    for step in steps:
        st.markdown("---")
        st.subheader(f"Supervivencia a {step} años")
        ts = tabla_supervivencia_desde_pivote(tabla, step)
        if ts.empty:
            st.warning("No se pudo construir la tabla de supervivencia.")
            continue
        with st.expander(f"Tabla de supervivencia ({step} años) — resumen"):
            st.dataframe(ts, width="stretch")
            st.download_button(f"Descargar supervivencia {step} CSV", data=ts.to_csv().encode("utf-8"), file_name=f"tabla_supervivencia_{step}.csv", mime="text/csv")

        sprv = proyeccion_supervivencia(ts, step, factores_ref=factores_ref)
        if sprv.empty:
            st.info("Sin datos para graficar.")
            continue

        # Mostrar tabla formateada
        sprv_fmt = sprv.copy()
        for c in sprv_fmt.columns:
            if c.startswith("Supervivientes después de"):
                sprv_fmt[c] = sprv_fmt[c].round(0).map(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
        st.dataframe(sprv_fmt, width="stretch", height=500)
        _note()

        # Gráfico
        columnas = [c for c in sprv.columns if c.startswith("Supervivientes después de")]
        if columnas:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            for i, col in enumerate(columnas):
                sec = i > 0
                color = "#08989C" if " UE" in col else "#003057"
                fig.add_trace(
                    go.Scatter(x=sprv["Año (t)"], y=sprv[col], name=col, mode="lines+markers",
                               line=dict(color=color), marker=dict(color=color), hovertemplate="%{y:,.0f}<br>Año: %{x}"),
                    secondary_y=sec,
                )
            fig.update_layout(
                hovermode="x unified",
                title=dict(text=f"Supervivencia (t) nacidas {step} años antes {t_ent},<br>{t_sec} {t_tam}", font=dict(size=15)),
                legend=dict(x=0.5, xanchor="center", y=-0.2, yanchor="top", orientation="h"),
                margin=dict(t=110),
            )
            fig.update_xaxes(title_text="Año (t)")
            st.plotly_chart(fig, width="stretch")
            _note()
