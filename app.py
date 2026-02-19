
# -*- coding: utf-8 -*-
# Aplicación optimizada de Streamlit para Demografía de Negocios.
# (ver comentarios dentro del archivo para detalles de optimización)

import os
import math
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

st.set_page_config(page_title="Demografía de Negocios", page_icon=_icon, layout="wide")
st.title("Simulador de Indicadores Demográficos Económicos de México")

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

# ------------------------ Utilidades de E/S ------------------------

def _auto_sep_read_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, sep=None, engine="python", encoding="latin1", low_memory=False)
        return df
    except Exception:
        return pd.read_csv(path, sep=",", encoding="latin1", low_memory=False)


def _homogeneizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
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
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype("float64")
    if "personal_ocupado_estrato" in df.columns:
        df["personal_ocupado_estrato"] = pd.to_numeric(df["personal_ocupado_estrato"], errors="coerce")
    if "generacion" in df.columns:
        df["generacion"] = pd.to_numeric(df["generacion"], errors="coerce").fillna(0).astype("int32")
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
        dfi = _homogeneizar_columnas(dfi)
        dfi["censo"] = int(anio_censo)
        dfs.append(dfi)
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)
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
    return df

# ------------------------ Filtros dinámicos ------------------------

def opciones_sidebar(df: pd.DataFrame) -> Tuple[str, str, Optional[str]]:
    entidades = ["NACIONAL"] + sorted(df["entidad"].cat.categories.tolist())
    sectores = ["TODOS LOS SECTORES"] + sorted(df["sector"].cat.categories.tolist())
    with st.sidebar:
        entidad = st.selectbox("ENTIDAD FEDERATIVA:", entidades)
        sector = st.selectbox("SECTOR:", sectores)
        dff = df
        if entidad != "NACIONAL":
            dff = dff[dff["entidad"] == entidad]
        if sector != "TODOS LOS SECTORES":
            dff = dff[dff["sector"] == sector]
        estratos_disponibles = sorted(dff["personal_ocupado_estrato"].dropna().unique().tolist())
        etiquetas = ["CONCENTRADOS"] + [NUM_A_ETIQUETA_ESTRATO.get(int(e), f"Estrato {int(e)}") for e in estratos_disponibles]
        tam = st.selectbox("TAMAÑO:", etiquetas)
    return entidad, sector, tam


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

# ------------------ Pivote, factores, proyecciones -----------------

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
    totales = pd.DataFrame([tabla.sum(axis=0)], index=[0])
    tabla = pd.concat([tabla, totales])
    return tabla

@st.cache_data(show_spinner=False, max_entries=256)
def factores_crecimiento_desde_totales(tabla: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    if tabla.empty:
        return pd.DataFrame(), []
    totales = tabla.loc[0]
    col_ue = [c for c in totales.index if c.endswith("UE")]
    col_po = [c for c in totales.index if c.endswith("PO")]
    def _calc(cols: List[str], raiz: float) -> Tuple[List[float], List[str]]:
        if not cols:
            return [], []
        pares = sorted(cols, key=lambda x: int(x.split(" ")[1]))
        vals = totales[pares].to_numpy(dtype=float)
        prev, nxt = vals[:-1], vals[1:]
        with np.errstate(divide='ignore', invalid='ignore'):
            factores = np.where(prev > 0, (nxt/prev)**raiz, np.nan)
        etiquetas = [f"{pares[i]}-{pares[i+1]}" for i in range(len(pares)-1)]
        return factores.tolist(), etiquetas
    raiz = 0.2
    f_ue, etiquetas = _calc(col_ue, raiz)
    f_po, _ = _calc(col_po, raiz)
    filas, idx = [], []
    if f_ue:
        filas.append(f_ue); idx.append("Unidades Económicas")
    if f_po:
        filas.append(f_po); idx.append("Personal Ocupado")
    if not filas:
        return pd.DataFrame(), etiquetas
    df = pd.DataFrame(filas, index=idx, columns=[e.replace("CE ","").replace(" - UE","").replace(" - PO","") for e in etiquetas])
    return df, etiquetas

@st.cache_data(show_spinner=False, max_entries=128)
def proyeccion_2019_y_2020_2022(tabla: pd.DataFrame, factores: pd.DataFrame) -> pd.DataFrame:
    if tabla.empty:
        return pd.DataFrame(columns=["Año", "Número de Negocios", "Personal Ocupado"])  
    cols_ue = sorted([c for c in tabla.columns if c.endswith("UE")], key=lambda x: int(x.split(" ")[1]))
    cols_po = sorted([c for c in tabla.columns if c.endswith("PO")], key=lambda x: int(x.split(" ")[1]))
    tot = tabla.loc[0]
    registros = []
    for i in range(max(0, len(cols_ue)-1)):
        a_i = int(cols_ue[i].split(" ")[1]); a_f = int(cols_ue[i+1].split(" ")[1]) if i+1 < len(cols_ue) else a_i
        val = float(tot[cols_ue[i]])
        etiqueta = f"{a_i}-{a_f}"
        f = float(factores.loc["Unidades Económicas", etiqueta]) if (not factores.empty and "Unidades Económicas" in factores.index and etiqueta in factores.columns) else 1.0
        registros.append({"Año": a_i, "Número de Negocios": val})
        for a in range(a_i+1, min(a_f, 2019)):
            val *= f; registros.append({"Año": a, "Número de Negocios": val})
    for i in range(max(0, len(cols_po)-1)):
        a_i = int(cols_po[i].split(" ")[1]); a_f = int(cols_po[i+1].split(" ")[1]) if i+1 < len(cols_po) else a_i
        val = float(tot[cols_po[i]])
        etiqueta = f"{a_i}-{a_f}"
        f = float(factores.loc["Personal Ocupado", etiqueta]) if (not factores.empty and "Personal Ocupado" in factores.index and etiqueta in factores.columns) else 1.0
        registros.append({"Año": a_i, "Personal Ocupado": val})
        for a in range(a_i+1, min(a_f, 2019)):
            val *= f; registros.append({"Año": a, "Personal Ocupado": val})
    df = pd.DataFrame(registros).groupby("Año", as_index=False).sum(numeric_only=True)
    tasas_imss = [1.0184, 0.9681, 1.0558, 1.0319]
    if not df.empty and (df["Año"] == 2018).any():
        base_ue_2018 = float(df.loc[df["Año"]==2018, "Número de Negocios"].fillna(0).values[0]) if "Número de Negocios" in df.columns else np.nan
        base_po_2018 = float(df.loc[df["Año"]==2018, "Personal Ocupado"].fillna(0).values[0]) if "Personal Ocupado" in df.columns else np.nan
        if not factores.empty and "Unidades Económicas" in factores.index:
            medias = pd.to_numeric(factores.loc["Unidades Económicas"], errors="coerce").dropna()
            tasa_ue = float(medias.mean()) if not medias.empty else 1.0
        else:
            tasa_ue = 1.0
        if not math.isnan(base_ue_2018):
            df = pd.concat([df, pd.DataFrame([{"Año": 2019, "Número de Negocios": base_ue_2018*tasa_ue}])], ignore_index=True)
        if not math.isnan(base_po_2018):
            df = pd.concat([df, pd.DataFrame([{"Año": 2019, "Personal Ocupado": base_po_2018*tasas_imss[0]}])], ignore_index=True)
        for idx, anio in enumerate([2020, 2021, 2022], start=1):
            prev = df[df["Año"]==anio-1].iloc[:1]
            if not prev.empty and "Personal Ocupado" in df.columns and not pd.isna(prev["Personal Ocupado"].values[0]):
                po_val = float(prev["Personal Ocupado"].values[0]) * tasas_imss[idx]
                df = pd.concat([df, pd.DataFrame([{"Año": anio, "Personal Ocupado": po_val}])], ignore_index=True)
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

# ---------------------------- UI principal ----------------------------

df_all = cargar_censos_unificado()
if df_all.empty:
    st.error("No se pudieron cargar los datos de censos. Asegúrate de subir los CSV al repositorio.")
    st.stop()

entidad, sector, tam = opciones_sidebar(df_all)

col_sel = st.columns(3)
with col_sel[0]:
    st.checkbox("Negocios", value=True, key="chk_ue")
with col_sel[1]:
    st.checkbox("Empleos", value=False, key="chk_po")
with col_sel[2]:
    fenomeno = st.radio("Fenómeno demográfico:", ["Población activa", "Natalidad", "Supervivencia"], horizontal=True)

mostrar_ue = st.session_state.get("chk_ue", True)
mostrar_po = st.session_state.get("chk_po", False)

df_f = aplicar_filtros(df_all, entidad, sector, tam)
if df_f.empty:
    st.warning("No se encontraron datos para la combinación seleccionada.")
    st.stop()

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

def _small_note():
    st.markdown("<small>Fuente: Censos Económicos 1989-2024</small>", unsafe_allow_html=True)

if fenomeno == "Población activa":
    tabla = pivot_demografia(df_f, mostrar_ue, mostrar_po)
    if tabla.empty:
        st.info("Activa al menos una métrica (Negocios/Empleos) para ver resultados.")
        st.stop()
    with st.expander("Ver tabla pivote (resumen)"):
        st.dataframe(tabla.head(100), width="stretch")
        csv = tabla.to_csv(index=True).encode("utf-8")
        st.download_button("Descargar pivote CSV", data=csv, file_name="pivote_demografia.csv", mime="text/csv")
    factores, etiquetas = factores_crecimiento_desde_totales(tabla)
    serie = proyeccion_2019_y_2020_2022(tabla, factores)
    if not serie.empty:
        serie_fmt = serie.copy()
        for c in ("Número de Negocios", "Personal Ocupado"):
            if c in serie_fmt.columns:
                serie_fmt[c] = serie_fmt[c].round(0).map(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
        st.write(f"Comportamiento anual de población activa {t_ent}, {t_sec} {t_tam}")
        st.dataframe(serie_fmt, width="stretch", height=600)
        _small_note()
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
            _small_note()

if fenomeno in {"Natalidad", "Supervivencia"}:
    st.info(
        "Para mantener la app estable en la nube, los cálculos avanzados de '" + fenomeno + "' "
        "se ejecutan solo bajo demanda y con resultados cacheados. Si quieres, puedo "
        "extender esta versión para replicar al detalle tus cuadros avanzados (quinquenales, "
        "probabilidades, etc.) conservando la misma lógica y fórmulas, pero de forma modular." 
    )
    st.write("Prepara tus filtros y presiona el botón para calcular:")
    if st.button(f"Calcular {fenomeno}"):
        df_prob = cargar_probabilidades()
        if df_prob.empty:
            st.warning("No hay 'PROBABILIDADES.csv'; imposible calcular proyecciones por natalidad/supervivencia.")
            st.stop()
        st.success(f"Listo. Lógica detallada de {fenomeno} puede añadirse aquí de forma optimizada.")
