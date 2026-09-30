import pandas as pd
import numpy as np
import sys 
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CARPETA_BASES =  BASE_DIR / "BASES"
CARPETA_RESULTADOS = BASE_DIR / "RESULTADOS"

CARPETA_RESULTADOS.mkdir(exist_ok=True)
#====================================================================================
#PASO NÚMERO 1
#====================================================================================
if len(sys.argv) > 1:
    archivo_base = CARPETA_BASES / sys.argv[1]
else:
    archivo_base =  CARPETA_BASES / "NACIONAL_TOTAL.xlsx"

def calcular_tabla(archivo_base):
    BASE = pd.read_excel(archivo_base)
    print(f"\nProcesando base: {archivo_base}\n")

    TABLAS = {}
    GENERACIONES = {}
    PROMEDIOS_QUINQUENALES = {}
    PROMEDIOS_AJUSTADOS = {}

    #====================================================================================
    #PARA PRUEBAS FUERA DEL PROGRAMA
    #====================================================================================

    #archivo_base =  r"C:\Users\manuel.lara\INTENTO\BASES\CAMPECHE_TOTAL.xlsx"
    #BASE = pd.read_excel(archivo_base)

    #====================================================================================
    # PASO NÚMERO 2
    #SE CÁLCULAN LAS PROBABILIDADES QUINQUENALES PARA LOS AÑOS CENSALES
    #====================================================================================

    probabilidad_quinquenal = BASE.copy()

    def calcular_probabilidad(base, numerador, denominador):
        return np.where(
            base[denominador] == 0,
            0,
            base[numerador] / base[denominador]
        )

    probabilidad_quinquenal["CE 1989"] = 0

    # Probabilidad para el CENSO 1994
    probabilidad_quinquenal["CE 1994"] = calcular_probabilidad(
        BASE,
        "CE 1994",
        "CE 1989"
    )

    # Probabilidad para el CENSO 1999
    probabilidad_quinquenal["CE 1999"] = calcular_probabilidad(
        BASE,
        "CE 1999",
        "CE 1994"
    )

    # Probabilidad para el CENSO 2004
    probabilidad_quinquenal["CE 2004"] = calcular_probabilidad(
        BASE,
        "CE 2004",
        "CE 1999"
    )

    # Probabilidad para el CENSO 2009
    probabilidad_quinquenal["CE 2009"] = calcular_probabilidad(
        BASE,
        "CE 2009",
        "CE 2004"
    )

    # Probabilidad para el CENSO 2014
    probabilidad_quinquenal["CE 2014"] = calcular_probabilidad(
        BASE,
        "CE 2014",
        "CE 2009"
    )

    # Probabilidad para el CENSO 2019
    probabilidad_quinquenal["CE 2019"] = calcular_probabilidad(
        BASE,
        "CE 2019",
        "CE 2014"
    )

    # Probabilidad para el CENSO 2024
    probabilidad_quinquenal["CE 2024"] = calcular_probabilidad(
        BASE,
        "CE 2024",
        "CE 2019"
    )

    #print(probabilidad_quinquenal)

    #----------------------------------------------------------------- PASO NÚMERO 3
    #CCONCENTRACIÓN 
    #TABLA GENERACIÓN1983
    GENERACION_1983 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "5-10",
            "10-15",
            "15-20",
            "20-25",
            "25-30",
            "30-35",
            "35-40",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1983] = GENERACION_1983

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1983
        ].iloc[0]

    GENERACION_1983["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1994"] >= 1 else fila["CE 1994"],
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1983 = (
        GENERACION_1983["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1983["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1983 = cocientes1983.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1983] = promedio_cocientes1983

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1983 < 1:
        PROMEDIO_QUINQUENAL1983 = 1 / promedio_cocientes1983
    else: 
        PROMEDIO_QUINQUENAL1983 = promedio_cocientes1983
    PROMEDIOS_AJUSTADOS[1983] = PROMEDIO_QUINQUENAL1983

    #TABLA GENERACIÓN 1983
    GENERACION_1984 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "4-9",
            "9-14",
            "14-19",
            "19-24",
            "24-29",
            "29-34",
            "34-39",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1984] = GENERACION_1984

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1984
        ].iloc[0]

    GENERACION_1984["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1994"] >= 1 else fila["CE 1994"],
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1984 = (
        GENERACION_1984["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1984["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1984 = cocientes1984.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1984] = promedio_cocientes1984

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1984 < 1:
        PROMEDIO_QUINQUENAL1984 = 1 / promedio_cocientes1984
    else: 
        PROMEDIO_QUINQUENAL1984 = promedio_cocientes1984
    PROMEDIOS_AJUSTADOS[1984] = PROMEDIO_QUINQUENAL1984

    #TABLA GENERACIÓN 1985
    GENERACION_1985 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "3-8",
            "8-13",
            "13-18",
            "18-23",
            "23-28",
            "28-33",
            "33-38",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1985] = GENERACION_1985

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1985
        ].iloc[0]

    GENERACION_1985["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1994"] >= 1 else fila["CE 1994"],
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1985 = (
        GENERACION_1985["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1985["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1985 = cocientes1985.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1985] = promedio_cocientes1985

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1985 < 1:
        PROMEDIO_QUINQUENAL1985 = 1 / promedio_cocientes1985
    else: 
        PROMEDIO_QUINQUENAL1985 = promedio_cocientes1985
    PROMEDIOS_AJUSTADOS[1985] = PROMEDIO_QUINQUENAL1985

    #TABLA GENERACIÓN 1986
    GENERACION_1986 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "2-7",
            "7-12",
            "12-17",
            "17-22",
            "22-27",
            "27-32",
            "32-37",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1986] = GENERACION_1986

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1986
        ].iloc[0]

    GENERACION_1986["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1994"] >= 1 else fila["CE 1994"],
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1986 = (
        GENERACION_1986["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1986["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1986 = cocientes1986.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1986] = promedio_cocientes1986

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1986 < 1:
        PROMEDIO_QUINQUENAL1986 = 1 / promedio_cocientes1986
    else: 
        PROMEDIO_QUINQUENAL1986 = promedio_cocientes1986
    PROMEDIOS_AJUSTADOS[1986] = PROMEDIO_QUINQUENAL1986

    #TABLA GENERACIÓN 1987
    GENERACION_1987 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "1-6",
            "6-11",
            "11-16",
            "16-21",
            "21-26",
            "26-31",
            "31-36",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1987] = GENERACION_1987

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1987
        ].iloc[0]

    GENERACION_1987["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1994"] >= 1 else fila["CE 1994"],
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1987 = (
        GENERACION_1987["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1987["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1987 = cocientes1987.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1987] = promedio_cocientes1987

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1987 < 1:
        PROMEDIO_QUINQUENAL1987 = 1 / promedio_cocientes1987
    else: 
        PROMEDIO_QUINQUENAL1987 = promedio_cocientes1987
    PROMEDIOS_AJUSTADOS[1987] = PROMEDIO_QUINQUENAL1987

    #TABLA GENERACIÓN 1988
    GENERACION_1988 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "0-5",
            "5-10",
            "10-15",
            "15-20",
            "20-25",
            "25-30",
            "30-35",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1988] = GENERACION_1988

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1988
        ].iloc[0]

    GENERACION_1988["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1994"] >= 1 else fila["CE 1994"],
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1988 = (
        GENERACION_1988["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1988["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1988 = cocientes1988.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1988] = promedio_cocientes1988

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1988 < 1:
        PROMEDIO_QUINQUENAL1988 = 1 / promedio_cocientes1988
    else: 
        PROMEDIO_QUINQUENAL1988 = promedio_cocientes1988
    PROMEDIOS_AJUSTADOS[1988] = PROMEDIO_QUINQUENAL1988

    #----------------------------------------------------------------------SE CÁLCULAN LAS PROBABILIDADES PARA LAS TABLAS CON 6 INTERVALOS DE 4-9, 9-14, ETC-------------------------------------------------------------------
    #----------------------------------TABLA GENERACIÓN 1989-----------------------------------
    GENERACION_1989 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "4-9",
            "9-14",
            "14-19",
            "19-24",
            "24-29",
            "29-34",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1989] = GENERACION_1989

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1989
        ].iloc[0]

    GENERACION_1989["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1989 = (
        GENERACION_1989["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1989["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1989 = cocientes1989.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1989] = promedio_cocientes1989

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1989 < 1:
        PROMEDIO_QUINQUENAL1989 = 1 / promedio_cocientes1989
    else: 
        PROMEDIO_QUINQUENAL1989 = promedio_cocientes1989
    PROMEDIOS_AJUSTADOS[1989] = PROMEDIO_QUINQUENAL1989

    #TABLA GENERACIÓN 1990
    GENERACION_1990 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "3-8",
            "8-13",
            "13-18",
            "18-23",
            "23-28",
            "28-33",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1990] = GENERACION_1990

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1990
        ].iloc[0]

    GENERACION_1990["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1990 = (
        GENERACION_1990["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1990["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1990 = cocientes1990.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1990] = promedio_cocientes1990

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1990 < 1:
        PROMEDIO_QUINQUENAL1990 = 1 / promedio_cocientes1990
    else: 
        PROMEDIO_QUINQUENAL1990 = promedio_cocientes1990
    PROMEDIOS_AJUSTADOS[1990] = PROMEDIO_QUINQUENAL1990

    #TABLA GENERACIÓN 1991
    GENERACION_1991 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "2-7",
            "7-12",
            "12-17",
            "17-22",
            "22-27",
            "27-32",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1991] = GENERACION_1991

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1991
        ].iloc[0]

    GENERACION_1991["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1991 = (
        GENERACION_1991["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1991["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1991 = cocientes1991.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1991] = promedio_cocientes1991

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1991 < 1:
        PROMEDIO_QUINQUENAL1991 = 1 / promedio_cocientes1991
    else: 
        PROMEDIO_QUINQUENAL1991 = promedio_cocientes1991
    PROMEDIOS_AJUSTADOS[1991] = PROMEDIO_QUINQUENAL1991

    #TABLA GENERACIÓN 1992
    GENERACION_1992 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "1-6",
            "6-11",
            "11-16",
            "16-21",
            "21-26",
            "26-31",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1992] = GENERACION_1992

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1992
        ].iloc[0]

    GENERACION_1992["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1992 = (
        GENERACION_1992["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1992["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1992 = cocientes1992.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1992] = promedio_cocientes1992

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1992 < 1:
        PROMEDIO_QUINQUENAL1992 = 1 / promedio_cocientes1992
    else: 
        PROMEDIO_QUINQUENAL1992 = promedio_cocientes1992
    PROMEDIOS_AJUSTADOS[1992] = PROMEDIO_QUINQUENAL1992

    #TABLA GENERACIÓN 1993
    GENERACION_1993 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "0-5",
            "5-10",
            "10-15",
            "15-20",
            "20-25",
            "25-30",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1993] = GENERACION_1993

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1993
        ].iloc[0]

    GENERACION_1993["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 1999"] >= 1 else fila["CE 1999"],
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1993 = (
        GENERACION_1993["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1993["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1993 = cocientes1993.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1993] = promedio_cocientes1993

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1993 < 1:
        PROMEDIO_QUINQUENAL1993 = 1 / promedio_cocientes1993
    else: 
        PROMEDIO_QUINQUENAL1993 = promedio_cocientes1993
    PROMEDIOS_AJUSTADOS[1993] = PROMEDIO_QUINQUENAL1993

    #----------------------------------------------------------------------SE CÁLCULAN LAS PROBABILIDADES PARA LAS TABLAS CON 5 INTERVALOS DE 4-9, 9-14, ETC-------------------------------------------------------------------
    #TABLA GENERACIÓN 1994
    GENERACION_1994 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "4-9",
            "9-14",
            "14-19",
            "19-24",
            "24-29",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1994] = GENERACION_1994

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1994
        ].iloc[0]

    GENERACION_1994["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1994 = (
        GENERACION_1994["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1994["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1994 = cocientes1994.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1994] = promedio_cocientes1994

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1994 < 1:
        PROMEDIO_QUINQUENAL1994 = 1 / promedio_cocientes1994
    else: 
        PROMEDIO_QUINQUENAL1994 = promedio_cocientes1994
    PROMEDIOS_AJUSTADOS[1994] = PROMEDIO_QUINQUENAL1994

    #TABLA GENERACIÓN 1995
    GENERACION_1995 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "3-8",
            "8-13",
            "13-18",
            "18-23",
            "23-28",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1995] = GENERACION_1995

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1995
        ].iloc[0]

    GENERACION_1995["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1995 = (
        GENERACION_1995["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1995["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1995 = cocientes1995.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1995] = promedio_cocientes1995

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1995 < 1:
        PROMEDIO_QUINQUENAL1995 = 1 / promedio_cocientes1995
    else: 
        PROMEDIO_QUINQUENAL1995 = promedio_cocientes1995
    PROMEDIOS_AJUSTADOS[1995] = PROMEDIO_QUINQUENAL1995

    #TABLA GENERACIÓN 1996
    GENERACION_1996 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "2-7",
            "7-12",
            "12-17",
            "17-22",
            "22-27",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1996] = GENERACION_1996

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1996
        ].iloc[0]

    GENERACION_1996["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1996 = (
        GENERACION_1996["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1996["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1996 = cocientes1996.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1996] = promedio_cocientes1996

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1996 < 1:
        PROMEDIO_QUINQUENAL1996 = 1 / promedio_cocientes1996
    else: 
        PROMEDIO_QUINQUENAL1996 = promedio_cocientes1996
    PROMEDIOS_AJUSTADOS[1996] = PROMEDIO_QUINQUENAL1996

    #TABLA GENERACIÓN 1997
    GENERACION_1997 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "1-6",
            "6-11",
            "11-16",
            "16-21",
            "21-26",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1997] = GENERACION_1997

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1997
        ].iloc[0]

    GENERACION_1997["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1997 = (
        GENERACION_1997["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1997["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1997 = cocientes1997.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1997] = promedio_cocientes1997

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1997 < 1:
        PROMEDIO_QUINQUENAL1997 = 1 / promedio_cocientes1997
    else: 
        PROMEDIO_QUINQUENAL1997 = promedio_cocientes1997
    PROMEDIOS_AJUSTADOS[1997] = PROMEDIO_QUINQUENAL1997

    #TABLA GENERACIÓN 1998
    GENERACION_1998 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "0-5",
            "5-10",
            "10-15",
            "15-20",
            "20-25",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1998] = GENERACION_1998

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1998
        ].iloc[0]

    GENERACION_1998["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2004"] >= 1 else fila["CE 2004"],
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1998 = (
        GENERACION_1998["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1998["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1998 = cocientes1998.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1998] = promedio_cocientes1998

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1998 < 1:
        PROMEDIO_QUINQUENAL1998 = 1 / promedio_cocientes1998
    else: 
        PROMEDIO_QUINQUENAL1998 = promedio_cocientes1998
    PROMEDIOS_AJUSTADOS[1998] = PROMEDIO_QUINQUENAL1998

    #----------------------------------------------------------------------SE CÁLCULAN LAS PROBABILIDADES PARA LAS TABLAS CON 4 INTERVALOS DE 4-9, 9-14, ETC-------------------------------------------------------------------
    #TABLA GENERACIÓN 1999
    GENERACION_1999 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "4-9",
            "9-14",
            "14-19",
            "19-24",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[1999] = GENERACION_1999

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 1999
        ].iloc[0]

    GENERACION_1999["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes1999 = (
        GENERACION_1999["PROBABILIDAD QUINQUENAL"]
        / GENERACION_1999["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes1999 = cocientes1999.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[1999] = promedio_cocientes1999

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes1999 < 1:
        PROMEDIO_QUINQUENAL1999 = 1 / promedio_cocientes1999
    else: 
        PROMEDIO_QUINQUENAL1999 = promedio_cocientes1999
    PROMEDIOS_AJUSTADOS[1999] = PROMEDIO_QUINQUENAL1999

    #TABLA GENERACIÓN 2000
    GENERACION_2000 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "3-8",
            "8-13",
            "13-18",
            "18-23",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2000] = GENERACION_2000

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2000
        ].iloc[0]

    GENERACION_2000["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2000 = (
        GENERACION_2000["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2000["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2000 = cocientes2000.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2000] = promedio_cocientes2000

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2000 < 1:
        PROMEDIO_QUINQUENAL2000 = 1 / promedio_cocientes2000
    else: 
        PROMEDIO_QUINQUENAL2000 = promedio_cocientes2000
    PROMEDIOS_AJUSTADOS[2000] = PROMEDIO_QUINQUENAL2000

    #TABLA GENERACIÓN 2001
    GENERACION_2001 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "2-7",
            "7-12",
            "12-17",
            "17-22",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2001] = GENERACION_2001

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2001
        ].iloc[0]

    GENERACION_2001["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2001 = (
        GENERACION_2001["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2001["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2001 = cocientes2001.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2001] = promedio_cocientes2001

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2001 < 1:
        PROMEDIO_QUINQUENAL2001 = 1 / promedio_cocientes2001
    else: 
        PROMEDIO_QUINQUENAL2001 = promedio_cocientes2001

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2001 < 1:
        PROMEDIO_QUINQUENAL2001 = 1 / promedio_cocientes2001
    else: 
        PROMEDIO_QUINQUENAL2001 = promedio_cocientes2001
    PROMEDIOS_AJUSTADOS[2001] = PROMEDIO_QUINQUENAL2001

    #TABLA GENERACIÓN 2002
    GENERACION_2002 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "1-6",
            "6-11",
            "11-16",
            "16-21",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2002] = GENERACION_2002

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2002
        ].iloc[0]

    GENERACION_2002["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2002 = (
        GENERACION_2002["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2002["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2002 = cocientes2002.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2002] = promedio_cocientes2002

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2002 < 1:
        PROMEDIO_QUINQUENAL2002 = 1 / promedio_cocientes2002
    else: 
        PROMEDIO_QUINQUENAL2002 = promedio_cocientes2002
    PROMEDIOS_AJUSTADOS[2002] = PROMEDIO_QUINQUENAL2002

    #TABLA GENERACIÓN 2003
    GENERACION_2003 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "0-5",
            "5-10",
            "10-15",
            "15-20",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2003] = GENERACION_2003

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2003
        ].iloc[0]

    GENERACION_2003["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2009"] >= 1 else fila["CE 2009"],
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2003 = (
        GENERACION_2003["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2003["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2003 = cocientes2003.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2003] = promedio_cocientes2003

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2003 < 1:
        PROMEDIO_QUINQUENAL2003 = 1 / promedio_cocientes2003
    else: 
        PROMEDIO_QUINQUENAL2003 = promedio_cocientes2003
    PROMEDIOS_AJUSTADOS[2003] = PROMEDIO_QUINQUENAL2003
        
    #----------------------------------------------------------------------SE CÁLCULAN LAS PROBABILIDADES PARA LAS TABLAS CON 3 INTERVALOS DE 4-9, 9-14, ETC-------------------------------------------------------------------
    #TABLA GENERACIÓN 2004
    GENERACION_2004 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "4-9",
            "9-14",
            "14-19",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2004] = GENERACION_2004

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2004
        ].iloc[0]

    GENERACION_2004["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2004 = (
        GENERACION_2004["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2004["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2004 = cocientes2004.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2004] = promedio_cocientes2004

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2004 < 1:
        PROMEDIO_QUINQUENAL2004 = 1 / promedio_cocientes2004
    else: 
        PROMEDIO_QUINQUENAL2004 = promedio_cocientes2004
    PROMEDIOS_AJUSTADOS[2004] = PROMEDIO_QUINQUENAL2004

    #TABLA GENERACIÓN 2005
    GENERACION_2005 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "3-8",
            "8-13",
            "13-18",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2005] = GENERACION_2005

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2005
        ].iloc[0]

    GENERACION_2005["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2005 = (
        GENERACION_2005["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2005["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2005 = cocientes2005.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2005] = promedio_cocientes2005

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2005 < 1:
        PROMEDIO_QUINQUENAL2005 = 1 / promedio_cocientes2005
    else: 
        PROMEDIO_QUINQUENAL2005 = promedio_cocientes2005
    PROMEDIOS_AJUSTADOS[2005] = PROMEDIO_QUINQUENAL2005

    #TABLA GENERACIÓN 2006
    GENERACION_2006 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "2-7",
            "7-12",
            "12-17",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2006] = GENERACION_2006

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2006
        ].iloc[0]

    GENERACION_2006["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2006 = (
        GENERACION_2006["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2006["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2006 = cocientes2006.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2006] = promedio_cocientes2006

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2006 < 1:
        PROMEDIO_QUINQUENAL2006 = 1 / promedio_cocientes2006
    else: 
        PROMEDIO_QUINQUENAL2006 = promedio_cocientes2006
    PROMEDIOS_AJUSTADOS[2006] = PROMEDIO_QUINQUENAL2006

    #TABLA GENERACIÓN 2007
    GENERACION_2007 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "1-6",
            "6-11",
            "11-16",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2007] = GENERACION_2007

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2007
        ].iloc[0]

    GENERACION_2007["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2007 = (
        GENERACION_2007["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2007["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2007 = cocientes2007.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2007] = promedio_cocientes2007

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2007 < 1:
        PROMEDIO_QUINQUENAL2007 = 1 / promedio_cocientes2007
    else: 
        PROMEDIO_QUINQUENAL2007 = promedio_cocientes2007
    PROMEDIOS_AJUSTADOS[2007] = PROMEDIO_QUINQUENAL2007

    #TABLA GENERACIÓN 2008
    GENERACION_2008 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "0-5",
            "5-10",
            "10-15",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2008] = GENERACION_2008

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2008
        ].iloc[0]

    GENERACION_2008["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2014"] >= 1 else fila["CE 2014"],
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2008 = (
        GENERACION_2008["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2008["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2008 = cocientes2008.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2008] = promedio_cocientes2008

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2008 < 1:
        PROMEDIO_QUINQUENAL2008 = 1 / promedio_cocientes2008
    else: 
        PROMEDIO_QUINQUENAL2008 = promedio_cocientes2008
    PROMEDIOS_AJUSTADOS[2008] = PROMEDIO_QUINQUENAL2008

    #----------------------------------------------------------------------SE CÁLCULAN LAS PROBABILIDADES PARA LAS TABLAS CON 2 INTERVALOS DE 4-9, 9-14, ETC-------------------------------------------------------------------
    #TABLA GENERACIÓN 2009
    GENERACION_2009 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "4-9",
            "9-14",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2009] = GENERACION_2009

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2009
        ].iloc[0]

    GENERACION_2009["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2009 = (
        GENERACION_2009["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2009["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2009 = cocientes2009.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2009] = promedio_cocientes2009

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2009 < 1:
        PROMEDIO_QUINQUENAL2009 = 1 / promedio_cocientes2009
    else: 
        PROMEDIO_QUINQUENAL2009 = promedio_cocientes2009
    PROMEDIOS_AJUSTADOS[2009] = PROMEDIO_QUINQUENAL2009

    #TABLA GENERACIÓN 2010
    GENERACION_2010 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "3-8",
            "8-13",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2010] = GENERACION_2010

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2010
        ].iloc[0]

    GENERACION_2010["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2010 = (
        GENERACION_2010["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2010["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2010 = cocientes2010.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2010] = promedio_cocientes2010

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2010 < 1:
        PROMEDIO_QUINQUENAL2010 = 1 / promedio_cocientes2010
    else: 
        PROMEDIO_QUINQUENAL2010 = promedio_cocientes2010
    PROMEDIOS_AJUSTADOS[2010] = PROMEDIO_QUINQUENAL2010

    #TABLA GENERACIÓN 2011
    GENERACION_2011 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "2-7",
            "7-12",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2011] = GENERACION_2011

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2011
        ].iloc[0]

    GENERACION_2011["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2011 = (
        GENERACION_2011["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2011["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2011 = cocientes2011.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2011] = promedio_cocientes2011

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2011 < 1:
        PROMEDIO_QUINQUENAL2011 = 1 / promedio_cocientes2011
    else: 
        PROMEDIO_QUINQUENAL2011 = promedio_cocientes2011
    PROMEDIOS_AJUSTADOS[2011] = PROMEDIO_QUINQUENAL2011

    #TABLA GENERACIÓN 2012
    GENERACION_2012 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "1-6",
            "6-11",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2012] = GENERACION_2012

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2012
        ].iloc[0]

    GENERACION_2012["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2012 = (
        GENERACION_2012["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2012["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2012 = cocientes2012.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2012] = promedio_cocientes2012

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2012 < 1:
        PROMEDIO_QUINQUENAL2012 = 1 / promedio_cocientes2012
    else: 
        PROMEDIO_QUINQUENAL2012 = promedio_cocientes2012
    PROMEDIOS_AJUSTADOS[2012] = PROMEDIO_QUINQUENAL2012

    #TABLA GENERACIÓN 2013
    GENERACION_2013 = pd.DataFrame({
        "INTERVALOS DE PROBABILIDAD": [
            "0-5",
            "5-10",
        ],
        "PROBABILIDAD QUINQUENAL": None
    })
    GENERACIONES[2013] = GENERACION_2013

    fila = probabilidad_quinquenal[
        probabilidad_quinquenal["CENSO"] == 2013
        ].iloc[0]

    GENERACION_2013["PROBABILIDAD QUINQUENAL"] = [
        1 if fila["CE 2019"] >= 1 else fila["CE 2019"],
        1 if fila["CE 2024"] >= 1 else fila["CE 2024"],
        ]

    cocientes2013 = (
        GENERACION_2013["PROBABILIDAD QUINQUENAL"]
        / GENERACION_2013["PROBABILIDAD QUINQUENAL"].shift(1)
    )

    promedio_cocientes2013 = cocientes2013.iloc[1:].mean()
    PROMEDIOS_QUINQUENALES[2013] = promedio_cocientes2013

    #SE CONDICIONAL EL PROMEDIO QUINQUENAL
    if promedio_cocientes2013 < 1:
        PROMEDIO_QUINQUENAL2013 = 1 / promedio_cocientes2013
    else: 
        PROMEDIO_QUINQUENAL2013 = promedio_cocientes2013
    PROMEDIOS_AJUSTADOS[2013] = PROMEDIO_QUINQUENAL2013

    #-----------------------------------------------------------------------------------------------------------------------------------------

    #GENERACIÓN 1983
    for intervalo in ["40-45", "45-50", "50-55", "55-60", "55-60"]:

        prob_ant = GENERACION_1983["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1983

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1983.loc[len(GENERACION_1983)] = [intervalo, nueva_prob]

    #GENERACIÓN 1984
    for intervalo in ["39-44", "44-49", "49-54", "54-59"]:

        prob_ant = GENERACION_1984["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1984

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1984.loc[len(GENERACION_1984)] = [intervalo, nueva_prob]
        
    #GENERACIÓN 1985
    for intervalo in ["38-43", "43-48", "48-53", "53-58"]:

        prob_ant = GENERACION_1985["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1985

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1985.loc[len(GENERACION_1985)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1986
    for intervalo in ["37-42", "42-47", "47-52", "52-57"]:

        prob_ant = GENERACION_1986["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1986

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1986.loc[len(GENERACION_1986)] = [intervalo, nueva_prob]
        
    #GENERACIÓN 1987
    for intervalo in ["36-41", "41-46", "46-51", "51-56"]:

        prob_ant = GENERACION_1987["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1987

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1987.loc[len(GENERACION_1987)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1988
    for intervalo in ["35-40", "40-45", "45-50", "50-55", "55-60"]:

        prob_ant = GENERACION_1988["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1988

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1988.loc[len(GENERACION_1988)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1989
    for intervalo in ["34-39","39-44", "44-49", "49-54", "54-59"]:

        prob_ant = GENERACION_1989["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1989

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1989.loc[len(GENERACION_1989)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1990
    for intervalo in ["33-38","38-43", "43-48", "48-53", "53-58"]:

        prob_ant = GENERACION_1990["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1990

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1990.loc[len(GENERACION_1990)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1991
    for intervalo in ["32-37","37-42", "42-47", "47-52", "52-57"]:

        prob_ant = GENERACION_1991["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1991

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1991.loc[len(GENERACION_1991)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1992
    for intervalo in ["31-36","36-41", "41-46", "46-51", "51-56"]:

        prob_ant = GENERACION_1992["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1992

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1992.loc[len(GENERACION_1992)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1993
    for intervalo in ["30-35","35-40", "40-45", "45-50", "50-55", "55-60"]:

        prob_ant = GENERACION_1993["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1993

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1993.loc[len(GENERACION_1993)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1994
    for intervalo in ["29-34","34-39","39-44", "44-49", "49-54", "54-59"]:

        prob_ant = GENERACION_1994["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1994

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1994.loc[len(GENERACION_1994)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1995
    for intervalo in ["28-33","33-38","38-43", "43-48", "48-53", "53-58"]:

        prob_ant = GENERACION_1995["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1995

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1995.loc[len(GENERACION_1995)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1996
    for intervalo in ["27-32","32-37","37-42", "42-47", "47-52", "52-57"]:

        prob_ant = GENERACION_1996["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1996

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1996.loc[len(GENERACION_1996)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1997
    for intervalo in ["26-31","31-36","36-41", "41-46", "46-51", "51-56"]:

        prob_ant = GENERACION_1997["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1997

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1997.loc[len(GENERACION_1997)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1998
    for intervalo in ["25-30","30-35","35-40", "40-45", "45-50", "50-55", "55-60"]:

        prob_ant = GENERACION_1998["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1998

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1998.loc[len(GENERACION_1998)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 1999
    for intervalo in ["24-29","29-34","34-39","39-44", "44-49", "49-54", "54-59"]:

        prob_ant = GENERACION_1999["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL1999

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_1999.loc[len(GENERACION_1999)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2000
    for intervalo in ["23-28","28-33","33-38","38-43", "43-48", "48-53", "53-58"]:

        prob_ant = GENERACION_2000["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2000

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2000.loc[len(GENERACION_2000)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2001
    for intervalo in ["22-27","27-32","32-37","37-42", "42-47", "47-52", "52-57"]:

        prob_ant = GENERACION_2001["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2001

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2001.loc[len(GENERACION_2001)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2002
    for intervalo in ["21-26","26-31","31-36","36-41", "41-46", "46-51", "51-56"]:

        prob_ant = GENERACION_2002["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2002

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2002.loc[len(GENERACION_2002)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2003
    for intervalo in ["20-25","25-30","30-35","35-40", "40-45", "45-50", "50-55", "55-60"]:

        prob_ant = GENERACION_2003["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2003

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2003.loc[len(GENERACION_2003)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2004
    for intervalo in ["19-24","24-29","29-34","34-39","39-44", "44-49", "49-54", "54-59"]:

        prob_ant = GENERACION_2004["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2004

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2004.loc[len(GENERACION_2004)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2005
    for intervalo in ["18-23","23-28","28-33","33-38","38-43", "43-48", "48-53", "53-58"]:

        prob_ant = GENERACION_2005["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2005

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2005.loc[len(GENERACION_2005)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2006
    for intervalo in ["17-22","22-27","27-32","32-37","37-42", "42-47", "47-52", "52-57"]:

        prob_ant = GENERACION_2006["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2006

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2006.loc[len(GENERACION_2006)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2007
    for intervalo in ["16-21","21-26","26-31","31-36","36-41", "41-46", "46-51", "51-56"]:

        prob_ant = GENERACION_2007["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2007

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2007.loc[len(GENERACION_2007)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2008
    for intervalo in ["15-20","20-25","25-30","30-35","35-40", "40-45", "45-50", "50-55", "55-60"]:

        prob_ant = GENERACION_2008["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2008

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2008.loc[len(GENERACION_2008)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2009
    for intervalo in ["14-19","19-24","24-29","29-34","34-39","39-44", "44-49", "49-54", "54-59"]:

        prob_ant = GENERACION_2009["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2009

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2009.loc[len(GENERACION_2009)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2010
    for intervalo in ["13-18","18-23","23-28","28-33","33-38","38-43", "43-48", "48-53", "53-58"]:

        prob_ant = GENERACION_2010["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2010

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2010.loc[len(GENERACION_2010)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2011
    for intervalo in ["12-17","17-22","22-27","27-32","32-37","37-42", "42-47", "47-52", "52-57"]:

        prob_ant = GENERACION_2011["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2011

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2011.loc[len(GENERACION_2011)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2012
    for intervalo in ["11-16","16-21","21-26","26-31","31-36","36-41", "41-46", "46-51", "51-56"]:

        prob_ant = GENERACION_2012["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2012

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2012.loc[len(GENERACION_2012)] = [intervalo, nueva_prob]
        
        #GENERACIÓN 2013
    for intervalo in ["10-15","15-20","20-25","25-30","30-35","35-40", "40-45", "45-50", "50-55", "55-60"]:

        prob_ant = GENERACION_2013["PROBABILIDAD QUINQUENAL"].iloc[-1]

        if prob_ant != 1:
            nueva_prob = prob_ant * PROMEDIO_QUINQUENAL2013

            if nueva_prob > 1:
                nueva_prob = 1
        else:
            nueva_prob = 1

        GENERACION_2013.loc[len(GENERACION_2013)] = [intervalo, nueva_prob]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1983 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1983] = tabla1983

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1983.loc[5, "P(x+5)"] = GENERACION_1983.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1983
    tabla1983.loc[6: 9, "P(x+5)"] = tabla1983.loc[5, "P(x+5)"]
    tabla1983.loc[10, "P(x+5)"] = GENERACION_1983.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1983.loc[11: 14, "P(x+5)"] = tabla1983.loc[10, "P(x+5)"]
    tabla1983.loc[15, "P(x+5)"] = GENERACION_1983.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1983.loc[16: 19, "P(x+5)"] = tabla1983.loc[15, "P(x+5)"]
    tabla1983.loc[20, "P(x+5)"] = GENERACION_1983.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1983.loc[21: 24, "P(x+5)"] = tabla1983.loc[20, "P(x+5)"]
    tabla1983.loc[25, "P(x+5)"] = GENERACION_1983.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1983.loc[26: 29, "P(x+5)"] = tabla1983.loc[25, "P(x+5)"]
    tabla1983.loc[30, "P(x+5)"] = GENERACION_1983.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1983.loc[31: 34, "P(x+5)"] = tabla1983.loc[30, "P(x+5)"]
    tabla1983.loc[35, "P(x+5)"] = GENERACION_1983.loc[5, "PROBABILIDAD QUINQUENAL"]
    tabla1983.loc[40, "P(x+5)"] = GENERACION_1983.loc[6, "PROBABILIDAD QUINQUENAL"]

    for i in [45, 50, 55, 60]:
        if tabla1983.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1983 <= 1:
            tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1983
        else:
            tabla1983.loc[i, "P(x+5)"] = 1

    for i in range(35, 41):
        if i not in [35, 40]:
            if (tabla1983.loc[35, "P(x+5)"] == 1 or tabla1983.loc[40, "P(x+5)"] == 1):
                if tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5)) >= 1:
                    tabla1983.loc[i, "P(x+5)"] = 1
                else: tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5))
            else: tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-1, "P(x+5)"] 

    for i in range(40, 46):
        if i not in [40, 45]:
            if (tabla1983.loc[40, "P(x+5)"] == 1 or tabla1983.loc[45, "P(x+5)"] == 1):
                if tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5)) >= 1:
                    tabla1983.loc[i, "P(x+5)"] = 1
                else: tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5))
            else: tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-1, "P(x+5)"] 

    for i in range(45, 51):
        if i not in [45, 50]:
            if (tabla1983.loc[45, "P(x+5)"] == 1 or tabla1983.loc[50, "P(x+5)"] == 1):
                if tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5)) >= 1:
                    tabla1983.loc[i, "P(x+5)"] = 1
                else: tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5))
            else: tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-1, "P(x+5)"]  

    for i in range(50, 56):
        if i not in [50, 55]:
            if (tabla1983.loc[50, "P(x+5)"] == 1 or tabla1983.loc[55, "P(x+5)"] == 1):
                if tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5)) >= 1:
                    tabla1983.loc[i, "P(x+5)"] = 1
                else: tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5))
            else: tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-1, "P(x+5)"]  
            
    for i in range(56, 61):
        if i not in [60]:
            if tabla1983.loc[i-1, "P(x+5)"] == 1:
                tabla1983.loc[i, "P(x+5)"] = 1
            if tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5)) < 1:
                tabla1983.loc[i, "P(x+5)"] = tabla1983.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1983 ** (1/5))
            else: tabla1983.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1983.loc[0, "S(x)"] = 100000
    tabla1983.loc[5, "S(x)"] = tabla1983.loc[0, "S(x)"] * tabla1983.loc[5, "P(x+5)"]

    for i in [10, 15, 20, 25, 30, 35]:
        tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-5, "S(x)"] * tabla1983.loc[i, "P(x+5)"]
        
    tabla1983.loc[0, "FACTOR ANUAL"] = (tabla1983.loc[0, "S(x)"] / tabla1983.loc[5, "S(x)"]) ** (1/5)

    for i in [5, 10, 15, 20, 25, 30]:
        tabla1983.loc[i, "FACTOR ANUAL"] = (tabla1983.loc[i, "S(x)"] / tabla1983.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 35):
        if i not in [5, 10, 15, 20, 25, 30]:
            tabla1983.loc[i, "FACTOR ANUAL"] = tabla1983.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 35):
        if i not in [5, 10, 15, 20, 25, 30]:
            if tabla1983.loc[i, "FACTOR ANUAL"] == 1:
                tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1, "S(x)"] / tabla1983.loc[i, "FACTOR ANUAL"]
            else: tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1, "S(x)"] / tabla1983.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1983.loc[35, "P(x+5)"] == 1:
        tabla1983.loc[35, "S(x)"] = tabla1983.loc[34, "S(x)"] * tabla1983.loc[35, "P(x+5)"]
    else: tabla1983.loc[35, "S(x)"] = tabla1983.loc[30, "S(x)"] * tabla1983.loc[35, "P(x+5)"]
    
    if tabla1983.loc[40, "P(x+5)"] == 1:
        tabla1983.loc[35, "FACTOR ANUAL"] = 1
    else: tabla1983.loc[35, "FACTOR ANUAL"] = (tabla1983.loc[35, "S(x)"] / ((tabla1983.loc[35, "S(x)"] * tabla1983.loc[40, "P(x+5)"]))) ** (1/5)    

    for i in range(36, 40):
        if tabla1983.loc[40, "P(x+5)"] == 1:
            tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1, "S(x)"] * tabla1983.loc[i, "P(x+5)"]
        else: tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1 , "S(x)"] / tabla1983.loc[35, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1983.loc[40, "P(x+5)"] == 1:
        tabla1983.loc[40, "S(x)"] = tabla1983.loc[39, "S(x)"] * tabla1983.loc[40, "P(x+5)"]
    else: tabla1983.loc[40, "S(x)"] = tabla1983.loc[35, "S(x)"] * tabla1983.loc[40, "P(x+5)"]

    #i+5   
    if tabla1983.loc[45, "P(x+5)"] == 1:
        tabla1983.loc[40, "FACTOR ANUAL"] = 1
    else: tabla1983.loc[40, "FACTOR ANUAL"] = (tabla1983.loc[40, "S(x)"] / ((tabla1983.loc[40, "S(x)"] * tabla1983.loc[45, "P(x+5)"]))) ** (1/5)    

    for i in range(41, 45):
        if tabla1983.loc[45, "P(x+5)"] == 1:
            tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1, "S(x)"] * tabla1983.loc[i, "P(x+5)"]
        else: tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1 , "S(x)"] / tabla1983.loc[40, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1983.loc[45, "P(x+5)"] == 1:
        tabla1983.loc[45, "S(x)"] = tabla1983.loc[44, "S(x)"] * tabla1983.loc[45, "P(x+5)"]
    else: tabla1983.loc[45, "S(x)"] = tabla1983.loc[40, "S(x)"] * tabla1983.loc[45, "P(x+5)"]
    
    if tabla1983.loc[50, "P(x+5)"] == 1:
        tabla1983.loc[45, "FACTOR ANUAL"] = 1
    else: tabla1983.loc[45, "FACTOR ANUAL"] = (tabla1983.loc[45, "S(x)"] / ((tabla1983.loc[45, "S(x)"] * tabla1983.loc[50, "P(x+5)"]))) ** (1/5)    

    for i in range(46, 50):
        if tabla1983.loc[45, "P(x+5)"] == 1 or tabla1983.loc[50, "P(x+5)"] == 1:
            tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1, "S(x)"] * tabla1983.loc[i, "P(x+5)"]
        else: tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1 , "S(x)"] / tabla1983.loc[45, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1983.loc[50, "P(x+5)"] == 1:
        tabla1983.loc[50, "S(x)"] = tabla1983.loc[49, "S(x)"] * tabla1983.loc[50, "P(x+5)"]
    else: tabla1983.loc[50, "S(x)"] = tabla1983.loc[45, "S(x)"] * tabla1983.loc[50, "P(x+5)"]

    if tabla1983.loc[55, "P(x+5)"] == 1:
        tabla1983.loc[50, "FACTOR ANUAL"] = 1
    else: tabla1983.loc[50, "FACTOR ANUAL"] = (tabla1983.loc[50, "S(x)"] / ((tabla1983.loc[50, "S(x)"] * tabla1983.loc[55, "P(x+5)"]))) ** (1/5) 

    for i in range(51, 55):
        if tabla1983.loc[50, "P(x+5)"] == 1 or tabla1983.loc[55, "P(x+5)"] == 1:
            tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1, "S(x)"] * tabla1983.loc[i, "P(x+5)"]
        else: tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1 , "S(x)"] / tabla1983.loc[50, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    

    if tabla1983.loc[55, "P(x+5)"] == 1:
        tabla1983.loc[55, "S(x)"] = tabla1983.loc[54, "S(x)"] * tabla1983.loc[55, "P(x+5)"]
    else: tabla1983.loc[55, "S(x)"] = tabla1983.loc[50, "S(x)"] * tabla1983.loc[55, "P(x+5)"]

    if tabla1983.loc[60, "P(x+5)"] == 1:
        tabla1983.loc[55, "FACTOR ANUAL"] = 1
    else: tabla1983.loc[55, "FACTOR ANUAL"] = (tabla1983.loc[55, "S(x)"] / ((tabla1983.loc[55, "S(x)"] * tabla1983.loc[60, "P(x+5)"]))) ** (1/5) 

    for i in range(56, 60):
        if tabla1983.loc[60, "P(x+5)"] == 1 or tabla1983.loc[55, "P(x+5)"] == 1:
            tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1, "S(x)"] * tabla1983.loc[i, "P(x+5)"]
        else: tabla1983.loc[i, "S(x)"] = tabla1983.loc[i-1 , "S(x)"] / tabla1983.loc[55, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1983.loc[60, "P(x+5)"] == 1:
        tabla1983.loc[60, "S(x)"] = tabla1983.loc[60, "P(x+5)"] * tabla1983.loc[59, "S(x)"]
    else: tabla1983.loc[60, "S(x)"] = tabla1983.loc[60, "P(x+5)"] * tabla1983.loc[55, "S(x)"]


    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1984 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1984] = tabla1984

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1984.loc[4, "P(x+5)"] = GENERACION_1984.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1984
    tabla1984.loc[5: 8, "P(x+5)"] = tabla1984.loc[4, "P(x+5)"]
    tabla1984.loc[9, "P(x+5)"] = GENERACION_1984.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1984.loc[10: 13, "P(x+5)"] = tabla1984.loc[9, "P(x+5)"]
    tabla1984.loc[14, "P(x+5)"] = GENERACION_1984.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1984.loc[15: 18, "P(x+5)"] = tabla1984.loc[14, "P(x+5)"]
    tabla1984.loc[19, "P(x+5)"] = GENERACION_1984.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1984.loc[20: 23, "P(x+5)"] = tabla1984.loc[19, "P(x+5)"]
    tabla1984.loc[24, "P(x+5)"] = GENERACION_1984.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1984.loc[25: 28, "P(x+5)"] = tabla1984.loc[24, "P(x+5)"]
    tabla1984.loc[29, "P(x+5)"] = GENERACION_1984.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1984.loc[30: 33, "P(x+5)"] = tabla1984.loc[29, "P(x+5)"]
    tabla1984.loc[34, "P(x+5)"] = GENERACION_1984.loc[5, "PROBABILIDAD QUINQUENAL"]
    tabla1984.loc[39, "P(x+5)"] = GENERACION_1984.loc[6, "PROBABILIDAD QUINQUENAL"]

    for i in [44, 49, 54, 59]:
        if tabla1984.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1984 <= 1:
            tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1984
        else:
            tabla1984.loc[i, "P(x+5)"] = 1

    for i in range(34, 40):
        if i not in [34, 39]:
            if (tabla1984.loc[34, "P(x+5)"] == 1 or tabla1984.loc[39, "P(x+5)"] == 1):
                if tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5)) >= 1:
                    tabla1984.loc[i, "P(x+5)"] = 1
                else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5))
            else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"] 

    for i in range(39, 45):
        if i not in [39, 44]:
            if (tabla1984.loc[39, "P(x+5)"] == 1 or tabla1984.loc[44, "P(x+5)"] == 1):
                if tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5)) >= 1:
                    tabla1984.loc[i, "P(x+5)"] = 1
                else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5))
            else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"] 

    for i in range(44, 50):
        if i not in [44, 49]:
            if (tabla1984.loc[44, "P(x+5)"] == 1 or tabla1984.loc[49, "P(x+5)"] == 1):
                if tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5)) >= 1:
                    tabla1984.loc[i, "P(x+5)"] = 1
                else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5))
            else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"]  

    for i in range(49, 55):
        if i not in [49, 54]:
            if (tabla1984.loc[49, "P(x+5)"] == 1 or tabla1984.loc[54, "P(x+5)"] == 1):
                if tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5)) >= 1:
                    tabla1984.loc[i, "P(x+5)"] = 1
                else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5))
            else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"]  
            
    for i in range(54, 60):
        if i not in [54, 59]:
            if (tabla1984.loc[54, "P(x+5)"] == 1 or tabla1984.loc[59, "P(x+5)"] == 1):
                if tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5)) >= 1:
                    tabla1984.loc[i, "P(x+5)"] = 1
                else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5))
            else: tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"]

    for i in range(60, 61):
        if tabla1984.loc[i-1, "P(x+5)"] == 1:
            tabla1984.loc[i, "P(x+5)"] = 1
        if tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5)) < 1:
            tabla1984.loc[i, "P(x+5)"] = tabla1984.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1984 ** (1/5))
        else: tabla1984.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1984.loc[0, "S(x)"] = 100000
    tabla1984.loc[4, "S(x)"] = tabla1984.loc[0, "S(x)"] * tabla1984.loc[4, "P(x+5)"]

    for i in [9, 14, 19, 24, 29, 34]:
        tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-5, "S(x)"] * tabla1984.loc[i, "P(x+5)"]
        
    tabla1984.loc[0, "FACTOR ANUAL"] = (tabla1984.loc[0, "S(x)"] / tabla1984.loc[4, "S(x)"]) ** (1/4)

    for i in [4, 9, 14, 19, 24, 29]:
        tabla1984.loc[i, "FACTOR ANUAL"] = (tabla1984.loc[i, "S(x)"] / tabla1984.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 34):
        if i not in [4, 9, 14, 19, 24, 29]:
            tabla1984.loc[i, "FACTOR ANUAL"] = tabla1984.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 34):
        if i not in [4, 9, 14, 19, 24, 29]:
            if tabla1984.loc[i, "FACTOR ANUAL"] == 1:
                tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1, "S(x)"] / tabla1984.loc[i, "FACTOR ANUAL"]
            else: tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1, "S(x)"] / tabla1984.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1984.loc[34, "P(x+5)"] == 1:
        tabla1984.loc[34, "S(x)"] = tabla1984.loc[33, "S(x)"] * tabla1984.loc[34, "P(x+5)"]
    else: tabla1984.loc[34, "S(x)"] = tabla1984.loc[29, "S(x)"] * tabla1984.loc[34, "P(x+5)"]
    
    if tabla1984.loc[39, "P(x+5)"] == 1:
        tabla1984.loc[34, "FACTOR ANUAL"] = 1
    else: tabla1984.loc[34, "FACTOR ANUAL"] = (tabla1984.loc[34, "S(x)"] / ((tabla1984.loc[34, "S(x)"] * tabla1984.loc[39, "P(x+5)"]))) ** (1/5)    

    for i in range(35, 39):
        if tabla1984.loc[39, "P(x+5)"] == 1:
            tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1, "S(x)"] * tabla1984.loc[i, "P(x+5)"]
        else: tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1 , "S(x)"] / tabla1984.loc[34, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1984.loc[39, "P(x+5)"] == 1:
        tabla1984.loc[39, "S(x)"] = tabla1984.loc[38, "S(x)"] * tabla1984.loc[39, "P(x+5)"]
    else: tabla1984.loc[39, "S(x)"] = tabla1984.loc[34, "S(x)"] * tabla1984.loc[39, "P(x+5)"]

    #i+5   
    if tabla1984.loc[44, "P(x+5)"] == 1:
        tabla1984.loc[39, "FACTOR ANUAL"] = 1
    else: tabla1984.loc[39, "FACTOR ANUAL"] = (tabla1984.loc[39, "S(x)"] / ((tabla1984.loc[39, "S(x)"] * tabla1984.loc[44, "P(x+5)"]))) ** (1/5)    

    for i in range(40, 44):
        if tabla1984.loc[44, "P(x+5)"] == 1:
            tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1, "S(x)"] * tabla1984.loc[i, "P(x+5)"]
        else: tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1 , "S(x)"] / tabla1984.loc[39, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1984.loc[44, "P(x+5)"] == 1:
        tabla1984.loc[44, "S(x)"] = tabla1984.loc[43, "S(x)"] * tabla1984.loc[44, "P(x+5)"]
    else: tabla1984.loc[44, "S(x)"] = tabla1984.loc[39, "S(x)"] * tabla1984.loc[44, "P(x+5)"]
    
    if tabla1984.loc[49, "P(x+5)"] == 1:
        tabla1984.loc[44, "FACTOR ANUAL"] = 1
    else: tabla1984.loc[44, "FACTOR ANUAL"] = (tabla1984.loc[44, "S(x)"] / ((tabla1984.loc[44, "S(x)"] * tabla1984.loc[49, "P(x+5)"]))) ** (1/5)    

    for i in range(45, 49):
        if tabla1984.loc[45, "P(x+5)"] == 1 or tabla1984.loc[49, "P(x+5)"] == 1:
            tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1, "S(x)"] * tabla1984.loc[i, "P(x+5)"]
        else: tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1 , "S(x)"] / tabla1984.loc[44, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1984.loc[49, "P(x+5)"] == 1:
        tabla1984.loc[49, "S(x)"] = tabla1984.loc[48, "S(x)"] * tabla1984.loc[49, "P(x+5)"]
    else: tabla1984.loc[49, "S(x)"] = tabla1984.loc[44, "S(x)"] * tabla1984.loc[49, "P(x+5)"]

    if tabla1984.loc[54, "P(x+5)"] == 1:
        tabla1984.loc[49, "FACTOR ANUAL"] = 1
    else: tabla1984.loc[49, "FACTOR ANUAL"] = (tabla1984.loc[49, "S(x)"] / ((tabla1984.loc[49, "S(x)"] * tabla1984.loc[54, "P(x+5)"]))) ** (1/5) 

    for i in range(50, 54):
        if tabla1984.loc[50, "P(x+5)"] == 1 or tabla1984.loc[54, "P(x+5)"] == 1:
            tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1, "S(x)"] * tabla1984.loc[i, "P(x+5)"]
        else: tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1 , "S(x)"] / tabla1984.loc[49, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1984.loc[54, "P(x+5)"] == 1:
        tabla1984.loc[54, "S(x)"] = tabla1984.loc[53, "S(x)"] * tabla1984.loc[54, "P(x+5)"]
    else: tabla1984.loc[54, "S(x)"] = tabla1984.loc[49, "S(x)"] * tabla1984.loc[54, "P(x+5)"]

    if tabla1984.loc[59, "P(x+5)"] == 1:
        tabla1984.loc[54, "FACTOR ANUAL"] = 1
    else: tabla1984.loc[54, "FACTOR ANUAL"] = (tabla1984.loc[54, "S(x)"] / ((tabla1984.loc[54, "S(x)"] * tabla1984.loc[59, "P(x+5)"]))) ** (1/5) 

    for i in range(55, 59):
        if tabla1984.loc[55, "P(x+5)"] == 1 or tabla1984.loc[59, "P(x+5)"] == 1:
            tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1, "S(x)"] * tabla1984.loc[i, "P(x+5)"]
        else: tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1 , "S(x)"] / tabla1984.loc[54, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1984.loc[59, "P(x+5)"] == 1:
        tabla1984.loc[59, "S(x)"] = tabla1984.loc[58, "S(x)"] * tabla1984.loc[59, "P(x+5)"]
    else: tabla1984.loc[59, "S(x)"] = tabla1984.loc[54, "S(x)"] * tabla1984.loc[59, "P(x+5)"]

    for i in range(59, 61):
        if i not in [59]:
            if tabla1984.loc[i-1, "P(x+5)"] == 1:
                tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1, "S(x)"] * tabla1984.loc[i, "P(x+5)"]
            else: tabla1984.loc[i, "S(x)"] = tabla1984.loc[i-1, "S(x)"] * tabla1984.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1985 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1985] = tabla1985

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1985.loc[3, "P(x+5)"] = GENERACION_1985.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1985
    tabla1985.loc[4: 7, "P(x+5)"] = tabla1985.loc[3, "P(x+5)"]
    tabla1985.loc[8, "P(x+5)"] = GENERACION_1985.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1985.loc[9: 12, "P(x+5)"] = tabla1985.loc[8, "P(x+5)"]
    tabla1985.loc[13, "P(x+5)"] = GENERACION_1985.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1985.loc[14: 17, "P(x+5)"] = tabla1985.loc[13, "P(x+5)"]
    tabla1985.loc[18, "P(x+5)"] = GENERACION_1985.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1985.loc[19: 22, "P(x+5)"] = tabla1985.loc[18, "P(x+5)"]
    tabla1985.loc[23, "P(x+5)"] = GENERACION_1985.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1985.loc[24: 27, "P(x+5)"] = tabla1985.loc[23, "P(x+5)"]
    tabla1985.loc[28, "P(x+5)"] = GENERACION_1985.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1985.loc[29: 32, "P(x+5)"] = tabla1985.loc[28, "P(x+5)"]
    tabla1985.loc[33, "P(x+5)"] = GENERACION_1985.loc[5, "PROBABILIDAD QUINQUENAL"]
    tabla1985.loc[38, "P(x+5)"] = GENERACION_1985.loc[6, "PROBABILIDAD QUINQUENAL"]

    for i in [43, 48, 53, 58]:
        if tabla1985.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1985 <= 1:
            tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1985
        else:
            tabla1985.loc[i, "P(x+5)"] = 1

    for i in range(33, 39):
        if i not in [33, 38]:
            if (tabla1985.loc[33, "P(x+5)"] == 1 or tabla1985.loc[38, "P(x+5)"] == 1):
                if tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5)) >= 1:
                    tabla1985.loc[i, "P(x+5)"] = 1
                else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5))
            else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"] 

    for i in range(38, 44):
        if i not in [38, 43]:
            if (tabla1985.loc[38, "P(x+5)"] == 1 or tabla1985.loc[43, "P(x+5)"] == 1):
                if tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5)) >= 1:
                    tabla1985.loc[i, "P(x+5)"] = 1
                else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5))
            else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"] 

    for i in range(43, 49):
        if i not in [43, 48]:
            if (tabla1985.loc[43, "P(x+5)"] == 1 or tabla1985.loc[48, "P(x+5)"] == 1):
                if tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5)) >= 1:
                    tabla1985.loc[i, "P(x+5)"] = 1
                else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5))
            else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"]  

    for i in range(48, 54):
        if i not in [48, 53]:
            if (tabla1985.loc[48, "P(x+5)"] == 1 or tabla1985.loc[53, "P(x+5)"] == 1):
                if tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5)) >= 1:
                    tabla1985.loc[i, "P(x+5)"] = 1
                else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5))
            else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"]  
            
    for i in range(53, 59):
        if i not in [53, 58]:
            if (tabla1985.loc[53, "P(x+5)"] == 1 or tabla1985.loc[58, "P(x+5)"] == 1):
                if tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5)) >= 1:
                    tabla1985.loc[i, "P(x+5)"] = 1
                else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5))
            else: tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"]

    for i in range(59, 61):
        if tabla1985.loc[i-1, "P(x+5)"] == 1:
            tabla1985.loc[i, "P(x+5)"] = 1
        if tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5)) < 1:
            tabla1985.loc[i, "P(x+5)"] = tabla1985.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1985 ** (1/5))
        else: tabla1985.loc[i, "P(x+5)"] = 1

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1985.loc[0, "S(x)"] = 100000
    tabla1985.loc[3, "S(x)"] = tabla1985.loc[0, "S(x)"] * tabla1985.loc[3, "P(x+5)"]

    for i in [8, 13, 18, 23, 28, 33]:
        tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-5, "S(x)"] * tabla1985.loc[i, "P(x+5)"]
        
    tabla1985.loc[0, "FACTOR ANUAL"] = (tabla1985.loc[0, "S(x)"] / tabla1985.loc[3, "S(x)"]) ** (1/3)

    for i in [3, 8, 13, 18, 23, 28]:
        tabla1985.loc[i, "FACTOR ANUAL"] = (tabla1985.loc[i, "S(x)"] / tabla1985.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 33):
        if i not in [3, 8, 13, 18, 23, 28]:
            tabla1985.loc[i, "FACTOR ANUAL"] = tabla1985.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 33):
        if i not in [3, 8, 13, 18, 23, 28]:
            if tabla1985.loc[i, "FACTOR ANUAL"] == 1:
                tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1, "S(x)"] / tabla1985.loc[i, "FACTOR ANUAL"]
            else: tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1, "S(x)"] / tabla1985.loc[i, "FACTOR ANUAL"]
            
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1985.loc[33, "P(x+5)"] == 1:
        tabla1985.loc[33, "S(x)"] = tabla1985.loc[32, "S(x)"] * tabla1985.loc[33, "P(x+5)"]
    else: tabla1985.loc[33, "S(x)"] = tabla1985.loc[28, "S(x)"] * tabla1985.loc[33, "P(x+5)"]
    
    if tabla1985.loc[38, "P(x+5)"] == 1:
        tabla1985.loc[33, "FACTOR ANUAL"] = 1
    else: tabla1985.loc[33, "FACTOR ANUAL"] = (tabla1985.loc[33, "S(x)"] / ((tabla1985.loc[33, "S(x)"] * tabla1985.loc[38, "P(x+5)"]))) ** (1/5)    

    for i in range(34, 38):
        if tabla1985.loc[38, "P(x+5)"] == 1:
            tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1, "S(x)"] * tabla1985.loc[i, "P(x+5)"]
        else: tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1 , "S(x)"] / tabla1985.loc[33, "FACTOR ANUAL"]        
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1985.loc[38, "P(x+5)"] == 1:
        tabla1985.loc[38, "S(x)"] = tabla1985.loc[37, "S(x)"] * tabla1985.loc[38, "P(x+5)"]
    else: tabla1985.loc[38, "S(x)"] = tabla1985.loc[33, "S(x)"] * tabla1985.loc[38, "P(x+5)"]

    #i+5   
    if tabla1985.loc[43, "P(x+5)"] == 1:
        tabla1985.loc[38, "FACTOR ANUAL"] = 1
    else: tabla1985.loc[38, "FACTOR ANUAL"] = (tabla1985.loc[38, "S(x)"] / ((tabla1985.loc[38, "S(x)"] * tabla1985.loc[43, "P(x+5)"]))) ** (1/5)    

    for i in range(39, 43):
        if tabla1985.loc[43, "P(x+5)"] == 1:
            tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1, "S(x)"] * tabla1985.loc[i, "P(x+5)"]
        else: tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1 , "S(x)"] / tabla1985.loc[38, "FACTOR ANUAL"]
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1985.loc[43, "P(x+5)"] == 1:
        tabla1985.loc[43, "S(x)"] = tabla1985.loc[42, "S(x)"] * tabla1985.loc[43, "P(x+5)"]
    else: tabla1985.loc[43, "S(x)"] = tabla1985.loc[38, "S(x)"] * tabla1985.loc[43, "P(x+5)"]
    
    if tabla1985.loc[48, "P(x+5)"] == 1:
        tabla1985.loc[43, "FACTOR ANUAL"] = 1
    else: tabla1985.loc[43, "FACTOR ANUAL"] = (tabla1985.loc[43, "S(x)"] / ((tabla1985.loc[43, "S(x)"] * tabla1985.loc[48, "P(x+5)"]))) ** (1/5)    

    for i in range(44, 48):
        if tabla1985.loc[48, "P(x+5)"] == 1 or tabla1985.loc[43, "P(x+5)"] == 1:
            tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1, "S(x)"] * tabla1985.loc[i, "P(x+5)"]
        else: tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1 , "S(x)"] / tabla1985.loc[43, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1985.loc[48, "P(x+5)"] == 1:
        tabla1985.loc[48, "S(x)"] = tabla1985.loc[47, "S(x)"] * tabla1985.loc[48, "P(x+5)"]
    else: tabla1985.loc[48, "S(x)"] = tabla1985.loc[43, "S(x)"] * tabla1985.loc[48, "P(x+5)"]

    if tabla1985.loc[53, "P(x+5)"] == 1:
        tabla1985.loc[48, "FACTOR ANUAL"] = 1
    else: tabla1985.loc[48, "FACTOR ANUAL"] = (tabla1985.loc[48, "S(x)"] / ((tabla1985.loc[48, "S(x)"] * tabla1985.loc[53, "P(x+5)"]))) ** (1/5) 

    for i in range(49, 53):
        if tabla1985.loc[53, "P(x+5)"] == 1 or tabla1985.loc[48, "P(x+5)"] == 1:
            tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1, "S(x)"] * tabla1985.loc[i, "P(x+5)"]
        else: tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1 , "S(x)"] / tabla1985.loc[48, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1985.loc[53, "P(x+5)"] == 1:
        tabla1985.loc[53, "S(x)"] = tabla1985.loc[52, "S(x)"] * tabla1985.loc[53, "P(x+5)"]
    else: tabla1985.loc[53, "S(x)"] = tabla1985.loc[48, "S(x)"] * tabla1985.loc[53, "P(x+5)"]

    if tabla1985.loc[58, "P(x+5)"] == 1:
        tabla1985.loc[53, "FACTOR ANUAL"] = 1
    else: tabla1985.loc[53, "FACTOR ANUAL"] = (tabla1985.loc[53, "S(x)"] / ((tabla1985.loc[53, "S(x)"] * tabla1985.loc[58, "P(x+5)"]))) ** (1/5) 

    for i in range(54, 58):
        if tabla1985.loc[58, "P(x+5)"] == 1 or tabla1985.loc[53, "P(x+5)"] == 1:
            tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1, "S(x)"] * tabla1985.loc[i, "P(x+5)"]
        else: tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1 , "S(x)"] / tabla1985.loc[53, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1985.loc[58, "P(x+5)"] == 1:
        tabla1985.loc[58, "S(x)"] = tabla1985.loc[57, "S(x)"] * tabla1985.loc[58, "P(x+5)"]
    else: tabla1985.loc[58, "S(x)"] = tabla1985.loc[53, "S(x)"] * tabla1985.loc[58, "P(x+5)"]

    for i in range(59, 61):
        if tabla1985.loc[i-1, "P(x+5)"] == 1:
            tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1, "S(x)"] * tabla1985.loc[i, "P(x+5)"]
        else: tabla1985.loc[i, "S(x)"] = tabla1985.loc[i-1, "S(x)"] * tabla1985.loc[i, "P(x+5)"]  

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1986 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1986] = tabla1986

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1986.loc[2, "P(x+5)"] = GENERACION_1986.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1986
    tabla1986.loc[3: 6, "P(x+5)"] = tabla1986.loc[2, "P(x+5)"]
    tabla1986.loc[7, "P(x+5)"] = GENERACION_1986.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1986.loc[8: 11, "P(x+5)"] = tabla1986.loc[7, "P(x+5)"]
    tabla1986.loc[12, "P(x+5)"] = GENERACION_1986.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1986.loc[13: 16, "P(x+5)"] = tabla1986.loc[12, "P(x+5)"]
    tabla1986.loc[17, "P(x+5)"] = GENERACION_1986.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1986.loc[18: 21, "P(x+5)"] = tabla1986.loc[17, "P(x+5)"]
    tabla1986.loc[22, "P(x+5)"] = GENERACION_1986.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1986.loc[23: 26, "P(x+5)"] = tabla1986.loc[22, "P(x+5)"]
    tabla1986.loc[27, "P(x+5)"] = GENERACION_1986.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1986.loc[28: 31, "P(x+5)"] = tabla1986.loc[27, "P(x+5)"]
    tabla1986.loc[32, "P(x+5)"] = GENERACION_1986.loc[5, "PROBABILIDAD QUINQUENAL"]
    tabla1986.loc[37, "P(x+5)"] = GENERACION_1986.loc[6, "PROBABILIDAD QUINQUENAL"]

    for i in [42, 47, 52, 57]:
        if tabla1986.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1986 <= 1:
            tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1986
        else:
            tabla1986.loc[i, "P(x+5)"] = 1

    for i in range(32, 38):
        if i not in [32, 37]:
            if (tabla1986.loc[32, "P(x+5)"] == 1 or tabla1986.loc[37, "P(x+5)"] == 1):
                if tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5)) >= 1:
                    tabla1986.loc[i, "P(x+5)"] = 1
                else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5))
            else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"] 

    for i in range(37, 43):
        if i not in [37, 42]:
            if (tabla1986.loc[37, "P(x+5)"] == 1 or tabla1986.loc[42, "P(x+5)"] == 1):
                if tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5)) >= 1:
                    tabla1986.loc[i, "P(x+5)"] = 1
                else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5))
            else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"] 

    for i in range(42, 48):
        if i not in [42, 47]:
            if (tabla1986.loc[42, "P(x+5)"] == 1 or tabla1986.loc[47, "P(x+5)"] == 1):
                if tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5)) >= 1:
                    tabla1986.loc[i, "P(x+5)"] = 1
                else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5))
            else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"]  

    for i in range(47, 53):
        if i not in [47, 52]:
            if (tabla1986.loc[47, "P(x+5)"] == 1 or tabla1986.loc[52, "P(x+5)"] == 1):
                if tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5)) >= 1:
                    tabla1986.loc[i, "P(x+5)"] = 1
                else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5))
            else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"]  
            
    for i in range(52, 58):
        if i not in [52, 57]:
            if (tabla1986.loc[52, "P(x+5)"] == 1 or tabla1986.loc[57, "P(x+5)"] == 1):
                if tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5)) >= 1:
                    tabla1986.loc[i, "P(x+5)"] = 1
                else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5))
            else: tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"]

    for i in range(58, 61):
        if tabla1986.loc[i-1, "P(x+5)"] == 1:
            tabla1986.loc[i, "P(x+5)"] = 1
        if tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5)) < 1:
            tabla1986.loc[i, "P(x+5)"] = tabla1986.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1986 ** (1/5))
        else: tabla1986.loc[i, "P(x+5)"] = 1 

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1986.loc[0, "S(x)"] = 100000
    tabla1986.loc[2, "S(x)"] = tabla1986.loc[0, "S(x)"] * tabla1986.loc[2, "P(x+5)"]

    for i in [7, 12, 17, 22, 27, 32]:
        tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-5, "S(x)"] * tabla1986.loc[i, "P(x+5)"]
        
    tabla1986.loc[0, "FACTOR ANUAL"] = (tabla1986.loc[0, "S(x)"] / tabla1986.loc[2, "S(x)"]) ** (1/2)

    for i in [2, 7, 12, 17, 22, 27]:
        tabla1986.loc[i, "FACTOR ANUAL"] = (tabla1986.loc[i, "S(x)"] / tabla1986.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 32):
        if i not in [2, 7, 12, 17, 22, 27]:
            tabla1986.loc[i, "FACTOR ANUAL"] = tabla1986.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 32):
        if i not in [2, 7, 12, 17, 22, 27]:
            if tabla1986.loc[i, "FACTOR ANUAL"] == 1:
                tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1, "S(x)"] / tabla1986.loc[i, "FACTOR ANUAL"]
            else: tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1, "S(x)"] / tabla1986.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1986.loc[32, "P(x+5)"] == 1:
        tabla1986.loc[32, "S(x)"] = tabla1986.loc[31, "S(x)"] * tabla1986.loc[32, "P(x+5)"]
    else: tabla1986.loc[32, "S(x)"] = tabla1986.loc[27, "S(x)"] * tabla1986.loc[32, "P(x+5)"]
    
    if tabla1986.loc[37, "P(x+5)"] == 1:
        tabla1986.loc[32, "FACTOR ANUAL"] = 1
    else: tabla1986.loc[32, "FACTOR ANUAL"] = (tabla1986.loc[32, "S(x)"] / ((tabla1986.loc[32, "S(x)"] * tabla1986.loc[37, "P(x+5)"]))) ** (1/5)    

    for i in range(33, 37):
        if tabla1986.loc[37, "P(x+5)"] == 1:
            tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1, "S(x)"] * tabla1986.loc[i, "P(x+5)"]
        else: tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1 , "S(x)"] / tabla1986.loc[32, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1986.loc[37, "P(x+5)"] == 1:
        tabla1986.loc[37, "S(x)"] = tabla1986.loc[36, "S(x)"] * tabla1986.loc[37, "P(x+5)"]
    else: tabla1986.loc[37, "S(x)"] = tabla1986.loc[32, "S(x)"] * tabla1986.loc[37, "P(x+5)"]

    #i+5   
    if tabla1986.loc[42, "P(x+5)"] == 1:
        tabla1986.loc[37, "FACTOR ANUAL"] = 1
    else: tabla1986.loc[37, "FACTOR ANUAL"] = (tabla1986.loc[37, "S(x)"] / ((tabla1986.loc[37, "S(x)"] * tabla1986.loc[42, "P(x+5)"]))) ** (1/5)    

    for i in range(38, 42):
        if tabla1986.loc[42, "P(x+5)"] == 1:
            tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1, "S(x)"] * tabla1986.loc[i, "P(x+5)"]
        else: tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1 , "S(x)"] / tabla1986.loc[37, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1986.loc[42, "P(x+5)"] == 1:
        tabla1986.loc[42, "S(x)"] = tabla1986.loc[41, "S(x)"] * tabla1986.loc[42, "P(x+5)"]
    else: tabla1986.loc[42, "S(x)"] = tabla1986.loc[37, "S(x)"] * tabla1986.loc[42, "P(x+5)"]
    
    if tabla1986.loc[47, "P(x+5)"] == 1:
        tabla1986.loc[42, "FACTOR ANUAL"] = 1
    else: tabla1986.loc[42, "FACTOR ANUAL"] = (tabla1986.loc[42, "S(x)"] / ((tabla1986.loc[42, "S(x)"] * tabla1986.loc[47, "P(x+5)"]))) ** (1/5)    

    for i in range(43, 47):
        if tabla1986.loc[47, "P(x+5)"] == 1 or tabla1986.loc[42, "P(x+5)"] == 1:
            tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1, "S(x)"] * tabla1986.loc[i, "P(x+5)"]
        else: tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1 , "S(x)"] / tabla1986.loc[42, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1986.loc[47, "P(x+5)"] == 1:
        tabla1986.loc[47, "S(x)"] = tabla1986.loc[46, "S(x)"] * tabla1986.loc[47, "P(x+5)"]
    else: tabla1986.loc[47, "S(x)"] = tabla1986.loc[42, "S(x)"] * tabla1986.loc[47, "P(x+5)"]

    if tabla1986.loc[52, "P(x+5)"] == 1:
        tabla1986.loc[47, "FACTOR ANUAL"] = 1
    else: tabla1986.loc[47, "FACTOR ANUAL"] = (tabla1986.loc[47, "S(x)"] / ((tabla1986.loc[47, "S(x)"] * tabla1986.loc[52, "P(x+5)"]))) ** (1/5) 

    for i in range(48, 52):
        if tabla1986.loc[52, "P(x+5)"] == 1 or tabla1986.loc[47, "P(x+5)"] == 1:
            tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1, "S(x)"] * tabla1986.loc[i, "P(x+5)"]
        else: tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1 , "S(x)"] / tabla1986.loc[47, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1986.loc[52, "P(x+5)"] == 1:
        tabla1986.loc[52, "S(x)"] = tabla1986.loc[51, "S(x)"] * tabla1986.loc[52, "P(x+5)"]
    else: tabla1986.loc[52, "S(x)"] = tabla1986.loc[47, "S(x)"] * tabla1986.loc[52, "P(x+5)"]

    if tabla1986.loc[57, "P(x+5)"] == 1:
        tabla1986.loc[52, "FACTOR ANUAL"] = 1
    else: tabla1986.loc[52, "FACTOR ANUAL"] = (tabla1986.loc[52, "S(x)"] / ((tabla1986.loc[52, "S(x)"] * tabla1986.loc[57, "P(x+5)"]))) ** (1/5) 

    for i in range(53, 57):
        if tabla1986.loc[57, "P(x+5)"] == 1 or tabla1986.loc[52, "P(x+5)"] == 1:
            tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1, "S(x)"] * tabla1986.loc[i, "P(x+5)"]
        else: tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1 , "S(x)"] / tabla1986.loc[52, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1986.loc[57, "P(x+5)"] == 1:
        tabla1986.loc[57, "S(x)"] = tabla1986.loc[56, "S(x)"] * tabla1986.loc[57, "P(x+5)"]
    else: tabla1986.loc[57, "S(x)"] = tabla1986.loc[52, "S(x)"] * tabla1986.loc[57, "P(x+5)"]

    for i in range(58, 61):
        if tabla1986.loc[i-1, "P(x+5)"] == 1:
            tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1, "S(x)"] * tabla1986.loc[i, "P(x+5)"]
        else: tabla1986.loc[i, "S(x)"] = tabla1986.loc[i-1, "S(x)"] * tabla1986.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1987 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1987] = tabla1987

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1987.loc[1, "P(x+5)"] = GENERACION_1987.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1987
    tabla1987.loc[2: 5, "P(x+5)"] = tabla1987.loc[1, "P(x+5)"]
    tabla1987.loc[6, "P(x+5)"] = GENERACION_1987.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1987.loc[7: 10, "P(x+5)"] = tabla1987.loc[6, "P(x+5)"]
    tabla1987.loc[11, "P(x+5)"] = GENERACION_1987.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1987.loc[12: 15, "P(x+5)"] = tabla1987.loc[11, "P(x+5)"]
    tabla1987.loc[16, "P(x+5)"] = GENERACION_1987.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1987.loc[17: 20, "P(x+5)"] = tabla1987.loc[16, "P(x+5)"]
    tabla1987.loc[21, "P(x+5)"] = GENERACION_1987.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1987.loc[22: 25, "P(x+5)"] = tabla1987.loc[21, "P(x+5)"]
    tabla1987.loc[26, "P(x+5)"] = GENERACION_1987.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1987.loc[27: 30, "P(x+5)"] = tabla1987.loc[26, "P(x+5)"]
    tabla1987.loc[31, "P(x+5)"] = GENERACION_1987.loc[5, "PROBABILIDAD QUINQUENAL"]
    tabla1987.loc[36, "P(x+5)"] = GENERACION_1987.loc[6, "PROBABILIDAD QUINQUENAL"]

    for i in [41, 46, 51, 56]:
        if tabla1987.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1987 <= 1:
            tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1987
        else:
            tabla1987.loc[i, "P(x+5)"] = 1

    for i in range(31, 37):
        if i not in [31, 36]:
            if (tabla1987.loc[31, "P(x+5)"] == 1 or tabla1987.loc[36, "P(x+5)"] == 1):
                if tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5)) >= 1:
                    tabla1987.loc[i, "P(x+5)"] = 1
                else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5))
            else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"] 

    for i in range(36, 42):
        if i not in [36, 41]:
            if (tabla1987.loc[36, "P(x+5)"] == 1 or tabla1987.loc[41, "P(x+5)"] == 1):
                if tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5)) >= 1:
                    tabla1987.loc[i, "P(x+5)"] = 1
                else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5))
            else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"] 

    for i in range(41, 47):
        if i not in [41, 46]:
            if (tabla1987.loc[41, "P(x+5)"] == 1 or tabla1987.loc[46, "P(x+5)"] == 1):
                if tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5)) >= 1:
                    tabla1987.loc[i, "P(x+5)"] = 1
                else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5))
            else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"]  

    for i in range(46, 52):
        if i not in [46, 51]:
            if (tabla1987.loc[46, "P(x+5)"] == 1 or tabla1987.loc[51, "P(x+5)"] == 1):
                if tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5)) >= 1:
                    tabla1987.loc[i, "P(x+5)"] = 1
                else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5))
            else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"]  
            
    for i in range(51, 57):
        if i not in [51, 56]:
            if (tabla1987.loc[51, "P(x+5)"] == 1 or tabla1987.loc[56, "P(x+5)"] == 1):
                if tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5)) >= 1:
                    tabla1987.loc[i, "P(x+5)"] = 1
                else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5))
            else: tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"]

    for i in range(57, 61):
        if tabla1987.loc[i-1, "P(x+5)"] == 1:
            tabla1987.loc[i, "P(x+5)"] = 1
        if tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5)) < 1:
            tabla1987.loc[i, "P(x+5)"] = tabla1987.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1987 ** (1/5))
        else: tabla1987.loc[i, "P(x+5)"] = 1 
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1987.loc[0, "S(x)"] = 100000
    tabla1987.loc[1, "S(x)"] = tabla1987.loc[0, "S(x)"] * tabla1987.loc[1, "P(x+5)"]

    for i in [6, 11, 16, 21, 26, 31]:
        tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-5, "S(x)"] * tabla1987.loc[i, "P(x+5)"]
        
    #tabla1987.loc[0, "FACTOR ANUAL"] = (tabla1987.loc[0, "S(x)"] / tabla1987.loc[1, "S(x)"]) ** (1/5)

    for i in [1, 6, 11, 16, 21, 26]:
        tabla1987.loc[i, "FACTOR ANUAL"] = (tabla1987.loc[i, "S(x)"] / tabla1987.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 31):
        if i not in [1, 6, 11, 16, 21, 26]:
            tabla1987.loc[i, "FACTOR ANUAL"] = tabla1987.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 31):
        if i not in [1, 6, 11, 16, 21, 26]:
            if tabla1987.loc[i, "FACTOR ANUAL"] == 1:
                tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1, "S(x)"] / tabla1987.loc[i, "FACTOR ANUAL"]
            else: tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1, "S(x)"] / tabla1987.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1987.loc[31, "P(x+5)"] == 1:
        tabla1987.loc[31, "S(x)"] = tabla1987.loc[30, "S(x)"] * tabla1987.loc[31, "P(x+5)"]
    else: tabla1987.loc[31, "S(x)"] = tabla1987.loc[26, "S(x)"] * tabla1987.loc[31, "P(x+5)"]
    
    if tabla1987.loc[36, "P(x+5)"] == 1:
        tabla1987.loc[31, "FACTOR ANUAL"] = 1
    else: tabla1987.loc[31, "FACTOR ANUAL"] = (tabla1987.loc[31, "S(x)"] / ((tabla1987.loc[31, "S(x)"] * tabla1987.loc[36, "P(x+5)"]))) ** (1/5)    

    for i in range(32, 36):
        if tabla1987.loc[36, "P(x+5)"] == 1:
            tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1, "S(x)"] * tabla1987.loc[i, "P(x+5)"]
        else: tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1 , "S(x)"] / tabla1987.loc[31, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1987.loc[36, "P(x+5)"] == 1:
        tabla1987.loc[36, "S(x)"] = tabla1987.loc[35, "S(x)"] * tabla1987.loc[36, "P(x+5)"]
    else: tabla1987.loc[36, "S(x)"] = tabla1987.loc[31, "S(x)"] * tabla1987.loc[36, "P(x+5)"]

    #i+5   
    if tabla1987.loc[41, "P(x+5)"] == 1:
        tabla1987.loc[36, "FACTOR ANUAL"] = 1
    else: tabla1987.loc[36, "FACTOR ANUAL"] = (tabla1987.loc[36, "S(x)"] / ((tabla1987.loc[36, "S(x)"] * tabla1987.loc[41, "P(x+5)"]))) ** (1/5)    

    for i in range(37, 41):
        if tabla1987.loc[41, "P(x+5)"] == 1:
            tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1, "S(x)"] * tabla1987.loc[i, "P(x+5)"]
        else: tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1 , "S(x)"] / tabla1987.loc[36, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1987.loc[41, "P(x+5)"] == 1:
        tabla1987.loc[41, "S(x)"] = tabla1987.loc[40, "S(x)"] * tabla1987.loc[41, "P(x+5)"]
    else: tabla1987.loc[41, "S(x)"] = tabla1987.loc[36, "S(x)"] * tabla1987.loc[41, "P(x+5)"]
    
    if tabla1987.loc[46, "P(x+5)"] == 1:
        tabla1987.loc[41, "FACTOR ANUAL"] = 1
    else: tabla1987.loc[41, "FACTOR ANUAL"] = (tabla1987.loc[41, "S(x)"] / ((tabla1987.loc[41, "S(x)"] * tabla1987.loc[46, "P(x+5)"]))) ** (1/5)    

    for i in range(42, 46):
        if tabla1987.loc[46, "P(x+5)"] == 1 or tabla1987.loc[41, "P(x+5)"] == 1:
            tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1, "S(x)"] * tabla1987.loc[i, "P(x+5)"]
        else: tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1 , "S(x)"] / tabla1987.loc[41, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1987.loc[46, "P(x+5)"] == 1:
        tabla1987.loc[46, "S(x)"] = tabla1987.loc[45, "S(x)"] * tabla1987.loc[46, "P(x+5)"]
    else: tabla1987.loc[46, "S(x)"] = tabla1987.loc[41, "S(x)"] * tabla1987.loc[46, "P(x+5)"]

    if tabla1987.loc[51, "P(x+5)"] == 1:
        tabla1987.loc[46, "FACTOR ANUAL"] = 1
    else: tabla1987.loc[46, "FACTOR ANUAL"] = (tabla1987.loc[46, "S(x)"] / ((tabla1987.loc[46, "S(x)"] * tabla1987.loc[51, "P(x+5)"]))) ** (1/5) 

    for i in range(47, 51):
        if tabla1987.loc[51, "P(x+5)"] == 1 or tabla1987.loc[46, "P(x+5)"] == 1:
            tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1, "S(x)"] * tabla1987.loc[i, "P(x+5)"]
        else: tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1 , "S(x)"] / tabla1987.loc[46, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1987.loc[51, "P(x+5)"] == 1:
        tabla1987.loc[51, "S(x)"] = tabla1987.loc[50, "S(x)"] * tabla1987.loc[52, "P(x+5)"]
    else: tabla1987.loc[51, "S(x)"] = tabla1987.loc[46, "S(x)"] * tabla1987.loc[51, "P(x+5)"]

    if tabla1987.loc[56, "P(x+5)"] == 1:
        tabla1987.loc[51, "FACTOR ANUAL"] = 1
    else: tabla1987.loc[51, "FACTOR ANUAL"] = (tabla1987.loc[51, "S(x)"] / ((tabla1987.loc[51, "S(x)"] * tabla1987.loc[56, "P(x+5)"]))) ** (1/5) 

    for i in range(52, 56):
        if tabla1987.loc[56, "P(x+5)"] == 1 or tabla1987.loc[51, "P(x+5)"] == 1:
            tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1, "S(x)"] * tabla1987.loc[i, "P(x+5)"]
        else: tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1 , "S(x)"] / tabla1987.loc[51, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1987.loc[56, "P(x+5)"] == 1:
        tabla1987.loc[56, "S(x)"] = tabla1987.loc[55, "S(x)"] * tabla1987.loc[56, "P(x+5)"]
    else: tabla1987.loc[56, "S(x)"] = tabla1987.loc[51, "S(x)"] * tabla1987.loc[56, "P(x+5)"]

    for i in range(57, 61):
        if tabla1987.loc[i-1, "P(x+5)"] == 1:
            tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1, "S(x)"] * tabla1987.loc[i, "P(x+5)"]
        else: tabla1987.loc[i, "S(x)"] = tabla1987.loc[i-1, "S(x)"] * tabla1987.loc[i, "P(x+5)"]  

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1988 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1988] = tabla1988

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1988.loc[5, "P(x+5)"] = GENERACION_1988.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1988.loc[6: 9, "P(x+5)"] = tabla1988.loc[5, "P(x+5)"]
    tabla1988.loc[10, "P(x+5)"] = GENERACION_1988.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1988.loc[11: 14, "P(x+5)"] = tabla1988.loc[10, "P(x+5)"]
    tabla1988.loc[15, "P(x+5)"] = GENERACION_1988.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1988.loc[16: 19, "P(x+5)"] = tabla1988.loc[15, "P(x+5)"]
    tabla1988.loc[20, "P(x+5)"] = GENERACION_1988.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1988.loc[21: 24, "P(x+5)"] = tabla1988.loc[20, "P(x+5)"]
    tabla1988.loc[25, "P(x+5)"] = GENERACION_1988.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1988.loc[26: 29, "P(x+5)"] = tabla1988.loc[25, "P(x+5)"]
    tabla1988.loc[30, "P(x+5)"] = GENERACION_1988.loc[5, "PROBABILIDAD QUINQUENAL"]
    tabla1988.loc[31: 34, "P(x+5)"] = tabla1988.loc[30, "P(x+5)"]
    tabla1988.loc[35, "P(x+5)"] = GENERACION_1988.loc[6, "PROBABILIDAD QUINQUENAL"]
    tabla1988.loc[40, "P(x+5)"] = GENERACION_1988.loc[7, "PROBABILIDAD QUINQUENAL"]

    for i in [45, 50, 55, 60]:
        if tabla1988.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1988 <= 1:
            tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1988
        else:
            tabla1988.loc[i, "P(x+5)"] = 1

    for i in range(35, 41):
        if i not in [35, 40]:
            if (tabla1988.loc[35, "P(x+5)"] == 1 or tabla1988.loc[40, "P(x+5)"] == 1):
                if tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5)) >= 1:
                    tabla1988.loc[i, "P(x+5)"] = 1
                else: tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5))
            else: tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-1, "P(x+5)"] 

    for i in range(40, 46):
        if i not in [40, 45]:
            if (tabla1988.loc[40, "P(x+5)"] == 1 or tabla1988.loc[45, "P(x+5)"] == 1):
                if tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5)) >= 1:
                    tabla1988.loc[i, "P(x+5)"] = 1
                else: tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5))
            else: tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-1, "P(x+5)"] 

    for i in range(45, 51):
        if i not in [45, 50]:
            if (tabla1988.loc[45, "P(x+5)"] == 1 or tabla1988.loc[50, "P(x+5)"] == 1):
                if tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5)) >= 1:
                    tabla1988.loc[i, "P(x+5)"] = 1
                else: tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5))
            else: tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-1, "P(x+5)"]  

    for i in range(50, 56):
        if i not in [50, 55]:
            if (tabla1988.loc[50, "P(x+5)"] == 1 or tabla1988.loc[55, "P(x+5)"] == 1):
                if tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5)) >= 1:
                    tabla1988.loc[i, "P(x+5)"] = 1
                else: tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5))
            else: tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-1, "P(x+5)"]  
            
    for i in range(56, 61):
        if i not in [60]:
            if tabla1988.loc[i-1, "P(x+5)"] == 1:
                tabla1988.loc[i, "P(x+5)"] = 1
            if tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5)) < 1:
                tabla1988.loc[i, "P(x+5)"] = tabla1988.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1988 ** (1/5))
            else: tabla1988.loc[i, "P(x+5)"] = 1 
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1988.loc[0, "S(x)"] = 100000
    tabla1988.loc[5, "S(x)"] = tabla1988.loc[0, "S(x)"] * tabla1988.loc[5, "P(x+5)"]

    for i in [10, 15, 20, 25, 30, 35]:
        tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-5, "S(x)"] * tabla1988.loc[i, "P(x+5)"]
        
    tabla1988.loc[0, "FACTOR ANUAL"] = (tabla1988.loc[0, "S(x)"] / tabla1988.loc[5, "S(x)"]) ** (1/5)

    for i in [5, 10, 15, 20, 25, 30]:
        tabla1988.loc[i, "FACTOR ANUAL"] = (tabla1988.loc[i, "S(x)"] / tabla1988.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 35):
        if i not in [5, 10, 15, 20, 25, 30]:
            tabla1988.loc[i, "FACTOR ANUAL"] = tabla1988.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 35):
        if i not in [5, 10, 15, 20, 25, 30]:
            if tabla1988.loc[i, "FACTOR ANUAL"] == 1:
                tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1, "S(x)"] / tabla1988.loc[i, "FACTOR ANUAL"]
            else: tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1, "S(x)"] / tabla1988.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1988.loc[35, "P(x+5)"] == 1:
        tabla1988.loc[35, "S(x)"] = tabla1988.loc[34, "S(x)"] * tabla1988.loc[35, "P(x+5)"]
    else: tabla1988.loc[35, "S(x)"] = tabla1988.loc[30, "S(x)"] * tabla1988.loc[35, "P(x+5)"]
    
    if tabla1988.loc[40, "P(x+5)"] == 1:
        tabla1988.loc[35, "FACTOR ANUAL"] = 1
    else: tabla1988.loc[35, "FACTOR ANUAL"] = (tabla1988.loc[35, "S(x)"] / ((tabla1988.loc[35, "S(x)"] * tabla1988.loc[40, "P(x+5)"]))) ** (1/5)    

    for i in range(36, 40):
        if tabla1988.loc[40, "P(x+5)"] == 1:
            tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1, "S(x)"] * tabla1988.loc[i, "P(x+5)"]
        else: tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1 , "S(x)"] / tabla1988.loc[35, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1988.loc[40, "P(x+5)"] == 1:
        tabla1988.loc[40, "S(x)"] = tabla1988.loc[39, "S(x)"] * tabla1988.loc[40, "P(x+5)"]
    else: tabla1988.loc[40, "S(x)"] = tabla1988.loc[35, "S(x)"] * tabla1988.loc[40, "P(x+5)"]

    #i+5   
    if tabla1988.loc[45, "P(x+5)"] == 1:
        tabla1988.loc[40, "FACTOR ANUAL"] = 1
    else: tabla1988.loc[40, "FACTOR ANUAL"] = (tabla1988.loc[40, "S(x)"] / ((tabla1988.loc[40, "S(x)"] * tabla1988.loc[45, "P(x+5)"]))) ** (1/5)    

    for i in range(41, 45):
        if tabla1988.loc[45, "P(x+5)"] == 1:
            tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1, "S(x)"] * tabla1988.loc[i, "P(x+5)"]
        else: tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1 , "S(x)"] / tabla1988.loc[40, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1988.loc[45, "P(x+5)"] == 1:
        tabla1988.loc[45, "S(x)"] = tabla1988.loc[44, "S(x)"] * tabla1988.loc[45, "P(x+5)"]
    else: tabla1988.loc[45, "S(x)"] = tabla1988.loc[40, "S(x)"] * tabla1988.loc[45, "P(x+5)"]
    
    if tabla1988.loc[50, "P(x+5)"] == 1:
        tabla1988.loc[45, "FACTOR ANUAL"] = 1
    else: tabla1988.loc[45, "FACTOR ANUAL"] = (tabla1988.loc[45, "S(x)"] / ((tabla1988.loc[45, "S(x)"] * tabla1988.loc[50, "P(x+5)"]))) ** (1/5)    

    for i in range(46, 50):
        if tabla1988.loc[50, "P(x+5)"] == 1 or tabla1988.loc[45, "P(x+5)"] == 1:
            tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1, "S(x)"] * tabla1988.loc[i, "P(x+5)"]
        else: tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1 , "S(x)"] / tabla1988.loc[45, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1988.loc[50, "P(x+5)"] == 1:
        tabla1988.loc[50, "S(x)"] = tabla1988.loc[49, "S(x)"] * tabla1988.loc[50, "P(x+5)"]
    else: tabla1988.loc[50, "S(x)"] = tabla1988.loc[45, "S(x)"] * tabla1988.loc[50, "P(x+5)"]

    if tabla1988.loc[55, "P(x+5)"] == 1:
        tabla1988.loc[50, "FACTOR ANUAL"] = 1
    else: tabla1988.loc[50, "FACTOR ANUAL"] = (tabla1988.loc[50, "S(x)"] / ((tabla1988.loc[50, "S(x)"] * tabla1988.loc[55, "P(x+5)"]))) ** (1/5) 

    for i in range(51, 55):
        if tabla1988.loc[55, "P(x+5)"] == 1 or tabla1988.loc[50, "P(x+5)"] == 1:
            tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1, "S(x)"] * tabla1988.loc[i, "P(x+5)"]
        else: tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1 , "S(x)"] / tabla1988.loc[50, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    

    if tabla1988.loc[55, "P(x+5)"] == 1:
        tabla1988.loc[55, "S(x)"] = tabla1988.loc[54, "S(x)"] * tabla1988.loc[55, "P(x+5)"]
    else: tabla1988.loc[55, "S(x)"] = tabla1988.loc[50, "S(x)"] * tabla1988.loc[55, "P(x+5)"]

    if tabla1988.loc[60, "P(x+5)"] == 1:
        tabla1988.loc[55, "FACTOR ANUAL"] = 1
    else: tabla1988.loc[55, "FACTOR ANUAL"] = (tabla1988.loc[55, "S(x)"] / ((tabla1988.loc[55, "S(x)"] * tabla1988.loc[60, "P(x+5)"]))) ** (1/5) 

    for i in range(56, 60):
        if tabla1988.loc[60, "P(x+5)"] == 1 or tabla1988.loc[55, "P(x+5)"] == 1:
            tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1, "S(x)"] * tabla1988.loc[i, "P(x+5)"]
        else: tabla1988.loc[i, "S(x)"] = tabla1988.loc[i-1 , "S(x)"] / tabla1988.loc[55, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1988.loc[60, "P(x+5)"] == 1:
        tabla1988.loc[60, "S(x)"] = tabla1988.loc[60, "P(x+5)"] * tabla1988.loc[59, "S(x)"]
    else: tabla1988.loc[60, "S(x)"] = tabla1988.loc[60, "P(x+5)"] * tabla1988.loc[55, "S(x)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1989 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1989] = tabla1989

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1989.loc[4, "P(x+5)"] = GENERACION_1989.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1989
    tabla1989.loc[5: 8, "P(x+5)"] = tabla1989.loc[4, "P(x+5)"]
    tabla1989.loc[9, "P(x+5)"] = GENERACION_1989.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1989.loc[10: 13, "P(x+5)"] = tabla1989.loc[9, "P(x+5)"]
    tabla1989.loc[14, "P(x+5)"] = GENERACION_1989.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1989.loc[15: 18, "P(x+5)"] = tabla1989.loc[14, "P(x+5)"]
    tabla1989.loc[19, "P(x+5)"] = GENERACION_1989.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1989.loc[20: 23, "P(x+5)"] = tabla1989.loc[19, "P(x+5)"]
    tabla1989.loc[24, "P(x+5)"] = GENERACION_1989.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1989.loc[25: 28, "P(x+5)"] = tabla1989.loc[24, "P(x+5)"]
    tabla1989.loc[29, "P(x+5)"] = GENERACION_1989.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1989.loc[34, "P(x+5)"] = GENERACION_1989.loc[5, "PROBABILIDAD QUINQUENAL"]

    for i in [39, 44, 49, 54, 59]:
        if tabla1989.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1989 <= 1:
            tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1989
        else:
            tabla1989.loc[i, "P(x+5)"] = 1

    for i in range(29, 35):
        if i not in [29, 34]:
            if (tabla1989.loc[29, "P(x+5)"] == 1 or tabla1989.loc[34, "P(x+5)"] == 1):
                if tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5)) >= 1:
                    tabla1989.loc[i, "P(x+5)"] = 1
                else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5))
            else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] 

    for i in range(34, 40):
        if i not in [34, 39]:
            if (tabla1989.loc[34, "P(x+5)"] == 1 or tabla1989.loc[39, "P(x+5)"] == 1):
                if tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5)) >= 1:
                    tabla1989.loc[i, "P(x+5)"] = 1
                else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5))
            else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] 

    for i in range(39, 45):
        if i not in [39, 44]:
            if (tabla1989.loc[39, "P(x+5)"] == 1 or tabla1989.loc[44, "P(x+5)"] == 1):
                if tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5)) >= 1:
                    tabla1989.loc[i, "P(x+5)"] = 1
                else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5))
            else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] 

    for i in range(44, 50):
        if i not in [44, 49]:
            if (tabla1989.loc[44, "P(x+5)"] == 1 or tabla1989.loc[49, "P(x+5)"] == 1):
                if tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5)) >= 1:
                    tabla1989.loc[i, "P(x+5)"] = 1
                else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5))
            else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"]  

    for i in range(49, 55):
        if i not in [49, 54]:
            if (tabla1989.loc[49, "P(x+5)"] == 1 or tabla1989.loc[54, "P(x+5)"] == 1):
                if tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5)) >= 1:
                    tabla1989.loc[i, "P(x+5)"] = 1
                else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5))
            else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"]  
            
    for i in range(54, 60):
        if i not in [54, 59]:
            if (tabla1989.loc[54, "P(x+5)"] == 1 or tabla1989.loc[59, "P(x+5)"] == 1):
                if tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5)) >= 1:
                    tabla1989.loc[i, "P(x+5)"] = 1
                else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5))
            else: tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"]

    for i in range(60, 61):
        if tabla1989.loc[i-1, "P(x+5)"] == 1:
            tabla1989.loc[i, "P(x+5)"] = 1
        if tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5)) < 1:
            tabla1989.loc[i, "P(x+5)"] = tabla1989.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1989 ** (1/5))
        else: tabla1989.loc[i, "P(x+5)"] = 1 
    
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1989.loc[0, "S(x)"] = 100000
    tabla1989.loc[4, "S(x)"] = tabla1989.loc[0, "S(x)"] * tabla1989.loc[4, "P(x+5)"]

    for i in [9, 14, 19, 24, 29]:
        tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-5, "S(x)"] * tabla1989.loc[i, "P(x+5)"]
        
    tabla1989.loc[0, "FACTOR ANUAL"] = (tabla1989.loc[0, "S(x)"] / tabla1989.loc[4, "S(x)"]) ** (1/4)

    for i in [4, 9, 14, 19, 24]:
        tabla1989.loc[i, "FACTOR ANUAL"] = (tabla1989.loc[i, "S(x)"] / tabla1989.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 29):
        if i not in [4, 9, 14, 19, 24]:
            tabla1989.loc[i, "FACTOR ANUAL"] = tabla1989.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 29):
        if i not in [4, 9, 14, 19, 24]:
            if tabla1989.loc[i, "FACTOR ANUAL"] == 1:
                tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] / tabla1989.loc[i, "FACTOR ANUAL"]
            else: tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] / tabla1989.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1989.loc[29, "P(x+5)"] == 1:
        tabla1989.loc[29, "S(x)"] = tabla1989.loc[28, "S(x)"] * tabla1989.loc[29, "P(x+5)"]
    else: tabla1989.loc[29, "S(x)"] = tabla1989.loc[24, "S(x)"] * tabla1989.loc[29, "P(x+5)"]
    
    if tabla1989.loc[34, "P(x+5)"] == 1:
        tabla1989.loc[29, "FACTOR ANUAL"] = 1
    else: tabla1989.loc[29, "FACTOR ANUAL"] = (tabla1989.loc[29, "S(x)"] / ((tabla1989.loc[29, "S(x)"] * tabla1989.loc[34, "P(x+5)"]))) ** (1/5)    

    for i in range(30, 34):
        if tabla1989.loc[34, "P(x+5)"] == 1:
            tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] * tabla1989.loc[i, "P(x+5)"]
        else: tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1 , "S(x)"] / tabla1989.loc[29, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1989.loc[34, "P(x+5)"] == 1:
        tabla1989.loc[34, "S(x)"] = tabla1989.loc[33, "S(x)"] * tabla1989.loc[34, "P(x+5)"]
    else: tabla1989.loc[34, "S(x)"] = tabla1989.loc[29, "S(x)"] * tabla1989.loc[34, "P(x+5)"]
    
    if tabla1989.loc[39, "P(x+5)"] == 1:
        tabla1989.loc[34, "FACTOR ANUAL"] = 1
    else: tabla1989.loc[34, "FACTOR ANUAL"] = (tabla1989.loc[34, "S(x)"] / ((tabla1989.loc[34, "S(x)"] * tabla1989.loc[39, "P(x+5)"]))) ** (1/5)    

    for i in range(35, 39):
        if tabla1989.loc[39, "P(x+5)"] == 1:
            tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] * tabla1989.loc[i, "P(x+5)"]
        else: tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1 , "S(x)"] / tabla1989.loc[34, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1989.loc[39, "P(x+5)"] == 1:
        tabla1989.loc[39, "S(x)"] = tabla1989.loc[38, "S(x)"] * tabla1989.loc[39, "P(x+5)"]
    else: tabla1989.loc[39, "S(x)"] = tabla1989.loc[34, "S(x)"] * tabla1989.loc[39, "P(x+5)"]

    #i+5   
    if tabla1989.loc[44, "P(x+5)"] == 1:
        tabla1989.loc[39, "FACTOR ANUAL"] = 1
    else: tabla1989.loc[39, "FACTOR ANUAL"] = (tabla1989.loc[39, "S(x)"] / ((tabla1989.loc[39, "S(x)"] * tabla1989.loc[44, "P(x+5)"]))) ** (1/5)    

    for i in range(40, 44):
        if tabla1989.loc[44, "P(x+5)"] == 1 or tabla1989.loc[39, "P(x+5)"] == 1:
            tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] * tabla1989.loc[i, "P(x+5)"]
        else: tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1 , "S(x)"] / tabla1989.loc[39, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1989.loc[44, "P(x+5)"] == 1:
        tabla1989.loc[44, "S(x)"] = tabla1989.loc[43, "S(x)"] * tabla1989.loc[44, "P(x+5)"]
    else: tabla1989.loc[44, "S(x)"] = tabla1989.loc[39, "S(x)"] * tabla1989.loc[44, "P(x+5)"]
    
    if tabla1989.loc[49, "P(x+5)"] == 1:
        tabla1989.loc[44, "FACTOR ANUAL"] = 1
    else: tabla1989.loc[44, "FACTOR ANUAL"] = (tabla1989.loc[44, "S(x)"] / ((tabla1989.loc[44, "S(x)"] * tabla1989.loc[49, "P(x+5)"]))) ** (1/5)    

    for i in range(45, 49):
        if tabla1989.loc[44, "P(x+5)"] == 1 or tabla1989.loc[49, "P(x+5)"] == 1:
            tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] * tabla1989.loc[i, "P(x+5)"]
        else: tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1 , "S(x)"] / tabla1989.loc[44, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1989.loc[49, "P(x+5)"] == 1:
        tabla1989.loc[49, "S(x)"] = tabla1989.loc[48, "S(x)"] * tabla1989.loc[49, "P(x+5)"]
    else: tabla1989.loc[49, "S(x)"] = tabla1989.loc[44, "S(x)"] * tabla1989.loc[49, "P(x+5)"]

    if tabla1989.loc[54, "P(x+5)"] == 1:
        tabla1989.loc[49, "FACTOR ANUAL"] = 1
    else: tabla1989.loc[49, "FACTOR ANUAL"] = (tabla1989.loc[49, "S(x)"] / ((tabla1989.loc[49, "S(x)"] * tabla1989.loc[54, "P(x+5)"]))) ** (1/5) 

    for i in range(50, 54):
        if tabla1989.loc[54, "P(x+5)"] == 1 or tabla1989.loc[49, "P(x+5)"] == 1:
            tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] * tabla1989.loc[i, "P(x+5)"]
        else: tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1 , "S(x)"] / tabla1989.loc[49, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1989.loc[54, "P(x+5)"] == 1:
        tabla1989.loc[54, "S(x)"] = tabla1989.loc[53, "S(x)"] * tabla1989.loc[54, "P(x+5)"]
    else: tabla1989.loc[54, "S(x)"] = tabla1989.loc[49, "S(x)"] * tabla1989.loc[54, "P(x+5)"]

    if tabla1989.loc[59, "P(x+5)"] == 1:
        tabla1989.loc[54, "FACTOR ANUAL"] = 1
    else: tabla1989.loc[54, "FACTOR ANUAL"] = (tabla1989.loc[54, "S(x)"] / ((tabla1989.loc[54, "S(x)"] * tabla1989.loc[59, "P(x+5)"]))) ** (1/5) 

    for i in range(55, 59):
        if tabla1989.loc[59, "P(x+5)"] == 1 or tabla1989.loc[54, "P(x+5)"] == 1:
            tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] * tabla1989.loc[i, "P(x+5)"]
        else: tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1 , "S(x)"] / tabla1989.loc[54, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1989.loc[59, "P(x+5)"] == 1:
        tabla1989.loc[59, "S(x)"] = tabla1989.loc[58, "S(x)"] * tabla1989.loc[59, "P(x+5)"]
    else: tabla1989.loc[59, "S(x)"] = tabla1989.loc[54, "S(x)"] * tabla1989.loc[59, "P(x+5)"]

    for i in range(59, 61):
        if i not in [59]:
            if tabla1989.loc[i-1, "P(x+5)"] == 1:
                tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] * tabla1989.loc[i, "P(x+5)"]
            else: tabla1989.loc[i, "S(x)"] = tabla1989.loc[i-1, "S(x)"] * tabla1989.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla1990 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1990] = tabla1990

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1990.loc[3, "P(x+5)"] = GENERACION_1990.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1990
    tabla1990.loc[4: 7, "P(x+5)"] = tabla1990.loc[3, "P(x+5)"]
    tabla1990.loc[8, "P(x+5)"] = GENERACION_1990.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1990.loc[9: 12, "P(x+5)"] = tabla1990.loc[8, "P(x+5)"]
    tabla1990.loc[13, "P(x+5)"] = GENERACION_1990.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1990.loc[14: 17, "P(x+5)"] = tabla1990.loc[13, "P(x+5)"]
    tabla1990.loc[18, "P(x+5)"] = GENERACION_1990.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1990.loc[19: 22, "P(x+5)"] = tabla1990.loc[18, "P(x+5)"]
    tabla1990.loc[23, "P(x+5)"] = GENERACION_1990.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1990.loc[24: 27, "P(x+5)"] = tabla1990.loc[23, "P(x+5)"]
    tabla1990.loc[28, "P(x+5)"] = GENERACION_1990.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1990.loc[33, "P(x+5)"] = GENERACION_1990.loc[5, "PROBABILIDAD QUINQUENAL"]
        
    for i in [38, 43, 48, 53, 58]:
        if tabla1990.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1990 <= 1:
            tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1990
        else:
            tabla1990.loc[i, "P(x+5)"] = 1
            
    for i in range(28, 34):
        if i not in [28, 33]:
            if (tabla1990.loc[28, "P(x+5)"] == 1 or tabla1990.loc[33, "P(x+5)"] == 1):
                if tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5)) >= 1:
                    tabla1990.loc[i, "P(x+5)"] = 1
                else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5))
            else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"]       

    for i in range(33, 39):
        if i not in [33, 38]:
            if (tabla1990.loc[33, "P(x+5)"] == 1 or tabla1990.loc[38, "P(x+5)"] == 1):
                if tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5)) >= 1:
                    tabla1990.loc[i, "P(x+5)"] = 1
                else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5))
            else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"] 
            
    for i in range(38, 44):
        if i not in [38, 43]:
            if (tabla1990.loc[38, "P(x+5)"] == 1 or tabla1990.loc[43, "P(x+5)"] == 1):
                if tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5)) >= 1:
                    tabla1990.loc[i, "P(x+5)"] = 1
                else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5))
            else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"]  

    for i in range(43, 49):
        if i not in [43, 48]:
            if (tabla1990.loc[43, "P(x+5)"] == 1 or tabla1990.loc[48, "P(x+5)"] == 1):
                if tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5)) >= 1:
                    tabla1990.loc[i, "P(x+5)"] = 1
                else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5))
            else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"]  

    for i in range(48, 54):
        if i not in [48, 53]:
            if (tabla1990.loc[48, "P(x+5)"] == 1 or tabla1990.loc[53, "P(x+5)"] == 1):
                if tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5)) >= 1:
                    tabla1990.loc[i, "P(x+5)"] = 1
                else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5))
            else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"]  
            
    for i in range(53, 59):
        if i not in [53, 58]:
            if (tabla1990.loc[53, "P(x+5)"] == 1 or tabla1990.loc[58, "P(x+5)"] == 1):
                if tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5)) >= 1:
                    tabla1990.loc[i, "P(x+5)"] = 1
                else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5))
            else: tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"]

    for i in range(59, 61):
        if tabla1990.loc[i-1, "P(x+5)"] == 1:
            tabla1990.loc[i, "P(x+5)"] = 1
        if tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5)) < 1:
            tabla1990.loc[i, "P(x+5)"] = tabla1990.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1990 ** (1/5))
        else: tabla1990.loc[i, "P(x+5)"] = 1 
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1990.loc[0, "S(x)"] = 100000
    tabla1990.loc[3, "S(x)"] = tabla1990.loc[0, "S(x)"] * tabla1990.loc[3, "P(x+5)"]

    for i in [8, 13, 18, 23, 28]:
        tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-5, "S(x)"] * tabla1990.loc[i, "P(x+5)"]
        
    tabla1990.loc[0, "FACTOR ANUAL"] = (tabla1990.loc[0, "S(x)"] / tabla1990.loc[3, "S(x)"]) ** (1/3)

    for i in [3, 8, 13, 18, 23]:
        tabla1990.loc[i, "FACTOR ANUAL"] = (tabla1990.loc[i, "S(x)"] / tabla1990.loc[i+5, "S(x)"]) ** (1/5)

    for i in range(1, 28):
        if i not in [3, 8, 13, 18, 23]:
            tabla1990.loc[i, "FACTOR ANUAL"] = tabla1990.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 28):
        if i not in [3, 8, 13, 18, 23]:
            if tabla1990.loc[i, "FACTOR ANUAL"] == 1:
                tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] / tabla1990.loc[i, "FACTOR ANUAL"]
            else: tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] / tabla1990.loc[i, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 28
    if tabla1990.loc[28, "P(x+5)"] == 1:
        tabla1990.loc[28, "S(x)"] = tabla1990.loc[27, "S(x)"] * tabla1990.loc[28, "P(x+5)"]
    else: tabla1990.loc[28, "S(x)"] = tabla1990.loc[23, "S(x)"] * tabla1990.loc[28, "P(x+5)"]

    if tabla1990.loc[33, "P(x+5)"] == 1:
        tabla1990.loc[28, "FACTOR ANUAL"] = 1
    else: tabla1990.loc[28, "FACTOR ANUAL"] = (tabla1990.loc[28, "S(x)"] / ((tabla1990.loc[28, "S(x)"] * tabla1990.loc[33, "P(x+5)"]))) ** (1/5)
    
    for i in range(29, 33):
        if tabla1990.loc[33, "P(x+5)"] == 1:
            tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] * tabla1990.loc[i, "P(x+5)"]
        else: tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1 , "S(x)"] / tabla1990.loc[28, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 33
    if tabla1990.loc[33, "P(x+5)"] == 1:
        tabla1990.loc[33, "S(x)"] = tabla1990.loc[32, "S(x)"] * tabla1990.loc[33, "P(x+5)"]
    else: tabla1990.loc[33, "S(x)"] = tabla1990.loc[28, "S(x)"] * tabla1990.loc[33, "P(x+5)"]
    
    if tabla1990.loc[38, "P(x+5)"] == 1:
        tabla1990.loc[33, "FACTOR ANUAL"] = 1
    else: tabla1990.loc[33, "FACTOR ANUAL"] = (tabla1990.loc[33, "S(x)"] / ((tabla1990.loc[33, "S(x)"] * tabla1990.loc[38, "P(x+5)"]))) ** (1/5)    

    for i in range(34, 38):
        if tabla1990.loc[38, "P(x+5)"] == 1:
            tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] * tabla1990.loc[i, "P(x+5)"]
        else: tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1 , "S(x)"] / tabla1990.loc[33, "FACTOR ANUAL"]
        
            #-----------------------------------------------------------------INTERVALO 38
    if tabla1990.loc[38, "P(x+5)"] == 1:
        tabla1990.loc[38, "S(x)"] = tabla1990.loc[37, "S(x)"] * tabla1990.loc[38, "P(x+5)"]
    else: tabla1990.loc[38, "S(x)"] = tabla1990.loc[33, "S(x)"] * tabla1990.loc[38, "P(x+5)"]

    #i+5   
    if tabla1990.loc[43, "P(x+5)"] == 1:
        tabla1990.loc[38, "FACTOR ANUAL"] = 1
    else: tabla1990.loc[38, "FACTOR ANUAL"] = (tabla1990.loc[38, "S(x)"] / ((tabla1990.loc[38, "S(x)"] * tabla1990.loc[43, "P(x+5)"]))) ** (1/5)    

    for i in range(39, 43):
        if tabla1990.loc[43, "P(x+5)"] == 1 or tabla1990.loc[38, "P(x+5)"] == 1:
            tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] * tabla1990.loc[i, "P(x+5)"]
        else: tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1 , "S(x)"] / tabla1990.loc[38, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 43
    if tabla1990.loc[43, "P(x+5)"] == 1:
        tabla1990.loc[43, "S(x)"] = tabla1990.loc[42, "S(x)"] * tabla1990.loc[43, "P(x+5)"]
    else: tabla1990.loc[43, "S(x)"] = tabla1990.loc[38, "S(x)"] * tabla1990.loc[43, "P(x+5)"]

    #i+5   
    if tabla1990.loc[48, "P(x+5)"] == 1:
        tabla1990.loc[43, "FACTOR ANUAL"] = 1
    else: tabla1990.loc[43, "FACTOR ANUAL"] = (tabla1990.loc[43, "S(x)"] / ((tabla1990.loc[43, "S(x)"] * tabla1990.loc[48, "P(x+5)"]))) ** (1/5)    

    for i in range(44, 48):
        if tabla1990.loc[48, "P(x+5)"] == 1 or tabla1990.loc[43, "P(x+5)"] == 1:
            tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] * tabla1990.loc[i, "P(x+5)"]
        else: tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1 , "S(x)"] / tabla1990.loc[43, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 48
    if tabla1990.loc[48, "P(x+5)"] == 1:
        tabla1990.loc[48, "S(x)"] = tabla1990.loc[47, "S(x)"] * tabla1990.loc[48, "P(x+5)"]
    else: tabla1990.loc[48, "S(x)"] = tabla1990.loc[43, "S(x)"] * tabla1990.loc[48, "P(x+5)"]

    #i+5   
    if tabla1990.loc[53, "P(x+5)"] == 1:
        tabla1990.loc[48, "FACTOR ANUAL"] = 1
    else: tabla1990.loc[48, "FACTOR ANUAL"] = (tabla1990.loc[48, "S(x)"] / ((tabla1990.loc[48, "S(x)"] * tabla1990.loc[53, "P(x+5)"]))) ** (1/5)    

    for i in range(49, 53):
        if tabla1990.loc[53, "P(x+5)"] == 1 or tabla1990.loc[48, "P(x+5)"] == 1:
            tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] * tabla1990.loc[i, "P(x+5)"]
        else: tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1 , "S(x)"] / tabla1990.loc[48, "FACTOR ANUAL"]
            
            #-----------------------------------------------------------------INTERVALO 53
    if tabla1990.loc[53, "P(x+5)"] == 1:
        tabla1990.loc[53, "S(x)"] = tabla1990.loc[52, "S(x)"] * tabla1990.loc[53, "P(x+5)"]
    else: tabla1990.loc[53, "S(x)"] = tabla1990.loc[48, "S(x)"] * tabla1990.loc[53, "P(x+5)"]

    #i+5   
    if tabla1990.loc[58, "P(x+5)"] == 1:
        tabla1990.loc[53, "FACTOR ANUAL"] = 1
    else: tabla1990.loc[53, "FACTOR ANUAL"] = (tabla1990.loc[53, "S(x)"] / ((tabla1990.loc[53, "S(x)"] * tabla1990.loc[58, "P(x+5)"]))) ** (1/5)    

    for i in range(54, 58):
        if tabla1990.loc[58, "P(x+5)"] == 1 or tabla1990.loc[53, "P(x+5)"] == 1:
            tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] * tabla1990.loc[i, "P(x+5)"]
        else: tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1 , "S(x)"] / tabla1990.loc[53, "FACTOR ANUAL"]    

            #-----------------------------------------------------------------INTERVALO 58
    if tabla1990.loc[58, "P(x+5)"] == 1:
        tabla1990.loc[58, "S(x)"] = tabla1990.loc[57, "S(x)"] * tabla1990.loc[58, "P(x+5)"]
    else: tabla1990.loc[58, "S(x)"] = tabla1990.loc[53, "S(x)"] * tabla1990.loc[58, "P(x+5)"]

    for i in range(59, 61):
        if tabla1990.loc[i-1, "P(x+5)"] == 1:
            tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] * tabla1990.loc[i, "P(x+5)"]
        else: tabla1990.loc[i, "S(x)"] = tabla1990.loc[i-1, "S(x)"] * tabla1990.loc[i, "P(x+5)"]       

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla1991 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1991] = tabla1991

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1991.loc[2, "P(x+5)"] = GENERACION_1991.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1991
    tabla1991.loc[3: 6, "P(x+5)"] = tabla1991.loc[2, "P(x+5)"]
    tabla1991.loc[7, "P(x+5)"] = GENERACION_1991.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1991.loc[8: 11, "P(x+5)"] = tabla1991.loc[7, "P(x+5)"]
    tabla1991.loc[12, "P(x+5)"] = GENERACION_1991.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1991.loc[13: 16, "P(x+5)"] = tabla1991.loc[12, "P(x+5)"]
    tabla1991.loc[17, "P(x+5)"] = GENERACION_1991.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1991.loc[18: 21, "P(x+5)"] = tabla1991.loc[17, "P(x+5)"]
    tabla1991.loc[22, "P(x+5)"] = GENERACION_1991.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1991.loc[23: 26, "P(x+5)"] = tabla1991.loc[22, "P(x+5)"]
    tabla1991.loc[27, "P(x+5)"] = GENERACION_1991.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1991.loc[32, "P(x+5)"] = GENERACION_1991.loc[5, "PROBABILIDAD QUINQUENAL"]
        
    for i in [37, 42, 47, 52, 57]:
        if tabla1991.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1991 <= 1:
            tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1991
        else:
            tabla1991.loc[i, "P(x+5)"] = 1
            
    for i in range(27, 33):
        if i not in [27, 32]:
            if (tabla1991.loc[27, "P(x+5)"] == 1 or tabla1991.loc[32, "P(x+5)"] == 1):
                if tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5)) >= 1:
                    tabla1991.loc[i, "P(x+5)"] = 1
                else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5))
            else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"]       

    for i in range(32, 38):
        if i not in [32, 37]:
            if (tabla1991.loc[32, "P(x+5)"] == 1 or tabla1991.loc[37, "P(x+5)"] == 1):
                if tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5)) >= 1:
                    tabla1991.loc[i, "P(x+5)"] = 1
                else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5))
            else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"] 
            
    for i in range(37, 43):
        if i not in [37, 42]:
            if (tabla1991.loc[37, "P(x+5)"] == 1 or tabla1991.loc[42, "P(x+5)"] == 1):
                if tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5)) >= 1:
                    tabla1991.loc[i, "P(x+5)"] = 1
                else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5))
            else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"]  

    for i in range(42, 48):
        if i not in [42, 47]:
            if (tabla1991.loc[42, "P(x+5)"] == 1 or tabla1991.loc[47, "P(x+5)"] == 1):
                if tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5)) >= 1:
                    tabla1991.loc[i, "P(x+5)"] = 1
                else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5))
            else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"]  

    for i in range(47, 53):
        if i not in [47, 52]:
            if (tabla1991.loc[47, "P(x+5)"] == 1 or tabla1991.loc[52, "P(x+5)"] == 1):
                if tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5)) >= 1:
                    tabla1991.loc[i, "P(x+5)"] = 1
                else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5))
            else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"]  
            
    for i in range(52, 58):
        if i not in [52, 57]:
            if (tabla1991.loc[52, "P(x+5)"] == 1 or tabla1991.loc[57, "P(x+5)"] == 1):
                if tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5)) >= 1:
                    tabla1991.loc[i, "P(x+5)"] = 1
                else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5))
            else: tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"]

    for i in range(58, 61):
        if tabla1991.loc[i-1, "P(x+5)"] == 1:
            tabla1991.loc[i, "P(x+5)"] = 1
        if tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5)) < 1:
            tabla1991.loc[i, "P(x+5)"] = tabla1991.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1991 ** (1/5))
        else: tabla1991.loc[i, "P(x+5)"] = 1 
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1991.loc[0, "S(x)"] = 100000
    tabla1991.loc[2, "S(x)"] = tabla1991.loc[0, "S(x)"] * tabla1991.loc[2, "P(x+5)"]

    for i in [7, 12, 17, 22, 27]:
        tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-5, "S(x)"] * tabla1991.loc[i, "P(x+5)"]
        
    tabla1991.loc[0, "FACTOR ANUAL"] = (tabla1991.loc[0, "S(x)"] / tabla1991.loc[2, "S(x)"]) ** (1/2)

    for i in [2, 7, 12, 17, 22]:
        tabla1991.loc[i, "FACTOR ANUAL"] = (tabla1991.loc[i, "S(x)"] / tabla1991.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 27):
        if i not in [2, 7, 12, 17, 22]:
            tabla1991.loc[i, "FACTOR ANUAL"] = tabla1991.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 27):
        if i not in [2, 7, 12, 17, 22]:
            if tabla1991.loc[i, "FACTOR ANUAL"] == 1:
                tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] / tabla1991.loc[i, "FACTOR ANUAL"]
            else: tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] / tabla1991.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1991.loc[27, "P(x+5)"] == 1:
        tabla1991.loc[27, "S(x)"] = tabla1991.loc[26, "S(x)"] * tabla1991.loc[27, "P(x+5)"]
    else: tabla1991.loc[27, "S(x)"] = tabla1991.loc[22, "S(x)"] * tabla1991.loc[27, "P(x+5)"]
    
    if tabla1991.loc[27, "P(x+5)"] == 1:
        tabla1991.loc[27, "FACTOR ANUAL"] = 1
    else: tabla1991.loc[27, "FACTOR ANUAL"] = (tabla1991.loc[27, "S(x)"] / ((tabla1991.loc[27, "S(x)"] * tabla1991.loc[32, "P(x+5)"]))) ** (1/5)    

    for i in range(28, 32):
        if tabla1991.loc[32, "P(x+5)"] == 1:
            tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] * tabla1991.loc[i, "P(x+5)"]
        else: tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1 , "S(x)"] / tabla1991.loc[27, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1991.loc[32, "P(x+5)"] == 1:
        tabla1991.loc[32, "S(x)"] = tabla1991.loc[31, "S(x)"] * tabla1991.loc[32, "P(x+5)"]
    else: tabla1991.loc[32, "S(x)"] = tabla1991.loc[27, "S(x)"] * tabla1991.loc[32, "P(x+5)"]
    
    if tabla1991.loc[37, "P(x+5)"] == 1:
        tabla1991.loc[32, "FACTOR ANUAL"] = 1
    else: tabla1991.loc[32, "FACTOR ANUAL"] = (tabla1991.loc[32, "S(x)"] / ((tabla1991.loc[32, "S(x)"] * tabla1991.loc[37, "P(x+5)"]))) ** (1/5)    

    for i in range(33, 37):
        if tabla1991.loc[37, "P(x+5)"] == 1:
            tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] * tabla1991.loc[i, "P(x+5)"]
        else: tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1 , "S(x)"] / tabla1991.loc[32, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1991.loc[37, "P(x+5)"] == 1:
        tabla1991.loc[37, "S(x)"] = tabla1991.loc[36, "S(x)"] * tabla1991.loc[37, "P(x+5)"]
    else: tabla1991.loc[37, "S(x)"] = tabla1991.loc[32, "S(x)"] * tabla1991.loc[37, "P(x+5)"]

    #i+5   
    if tabla1991.loc[42, "P(x+5)"] == 1:
        tabla1991.loc[37, "FACTOR ANUAL"] = 1
    else: tabla1991.loc[37, "FACTOR ANUAL"] = (tabla1991.loc[37, "S(x)"] / ((tabla1991.loc[37, "S(x)"] * tabla1991.loc[42, "P(x+5)"]))) ** (1/5)    

    for i in range(38, 42):
        if tabla1991.loc[42, "P(x+5)"] == 1 or tabla1991.loc[37, "P(x+5)"] == 1:
            tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] * tabla1991.loc[i, "P(x+5)"]
        else: tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1 , "S(x)"] / tabla1991.loc[37, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1991.loc[42, "P(x+5)"] == 1:
        tabla1991.loc[42, "S(x)"] = tabla1991.loc[41, "S(x)"] * tabla1991.loc[42, "P(x+5)"]
    else: tabla1991.loc[42, "S(x)"] = tabla1991.loc[37, "S(x)"] * tabla1991.loc[42, "P(x+5)"]
    
    if tabla1991.loc[47, "P(x+5)"] == 1:
        tabla1991.loc[42, "FACTOR ANUAL"] = 1
    else: tabla1991.loc[42, "FACTOR ANUAL"] = (tabla1991.loc[42, "S(x)"] / ((tabla1991.loc[42, "S(x)"] * tabla1991.loc[47, "P(x+5)"]))) ** (1/5)    

    for i in range(43, 47):
        if tabla1991.loc[47, "P(x+5)"] == 1 or tabla1991.loc[42, "P(x+5)"] == 1:
            tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] * tabla1991.loc[i, "P(x+5)"]
        else: tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1 , "S(x)"] / tabla1991.loc[42, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1991.loc[47, "P(x+5)"] == 1:
        tabla1991.loc[47, "S(x)"] = tabla1991.loc[46, "S(x)"] * tabla1991.loc[47, "P(x+5)"]
    else: tabla1991.loc[47, "S(x)"] = tabla1991.loc[42, "S(x)"] * tabla1991.loc[47, "P(x+5)"]

    if tabla1991.loc[52, "P(x+5)"] == 1:
        tabla1991.loc[47, "FACTOR ANUAL"] = 1
    else: tabla1991.loc[47, "FACTOR ANUAL"] = (tabla1991.loc[47, "S(x)"] / ((tabla1991.loc[47, "S(x)"] * tabla1991.loc[52, "P(x+5)"]))) ** (1/5) 

    for i in range(48, 52):
        if tabla1991.loc[52, "P(x+5)"] == 1 or tabla1991.loc[47, "P(x+5)"] == 1:
            tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] * tabla1991.loc[i, "P(x+5)"]
        else: tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1 , "S(x)"] / tabla1991.loc[47, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1991.loc[52, "P(x+5)"] == 1:
        tabla1991.loc[52, "S(x)"] = tabla1991.loc[51, "S(x)"] * tabla1991.loc[52, "P(x+5)"]
    else: tabla1991.loc[52, "S(x)"] = tabla1991.loc[47, "S(x)"] * tabla1991.loc[52, "P(x+5)"]

    if tabla1991.loc[57, "P(x+5)"] == 1:
        tabla1991.loc[52, "FACTOR ANUAL"] = 1
    else: tabla1991.loc[52, "FACTOR ANUAL"] = (tabla1991.loc[52, "S(x)"] / ((tabla1991.loc[52, "S(x)"] * tabla1991.loc[57, "P(x+5)"]))) ** (1/5) 

    for i in range(53, 57):
        if tabla1991.loc[57, "P(x+5)"] == 1 or tabla1991.loc[52, "P(x+5)"] == 1:
            tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] * tabla1991.loc[i, "P(x+5)"]
        else: tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1 , "S(x)"] / tabla1991.loc[52, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1991.loc[57, "P(x+5)"] == 1:
        tabla1991.loc[57, "S(x)"] = tabla1991.loc[56, "S(x)"] * tabla1991.loc[57, "P(x+5)"]
    else: tabla1991.loc[57, "S(x)"] = tabla1991.loc[52, "S(x)"] * tabla1991.loc[57, "P(x+5)"]

    for i in range(58, 61):
        if tabla1991.loc[i-1, "P(x+5)"] == 1:
            tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] * tabla1991.loc[i, "P(x+5)"]
        else: tabla1991.loc[i, "S(x)"] = tabla1991.loc[i-1, "S(x)"] * tabla1991.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1992 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1992] = tabla1992

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1992.loc[1, "P(x+5)"] = GENERACION_1992.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1992
    tabla1992.loc[2: 5, "P(x+5)"] = tabla1992.loc[1, "P(x+5)"]
    tabla1992.loc[6, "P(x+5)"] = GENERACION_1992.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1992.loc[7: 10, "P(x+5)"] = tabla1992.loc[6, "P(x+5)"]
    tabla1992.loc[11, "P(x+5)"] = GENERACION_1992.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1992.loc[12: 15, "P(x+5)"] = tabla1992.loc[11, "P(x+5)"]
    tabla1992.loc[16, "P(x+5)"] = GENERACION_1992.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1992.loc[17: 20, "P(x+5)"] = tabla1992.loc[16, "P(x+5)"]
    tabla1992.loc[21, "P(x+5)"] = GENERACION_1992.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1992.loc[22: 25, "P(x+5)"] = tabla1992.loc[21, "P(x+5)"]
    tabla1992.loc[26, "P(x+5)"] = GENERACION_1992.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1992.loc[31, "P(x+5)"] = GENERACION_1992.loc[5, "PROBABILIDAD QUINQUENAL"]

    for i in [36, 41, 46, 51, 56]:
        if tabla1992.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1992 <= 1:
            tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1992
        else:
            tabla1992.loc[i, "P(x+5)"] = 1

    for i in range(26, 32):
        if i not in [26, 31]:
            if (tabla1992.loc[26, "P(x+5)"] == 1 or tabla1992.loc[31, "P(x+5)"] == 1):
                if tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5)) >= 1:
                    tabla1992.loc[i, "P(x+5)"] = 1
                else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5))
            else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] 

    for i in range(31, 37):
        if i not in [31, 36]:
            if (tabla1992.loc[31, "P(x+5)"] == 1 or tabla1992.loc[36, "P(x+5)"] == 1):
                if tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5)) >= 1:
                    tabla1992.loc[i, "P(x+5)"] = 1
                else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5))
            else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] 

    for i in range(36, 42):
        if i not in [36, 41]:
            if (tabla1992.loc[36, "P(x+5)"] == 1 or tabla1992.loc[41, "P(x+5)"] == 1):
                if tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5)) >= 1:
                    tabla1992.loc[i, "P(x+5)"] = 1
                else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5))
            else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] 

    for i in range(41, 47):
        if i not in [41, 46]:
            if (tabla1992.loc[41, "P(x+5)"] == 1 or tabla1992.loc[46, "P(x+5)"] == 1):
                if tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5)) >= 1:
                    tabla1992.loc[i, "P(x+5)"] = 1
                else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5))
            else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"]  

    for i in range(46, 52):
        if i not in [46, 51]:
            if (tabla1992.loc[46, "P(x+5)"] == 1 or tabla1992.loc[51, "P(x+5)"] == 1):
                if tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5)) >= 1:
                    tabla1992.loc[i, "P(x+5)"] = 1
                else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5))
            else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"]  
            
    for i in range(51, 57):
        if i not in [51, 56]:
            if (tabla1992.loc[51, "P(x+5)"] == 1 or tabla1992.loc[56, "P(x+5)"] == 1):
                if tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5)) >= 1:
                    tabla1992.loc[i, "P(x+5)"] = 1
                else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5))
            else: tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"]

    for i in range(57, 61):
        if tabla1992.loc[i-1, "P(x+5)"] == 1:
            tabla1992.loc[i, "P(x+5)"] = 1
        if tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5)) < 1:
            tabla1992.loc[i, "P(x+5)"] = tabla1992.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1992 ** (1/5))
        else: tabla1992.loc[i, "P(x+5)"] = 1 
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1992.loc[0, "S(x)"] = 100000
    tabla1992.loc[1, "S(x)"] = tabla1992.loc[0, "S(x)"] * tabla1992.loc[1, "P(x+5)"]

    for i in [6, 11, 16, 21, 26]:
        tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-5, "S(x)"] * tabla1992.loc[i, "P(x+5)"]
        
    #tabla1992.loc[0, "FACTOR ANUAL"] = (tabla1992.loc[0, "S(x)"] / tabla1992.loc[1, "S(x)"]) ** (1/5)

    for i in [1, 6, 11, 16, 21]:
        tabla1992.loc[i, "FACTOR ANUAL"] = (tabla1992.loc[i, "S(x)"] / tabla1992.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 26):
        if i not in [1, 6, 11, 16, 21]:
            tabla1992.loc[i, "FACTOR ANUAL"] = tabla1992.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 26):
        if i not in [1, 6, 11, 16, 21]:
            if tabla1992.loc[i, "FACTOR ANUAL"] == 1:
                tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] / tabla1992.loc[i, "FACTOR ANUAL"]
            else: tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] / tabla1992.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1992.loc[26, "P(x+5)"] == 1:
        tabla1992.loc[26, "S(x)"] = tabla1992.loc[25, "S(x)"] * tabla1992.loc[26, "P(x+5)"]
    else: tabla1992.loc[26, "S(x)"] = tabla1992.loc[21, "S(x)"] * tabla1992.loc[26, "P(x+5)"]
    
    if tabla1992.loc[31, "P(x+5)"] == 1:
        tabla1992.loc[26, "FACTOR ANUAL"] = 1
    else: tabla1992.loc[26, "FACTOR ANUAL"] = (tabla1992.loc[26, "S(x)"] / ((tabla1992.loc[26, "S(x)"] * tabla1992.loc[31, "P(x+5)"]))) ** (1/5)    

    for i in range(27, 31):
        if tabla1992.loc[31, "P(x+5)"] == 1:
            tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] * tabla1992.loc[i, "P(x+5)"]
        else: tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1 , "S(x)"] / tabla1992.loc[26, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1992.loc[31, "P(x+5)"] == 1:
        tabla1992.loc[31, "S(x)"] = tabla1992.loc[30, "S(x)"] * tabla1992.loc[31, "P(x+5)"]
    else: tabla1992.loc[31, "S(x)"] = tabla1992.loc[26, "S(x)"] * tabla1992.loc[31, "P(x+5)"]
    
    if tabla1992.loc[36, "P(x+5)"] == 1:
        tabla1992.loc[31, "FACTOR ANUAL"] = 1
    else: tabla1992.loc[31, "FACTOR ANUAL"] = (tabla1992.loc[31, "S(x)"] / ((tabla1992.loc[31, "S(x)"] * tabla1992.loc[36, "P(x+5)"]))) ** (1/5)    

    for i in range(32, 36):
        if tabla1992.loc[36, "P(x+5)"] == 1:
            tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] * tabla1992.loc[i, "P(x+5)"]
        else: tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1 , "S(x)"] / tabla1992.loc[31, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1992.loc[36, "P(x+5)"] == 1:
        tabla1992.loc[36, "S(x)"] = tabla1992.loc[35, "S(x)"] * tabla1992.loc[36, "P(x+5)"]
    else: tabla1992.loc[36, "S(x)"] = tabla1992.loc[31, "S(x)"] * tabla1992.loc[36, "P(x+5)"]

    #i+5   
    if tabla1992.loc[41, "P(x+5)"] == 1:
        tabla1992.loc[36, "FACTOR ANUAL"] = 1
    else: tabla1992.loc[36, "FACTOR ANUAL"] = (tabla1992.loc[36, "S(x)"] / ((tabla1992.loc[36, "S(x)"] * tabla1992.loc[41, "P(x+5)"]))) ** (1/5)    

    for i in range(37, 41):
        if tabla1992.loc[41, "P(x+5)"] == 1 or tabla1992.loc[36, "P(x+5)"] == 1:
            tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] * tabla1992.loc[i, "P(x+5)"]
        else: tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1 , "S(x)"] / tabla1992.loc[36, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1992.loc[41, "P(x+5)"] == 1:
        tabla1992.loc[41, "S(x)"] = tabla1992.loc[40, "S(x)"] * tabla1992.loc[41, "P(x+5)"]
    else: tabla1992.loc[41, "S(x)"] = tabla1992.loc[36, "S(x)"] * tabla1992.loc[41, "P(x+5)"]
    
    if tabla1992.loc[46, "P(x+5)"] == 1:
        tabla1992.loc[41, "FACTOR ANUAL"] = 1
    else: tabla1992.loc[41, "FACTOR ANUAL"] = (tabla1992.loc[41, "S(x)"] / ((tabla1992.loc[41, "S(x)"] * tabla1992.loc[46, "P(x+5)"]))) ** (1/5)    

    for i in range(42, 46):
        if tabla1992.loc[46, "P(x+5)"] == 1 or tabla1992.loc[41, "P(x+5)"] == 1:
            tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] * tabla1992.loc[i, "P(x+5)"]
        else: tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1 , "S(x)"] / tabla1992.loc[41, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1992.loc[46, "P(x+5)"] == 1:
        tabla1992.loc[46, "S(x)"] = tabla1992.loc[45, "S(x)"] * tabla1992.loc[46, "P(x+5)"]
    else: tabla1992.loc[46, "S(x)"] = tabla1992.loc[41, "S(x)"] * tabla1992.loc[46, "P(x+5)"]

    if tabla1992.loc[51, "P(x+5)"] == 1:
        tabla1992.loc[46, "FACTOR ANUAL"] = 1
    else: tabla1992.loc[46, "FACTOR ANUAL"] = (tabla1992.loc[46, "S(x)"] / ((tabla1992.loc[46, "S(x)"] * tabla1992.loc[51, "P(x+5)"]))) ** (1/5) 

    for i in range(47, 51):
        if tabla1992.loc[51, "P(x+5)"] == 1 or tabla1992.loc[46, "P(x+5)"] == 1:
            tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] * tabla1992.loc[i, "P(x+5)"]
        else: tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1 , "S(x)"] / tabla1992.loc[46, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1992.loc[51, "P(x+5)"] == 1:
        tabla1992.loc[51, "S(x)"] = tabla1992.loc[50, "S(x)"] * tabla1992.loc[52, "P(x+5)"]
    else: tabla1992.loc[51, "S(x)"] = tabla1992.loc[46, "S(x)"] * tabla1992.loc[51, "P(x+5)"]

    if tabla1992.loc[56, "P(x+5)"] == 1:
        tabla1992.loc[51, "FACTOR ANUAL"] = 1
    else: tabla1992.loc[51, "FACTOR ANUAL"] = (tabla1992.loc[51, "S(x)"] / ((tabla1992.loc[51, "S(x)"] * tabla1992.loc[56, "P(x+5)"]))) ** (1/5) 

    for i in range(52, 56):
        if tabla1992.loc[56, "P(x+5)"] == 1 or tabla1992.loc[51, "P(x+5)"] == 1:
            tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] * tabla1992.loc[i, "P(x+5)"]
        else: tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1 , "S(x)"] / tabla1992.loc[51, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1992.loc[56, "P(x+5)"] == 1:
        tabla1992.loc[56, "S(x)"] = tabla1992.loc[55, "S(x)"] * tabla1992.loc[56, "P(x+5)"]
    else: tabla1992.loc[56, "S(x)"] = tabla1992.loc[51, "S(x)"] * tabla1992.loc[56, "P(x+5)"]

    for i in range(57, 61):
        if tabla1992.loc[i-1, "P(x+5)"] == 1:
            tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] * tabla1992.loc[i, "P(x+5)"]
        else: tabla1992.loc[i, "S(x)"] = tabla1992.loc[i-1, "S(x)"] * tabla1992.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1993 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1993] = tabla1993

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1993.loc[5, "P(x+5)"] = GENERACION_1993.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1993.loc[6: 9, "P(x+5)"] = tabla1993.loc[5, "P(x+5)"]
    tabla1993.loc[10, "P(x+5)"] = GENERACION_1993.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1993.loc[11: 14, "P(x+5)"] = tabla1993.loc[10, "P(x+5)"]
    tabla1993.loc[15, "P(x+5)"] = GENERACION_1993.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1993.loc[16: 19, "P(x+5)"] = tabla1993.loc[15, "P(x+5)"]
    tabla1993.loc[20, "P(x+5)"] = GENERACION_1993.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1993.loc[21: 24, "P(x+5)"] = tabla1993.loc[20, "P(x+5)"]
    tabla1993.loc[25, "P(x+5)"] = GENERACION_1993.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1993.loc[26: 29, "P(x+5)"] = tabla1993.loc[25, "P(x+5)"]
    tabla1993.loc[30, "P(x+5)"] = GENERACION_1993.loc[5, "PROBABILIDAD QUINQUENAL"]
    tabla1993.loc[35, "P(x+5)"] = GENERACION_1993.loc[6, "PROBABILIDAD QUINQUENAL"]

    for i in [40, 45, 50, 55, 60]:
        if tabla1993.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1993 <= 1:
            tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1993
        else:
            tabla1993.loc[i, "P(x+5)"] = 1

    for i in range(30, 36):
        if i not in [30, 35]:
            if (tabla1993.loc[30, "P(x+5)"] == 1 or tabla1993.loc[35, "P(x+5)"] == 1):
                if tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5)) >= 1:
                    tabla1993.loc[i, "P(x+5)"] = 1
                else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5))
            else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"] 

    for i in range(35, 41):
        if i not in [35, 40]:
            if (tabla1993.loc[35, "P(x+5)"] == 1 or tabla1993.loc[40, "P(x+5)"] == 1):
                if tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5)) >= 1:
                    tabla1993.loc[i, "P(x+5)"] = 1
                else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5))
            else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"] 

    for i in range(40, 46):
        if i not in [40, 45]:
            if (tabla1993.loc[40, "P(x+5)"] == 1 or tabla1993.loc[45, "P(x+5)"] == 1):
                if tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5)) >= 1:
                    tabla1993.loc[i, "P(x+5)"] = 1
                else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5))
            else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"] 

    for i in range(45, 51):
        if i not in [45, 50]:
            if (tabla1993.loc[45, "P(x+5)"] == 1 or tabla1993.loc[50, "P(x+5)"] == 1):
                if tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5)) >= 1:
                    tabla1993.loc[i, "P(x+5)"] = 1
                else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5))
            else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"]  

    for i in range(50, 56):
        if i not in [50, 55]:
            if (tabla1993.loc[50, "P(x+5)"] == 1 or tabla1993.loc[55, "P(x+5)"] == 1):
                if tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5)) >= 1:
                    tabla1993.loc[i, "P(x+5)"] = 1
                else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5))
            else: tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"]  
            
    for i in range(56, 61):
        if i not in [60]:
            if tabla1993.loc[i-1, "P(x+5)"] == 1:
                tabla1993.loc[i, "P(x+5)"] = 1
            if tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5)) < 1:
                tabla1993.loc[i, "P(x+5)"] = tabla1993.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1993 ** (1/5))
            else: tabla1993.loc[i, "P(x+5)"] = 1 
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1993.loc[0, "S(x)"] = 100000
    tabla1993.loc[5, "S(x)"] = tabla1993.loc[0, "S(x)"] * tabla1993.loc[5, "P(x+5)"]

    for i in [10, 15, 20, 25, 30]:
        tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-5, "S(x)"] * tabla1993.loc[i, "P(x+5)"]
        
    tabla1993.loc[0, "FACTOR ANUAL"] = (tabla1993.loc[0, "S(x)"] / tabla1993.loc[5, "S(x)"]) ** (1/5)

    for i in [5, 10, 15, 20, 25]:
        tabla1993.loc[i, "FACTOR ANUAL"] = (tabla1993.loc[i, "S(x)"] / tabla1993.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 30):
        if i not in [5, 10, 15, 20, 25]:
            tabla1993.loc[i, "FACTOR ANUAL"] = tabla1993.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 30):
        if i not in [5, 10, 15, 20, 25]:
            if tabla1993.loc[i, "FACTOR ANUAL"] == 1:
                tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1, "S(x)"] / tabla1993.loc[i, "FACTOR ANUAL"]
            else: tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1, "S(x)"] / tabla1993.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1993.loc[30, "P(x+5)"] == 1:
        tabla1993.loc[30, "S(x)"] = tabla1993.loc[29, "S(x)"] * tabla1993.loc[30, "P(x+5)"]
    else: tabla1993.loc[30, "S(x)"] = tabla1993.loc[25, "S(x)"] * tabla1993.loc[30, "P(x+5)"]
    
    if tabla1993.loc[35, "P(x+5)"] == 1:
        tabla1993.loc[30, "FACTOR ANUAL"] = 1
    else: tabla1993.loc[30, "FACTOR ANUAL"] = (tabla1993.loc[30, "S(x)"] / ((tabla1993.loc[30, "S(x)"] * tabla1993.loc[35, "P(x+5)"]))) ** (1/5)    

    for i in range(31, 35):
        if tabla1993.loc[35, "P(x+5)"] == 1:
            tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1, "S(x)"] * tabla1993.loc[i, "P(x+5)"]
        else: tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1 , "S(x)"] / tabla1993.loc[30, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1993.loc[35, "P(x+5)"] == 1:
        tabla1993.loc[35, "S(x)"] = tabla1993.loc[34, "S(x)"] * tabla1993.loc[35, "P(x+5)"]
    else: tabla1993.loc[35, "S(x)"] = tabla1993.loc[30, "S(x)"] * tabla1993.loc[35, "P(x+5)"]
    
    if tabla1993.loc[40, "P(x+5)"] == 1:
        tabla1993.loc[35, "FACTOR ANUAL"] = 1
    else: tabla1993.loc[35, "FACTOR ANUAL"] = (tabla1993.loc[35, "S(x)"] / ((tabla1993.loc[35, "S(x)"] * tabla1993.loc[40, "P(x+5)"]))) ** (1/5)    

    for i in range(36, 40):
        if tabla1993.loc[40, "P(x+5)"] == 1:
            tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1, "S(x)"] * tabla1993.loc[i, "P(x+5)"]
        else: tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1 , "S(x)"] / tabla1993.loc[35, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1993.loc[40, "P(x+5)"] == 1:
        tabla1993.loc[40, "S(x)"] = tabla1993.loc[39, "S(x)"] * tabla1993.loc[40, "P(x+5)"]
    else: tabla1993.loc[40, "S(x)"] = tabla1993.loc[35, "S(x)"] * tabla1993.loc[40, "P(x+5)"]

    #i+5   
    if tabla1993.loc[45, "P(x+5)"] == 1:
        tabla1993.loc[40, "FACTOR ANUAL"] = 1
    else: tabla1993.loc[40, "FACTOR ANUAL"] = (tabla1993.loc[40, "S(x)"] / ((tabla1993.loc[40, "S(x)"] * tabla1993.loc[45, "P(x+5)"]))) ** (1/5)    

    for i in range(41, 45):
        if tabla1993.loc[45, "P(x+5)"] == 1 or tabla1993.loc[40, "P(x+5)"] == 1:
            tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1, "S(x)"] * tabla1993.loc[i, "P(x+5)"]
        else: tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1 , "S(x)"] / tabla1993.loc[40, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1993.loc[45, "P(x+5)"] == 1:
        tabla1993.loc[45, "S(x)"] = tabla1993.loc[44, "S(x)"] * tabla1993.loc[45, "P(x+5)"]
    else: tabla1993.loc[45, "S(x)"] = tabla1993.loc[40, "S(x)"] * tabla1993.loc[45, "P(x+5)"]
    
    if tabla1993.loc[50, "P(x+5)"] == 1:
        tabla1993.loc[45, "FACTOR ANUAL"] = 1
    else: tabla1993.loc[45, "FACTOR ANUAL"] = (tabla1993.loc[45, "S(x)"] / ((tabla1993.loc[45, "S(x)"] * tabla1993.loc[50, "P(x+5)"]))) ** (1/5)    

    for i in range(46, 50):
        if tabla1993.loc[50, "P(x+5)"] == 1 or tabla1993.loc[45, "P(x+5)"] == 1:
            tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1, "S(x)"] * tabla1993.loc[i, "P(x+5)"]
        else: tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1 , "S(x)"] / tabla1993.loc[45, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1993.loc[50, "P(x+5)"] == 1:
        tabla1993.loc[50, "S(x)"] = tabla1993.loc[49, "S(x)"] * tabla1993.loc[50, "P(x+5)"]
    else: tabla1993.loc[50, "S(x)"] = tabla1993.loc[45, "S(x)"] * tabla1993.loc[50, "P(x+5)"]

    if tabla1993.loc[55, "P(x+5)"] == 1:
        tabla1993.loc[50, "FACTOR ANUAL"] = 1
    else: tabla1993.loc[50, "FACTOR ANUAL"] = (tabla1993.loc[50, "S(x)"] / ((tabla1993.loc[50, "S(x)"] * tabla1993.loc[55, "P(x+5)"]))) ** (1/5) 

    for i in range(51, 55):
        if tabla1993.loc[55, "P(x+5)"] == 1 or tabla1993.loc[50, "P(x+5)"] == 1:
            tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1, "S(x)"] * tabla1993.loc[i, "P(x+5)"]
        else: tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1 , "S(x)"] / tabla1993.loc[50, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1993.loc[55, "P(x+5)"] == 1:
        tabla1993.loc[55, "S(x)"] = tabla1993.loc[54, "S(x)"] * tabla1993.loc[55, "P(x+5)"]
    else: tabla1993.loc[55, "S(x)"] = tabla1993.loc[50, "S(x)"] * tabla1993.loc[55, "P(x+5)"]

    if tabla1993.loc[60, "P(x+5)"] == 1:
        tabla1993.loc[55, "FACTOR ANUAL"] = 1
    else: tabla1993.loc[55, "FACTOR ANUAL"] = (tabla1993.loc[55, "S(x)"] / ((tabla1993.loc[55, "S(x)"] * tabla1993.loc[60, "P(x+5)"]))) ** (1/5) 

    for i in range(56, 60):
        if tabla1993.loc[60, "P(x+5)"] == 1 or tabla1993.loc[55, "P(x+5)"] == 1:
            tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1, "S(x)"] * tabla1993.loc[i, "P(x+5)"]
        else: tabla1993.loc[i, "S(x)"] = tabla1993.loc[i-1 , "S(x)"] / tabla1993.loc[55, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1993.loc[60, "P(x+5)"] == 1:
        tabla1993.loc[60, "S(x)"] = tabla1993.loc[60, "P(x+5)"] * tabla1993.loc[59, "S(x)"]
    else: tabla1993.loc[60, "S(x)"] = tabla1993.loc[60, "P(x+5)"] * tabla1993.loc[55, "S(x)"]
        
    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1994 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1994] = tabla1994

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1994.loc[4, "P(x+5)"] = GENERACION_1994.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1994
    tabla1994.loc[5: 8, "P(x+5)"] = tabla1994.loc[4, "P(x+5)"]
    tabla1994.loc[9, "P(x+5)"] = GENERACION_1994.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1994.loc[10: 13, "P(x+5)"] = tabla1994.loc[9, "P(x+5)"]
    tabla1994.loc[14, "P(x+5)"] = GENERACION_1994.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1994.loc[15: 18, "P(x+5)"] = tabla1994.loc[14, "P(x+5)"]
    tabla1994.loc[19, "P(x+5)"] = GENERACION_1994.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1994.loc[20: 23, "P(x+5)"] = tabla1994.loc[19, "P(x+5)"]
    tabla1994.loc[24, "P(x+5)"] = GENERACION_1994.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1994.loc[29, "P(x+5)"] = GENERACION_1994.loc[4, "PROBABILIDAD QUINQUENAL"]

    for i in [34, 39, 44, 49, 54, 59]:
        if tabla1994.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1994 <= 1:
            tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1994
        else:
            tabla1994.loc[i, "P(x+5)"] = 1

    for i in range(24, 30):
        if i not in [24, 29]:
            if (tabla1994.loc[24, "P(x+5)"] == 1 or tabla1994.loc[29, "P(x+5)"] == 1):
                if tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5)) >= 1:
                    tabla1994.loc[i, "P(x+5)"] = 1
                else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5))
            else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] 

    for i in range(29, 35):
        if i not in [29, 34]:
            if (tabla1994.loc[29, "P(x+5)"] == 1 or tabla1994.loc[34, "P(x+5)"] == 1):
                if tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5)) >= 1:
                    tabla1994.loc[i, "P(x+5)"] = 1
                else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5))
            else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] 

    for i in range(34, 40):
        if i not in [34, 39]:
            if (tabla1994.loc[34, "P(x+5)"] == 1 or tabla1994.loc[39, "P(x+5)"] == 1):
                if tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5)) >= 1:
                    tabla1994.loc[i, "P(x+5)"] = 1
                else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5))
            else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] 

    for i in range(39, 45):
        if i not in [39, 44]:
            if (tabla1994.loc[39, "P(x+5)"] == 1 or tabla1994.loc[44, "P(x+5)"] == 1):
                if tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5)) >= 1:
                    tabla1994.loc[i, "P(x+5)"] = 1
                else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5))
            else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] 

    for i in range(44, 50):
        if i not in [44, 49]:
            if (tabla1994.loc[44, "P(x+5)"] == 1 or tabla1994.loc[49, "P(x+5)"] == 1):
                if tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5)) >= 1:
                    tabla1994.loc[i, "P(x+5)"] = 1
                else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5))
            else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"]  

    for i in range(49, 55):
        if i not in [49, 54]:
            if (tabla1994.loc[49, "P(x+5)"] == 1 or tabla1994.loc[54, "P(x+5)"] == 1):
                if tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5)) >= 1:
                    tabla1994.loc[i, "P(x+5)"] = 1
                else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5))
            else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"]  
            
    for i in range(54, 60):
        if i not in [54, 59]:
            if (tabla1994.loc[54, "P(x+5)"] == 1 or tabla1994.loc[59, "P(x+5)"] == 1):
                if tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5)) >= 1:
                    tabla1994.loc[i, "P(x+5)"] = 1
                else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5))
            else: tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"]

    for i in range(60, 61):
        if tabla1994.loc[i-1, "P(x+5)"] == 1:
            tabla1994.loc[i, "P(x+5)"] = 1
        if tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5)) < 1:
            tabla1994.loc[i, "P(x+5)"] = tabla1994.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1994 ** (1/5))
        else: tabla1994.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1994.loc[0, "S(x)"] = 100000
    tabla1994.loc[4, "S(x)"] = tabla1994.loc[0, "S(x)"] * tabla1994.loc[4, "P(x+5)"]

    for i in [9, 14, 19, 24]:
        tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-5, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
        
    tabla1994.loc[0, "FACTOR ANUAL"] = (tabla1994.loc[0, "S(x)"] / tabla1994.loc[4, "S(x)"]) ** (1/4)

    for i in [4, 9, 14, 19]:
        tabla1994.loc[i, "FACTOR ANUAL"] = (tabla1994.loc[i, "S(x)"] / tabla1994.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 24):
        if i not in [4, 9, 14, 19]:
            tabla1994.loc[i, "FACTOR ANUAL"] = tabla1994.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 24):
        if i not in [4, 9, 14, 19]:
            if tabla1994.loc[i, "FACTOR ANUAL"] == 1:
                tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] / tabla1994.loc[i, "FACTOR ANUAL"]
            else: tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] / tabla1994.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1994.loc[24, "P(x+5)"] == 1:
        tabla1994.loc[24, "S(x)"] = tabla1994.loc[23, "S(x)"] * tabla1994.loc[24, "P(x+5)"]
    else: tabla1994.loc[24, "S(x)"] = tabla1994.loc[19, "S(x)"] * tabla1994.loc[24, "P(x+5)"]
    
    if tabla1994.loc[29, "P(x+5)"] == 1:
        tabla1994.loc[24, "FACTOR ANUAL"] = 1
    else: tabla1994.loc[24, "FACTOR ANUAL"] = (tabla1994.loc[24, "S(x)"] / ((tabla1994.loc[24, "S(x)"] * tabla1994.loc[29, "P(x+5)"]))) ** (1/5)    

    for i in range(25, 29):
        if tabla1994.loc[29, "P(x+5)"] == 1:
            tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
        else: tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1 , "S(x)"] / tabla1994.loc[24, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1994.loc[29, "P(x+5)"] == 1:
        tabla1994.loc[29, "S(x)"] = tabla1994.loc[28, "S(x)"] * tabla1994.loc[29, "P(x+5)"]
    else: tabla1994.loc[29, "S(x)"] = tabla1994.loc[24, "S(x)"] * tabla1994.loc[29, "P(x+5)"]
    
    if tabla1994.loc[34, "P(x+5)"] == 1:
        tabla1994.loc[29, "FACTOR ANUAL"] = 1
    else: tabla1994.loc[29, "FACTOR ANUAL"] = (tabla1994.loc[29, "S(x)"] / ((tabla1994.loc[29, "S(x)"] * tabla1994.loc[34, "P(x+5)"]))) ** (1/5)    

    for i in range(30, 34):
        if tabla1994.loc[34, "P(x+5)"] == 1:
            tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
        else: tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1 , "S(x)"] / tabla1994.loc[29, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1994.loc[34, "P(x+5)"] == 1:
        tabla1994.loc[34, "S(x)"] = tabla1994.loc[33, "S(x)"] * tabla1994.loc[34, "P(x+5)"]
    else: tabla1994.loc[34, "S(x)"] = tabla1994.loc[29, "S(x)"] * tabla1994.loc[34, "P(x+5)"]
    
    if tabla1994.loc[39, "P(x+5)"] == 1:
        tabla1994.loc[34, "FACTOR ANUAL"] = 1
    else: tabla1994.loc[34, "FACTOR ANUAL"] = (tabla1994.loc[34, "S(x)"] / ((tabla1994.loc[34, "S(x)"] * tabla1994.loc[39, "P(x+5)"]))) ** (1/5)    

    for i in range(35, 39):
        if tabla1994.loc[39, "P(x+5)"] == 1 or tabla1994.loc[34, "P(x+5)"] == 1:
            tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
        else: tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1 , "S(x)"] / tabla1994.loc[34, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1994.loc[39, "P(x+5)"] == 1:
        tabla1994.loc[39, "S(x)"] = tabla1994.loc[38, "S(x)"] * tabla1994.loc[39, "P(x+5)"]
    else: tabla1994.loc[39, "S(x)"] = tabla1994.loc[34, "S(x)"] * tabla1994.loc[39, "P(x+5)"]

    #i+5   
    if tabla1994.loc[44, "P(x+5)"] == 1:
        tabla1994.loc[39, "FACTOR ANUAL"] = 1
    else: tabla1994.loc[39, "FACTOR ANUAL"] = (tabla1994.loc[39, "S(x)"] / ((tabla1994.loc[39, "S(x)"] * tabla1994.loc[44, "P(x+5)"]))) ** (1/5)    

    for i in range(40, 44):
        if tabla1994.loc[39, "P(x+5)"] == 1 or tabla1994.loc[44, "P(x+5)"] == 1:
            tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
        else: tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1 , "S(x)"] / tabla1994.loc[39, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1994.loc[44, "P(x+5)"] == 1:
        tabla1994.loc[44, "S(x)"] = tabla1994.loc[43, "S(x)"] * tabla1994.loc[44, "P(x+5)"]
    else: tabla1994.loc[44, "S(x)"] = tabla1994.loc[39, "S(x)"] * tabla1994.loc[44, "P(x+5)"]
    
    if tabla1994.loc[49, "P(x+5)"] == 1:
        tabla1994.loc[44, "FACTOR ANUAL"] = 1
    else: tabla1994.loc[44, "FACTOR ANUAL"] = (tabla1994.loc[44, "S(x)"] / ((tabla1994.loc[44, "S(x)"] * tabla1994.loc[49, "P(x+5)"]))) ** (1/5)    

    for i in range(45, 49):
        if tabla1994.loc[49, "P(x+5)"] == 1 or tabla1994.loc[44, "P(x+5)"] == 1:
            tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
        else: tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1 , "S(x)"] / tabla1994.loc[44, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1994.loc[49, "P(x+5)"] == 1:
        tabla1994.loc[49, "S(x)"] = tabla1994.loc[48, "S(x)"] * tabla1994.loc[49, "P(x+5)"]
    else: tabla1994.loc[49, "S(x)"] = tabla1994.loc[44, "S(x)"] * tabla1994.loc[49, "P(x+5)"]

    if tabla1994.loc[54, "P(x+5)"] == 1:
        tabla1994.loc[49, "FACTOR ANUAL"] = 1
    else: tabla1994.loc[49, "FACTOR ANUAL"] = (tabla1994.loc[49, "S(x)"] / ((tabla1994.loc[49, "S(x)"] * tabla1994.loc[54, "P(x+5)"]))) ** (1/5) 

    for i in range(50, 54):
        if tabla1994.loc[54, "P(x+5)"] == 1 or tabla1994.loc[49, "P(x+5)"] == 1:
            tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
        else: tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1 , "S(x)"] / tabla1994.loc[49, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1994.loc[54, "P(x+5)"] == 1:
        tabla1994.loc[54, "S(x)"] = tabla1994.loc[53, "S(x)"] * tabla1994.loc[54, "P(x+5)"]
    else: tabla1994.loc[54, "S(x)"] = tabla1994.loc[49, "S(x)"] * tabla1994.loc[54, "P(x+5)"]

    if tabla1994.loc[59, "P(x+5)"] == 1:
        tabla1994.loc[54, "FACTOR ANUAL"] = 1
    else: tabla1994.loc[54, "FACTOR ANUAL"] = (tabla1994.loc[54, "S(x)"] / ((tabla1994.loc[54, "S(x)"] * tabla1994.loc[59, "P(x+5)"]))) ** (1/5) 

    for i in range(55, 59):
        if tabla1994.loc[59, "P(x+5)"] == 1 or tabla1994.loc[54, "P(x+5)"] == 1:
            tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
        else: tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1 , "S(x)"] / tabla1994.loc[54, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1994.loc[59, "P(x+5)"] == 1:
        tabla1994.loc[59, "S(x)"] = tabla1994.loc[58, "S(x)"] * tabla1994.loc[59, "P(x+5)"]
    else: tabla1994.loc[59, "S(x)"] = tabla1994.loc[54, "S(x)"] * tabla1994.loc[59, "P(x+5)"]

    for i in range(59, 61):
        if i not in [59]:
            if tabla1994.loc[i-1, "P(x+5)"] == 1:
                tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
            else: tabla1994.loc[i, "S(x)"] = tabla1994.loc[i-1, "S(x)"] * tabla1994.loc[i, "P(x+5)"]
        
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla1995 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1995] = tabla1995

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1995.loc[3, "P(x+5)"] = GENERACION_1995.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1995
    tabla1995.loc[4: 7, "P(x+5)"] = tabla1995.loc[3, "P(x+5)"]
    tabla1995.loc[8, "P(x+5)"] = GENERACION_1995.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1995.loc[9: 12, "P(x+5)"] = tabla1995.loc[8, "P(x+5)"]
    tabla1995.loc[13, "P(x+5)"] = GENERACION_1995.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1995.loc[14: 17, "P(x+5)"] = tabla1995.loc[13, "P(x+5)"]
    tabla1995.loc[18, "P(x+5)"] = GENERACION_1995.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1995.loc[19: 22, "P(x+5)"] = tabla1995.loc[18, "P(x+5)"]
    tabla1995.loc[23, "P(x+5)"] = GENERACION_1995.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1995.loc[28, "P(x+5)"] = GENERACION_1995.loc[4, "PROBABILIDAD QUINQUENAL"]
        
    for i in [33, 38, 43, 48, 53, 58]:
        if tabla1995.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1995 <= 1:
            tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1995
        else:
            tabla1995.loc[i, "P(x+5)"] = 1

    for i in range(23, 29):
        if i not in [23, 28]:
            if (tabla1995.loc[23, "P(x+5)"] == 1 or tabla1995.loc[28, "P(x+5)"] == 1):
                if tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5)) >= 1:
                    tabla1995.loc[i, "P(x+5)"] = 1
                else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5))
            else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] 
            
    for i in range(28, 34):
        if i not in [28, 33]:
            if (tabla1995.loc[28, "P(x+5)"] == 1 or tabla1995.loc[33, "P(x+5)"] == 1):
                if tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5)) >= 1:
                    tabla1995.loc[i, "P(x+5)"] = 1
                else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5))
            else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"]       

    for i in range(33, 39):
        if i not in [33, 38]:
            if (tabla1995.loc[33, "P(x+5)"] == 1 or tabla1995.loc[38, "P(x+5)"] == 1):
                if tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5)) >= 1:
                    tabla1995.loc[i, "P(x+5)"] = 1
                else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5))
            else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] 
            
    for i in range(38, 44):
        if i not in [38, 43]:
            if (tabla1995.loc[38, "P(x+5)"] == 1 or tabla1995.loc[43, "P(x+5)"] == 1):
                if tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5)) >= 1:
                    tabla1995.loc[i, "P(x+5)"] = 1
                else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5))
            else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"]  

    for i in range(43, 49):
        if i not in [43, 48]:
            if (tabla1995.loc[43, "P(x+5)"] == 1 or tabla1995.loc[48, "P(x+5)"] == 1):
                if tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5)) >= 1:
                    tabla1995.loc[i, "P(x+5)"] = 1
                else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5))
            else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"]  

    for i in range(48, 54):
        if i not in [48, 53]:
            if (tabla1995.loc[48, "P(x+5)"] == 1 or tabla1995.loc[53, "P(x+5)"] == 1):
                if tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5)) >= 1:
                    tabla1995.loc[i, "P(x+5)"] = 1
                else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5))
            else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"]  
            
    for i in range(53, 59):
        if i not in [53, 58]:
            if (tabla1995.loc[53, "P(x+5)"] == 1 or tabla1995.loc[58, "P(x+5)"] == 1):
                if tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5)) >= 1:
                    tabla1995.loc[i, "P(x+5)"] = 1
                else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5))
            else: tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"]

    for i in range(59, 61):
        if tabla1995.loc[i-1, "P(x+5)"] == 1:
            tabla1995.loc[i, "P(x+5)"] = 1
        if tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5)) < 1:
            tabla1995.loc[i, "P(x+5)"] = tabla1995.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1995 ** (1/5))
        else: tabla1995.loc[i, "P(x+5)"] = 1 
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1995.loc[0, "S(x)"] = 100000
    tabla1995.loc[3, "S(x)"] = tabla1995.loc[0, "S(x)"] * tabla1995.loc[3, "P(x+5)"]

    for i in [8, 13, 18, 23]:
        tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-5, "S(x)"] * tabla1995.loc[i, "P(x+5)"]
        
    tabla1995.loc[0, "FACTOR ANUAL"] = (tabla1995.loc[0, "S(x)"] / tabla1995.loc[3, "S(x)"]) ** (1/3)

    for i in [3, 8, 13, 18]:
        tabla1995.loc[i, "FACTOR ANUAL"] = (tabla1995.loc[i, "S(x)"] / tabla1995.loc[i+5, "S(x)"]) ** (1/5)

    for i in range(1, 23):
        if i not in [3, 8, 13, 18]:
            tabla1995.loc[i, "FACTOR ANUAL"] = tabla1995.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 23):
        if i not in [3, 8, 13, 18]:
            if tabla1995.loc[i, "FACTOR ANUAL"] == 1:
                tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] / tabla1995.loc[i, "FACTOR ANUAL"]
            else: tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] / tabla1995.loc[i, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 23        
    if tabla1995.loc[23, "P(x+5)"] == 1:
        tabla1995.loc[23, "S(x)"] = tabla1995.loc[22, "S(x)"] * tabla1995.loc[23, "P(x+5)"]
    else: tabla1995.loc[23, "S(x)"] = tabla1995.loc[18, "S(x)"] * tabla1995.loc[23, "P(x+5)"]

    if tabla1995.loc[28, "P(x+5)"] == 1:
        tabla1995.loc[23, "FACTOR ANUAL"] = 1
    else: tabla1995.loc[23, "FACTOR ANUAL"] = (tabla1995.loc[23, "S(x)"] / ((tabla1995.loc[23, "S(x)"] * tabla1995.loc[28, "P(x+5)"]))) ** (1/5)
    
    for i in range(24, 28):
        if tabla1995.loc[28, "P(x+5)"] == 1:
            tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] * tabla1995.loc[i, "P(x+5)"]
        else: tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1 , "S(x)"] / tabla1995.loc[23, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 28
    if tabla1995.loc[28, "P(x+5)"] == 1:
        tabla1995.loc[28, "S(x)"] = tabla1995.loc[27, "S(x)"] * tabla1995.loc[28, "P(x+5)"]
    else: tabla1995.loc[28, "S(x)"] = tabla1995.loc[23, "S(x)"] * tabla1995.loc[28, "P(x+5)"]

    if tabla1995.loc[33, "P(x+5)"] == 1:
        tabla1995.loc[28, "FACTOR ANUAL"] = 1
    else: tabla1995.loc[28, "FACTOR ANUAL"] = (tabla1995.loc[28, "S(x)"] / ((tabla1995.loc[28, "S(x)"] * tabla1995.loc[33, "P(x+5)"]))) ** (1/5)
    
    for i in range(29, 33):
        if tabla1995.loc[33, "P(x+5)"] == 1:
            tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] * tabla1995.loc[i, "P(x+5)"]
        else: tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1 , "S(x)"] / tabla1995.loc[28, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 33
    if tabla1995.loc[33, "P(x+5)"] == 1:
        tabla1995.loc[33, "S(x)"] = tabla1995.loc[32, "S(x)"] * tabla1995.loc[33, "P(x+5)"]
    else: tabla1995.loc[33, "S(x)"] = tabla1995.loc[28, "S(x)"] * tabla1995.loc[33, "P(x+5)"]
    
    if tabla1995.loc[38, "P(x+5)"] == 1:
        tabla1995.loc[33, "FACTOR ANUAL"] = 1
    else: tabla1995.loc[33, "FACTOR ANUAL"] = (tabla1995.loc[33, "S(x)"] / ((tabla1995.loc[33, "S(x)"] * tabla1995.loc[38, "P(x+5)"]))) ** (1/5)    

    for i in range(34, 38):
        if tabla1995.loc[38, "P(x+5)"] == 1 or tabla1995.loc[33, "P(x+5)"] == 1:
            tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] * tabla1995.loc[i, "P(x+5)"]
        else: tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1 , "S(x)"] / tabla1995.loc[33, "FACTOR ANUAL"]
        
            #-----------------------------------------------------------------INTERVALO 38
    if tabla1995.loc[38, "P(x+5)"] == 1:
        tabla1995.loc[38, "S(x)"] = tabla1995.loc[37, "S(x)"] * tabla1995.loc[38, "P(x+5)"]
    else: tabla1995.loc[38, "S(x)"] = tabla1995.loc[33, "S(x)"] * tabla1995.loc[38, "P(x+5)"]

    #i+5   
    if tabla1995.loc[43, "P(x+5)"] == 1:
        tabla1995.loc[38, "FACTOR ANUAL"] = 1
    else: tabla1995.loc[38, "FACTOR ANUAL"] = (tabla1995.loc[38, "S(x)"] / ((tabla1995.loc[38, "S(x)"] * tabla1995.loc[43, "P(x+5)"]))) ** (1/5)    

    for i in range(39, 43):
        if tabla1995.loc[43, "P(x+5)"] == 1 or tabla1995.loc[38, "P(x+5)"] == 1:
            tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] * tabla1995.loc[i, "P(x+5)"]
        else: tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1 , "S(x)"] / tabla1995.loc[38, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 43
    if tabla1995.loc[43, "P(x+5)"] == 1:
        tabla1995.loc[43, "S(x)"] = tabla1995.loc[42, "S(x)"] * tabla1995.loc[43, "P(x+5)"]
    else: tabla1995.loc[43, "S(x)"] = tabla1995.loc[38, "S(x)"] * tabla1995.loc[43, "P(x+5)"]

    #i+5   
    if tabla1995.loc[48, "P(x+5)"] == 1:
        tabla1995.loc[43, "FACTOR ANUAL"] = 1
    else: tabla1995.loc[43, "FACTOR ANUAL"] = (tabla1995.loc[43, "S(x)"] / ((tabla1995.loc[43, "S(x)"] * tabla1995.loc[48, "P(x+5)"]))) ** (1/5)    

    for i in range(44, 48):
        if tabla1995.loc[48, "P(x+5)"] == 1 or tabla1995.loc[43, "P(x+5)"] == 1:
            tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] * tabla1995.loc[i, "P(x+5)"]
        else: tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1 , "S(x)"] / tabla1995.loc[43, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 48
    if tabla1995.loc[48, "P(x+5)"] == 1:
        tabla1995.loc[48, "S(x)"] = tabla1995.loc[47, "S(x)"] * tabla1995.loc[48, "P(x+5)"]
    else: tabla1995.loc[48, "S(x)"] = tabla1995.loc[43, "S(x)"] * tabla1995.loc[48, "P(x+5)"]

    #i+5   
    if tabla1995.loc[53, "P(x+5)"] == 1:
        tabla1995.loc[48, "FACTOR ANUAL"] = 1
    else: tabla1995.loc[48, "FACTOR ANUAL"] = (tabla1995.loc[48, "S(x)"] / ((tabla1995.loc[48, "S(x)"] * tabla1995.loc[53, "P(x+5)"]))) ** (1/5)    

    for i in range(49, 53):
        if tabla1995.loc[53, "P(x+5)"] == 1 or tabla1995.loc[48, "P(x+5)"] == 1:
            tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] * tabla1995.loc[i, "P(x+5)"]
        else: tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1 , "S(x)"] / tabla1995.loc[48, "FACTOR ANUAL"]
            
            #-----------------------------------------------------------------INTERVALO 53
    if tabla1995.loc[53, "P(x+5)"] == 1:
        tabla1995.loc[53, "S(x)"] = tabla1995.loc[52, "S(x)"] * tabla1995.loc[53, "P(x+5)"]
    else: tabla1995.loc[53, "S(x)"] = tabla1995.loc[48, "S(x)"] * tabla1995.loc[53, "P(x+5)"]

    #i+5   
    if tabla1995.loc[58, "P(x+5)"] == 1:
        tabla1995.loc[53, "FACTOR ANUAL"] = 1
    else: tabla1995.loc[53, "FACTOR ANUAL"] = (tabla1995.loc[53, "S(x)"] / ((tabla1995.loc[53, "S(x)"] * tabla1995.loc[58, "P(x+5)"]))) ** (1/5)    

    for i in range(54, 58):
        if tabla1995.loc[58, "P(x+5)"] == 1 or tabla1995.loc[53, "P(x+5)"] == 1:
            tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] * tabla1995.loc[i, "P(x+5)"]
        else: tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1 , "S(x)"] / tabla1995.loc[53, "FACTOR ANUAL"]    

            #-----------------------------------------------------------------INTERVALO 58
    if tabla1995.loc[58, "P(x+5)"] == 1:
        tabla1995.loc[58, "S(x)"] = tabla1995.loc[57, "S(x)"] * tabla1995.loc[58, "P(x+5)"]
    else: tabla1995.loc[58, "S(x)"] = tabla1995.loc[53, "S(x)"] * tabla1995.loc[58, "P(x+5)"]

    for i in range(59, 61):
        if tabla1995.loc[i-1, "P(x+5)"] == 1:
            tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] * tabla1995.loc[i, "P(x+5)"]
        else: tabla1995.loc[i, "S(x)"] = tabla1995.loc[i-1, "S(x)"] * tabla1995.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla1996 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1996] = tabla1996

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1996.loc[2, "P(x+5)"] = GENERACION_1996.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1996
    tabla1996.loc[3: 6, "P(x+5)"] = tabla1996.loc[2, "P(x+5)"]
    tabla1996.loc[7, "P(x+5)"] = GENERACION_1996.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1996.loc[8: 11, "P(x+5)"] = tabla1996.loc[7, "P(x+5)"]
    tabla1996.loc[12, "P(x+5)"] = GENERACION_1996.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1996.loc[13: 16, "P(x+5)"] = tabla1996.loc[12, "P(x+5)"]
    tabla1996.loc[17, "P(x+5)"] = GENERACION_1996.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1996.loc[18: 21, "P(x+5)"] = tabla1996.loc[17, "P(x+5)"]
    tabla1996.loc[22, "P(x+5)"] = GENERACION_1996.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1996.loc[27, "P(x+5)"] = GENERACION_1996.loc[4, "PROBABILIDAD QUINQUENAL"]
        
    for i in [32, 37, 42, 47, 52, 57]:
        if tabla1996.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1996 <= 1:
            tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1996
        else:
            tabla1996.loc[i, "P(x+5)"] = 1

    for i in range(22, 28):
        if i not in [22, 27]:
            if (tabla1996.loc[22, "P(x+5)"] == 1 or tabla1996.loc[27, "P(x+5)"] == 1):
                if tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5)) >= 1:
                    tabla1996.loc[i, "P(x+5)"] = 1
                else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5))
            else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"]
            
    for i in range(27, 33):
        if i not in [27, 32]:
            if (tabla1996.loc[27, "P(x+5)"] == 1 or tabla1996.loc[32, "P(x+5)"] == 1):
                if tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5)) >= 1:
                    tabla1996.loc[i, "P(x+5)"] = 1
                else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5))
            else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"]       

    for i in range(32, 38):
        if i not in [32, 37]:
            if (tabla1996.loc[32, "P(x+5)"] == 1 or tabla1996.loc[37, "P(x+5)"] == 1):
                if tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5)) >= 1:
                    tabla1996.loc[i, "P(x+5)"] = 1
                else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5))
            else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"] 
            
    for i in range(37, 43):
        if i not in [37, 42]:
            if (tabla1996.loc[37, "P(x+5)"] == 1 or tabla1996.loc[42, "P(x+5)"] == 1):
                if tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5)) >= 1:
                    tabla1996.loc[i, "P(x+5)"] = 1
                else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5))
            else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"]  

    for i in range(42, 48):
        if i not in [42, 47]:
            if (tabla1996.loc[42, "P(x+5)"] == 1 or tabla1996.loc[47, "P(x+5)"] == 1):
                if tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5)) >= 1:
                    tabla1996.loc[i, "P(x+5)"] = 1
                else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5))
            else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"]  

    for i in range(47, 53):
        if i not in [47, 52]:
            if (tabla1996.loc[47, "P(x+5)"] == 1 or tabla1996.loc[52, "P(x+5)"] == 1):
                if tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5)) >= 1:
                    tabla1996.loc[i, "P(x+5)"] = 1
                else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5))
            else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"]  
            
    for i in range(52, 58):
        if i not in [52, 57]:
            if (tabla1996.loc[52, "P(x+5)"] == 1 or tabla1996.loc[57, "P(x+5)"] == 1):
                if tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5)) >= 1:
                    tabla1996.loc[i, "P(x+5)"] = 1
                else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5))
            else: tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"]

    for i in range(58, 61):
        if tabla1996.loc[i-1, "P(x+5)"] == 1:
            tabla1996.loc[i, "P(x+5)"] = 1
        if tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5)) < 1:
            tabla1996.loc[i, "P(x+5)"] = tabla1996.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1996 ** (1/5))
        else: tabla1996.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1996.loc[0, "S(x)"] = 100000
    tabla1996.loc[2, "S(x)"] = tabla1996.loc[0, "S(x)"] * tabla1996.loc[2, "P(x+5)"]

    for i in [7, 12, 17, 22]:
        tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-5, "S(x)"] * tabla1996.loc[i, "P(x+5)"]
        
    tabla1996.loc[0, "FACTOR ANUAL"] = (tabla1996.loc[0, "S(x)"] / tabla1996.loc[2, "S(x)"]) ** (1/2)

    for i in [2, 7, 12, 17]:
        tabla1996.loc[i, "FACTOR ANUAL"] = (tabla1996.loc[i, "S(x)"] / tabla1996.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 22):
        if i not in [2, 7, 12, 17]:
            tabla1996.loc[i, "FACTOR ANUAL"] = tabla1996.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 22):
        if i not in [2, 7, 12, 17]:
            if tabla1996.loc[i, "FACTOR ANUAL"] == 1:
                tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] / tabla1996.loc[i, "FACTOR ANUAL"]
            else: tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] / tabla1996.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1996.loc[22, "P(x+5)"] == 1:
        tabla1996.loc[22, "S(x)"] = tabla1996.loc[21, "S(x)"] * tabla1996.loc[22, "P(x+5)"]
    else: tabla1996.loc[22, "S(x)"] = tabla1996.loc[17, "S(x)"] * tabla1996.loc[22, "P(x+5)"]
    
    if tabla1996.loc[27, "P(x+5)"] == 1:
        tabla1996.loc[22, "FACTOR ANUAL"] = 1
    else: tabla1996.loc[22, "FACTOR ANUAL"] = (tabla1996.loc[22, "S(x)"] / ((tabla1996.loc[22, "S(x)"] * tabla1996.loc[27, "P(x+5)"]))) ** (1/5)    

    for i in range(23, 27):
        if tabla1996.loc[27, "P(x+5)"] == 1:
            tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] * tabla1996.loc[i, "P(x+5)"]
        else: tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1 , "S(x)"] / tabla1996.loc[22, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1996.loc[27, "P(x+5)"] == 1:
        tabla1996.loc[27, "S(x)"] = tabla1996.loc[26, "S(x)"] * tabla1996.loc[27, "P(x+5)"]
    else: tabla1996.loc[27, "S(x)"] = tabla1996.loc[22, "S(x)"] * tabla1996.loc[27, "P(x+5)"]
    
    if tabla1996.loc[32, "P(x+5)"] == 1:
        tabla1996.loc[27, "FACTOR ANUAL"] = 1
    else: tabla1996.loc[27, "FACTOR ANUAL"] = (tabla1996.loc[27, "S(x)"] / ((tabla1996.loc[27, "S(x)"] * tabla1996.loc[32, "P(x+5)"]))) ** (1/5)    

    for i in range(28, 32):
        if tabla1996.loc[32, "P(x+5)"] == 1:
            tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] * tabla1996.loc[i, "P(x+5)"]
        else: tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1 , "S(x)"] / tabla1996.loc[27, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1996.loc[32, "P(x+5)"] == 1:
        tabla1996.loc[32, "S(x)"] = tabla1996.loc[31, "S(x)"] * tabla1996.loc[32, "P(x+5)"]
    else: tabla1996.loc[32, "S(x)"] = tabla1996.loc[27, "S(x)"] * tabla1996.loc[32, "P(x+5)"]
    
    if tabla1996.loc[37, "P(x+5)"] == 1:
        tabla1996.loc[32, "FACTOR ANUAL"] = 1
    else: tabla1996.loc[32, "FACTOR ANUAL"] = (tabla1996.loc[32, "S(x)"] / ((tabla1996.loc[32, "S(x)"] * tabla1996.loc[37, "P(x+5)"]))) ** (1/5)    

    for i in range(33, 37):
        if tabla1996.loc[37, "P(x+5)"] == 1 or tabla1996.loc[32, "P(x+5)"] == 1:
            tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] * tabla1996.loc[i, "P(x+5)"]
        else: tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1 , "S(x)"] / tabla1996.loc[32, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1996.loc[37, "P(x+5)"] == 1:
        tabla1996.loc[37, "S(x)"] = tabla1996.loc[36, "S(x)"] * tabla1996.loc[37, "P(x+5)"]
    else: tabla1996.loc[37, "S(x)"] = tabla1996.loc[32, "S(x)"] * tabla1996.loc[37, "P(x+5)"]

    #i+5   
    if tabla1996.loc[42, "P(x+5)"] == 1:
        tabla1996.loc[37, "FACTOR ANUAL"] = 1
    else: tabla1996.loc[37, "FACTOR ANUAL"] = (tabla1996.loc[37, "S(x)"] / ((tabla1996.loc[37, "S(x)"] * tabla1996.loc[42, "P(x+5)"]))) ** (1/5)    

    for i in range(38, 42):
        if tabla1996.loc[42, "P(x+5)"] == 1 or tabla1996.loc[37, "P(x+5)"] == 1:
            tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] * tabla1996.loc[i, "P(x+5)"]
        else: tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1 , "S(x)"] / tabla1996.loc[37, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1996.loc[42, "P(x+5)"] == 1:
        tabla1996.loc[42, "S(x)"] = tabla1996.loc[41, "S(x)"] * tabla1996.loc[42, "P(x+5)"]
    else: tabla1996.loc[42, "S(x)"] = tabla1996.loc[37, "S(x)"] * tabla1996.loc[42, "P(x+5)"]
    
    if tabla1996.loc[47, "P(x+5)"] == 1:
        tabla1996.loc[42, "FACTOR ANUAL"] = 1
    else: tabla1996.loc[42, "FACTOR ANUAL"] = (tabla1996.loc[42, "S(x)"] / ((tabla1996.loc[42, "S(x)"] * tabla1996.loc[47, "P(x+5)"]))) ** (1/5)    

    for i in range(43, 47):
        if tabla1996.loc[47, "P(x+5)"] == 1 or tabla1996.loc[42, "P(x+5)"] == 1:
            tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] * tabla1996.loc[i, "P(x+5)"]
        else: tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1 , "S(x)"] / tabla1996.loc[42, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1996.loc[47, "P(x+5)"] == 1:
        tabla1996.loc[47, "S(x)"] = tabla1996.loc[46, "S(x)"] * tabla1996.loc[47, "P(x+5)"]
    else: tabla1996.loc[47, "S(x)"] = tabla1996.loc[42, "S(x)"] * tabla1996.loc[47, "P(x+5)"]

    if tabla1996.loc[52, "P(x+5)"] == 1:
        tabla1996.loc[47, "FACTOR ANUAL"] = 1
    else: tabla1996.loc[47, "FACTOR ANUAL"] = (tabla1996.loc[47, "S(x)"] / ((tabla1996.loc[47, "S(x)"] * tabla1996.loc[52, "P(x+5)"]))) ** (1/5) 

    for i in range(48, 52):
        if tabla1996.loc[52, "P(x+5)"] == 1 or tabla1996.loc[47, "P(x+5)"] == 1:
            tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] * tabla1996.loc[i, "P(x+5)"]
        else: tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1 , "S(x)"] / tabla1996.loc[47, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1996.loc[52, "P(x+5)"] == 1:
        tabla1996.loc[52, "S(x)"] = tabla1996.loc[51, "S(x)"] * tabla1996.loc[52, "P(x+5)"]
    else: tabla1996.loc[52, "S(x)"] = tabla1996.loc[47, "S(x)"] * tabla1996.loc[52, "P(x+5)"]

    if tabla1996.loc[57, "P(x+5)"] == 1:
        tabla1996.loc[52, "FACTOR ANUAL"] = 1
    else: tabla1996.loc[52, "FACTOR ANUAL"] = (tabla1996.loc[52, "S(x)"] / ((tabla1996.loc[52, "S(x)"] * tabla1996.loc[57, "P(x+5)"]))) ** (1/5) 

    for i in range(53, 57):
        if tabla1996.loc[57, "P(x+5)"] == 1 or tabla1996.loc[52, "P(x+5)"] == 1:
            tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] * tabla1996.loc[i, "P(x+5)"]
        else: tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1 , "S(x)"] / tabla1996.loc[52, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1996.loc[57, "P(x+5)"] == 1:
        tabla1996.loc[57, "S(x)"] = tabla1996.loc[56, "S(x)"] * tabla1996.loc[57, "P(x+5)"]
    else: tabla1996.loc[57, "S(x)"] = tabla1996.loc[52, "S(x)"] * tabla1996.loc[57, "P(x+5)"]

    for i in range(58, 61):
        if tabla1996.loc[i-1, "P(x+5)"] == 1:
            tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] * tabla1996.loc[i, "P(x+5)"]
        else: tabla1996.loc[i, "S(x)"] = tabla1996.loc[i-1, "S(x)"] * tabla1996.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1997 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1997] = tabla1997

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1997.loc[1, "P(x+5)"] = GENERACION_1997.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1997
    tabla1997.loc[2: 5, "P(x+5)"] = tabla1997.loc[1, "P(x+5)"]
    tabla1997.loc[6, "P(x+5)"] = GENERACION_1997.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1997.loc[7: 10, "P(x+5)"] = tabla1997.loc[6, "P(x+5)"]
    tabla1997.loc[11, "P(x+5)"] = GENERACION_1997.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1997.loc[12: 15, "P(x+5)"] = tabla1997.loc[11, "P(x+5)"]
    tabla1997.loc[16, "P(x+5)"] = GENERACION_1997.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1997.loc[17: 20, "P(x+5)"] = tabla1997.loc[16, "P(x+5)"]
    tabla1997.loc[21, "P(x+5)"] = GENERACION_1997.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1997.loc[26, "P(x+5)"] = GENERACION_1997.loc[4, "PROBABILIDAD QUINQUENAL"]

    for i in [31, 36, 41, 46, 51, 56]:
        if tabla1997.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1997 <= 1:
            tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1997
        else:
            tabla1997.loc[i, "P(x+5)"] = 1

    for i in range(21, 27):
        if i not in [21, 26]:
            if (tabla1997.loc[21, "P(x+5)"] == 1 or tabla1997.loc[26, "P(x+5)"] == 1):
                if tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5)) >= 1:
                    tabla1997.loc[i, "P(x+5)"] = 1
                else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5))
            else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] 

    for i in range(26, 32):
        if i not in [26, 31]:
            if (tabla1997.loc[26, "P(x+5)"] == 1 or tabla1997.loc[31, "P(x+5)"] == 1):
                if tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5)) >= 1:
                    tabla1997.loc[i, "P(x+5)"] = 1
                else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5))
            else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] 

    for i in range(31, 37):
        if i not in [31, 36]:
            if (tabla1997.loc[31, "P(x+5)"] == 1 or tabla1997.loc[36, "P(x+5)"] == 1):
                if tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5)) >= 1:
                    tabla1997.loc[i, "P(x+5)"] = 1
                else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5))
            else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] 

    for i in range(36, 42):
        if i not in [36, 41]:
            if (tabla1997.loc[36, "P(x+5)"] == 1 or tabla1997.loc[41, "P(x+5)"] == 1):
                if tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5)) >= 1:
                    tabla1997.loc[i, "P(x+5)"] = 1
                else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5))
            else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] 

    for i in range(41, 47):
        if i not in [41, 46]:
            if (tabla1997.loc[41, "P(x+5)"] == 1 or tabla1997.loc[46, "P(x+5)"] == 1):
                if tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5)) >= 1:
                    tabla1997.loc[i, "P(x+5)"] = 1
                else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5))
            else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"]  

    for i in range(46, 52):
        if i not in [46, 51]:
            if (tabla1997.loc[46, "P(x+5)"] == 1 or tabla1997.loc[51, "P(x+5)"] == 1):
                if tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5)) >= 1:
                    tabla1997.loc[i, "P(x+5)"] = 1
                else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5))
            else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"]  
            
    for i in range(51, 57):
        if i not in [51, 56]:
            if (tabla1997.loc[51, "P(x+5)"] == 1 or tabla1997.loc[56, "P(x+5)"] == 1):
                if tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5)) >= 1:
                    tabla1997.loc[i, "P(x+5)"] = 1
                else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5))
            else: tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"]

    for i in range(57, 61):
        if tabla1997.loc[i-1, "P(x+5)"] == 1:
            tabla1997.loc[i, "P(x+5)"] = 1
        if tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5)) < 1:
            tabla1997.loc[i, "P(x+5)"] = tabla1997.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1997 ** (1/5))
        else: tabla1997.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1997.loc[0, "S(x)"] = 100000
    tabla1997.loc[1, "S(x)"] = tabla1997.loc[0, "S(x)"] * tabla1997.loc[1, "P(x+5)"]

    for i in [6, 11, 16, 21]:
        tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-5, "S(x)"] * tabla1997.loc[i, "P(x+5)"]
        
    #tabla1997.loc[0, "FACTOR ANUAL"] = (tabla1997.loc[0, "S(x)"] / tabla1997.loc[1, "S(x)"]) ** (1/5)

    for i in [1, 6, 11, 16]:
        tabla1997.loc[i, "FACTOR ANUAL"] = (tabla1997.loc[i, "S(x)"] / tabla1997.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 21):
        if i not in [1, 6, 11, 16]:
            tabla1997.loc[i, "FACTOR ANUAL"] = tabla1997.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 21):
        if i not in [1, 6, 11, 16]:
            if tabla1997.loc[i, "FACTOR ANUAL"] == 1:
                tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] / tabla1997.loc[i, "FACTOR ANUAL"]
            else: tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] / tabla1997.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1997.loc[21, "P(x+5)"] == 1:
        tabla1997.loc[21, "S(x)"] = tabla1997.loc[20, "S(x)"] * tabla1997.loc[21, "P(x+5)"]
    else: tabla1997.loc[21, "S(x)"] = tabla1997.loc[16, "S(x)"] * tabla1997.loc[21, "P(x+5)"]
    
    if tabla1997.loc[26, "P(x+5)"] == 1:
        tabla1997.loc[21, "FACTOR ANUAL"] = 1
    else: tabla1997.loc[21, "FACTOR ANUAL"] = (tabla1997.loc[21, "S(x)"] / ((tabla1997.loc[21, "S(x)"] * tabla1997.loc[26, "P(x+5)"]))) ** (1/5)    

    for i in range(22, 26):
        if tabla1997.loc[26, "P(x+5)"] == 1:
            tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] * tabla1997.loc[i, "P(x+5)"]
        else: tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1 , "S(x)"] / tabla1997.loc[21, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1997.loc[26, "P(x+5)"] == 1:
        tabla1997.loc[26, "S(x)"] = tabla1997.loc[25, "S(x)"] * tabla1997.loc[26, "P(x+5)"]
    else: tabla1997.loc[26, "S(x)"] = tabla1997.loc[21, "S(x)"] * tabla1997.loc[26, "P(x+5)"]
    
    if tabla1997.loc[31, "P(x+5)"] == 1:
        tabla1997.loc[26, "FACTOR ANUAL"] = 1
    else: tabla1997.loc[26, "FACTOR ANUAL"] = (tabla1997.loc[26, "S(x)"] / ((tabla1997.loc[26, "S(x)"] * tabla1997.loc[31, "P(x+5)"]))) ** (1/5)    

    for i in range(27, 31):
        if tabla1997.loc[31, "P(x+5)"] == 1:
            tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] * tabla1997.loc[i, "P(x+5)"]
        else: tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1 , "S(x)"] / tabla1997.loc[26, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1997.loc[31, "P(x+5)"] == 1:
        tabla1997.loc[31, "S(x)"] = tabla1997.loc[30, "S(x)"] * tabla1997.loc[31, "P(x+5)"]
    else: tabla1997.loc[31, "S(x)"] = tabla1997.loc[26, "S(x)"] * tabla1997.loc[31, "P(x+5)"]
    
    if tabla1997.loc[36, "P(x+5)"] == 1:
        tabla1997.loc[31, "FACTOR ANUAL"] = 1
    else: tabla1997.loc[31, "FACTOR ANUAL"] = (tabla1997.loc[31, "S(x)"] / ((tabla1997.loc[31, "S(x)"] * tabla1997.loc[36, "P(x+5)"]))) ** (1/5)    

    for i in range(32, 36):
        if tabla1997.loc[36, "P(x+5)"] == 1 or tabla1997.loc[31, "P(x+5)"] == 1:
            tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] * tabla1997.loc[i, "P(x+5)"]
        else: tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1 , "S(x)"] / tabla1997.loc[31, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1997.loc[36, "P(x+5)"] == 1:
        tabla1997.loc[36, "S(x)"] = tabla1997.loc[35, "S(x)"] * tabla1997.loc[36, "P(x+5)"]
    else: tabla1997.loc[36, "S(x)"] = tabla1997.loc[31, "S(x)"] * tabla1997.loc[36, "P(x+5)"]

    #i+5   
    if tabla1997.loc[41, "P(x+5)"] == 1:
        tabla1997.loc[36, "FACTOR ANUAL"] = 1
    else: tabla1997.loc[36, "FACTOR ANUAL"] = (tabla1997.loc[36, "S(x)"] / ((tabla1997.loc[36, "S(x)"] * tabla1997.loc[41, "P(x+5)"]))) ** (1/5)    

    for i in range(37, 41):
        if tabla1997.loc[41, "P(x+5)"] == 1 or tabla1997.loc[36, "P(x+5)"] == 1:
            tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] * tabla1997.loc[i, "P(x+5)"]
        else: tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1 , "S(x)"] / tabla1997.loc[36, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1997.loc[41, "P(x+5)"] == 1:
        tabla1997.loc[41, "S(x)"] = tabla1997.loc[40, "S(x)"] * tabla1997.loc[41, "P(x+5)"]
    else: tabla1997.loc[41, "S(x)"] = tabla1997.loc[36, "S(x)"] * tabla1997.loc[41, "P(x+5)"]
    
    if tabla1997.loc[46, "P(x+5)"] == 1:
        tabla1997.loc[41, "FACTOR ANUAL"] = 1
    else: tabla1997.loc[41, "FACTOR ANUAL"] = (tabla1997.loc[41, "S(x)"] / ((tabla1997.loc[41, "S(x)"] * tabla1997.loc[46, "P(x+5)"]))) ** (1/5)    

    for i in range(42, 46):
        if tabla1997.loc[46, "P(x+5)"] == 1 or tabla1997.loc[41, "P(x+5)"] == 1:
            tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] * tabla1997.loc[i, "P(x+5)"]
        else: tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1 , "S(x)"] / tabla1997.loc[41, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1997.loc[46, "P(x+5)"] == 1:
        tabla1997.loc[46, "S(x)"] = tabla1997.loc[45, "S(x)"] * tabla1997.loc[46, "P(x+5)"]
    else: tabla1997.loc[46, "S(x)"] = tabla1997.loc[41, "S(x)"] * tabla1997.loc[46, "P(x+5)"]

    if tabla1997.loc[51, "P(x+5)"] == 1:
        tabla1997.loc[46, "FACTOR ANUAL"] = 1
    else: tabla1997.loc[46, "FACTOR ANUAL"] = (tabla1997.loc[46, "S(x)"] / ((tabla1997.loc[46, "S(x)"] * tabla1997.loc[51, "P(x+5)"]))) ** (1/5) 

    for i in range(47, 51):
        if tabla1997.loc[51, "P(x+5)"] == 1 or tabla1997.loc[46, "P(x+5)"] == 1:
            tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] * tabla1997.loc[i, "P(x+5)"]
        else: tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1 , "S(x)"] / tabla1997.loc[46, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1997.loc[51, "P(x+5)"] == 1:
        tabla1997.loc[51, "S(x)"] = tabla1997.loc[50, "S(x)"] * tabla1997.loc[52, "P(x+5)"]
    else: tabla1997.loc[51, "S(x)"] = tabla1997.loc[46, "S(x)"] * tabla1997.loc[51, "P(x+5)"]

    if tabla1997.loc[56, "P(x+5)"] == 1:
        tabla1997.loc[51, "FACTOR ANUAL"] = 1
    else: tabla1997.loc[51, "FACTOR ANUAL"] = (tabla1997.loc[51, "S(x)"] / ((tabla1997.loc[51, "S(x)"] * tabla1997.loc[56, "P(x+5)"]))) ** (1/5) 

    for i in range(52, 56):
        if tabla1997.loc[56, "P(x+5)"] == 1 or tabla1997.loc[51, "P(x+5)"] == 1:
            tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] * tabla1997.loc[i, "P(x+5)"]
        else: tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1 , "S(x)"] / tabla1997.loc[51, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1997.loc[56, "P(x+5)"] == 1:
        tabla1997.loc[56, "S(x)"] = tabla1997.loc[55, "S(x)"] * tabla1997.loc[56, "P(x+5)"]
    else: tabla1997.loc[56, "S(x)"] = tabla1997.loc[51, "S(x)"] * tabla1997.loc[56, "P(x+5)"]

    for i in range(57, 61):
        if tabla1997.loc[i-1, "P(x+5)"] == 1:
            tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] * tabla1997.loc[i, "P(x+5)"]
        else: tabla1997.loc[i, "S(x)"] = tabla1997.loc[i-1, "S(x)"] * tabla1997.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1998 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1998] = tabla1998

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1998.loc[5, "P(x+5)"] = GENERACION_1998.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1998.loc[6: 9, "P(x+5)"] = tabla1998.loc[5, "P(x+5)"]
    tabla1998.loc[10, "P(x+5)"] = GENERACION_1998.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1998.loc[11: 14, "P(x+5)"] = tabla1998.loc[10, "P(x+5)"]
    tabla1998.loc[15, "P(x+5)"] = GENERACION_1998.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1998.loc[16: 19, "P(x+5)"] = tabla1998.loc[15, "P(x+5)"]
    tabla1998.loc[20, "P(x+5)"] = GENERACION_1998.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla1998.loc[21: 24, "P(x+5)"] = tabla1998.loc[20, "P(x+5)"]
    tabla1998.loc[25, "P(x+5)"] = GENERACION_1998.loc[4, "PROBABILIDAD QUINQUENAL"]
    tabla1998.loc[30, "P(x+5)"] = GENERACION_1998.loc[5, "PROBABILIDAD QUINQUENAL"]

    for i in [35, 40, 45, 50, 55, 60]:
        if tabla1998.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1998 <= 1:
            tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1998
        else:
            tabla1998.loc[i, "P(x+5)"] = 1

    for i in range(25, 31):
        if i not in [25, 30]:
            if (tabla1998.loc[25, "P(x+5)"] == 1 or tabla1998.loc[30, "P(x+5)"] == 1):
                if tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5)) >= 1:
                    tabla1998.loc[i, "P(x+5)"] = 1
                else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5))
            else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] 

    for i in range(30, 36):
        if i not in [30, 35]:
            if (tabla1998.loc[30, "P(x+5)"] == 1 or tabla1998.loc[35, "P(x+5)"] == 1):
                if tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5)) >= 1:
                    tabla1998.loc[i, "P(x+5)"] = 1
                else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5))
            else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] 

    for i in range(35, 41):
        if i not in [35, 40]:
            if (tabla1998.loc[35, "P(x+5)"] == 1 or tabla1998.loc[40, "P(x+5)"] == 1):
                if tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5)) >= 1:
                    tabla1998.loc[i, "P(x+5)"] = 1
                else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5))
            else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] 

    for i in range(40, 46):
        if i not in [40, 45]:
            if (tabla1998.loc[40, "P(x+5)"] == 1 or tabla1998.loc[45, "P(x+5)"] == 1):
                if tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5)) >= 1:
                    tabla1998.loc[i, "P(x+5)"] = 1
                else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5))
            else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] 

    for i in range(45, 51):
        if i not in [45, 50]:
            if (tabla1998.loc[45, "P(x+5)"] == 1 or tabla1998.loc[50, "P(x+5)"] == 1):
                if tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5)) >= 1:
                    tabla1998.loc[i, "P(x+5)"] = 1
                else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5))
            else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"]  

    for i in range(50, 56):
        if i not in [50, 55]:
            if (tabla1998.loc[50, "P(x+5)"] == 1 or tabla1998.loc[55, "P(x+5)"] == 1):
                if tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5)) >= 1:
                    tabla1998.loc[i, "P(x+5)"] = 1
                else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5))
            else: tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"]  
            
    for i in range(56, 61):
        if i not in [60]:
            if tabla1998.loc[i-1, "P(x+5)"] == 1:
                tabla1998.loc[i, "P(x+5)"] = 1
            if tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5)) < 1:
                tabla1998.loc[i, "P(x+5)"] = tabla1998.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1998 ** (1/5))
            else: tabla1998.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1998.loc[0, "S(x)"] = 100000
    tabla1998.loc[5, "S(x)"] = tabla1998.loc[0, "S(x)"] * tabla1998.loc[5, "P(x+5)"]

    for i in [10, 15, 20, 25]:
        tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-5, "S(x)"] * tabla1998.loc[i, "P(x+5)"]
        
    tabla1998.loc[0, "FACTOR ANUAL"] = (tabla1998.loc[0, "S(x)"] / tabla1998.loc[5, "S(x)"]) ** (1/5)

    for i in [5, 10, 15, 20]:
        tabla1998.loc[i, "FACTOR ANUAL"] = (tabla1998.loc[i, "S(x)"] / tabla1998.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 25):
        if i not in [5, 10, 15, 20]:
            tabla1998.loc[i, "FACTOR ANUAL"] = tabla1998.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 25):
        if i not in [5, 10, 15, 20]:
            if tabla1998.loc[i, "FACTOR ANUAL"] == 1:
                tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1, "S(x)"] / tabla1998.loc[i, "FACTOR ANUAL"]
            else: tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1, "S(x)"] / tabla1998.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1998.loc[25, "P(x+5)"] == 1:
        tabla1998.loc[25, "S(x)"] = tabla1998.loc[24, "S(x)"] * tabla1998.loc[25, "P(x+5)"]
    else: tabla1998.loc[25, "S(x)"] = tabla1998.loc[20, "S(x)"] * tabla1998.loc[25, "P(x+5)"]
    
    if tabla1998.loc[30, "P(x+5)"] == 1:
        tabla1998.loc[25, "FACTOR ANUAL"] = 1
    else: tabla1998.loc[25, "FACTOR ANUAL"] = (tabla1998.loc[25, "S(x)"] / ((tabla1998.loc[25, "S(x)"] * tabla1998.loc[30, "P(x+5)"]))) ** (1/5)    

    for i in range(26, 30):
        if tabla1998.loc[30, "P(x+5)"] == 1:
            tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1, "S(x)"] * tabla1998.loc[i, "P(x+5)"]
        else: tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1 , "S(x)"] / tabla1998.loc[25, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1998.loc[30, "P(x+5)"] == 1:
        tabla1998.loc[30, "S(x)"] = tabla1998.loc[29, "S(x)"] * tabla1998.loc[30, "P(x+5)"]
    else: tabla1998.loc[30, "S(x)"] = tabla1998.loc[25, "S(x)"] * tabla1998.loc[30, "P(x+5)"]
    
    if tabla1998.loc[35, "P(x+5)"] == 1:
        tabla1998.loc[30, "FACTOR ANUAL"] = 1
    else: tabla1998.loc[30, "FACTOR ANUAL"] = (tabla1998.loc[30, "S(x)"] / ((tabla1998.loc[30, "S(x)"] * tabla1998.loc[35, "P(x+5)"]))) ** (1/5)    

    for i in range(31, 35):
        if tabla1998.loc[35, "P(x+5)"] == 1:
            tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1, "S(x)"] * tabla1998.loc[i, "P(x+5)"]
        else: tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1 , "S(x)"] / tabla1998.loc[30, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1998.loc[35, "P(x+5)"] == 1:
        tabla1998.loc[35, "S(x)"] = tabla1998.loc[34, "S(x)"] * tabla1998.loc[35, "P(x+5)"]
    else: tabla1998.loc[35, "S(x)"] = tabla1998.loc[30, "S(x)"] * tabla1998.loc[35, "P(x+5)"]
    
    if tabla1998.loc[40, "P(x+5)"] == 1:
        tabla1998.loc[35, "FACTOR ANUAL"] = 1
    else: tabla1998.loc[35, "FACTOR ANUAL"] = (tabla1998.loc[35, "S(x)"] / ((tabla1998.loc[35, "S(x)"] * tabla1998.loc[40, "P(x+5)"]))) ** (1/5)    

    for i in range(36, 40):
        if tabla1998.loc[40, "P(x+5)"] == 1 or tabla1998.loc[35, "P(x+5)"] == 1:
            tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1, "S(x)"] * tabla1998.loc[i, "P(x+5)"]
        else: tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1 , "S(x)"] / tabla1998.loc[35, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1998.loc[40, "P(x+5)"] == 1:
        tabla1998.loc[40, "S(x)"] = tabla1998.loc[39, "S(x)"] * tabla1998.loc[40, "P(x+5)"]
    else: tabla1998.loc[40, "S(x)"] = tabla1998.loc[35, "S(x)"] * tabla1998.loc[40, "P(x+5)"]

    #i+5   
    if tabla1998.loc[45, "P(x+5)"] == 1:
        tabla1998.loc[40, "FACTOR ANUAL"] = 1
    else: tabla1998.loc[40, "FACTOR ANUAL"] = (tabla1998.loc[40, "S(x)"] / ((tabla1998.loc[40, "S(x)"] * tabla1998.loc[45, "P(x+5)"]))) ** (1/5)    

    for i in range(41, 45):
        if tabla1998.loc[45, "P(x+5)"] == 1 or tabla1998.loc[40, "P(x+5)"] == 1:
            tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1, "S(x)"] * tabla1998.loc[i, "P(x+5)"]
        else: tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1 , "S(x)"] / tabla1998.loc[40, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1998.loc[45, "P(x+5)"] == 1:
        tabla1998.loc[45, "S(x)"] = tabla1998.loc[44, "S(x)"] * tabla1998.loc[45, "P(x+5)"]
    else: tabla1998.loc[45, "S(x)"] = tabla1998.loc[40, "S(x)"] * tabla1998.loc[45, "P(x+5)"]
    
    if tabla1998.loc[50, "P(x+5)"] == 1:
        tabla1998.loc[45, "FACTOR ANUAL"] = 1
    else: tabla1998.loc[45, "FACTOR ANUAL"] = (tabla1998.loc[45, "S(x)"] / ((tabla1998.loc[45, "S(x)"] * tabla1998.loc[50, "P(x+5)"]))) ** (1/5)    

    for i in range(46, 50):
        if tabla1998.loc[50, "P(x+5)"] == 1 or tabla1998.loc[45, "P(x+5)"] == 1:
            tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1, "S(x)"] * tabla1998.loc[i, "P(x+5)"]
        else: tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1 , "S(x)"] / tabla1998.loc[45, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1998.loc[50, "P(x+5)"] == 1:
        tabla1998.loc[50, "S(x)"] = tabla1998.loc[49, "S(x)"] * tabla1998.loc[50, "P(x+5)"]
    else: tabla1998.loc[50, "S(x)"] = tabla1998.loc[45, "S(x)"] * tabla1998.loc[50, "P(x+5)"]

    if tabla1998.loc[55, "P(x+5)"] == 1:
        tabla1998.loc[50, "FACTOR ANUAL"] = 1
    else: tabla1998.loc[50, "FACTOR ANUAL"] = (tabla1998.loc[50, "S(x)"] / ((tabla1998.loc[50, "S(x)"] * tabla1998.loc[55, "P(x+5)"]))) ** (1/5) 

    for i in range(51, 55):
        if tabla1998.loc[55, "P(x+5)"] == 1 or tabla1998.loc[50, "P(x+5)"] == 1:
            tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1, "S(x)"] * tabla1998.loc[i, "P(x+5)"]
        else: tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1 , "S(x)"] / tabla1998.loc[50, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    

    if tabla1998.loc[55, "P(x+5)"] == 1:
        tabla1998.loc[55, "S(x)"] = tabla1998.loc[54, "S(x)"] * tabla1998.loc[55, "P(x+5)"]
    else: tabla1998.loc[55, "S(x)"] = tabla1998.loc[50, "S(x)"] * tabla1998.loc[55, "P(x+5)"]

    if tabla1998.loc[60, "P(x+5)"] == 1:
        tabla1998.loc[55, "FACTOR ANUAL"] = 1
    else: tabla1998.loc[55, "FACTOR ANUAL"] = (tabla1998.loc[55, "S(x)"] / ((tabla1998.loc[55, "S(x)"] * tabla1998.loc[60, "P(x+5)"]))) ** (1/5) 

    for i in range(56, 60):
        if tabla1998.loc[60, "P(x+5)"] == 1 or tabla1998.loc[55, "P(x+5)"] == 1:
            tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1, "S(x)"] * tabla1998.loc[i, "P(x+5)"]
        else: tabla1998.loc[i, "S(x)"] = tabla1998.loc[i-1 , "S(x)"] / tabla1998.loc[55, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1998.loc[60, "P(x+5)"] == 1:
        tabla1998.loc[60, "S(x)"] = tabla1998.loc[60, "P(x+5)"] * tabla1998.loc[59, "S(x)"]
    else: tabla1998.loc[60, "S(x)"] = tabla1998.loc[60, "P(x+5)"] * tabla1998.loc[55, "S(x)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla1999 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[1999] = tabla1999

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla1999.loc[4, "P(x+5)"] = GENERACION_1999.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL1999
    tabla1999.loc[5: 8, "P(x+5)"] = tabla1999.loc[4, "P(x+5)"]
    tabla1999.loc[9, "P(x+5)"] = GENERACION_1999.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla1999.loc[10: 13, "P(x+5)"] = tabla1999.loc[9, "P(x+5)"]
    tabla1999.loc[14, "P(x+5)"] = GENERACION_1999.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla1999.loc[15: 18, "P(x+5)"] = tabla1999.loc[14, "P(x+5)"]
    tabla1999.loc[19, "P(x+5)"] = GENERACION_1999.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla1999.loc[24, "P(x+5)"] = GENERACION_1999.loc[3, "PROBABILIDAD QUINQUENAL"]

    for i in [29, 34, 39, 44, 49, 54, 59]:
        if tabla1999.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1999 <= 1:
            tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL1999
        else:
            tabla1999.loc[i, "P(x+5)"] = 1

    for i in range(19, 25):
        if i not in [19, 24]:
            if (tabla1999.loc[19, "P(x+5)"] == 1 or tabla1999.loc[24, "P(x+5)"] == 1):
                if tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5)) >= 1:
                    tabla1999.loc[i, "P(x+5)"] = 1
                else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5))
            else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"]

    for i in range(24, 30):
        if i not in [24, 29]:
            if (tabla1999.loc[24, "P(x+5)"] == 1 or tabla1999.loc[29, "P(x+5)"] == 1):
                if tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5)) >= 1:
                    tabla1999.loc[i, "P(x+5)"] = 1
                else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5))
            else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] 

    for i in range(29, 35):
        if i not in [29, 34]:
            if (tabla1999.loc[29, "P(x+5)"] == 1 or tabla1999.loc[34, "P(x+5)"] == 1):
                if tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5)) >= 1:
                    tabla1999.loc[i, "P(x+5)"] = 1
                else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5))
            else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] 

    for i in range(34, 40):
        if i not in [34, 39]:
            if (tabla1999.loc[34, "P(x+5)"] == 1 or tabla1999.loc[39, "P(x+5)"] == 1):
                if tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5)) >= 1:
                    tabla1999.loc[i, "P(x+5)"] = 1
                else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5))
            else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] 

    for i in range(39, 45):
        if i not in [39, 44]:
            if (tabla1999.loc[39, "P(x+5)"] == 1 or tabla1999.loc[44, "P(x+5)"] == 1):
                if tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5)) >= 1:
                    tabla1999.loc[i, "P(x+5)"] = 1
                else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5))
            else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] 

    for i in range(44, 50):
        if i not in [44, 49]:
            if (tabla1999.loc[44, "P(x+5)"] == 1 or tabla1999.loc[49, "P(x+5)"] == 1):
                if tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5)) >= 1:
                    tabla1999.loc[i, "P(x+5)"] = 1
                else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5))
            else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"]  

    for i in range(49, 55):
        if i not in [49, 54]:
            if (tabla1999.loc[49, "P(x+5)"] == 1 or tabla1999.loc[54, "P(x+5)"] == 1):
                if tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5)) >= 1:
                    tabla1999.loc[i, "P(x+5)"] = 1
                else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5))
            else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"]  
            
    for i in range(54, 60):
        if i not in [54, 59]:
            if (tabla1999.loc[54, "P(x+5)"] == 1 or tabla1999.loc[59, "P(x+5)"] == 1):
                if tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5)) >= 1:
                    tabla1999.loc[i, "P(x+5)"] = 1
                else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5))
            else: tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"]

    for i in range(60, 61):
        if tabla1999.loc[i-1, "P(x+5)"] == 1:
            tabla1999.loc[i, "P(x+5)"] = 1
        if tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5)) < 1:
            tabla1999.loc[i, "P(x+5)"] = tabla1999.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL1999 ** (1/5))
        else: tabla1999.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla1999.loc[0, "S(x)"] = 100000
    tabla1999.loc[4, "S(x)"] = tabla1999.loc[0, "S(x)"] * tabla1999.loc[4, "P(x+5)"]

    for i in [9, 14, 19]:
        tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-5, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
        
    tabla1999.loc[0, "FACTOR ANUAL"] = (tabla1999.loc[0, "S(x)"] / tabla1999.loc[4, "S(x)"]) ** (1/4)

    for i in [4, 9, 14]:
        tabla1999.loc[i, "FACTOR ANUAL"] = (tabla1999.loc[i, "S(x)"] / tabla1999.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 19):
        if i not in [4, 9, 14]:
            tabla1999.loc[i, "FACTOR ANUAL"] = tabla1999.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 19):
        if i not in [4, 9, 14]:
            if tabla1999.loc[i, "FACTOR ANUAL"] == 1:
                tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] / tabla1999.loc[i, "FACTOR ANUAL"]
            else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] / tabla1999.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1999.loc[19, "P(x+5)"] == 1:
        tabla1999.loc[19, "S(x)"] = tabla1999.loc[18, "S(x)"] * tabla1999.loc[19, "P(x+5)"]
    else: tabla1999.loc[19, "S(x)"] = tabla1999.loc[14, "S(x)"] * tabla1999.loc[19, "P(x+5)"]
    
    if tabla1999.loc[24, "P(x+5)"] == 1:
        tabla1999.loc[19, "FACTOR ANUAL"] = 1
    else: tabla1999.loc[19, "FACTOR ANUAL"] = (tabla1999.loc[19, "S(x)"] / ((tabla1999.loc[19, "S(x)"] * tabla1999.loc[24, "P(x+5)"]))) ** (1/5)    

    for i in range(20, 24):
        if tabla1999.loc[24, "P(x+5)"] == 1:
            tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
        else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1 , "S(x)"] / tabla1999.loc[19, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1999.loc[24, "P(x+5)"] == 1:
        tabla1999.loc[24, "S(x)"] = tabla1999.loc[23, "S(x)"] * tabla1999.loc[24, "P(x+5)"]
    else: tabla1999.loc[24, "S(x)"] = tabla1999.loc[19, "S(x)"] * tabla1999.loc[24, "P(x+5)"]
    
    if tabla1999.loc[29, "P(x+5)"] == 1:
        tabla1999.loc[24, "FACTOR ANUAL"] = 1
    else: tabla1999.loc[24, "FACTOR ANUAL"] = (tabla1999.loc[24, "S(x)"] / ((tabla1999.loc[24, "S(x)"] * tabla1999.loc[29, "P(x+5)"]))) ** (1/5)    

    for i in range(25, 29):
        if tabla1999.loc[29, "P(x+5)"] == 1:
            tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
        else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1 , "S(x)"] / tabla1999.loc[24, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1999.loc[29, "P(x+5)"] == 1:
        tabla1999.loc[29, "S(x)"] = tabla1999.loc[28, "S(x)"] * tabla1999.loc[29, "P(x+5)"]
    else: tabla1999.loc[29, "S(x)"] = tabla1999.loc[24, "S(x)"] * tabla1999.loc[29, "P(x+5)"]
    
    if tabla1999.loc[34, "P(x+5)"] == 1:
        tabla1999.loc[29, "FACTOR ANUAL"] = 1
    else: tabla1999.loc[29, "FACTOR ANUAL"] = (tabla1999.loc[29, "S(x)"] / ((tabla1999.loc[29, "S(x)"] * tabla1999.loc[34, "P(x+5)"]))) ** (1/5)    

    for i in range(30, 34):
        if tabla1999.loc[29, "P(x+5)"] == 1 or tabla1999.loc[34, "P(x+5)"] == 1:
            tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
        else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1 , "S(x)"] / tabla1999.loc[29, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1999.loc[34, "P(x+5)"] == 1:
        tabla1999.loc[34, "S(x)"] = tabla1999.loc[33, "S(x)"] * tabla1999.loc[34, "P(x+5)"]
    else: tabla1999.loc[34, "S(x)"] = tabla1999.loc[29, "S(x)"] * tabla1999.loc[34, "P(x+5)"]
    
    if tabla1999.loc[39, "P(x+5)"] == 1:
        tabla1999.loc[34, "FACTOR ANUAL"] = 1
    else: tabla1999.loc[34, "FACTOR ANUAL"] = (tabla1999.loc[34, "S(x)"] / ((tabla1999.loc[34, "S(x)"] * tabla1999.loc[39, "P(x+5)"]))) ** (1/5)    

    for i in range(35, 39):
        if tabla1999.loc[39, "P(x+5)"] == 1 or tabla1999.loc[34, "P(x+5)"] == 1:
            tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
        else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1 , "S(x)"] / tabla1999.loc[34, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla1999.loc[39, "P(x+5)"] == 1:
        tabla1999.loc[39, "S(x)"] = tabla1999.loc[38, "S(x)"] * tabla1999.loc[39, "P(x+5)"]
    else: tabla1999.loc[39, "S(x)"] = tabla1999.loc[34, "S(x)"] * tabla1999.loc[39, "P(x+5)"]

    #i+5   
    if tabla1999.loc[44, "P(x+5)"] == 1:
        tabla1999.loc[39, "FACTOR ANUAL"] = 1
    else: tabla1999.loc[39, "FACTOR ANUAL"] = (tabla1999.loc[39, "S(x)"] / ((tabla1999.loc[39, "S(x)"] * tabla1999.loc[44, "P(x+5)"]))) ** (1/5)    

    for i in range(40, 44):
        if tabla1999.loc[44, "P(x+5)"] == 1 or tabla1999.loc[39, "P(x+5)"] == 1:
            tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
        else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1 , "S(x)"] / tabla1999.loc[39, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1999.loc[44, "P(x+5)"] == 1:
        tabla1999.loc[44, "S(x)"] = tabla1999.loc[43, "S(x)"] * tabla1999.loc[44, "P(x+5)"]
    else: tabla1999.loc[44, "S(x)"] = tabla1999.loc[39, "S(x)"] * tabla1999.loc[44, "P(x+5)"]
    
    if tabla1999.loc[49, "P(x+5)"] == 1:
        tabla1999.loc[44, "FACTOR ANUAL"] = 1
    else: tabla1999.loc[44, "FACTOR ANUAL"] = (tabla1999.loc[44, "S(x)"] / ((tabla1999.loc[44, "S(x)"] * tabla1999.loc[49, "P(x+5)"]))) ** (1/5)    

    for i in range(45, 49):
        if tabla1999.loc[44, "P(x+5)"] == 1 or tabla1999.loc[49, "P(x+5)"] == 1:
            tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
        else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1 , "S(x)"] / tabla1999.loc[44, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1999.loc[49, "P(x+5)"] == 1:
        tabla1999.loc[49, "S(x)"] = tabla1999.loc[48, "S(x)"] * tabla1999.loc[49, "P(x+5)"]
    else: tabla1999.loc[49, "S(x)"] = tabla1999.loc[44, "S(x)"] * tabla1999.loc[49, "P(x+5)"]

    if tabla1999.loc[54, "P(x+5)"] == 1:
        tabla1999.loc[49, "FACTOR ANUAL"] = 1
    else: tabla1999.loc[49, "FACTOR ANUAL"] = (tabla1999.loc[49, "S(x)"] / ((tabla1999.loc[49, "S(x)"] * tabla1999.loc[54, "P(x+5)"]))) ** (1/5) 

    for i in range(50, 54):
        if tabla1999.loc[54, "P(x+5)"] == 1 or tabla1999.loc[49, "P(x+5)"] == 1:
            tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
        else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1 , "S(x)"] / tabla1999.loc[49, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1999.loc[54, "P(x+5)"] == 1:
        tabla1999.loc[54, "S(x)"] = tabla1999.loc[53, "S(x)"] * tabla1999.loc[54, "P(x+5)"]
    else: tabla1999.loc[54, "S(x)"] = tabla1999.loc[49, "S(x)"] * tabla1999.loc[54, "P(x+5)"]

    if tabla1999.loc[59, "P(x+5)"] == 1:
        tabla1999.loc[54, "FACTOR ANUAL"] = 1
    else: tabla1999.loc[54, "FACTOR ANUAL"] = (tabla1999.loc[54, "S(x)"] / ((tabla1999.loc[54, "S(x)"] * tabla1999.loc[59, "P(x+5)"]))) ** (1/5) 

    for i in range(55, 59):
        if tabla1999.loc[59, "P(x+5)"] == 1 or tabla1999.loc[54, "P(x+5)"] == 1:
            tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
        else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1 , "S(x)"] / tabla1999.loc[54, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla1999.loc[59, "P(x+5)"] == 1:
        tabla1999.loc[59, "S(x)"] = tabla1999.loc[58, "S(x)"] * tabla1999.loc[59, "P(x+5)"]
    else: tabla1999.loc[59, "S(x)"] = tabla1999.loc[54, "S(x)"] * tabla1999.loc[59, "P(x+5)"]

    for i in range(59, 61):
        if i not in [59]:
            if tabla1999.loc[i-1, "P(x+5)"] == 1:
                tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]
            else: tabla1999.loc[i, "S(x)"] = tabla1999.loc[i-1, "S(x)"] * tabla1999.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla2000 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2000] = tabla2000

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2000.loc[3, "P(x+5)"] = GENERACION_2000.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2000
    tabla2000.loc[4: 7, "P(x+5)"] = tabla2000.loc[3, "P(x+5)"]
    tabla2000.loc[8, "P(x+5)"] = GENERACION_2000.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2000.loc[9: 12, "P(x+5)"] = tabla2000.loc[8, "P(x+5)"]
    tabla2000.loc[13, "P(x+5)"] = GENERACION_2000.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2000.loc[14: 17, "P(x+5)"] = tabla2000.loc[13, "P(x+5)"]
    tabla2000.loc[18, "P(x+5)"] = GENERACION_2000.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla2000.loc[23, "P(x+5)"] = GENERACION_2000.loc[3, "PROBABILIDAD QUINQUENAL"]
        
    for i in [28, 33, 38, 43, 48, 53, 58]:
        if tabla2000.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2000 <= 1:
            tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2000
        else:
            tabla2000.loc[i, "P(x+5)"] = 1

    for i in range(18, 24):
        if i not in [18, 23]:
            if (tabla2000.loc[18, "P(x+5)"] == 1 or tabla2000.loc[23, "P(x+5)"] == 1):
                if tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5)) >= 1:
                    tabla2000.loc[i, "P(x+5)"] = 1
                else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5))
            else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"]

    for i in range(23, 29):
        if i not in [23, 28]:
            if (tabla2000.loc[23, "P(x+5)"] == 1 or tabla2000.loc[28, "P(x+5)"] == 1):
                if tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5)) >= 1:
                    tabla2000.loc[i, "P(x+5)"] = 1
                else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5))
            else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] 
            
    for i in range(28, 34):
        if i not in [28, 33]:
            if (tabla2000.loc[28, "P(x+5)"] == 1 or tabla2000.loc[33, "P(x+5)"] == 1):
                if tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5)) >= 1:
                    tabla2000.loc[i, "P(x+5)"] = 1
                else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5))
            else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"]       

    for i in range(33, 39):
        if i not in [33, 38]:
            if (tabla2000.loc[33, "P(x+5)"] == 1 or tabla2000.loc[38, "P(x+5)"] == 1):
                if tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5)) >= 1:
                    tabla2000.loc[i, "P(x+5)"] = 1
                else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5))
            else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] 
            
    for i in range(38, 44):
        if i not in [38, 43]:
            if (tabla2000.loc[38, "P(x+5)"] == 1 or tabla2000.loc[43, "P(x+5)"] == 1):
                if tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5)) >= 1:
                    tabla2000.loc[i, "P(x+5)"] = 1
                else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5))
            else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"]  

    for i in range(43, 49):
        if i not in [43, 48]:
            if (tabla2000.loc[43, "P(x+5)"] == 1 or tabla2000.loc[48, "P(x+5)"] == 1):
                if tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5)) >= 1:
                    tabla2000.loc[i, "P(x+5)"] = 1
                else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5))
            else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"]  

    for i in range(48, 54):
        if i not in [48, 53]:
            if (tabla2000.loc[48, "P(x+5)"] == 1 or tabla2000.loc[53, "P(x+5)"] == 1):
                if tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5)) >= 1:
                    tabla2000.loc[i, "P(x+5)"] = 1
                else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5))
            else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"]  
            
    for i in range(53, 59):
        if i not in [53, 58]:
            if (tabla2000.loc[53, "P(x+5)"] == 1 or tabla2000.loc[58, "P(x+5)"] == 1):
                if tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5)) >= 1:
                    tabla2000.loc[i, "P(x+5)"] = 1
                else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5))
            else: tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"]

    for i in range(59, 61):
        if tabla2000.loc[i-1, "P(x+5)"] == 1:
            tabla2000.loc[i, "P(x+5)"] = 1
        if tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5)) < 1:
            tabla2000.loc[i, "P(x+5)"] = tabla2000.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2000 ** (1/5))
        else: tabla2000.loc[i, "P(x+5)"] = 1

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2000.loc[0, "S(x)"] = 100000
    tabla2000.loc[3, "S(x)"] = tabla2000.loc[0, "S(x)"] * tabla2000.loc[3, "P(x+5)"]

    for i in [8, 13, 18]:
        tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-5, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        
    tabla2000.loc[0, "FACTOR ANUAL"] = (tabla2000.loc[0, "S(x)"] / tabla2000.loc[3, "S(x)"]) ** (1/3)

    for i in [3, 8, 13]:
        tabla2000.loc[i, "FACTOR ANUAL"] = (tabla2000.loc[i, "S(x)"] / tabla2000.loc[i+5, "S(x)"]) ** (1/5)

    for i in range(1, 18):
        if i not in [3, 8, 13]:
            tabla2000.loc[i, "FACTOR ANUAL"] = tabla2000.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 18):
        if i not in [3, 8, 13]:
            if tabla2000.loc[i, "FACTOR ANUAL"] == 1:
                tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] / tabla2000.loc[i, "FACTOR ANUAL"]
            else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] / tabla2000.loc[i, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 18        
    if tabla2000.loc[18, "P(x+5)"] == 1:
        tabla2000.loc[18, "S(x)"] = tabla2000.loc[17, "S(x)"] * tabla2000.loc[18, "P(x+5)"]
    else: tabla2000.loc[18, "S(x)"] = tabla2000.loc[13, "S(x)"] * tabla2000.loc[18, "P(x+5)"]

    if tabla2000.loc[23, "P(x+5)"] == 1:
        tabla2000.loc[18, "FACTOR ANUAL"] = 1
    else: tabla2000.loc[18, "FACTOR ANUAL"] = (tabla2000.loc[18, "S(x)"] / ((tabla2000.loc[18, "S(x)"] * tabla2000.loc[23, "P(x+5)"]))) ** (1/5)
    
    for i in range(19, 23):
        if tabla2000.loc[23, "P(x+5)"] == 1:
            tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1 , "S(x)"] / tabla2000.loc[18, "FACTOR ANUAL"]
        
            #-----------------------------------------------------------------INTERVALO 23        
    if tabla2000.loc[23, "P(x+5)"] == 1:
        tabla2000.loc[23, "S(x)"] = tabla2000.loc[22, "S(x)"] * tabla2000.loc[23, "P(x+5)"]
    else: tabla2000.loc[23, "S(x)"] = tabla2000.loc[18, "S(x)"] * tabla2000.loc[23, "P(x+5)"]

    if tabla2000.loc[28, "P(x+5)"] == 1:
        tabla2000.loc[23, "FACTOR ANUAL"] = 1
    else: tabla2000.loc[23, "FACTOR ANUAL"] = (tabla2000.loc[23, "S(x)"] / ((tabla2000.loc[23, "S(x)"] * tabla2000.loc[28, "P(x+5)"]))) ** (1/5)
    
    for i in range(24, 28):
        if tabla2000.loc[28, "P(x+5)"] == 1:
            tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1 , "S(x)"] / tabla2000.loc[23, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 28
    if tabla2000.loc[28, "P(x+5)"] == 1:
        tabla2000.loc[28, "S(x)"] = tabla2000.loc[27, "S(x)"] * tabla2000.loc[28, "P(x+5)"]
    else: tabla2000.loc[28, "S(x)"] = tabla2000.loc[23, "S(x)"] * tabla2000.loc[28, "P(x+5)"]

    if tabla2000.loc[33, "P(x+5)"] == 1:
        tabla2000.loc[28, "FACTOR ANUAL"] = 1
    else: tabla2000.loc[28, "FACTOR ANUAL"] = (tabla2000.loc[28, "S(x)"] / ((tabla2000.loc[28, "S(x)"] * tabla2000.loc[33, "P(x+5)"]))) ** (1/5)
    
    for i in range(29, 33):
        if tabla2000.loc[33, "P(x+5)"] == 1 or tabla2000.loc[28, "P(x+5)"] == 1:
            tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1 , "S(x)"] / tabla2000.loc[28, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 33
    if tabla2000.loc[33, "P(x+5)"] == 1:
        tabla2000.loc[33, "S(x)"] = tabla2000.loc[32, "S(x)"] * tabla2000.loc[33, "P(x+5)"]
    else: tabla2000.loc[33, "S(x)"] = tabla2000.loc[28, "S(x)"] * tabla2000.loc[33, "P(x+5)"]
    
    if tabla2000.loc[38, "P(x+5)"] == 1:
        tabla2000.loc[33, "FACTOR ANUAL"] = 1
    else: tabla2000.loc[33, "FACTOR ANUAL"] = (tabla2000.loc[33, "S(x)"] / ((tabla2000.loc[33, "S(x)"] * tabla2000.loc[38, "P(x+5)"]))) ** (1/5)    

    for i in range(34, 38):
        if tabla2000.loc[33, "P(x+5)"] == 1 or tabla2000.loc[38, "P(x+5)"] == 1:
            tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1 , "S(x)"] / tabla2000.loc[33, "FACTOR ANUAL"]
        
            #-----------------------------------------------------------------INTERVALO 38
    if tabla2000.loc[38, "P(x+5)"] == 1:
        tabla2000.loc[38, "S(x)"] = tabla2000.loc[37, "S(x)"] * tabla2000.loc[38, "P(x+5)"]
    else: tabla2000.loc[38, "S(x)"] = tabla2000.loc[33, "S(x)"] * tabla2000.loc[38, "P(x+5)"]

    #i+5   
    if tabla2000.loc[43, "P(x+5)"] == 1:
        tabla2000.loc[38, "FACTOR ANUAL"] = 1
    else: tabla2000.loc[38, "FACTOR ANUAL"] = (tabla2000.loc[38, "S(x)"] / ((tabla2000.loc[38, "S(x)"] * tabla2000.loc[43, "P(x+5)"]))) ** (1/5)    

    for i in range(39, 43):
        if tabla2000.loc[43, "P(x+5)"] == 1 or tabla2000.loc[38, "P(x+5)"] == 1:
            tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1 , "S(x)"] / tabla2000.loc[38, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 43
    if tabla2000.loc[43, "P(x+5)"] == 1:
        tabla2000.loc[43, "S(x)"] = tabla2000.loc[42, "S(x)"] * tabla2000.loc[43, "P(x+5)"]
    else: tabla2000.loc[43, "S(x)"] = tabla2000.loc[38, "S(x)"] * tabla2000.loc[43, "P(x+5)"]

    #i+5   
    if tabla2000.loc[48, "P(x+5)"] == 1:
        tabla2000.loc[43, "FACTOR ANUAL"] = 1
    else: tabla2000.loc[43, "FACTOR ANUAL"] = (tabla2000.loc[43, "S(x)"] / ((tabla2000.loc[43, "S(x)"] * tabla2000.loc[48, "P(x+5)"]))) ** (1/5)    

    for i in range(44, 48):
        if tabla2000.loc[48, "P(x+5)"] == 1 or tabla2000.loc[43, "P(x+5)"] == 1:
            tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1 , "S(x)"] / tabla2000.loc[43, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 48
    if tabla2000.loc[48, "P(x+5)"] == 1:
        tabla2000.loc[48, "S(x)"] = tabla2000.loc[47, "S(x)"] * tabla2000.loc[48, "P(x+5)"]
    else: tabla2000.loc[48, "S(x)"] = tabla2000.loc[43, "S(x)"] * tabla2000.loc[48, "P(x+5)"]

    #i+5   
    if tabla2000.loc[53, "P(x+5)"] == 1:
        tabla2000.loc[48, "FACTOR ANUAL"] = 1
    else: tabla2000.loc[48, "FACTOR ANUAL"] = (tabla2000.loc[48, "S(x)"] / ((tabla2000.loc[48, "S(x)"] * tabla2000.loc[53, "P(x+5)"]))) ** (1/5)    

    for i in range(49, 53):
        if tabla2000.loc[53, "P(x+5)"] == 1 or tabla2000.loc[48, "P(x+5)"] == 1:
            tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1 , "S(x)"] / tabla2000.loc[48, "FACTOR ANUAL"]
            
            #-----------------------------------------------------------------INTERVALO 53
    if tabla2000.loc[53, "P(x+5)"] == 1:
        tabla2000.loc[53, "S(x)"] = tabla2000.loc[52, "S(x)"] * tabla2000.loc[53, "P(x+5)"]
    else: tabla2000.loc[53, "S(x)"] = tabla2000.loc[48, "S(x)"] * tabla2000.loc[53, "P(x+5)"]

    #i+5   
    if tabla2000.loc[58, "P(x+5)"] == 1:
        tabla2000.loc[53, "FACTOR ANUAL"] = 1
    else: tabla2000.loc[53, "FACTOR ANUAL"] = (tabla2000.loc[53, "S(x)"] / ((tabla2000.loc[53, "S(x)"] * tabla2000.loc[58, "P(x+5)"]))) ** (1/5)    

    for i in range(54, 58):
        if tabla2000.loc[58, "P(x+5)"] == 1 or tabla2000.loc[53, "P(x+5)"] == 1:
            tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1 , "S(x)"] / tabla2000.loc[53, "FACTOR ANUAL"]    

            #-----------------------------------------------------------------INTERVALO 58
    if tabla2000.loc[58, "P(x+5)"] == 1:
        tabla2000.loc[58, "S(x)"] = tabla2000.loc[57, "S(x)"] * tabla2000.loc[58, "P(x+5)"]
    else: tabla2000.loc[58, "S(x)"] = tabla2000.loc[53, "S(x)"] * tabla2000.loc[58, "P(x+5)"]

    for i in range(59, 61):
        if tabla2000.loc[i-1, "P(x+5)"] == 1:
            tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]
        else: tabla2000.loc[i, "S(x)"] = tabla2000.loc[i-1, "S(x)"] * tabla2000.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla2001 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2001] = tabla2001

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2001.loc[2, "P(x+5)"] = GENERACION_2001.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2001
    tabla2001.loc[3: 6, "P(x+5)"] = tabla2001.loc[2, "P(x+5)"]
    tabla2001.loc[7, "P(x+5)"] = GENERACION_2001.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2001.loc[8: 11, "P(x+5)"] = tabla2001.loc[7, "P(x+5)"]
    tabla2001.loc[12, "P(x+5)"] = GENERACION_2001.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2001.loc[13: 16, "P(x+5)"] = tabla2001.loc[12, "P(x+5)"]
    tabla2001.loc[17, "P(x+5)"] = GENERACION_2001.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla2001.loc[22, "P(x+5)"] = GENERACION_2001.loc[3, "PROBABILIDAD QUINQUENAL"]
        
    for i in [27, 32, 37, 42, 47, 52, 57]:
        if tabla2001.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2001 <= 1:
            tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2001
        else:
            tabla2001.loc[i, "P(x+5)"] = 1

    for i in range(17, 23):
        if i not in [17, 22]:
            if (tabla2001.loc[17, "P(x+5)"] == 1 or tabla2001.loc[22, "P(x+5)"] == 1):
                if tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5)) >= 1:
                    tabla2001.loc[i, "P(x+5)"] = 1
                else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5))
            else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"]

    for i in range(22, 28):
        if i not in [22, 27]:
            if (tabla2001.loc[22, "P(x+5)"] == 1 or tabla2001.loc[27, "P(x+5)"] == 1):
                if tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5)) >= 1:
                    tabla2001.loc[i, "P(x+5)"] = 1
                else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5))
            else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"]
            
    for i in range(27, 33):
        if i not in [27, 32]:
            if (tabla2001.loc[27, "P(x+5)"] == 1 or tabla2001.loc[32, "P(x+5)"] == 1):
                if tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5)) >= 1:
                    tabla2001.loc[i, "P(x+5)"] = 1
                else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5))
            else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"]       

    for i in range(32, 38):
        if i not in [32, 37]:
            if (tabla2001.loc[32, "P(x+5)"] == 1 or tabla2001.loc[37, "P(x+5)"] == 1):
                if tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5)) >= 1:
                    tabla2001.loc[i, "P(x+5)"] = 1
                else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5))
            else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] 
            
    for i in range(37, 43):
        if i not in [37, 42]:
            if (tabla2001.loc[37, "P(x+5)"] == 1 or tabla2001.loc[42, "P(x+5)"] == 1):
                if tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5)) >= 1:
                    tabla2001.loc[i, "P(x+5)"] = 1
                else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5))
            else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"]  

    for i in range(42, 48):
        if i not in [42, 47]:
            if (tabla2001.loc[42, "P(x+5)"] == 1 or tabla2001.loc[47, "P(x+5)"] == 1):
                if tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5)) >= 1:
                    tabla2001.loc[i, "P(x+5)"] = 1
                else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5))
            else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"]  

    for i in range(47, 53):
        if i not in [47, 52]:
            if (tabla2001.loc[47, "P(x+5)"] == 1 or tabla2001.loc[52, "P(x+5)"] == 1):
                if tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5)) >= 1:
                    tabla2001.loc[i, "P(x+5)"] = 1
                else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5))
            else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"]  
            
    for i in range(52, 58):
        if i not in [52, 57]:
            if (tabla2001.loc[52, "P(x+5)"] == 1 or tabla2001.loc[57, "P(x+5)"] == 1):
                if tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5)) >= 1:
                    tabla2001.loc[i, "P(x+5)"] = 1
                else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5))
            else: tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"]

    for i in range(58, 61):
        if tabla2001.loc[i-1, "P(x+5)"] == 1:
            tabla2001.loc[i, "P(x+5)"] = 1
        if tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5)) < 1:
            tabla2001.loc[i, "P(x+5)"] = tabla2001.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2001 ** (1/5))
        else: tabla2001.loc[i, "P(x+5)"] = 1  

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2001.loc[0, "S(x)"] = 100000
    tabla2001.loc[2, "S(x)"] = tabla2001.loc[0, "S(x)"] * tabla2001.loc[2, "P(x+5)"]

    for i in [7, 12, 17]:
        tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-5, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        
    tabla2001.loc[0, "FACTOR ANUAL"] = (tabla2001.loc[0, "S(x)"] / tabla2001.loc[2, "S(x)"]) ** (1/2)

    for i in [2, 7, 12]:
        tabla2001.loc[i, "FACTOR ANUAL"] = (tabla2001.loc[i, "S(x)"] / tabla2001.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 17):
        if i not in [2, 7, 12]:
            tabla2001.loc[i, "FACTOR ANUAL"] = tabla2001.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 17):
        if i not in [2, 7, 12]:
            if tabla2001.loc[i, "FACTOR ANUAL"] == 1:
                tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] / tabla2001.loc[i, "FACTOR ANUAL"]
            else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] / tabla2001.loc[i, "FACTOR ANUAL"]
            
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2001.loc[17, "P(x+5)"] == 1:
        tabla2001.loc[17, "S(x)"] = tabla2001.loc[16, "S(x)"] * tabla2001.loc[17, "P(x+5)"]
    else: tabla2001.loc[17, "S(x)"] = tabla2001.loc[12, "S(x)"] * tabla2001.loc[17, "P(x+5)"]
    
    if tabla2001.loc[22, "P(x+5)"] == 1:
        tabla2001.loc[17, "FACTOR ANUAL"] = 1
    else: tabla2001.loc[17, "FACTOR ANUAL"] = (tabla2001.loc[17, "S(x)"] / ((tabla2001.loc[17, "S(x)"] * tabla2001.loc[22, "P(x+5)"]))) ** (1/5)    

    for i in range(18, 22):
        if tabla2001.loc[22, "P(x+5)"] == 1:
            tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1 , "S(x)"] / tabla2001.loc[17, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2001.loc[22, "P(x+5)"] == 1:
        tabla2001.loc[22, "S(x)"] = tabla2001.loc[21, "S(x)"] * tabla2001.loc[22, "P(x+5)"]
    else: tabla2001.loc[22, "S(x)"] = tabla2001.loc[17, "S(x)"] * tabla2001.loc[22, "P(x+5)"]
    
    if tabla2001.loc[27, "P(x+5)"] == 1:
        tabla2001.loc[22, "FACTOR ANUAL"] = 1
    else: tabla2001.loc[22, "FACTOR ANUAL"] = (tabla2001.loc[22, "S(x)"] / ((tabla2001.loc[22, "S(x)"] * tabla2001.loc[27, "P(x+5)"]))) ** (1/5)    

    for i in range(23, 27):
        if tabla2001.loc[27, "P(x+5)"] == 1:
            tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1 , "S(x)"] / tabla2001.loc[22, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2001.loc[27, "P(x+5)"] == 1:
        tabla2001.loc[27, "S(x)"] = tabla2001.loc[26, "S(x)"] * tabla2001.loc[27, "P(x+5)"]
    else: tabla2001.loc[27, "S(x)"] = tabla2001.loc[22, "S(x)"] * tabla2001.loc[27, "P(x+5)"]
    
    if tabla2001.loc[32, "P(x+5)"] == 1:
        tabla2001.loc[27, "FACTOR ANUAL"] = 1
    else: tabla2001.loc[27, "FACTOR ANUAL"] = (tabla2001.loc[27, "S(x)"] / ((tabla2001.loc[27, "S(x)"] * tabla2001.loc[32, "P(x+5)"]))) ** (1/5)    

    for i in range(28, 32):
        if tabla2001.loc[32, "P(x+5)"] == 1 or tabla2001.loc[27, "P(x+5)"] == 1:
            tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1 , "S(x)"] / tabla2001.loc[27, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2001.loc[32, "P(x+5)"] == 1:
        tabla2001.loc[32, "S(x)"] = tabla2001.loc[31, "S(x)"] * tabla2001.loc[32, "P(x+5)"]
    else: tabla2001.loc[32, "S(x)"] = tabla2001.loc[27, "S(x)"] * tabla2001.loc[32, "P(x+5)"]
    
    if tabla2001.loc[37, "P(x+5)"] == 1:
        tabla2001.loc[32, "FACTOR ANUAL"] = 1
    else: tabla2001.loc[32, "FACTOR ANUAL"] = (tabla2001.loc[32, "S(x)"] / ((tabla2001.loc[32, "S(x)"] * tabla2001.loc[37, "P(x+5)"]))) ** (1/5)    

    for i in range(33, 37):
        if tabla2001.loc[37, "P(x+5)"] == 1 or tabla2001.loc[32, "P(x+5)"] == 1:
            tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1 , "S(x)"] / tabla2001.loc[32, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2001.loc[37, "P(x+5)"] == 1:
        tabla2001.loc[37, "S(x)"] = tabla2001.loc[36, "S(x)"] * tabla2001.loc[37, "P(x+5)"]
    else: tabla2001.loc[37, "S(x)"] = tabla2001.loc[32, "S(x)"] * tabla2001.loc[37, "P(x+5)"]

    #i+5   
    if tabla2001.loc[42, "P(x+5)"] == 1:
        tabla2001.loc[37, "FACTOR ANUAL"] = 1
    else: tabla2001.loc[37, "FACTOR ANUAL"] = (tabla2001.loc[37, "S(x)"] / ((tabla2001.loc[37, "S(x)"] * tabla2001.loc[42, "P(x+5)"]))) ** (1/5)    

    for i in range(38, 42):
        if tabla2001.loc[42, "P(x+5)"] == 1 or tabla2001.loc[37, "P(x+5)"] == 1:
            tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1 , "S(x)"] / tabla2001.loc[37, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2001.loc[42, "P(x+5)"] == 1:
        tabla2001.loc[42, "S(x)"] = tabla2001.loc[41, "S(x)"] * tabla2001.loc[42, "P(x+5)"]
    else: tabla2001.loc[42, "S(x)"] = tabla2001.loc[37, "S(x)"] * tabla2001.loc[42, "P(x+5)"]
    
    if tabla2001.loc[47, "P(x+5)"] == 1:
        tabla2001.loc[42, "FACTOR ANUAL"] = 1
    else: tabla2001.loc[42, "FACTOR ANUAL"] = (tabla2001.loc[42, "S(x)"] / ((tabla2001.loc[42, "S(x)"] * tabla2001.loc[47, "P(x+5)"]))) ** (1/5)    

    for i in range(43, 47):
        if tabla2001.loc[47, "P(x+5)"] == 1 or tabla2001.loc[42, "P(x+5)"] == 1:
            tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1 , "S(x)"] / tabla2001.loc[42, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2001.loc[47, "P(x+5)"] == 1:
        tabla2001.loc[47, "S(x)"] = tabla2001.loc[46, "S(x)"] * tabla2001.loc[47, "P(x+5)"]
    else: tabla2001.loc[47, "S(x)"] = tabla2001.loc[42, "S(x)"] * tabla2001.loc[47, "P(x+5)"]

    if tabla2001.loc[52, "P(x+5)"] == 1:
        tabla2001.loc[47, "FACTOR ANUAL"] = 1
    else: tabla2001.loc[47, "FACTOR ANUAL"] = (tabla2001.loc[47, "S(x)"] / ((tabla2001.loc[47, "S(x)"] * tabla2001.loc[52, "P(x+5)"]))) ** (1/5) 

    for i in range(48, 52):
        if tabla2001.loc[52, "P(x+5)"] == 1 or tabla2001.loc[47, "P(x+5)"] == 1:
            tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1 , "S(x)"] / tabla2001.loc[47, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2001.loc[52, "P(x+5)"] == 1:
        tabla2001.loc[52, "S(x)"] = tabla2001.loc[51, "S(x)"] * tabla2001.loc[52, "P(x+5)"]
    else: tabla2001.loc[52, "S(x)"] = tabla2001.loc[47, "S(x)"] * tabla2001.loc[52, "P(x+5)"]

    if tabla2001.loc[57, "P(x+5)"] == 1:
        tabla2001.loc[52, "FACTOR ANUAL"] = 1
    else: tabla2001.loc[52, "FACTOR ANUAL"] = (tabla2001.loc[52, "S(x)"] / ((tabla2001.loc[52, "S(x)"] * tabla2001.loc[57, "P(x+5)"]))) ** (1/5) 

    for i in range(53, 57):
        if tabla2001.loc[57, "P(x+5)"] == 1 or tabla2001.loc[52, "P(x+5)"] == 1:
            tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1 , "S(x)"] / tabla2001.loc[52, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2001.loc[57, "P(x+5)"] == 1:
        tabla2001.loc[57, "S(x)"] = tabla2001.loc[56, "S(x)"] * tabla2001.loc[57, "P(x+5)"]
    else: tabla2001.loc[57, "S(x)"] = tabla2001.loc[52, "S(x)"] * tabla2001.loc[57, "P(x+5)"]

    for i in range(58, 61):
        if tabla2001.loc[i-1, "P(x+5)"] == 1:
            tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]
        else: tabla2001.loc[i, "S(x)"] = tabla2001.loc[i-1, "S(x)"] * tabla2001.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla2002 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2002] = tabla2002

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2002.loc[1, "P(x+5)"] = GENERACION_2002.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2002
    tabla2002.loc[2: 5, "P(x+5)"] = tabla2002.loc[1, "P(x+5)"]
    tabla2002.loc[6, "P(x+5)"] = GENERACION_2002.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2002.loc[7: 10, "P(x+5)"] = tabla2002.loc[6, "P(x+5)"]
    tabla2002.loc[11, "P(x+5)"] = GENERACION_2002.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2002.loc[12: 15, "P(x+5)"] = tabla2002.loc[11, "P(x+5)"]
    tabla2002.loc[16, "P(x+5)"] = GENERACION_2002.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla2002.loc[21, "P(x+5)"] = GENERACION_2002.loc[3, "PROBABILIDAD QUINQUENAL"]

    for i in [26, 31, 36, 41, 46, 51, 56]:
        if tabla2002.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2002 <= 1:
            tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2002
        else:
            tabla2002.loc[i, "P(x+5)"] = 1

    for i in range(16, 22):
        if i not in [16, 21]:
            if (tabla2002.loc[16, "P(x+5)"] == 1 or tabla2002.loc[21, "P(x+5)"] == 1):
                if tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5)) >= 1:
                    tabla2002.loc[i, "P(x+5)"] = 1
                else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5))
            else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] 

    for i in range(21, 27):
        if i not in [21, 26]:
            if (tabla2002.loc[21, "P(x+5)"] == 1 or tabla2002.loc[26, "P(x+5)"] == 1):
                if tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5)) >= 1:
                    tabla2002.loc[i, "P(x+5)"] = 1
                else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5))
            else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] 

    for i in range(26, 32):
        if i not in [26, 31]:
            if (tabla2002.loc[26, "P(x+5)"] == 1 or tabla2002.loc[31, "P(x+5)"] == 1):
                if tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5)) >= 1:
                    tabla2002.loc[i, "P(x+5)"] = 1
                else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5))
            else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] 

    for i in range(31, 37):
        if i not in [31, 36]:
            if (tabla2002.loc[31, "P(x+5)"] == 1 or tabla2002.loc[36, "P(x+5)"] == 1):
                if tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5)) >= 1:
                    tabla2002.loc[i, "P(x+5)"] = 1
                else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5))
            else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] 

    for i in range(36, 42):
        if i not in [36, 41]:
            if (tabla2002.loc[36, "P(x+5)"] == 1 or tabla2002.loc[41, "P(x+5)"] == 1):
                if tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5)) >= 1:
                    tabla2002.loc[i, "P(x+5)"] = 1
                else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5))
            else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] 

    for i in range(41, 47):
        if i not in [41, 46]:
            if (tabla2002.loc[41, "P(x+5)"] == 1 or tabla2002.loc[46, "P(x+5)"] == 1):
                if tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5)) >= 1:
                    tabla2002.loc[i, "P(x+5)"] = 1
                else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5))
            else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"]  

    for i in range(46, 52):
        if i not in [46, 51]:
            if (tabla2002.loc[46, "P(x+5)"] == 1 or tabla2002.loc[51, "P(x+5)"] == 1):
                if tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5)) >= 1:
                    tabla2002.loc[i, "P(x+5)"] = 1
                else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5))
            else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"]  
            
    for i in range(51, 57):
        if i not in [51, 56]:
            if (tabla2002.loc[51, "P(x+5)"] == 1 or tabla2002.loc[56, "P(x+5)"] == 1):
                if tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5)) >= 1:
                    tabla2002.loc[i, "P(x+5)"] = 1
                else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5))
            else: tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"]

    for i in range(57, 61):
        if tabla2002.loc[i-1, "P(x+5)"] == 1:
            tabla2002.loc[i, "P(x+5)"] = 1
        if tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5)) < 1:
            tabla2002.loc[i, "P(x+5)"] = tabla2002.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2002 ** (1/5))
        else: tabla2002.loc[i, "P(x+5)"] = 1  
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2002.loc[0, "S(x)"] = 100000
    tabla2002.loc[1, "S(x)"] = tabla2002.loc[0, "S(x)"] * tabla2002.loc[1, "P(x+5)"]

    for i in [6, 11, 16]:
        tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-5, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        
    #tabla2002.loc[0, "FACTOR ANUAL"] = (tabla2002.loc[0, "S(x)"] / tabla2002.loc[1, "S(x)"]) ** (1/5)

    for i in [1, 6, 11]:
        tabla2002.loc[i, "FACTOR ANUAL"] = (tabla2002.loc[i, "S(x)"] / tabla2002.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 16):
        if i not in [1, 6, 11]:
            tabla2002.loc[i, "FACTOR ANUAL"] = tabla2002.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 16):
        if i not in [1, 6, 11]:
            if tabla2002.loc[i, "FACTOR ANUAL"] == 1:
                tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] / tabla2002.loc[i, "FACTOR ANUAL"]
            else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] / tabla2002.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2002.loc[16, "P(x+5)"] == 1:
        tabla2002.loc[16, "S(x)"] = tabla2002.loc[15, "S(x)"] * tabla2002.loc[16, "P(x+5)"]
    else: tabla2002.loc[16, "S(x)"] = tabla2002.loc[11, "S(x)"] * tabla2002.loc[16, "P(x+5)"]
    
    if tabla2002.loc[21, "P(x+5)"] == 1:
        tabla2002.loc[16, "FACTOR ANUAL"] = 1
    else: tabla2002.loc[16, "FACTOR ANUAL"] = (tabla2002.loc[16, "S(x)"] / ((tabla2002.loc[16, "S(x)"] * tabla2002.loc[21, "P(x+5)"]))) ** (1/5)    

    for i in range(17, 21):
        if tabla2002.loc[21, "P(x+5)"] == 1:
            tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1 , "S(x)"] / tabla2002.loc[16, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2002.loc[21, "P(x+5)"] == 1:
        tabla2002.loc[21, "S(x)"] = tabla2002.loc[20, "S(x)"] * tabla2002.loc[21, "P(x+5)"]
    else: tabla2002.loc[21, "S(x)"] = tabla2002.loc[16, "S(x)"] * tabla2002.loc[21, "P(x+5)"]
    
    if tabla2002.loc[26, "P(x+5)"] == 1:
        tabla2002.loc[21, "FACTOR ANUAL"] = 1
    else: tabla2002.loc[21, "FACTOR ANUAL"] = (tabla2002.loc[21, "S(x)"] / ((tabla2002.loc[21, "S(x)"] * tabla2002.loc[26, "P(x+5)"]))) ** (1/5)    

    for i in range(22, 26):
        if tabla2002.loc[26, "P(x+5)"] == 1:
            tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1 , "S(x)"] / tabla2002.loc[21, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2002.loc[26, "P(x+5)"] == 1:
        tabla2002.loc[26, "S(x)"] = tabla2002.loc[25, "S(x)"] * tabla2002.loc[26, "P(x+5)"]
    else: tabla2002.loc[26, "S(x)"] = tabla2002.loc[21, "S(x)"] * tabla2002.loc[26, "P(x+5)"]
    
    if tabla2002.loc[31, "P(x+5)"] == 1:
        tabla2002.loc[26, "FACTOR ANUAL"] = 1
    else: tabla2002.loc[26, "FACTOR ANUAL"] = (tabla2002.loc[26, "S(x)"] / ((tabla2002.loc[26, "S(x)"] * tabla2002.loc[31, "P(x+5)"]))) ** (1/5)    

    for i in range(27, 31):
        if tabla2002.loc[31, "P(x+5)"] == 1 or tabla2002.loc[26, "P(x+5)"] == 1:
            tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1 , "S(x)"] / tabla2002.loc[26, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2002.loc[31, "P(x+5)"] == 1:
        tabla2002.loc[31, "S(x)"] = tabla2002.loc[30, "S(x)"] * tabla2002.loc[31, "P(x+5)"]
    else: tabla2002.loc[31, "S(x)"] = tabla2002.loc[26, "S(x)"] * tabla2002.loc[31, "P(x+5)"]
    
    if tabla2002.loc[36, "P(x+5)"] == 1:
        tabla2002.loc[31, "FACTOR ANUAL"] = 1
    else: tabla2002.loc[31, "FACTOR ANUAL"] = (tabla2002.loc[31, "S(x)"] / ((tabla2002.loc[31, "S(x)"] * tabla2002.loc[36, "P(x+5)"]))) ** (1/5)    

    for i in range(32, 36):
        if tabla2002.loc[36, "P(x+5)"] == 1 or tabla2002.loc[31, "P(x+5)"] == 1:
            tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1 , "S(x)"] / tabla2002.loc[31, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2002.loc[36, "P(x+5)"] == 1:
        tabla2002.loc[36, "S(x)"] = tabla2002.loc[35, "S(x)"] * tabla2002.loc[36, "P(x+5)"]
    else: tabla2002.loc[36, "S(x)"] = tabla2002.loc[31, "S(x)"] * tabla2002.loc[36, "P(x+5)"]

    #i+5   
    if tabla2002.loc[41, "P(x+5)"] == 1:
        tabla2002.loc[36, "FACTOR ANUAL"] = 1
    else: tabla2002.loc[36, "FACTOR ANUAL"] = (tabla2002.loc[36, "S(x)"] / ((tabla2002.loc[36, "S(x)"] * tabla2002.loc[41, "P(x+5)"]))) ** (1/5)    

    for i in range(37, 41):
        if tabla2002.loc[41, "P(x+5)"] == 1 or tabla2002.loc[36, "P(x+5)"] == 1:
            tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1 , "S(x)"] / tabla2002.loc[36, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2002.loc[41, "P(x+5)"] == 1:
        tabla2002.loc[41, "S(x)"] = tabla2002.loc[40, "S(x)"] * tabla2002.loc[41, "P(x+5)"]
    else: tabla2002.loc[41, "S(x)"] = tabla2002.loc[36, "S(x)"] * tabla2002.loc[41, "P(x+5)"]
    
    if tabla2002.loc[46, "P(x+5)"] == 1:
        tabla2002.loc[41, "FACTOR ANUAL"] = 1
    else: tabla2002.loc[41, "FACTOR ANUAL"] = (tabla2002.loc[41, "S(x)"] / ((tabla2002.loc[41, "S(x)"] * tabla2002.loc[46, "P(x+5)"]))) ** (1/5)    

    for i in range(42, 46):
        if tabla2002.loc[46, "P(x+5)"] == 1 or tabla2002.loc[41, "P(x+5)"] == 1:
            tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1 , "S(x)"] / tabla2002.loc[41, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2002.loc[46, "P(x+5)"] == 1:
        tabla2002.loc[46, "S(x)"] = tabla2002.loc[45, "S(x)"] * tabla2002.loc[46, "P(x+5)"]
    else: tabla2002.loc[46, "S(x)"] = tabla2002.loc[41, "S(x)"] * tabla2002.loc[46, "P(x+5)"]

    if tabla2002.loc[51, "P(x+5)"] == 1:
        tabla2002.loc[46, "FACTOR ANUAL"] = 1
    else: tabla2002.loc[46, "FACTOR ANUAL"] = (tabla2002.loc[46, "S(x)"] / ((tabla2002.loc[46, "S(x)"] * tabla2002.loc[51, "P(x+5)"]))) ** (1/5) 

    for i in range(47, 51):
        if tabla2002.loc[46, "P(x+5)"] == 1 or tabla2002.loc[51, "P(x+5)"] == 1:
            tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1 , "S(x)"] / tabla2002.loc[46, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2002.loc[51, "P(x+5)"] == 1:
        tabla2002.loc[51, "S(x)"] = tabla2002.loc[50, "S(x)"] * tabla2002.loc[52, "P(x+5)"]
    else: tabla2002.loc[51, "S(x)"] = tabla2002.loc[46, "S(x)"] * tabla2002.loc[51, "P(x+5)"]

    if tabla2002.loc[56, "P(x+5)"] == 1:
        tabla2002.loc[51, "FACTOR ANUAL"] = 1
    else: tabla2002.loc[51, "FACTOR ANUAL"] = (tabla2002.loc[51, "S(x)"] / ((tabla2002.loc[51, "S(x)"] * tabla2002.loc[56, "P(x+5)"]))) ** (1/5) 

    for i in range(52, 56):
        if tabla2002.loc[56, "P(x+5)"] == 1 or tabla2002.loc[51, "P(x+5)"] == 1:
            tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1 , "S(x)"] / tabla2002.loc[51, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2002.loc[56, "P(x+5)"] == 1:
        tabla2002.loc[56, "S(x)"] = tabla2002.loc[55, "S(x)"] * tabla2002.loc[56, "P(x+5)"]
    else: tabla2002.loc[56, "S(x)"] = tabla2002.loc[51, "S(x)"] * tabla2002.loc[56, "P(x+5)"]

    for i in range(57, 61):
        if tabla2002.loc[i-1, "P(x+5)"] == 1:
            tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]
        else: tabla2002.loc[i, "S(x)"] = tabla2002.loc[i-1, "S(x)"] * tabla2002.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla2003 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2003] = tabla2003

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2003.loc[5, "P(x+5)"] = GENERACION_2003.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2003.loc[6: 9, "P(x+5)"] = tabla2003.loc[5, "P(x+5)"]
    tabla2003.loc[10, "P(x+5)"] = GENERACION_2003.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2003.loc[11: 14, "P(x+5)"] = tabla2003.loc[10, "P(x+5)"]
    tabla2003.loc[15, "P(x+5)"] = GENERACION_2003.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla2003.loc[16: 19, "P(x+5)"] = tabla2003.loc[15, "P(x+5)"]
    tabla2003.loc[20, "P(x+5)"] = GENERACION_2003.loc[3, "PROBABILIDAD QUINQUENAL"]
    tabla2003.loc[25, "P(x+5)"] = GENERACION_2003.loc[4, "PROBABILIDAD QUINQUENAL"]

    for i in [30, 35, 40, 45, 50, 55, 60]:
        if tabla2003.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2003 <= 1:
            tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2003
        else:
            tabla2003.loc[i, "P(x+5)"] = 1

    for i in range(20, 26):
        if i not in [20, 25]:
            if (tabla2003.loc[20, "P(x+5)"] == 1 or tabla2003.loc[25, "P(x+5)"] == 1):
                if tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5)) >= 1:
                    tabla2003.loc[i, "P(x+5)"] = 1
                else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5))
            else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"]

    for i in range(25, 31):
        if i not in [25, 30]:
            if (tabla2003.loc[25, "P(x+5)"] == 1 or tabla2003.loc[30, "P(x+5)"] == 1):
                if tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5)) >= 1:
                    tabla2003.loc[i, "P(x+5)"] = 1
                else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5))
            else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] 

    for i in range(30, 36):
        if i not in [30, 35]:
            if (tabla2003.loc[30, "P(x+5)"] == 1 or tabla2003.loc[35, "P(x+5)"] == 1):
                if tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5)) >= 1:
                    tabla2003.loc[i, "P(x+5)"] = 1
                else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5))
            else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] 

    for i in range(35, 41):
        if i not in [35, 40]:
            if (tabla2003.loc[35, "P(x+5)"] == 1 or tabla2003.loc[40, "P(x+5)"] == 1):
                if tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5)) >= 1:
                    tabla2003.loc[i, "P(x+5)"] = 1
                else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5))
            else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] 

    for i in range(40, 46):
        if i not in [40, 45]:
            if (tabla2003.loc[40, "P(x+5)"] == 1 or tabla2003.loc[45, "P(x+5)"] == 1):
                if tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5)) >= 1:
                    tabla2003.loc[i, "P(x+5)"] = 1
                else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5))
            else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] 

    for i in range(45, 51):
        if i not in [45, 50]:
            if (tabla2003.loc[45, "P(x+5)"] == 1 or tabla2003.loc[50, "P(x+5)"] == 1):
                if tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5)) >= 1:
                    tabla2003.loc[i, "P(x+5)"] = 1
                else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5))
            else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"]  

    for i in range(50, 56):
        if i not in [50, 55]:
            if (tabla2003.loc[50, "P(x+5)"] == 1 or tabla2003.loc[55, "P(x+5)"] == 1):
                if tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5)) >= 1:
                    tabla2003.loc[i, "P(x+5)"] = 1
                else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5))
            else: tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"]  
            
    for i in range(56, 61):
        if i not in [60]:
            if tabla2003.loc[i-1, "P(x+5)"] == 1:
                tabla2003.loc[i, "P(x+5)"] = 1
            if tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5)) < 1:
                tabla2003.loc[i, "P(x+5)"] = tabla2003.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2003 ** (1/5))
            else: tabla2003.loc[i, "P(x+5)"] = 1  
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2003.loc[0, "S(x)"] = 100000
    tabla2003.loc[5, "S(x)"] = tabla2003.loc[0, "S(x)"] * tabla2003.loc[5, "P(x+5)"]

    for i in [10, 15, 20]:
        tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-5, "S(x)"] * tabla2003.loc[i, "P(x+5)"]
        
    tabla2003.loc[0, "FACTOR ANUAL"] = (tabla2003.loc[0, "S(x)"] / tabla2003.loc[5, "S(x)"]) ** (1/5)

    for i in [5, 10, 15]:
        tabla2003.loc[i, "FACTOR ANUAL"] = (tabla2003.loc[i, "S(x)"] / tabla2003.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 20):
        if i not in [5, 10, 15]:
            tabla2003.loc[i, "FACTOR ANUAL"] = tabla2003.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 20):
        if i not in [5, 10, 15]:
            if tabla2003.loc[i, "FACTOR ANUAL"] == 1:
                tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] / tabla2003.loc[i, "FACTOR ANUAL"]
            else: tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] / tabla2003.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2003.loc[20, "P(x+5)"] == 1:
        tabla2003.loc[20, "S(x)"] = tabla2003.loc[19, "S(x)"] * tabla2003.loc[20, "P(x+5)"]
    else: tabla2003.loc[20, "S(x)"] = tabla2003.loc[15, "S(x)"] * tabla2003.loc[20, "P(x+5)"]
    
    if tabla2003.loc[25, "P(x+5)"] == 1:
        tabla2003.loc[20, "FACTOR ANUAL"] = 1
    else: tabla2003.loc[20, "FACTOR ANUAL"] = (tabla2003.loc[20, "S(x)"] / ((tabla2003.loc[20, "S(x)"] * tabla2003.loc[25, "P(x+5)"]))) ** (1/5)    

    for i in range(21, 25):
        if tabla2003.loc[25, "P(x+5)"] == 1:
            tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] * tabla2003.loc[i, "P(x+5)"]
        else: tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1 , "S(x)"] / tabla2003.loc[20, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2003.loc[25, "P(x+5)"] == 1:
        tabla2003.loc[25, "S(x)"] = tabla2003.loc[24, "S(x)"] * tabla2003.loc[25, "P(x+5)"]
    else: tabla2003.loc[25, "S(x)"] = tabla2003.loc[20, "S(x)"] * tabla2003.loc[25, "P(x+5)"]
    
    if tabla2003.loc[30, "P(x+5)"] == 1:
        tabla2003.loc[25, "FACTOR ANUAL"] = 1
    else: tabla2003.loc[25, "FACTOR ANUAL"] = (tabla2003.loc[25, "S(x)"] / ((tabla2003.loc[25, "S(x)"] * tabla2003.loc[30, "P(x+5)"]))) ** (1/5)    

    for i in range(26, 30):
        if tabla2003.loc[30, "P(x+5)"] == 1:
            tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] * tabla2003.loc[i, "P(x+5)"]
        else: tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1 , "S(x)"] / tabla2003.loc[25, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2003.loc[30, "P(x+5)"] == 1:
        tabla2003.loc[30, "S(x)"] = tabla2003.loc[29, "S(x)"] * tabla2003.loc[30, "P(x+5)"]
    else: tabla2003.loc[30, "S(x)"] = tabla2003.loc[25, "S(x)"] * tabla2003.loc[30, "P(x+5)"]
    
    if tabla2003.loc[35, "P(x+5)"] == 1:
        tabla2003.loc[30, "FACTOR ANUAL"] = 1
    else: tabla2003.loc[30, "FACTOR ANUAL"] = (tabla2003.loc[30, "S(x)"] / ((tabla2003.loc[30, "S(x)"] * tabla2003.loc[35, "P(x+5)"]))) ** (1/5)    

    for i in range(31, 35):
        if tabla2003.loc[35, "P(x+5)"] == 1 or tabla2003.loc[30, "P(x+5)"] == 1:
            tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] * tabla2003.loc[i, "P(x+5)"]
        else: tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1 , "S(x)"] / tabla2003.loc[30, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2003.loc[35, "P(x+5)"] == 1:
        tabla2003.loc[35, "S(x)"] = tabla2003.loc[34, "S(x)"] * tabla2003.loc[35, "P(x+5)"]
    else: tabla2003.loc[35, "S(x)"] = tabla2003.loc[30, "S(x)"] * tabla2003.loc[35, "P(x+5)"]
    
    if tabla2003.loc[40, "P(x+5)"] == 1:
        tabla2003.loc[35, "FACTOR ANUAL"] = 1
    else: tabla2003.loc[35, "FACTOR ANUAL"] = (tabla2003.loc[35, "S(x)"] / ((tabla2003.loc[35, "S(x)"] * tabla2003.loc[40, "P(x+5)"]))) ** (1/5)    

    for i in range(36, 40):
        if tabla2003.loc[40, "P(x+5)"] == 1 or tabla2003.loc[35, "P(x+5)"] == 1:
            tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] * tabla2003.loc[i, "P(x+5)"]
        else: tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1 , "S(x)"] / tabla2003.loc[35, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2003.loc[40, "P(x+5)"] == 1:
        tabla2003.loc[40, "S(x)"] = tabla2003.loc[39, "S(x)"] * tabla2003.loc[40, "P(x+5)"]
    else: tabla2003.loc[40, "S(x)"] = tabla2003.loc[35, "S(x)"] * tabla2003.loc[40, "P(x+5)"]

    #i+5   
    if tabla2003.loc[45, "P(x+5)"] == 1:
        tabla2003.loc[40, "FACTOR ANUAL"] = 1
    else: tabla2003.loc[40, "FACTOR ANUAL"] = (tabla2003.loc[40, "S(x)"] / ((tabla2003.loc[40, "S(x)"] * tabla2003.loc[45, "P(x+5)"]))) ** (1/5)    

    for i in range(41, 45):
        if tabla2003.loc[45, "P(x+5)"] == 1 or tabla2003.loc[40, "P(x+5)"] == 1:
            tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] * tabla2003.loc[i, "P(x+5)"]
        else: tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1 , "S(x)"] / tabla2003.loc[40, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2003.loc[45, "P(x+5)"] == 1:
        tabla2003.loc[45, "S(x)"] = tabla2003.loc[44, "S(x)"] * tabla2003.loc[45, "P(x+5)"]
    else: tabla2003.loc[45, "S(x)"] = tabla2003.loc[40, "S(x)"] * tabla2003.loc[45, "P(x+5)"]
    
    if tabla2003.loc[50, "P(x+5)"] == 1:
        tabla2003.loc[45, "FACTOR ANUAL"] = 1
    else: tabla2003.loc[45, "FACTOR ANUAL"] = (tabla2003.loc[45, "S(x)"] / ((tabla2003.loc[45, "S(x)"] * tabla2003.loc[50, "P(x+5)"]))) ** (1/5)    

    for i in range(46, 50):
        if tabla2003.loc[50, "P(x+5)"] == 1 or tabla2003.loc[45, "P(x+5)"] == 1:
            tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] * tabla2003.loc[i, "P(x+5)"]
        else: tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1 , "S(x)"] / tabla2003.loc[45, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2003.loc[50, "P(x+5)"] == 1:
        tabla2003.loc[50, "S(x)"] = tabla2003.loc[49, "S(x)"] * tabla2003.loc[50, "P(x+5)"]
    else: tabla2003.loc[50, "S(x)"] = tabla2003.loc[45, "S(x)"] * tabla2003.loc[50, "P(x+5)"]

    if tabla2003.loc[55, "P(x+5)"] == 1:
        tabla2003.loc[50, "FACTOR ANUAL"] = 1
    else: tabla2003.loc[50, "FACTOR ANUAL"] = (tabla2003.loc[50, "S(x)"] / ((tabla2003.loc[50, "S(x)"] * tabla2003.loc[55, "P(x+5)"]))) ** (1/5) 

    for i in range(51, 55):
        if tabla2003.loc[55, "P(x+5)"] == 1 or tabla2003.loc[50, "P(x+5)"] == 1:
            tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] * tabla2003.loc[i, "P(x+5)"]
        else: tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1 , "S(x)"] / tabla2003.loc[50, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    

    if tabla2003.loc[55, "P(x+5)"] == 1:
        tabla2003.loc[55, "S(x)"] = tabla2003.loc[54, "S(x)"] * tabla2003.loc[55, "P(x+5)"]
    else: tabla2003.loc[55, "S(x)"] = tabla2003.loc[50, "S(x)"] * tabla2003.loc[55, "P(x+5)"]

    if tabla2003.loc[60, "P(x+5)"] == 1:
        tabla2003.loc[55, "FACTOR ANUAL"] = 1
    else: tabla2003.loc[55, "FACTOR ANUAL"] = (tabla2003.loc[55, "S(x)"] / ((tabla2003.loc[55, "S(x)"] * tabla2003.loc[60, "P(x+5)"]))) ** (1/5) 

    for i in range(56, 60):
        if tabla2003.loc[60, "P(x+5)"] == 1 or tabla2003.loc[55, "P(x+5)"] == 1:
            tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1, "S(x)"] * tabla2003.loc[i, "P(x+5)"]
        else: tabla2003.loc[i, "S(x)"] = tabla2003.loc[i-1 , "S(x)"] / tabla2003.loc[55, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2003.loc[60, "P(x+5)"] == 1:
        tabla2003.loc[60, "S(x)"] = tabla2003.loc[60, "P(x+5)"] * tabla2003.loc[59, "S(x)"]
    else: tabla2003.loc[60, "S(x)"] = tabla2003.loc[60, "P(x+5)"] * tabla2003.loc[55, "S(x)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla2004 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2004] = tabla2004

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2004.loc[4, "P(x+5)"] = GENERACION_2004.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2004
    tabla2004.loc[5: 8, "P(x+5)"] = tabla2004.loc[4, "P(x+5)"]
    tabla2004.loc[9, "P(x+5)"] = GENERACION_2004.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2004.loc[10: 13, "P(x+5)"] = tabla2004.loc[9, "P(x+5)"]
    tabla2004.loc[14, "P(x+5)"] = GENERACION_2004.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2004.loc[19, "P(x+5)"] = GENERACION_2004.loc[2, "PROBABILIDAD QUINQUENAL"]

    for i in [24, 29, 34, 39, 44, 49, 54, 59]:
        if tabla2004.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2004 <= 1:
            tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2004
        else:
            tabla2004.loc[i, "P(x+5)"] = 1

    for i in range(14, 20):
        if i not in [14, 19]:
            if (tabla2004.loc[14, "P(x+5)"] == 1 or tabla2004.loc[19, "P(x+5)"] == 1):
                if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) >= 1:
                    tabla2004.loc[i, "P(x+5)"] = 1
                else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
            else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"]

    for i in range(19, 25):
        if i not in [19, 24]:
            if (tabla2004.loc[19, "P(x+5)"] == 1 or tabla2004.loc[24, "P(x+5)"] == 1):
                if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) >= 1:
                    tabla2004.loc[i, "P(x+5)"] = 1
                else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
            else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"]

    for i in range(24, 30):
        if i not in [24, 29]:
            if (tabla2004.loc[24, "P(x+5)"] == 1 or tabla2004.loc[29, "P(x+5)"] == 1):
                if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) >= 1:
                    tabla2004.loc[i, "P(x+5)"] = 1
                else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
            else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] 

    for i in range(29, 35):
        if i not in [29, 34]:
            if (tabla2004.loc[29, "P(x+5)"] == 1 or tabla2004.loc[34, "P(x+5)"] == 1):
                if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) >= 1:
                    tabla2004.loc[i, "P(x+5)"] = 1
                else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
            else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] 

    for i in range(34, 40):
        if i not in [34, 39]:
            if (tabla2004.loc[34, "P(x+5)"] == 1 or tabla2004.loc[39, "P(x+5)"] == 1):
                if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) >= 1:
                    tabla2004.loc[i, "P(x+5)"] = 1
                else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
            else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] 

    for i in range(39, 45):
        if i not in [39, 44]:
            if (tabla2004.loc[39, "P(x+5)"] == 1 or tabla2004.loc[44, "P(x+5)"] == 1):
                if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) >= 1:
                    tabla2004.loc[i, "P(x+5)"] = 1
                else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
            else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] 

    for i in range(44, 50):
        if i not in [44, 49]:
            if (tabla2004.loc[44, "P(x+5)"] == 1 or tabla2004.loc[49, "P(x+5)"] == 1):
                if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) >= 1:
                    tabla2004.loc[i, "P(x+5)"] = 1
                else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
            else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"]  

    for i in range(49, 55):
        if i not in [49, 54]:
            if (tabla2004.loc[49, "P(x+5)"] == 1 or tabla2004.loc[54, "P(x+5)"] == 1):
                if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) >= 1:
                    tabla2004.loc[i, "P(x+5)"] = 1
                else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
            else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"]  
            
    for i in range(54, 60):
        if i not in [54, 59]:
            if (tabla2004.loc[54, "P(x+5)"] == 1 or tabla2004.loc[59, "P(x+5)"] == 1):
                if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) >= 1:
                    tabla2004.loc[i, "P(x+5)"] = 1
                else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
            else: tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"]

    for i in range(60, 61):
        if tabla2004.loc[i-1, "P(x+5)"] == 1:
            tabla2004.loc[i, "P(x+5)"] = 1
        if tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5)) < 1:
            tabla2004.loc[i, "P(x+5)"] = tabla2004.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2004 ** (1/5))
        else: tabla2004.loc[i, "P(x+5)"] = 1 
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2004.loc[0, "S(x)"] = 100000
    tabla2004.loc[4, "S(x)"] = tabla2004.loc[0, "S(x)"] * tabla2004.loc[4, "P(x+5)"]

    for i in [9, 14]:
        tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-5, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        
    tabla2004.loc[0, "FACTOR ANUAL"] = (tabla2004.loc[0, "S(x)"] / tabla2004.loc[4, "S(x)"]) ** (1/4)

    for i in [4, 9]:
        tabla2004.loc[i, "FACTOR ANUAL"] = (tabla2004.loc[i, "S(x)"] / tabla2004.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 14):
        if i not in [4, 9]:
            tabla2004.loc[i, "FACTOR ANUAL"] = tabla2004.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 14):
        if i not in [4, 9]:
            if tabla2004.loc[i, "FACTOR ANUAL"] == 1:
                tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] / tabla2004.loc[i, "FACTOR ANUAL"]
            else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] / tabla2004.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2004.loc[14, "P(x+5)"] == 1:
        tabla2004.loc[14, "S(x)"] = tabla2004.loc[13, "S(x)"] * tabla2004.loc[14, "P(x+5)"]
    else: tabla2004.loc[14, "S(x)"] = tabla2004.loc[9, "S(x)"] * tabla2004.loc[14, "P(x+5)"]
    
    if tabla2004.loc[19, "P(x+5)"] == 1:
        tabla2004.loc[14, "FACTOR ANUAL"] = 1
    else: tabla2004.loc[14, "FACTOR ANUAL"] = (tabla2004.loc[14, "S(x)"] / ((tabla2004.loc[14, "S(x)"] * tabla2004.loc[19, "P(x+5)"]))) ** (1/5)    

    for i in range(15, 19):
        if tabla2004.loc[19, "P(x+5)"] == 1:
            tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1 , "S(x)"] / tabla2004.loc[14, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2004.loc[19, "P(x+5)"] == 1:
        tabla2004.loc[19, "S(x)"] = tabla2004.loc[18, "S(x)"] * tabla2004.loc[19, "P(x+5)"]
    else: tabla2004.loc[19, "S(x)"] = tabla2004.loc[14, "S(x)"] * tabla2004.loc[19, "P(x+5)"]
    
    if tabla2004.loc[24, "P(x+5)"] == 1:
        tabla2004.loc[19, "FACTOR ANUAL"] = 1
    else: tabla2004.loc[19, "FACTOR ANUAL"] = (tabla2004.loc[19, "S(x)"] / ((tabla2004.loc[19, "S(x)"] * tabla2004.loc[24, "P(x+5)"]))) ** (1/5)    

    for i in range(20, 24):
        if tabla2004.loc[24, "P(x+5)"] == 1:
            tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1 , "S(x)"] / tabla2004.loc[19, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2004.loc[24, "P(x+5)"] == 1:
        tabla2004.loc[24, "S(x)"] = tabla2004.loc[23, "S(x)"] * tabla2004.loc[24, "P(x+5)"]
    else: tabla2004.loc[24, "S(x)"] = tabla2004.loc[19, "S(x)"] * tabla2004.loc[24, "P(x+5)"]
    
    if tabla2004.loc[29, "P(x+5)"] == 1:
        tabla2004.loc[24, "FACTOR ANUAL"] = 1
    else: tabla2004.loc[24, "FACTOR ANUAL"] = (tabla2004.loc[24, "S(x)"] / ((tabla2004.loc[24, "S(x)"] * tabla2004.loc[29, "P(x+5)"]))) ** (1/5)    

    for i in range(25, 29):
        if tabla2004.loc[29, "P(x+5)"] == 1 or tabla2004.loc[24, "P(x+5)"] == 1:
            tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1 , "S(x)"] / tabla2004.loc[24, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2004.loc[29, "P(x+5)"] == 1:
        tabla2004.loc[29, "S(x)"] = tabla2004.loc[28, "S(x)"] * tabla2004.loc[29, "P(x+5)"]
    else: tabla2004.loc[29, "S(x)"] = tabla2004.loc[24, "S(x)"] * tabla2004.loc[29, "P(x+5)"]
    
    if tabla2004.loc[34, "P(x+5)"] == 1:
        tabla2004.loc[29, "FACTOR ANUAL"] = 1
    else: tabla2004.loc[29, "FACTOR ANUAL"] = (tabla2004.loc[29, "S(x)"] / ((tabla2004.loc[29, "S(x)"] * tabla2004.loc[34, "P(x+5)"]))) ** (1/5)    

    for i in range(30, 34):
        if tabla2004.loc[34, "P(x+5)"] == 1 or tabla2004.loc[29, "P(x+5)"] == 1:
            tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1 , "S(x)"] / tabla2004.loc[29, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2004.loc[34, "P(x+5)"] == 1:
        tabla2004.loc[34, "S(x)"] = tabla2004.loc[33, "S(x)"] * tabla2004.loc[34, "P(x+5)"]
    else: tabla2004.loc[34, "S(x)"] = tabla2004.loc[29, "S(x)"] * tabla2004.loc[34, "P(x+5)"]
    
    if tabla2004.loc[39, "P(x+5)"] == 1:
        tabla2004.loc[34, "FACTOR ANUAL"] = 1
    else: tabla2004.loc[34, "FACTOR ANUAL"] = (tabla2004.loc[34, "S(x)"] / ((tabla2004.loc[34, "S(x)"] * tabla2004.loc[39, "P(x+5)"]))) ** (1/5)    

    for i in range(35, 39):
        if tabla2004.loc[39, "P(x+5)"] == 1 or tabla2004.loc[34, "P(x+5)"] == 1:
            tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1 , "S(x)"] / tabla2004.loc[34, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2004.loc[39, "P(x+5)"] == 1:
        tabla2004.loc[39, "S(x)"] = tabla2004.loc[38, "S(x)"] * tabla2004.loc[39, "P(x+5)"]
    else: tabla2004.loc[39, "S(x)"] = tabla2004.loc[34, "S(x)"] * tabla2004.loc[39, "P(x+5)"]

    #i+5   
    if tabla2004.loc[44, "P(x+5)"] == 1:
        tabla2004.loc[39, "FACTOR ANUAL"] = 1
    else: tabla2004.loc[39, "FACTOR ANUAL"] = (tabla2004.loc[39, "S(x)"] / ((tabla2004.loc[39, "S(x)"] * tabla2004.loc[44, "P(x+5)"]))) ** (1/5)    

    for i in range(40, 44):
        if tabla2004.loc[44, "P(x+5)"] == 1 or tabla2004.loc[39, "P(x+5)"] == 1:
            tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1 , "S(x)"] / tabla2004.loc[39, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2004.loc[44, "P(x+5)"] == 1:
        tabla2004.loc[44, "S(x)"] = tabla2004.loc[43, "S(x)"] * tabla2004.loc[44, "P(x+5)"]
    else: tabla2004.loc[44, "S(x)"] = tabla2004.loc[39, "S(x)"] * tabla2004.loc[44, "P(x+5)"]
    
    if tabla2004.loc[49, "P(x+5)"] == 1:
        tabla2004.loc[44, "FACTOR ANUAL"] = 1
    else: tabla2004.loc[44, "FACTOR ANUAL"] = (tabla2004.loc[44, "S(x)"] / ((tabla2004.loc[44, "S(x)"] * tabla2004.loc[49, "P(x+5)"]))) ** (1/5)    

    for i in range(45, 49):
        if tabla2004.loc[49, "P(x+5)"] == 1 or tabla2004.loc[44, "P(x+5)"] == 1:
            tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1 , "S(x)"] / tabla2004.loc[44, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2004.loc[49, "P(x+5)"] == 1:
        tabla2004.loc[49, "S(x)"] = tabla2004.loc[48, "S(x)"] * tabla2004.loc[49, "P(x+5)"]
    else: tabla2004.loc[49, "S(x)"] = tabla2004.loc[44, "S(x)"] * tabla2004.loc[49, "P(x+5)"]

    if tabla2004.loc[54, "P(x+5)"] == 1:
        tabla2004.loc[49, "FACTOR ANUAL"] = 1
    else: tabla2004.loc[49, "FACTOR ANUAL"] = (tabla2004.loc[49, "S(x)"] / ((tabla2004.loc[49, "S(x)"] * tabla2004.loc[54, "P(x+5)"]))) ** (1/5) 

    for i in range(50, 54):
        if tabla2004.loc[54, "P(x+5)"] == 1 or tabla2004.loc[49, "P(x+5)"] == 1:
            tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1 , "S(x)"] / tabla2004.loc[49, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2004.loc[54, "P(x+5)"] == 1:
        tabla2004.loc[54, "S(x)"] = tabla2004.loc[53, "S(x)"] * tabla2004.loc[54, "P(x+5)"]
    else: tabla2004.loc[54, "S(x)"] = tabla2004.loc[49, "S(x)"] * tabla2004.loc[54, "P(x+5)"]

    if tabla2004.loc[59, "P(x+5)"] == 1:
        tabla2004.loc[54, "FACTOR ANUAL"] = 1
    else: tabla2004.loc[54, "FACTOR ANUAL"] = (tabla2004.loc[54, "S(x)"] / ((tabla2004.loc[54, "S(x)"] * tabla2004.loc[59, "P(x+5)"]))) ** (1/5) 

    for i in range(55, 59):
        if tabla2004.loc[59, "P(x+5)"] == 1 or tabla2004.loc[54, "P(x+5)"] == 1:
            tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1 , "S(x)"] / tabla2004.loc[54, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2004.loc[59, "P(x+5)"] == 1:
        tabla2004.loc[59, "S(x)"] = tabla2004.loc[58, "S(x)"] * tabla2004.loc[59, "P(x+5)"]
    else: tabla2004.loc[59, "S(x)"] = tabla2004.loc[54, "S(x)"] * tabla2004.loc[59, "P(x+5)"]

    for i in range(59, 61):
        if i not in [59]:
            if tabla2004.loc[i-1, "P(x+5)"] == 1:
                tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
            else: tabla2004.loc[i, "S(x)"] = tabla2004.loc[i-1, "S(x)"] * tabla2004.loc[i, "P(x+5)"]
        
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla2005 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2005] = tabla2005

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2005.loc[3, "P(x+5)"] = GENERACION_2005.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2005
    tabla2005.loc[4: 7, "P(x+5)"] = tabla2005.loc[3, "P(x+5)"]
    tabla2005.loc[8, "P(x+5)"] = GENERACION_2005.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2005.loc[9: 12, "P(x+5)"] = tabla2005.loc[8, "P(x+5)"]
    tabla2005.loc[13, "P(x+5)"] = GENERACION_2005.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2005.loc[18, "P(x+5)"] = GENERACION_2005.loc[2, "PROBABILIDAD QUINQUENAL"]
        
    for i in [23, 28, 33, 38, 43, 48, 53, 58]:
        if tabla2005.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2005 <= 1:
            tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2005
        else:
            tabla2005.loc[i, "P(x+5)"] = 1

    for i in range(13, 19):
        if i not in [13, 18]:
            if (tabla2005.loc[13, "P(x+5)"] == 1 or tabla2005.loc[19, "P(x+5)"] == 1):
                if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) >= 1:
                    tabla2005.loc[i, "P(x+5)"] = 1
                else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
            else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"]

    for i in range(18, 24):
        if i not in [18, 23]:
            if (tabla2005.loc[18, "P(x+5)"] == 1 or tabla2005.loc[23, "P(x+5)"] == 1):
                if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) >= 1:
                    tabla2005.loc[i, "P(x+5)"] = 1
                else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
            else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"]

    for i in range(23, 29):
        if i not in [23, 28]:
            if (tabla2005.loc[23, "P(x+5)"] == 1 or tabla2005.loc[28, "P(x+5)"] == 1):
                if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) >= 1:
                    tabla2005.loc[i, "P(x+5)"] = 1
                else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
            else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] 
            
    for i in range(28, 34):
        if i not in [28, 33]:
            if (tabla2005.loc[28, "P(x+5)"] == 1 or tabla2005.loc[33, "P(x+5)"] == 1):
                if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) >= 1:
                    tabla2005.loc[i, "P(x+5)"] = 1
                else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
            else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"]       

    for i in range(33, 39):
        if i not in [33, 38]:
            if (tabla2005.loc[33, "P(x+5)"] == 1 or tabla2005.loc[38, "P(x+5)"] == 1):
                if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) >= 1:
                    tabla2005.loc[i, "P(x+5)"] = 1
                else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
            else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] 
            
    for i in range(38, 44):
        if i not in [38, 43]:
            if (tabla2005.loc[38, "P(x+5)"] == 1 or tabla2005.loc[43, "P(x+5)"] == 1):
                if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) >= 1:
                    tabla2005.loc[i, "P(x+5)"] = 1
                else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
            else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"]  

    for i in range(43, 49):
        if i not in [43, 48]:
            if (tabla2005.loc[43, "P(x+5)"] == 1 or tabla2005.loc[48, "P(x+5)"] == 1):
                if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) >= 1:
                    tabla2005.loc[i, "P(x+5)"] = 1
                else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
            else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"]  

    for i in range(48, 54):
        if i not in [48, 53]:
            if (tabla2005.loc[48, "P(x+5)"] == 1 or tabla2005.loc[53, "P(x+5)"] == 1):
                if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) >= 1:
                    tabla2005.loc[i, "P(x+5)"] = 1
                else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
            else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"]  
            
    for i in range(53, 59):
        if i not in [53, 58]:
            if (tabla2005.loc[53, "P(x+5)"] == 1 or tabla2005.loc[58, "P(x+5)"] == 1):
                if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) >= 1:
                    tabla2005.loc[i, "P(x+5)"] = 1
                else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
            else: tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"]

    for i in range(59, 61):
        if tabla2005.loc[i-1, "P(x+5)"] == 1:
            tabla2005.loc[i, "P(x+5)"] = 1
        if tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5)) < 1:
            tabla2005.loc[i, "P(x+5)"] = tabla2005.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2005 ** (1/5))
        else: tabla2005.loc[i, "P(x+5)"] = 1  
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2005.loc[0, "S(x)"] = 100000
    tabla2005.loc[3, "S(x)"] = tabla2005.loc[0, "S(x)"] * tabla2005.loc[3, "P(x+5)"]

    for i in [8, 13]:
        tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-5, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        
    tabla2005.loc[0, "FACTOR ANUAL"] = (tabla2005.loc[0, "S(x)"] / tabla2005.loc[3, "S(x)"]) ** (1/3)

    for i in [3, 8]:
        tabla2005.loc[i, "FACTOR ANUAL"] = (tabla2005.loc[i, "S(x)"] / tabla2005.loc[i+5, "S(x)"]) ** (1/5)

    for i in range(1, 13):
        if i not in [3, 8]:
            tabla2005.loc[i, "FACTOR ANUAL"] = tabla2005.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 13):
        if i not in [3, 8]:
            if tabla2005.loc[i, "FACTOR ANUAL"] == 1:
                tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] / tabla2005.loc[i, "FACTOR ANUAL"]
            else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] / tabla2005.loc[i, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 13        
    if tabla2005.loc[13, "P(x+5)"] == 1:
        tabla2005.loc[13, "S(x)"] = tabla2005.loc[12, "S(x)"] * tabla2005.loc[13, "P(x+5)"]
    else: tabla2005.loc[13, "S(x)"] = tabla2005.loc[8, "S(x)"] * tabla2005.loc[13, "P(x+5)"]

    if tabla2005.loc[18, "P(x+5)"] == 1:
        tabla2005.loc[13, "FACTOR ANUAL"] = 1
    else: tabla2005.loc[13, "FACTOR ANUAL"] = (tabla2005.loc[13, "S(x)"] / ((tabla2005.loc[13, "S(x)"] * tabla2005.loc[18, "P(x+5)"]))) ** (1/5)
    
    for i in range(14, 18):
        if tabla2005.loc[18, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1 , "S(x)"] / tabla2005.loc[13, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 18        
    if tabla2005.loc[18, "P(x+5)"] == 1:
        tabla2005.loc[18, "S(x)"] = tabla2005.loc[17, "S(x)"] * tabla2005.loc[18, "P(x+5)"]
    else: tabla2005.loc[18, "S(x)"] = tabla2005.loc[13, "S(x)"] * tabla2005.loc[18, "P(x+5)"]

    if tabla2005.loc[23, "P(x+5)"] == 1:
        tabla2005.loc[18, "FACTOR ANUAL"] = 1
    else: tabla2005.loc[18, "FACTOR ANUAL"] = (tabla2005.loc[18, "S(x)"] / ((tabla2005.loc[18, "S(x)"] * tabla2005.loc[23, "P(x+5)"]))) ** (1/5)
    
    for i in range(19, 23):
        if tabla2005.loc[23, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1 , "S(x)"] / tabla2005.loc[18, "FACTOR ANUAL"]
        
            #-----------------------------------------------------------------INTERVALO 23        
    if tabla2005.loc[23, "P(x+5)"] == 1:
        tabla2005.loc[23, "S(x)"] = tabla2005.loc[22, "S(x)"] * tabla2005.loc[23, "P(x+5)"]
    else: tabla2005.loc[23, "S(x)"] = tabla2005.loc[18, "S(x)"] * tabla2005.loc[23, "P(x+5)"]

    if tabla2005.loc[28, "P(x+5)"] == 1:
        tabla2005.loc[23, "FACTOR ANUAL"] = 1
    else: tabla2005.loc[23, "FACTOR ANUAL"] = (tabla2005.loc[23, "S(x)"] / ((tabla2005.loc[23, "S(x)"] * tabla2005.loc[28, "P(x+5)"]))) ** (1/5)
    
    for i in range(24, 28):
        if tabla2005.loc[28, "P(x+5)"] == 1 or tabla2005.loc[23, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1 , "S(x)"] / tabla2005.loc[23, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 28
    if tabla2005.loc[28, "P(x+5)"] == 1:
        tabla2005.loc[28, "S(x)"] = tabla2005.loc[27, "S(x)"] * tabla2005.loc[28, "P(x+5)"]
    else: tabla2005.loc[28, "S(x)"] = tabla2005.loc[23, "S(x)"] * tabla2005.loc[28, "P(x+5)"]

    if tabla2005.loc[33, "P(x+5)"] == 1:
        tabla2005.loc[28, "FACTOR ANUAL"] = 1
    else: tabla2005.loc[28, "FACTOR ANUAL"] = (tabla2005.loc[28, "S(x)"] / ((tabla2005.loc[28, "S(x)"] * tabla2005.loc[33, "P(x+5)"]))) ** (1/5)
    
    for i in range(29, 33):
        if tabla2005.loc[28, "P(x+5)"] == 1 or tabla2005.loc[33, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1 , "S(x)"] / tabla2005.loc[28, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 33
    if tabla2005.loc[33, "P(x+5)"] == 1:
        tabla2005.loc[33, "S(x)"] = tabla2005.loc[32, "S(x)"] * tabla2005.loc[33, "P(x+5)"]
    else: tabla2005.loc[33, "S(x)"] = tabla2005.loc[28, "S(x)"] * tabla2005.loc[33, "P(x+5)"]
    
    if tabla2005.loc[38, "P(x+5)"] == 1:
        tabla2005.loc[33, "FACTOR ANUAL"] = 1
    else: tabla2005.loc[33, "FACTOR ANUAL"] = (tabla2005.loc[33, "S(x)"] / ((tabla2005.loc[33, "S(x)"] * tabla2005.loc[38, "P(x+5)"]))) ** (1/5)    

    for i in range(34, 38):
        if tabla2005.loc[38, "P(x+5)"] == 1 or tabla2005.loc[33, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1 , "S(x)"] / tabla2005.loc[33, "FACTOR ANUAL"]
        
            #-----------------------------------------------------------------INTERVALO 38
    if tabla2005.loc[38, "P(x+5)"] == 1:
        tabla2005.loc[38, "S(x)"] = tabla2005.loc[37, "S(x)"] * tabla2005.loc[38, "P(x+5)"]
    else: tabla2005.loc[38, "S(x)"] = tabla2005.loc[33, "S(x)"] * tabla2005.loc[38, "P(x+5)"]

    #i+5   
    if tabla2005.loc[43, "P(x+5)"] == 1:
        tabla2005.loc[38, "FACTOR ANUAL"] = 1
    else: tabla2005.loc[38, "FACTOR ANUAL"] = (tabla2005.loc[38, "S(x)"] / ((tabla2005.loc[38, "S(x)"] * tabla2005.loc[43, "P(x+5)"]))) ** (1/5)    

    for i in range(39, 43):
        if tabla2005.loc[43, "P(x+5)"] == 1 or tabla2005.loc[38, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1 , "S(x)"] / tabla2005.loc[38, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 43
    if tabla2005.loc[43, "P(x+5)"] == 1:
        tabla2005.loc[43, "S(x)"] = tabla2005.loc[42, "S(x)"] * tabla2005.loc[43, "P(x+5)"]
    else: tabla2005.loc[43, "S(x)"] = tabla2005.loc[38, "S(x)"] * tabla2005.loc[43, "P(x+5)"]

    #i+5   
    if tabla2005.loc[48, "P(x+5)"] == 1:
        tabla2005.loc[43, "FACTOR ANUAL"] = 1
    else: tabla2005.loc[43, "FACTOR ANUAL"] = (tabla2005.loc[43, "S(x)"] / ((tabla2005.loc[43, "S(x)"] * tabla2005.loc[48, "P(x+5)"]))) ** (1/5)    

    for i in range(44, 48):
        if tabla2005.loc[48, "P(x+5)"] == 1 or tabla2005.loc[43, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1 , "S(x)"] / tabla2005.loc[43, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 48
    if tabla2005.loc[48, "P(x+5)"] == 1:
        tabla2005.loc[48, "S(x)"] = tabla2005.loc[47, "S(x)"] * tabla2005.loc[48, "P(x+5)"]
    else: tabla2005.loc[48, "S(x)"] = tabla2005.loc[43, "S(x)"] * tabla2005.loc[48, "P(x+5)"]

    #i+5   
    if tabla2005.loc[53, "P(x+5)"] == 1:
        tabla2005.loc[48, "FACTOR ANUAL"] = 1
    else: tabla2005.loc[48, "FACTOR ANUAL"] = (tabla2005.loc[48, "S(x)"] / ((tabla2005.loc[48, "S(x)"] * tabla2005.loc[53, "P(x+5)"]))) ** (1/5)    

    for i in range(49, 53):
        if tabla2005.loc[53, "P(x+5)"] == 1 or tabla2005.loc[48, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1 , "S(x)"] / tabla2005.loc[48, "FACTOR ANUAL"]
            
            #-----------------------------------------------------------------INTERVALO 53
    if tabla2005.loc[53, "P(x+5)"] == 1:
        tabla2005.loc[53, "S(x)"] = tabla2005.loc[52, "S(x)"] * tabla2005.loc[53, "P(x+5)"]
    else: tabla2005.loc[53, "S(x)"] = tabla2005.loc[48, "S(x)"] * tabla2005.loc[53, "P(x+5)"]

    #i+5   
    if tabla2005.loc[58, "P(x+5)"] == 1:
        tabla2005.loc[53, "FACTOR ANUAL"] = 1
    else: tabla2005.loc[53, "FACTOR ANUAL"] = (tabla2005.loc[53, "S(x)"] / ((tabla2005.loc[53, "S(x)"] * tabla2005.loc[58, "P(x+5)"]))) ** (1/5)    

    for i in range(54, 58):
        if tabla2005.loc[58, "P(x+5)"] == 1 or tabla2005.loc[53, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1 , "S(x)"] / tabla2005.loc[53, "FACTOR ANUAL"]    

            #-----------------------------------------------------------------INTERVALO 58
    if tabla2005.loc[58, "P(x+5)"] == 1:
        tabla2005.loc[58, "S(x)"] = tabla2005.loc[57, "S(x)"] * tabla2005.loc[58, "P(x+5)"]
    else: tabla2005.loc[58, "S(x)"] = tabla2005.loc[53, "S(x)"] * tabla2005.loc[58, "P(x+5)"]

    for i in range(59, 61):
        if tabla2005.loc[i-1, "P(x+5)"] == 1:
            tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]
        else: tabla2005.loc[i, "S(x)"] = tabla2005.loc[i-1, "S(x)"] * tabla2005.loc[i, "P(x+5)"]    

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla2006 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2006] = tabla2006

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2006.loc[2, "P(x+5)"] = GENERACION_2006.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2006
    tabla2006.loc[3: 6, "P(x+5)"] = tabla2006.loc[2, "P(x+5)"]
    tabla2006.loc[7, "P(x+5)"] = GENERACION_2006.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2006.loc[8: 11, "P(x+5)"] = tabla2006.loc[7, "P(x+5)"]
    tabla2006.loc[12, "P(x+5)"] = GENERACION_2006.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2006.loc[17, "P(x+5)"] = GENERACION_2006.loc[2, "PROBABILIDAD QUINQUENAL"]
        
    for i in [22, 27, 32, 37, 42, 47, 52, 57]:
        if tabla2006.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2006 <= 1:
            tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2006
        else:
            tabla2006.loc[i, "P(x+5)"] = 1

    for i in range(12, 18):
        if i not in [12, 17]:
            if (tabla2006.loc[12, "P(x+5)"] == 1 or tabla2006.loc[17, "P(x+5)"] == 1):
                if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) >= 1:
                    tabla2006.loc[i, "P(x+5)"] = 1
                else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
            else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"]

    for i in range(17, 23):
        if i not in [17, 22]:
            if (tabla2006.loc[17, "P(x+5)"] == 1 or tabla2006.loc[22, "P(x+5)"] == 1):
                if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) >= 1:
                    tabla2006.loc[i, "P(x+5)"] = 1
                else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
            else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"]

    for i in range(22, 28):
        if i not in [22, 27]:
            if (tabla2006.loc[22, "P(x+5)"] == 1 or tabla2006.loc[27, "P(x+5)"] == 1):
                if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) >= 1:
                    tabla2006.loc[i, "P(x+5)"] = 1
                else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
            else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"]
            
    for i in range(27, 33):
        if i not in [27, 32]:
            if (tabla2006.loc[27, "P(x+5)"] == 1 or tabla2006.loc[32, "P(x+5)"] == 1):
                if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) >= 1:
                    tabla2006.loc[i, "P(x+5)"] = 1
                else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
            else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"]       

    for i in range(32, 38):
        if i not in [32, 37]:
            if (tabla2006.loc[32, "P(x+5)"] == 1 or tabla2006.loc[37, "P(x+5)"] == 1):
                if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) >= 1:
                    tabla2006.loc[i, "P(x+5)"] = 1
                else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
            else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] 
            
    for i in range(37, 43):
        if i not in [37, 42]:
            if (tabla2006.loc[37, "P(x+5)"] == 1 or tabla2006.loc[42, "P(x+5)"] == 1):
                if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) >= 1:
                    tabla2006.loc[i, "P(x+5)"] = 1
                else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
            else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"]  

    for i in range(42, 48):
        if i not in [42, 47]:
            if (tabla2006.loc[42, "P(x+5)"] == 1 or tabla2006.loc[47, "P(x+5)"] == 1):
                if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) >= 1:
                    tabla2006.loc[i, "P(x+5)"] = 1
                else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
            else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"]  

    for i in range(47, 53):
        if i not in [47, 52]:
            if (tabla2006.loc[47, "P(x+5)"] == 1 or tabla2006.loc[52, "P(x+5)"] == 1):
                if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) >= 1:
                    tabla2006.loc[i, "P(x+5)"] = 1
                else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
            else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"]  
            
    for i in range(52, 58):
        if i not in [52, 57]:
            if (tabla2006.loc[52, "P(x+5)"] == 1 or tabla2006.loc[57, "P(x+5)"] == 1):
                if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) >= 1:
                    tabla2006.loc[i, "P(x+5)"] = 1
                else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
            else: tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"]

    for i in range(58, 61):
        if tabla2006.loc[i-1, "P(x+5)"] == 1:
            tabla2006.loc[i, "P(x+5)"] = 1
        if tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5)) < 1:
            tabla2006.loc[i, "P(x+5)"] = tabla2006.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2006 ** (1/5))
        else: tabla2006.loc[i, "P(x+5)"] = 1

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2006.loc[0, "S(x)"] = 100000
    tabla2006.loc[2, "S(x)"] = tabla2006.loc[0, "S(x)"] * tabla2006.loc[2, "P(x+5)"]

    for i in [7, 12]:
        tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-5, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        
    tabla2006.loc[0, "FACTOR ANUAL"] = (tabla2006.loc[0, "S(x)"] / tabla2006.loc[2, "S(x)"]) ** (1/2)

    for i in [2, 7]:
        tabla2006.loc[i, "FACTOR ANUAL"] = (tabla2006.loc[i, "S(x)"] / tabla2006.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 12):
        if i not in [2, 7]:
            tabla2006.loc[i, "FACTOR ANUAL"] = tabla2006.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 12):
        if i not in [2, 7]:
            if tabla2006.loc[i, "FACTOR ANUAL"] == 1:
                tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] / tabla2006.loc[i, "FACTOR ANUAL"]
            else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] / tabla2006.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2006.loc[12, "P(x+5)"] == 1:
        tabla2006.loc[12, "S(x)"] = tabla2006.loc[11, "S(x)"] * tabla2006.loc[12, "P(x+5)"]
    else: tabla2006.loc[12, "S(x)"] = tabla2006.loc[7, "S(x)"] * tabla2006.loc[12, "P(x+5)"]
    
    if tabla2006.loc[17, "P(x+5)"] == 1:
        tabla2006.loc[12, "FACTOR ANUAL"] = 1
    else: tabla2006.loc[12, "FACTOR ANUAL"] = (tabla2006.loc[12, "S(x)"] / ((tabla2006.loc[12, "S(x)"] * tabla2006.loc[17, "P(x+5)"]))) ** (1/5)    

    for i in range(13, 17):
        if tabla2006.loc[17, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1 , "S(x)"] / tabla2006.loc[12, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2006.loc[17, "P(x+5)"] == 1:
        tabla2006.loc[17, "S(x)"] = tabla2006.loc[16, "S(x)"] * tabla2006.loc[17, "P(x+5)"]
    else: tabla2006.loc[17, "S(x)"] = tabla2006.loc[12, "S(x)"] * tabla2006.loc[17, "P(x+5)"]
    
    if tabla2006.loc[22, "P(x+5)"] == 1:
        tabla2006.loc[17, "FACTOR ANUAL"] = 1
    else: tabla2006.loc[17, "FACTOR ANUAL"] = (tabla2006.loc[17, "S(x)"] / ((tabla2006.loc[17, "S(x)"] * tabla2006.loc[22, "P(x+5)"]))) ** (1/5)    

    for i in range(18, 22):
        if tabla2006.loc[22, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1 , "S(x)"] / tabla2006.loc[17, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2006.loc[22, "P(x+5)"] == 1:
        tabla2006.loc[22, "S(x)"] = tabla2006.loc[21, "S(x)"] * tabla2006.loc[22, "P(x+5)"]
    else: tabla2006.loc[22, "S(x)"] = tabla2006.loc[17, "S(x)"] * tabla2006.loc[22, "P(x+5)"]
    
    if tabla2006.loc[27, "P(x+5)"] == 1:
        tabla2006.loc[22, "FACTOR ANUAL"] = 1
    else: tabla2006.loc[22, "FACTOR ANUAL"] = (tabla2006.loc[22, "S(x)"] / ((tabla2006.loc[22, "S(x)"] * tabla2006.loc[27, "P(x+5)"]))) ** (1/5)    

    for i in range(23, 27):
        if tabla2006.loc[27, "P(x+5)"] == 1 or tabla2006.loc[22, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1 , "S(x)"] / tabla2006.loc[22, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2006.loc[27, "P(x+5)"] == 1:
        tabla2006.loc[27, "S(x)"] = tabla2006.loc[26, "S(x)"] * tabla2006.loc[27, "P(x+5)"]
    else: tabla2006.loc[27, "S(x)"] = tabla2006.loc[22, "S(x)"] * tabla2006.loc[27, "P(x+5)"]
    
    if tabla2006.loc[32, "P(x+5)"] == 1:
        tabla2006.loc[27, "FACTOR ANUAL"] = 1
    else: tabla2006.loc[27, "FACTOR ANUAL"] = (tabla2006.loc[27, "S(x)"] / ((tabla2006.loc[27, "S(x)"] * tabla2006.loc[32, "P(x+5)"]))) ** (1/5)    

    for i in range(28, 32):
        if tabla2006.loc[32, "P(x+5)"] == 1 or tabla2006.loc[27, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1 , "S(x)"] / tabla2006.loc[27, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2006.loc[32, "P(x+5)"] == 1:
        tabla2006.loc[32, "S(x)"] = tabla2006.loc[31, "S(x)"] * tabla2006.loc[32, "P(x+5)"]
    else: tabla2006.loc[32, "S(x)"] = tabla2006.loc[27, "S(x)"] * tabla2006.loc[32, "P(x+5)"]
    
    if tabla2006.loc[37, "P(x+5)"] == 1:
        tabla2006.loc[32, "FACTOR ANUAL"] = 1
    else: tabla2006.loc[32, "FACTOR ANUAL"] = (tabla2006.loc[32, "S(x)"] / ((tabla2006.loc[32, "S(x)"] * tabla2006.loc[37, "P(x+5)"]))) ** (1/5)    

    for i in range(33, 37):
        if tabla2006.loc[37, "P(x+5)"] == 1 or tabla2006.loc[32, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1 , "S(x)"] / tabla2006.loc[32, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2006.loc[37, "P(x+5)"] == 1:
        tabla2006.loc[37, "S(x)"] = tabla2006.loc[36, "S(x)"] * tabla2006.loc[37, "P(x+5)"]
    else: tabla2006.loc[37, "S(x)"] = tabla2006.loc[32, "S(x)"] * tabla2006.loc[37, "P(x+5)"]

    #i+5   
    if tabla2006.loc[42, "P(x+5)"] == 1:
        tabla2006.loc[37, "FACTOR ANUAL"] = 1
    else: tabla2006.loc[37, "FACTOR ANUAL"] = (tabla2006.loc[37, "S(x)"] / ((tabla2006.loc[37, "S(x)"] * tabla2006.loc[42, "P(x+5)"]))) ** (1/5)    

    for i in range(38, 42):
        if tabla2006.loc[42, "P(x+5)"] == 1 or tabla2006.loc[37, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1 , "S(x)"] / tabla2006.loc[37, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2006.loc[42, "P(x+5)"] == 1:
        tabla2006.loc[42, "S(x)"] = tabla2006.loc[41, "S(x)"] * tabla2006.loc[42, "P(x+5)"]
    else: tabla2006.loc[42, "S(x)"] = tabla2006.loc[37, "S(x)"] * tabla2006.loc[42, "P(x+5)"]
    
    if tabla2006.loc[47, "P(x+5)"] == 1:
        tabla2006.loc[42, "FACTOR ANUAL"] = 1
    else: tabla2006.loc[42, "FACTOR ANUAL"] = (tabla2006.loc[42, "S(x)"] / ((tabla2006.loc[42, "S(x)"] * tabla2006.loc[47, "P(x+5)"]))) ** (1/5)    

    for i in range(43, 47):
        if tabla2006.loc[47, "P(x+5)"] == 1 or tabla2006.loc[42, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1 , "S(x)"] / tabla2006.loc[42, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2006.loc[47, "P(x+5)"] == 1:
        tabla2006.loc[47, "S(x)"] = tabla2006.loc[46, "S(x)"] * tabla2006.loc[47, "P(x+5)"]
    else: tabla2006.loc[47, "S(x)"] = tabla2006.loc[42, "S(x)"] * tabla2006.loc[47, "P(x+5)"]

    if tabla2006.loc[52, "P(x+5)"] == 1:
        tabla2006.loc[47, "FACTOR ANUAL"] = 1
    else: tabla2006.loc[47, "FACTOR ANUAL"] = (tabla2006.loc[47, "S(x)"] / ((tabla2006.loc[47, "S(x)"] * tabla2006.loc[52, "P(x+5)"]))) ** (1/5) 

    for i in range(48, 52):
        if tabla2006.loc[52, "P(x+5)"] == 1 or tabla2006.loc[47, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1 , "S(x)"] / tabla2006.loc[47, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2006.loc[52, "P(x+5)"] == 1:
        tabla2006.loc[52, "S(x)"] = tabla2006.loc[51, "S(x)"] * tabla2006.loc[52, "P(x+5)"]
    else: tabla2006.loc[52, "S(x)"] = tabla2006.loc[47, "S(x)"] * tabla2006.loc[52, "P(x+5)"]

    if tabla2006.loc[57, "P(x+5)"] == 1:
        tabla2006.loc[52, "FACTOR ANUAL"] = 1
    else: tabla2006.loc[52, "FACTOR ANUAL"] = (tabla2006.loc[52, "S(x)"] / ((tabla2006.loc[52, "S(x)"] * tabla2006.loc[57, "P(x+5)"]))) ** (1/5) 

    for i in range(53, 57):
        if tabla2006.loc[57, "P(x+5)"] == 1 or tabla2006.loc[52, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1 , "S(x)"] / tabla2006.loc[52, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2006.loc[57, "P(x+5)"] == 1:
        tabla2006.loc[57, "S(x)"] = tabla2006.loc[56, "S(x)"] * tabla2006.loc[57, "P(x+5)"]
    else: tabla2006.loc[57, "S(x)"] = tabla2006.loc[52, "S(x)"] * tabla2006.loc[57, "P(x+5)"]

    for i in range(58, 61):
        if tabla2006.loc[i-1, "P(x+5)"] == 1:
            tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]
        else: tabla2006.loc[i, "S(x)"] = tabla2006.loc[i-1, "S(x)"] * tabla2006.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla2007 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2007] = tabla2007

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2007.loc[1, "P(x+5)"] = GENERACION_2007.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2007
    tabla2007.loc[2: 5, "P(x+5)"] = tabla2007.loc[1, "P(x+5)"]
    tabla2007.loc[6, "P(x+5)"] = GENERACION_2007.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2007.loc[7: 10, "P(x+5)"] = tabla2007.loc[6, "P(x+5)"]
    tabla2007.loc[11, "P(x+5)"] = GENERACION_2007.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2007.loc[16, "P(x+5)"] = GENERACION_2007.loc[2, "PROBABILIDAD QUINQUENAL"]

    for i in [21, 26, 31, 36, 41, 46, 51, 56]:
        if tabla2007.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2007 <= 1:
            tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2007
        else:
            tabla2007.loc[i, "P(x+5)"] = 1

    for i in range(11, 17):
        if i not in [11, 16]:
            if (tabla2007.loc[11, "P(x+5)"] == 1 or tabla2007.loc[16, "P(x+5)"] == 1):
                if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) >= 1:
                    tabla2007.loc[i, "P(x+5)"] = 1
                else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
            else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"]

    for i in range(16, 22):
        if i not in [16, 21]:
            if (tabla2007.loc[16, "P(x+5)"] == 1 or tabla2007.loc[21, "P(x+5)"] == 1):
                if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) >= 1:
                    tabla2007.loc[i, "P(x+5)"] = 1
                else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
            else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] 

    for i in range(21, 27):
        if i not in [21, 26]:
            if (tabla2007.loc[21, "P(x+5)"] == 1 or tabla2007.loc[26, "P(x+5)"] == 1):
                if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) >= 1:
                    tabla2007.loc[i, "P(x+5)"] = 1
                else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
            else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] 

    for i in range(26, 32):
        if i not in [26, 31]:
            if (tabla2007.loc[26, "P(x+5)"] == 1 or tabla2007.loc[31, "P(x+5)"] == 1):
                if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) >= 1:
                    tabla2007.loc[i, "P(x+5)"] = 1
                else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
            else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] 

    for i in range(31, 37):
        if i not in [31, 36]:
            if (tabla2007.loc[31, "P(x+5)"] == 1 or tabla2007.loc[36, "P(x+5)"] == 1):
                if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) >= 1:
                    tabla2007.loc[i, "P(x+5)"] = 1
                else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
            else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] 

    for i in range(36, 42):
        if i not in [36, 41]:
            if (tabla2007.loc[36, "P(x+5)"] == 1 or tabla2007.loc[41, "P(x+5)"] == 1):
                if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) >= 1:
                    tabla2007.loc[i, "P(x+5)"] = 1
                else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
            else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] 

    for i in range(41, 47):
        if i not in [41, 46]:
            if (tabla2007.loc[41, "P(x+5)"] == 1 or tabla2007.loc[46, "P(x+5)"] == 1):
                if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) >= 1:
                    tabla2007.loc[i, "P(x+5)"] = 1
                else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
            else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"]  

    for i in range(46, 52):
        if i not in [46, 51]:
            if (tabla2007.loc[46, "P(x+5)"] == 1 or tabla2007.loc[51, "P(x+5)"] == 1):
                if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) >= 1:
                    tabla2007.loc[i, "P(x+5)"] = 1
                else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
            else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"]  
            
    for i in range(51, 57):
        if i not in [51, 56]:
            if (tabla2007.loc[51, "P(x+5)"] == 1 or tabla2007.loc[56, "P(x+5)"] == 1):
                if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) >= 1:
                    tabla2007.loc[i, "P(x+5)"] = 1
                else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
            else: tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"]

    for i in range(57, 61):
        if tabla2007.loc[i-1, "P(x+5)"] == 1:
            tabla2007.loc[i, "P(x+5)"] = 1
        if tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5)) < 1:
            tabla2007.loc[i, "P(x+5)"] = tabla2007.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2007 ** (1/5))
        else: tabla2007.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2007.loc[0, "S(x)"] = 100000
    tabla2007.loc[1, "S(x)"] = tabla2007.loc[0, "S(x)"] * tabla2007.loc[1, "P(x+5)"]

    for i in [6, 11]:
        tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-5, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        
    #tabla2007.loc[0, "FACTOR ANUAL"] = (tabla2007.loc[0, "S(x)"] / tabla2007.loc[1, "S(x)"]) ** (1/5)

    for i in [1, 6]:
        tabla2007.loc[i, "FACTOR ANUAL"] = (tabla2007.loc[i, "S(x)"] / tabla2007.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 11):
        if i not in [1, 6]:
            tabla2007.loc[i, "FACTOR ANUAL"] = tabla2007.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 11):
        if i not in [1, 6]:
            if tabla2007.loc[i, "FACTOR ANUAL"] == 1:
                tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] / tabla2007.loc[i, "FACTOR ANUAL"]
            else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] / tabla2007.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2007.loc[11, "P(x+5)"] == 1:
        tabla2007.loc[11, "S(x)"] = tabla2007.loc[10, "S(x)"] * tabla2007.loc[11, "P(x+5)"]
    else: tabla2007.loc[11, "S(x)"] = tabla2007.loc[6, "S(x)"] * tabla2007.loc[11, "P(x+5)"]
    
    if tabla2007.loc[16, "P(x+5)"] == 1:
        tabla2007.loc[11, "FACTOR ANUAL"] = 1
    else: tabla2007.loc[11, "FACTOR ANUAL"] = (tabla2007.loc[11, "S(x)"] / ((tabla2007.loc[11, "S(x)"] * tabla2007.loc[16, "P(x+5)"]))) ** (1/5)    

    for i in range(12, 16):
        if tabla2007.loc[16, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1 , "S(x)"] / tabla2007.loc[11, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2007.loc[16, "P(x+5)"] == 1:
        tabla2007.loc[16, "S(x)"] = tabla2007.loc[15, "S(x)"] * tabla2007.loc[16, "P(x+5)"]
    else: tabla2007.loc[16, "S(x)"] = tabla2007.loc[11, "S(x)"] * tabla2007.loc[16, "P(x+5)"]
    
    if tabla2007.loc[21, "P(x+5)"] == 1:
        tabla2007.loc[16, "FACTOR ANUAL"] = 1
    else: tabla2007.loc[16, "FACTOR ANUAL"] = (tabla2007.loc[16, "S(x)"] / ((tabla2007.loc[16, "S(x)"] * tabla2007.loc[21, "P(x+5)"]))) ** (1/5)    

    for i in range(17, 21):
        if tabla2007.loc[21, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1 , "S(x)"] / tabla2007.loc[16, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2007.loc[21, "P(x+5)"] == 1:
        tabla2007.loc[21, "S(x)"] = tabla2007.loc[20, "S(x)"] * tabla2007.loc[21, "P(x+5)"]
    else: tabla2007.loc[21, "S(x)"] = tabla2007.loc[16, "S(x)"] * tabla2007.loc[21, "P(x+5)"]
    
    if tabla2007.loc[26, "P(x+5)"] == 1:
        tabla2007.loc[21, "FACTOR ANUAL"] = 1
    else: tabla2007.loc[21, "FACTOR ANUAL"] = (tabla2007.loc[21, "S(x)"] / ((tabla2007.loc[21, "S(x)"] * tabla2007.loc[26, "P(x+5)"]))) ** (1/5)    

    for i in range(22, 26):
        if tabla2007.loc[26, "P(x+5)"] == 1 or tabla2007.loc[21, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1 , "S(x)"] / tabla2007.loc[21, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2007.loc[26, "P(x+5)"] == 1:
        tabla2007.loc[26, "S(x)"] = tabla2007.loc[25, "S(x)"] * tabla2007.loc[26, "P(x+5)"]
    else: tabla2007.loc[26, "S(x)"] = tabla2007.loc[21, "S(x)"] * tabla2007.loc[26, "P(x+5)"]
    
    if tabla2007.loc[31, "P(x+5)"] == 1:
        tabla2007.loc[26, "FACTOR ANUAL"] = 1
    else: tabla2007.loc[26, "FACTOR ANUAL"] = (tabla2007.loc[26, "S(x)"] / ((tabla2007.loc[26, "S(x)"] * tabla2007.loc[31, "P(x+5)"]))) ** (1/5)    

    for i in range(27, 31):
        if tabla2007.loc[31, "P(x+5)"] == 1 or tabla2007.loc[26, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1 , "S(x)"] / tabla2007.loc[26, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2007.loc[31, "P(x+5)"] == 1:
        tabla2007.loc[31, "S(x)"] = tabla2007.loc[30, "S(x)"] * tabla2007.loc[31, "P(x+5)"]
    else: tabla2007.loc[31, "S(x)"] = tabla2007.loc[26, "S(x)"] * tabla2007.loc[31, "P(x+5)"]
    
    if tabla2007.loc[36, "P(x+5)"] == 1:
        tabla2007.loc[31, "FACTOR ANUAL"] = 1
    else: tabla2007.loc[31, "FACTOR ANUAL"] = (tabla2007.loc[31, "S(x)"] / ((tabla2007.loc[31, "S(x)"] * tabla2007.loc[36, "P(x+5)"]))) ** (1/5)    

    for i in range(32, 36):
        if tabla2007.loc[36, "P(x+5)"] == 1 or tabla2007.loc[31, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1 , "S(x)"] / tabla2007.loc[31, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2007.loc[36, "P(x+5)"] == 1:
        tabla2007.loc[36, "S(x)"] = tabla2007.loc[35, "S(x)"] * tabla2007.loc[36, "P(x+5)"]
    else: tabla2007.loc[36, "S(x)"] = tabla2007.loc[31, "S(x)"] * tabla2007.loc[36, "P(x+5)"]

    #i+5   
    if tabla2007.loc[41, "P(x+5)"] == 1:
        tabla2007.loc[36, "FACTOR ANUAL"] = 1
    else: tabla2007.loc[36, "FACTOR ANUAL"] = (tabla2007.loc[36, "S(x)"] / ((tabla2007.loc[36, "S(x)"] * tabla2007.loc[41, "P(x+5)"]))) ** (1/5)    

    for i in range(37, 41):
        if tabla2007.loc[41, "P(x+5)"] == 1 or tabla2007.loc[36, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1 , "S(x)"] / tabla2007.loc[36, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2007.loc[41, "P(x+5)"] == 1:
        tabla2007.loc[41, "S(x)"] = tabla2007.loc[40, "S(x)"] * tabla2007.loc[41, "P(x+5)"]
    else: tabla2007.loc[41, "S(x)"] = tabla2007.loc[36, "S(x)"] * tabla2007.loc[41, "P(x+5)"]
    
    if tabla2007.loc[46, "P(x+5)"] == 1:
        tabla2007.loc[41, "FACTOR ANUAL"] = 1
    else: tabla2007.loc[41, "FACTOR ANUAL"] = (tabla2007.loc[41, "S(x)"] / ((tabla2007.loc[41, "S(x)"] * tabla2007.loc[46, "P(x+5)"]))) ** (1/5)    

    for i in range(42, 46):
        if tabla2007.loc[46, "P(x+5)"] == 1 or tabla2007.loc[41, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1 , "S(x)"] / tabla2007.loc[41, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2007.loc[46, "P(x+5)"] == 1:
        tabla2007.loc[46, "S(x)"] = tabla2007.loc[45, "S(x)"] * tabla2007.loc[46, "P(x+5)"]
    else: tabla2007.loc[46, "S(x)"] = tabla2007.loc[41, "S(x)"] * tabla2007.loc[46, "P(x+5)"]

    if tabla2007.loc[51, "P(x+5)"] == 1:
        tabla2007.loc[46, "FACTOR ANUAL"] = 1
    else: tabla2007.loc[46, "FACTOR ANUAL"] = (tabla2007.loc[46, "S(x)"] / ((tabla2007.loc[46, "S(x)"] * tabla2007.loc[51, "P(x+5)"]))) ** (1/5) 

    for i in range(47, 51):
        if tabla2007.loc[51, "P(x+5)"] == 1 or tabla2007.loc[46, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1 , "S(x)"] / tabla2007.loc[46, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2007.loc[51, "P(x+5)"] == 1:
        tabla2007.loc[51, "S(x)"] = tabla2007.loc[50, "S(x)"] * tabla2007.loc[52, "P(x+5)"]
    else: tabla2007.loc[51, "S(x)"] = tabla2007.loc[46, "S(x)"] * tabla2007.loc[51, "P(x+5)"]

    if tabla2007.loc[56, "P(x+5)"] == 1:
        tabla2007.loc[51, "FACTOR ANUAL"] = 1
    else: tabla2007.loc[51, "FACTOR ANUAL"] = (tabla2007.loc[51, "S(x)"] / ((tabla2007.loc[51, "S(x)"] * tabla2007.loc[56, "P(x+5)"]))) ** (1/5) 

    for i in range(52, 56):
        if tabla2007.loc[56, "P(x+5)"] == 1 or tabla2007.loc[51, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1 , "S(x)"] / tabla2007.loc[51, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2007.loc[56, "P(x+5)"] == 1:
        tabla2007.loc[56, "S(x)"] = tabla2007.loc[55, "S(x)"] * tabla2007.loc[56, "P(x+5)"]
    else: tabla2007.loc[56, "S(x)"] = tabla2007.loc[51, "S(x)"] * tabla2007.loc[56, "P(x+5)"]

    for i in range(57, 61):
        if tabla2007.loc[i-1, "P(x+5)"] == 1:
            tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]
        else: tabla2007.loc[i, "S(x)"] = tabla2007.loc[i-1, "S(x)"] * tabla2007.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla2008 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2008] = tabla2008

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2008.loc[5, "P(x+5)"] = GENERACION_2008.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2008.loc[6: 9, "P(x+5)"] = tabla2008.loc[5, "P(x+5)"]
    tabla2008.loc[10, "P(x+5)"] = GENERACION_2008.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2008.loc[11: 14, "P(x+5)"] = tabla2008.loc[10, "P(x+5)"]
    tabla2008.loc[15, "P(x+5)"] = GENERACION_2008.loc[2, "PROBABILIDAD QUINQUENAL"]
    tabla2008.loc[20, "P(x+5)"] = GENERACION_2008.loc[3, "PROBABILIDAD QUINQUENAL"]

    for i in [25, 30, 35, 40, 45, 50, 55, 60]:
        if tabla2008.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2008 <= 1:
            tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2008
        else:
            tabla2008.loc[i, "P(x+5)"] = 1

    for i in range(15, 21):
        if i not in [15, 20]:
            if (tabla2008.loc[15, "P(x+5)"] == 1 or tabla2008.loc[20, "P(x+5)"] == 1):
                if tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5)) >= 1:
                    tabla2008.loc[i, "P(x+5)"] = 1
                else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5))
            else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"]

    for i in range(20, 26):
        if i not in [20, 25]:
            if (tabla2008.loc[20, "P(x+5)"] == 1 or tabla2008.loc[25, "P(x+5)"] == 1):
                if tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5)) >= 1:
                    tabla2008.loc[i, "P(x+5)"] = 1
                else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5))
            else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"]

    for i in range(25, 31):
        if i not in [25, 30]:
            if (tabla2008.loc[25, "P(x+5)"] == 1 or tabla2008.loc[30, "P(x+5)"] == 1):
                if tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5)) >= 1:
                    tabla2008.loc[i, "P(x+5)"] = 1
                else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5))
            else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] 

    for i in range(30, 36):
        if i not in [30, 35]:
            if (tabla2008.loc[30, "P(x+5)"] == 1 or tabla2008.loc[35, "P(x+5)"] == 1):
                if tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5)) >= 1:
                    tabla2008.loc[i, "P(x+5)"] = 1
                else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5))
            else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] 

    for i in range(35, 41):
        if i not in [35, 40]:
            if (tabla2008.loc[35, "P(x+5)"] == 1 or tabla2008.loc[40, "P(x+5)"] == 1):
                if tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5)) >= 1:
                    tabla2008.loc[i, "P(x+5)"] = 1
                else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5))
            else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] 

    for i in range(40, 46):
        if i not in [40, 45]:
            if (tabla2008.loc[40, "P(x+5)"] == 1 or tabla2008.loc[45, "P(x+5)"] == 1):
                if tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5)) >= 1:
                    tabla2008.loc[i, "P(x+5)"] = 1
                else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5))
            else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] 

    for i in range(45, 51):
        if i not in [45, 50]:
            if (tabla2008.loc[45, "P(x+5)"] == 1 or tabla2008.loc[50, "P(x+5)"] == 1):
                if tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5)) >= 1:
                    tabla2008.loc[i, "P(x+5)"] = 1
                else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5))
            else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"]  

    for i in range(50, 56):
        if i not in [50, 55]:
            if (tabla2008.loc[50, "P(x+5)"] == 1 or tabla2008.loc[55, "P(x+5)"] == 1):
                if tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5)) >= 1:
                    tabla2008.loc[i, "P(x+5)"] = 1
                else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5))
            else: tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"]  
            
    for i in range(56, 61):
        if i not in [60]:
            if tabla2008.loc[i-1, "P(x+5)"] == 1:
                tabla2008.loc[i, "P(x+5)"] = 1
            if tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5)) < 1:
                tabla2008.loc[i, "P(x+5)"] = tabla2008.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2008 ** (1/5))
            else: tabla2008.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2008.loc[0, "S(x)"] = 100000
    tabla2008.loc[5, "S(x)"] = tabla2008.loc[0, "S(x)"] * tabla2008.loc[5, "P(x+5)"]

    for i in [10, 15]:
        tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-5, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        
    tabla2008.loc[0, "FACTOR ANUAL"] = (tabla2008.loc[0, "S(x)"] / tabla2008.loc[5, "S(x)"]) ** (1/5)

    for i in [5, 10]:
        tabla2008.loc[i, "FACTOR ANUAL"] = (tabla2008.loc[i, "S(x)"] / tabla2008.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 15):
        if i not in [5, 10]:
            tabla2008.loc[i, "FACTOR ANUAL"] = tabla2008.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 15):
        if i not in [5, 10]:
            if tabla2008.loc[i, "FACTOR ANUAL"] == 1:
                tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] / tabla2008.loc[i, "FACTOR ANUAL"]
            else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] / tabla2008.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2008.loc[15, "P(x+5)"] == 1:
        tabla2008.loc[15, "S(x)"] = tabla2008.loc[14, "S(x)"] * tabla2008.loc[15, "P(x+5)"]
    else: tabla2008.loc[15, "S(x)"] = tabla2008.loc[10, "S(x)"] * tabla2008.loc[15, "P(x+5)"]
    
    if tabla2008.loc[20, "P(x+5)"] == 1:
        tabla2008.loc[15, "FACTOR ANUAL"] = 1
    else: tabla2008.loc[15, "FACTOR ANUAL"] = (tabla2008.loc[15, "S(x)"] / ((tabla2008.loc[15, "S(x)"] * tabla2008.loc[20, "P(x+5)"]))) ** (1/5)    

    for i in range(16, 20):
        if tabla2008.loc[20, "P(x+5)"] == 1:
            tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1 , "S(x)"] / tabla2008.loc[15, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2008.loc[20, "P(x+5)"] == 1:
        tabla2008.loc[20, "S(x)"] = tabla2008.loc[19, "S(x)"] * tabla2008.loc[20, "P(x+5)"]
    else: tabla2008.loc[20, "S(x)"] = tabla2008.loc[15, "S(x)"] * tabla2008.loc[20, "P(x+5)"]
    
    if tabla2008.loc[25, "P(x+5)"] == 1:
        tabla2008.loc[20, "FACTOR ANUAL"] = 1
    else: tabla2008.loc[20, "FACTOR ANUAL"] = (tabla2008.loc[20, "S(x)"] / ((tabla2008.loc[20, "S(x)"] * tabla2008.loc[25, "P(x+5)"]))) ** (1/5)    

    for i in range(21, 25):
        if tabla2008.loc[25, "P(x+5)"] == 1:
            tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1 , "S(x)"] / tabla2008.loc[20, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2008.loc[25, "P(x+5)"] == 1:
        tabla2008.loc[25, "S(x)"] = tabla2008.loc[24, "S(x)"] * tabla2008.loc[25, "P(x+5)"]
    else: tabla2008.loc[25, "S(x)"] = tabla2008.loc[20, "S(x)"] * tabla2008.loc[25, "P(x+5)"]
    
    if tabla2008.loc[30, "P(x+5)"] == 1:
        tabla2008.loc[25, "FACTOR ANUAL"] = 1
    else: tabla2008.loc[25, "FACTOR ANUAL"] = (tabla2008.loc[25, "S(x)"] / ((tabla2008.loc[25, "S(x)"] * tabla2008.loc[30, "P(x+5)"]))) ** (1/5)    

    for i in range(26, 30):
        if tabla2008.loc[30, "P(x+5)"] == 1 or tabla2008.loc[25, "P(x+5)"] == 1:
            tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1 , "S(x)"] / tabla2008.loc[25, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2008.loc[30, "P(x+5)"] == 1:
        tabla2008.loc[30, "S(x)"] = tabla2008.loc[29, "S(x)"] * tabla2008.loc[30, "P(x+5)"]
    else: tabla2008.loc[30, "S(x)"] = tabla2008.loc[25, "S(x)"] * tabla2008.loc[30, "P(x+5)"]
    
    if tabla2008.loc[35, "P(x+5)"] == 1:
        tabla2008.loc[30, "FACTOR ANUAL"] = 1
    else: tabla2008.loc[30, "FACTOR ANUAL"] = (tabla2008.loc[30, "S(x)"] / ((tabla2008.loc[30, "S(x)"] * tabla2008.loc[35, "P(x+5)"]))) ** (1/5)    

    for i in range(31, 35):
        if tabla2008.loc[35, "P(x+5)"] == 1 or tabla2008.loc[30, "P(x+5)"] == 1:
            tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1 , "S(x)"] / tabla2008.loc[30, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2008.loc[35, "P(x+5)"] == 1:
        tabla2008.loc[35, "S(x)"] = tabla2008.loc[34, "S(x)"] * tabla2008.loc[35, "P(x+5)"]
    else: tabla2008.loc[35, "S(x)"] = tabla2008.loc[30, "S(x)"] * tabla2008.loc[35, "P(x+5)"]
    
    if tabla2008.loc[40, "P(x+5)"] == 1:
        tabla2008.loc[35, "FACTOR ANUAL"] = 1
    else: tabla2008.loc[35, "FACTOR ANUAL"] = (tabla2008.loc[35, "S(x)"] / ((tabla2008.loc[35, "S(x)"] * tabla2008.loc[40, "P(x+5)"]))) ** (1/5)    

    for i in range(36, 40):
        if tabla2008.loc[40, "P(x+5)"] == 1 or tabla2008.loc[35, "P(x+5)"] == 1:
            tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1 , "S(x)"] / tabla2008.loc[35, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2008.loc[40, "P(x+5)"] == 1:
        tabla2008.loc[40, "S(x)"] = tabla2008.loc[39, "S(x)"] * tabla2008.loc[40, "P(x+5)"]
    else: tabla2008.loc[40, "S(x)"] = tabla2008.loc[35, "S(x)"] * tabla2008.loc[40, "P(x+5)"]

    #i+5   
    if tabla2008.loc[45, "P(x+5)"] == 1:
        tabla2008.loc[40, "FACTOR ANUAL"] = 1
    else: tabla2008.loc[40, "FACTOR ANUAL"] = (tabla2008.loc[40, "S(x)"] / ((tabla2008.loc[40, "S(x)"] * tabla2008.loc[45, "P(x+5)"]))) ** (1/5)    

    for i in range(41, 45):
        if tabla2008.loc[40, "P(x+5)"] == 1 or tabla2008.loc[45, "P(x+5)"] == 1:
            tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1 , "S(x)"] / tabla2008.loc[40, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2008.loc[45, "P(x+5)"] == 1:
        tabla2008.loc[45, "S(x)"] = tabla2008.loc[44, "S(x)"] * tabla2008.loc[45, "P(x+5)"]
    else: tabla2008.loc[45, "S(x)"] = tabla2008.loc[40, "S(x)"] * tabla2008.loc[45, "P(x+5)"]
    
    if tabla2008.loc[50, "P(x+5)"] == 1:
        tabla2008.loc[45, "FACTOR ANUAL"] = 1
    else: tabla2008.loc[45, "FACTOR ANUAL"] = (tabla2008.loc[45, "S(x)"] / ((tabla2008.loc[45, "S(x)"] * tabla2008.loc[50, "P(x+5)"]))) ** (1/5)    

    for i in range(46, 50):
        if tabla2008.loc[50, "P(x+5)"] == 1 or tabla2008.loc[45, "P(x+5)"] == 1:
            tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1 , "S(x)"] / tabla2008.loc[45, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2008.loc[50, "P(x+5)"] == 1:
        tabla2008.loc[50, "S(x)"] = tabla2008.loc[49, "S(x)"] * tabla2008.loc[50, "P(x+5)"]
    else: tabla2008.loc[50, "S(x)"] = tabla2008.loc[45, "S(x)"] * tabla2008.loc[50, "P(x+5)"]

    if tabla2008.loc[55, "P(x+5)"] == 1:
        tabla2008.loc[50, "FACTOR ANUAL"] = 1
    else: tabla2008.loc[50, "FACTOR ANUAL"] = (tabla2008.loc[50, "S(x)"] / ((tabla2008.loc[50, "S(x)"] * tabla2008.loc[55, "P(x+5)"]))) ** (1/5) 

    for i in range(51, 55):
        if tabla2008.loc[55, "P(x+5)"] == 1 or tabla2008.loc[50, "P(x+5)"] == 1:
            tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1 , "S(x)"] / tabla2008.loc[50, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    

    if tabla2008.loc[55, "P(x+5)"] == 1:
        tabla2008.loc[55, "S(x)"] = tabla2008.loc[54, "S(x)"] * tabla2008.loc[55, "P(x+5)"]
    else: tabla2008.loc[55, "S(x)"] = tabla2008.loc[50, "S(x)"] * tabla2008.loc[55, "P(x+5)"]

    if tabla2008.loc[60, "P(x+5)"] == 1:
        tabla2008.loc[55, "FACTOR ANUAL"] = 1
    else: tabla2008.loc[55, "FACTOR ANUAL"] = (tabla2008.loc[55, "S(x)"] / ((tabla2008.loc[55, "S(x)"] * tabla2008.loc[60, "P(x+5)"]))) ** (1/5) 

    for i in range(56, 60):
        if tabla2008.loc[60, "P(x+5)"] == 1 or tabla2008.loc[55, "P(x+5)"] == 1:
            tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1, "S(x)"] * tabla2008.loc[i, "P(x+5)"]
        else: tabla2008.loc[i, "S(x)"] = tabla2008.loc[i-1 , "S(x)"] / tabla2008.loc[55, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2008.loc[60, "P(x+5)"] == 1:
        tabla2008.loc[60, "S(x)"] = tabla2008.loc[60, "P(x+5)"] * tabla2008.loc[59, "S(x)"]
    else: tabla2008.loc[60, "S(x)"] = tabla2008.loc[60, "P(x+5)"] * tabla2008.loc[55, "S(x)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla2009 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2009] = tabla2009

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2009.loc[4, "P(x+5)"] = GENERACION_2009.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2009
    tabla2009.loc[5: 8, "P(x+5)"] = tabla2009.loc[4, "P(x+5)"]
    tabla2009.loc[9, "P(x+5)"] = GENERACION_2009.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2009.loc[14, "P(x+5)"] = GENERACION_2009.loc[1, "PROBABILIDAD QUINQUENAL"]

    for i in [19, 24, 29, 34, 39, 44, 49, 54, 59]:
        if tabla2009.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2009 <= 1:
            tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2009
        else:
            tabla2009.loc[i, "P(x+5)"] = 1

    for i in range(9, 15):
        if i not in [9, 14]:
            if (tabla2009.loc[9, "P(x+5)"] == 1 or tabla2009.loc[14, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"]

    for i in range(14, 20):
        if i not in [14, 19]:
            if (tabla2009.loc[14, "P(x+5)"] == 1 or tabla2009.loc[19, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"]

    for i in range(19, 25):
        if i not in [19, 24]:
            if (tabla2009.loc[19, "P(x+5)"] == 1 or tabla2009.loc[24, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"]

    for i in range(24, 30):
        if i not in [24, 29]:
            if (tabla2009.loc[24, "P(x+5)"] == 1 or tabla2009.loc[29, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] 

    for i in range(29, 35):
        if i not in [29, 34]:
            if (tabla2009.loc[29, "P(x+5)"] == 1 or tabla2009.loc[34, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] 

    for i in range(34, 40):
        if i not in [34, 39]:
            if (tabla2009.loc[34, "P(x+5)"] == 1 or tabla2009.loc[39, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] 

    for i in range(39, 45):
        if i not in [39, 44]:
            if (tabla2009.loc[39, "P(x+5)"] == 1 or tabla2009.loc[44, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] 

    for i in range(44, 50):
        if i not in [44, 49]:
            if (tabla2009.loc[44, "P(x+5)"] == 1 or tabla2009.loc[49, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"]  

    for i in range(49, 55):
        if i not in [49, 54]:
            if (tabla2009.loc[49, "P(x+5)"] == 1 or tabla2009.loc[54, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"]  
            
    for i in range(54, 60):
        if i not in [54, 59]:
            if (tabla2009.loc[54, "P(x+5)"] == 1 or tabla2009.loc[59, "P(x+5)"] == 1):
                if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) >= 1:
                    tabla2009.loc[i, "P(x+5)"] = 1
                else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
            else: tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"]

    for i in range(60, 61):
        if tabla2009.loc[i-1, "P(x+5)"] == 1:
            tabla2009.loc[i, "P(x+5)"] = 1
        if tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5)) < 1:
            tabla2009.loc[i, "P(x+5)"] = tabla2009.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2009 ** (1/5))
        else: tabla2009.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2009.loc[0, "S(x)"] = 100000
    tabla2009.loc[4, "S(x)"] = tabla2009.loc[0, "S(x)"] * tabla2009.loc[4, "P(x+5)"]

    for i in [9]:
        tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-5, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        
    tabla2009.loc[0, "FACTOR ANUAL"] = (tabla2009.loc[0, "S(x)"] / tabla2009.loc[4, "S(x)"]) ** (1/4)

    for i in [4]:
        tabla2009.loc[i, "FACTOR ANUAL"] = (tabla2009.loc[i, "S(x)"] / tabla2009.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 9):
        if i not in [4]:
            tabla2009.loc[i, "FACTOR ANUAL"] = tabla2009.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 9):
        if i not in [4]:
            if tabla2009.loc[i, "FACTOR ANUAL"] == 1:
                tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] / tabla2009.loc[i, "FACTOR ANUAL"]
            else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] / tabla2009.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[9, "P(x+5)"] == 1:
        tabla2009.loc[9, "S(x)"] = tabla2009.loc[8, "S(x)"] * tabla2009.loc[9, "P(x+5)"]
    else: tabla2009.loc[9, "S(x)"] = tabla2009.loc[4, "S(x)"] * tabla2009.loc[9, "P(x+5)"]
    
    if tabla2009.loc[14, "P(x+5)"] == 1:
        tabla2009.loc[9, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[9, "FACTOR ANUAL"] = (tabla2009.loc[9, "S(x)"] / ((tabla2009.loc[9, "S(x)"] * tabla2009.loc[14, "P(x+5)"]))) ** (1/5)    

    for i in range(10, 14):
        if tabla2009.loc[14, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[9, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[14, "P(x+5)"] == 1:
        tabla2009.loc[14, "S(x)"] = tabla2009.loc[13, "S(x)"] * tabla2009.loc[14, "P(x+5)"]
    else: tabla2009.loc[14, "S(x)"] = tabla2009.loc[9, "S(x)"] * tabla2009.loc[14, "P(x+5)"]
    
    if tabla2009.loc[19, "P(x+5)"] == 1:
        tabla2009.loc[14, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[14, "FACTOR ANUAL"] = (tabla2009.loc[14, "S(x)"] / ((tabla2009.loc[14, "S(x)"] * tabla2009.loc[19, "P(x+5)"]))) ** (1/5)    

    for i in range(15, 19):
        if tabla2009.loc[19, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[14, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[19, "P(x+5)"] == 1:
        tabla2009.loc[19, "S(x)"] = tabla2009.loc[18, "S(x)"] * tabla2009.loc[19, "P(x+5)"]
    else: tabla2009.loc[19, "S(x)"] = tabla2009.loc[14, "S(x)"] * tabla2009.loc[19, "P(x+5)"]
    
    if tabla2009.loc[24, "P(x+5)"] == 1:
        tabla2009.loc[19, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[19, "FACTOR ANUAL"] = (tabla2009.loc[19, "S(x)"] / ((tabla2009.loc[19, "S(x)"] * tabla2009.loc[24, "P(x+5)"]))) ** (1/5)    

    for i in range(20, 24):
        if tabla2009.loc[24, "P(x+5)"] == 1 or tabla2009.loc[19, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[19, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[24, "P(x+5)"] == 1:
        tabla2009.loc[24, "S(x)"] = tabla2009.loc[23, "S(x)"] * tabla2009.loc[24, "P(x+5)"]
    else: tabla2009.loc[24, "S(x)"] = tabla2009.loc[19, "S(x)"] * tabla2009.loc[24, "P(x+5)"]
    
    if tabla2009.loc[29, "P(x+5)"] == 1:
        tabla2009.loc[24, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[24, "FACTOR ANUAL"] = (tabla2009.loc[24, "S(x)"] / ((tabla2009.loc[24, "S(x)"] * tabla2009.loc[29, "P(x+5)"]))) ** (1/5)    

    for i in range(25, 29):
        if tabla2009.loc[29, "P(x+5)"] == 1 or tabla2009.loc[24, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[24, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[29, "P(x+5)"] == 1:
        tabla2009.loc[29, "S(x)"] = tabla2009.loc[28, "S(x)"] * tabla2009.loc[29, "P(x+5)"]
    else: tabla2009.loc[29, "S(x)"] = tabla2009.loc[24, "S(x)"] * tabla2009.loc[29, "P(x+5)"]
    
    if tabla2009.loc[34, "P(x+5)"] == 1:
        tabla2009.loc[29, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[29, "FACTOR ANUAL"] = (tabla2009.loc[29, "S(x)"] / ((tabla2009.loc[29, "S(x)"] * tabla2009.loc[34, "P(x+5)"]))) ** (1/5)    

    for i in range(30, 34):
        if tabla2009.loc[34, "P(x+5)"] == 1 or tabla2009.loc[29, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[29, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[34, "P(x+5)"] == 1:
        tabla2009.loc[34, "S(x)"] = tabla2009.loc[33, "S(x)"] * tabla2009.loc[34, "P(x+5)"]
    else: tabla2009.loc[34, "S(x)"] = tabla2009.loc[29, "S(x)"] * tabla2009.loc[34, "P(x+5)"]
    
    if tabla2009.loc[39, "P(x+5)"] == 1:
        tabla2009.loc[34, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[34, "FACTOR ANUAL"] = (tabla2009.loc[34, "S(x)"] / ((tabla2009.loc[34, "S(x)"] * tabla2009.loc[39, "P(x+5)"]))) ** (1/5)    

    for i in range(35, 39):
        if tabla2009.loc[39, "P(x+5)"] == 1 or tabla2009.loc[34, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[34, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2009.loc[39, "P(x+5)"] == 1:
        tabla2009.loc[39, "S(x)"] = tabla2009.loc[38, "S(x)"] * tabla2009.loc[39, "P(x+5)"]
    else: tabla2009.loc[39, "S(x)"] = tabla2009.loc[34, "S(x)"] * tabla2009.loc[39, "P(x+5)"]

    #i+5   
    if tabla2009.loc[44, "P(x+5)"] == 1:
        tabla2009.loc[39, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[39, "FACTOR ANUAL"] = (tabla2009.loc[39, "S(x)"] / ((tabla2009.loc[39, "S(x)"] * tabla2009.loc[44, "P(x+5)"]))) ** (1/5)    

    for i in range(40, 44):
        if tabla2009.loc[44, "P(x+5)"] == 1 or tabla2009.loc[39, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[39, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[44, "P(x+5)"] == 1:
        tabla2009.loc[44, "S(x)"] = tabla2009.loc[43, "S(x)"] * tabla2009.loc[44, "P(x+5)"]
    else: tabla2009.loc[44, "S(x)"] = tabla2009.loc[39, "S(x)"] * tabla2009.loc[44, "P(x+5)"]
    
    if tabla2009.loc[49, "P(x+5)"] == 1:
        tabla2009.loc[44, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[44, "FACTOR ANUAL"] = (tabla2009.loc[44, "S(x)"] / ((tabla2009.loc[44, "S(x)"] * tabla2009.loc[49, "P(x+5)"]))) ** (1/5)    

    for i in range(45, 49):
        if tabla2009.loc[49, "P(x+5)"] == 1 or tabla2009.loc[44, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[44, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[49, "P(x+5)"] == 1:
        tabla2009.loc[49, "S(x)"] = tabla2009.loc[48, "S(x)"] * tabla2009.loc[49, "P(x+5)"]
    else: tabla2009.loc[49, "S(x)"] = tabla2009.loc[44, "S(x)"] * tabla2009.loc[49, "P(x+5)"]

    if tabla2009.loc[54, "P(x+5)"] == 1:
        tabla2009.loc[49, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[49, "FACTOR ANUAL"] = (tabla2009.loc[49, "S(x)"] / ((tabla2009.loc[49, "S(x)"] * tabla2009.loc[54, "P(x+5)"]))) ** (1/5) 

    for i in range(50, 54):
        if tabla2009.loc[54, "P(x+5)"] == 1 or tabla2009.loc[49, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[49, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[54, "P(x+5)"] == 1:
        tabla2009.loc[54, "S(x)"] = tabla2009.loc[53, "S(x)"] * tabla2009.loc[54, "P(x+5)"]
    else: tabla2009.loc[54, "S(x)"] = tabla2009.loc[49, "S(x)"] * tabla2009.loc[54, "P(x+5)"]

    if tabla2009.loc[59, "P(x+5)"] == 1:
        tabla2009.loc[54, "FACTOR ANUAL"] = 1
    else: tabla2009.loc[54, "FACTOR ANUAL"] = (tabla2009.loc[54, "S(x)"] / ((tabla2009.loc[54, "S(x)"] * tabla2009.loc[59, "P(x+5)"]))) ** (1/5) 

    for i in range(55, 59):
        if tabla2009.loc[59, "P(x+5)"] == 1 or tabla2009.loc[54, "P(x+5)"] == 1:
            tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1 , "S(x)"] / tabla2009.loc[54, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2009.loc[59, "P(x+5)"] == 1:
        tabla2009.loc[59, "S(x)"] = tabla2009.loc[58, "S(x)"] * tabla2009.loc[59, "P(x+5)"]
    else: tabla2009.loc[59, "S(x)"] = tabla2009.loc[54, "S(x)"] * tabla2009.loc[59, "P(x+5)"]

    for i in range(59, 61):
        if i not in [59]:
            if tabla2009.loc[i-1, "P(x+5)"] == 1:
                tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
            else: tabla2009.loc[i, "S(x)"] = tabla2009.loc[i-1, "S(x)"] * tabla2009.loc[i, "P(x+5)"]
        
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla2010 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2010] = tabla2010

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2010.loc[3, "P(x+5)"] = GENERACION_2010.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2010
    tabla2010.loc[4: 7, "P(x+5)"] = tabla2010.loc[3, "P(x+5)"]
    tabla2010.loc[8, "P(x+5)"] = GENERACION_2010.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2010.loc[13, "P(x+5)"] = GENERACION_2010.loc[1, "PROBABILIDAD QUINQUENAL"]

    for i in [18, 23, 28, 33, 38, 43, 48, 53, 58]:
        if tabla2010.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2010 <= 1:
            tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2010
        else:
            tabla2010.loc[i, "P(x+5)"] = 1

    for i in range(8, 14):
        if i not in [8, 13]:
            if (tabla2010.loc[8, "P(x+5)"] == 1 or tabla2010.loc[13, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"]
        
    for i in range(13, 19):
        if i not in [13, 18]:
            if (tabla2010.loc[13, "P(x+5)"] == 1 or tabla2010.loc[18, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"]

    for i in range(18, 24):
        if i not in [18, 23]:
            if (tabla2010.loc[18, "P(x+5)"] == 1 or tabla2010.loc[23, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"]

    for i in range(23, 29):
        if i not in [23, 28]:
            if (tabla2010.loc[23, "P(x+5)"] == 1 or tabla2010.loc[28, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] 
            
    for i in range(28, 34):
        if i not in [28, 33]:
            if (tabla2010.loc[28, "P(x+5)"] == 1 or tabla2010.loc[33, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"]       

    for i in range(33, 39):
        if i not in [33, 38]:
            if (tabla2010.loc[33, "P(x+5)"] == 1 or tabla2010.loc[38, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] 
            
    for i in range(38, 44):
        if i not in [38, 43]:
            if (tabla2010.loc[38, "P(x+5)"] == 1 or tabla2010.loc[43, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"]  

    for i in range(43, 49):
        if i not in [43, 48]:
            if (tabla2010.loc[43, "P(x+5)"] == 1 or tabla2010.loc[48, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"]  

    for i in range(48, 54):
        if i not in [48, 53]:
            if (tabla2010.loc[48, "P(x+5)"] == 1 or tabla2010.loc[53, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"]  
            
    for i in range(53, 59):
        if i not in [53, 58]:
            if (tabla2010.loc[53, "P(x+5)"] == 1 or tabla2010.loc[58, "P(x+5)"] == 1):
                if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) >= 1:
                    tabla2010.loc[i, "P(x+5)"] = 1
                else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
            else: tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"]

    for i in range(59, 61):
        if tabla2010.loc[i-1, "P(x+5)"] == 1:
            tabla2010.loc[i, "P(x+5)"] = 1
        if tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5)) < 1:
            tabla2010.loc[i, "P(x+5)"] = tabla2010.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2010 ** (1/5))
        else: tabla2010.loc[i, "P(x+5)"] = 1
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2010.loc[0, "S(x)"] = 100000
    tabla2010.loc[3, "S(x)"] = tabla2010.loc[0, "S(x)"] * tabla2010.loc[3, "P(x+5)"]

    for i in [8]:
        tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-5, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        
    tabla2010.loc[0, "FACTOR ANUAL"] = (tabla2010.loc[0, "S(x)"] / tabla2010.loc[3, "S(x)"]) ** (1/3)

    for i in [3]:
        tabla2010.loc[i, "FACTOR ANUAL"] = (tabla2010.loc[i, "S(x)"] / tabla2010.loc[i+5, "S(x)"]) ** (1/5)

    for i in range(1, 8):
        if i not in [3]:
            tabla2010.loc[i, "FACTOR ANUAL"] = tabla2010.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 8):
        if i not in [3]:
            if tabla2010.loc[i, "FACTOR ANUAL"] == 1:
                tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] / tabla2010.loc[i, "FACTOR ANUAL"]
            else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] / tabla2010.loc[i, "FACTOR ANUAL"]
            
            #-----------------------------------------------------------------INTERVALO 8        
    if tabla2010.loc[8, "P(x+5)"] == 1:
        tabla2010.loc[8, "S(x)"] = tabla2010.loc[7, "S(x)"] * tabla2010.loc[8, "P(x+5)"]
    else: tabla2010.loc[8, "S(x)"] = tabla2010.loc[3, "S(x)"] * tabla2010.loc[8, "P(x+5)"]

    if tabla2010.loc[13, "P(x+5)"] == 1:
        tabla2010.loc[8, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[8, "FACTOR ANUAL"] = (tabla2010.loc[8, "S(x)"] / ((tabla2010.loc[8, "S(x)"] * tabla2010.loc[13, "P(x+5)"]))) ** (1/5)
    
    for i in range(9, 13):
        if tabla2010.loc[13, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[8, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 13        
    if tabla2010.loc[13, "P(x+5)"] == 1:
        tabla2010.loc[13, "S(x)"] = tabla2010.loc[12, "S(x)"] * tabla2010.loc[13, "P(x+5)"]
    else: tabla2010.loc[13, "S(x)"] = tabla2010.loc[8, "S(x)"] * tabla2010.loc[13, "P(x+5)"]

    if tabla2010.loc[18, "P(x+5)"] == 1:
        tabla2010.loc[13, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[13, "FACTOR ANUAL"] = (tabla2010.loc[13, "S(x)"] / ((tabla2010.loc[13, "S(x)"] * tabla2010.loc[18, "P(x+5)"]))) ** (1/5)
    
    for i in range(14, 18):
        if tabla2010.loc[18, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[13, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 18        
    if tabla2010.loc[18, "P(x+5)"] == 1:
        tabla2010.loc[18, "S(x)"] = tabla2010.loc[17, "S(x)"] * tabla2010.loc[18, "P(x+5)"]
    else: tabla2010.loc[18, "S(x)"] = tabla2010.loc[13, "S(x)"] * tabla2010.loc[18, "P(x+5)"]

    if tabla2010.loc[23, "P(x+5)"] == 1:
        tabla2010.loc[18, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[18, "FACTOR ANUAL"] = (tabla2010.loc[18, "S(x)"] / ((tabla2010.loc[18, "S(x)"] * tabla2010.loc[23, "P(x+5)"]))) ** (1/5)
    
    for i in range(19, 23):
        if tabla2010.loc[23, "P(x+5)"] == 1 or tabla2010.loc[18, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[18, "FACTOR ANUAL"]
        
            #-----------------------------------------------------------------INTERVALO 23        
    if tabla2010.loc[23, "P(x+5)"] == 1:
        tabla2010.loc[23, "S(x)"] = tabla2010.loc[22, "S(x)"] * tabla2010.loc[23, "P(x+5)"]
    else: tabla2010.loc[23, "S(x)"] = tabla2010.loc[18, "S(x)"] * tabla2010.loc[23, "P(x+5)"]

    if tabla2010.loc[28, "P(x+5)"] == 1:
        tabla2010.loc[23, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[23, "FACTOR ANUAL"] = (tabla2010.loc[23, "S(x)"] / ((tabla2010.loc[23, "S(x)"] * tabla2010.loc[28, "P(x+5)"]))) ** (1/5)
    
    for i in range(24, 28):
        if tabla2010.loc[28, "P(x+5)"] == 1 or tabla2010.loc[23, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[23, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 28
    if tabla2010.loc[28, "P(x+5)"] == 1:
        tabla2010.loc[28, "S(x)"] = tabla2010.loc[27, "S(x)"] * tabla2010.loc[28, "P(x+5)"]
    else: tabla2010.loc[28, "S(x)"] = tabla2010.loc[23, "S(x)"] * tabla2010.loc[28, "P(x+5)"]

    if tabla2010.loc[33, "P(x+5)"] == 1:
        tabla2010.loc[28, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[28, "FACTOR ANUAL"] = (tabla2010.loc[28, "S(x)"] / ((tabla2010.loc[28, "S(x)"] * tabla2010.loc[33, "P(x+5)"]))) ** (1/5)
    
    for i in range(29, 33):
        if tabla2010.loc[33, "P(x+5)"] == 1 or tabla2010.loc[28, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[28, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 33
    if tabla2010.loc[33, "P(x+5)"] == 1:
        tabla2010.loc[33, "S(x)"] = tabla2010.loc[32, "S(x)"] * tabla2010.loc[33, "P(x+5)"]
    else: tabla2010.loc[33, "S(x)"] = tabla2010.loc[28, "S(x)"] * tabla2010.loc[33, "P(x+5)"]
    
    if tabla2010.loc[38, "P(x+5)"] == 1:
        tabla2010.loc[33, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[33, "FACTOR ANUAL"] = (tabla2010.loc[33, "S(x)"] / ((tabla2010.loc[33, "S(x)"] * tabla2010.loc[38, "P(x+5)"]))) ** (1/5)    

    for i in range(34, 38):
        if tabla2010.loc[38, "P(x+5)"] == 1 or tabla2010.loc[33, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[33, "FACTOR ANUAL"]
        
            #-----------------------------------------------------------------INTERVALO 38
    if tabla2010.loc[38, "P(x+5)"] == 1:
        tabla2010.loc[38, "S(x)"] = tabla2010.loc[37, "S(x)"] * tabla2010.loc[38, "P(x+5)"]
    else: tabla2010.loc[38, "S(x)"] = tabla2010.loc[33, "S(x)"] * tabla2010.loc[38, "P(x+5)"]

    #i+5   
    if tabla2010.loc[43, "P(x+5)"] == 1:
        tabla2010.loc[38, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[38, "FACTOR ANUAL"] = (tabla2010.loc[38, "S(x)"] / ((tabla2010.loc[38, "S(x)"] * tabla2010.loc[43, "P(x+5)"]))) ** (1/5)    

    for i in range(39, 43):
        if tabla2010.loc[43, "P(x+5)"] == 1 or tabla2010.loc[38, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[38, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 43
    if tabla2010.loc[43, "P(x+5)"] == 1:
        tabla2010.loc[43, "S(x)"] = tabla2010.loc[42, "S(x)"] * tabla2010.loc[43, "P(x+5)"]
    else: tabla2010.loc[43, "S(x)"] = tabla2010.loc[38, "S(x)"] * tabla2010.loc[43, "P(x+5)"]

    #i+5   
    if tabla2010.loc[48, "P(x+5)"] == 1:
        tabla2010.loc[43, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[43, "FACTOR ANUAL"] = (tabla2010.loc[43, "S(x)"] / ((tabla2010.loc[43, "S(x)"] * tabla2010.loc[48, "P(x+5)"]))) ** (1/5)    

    for i in range(44, 48):
        if tabla2010.loc[48, "P(x+5)"] == 1 or tabla2010.loc[43, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[43, "FACTOR ANUAL"]

            #-----------------------------------------------------------------INTERVALO 48
    if tabla2010.loc[48, "P(x+5)"] == 1:
        tabla2010.loc[48, "S(x)"] = tabla2010.loc[47, "S(x)"] * tabla2010.loc[48, "P(x+5)"]
    else: tabla2010.loc[48, "S(x)"] = tabla2010.loc[43, "S(x)"] * tabla2010.loc[48, "P(x+5)"]

    #i+5   
    if tabla2010.loc[53, "P(x+5)"] == 1:
        tabla2010.loc[48, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[48, "FACTOR ANUAL"] = (tabla2010.loc[48, "S(x)"] / ((tabla2010.loc[48, "S(x)"] * tabla2010.loc[53, "P(x+5)"]))) ** (1/5)    

    for i in range(49, 53):
        if tabla2010.loc[53, "P(x+5)"] == 1 or tabla2010.loc[48, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[48, "FACTOR ANUAL"]
            
            #-----------------------------------------------------------------INTERVALO 53
    if tabla2010.loc[53, "P(x+5)"] == 1:
        tabla2010.loc[53, "S(x)"] = tabla2010.loc[52, "S(x)"] * tabla2010.loc[53, "P(x+5)"]
    else: tabla2010.loc[53, "S(x)"] = tabla2010.loc[48, "S(x)"] * tabla2010.loc[53, "P(x+5)"]

    #i+5   
    if tabla2010.loc[58, "P(x+5)"] == 1:
        tabla2010.loc[53, "FACTOR ANUAL"] = 1
    else: tabla2010.loc[53, "FACTOR ANUAL"] = (tabla2010.loc[53, "S(x)"] / ((tabla2010.loc[53, "S(x)"] * tabla2010.loc[58, "P(x+5)"]))) ** (1/5)    

    for i in range(54, 58):
        if tabla2010.loc[58, "P(x+5)"] == 1 or tabla2010.loc[53, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1 , "S(x)"] / tabla2010.loc[53, "FACTOR ANUAL"]    

            #-----------------------------------------------------------------INTERVALO 58
    if tabla2010.loc[58, "P(x+5)"] == 1:
        tabla2010.loc[58, "S(x)"] = tabla2010.loc[57, "S(x)"] * tabla2010.loc[58, "P(x+5)"]
    else: tabla2010.loc[58, "S(x)"] = tabla2010.loc[53, "S(x)"] * tabla2010.loc[58, "P(x+5)"]
            
    for i in range(59, 61):
        if tabla2010.loc[i-1, "P(x+5)"] == 1:
            tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]
        else: tabla2010.loc[i, "S(x)"] = tabla2010.loc[i-1, "S(x)"] * tabla2010.loc[i, "P(x+5)"]        

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tabla2011 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2011] = tabla2011

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2011.loc[2, "P(x+5)"] = GENERACION_2011.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2011
    tabla2011.loc[3: 6, "P(x+5)"] = tabla2011.loc[2, "P(x+5)"]
    tabla2011.loc[7, "P(x+5)"] = GENERACION_2011.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2011.loc[12, "P(x+5)"] = GENERACION_2011.loc[1, "PROBABILIDAD QUINQUENAL"]
        
    for i in [17, 22, 27, 32, 37, 42, 47, 52, 57]:
        if tabla2011.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2011 <= 1:
            tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2011
        else:
            tabla2011.loc[i, "P(x+5)"] = 1

    for i in range(7, 13):
        if i not in [7, 12]:
            if (tabla2011.loc[7, "P(x+5)"] == 1 or tabla2011.loc[12, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"]

    for i in range(12, 18):
        if i not in [12, 17]:
            if (tabla2011.loc[12, "P(x+5)"] == 1 or tabla2011.loc[17, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"]

    for i in range(17, 23):
        if i not in [17, 22]:
            if (tabla2011.loc[17, "P(x+5)"] == 1 or tabla2011.loc[22, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"]

    for i in range(22, 28):
        if i not in [22, 27]:
            if (tabla2011.loc[22, "P(x+5)"] == 1 or tabla2011.loc[27, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"]
            
    for i in range(27, 33):
        if i not in [27, 32]:
            if (tabla2011.loc[27, "P(x+5)"] == 1 or tabla2011.loc[32, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"]       

    for i in range(32, 38):
        if i not in [32, 37]:
            if (tabla2011.loc[32, "P(x+5)"] == 1 or tabla2011.loc[37, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] 
            
    for i in range(37, 43):
        if i not in [37, 42]:
            if (tabla2011.loc[37, "P(x+5)"] == 1 or tabla2011.loc[42, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"]  

    for i in range(42, 48):
        if i not in [42, 47]:
            if (tabla2011.loc[42, "P(x+5)"] == 1 or tabla2011.loc[47, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"]  

    for i in range(47, 53):
        if i not in [47, 52]:
            if (tabla2011.loc[47, "P(x+5)"] == 1 or tabla2011.loc[52, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"]  
            
    for i in range(52, 58):
        if i not in [52, 57]:
            if (tabla2011.loc[52, "P(x+5)"] == 1 or tabla2011.loc[57, "P(x+5)"] == 1):
                if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) >= 1:
                    tabla2011.loc[i, "P(x+5)"] = 1
                else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
            else: tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"]

    for i in range(58, 61):
        if tabla2011.loc[i-1, "P(x+5)"] == 1:
            tabla2011.loc[i, "P(x+5)"] = 1
        if tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5)) < 1:
            tabla2011.loc[i, "P(x+5)"] = tabla2011.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2011 ** (1/5))
        else: tabla2011.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2011.loc[0, "S(x)"] = 100000
    tabla2011.loc[2, "S(x)"] = tabla2011.loc[0, "S(x)"] * tabla2011.loc[2, "P(x+5)"]

    for i in [7]:
        tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-5, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        
    tabla2011.loc[0, "FACTOR ANUAL"] = (tabla2011.loc[0, "S(x)"] / tabla2011.loc[2, "S(x)"]) ** (1/2)

    for i in [2]:
        tabla2011.loc[i, "FACTOR ANUAL"] = (tabla2011.loc[i, "S(x)"] / tabla2011.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 7):
        if i not in [2]:
            tabla2011.loc[i, "FACTOR ANUAL"] = tabla2011.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 7):
        if i not in [2]:
            if tabla2011.loc[i, "FACTOR ANUAL"] == 1:
                tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] / tabla2011.loc[i, "FACTOR ANUAL"]
            else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] / tabla2011.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[7, "P(x+5)"] == 1:
        tabla2011.loc[7, "S(x)"] = tabla2011.loc[6, "S(x)"] * tabla2011.loc[7, "P(x+5)"]
    else: tabla2011.loc[7, "S(x)"] = tabla2011.loc[2, "S(x)"] * tabla2011.loc[7, "P(x+5)"]
    
    if tabla2011.loc[12, "P(x+5)"] == 1:
        tabla2011.loc[7, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[7, "FACTOR ANUAL"] = (tabla2011.loc[7, "S(x)"] / ((tabla2011.loc[7, "S(x)"] * tabla2011.loc[12, "P(x+5)"]))) ** (1/5)    

    for i in range(8, 12):
        if tabla2011.loc[12, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[7, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[12, "P(x+5)"] == 1:
        tabla2011.loc[12, "S(x)"] = tabla2011.loc[11, "S(x)"] * tabla2011.loc[12, "P(x+5)"]
    else: tabla2011.loc[12, "S(x)"] = tabla2011.loc[7, "S(x)"] * tabla2011.loc[12, "P(x+5)"]
    
    if tabla2011.loc[17, "P(x+5)"] == 1:
        tabla2011.loc[12, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[12, "FACTOR ANUAL"] = (tabla2011.loc[12, "S(x)"] / ((tabla2011.loc[12, "S(x)"] * tabla2011.loc[17, "P(x+5)"]))) ** (1/5)    

    for i in range(13, 17):
        if tabla2011.loc[17, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[12, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[17, "P(x+5)"] == 1:
        tabla2011.loc[17, "S(x)"] = tabla2011.loc[16, "S(x)"] * tabla2011.loc[17, "P(x+5)"]
    else: tabla2011.loc[17, "S(x)"] = tabla2011.loc[12, "S(x)"] * tabla2011.loc[17, "P(x+5)"]
    
    if tabla2011.loc[22, "P(x+5)"] == 1:
        tabla2011.loc[17, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[17, "FACTOR ANUAL"] = (tabla2011.loc[17, "S(x)"] / ((tabla2011.loc[17, "S(x)"] * tabla2011.loc[22, "P(x+5)"]))) ** (1/5)    

    for i in range(18, 22):
        if tabla2011.loc[17, "P(x+5)"] == 1 or tabla2011.loc[22, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[17, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[22, "P(x+5)"] == 1:
        tabla2011.loc[22, "S(x)"] = tabla2011.loc[21, "S(x)"] * tabla2011.loc[22, "P(x+5)"]
    else: tabla2011.loc[22, "S(x)"] = tabla2011.loc[17, "S(x)"] * tabla2011.loc[22, "P(x+5)"]
    
    if tabla2011.loc[27, "P(x+5)"] == 1:
        tabla2011.loc[22, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[22, "FACTOR ANUAL"] = (tabla2011.loc[22, "S(x)"] / ((tabla2011.loc[22, "S(x)"] * tabla2011.loc[27, "P(x+5)"]))) ** (1/5)    

    for i in range(23, 27):
        if tabla2011.loc[27, "P(x+5)"] == 1 or tabla2011.loc[22, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[22, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[27, "P(x+5)"] == 1:
        tabla2011.loc[27, "S(x)"] = tabla2011.loc[26, "S(x)"] * tabla2011.loc[27, "P(x+5)"]
    else: tabla2011.loc[27, "S(x)"] = tabla2011.loc[22, "S(x)"] * tabla2011.loc[27, "P(x+5)"]
    
    if tabla2011.loc[32, "P(x+5)"] == 1:
        tabla2011.loc[27, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[27, "FACTOR ANUAL"] = (tabla2011.loc[27, "S(x)"] / ((tabla2011.loc[27, "S(x)"] * tabla2011.loc[32, "P(x+5)"]))) ** (1/5)    

    for i in range(28, 32):
        if tabla2011.loc[32, "P(x+5)"] == 1 or tabla2011.loc[27, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[27, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[32, "P(x+5)"] == 1:
        tabla2011.loc[32, "S(x)"] = tabla2011.loc[31, "S(x)"] * tabla2011.loc[32, "P(x+5)"]
    else: tabla2011.loc[32, "S(x)"] = tabla2011.loc[27, "S(x)"] * tabla2011.loc[32, "P(x+5)"]
    
    if tabla2011.loc[37, "P(x+5)"] == 1:
        tabla2011.loc[32, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[32, "FACTOR ANUAL"] = (tabla2011.loc[32, "S(x)"] / ((tabla2011.loc[32, "S(x)"] * tabla2011.loc[37, "P(x+5)"]))) ** (1/5)    

    for i in range(33, 37):
        if tabla2011.loc[32, "P(x+5)"] == 1 or tabla2011.loc[37, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[32, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2011.loc[37, "P(x+5)"] == 1:
        tabla2011.loc[37, "S(x)"] = tabla2011.loc[36, "S(x)"] * tabla2011.loc[37, "P(x+5)"]
    else: tabla2011.loc[37, "S(x)"] = tabla2011.loc[32, "S(x)"] * tabla2011.loc[37, "P(x+5)"]

    #i+5   
    if tabla2011.loc[42, "P(x+5)"] == 1:
        tabla2011.loc[37, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[37, "FACTOR ANUAL"] = (tabla2011.loc[37, "S(x)"] / ((tabla2011.loc[37, "S(x)"] * tabla2011.loc[42, "P(x+5)"]))) ** (1/5)    

    for i in range(38, 42):
        if tabla2011.loc[42, "P(x+5)"] == 1 or tabla2011.loc[37, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[37, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[42, "P(x+5)"] == 1:
        tabla2011.loc[42, "S(x)"] = tabla2011.loc[41, "S(x)"] * tabla2011.loc[42, "P(x+5)"]
    else: tabla2011.loc[42, "S(x)"] = tabla2011.loc[37, "S(x)"] * tabla2011.loc[42, "P(x+5)"]
    
    if tabla2011.loc[47, "P(x+5)"] == 1:
        tabla2011.loc[42, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[42, "FACTOR ANUAL"] = (tabla2011.loc[42, "S(x)"] / ((tabla2011.loc[42, "S(x)"] * tabla2011.loc[47, "P(x+5)"]))) ** (1/5)    

    for i in range(43, 47):
        if tabla2011.loc[47, "P(x+5)"] == 1 or tabla2011.loc[42, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[42, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[47, "P(x+5)"] == 1:
        tabla2011.loc[47, "S(x)"] = tabla2011.loc[46, "S(x)"] * tabla2011.loc[47, "P(x+5)"]
    else: tabla2011.loc[47, "S(x)"] = tabla2011.loc[42, "S(x)"] * tabla2011.loc[47, "P(x+5)"]

    if tabla2011.loc[52, "P(x+5)"] == 1:
        tabla2011.loc[47, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[47, "FACTOR ANUAL"] = (tabla2011.loc[47, "S(x)"] / ((tabla2011.loc[47, "S(x)"] * tabla2011.loc[52, "P(x+5)"]))) ** (1/5) 

    for i in range(48, 52):
        if tabla2011.loc[52, "P(x+5)"] == 1 or tabla2011.loc[47, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[47, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[52, "P(x+5)"] == 1:
        tabla2011.loc[52, "S(x)"] = tabla2011.loc[51, "S(x)"] * tabla2011.loc[52, "P(x+5)"]
    else: tabla2011.loc[52, "S(x)"] = tabla2011.loc[47, "S(x)"] * tabla2011.loc[52, "P(x+5)"]

    if tabla2011.loc[57, "P(x+5)"] == 1:
        tabla2011.loc[52, "FACTOR ANUAL"] = 1
    else: tabla2011.loc[52, "FACTOR ANUAL"] = (tabla2011.loc[52, "S(x)"] / ((tabla2011.loc[52, "S(x)"] * tabla2011.loc[57, "P(x+5)"]))) ** (1/5) 

    for i in range(53, 57):
        if tabla2011.loc[57, "P(x+5)"] == 1 or tabla2011.loc[52, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1 , "S(x)"] / tabla2011.loc[52, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2011.loc[57, "P(x+5)"] == 1:
        tabla2011.loc[57, "S(x)"] = tabla2011.loc[56, "S(x)"] * tabla2011.loc[57, "P(x+5)"]
    else: tabla2011.loc[57, "S(x)"] = tabla2011.loc[52, "S(x)"] * tabla2011.loc[57, "P(x+5)"]

    for i in range(58, 61):
        if tabla2011.loc[i-1, "P(x+5)"] == 1:
            tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]
        else: tabla2011.loc[i, "S(x)"] = tabla2011.loc[i-1, "S(x)"] * tabla2011.loc[i, "P(x+5)"]   

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla2012 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2012] = tabla2012

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2012.loc[1, "P(x+5)"] = GENERACION_2012.loc[0, "PROBABILIDAD QUINQUENAL"] / PROMEDIO_QUINQUENAL2012
    tabla2012.loc[2: 5, "P(x+5)"] = tabla2012.loc[1, "P(x+5)"]
    tabla2012.loc[6, "P(x+5)"] = GENERACION_2012.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2012.loc[11, "P(x+5)"] = GENERACION_2012.loc[1, "PROBABILIDAD QUINQUENAL"]

    for i in [16, 21, 26, 31, 36, 41, 46, 51, 56]:
        if tabla2012.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2012 <= 1:
            tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2012
        else:
            tabla2012.loc[i, "P(x+5)"] = 1

    for i in range(6, 12):
        if i not in [6, 11]:
            if (tabla2012.loc[6, "P(x+5)"] == 1 or tabla2012.loc[11, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"]

    for i in range(11, 17):
        if i not in [11, 16]:
            if (tabla2012.loc[11, "P(x+5)"] == 1 or tabla2012.loc[16, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"]

    for i in range(16, 22):
        if i not in [16, 21]:
            if (tabla2012.loc[16, "P(x+5)"] == 1 or tabla2012.loc[21, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] 

    for i in range(21, 27):
        if i not in [21, 26]:
            if (tabla2012.loc[21, "P(x+5)"] == 1 or tabla2012.loc[26, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] 

    for i in range(26, 32):
        if i not in [26, 31]:
            if (tabla2012.loc[26, "P(x+5)"] == 1 or tabla2012.loc[31, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] 

    for i in range(31, 37):
        if i not in [31, 36]:
            if (tabla2012.loc[31, "P(x+5)"] == 1 or tabla2012.loc[36, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] 

    for i in range(36, 42):
        if i not in [36, 41]:
            if (tabla2012.loc[36, "P(x+5)"] == 1 or tabla2012.loc[41, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] 

    for i in range(41, 47):
        if i not in [41, 46]:
            if (tabla2012.loc[41, "P(x+5)"] == 1 or tabla2012.loc[46, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"]  

    for i in range(46, 52):
        if i not in [46, 51]:
            if (tabla2012.loc[46, "P(x+5)"] == 1 or tabla2012.loc[51, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"]  
            
    for i in range(51, 57):
        if i not in [51, 56]:
            if (tabla2012.loc[51, "P(x+5)"] == 1 or tabla2012.loc[56, "P(x+5)"] == 1):
                if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) >= 1:
                    tabla2012.loc[i, "P(x+5)"] = 1
                else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
            else: tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"]

    for i in range(57, 61):
        if tabla2012.loc[i-1, "P(x+5)"] == 1:
            tabla2012.loc[i, "P(x+5)"] = 1
        if tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5)) < 1:
            tabla2012.loc[i, "P(x+5)"] = tabla2012.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2012 ** (1/5))
        else: tabla2012.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2012.loc[0, "S(x)"] = 100000
    tabla2012.loc[1, "S(x)"] = tabla2012.loc[0, "S(x)"] * tabla2012.loc[1, "P(x+5)"]

    for i in [6]:
        tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-5, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        
    #tabla2012.loc[0, "FACTOR ANUAL"] = (tabla2012.loc[0, "S(x)"] / tabla2012.loc[1, "S(x)"]) ** (1/5)

    for i in [1]:
        tabla2012.loc[i, "FACTOR ANUAL"] = (tabla2012.loc[i, "S(x)"] / tabla2012.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 6):
        if i not in [1]:
            tabla2012.loc[i, "FACTOR ANUAL"] = tabla2012.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 6):
        if i not in [1]:
            if tabla2012.loc[i, "FACTOR ANUAL"] == 1:
                tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] / tabla2012.loc[i, "FACTOR ANUAL"]
            else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] / tabla2012.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[6, "P(x+5)"] == 1:
        tabla2012.loc[6, "S(x)"] = tabla2012.loc[5, "S(x)"] * tabla2012.loc[6, "P(x+5)"]
    else: tabla2012.loc[6, "S(x)"] = tabla2012.loc[1, "S(x)"] * tabla2012.loc[6, "P(x+5)"]
    
    if tabla2012.loc[11, "P(x+5)"] == 1:
        tabla2012.loc[6, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[6, "FACTOR ANUAL"] = (tabla2012.loc[6, "S(x)"] / ((tabla2012.loc[6, "S(x)"] * tabla2012.loc[11, "P(x+5)"]))) ** (1/5)    

    for i in range(7, 11):
        if tabla2012.loc[11, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[6, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[11, "P(x+5)"] == 1:
        tabla2012.loc[11, "S(x)"] = tabla2012.loc[10, "S(x)"] * tabla2012.loc[11, "P(x+5)"]
    else: tabla2012.loc[11, "S(x)"] = tabla2012.loc[6, "S(x)"] * tabla2012.loc[11, "P(x+5)"]
    
    if tabla2012.loc[16, "P(x+5)"] == 1:
        tabla2012.loc[11, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[11, "FACTOR ANUAL"] = (tabla2012.loc[11, "S(x)"] / ((tabla2012.loc[11, "S(x)"] * tabla2012.loc[16, "P(x+5)"]))) ** (1/5)    

    for i in range(12, 16):
        if tabla2012.loc[16, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[11, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[16, "P(x+5)"] == 1:
        tabla2012.loc[16, "S(x)"] = tabla2012.loc[15, "S(x)"] * tabla2012.loc[16, "P(x+5)"]
    else: tabla2012.loc[16, "S(x)"] = tabla2012.loc[11, "S(x)"] * tabla2012.loc[16, "P(x+5)"]
    
    if tabla2012.loc[21, "P(x+5)"] == 1:
        tabla2012.loc[16, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[16, "FACTOR ANUAL"] = (tabla2012.loc[16, "S(x)"] / ((tabla2012.loc[16, "S(x)"] * tabla2012.loc[21, "P(x+5)"]))) ** (1/5)    

    for i in range(17, 21):
        if tabla2012.loc[21, "P(x+5)"] == 1 or tabla2012.loc[16, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[16, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[21, "P(x+5)"] == 1:
        tabla2012.loc[21, "S(x)"] = tabla2012.loc[20, "S(x)"] * tabla2012.loc[21, "P(x+5)"]
    else: tabla2012.loc[21, "S(x)"] = tabla2012.loc[16, "S(x)"] * tabla2012.loc[21, "P(x+5)"]
    
    if tabla2012.loc[26, "P(x+5)"] == 1:
        tabla2012.loc[21, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[21, "FACTOR ANUAL"] = (tabla2012.loc[21, "S(x)"] / ((tabla2012.loc[21, "S(x)"] * tabla2012.loc[26, "P(x+5)"]))) ** (1/5)    

    for i in range(22, 26):
        if tabla2012.loc[26, "P(x+5)"] == 1 or tabla2012.loc[21, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[21, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[26, "P(x+5)"] == 1:
        tabla2012.loc[26, "S(x)"] = tabla2012.loc[25, "S(x)"] * tabla2012.loc[26, "P(x+5)"]
    else: tabla2012.loc[26, "S(x)"] = tabla2012.loc[21, "S(x)"] * tabla2012.loc[26, "P(x+5)"]
    
    if tabla2012.loc[31, "P(x+5)"] == 1:
        tabla2012.loc[26, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[26, "FACTOR ANUAL"] = (tabla2012.loc[26, "S(x)"] / ((tabla2012.loc[26, "S(x)"] * tabla2012.loc[31, "P(x+5)"]))) ** (1/5)    

    for i in range(27, 31):
        if tabla2012.loc[31, "P(x+5)"] == 1 or tabla2012.loc[26, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[26, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[31, "P(x+5)"] == 1:
        tabla2012.loc[31, "S(x)"] = tabla2012.loc[30, "S(x)"] * tabla2012.loc[31, "P(x+5)"]
    else: tabla2012.loc[31, "S(x)"] = tabla2012.loc[26, "S(x)"] * tabla2012.loc[31, "P(x+5)"]
    
    if tabla2012.loc[36, "P(x+5)"] == 1:
        tabla2012.loc[31, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[31, "FACTOR ANUAL"] = (tabla2012.loc[31, "S(x)"] / ((tabla2012.loc[31, "S(x)"] * tabla2012.loc[36, "P(x+5)"]))) ** (1/5)    

    for i in range(32, 36):
        if tabla2012.loc[36, "P(x+5)"] == 1 or tabla2012.loc[31, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[31, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2012.loc[36, "P(x+5)"] == 1:
        tabla2012.loc[36, "S(x)"] = tabla2012.loc[35, "S(x)"] * tabla2012.loc[36, "P(x+5)"]
    else: tabla2012.loc[36, "S(x)"] = tabla2012.loc[31, "S(x)"] * tabla2012.loc[36, "P(x+5)"]

    #i+5   
    if tabla2012.loc[41, "P(x+5)"] == 1:
        tabla2012.loc[36, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[36, "FACTOR ANUAL"] = (tabla2012.loc[36, "S(x)"] / ((tabla2012.loc[36, "S(x)"] * tabla2012.loc[41, "P(x+5)"]))) ** (1/5)    

    for i in range(37, 41):
        if tabla2012.loc[41, "P(x+5)"] == 1 or tabla2012.loc[36, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[36, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[41, "P(x+5)"] == 1:
        tabla2012.loc[41, "S(x)"] = tabla2012.loc[40, "S(x)"] * tabla2012.loc[41, "P(x+5)"]
    else: tabla2012.loc[41, "S(x)"] = tabla2012.loc[36, "S(x)"] * tabla2012.loc[41, "P(x+5)"]
    
    if tabla2012.loc[46, "P(x+5)"] == 1:
        tabla2012.loc[41, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[41, "FACTOR ANUAL"] = (tabla2012.loc[41, "S(x)"] / ((tabla2012.loc[41, "S(x)"] * tabla2012.loc[46, "P(x+5)"]))) ** (1/5)    

    for i in range(42, 46):
        if tabla2012.loc[46, "P(x+5)"] == 1 or tabla2012.loc[41, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[41, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[46, "P(x+5)"] == 1:
        tabla2012.loc[46, "S(x)"] = tabla2012.loc[45, "S(x)"] * tabla2012.loc[46, "P(x+5)"]
    else: tabla2012.loc[46, "S(x)"] = tabla2012.loc[41, "S(x)"] * tabla2012.loc[46, "P(x+5)"]

    if tabla2012.loc[51, "P(x+5)"] == 1:
        tabla2012.loc[46, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[46, "FACTOR ANUAL"] = (tabla2012.loc[46, "S(x)"] / ((tabla2012.loc[46, "S(x)"] * tabla2012.loc[51, "P(x+5)"]))) ** (1/5) 

    for i in range(47, 51):
        if tabla2012.loc[51, "P(x+5)"] == 1 or tabla2012.loc[46, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[46, "FACTOR ANUAL"]
        
        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[51, "P(x+5)"] == 1:
        tabla2012.loc[51, "S(x)"] = tabla2012.loc[50, "S(x)"] * tabla2012.loc[52, "P(x+5)"]
    else: tabla2012.loc[51, "S(x)"] = tabla2012.loc[46, "S(x)"] * tabla2012.loc[51, "P(x+5)"]

    if tabla2012.loc[56, "P(x+5)"] == 1:
        tabla2012.loc[51, "FACTOR ANUAL"] = 1
    else: tabla2012.loc[51, "FACTOR ANUAL"] = (tabla2012.loc[51, "S(x)"] / ((tabla2012.loc[51, "S(x)"] * tabla2012.loc[56, "P(x+5)"]))) ** (1/5) 

    for i in range(52, 56):
        if tabla2012.loc[56, "P(x+5)"] == 1 or tabla2012.loc[51, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1 , "S(x)"] / tabla2012.loc[51, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2012.loc[56, "P(x+5)"] == 1:
        tabla2012.loc[56, "S(x)"] = tabla2012.loc[55, "S(x)"] * tabla2012.loc[56, "P(x+5)"]
    else: tabla2012.loc[56, "S(x)"] = tabla2012.loc[51, "S(x)"] * tabla2012.loc[56, "P(x+5)"]

    for i in range(57, 61):
        if tabla2012.loc[i-1, "P(x+5)"] == 1:
            tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]
        else: tabla2012.loc[i, "S(x)"] = tabla2012.loc[i-1, "S(x)"] * tabla2012.loc[i, "P(x+5)"]

    #----------------------------------------------------------------------------------------------------------------------------------------
    tabla2013 = pd.DataFrame({
            "Edad": range(61),
            "P(x+5)": 0.0,
            "S(x)": 0.0,
            "FACTOR ANUAL":0.0 
        })
    TABLAS[2013] = tabla2013

    # Colocar en el renglón 11 el primer valor de PROBABILIDAD QUINQUENAL
    tabla2013.loc[5, "P(x+5)"] = GENERACION_2013.loc[0, "PROBABILIDAD QUINQUENAL"]
    tabla2013.loc[6: 9, "P(x+5)"] = tabla2013.loc[5, "P(x+5)"]
    tabla2013.loc[10, "P(x+5)"] = GENERACION_2013.loc[1, "PROBABILIDAD QUINQUENAL"]
    tabla2013.loc[15, "P(x+5)"] = GENERACION_2013.loc[2, "PROBABILIDAD QUINQUENAL"]

    for i in [20, 25, 30, 35, 40, 45, 50, 55, 60]:
        if tabla2013.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2013 <= 1:
            tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-5, "P(x+5)"] * PROMEDIO_QUINQUENAL2013
        else:
            tabla2013.loc[i, "P(x+5)"] = 1

    for i in range(10, 16):
        if i not in [10, 15]:
            if (tabla2013.loc[10, "P(x+5)"] == 1 or tabla2013.loc[15, "P(x+5)"] == 1):
                if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) >= 1:
                    tabla2013.loc[i, "P(x+5)"] = 1
                else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"]

    for i in range(15, 21):
        if i not in [15, 20]:
            if (tabla2013.loc[15, "P(x+5)"] == 1 or tabla2013.loc[20, "P(x+5)"] == 1):
                if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) >= 1:
                    tabla2013.loc[i, "P(x+5)"] = 1
                else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"]

    for i in range(20, 26):
        if i not in [20, 25]:
            if (tabla2013.loc[20, "P(x+5)"] == 1 or tabla2013.loc[25, "P(x+5)"] == 1):
                if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) >= 1:
                    tabla2013.loc[i, "P(x+5)"] = 1
                else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"]

    for i in range(25, 31):
        if i not in [25, 30]:
            if (tabla2013.loc[25, "P(x+5)"] == 1 or tabla2013.loc[30, "P(x+5)"] == 1):
                if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) >= 1:
                    tabla2013.loc[i, "P(x+5)"] = 1
                else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] 

    for i in range(30, 36):
        if i not in [30, 35]:
            if (tabla2013.loc[30, "P(x+5)"] == 1 or tabla2013.loc[35, "P(x+5)"] == 1):
                if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) >= 1:
                    tabla2013.loc[i, "P(x+5)"] = 1
                else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] 

    for i in range(35, 41):
        if i not in [35, 40]:
            if (tabla2013.loc[35, "P(x+5)"] == 1 or tabla2013.loc[40, "P(x+5)"] == 1):
                if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) >= 1:
                    tabla2013.loc[i, "P(x+5)"] = 1
                else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] 

    for i in range(40, 46):
        if i not in [40, 45]:
            if (tabla2013.loc[40, "P(x+5)"] == 1 or tabla2013.loc[45, "P(x+5)"] == 1):
                if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) >= 1:
                    tabla2013.loc[i, "P(x+5)"] = 1
                else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] 

    for i in range(45, 51):
        if i not in [45, 50]:
            if (tabla2013.loc[45, "P(x+5)"] == 1 or tabla2013.loc[50, "P(x+5)"] == 1):
                if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) >= 1:
                    tabla2013.loc[i, "P(x+5)"] = 1
                else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"]  

    for i in range(50, 56):
        if i not in [50, 55]:
            if (tabla2013.loc[50, "P(x+5)"] == 1 or tabla2013.loc[55, "P(x+5)"] == 1):
                if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) >= 1:
                    tabla2013.loc[i, "P(x+5)"] = 1
                else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"]  
            
    for i in range(56, 61):
        if i not in [60]:
            if tabla2013.loc[i-1, "P(x+5)"] == 1:
                tabla2013.loc[i, "P(x+5)"] = 1
            if tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5)) < 1:
                tabla2013.loc[i, "P(x+5)"] = tabla2013.loc[i-1, "P(x+5)"] * (PROMEDIO_QUINQUENAL2013 ** (1/5))
            else: tabla2013.loc[i, "P(x+5)"] = 1
        
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    tabla2013.loc[0, "S(x)"] = 100000
    tabla2013.loc[5, "S(x)"] = tabla2013.loc[0, "S(x)"] * tabla2013.loc[5, "P(x+5)"]

    for i in [10]:
        tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-5, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        
    tabla2013.loc[0, "FACTOR ANUAL"] = (tabla2013.loc[0, "S(x)"] / tabla2013.loc[5, "S(x)"]) ** (1/5)

    for i in [5]:
        tabla2013.loc[i, "FACTOR ANUAL"] = (tabla2013.loc[i, "S(x)"] / tabla2013.loc[i+5, "S(x)"]) ** (1/5)
        
    for i in range(1, 10):
        if i not in [5]:
            tabla2013.loc[i, "FACTOR ANUAL"] = tabla2013.loc[i-1, "FACTOR ANUAL"]
        
    for i in range(1, 10):
        if i not in [5]:
            if tabla2013.loc[i, "FACTOR ANUAL"] == 1:
                tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] / tabla2013.loc[i, "FACTOR ANUAL"] 
            else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] / tabla2013.loc[i, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2013.loc[10, "P(x+5)"] == 1:
        tabla2013.loc[10, "S(x)"] = tabla2013.loc[9, "S(x)"] * tabla2013.loc[10, "P(x+5)"]
    else: tabla2013.loc[10, "S(x)"] = tabla2013.loc[5, "S(x)"] * tabla2013.loc[10, "P(x+5)"]
    
    if tabla2013.loc[15, "P(x+5)"] == 1:
        tabla2013.loc[10, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[10, "FACTOR ANUAL"] = (tabla2013.loc[10, "S(x)"] / ((tabla2013.loc[10, "S(x)"] * tabla2013.loc[15, "P(x+5)"]))) ** (1/5)    

    for i in range(11, 15):
        if tabla2013.loc[15, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[10, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2013.loc[15, "P(x+5)"] == 1:
        tabla2013.loc[15, "S(x)"] = tabla2013.loc[14, "S(x)"] * tabla2013.loc[15, "P(x+5)"]
    else: tabla2013.loc[15, "S(x)"] = tabla2013.loc[10, "S(x)"] * tabla2013.loc[15, "P(x+5)"]
    
    if tabla2013.loc[20, "P(x+5)"] == 1:
        tabla2013.loc[15, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[15, "FACTOR ANUAL"] = (tabla2013.loc[15, "S(x)"] / ((tabla2013.loc[15, "S(x)"] * tabla2013.loc[20, "P(x+5)"]))) ** (1/5)    

    for i in range(16, 20):
        if tabla2013.loc[20, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[15, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2013.loc[20, "P(x+5)"] == 1:
        tabla2013.loc[20, "S(x)"] = tabla2013.loc[19, "S(x)"] * tabla2013.loc[20, "P(x+5)"]
    else: tabla2013.loc[20, "S(x)"] = tabla2013.loc[15, "S(x)"] * tabla2013.loc[20, "P(x+5)"]
    
    if tabla2013.loc[25, "P(x+5)"] == 1:
        tabla2013.loc[20, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[20, "FACTOR ANUAL"] = (tabla2013.loc[20, "S(x)"] / ((tabla2013.loc[20, "S(x)"] * tabla2013.loc[25, "P(x+5)"]))) ** (1/5)    

    for i in range(21, 25):
        if tabla2013.loc[25, "P(x+5)"] == 1 or tabla2013.loc[20, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[20, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2013.loc[25, "P(x+5)"] == 1:
        tabla2013.loc[25, "S(x)"] = tabla2013.loc[24, "S(x)"] * tabla2013.loc[25, "P(x+5)"]
    else: tabla2013.loc[25, "S(x)"] = tabla2013.loc[20, "S(x)"] * tabla2013.loc[25, "P(x+5)"]
    
    if tabla2013.loc[30, "P(x+5)"] == 1:
        tabla2013.loc[25, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[25, "FACTOR ANUAL"] = (tabla2013.loc[25, "S(x)"] / ((tabla2013.loc[25, "S(x)"] * tabla2013.loc[30, "P(x+5)"]))) ** (1/5)    

    for i in range(26, 30):
        if tabla2013.loc[30, "P(x+5)"] == 1 or tabla2013.loc[25, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[25, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2013.loc[30, "P(x+5)"] == 1:
        tabla2013.loc[30, "S(x)"] = tabla2013.loc[29, "S(x)"] * tabla2013.loc[30, "P(x+5)"]
    else: tabla2013.loc[30, "S(x)"] = tabla2013.loc[25, "S(x)"] * tabla2013.loc[30, "P(x+5)"]
    
    if tabla2013.loc[35, "P(x+5)"] == 1:
        tabla2013.loc[30, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[30, "FACTOR ANUAL"] = (tabla2013.loc[30, "S(x)"] / ((tabla2013.loc[30, "S(x)"] * tabla2013.loc[35, "P(x+5)"]))) ** (1/5)    

    for i in range(31, 35):
        if tabla2013.loc[35, "P(x+5)"] == 1 or tabla2013.loc[30, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[30, "FACTOR ANUAL"] 

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2013.loc[35, "P(x+5)"] == 1:
        tabla2013.loc[35, "S(x)"] = tabla2013.loc[34, "S(x)"] * tabla2013.loc[35, "P(x+5)"]
    else: tabla2013.loc[35, "S(x)"] = tabla2013.loc[30, "S(x)"] * tabla2013.loc[35, "P(x+5)"]
    
    if tabla2013.loc[40, "P(x+5)"] == 1:
        tabla2013.loc[35, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[35, "FACTOR ANUAL"] = (tabla2013.loc[35, "S(x)"] / ((tabla2013.loc[35, "S(x)"] * tabla2013.loc[40, "P(x+5)"]))) ** (1/5)    

    for i in range(36, 40):
        if tabla2013.loc[40, "P(x+5)"] == 1 or tabla2013.loc[35, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[35, "FACTOR ANUAL"] 
        
        #-------------------------------------------------------------------------------------------------------------------------------------------  
    if tabla2013.loc[40, "P(x+5)"] == 1:
        tabla2013.loc[40, "S(x)"] = tabla2013.loc[39, "S(x)"] * tabla2013.loc[40, "P(x+5)"]
    else: tabla2013.loc[40, "S(x)"] = tabla2013.loc[35, "S(x)"] * tabla2013.loc[40, "P(x+5)"]

    #i+5   
    if tabla2013.loc[45, "P(x+5)"] == 1:
        tabla2013.loc[40, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[40, "FACTOR ANUAL"] = (tabla2013.loc[40, "S(x)"] / ((tabla2013.loc[40, "S(x)"] * tabla2013.loc[45, "P(x+5)"]))) ** (1/5)    

    for i in range(41, 45):
        if tabla2013.loc[45, "P(x+5)"] == 1 or tabla2013.loc[40, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[40, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2013.loc[45, "P(x+5)"] == 1:
        tabla2013.loc[45, "S(x)"] = tabla2013.loc[44, "S(x)"] * tabla2013.loc[45, "P(x+5)"]
    else: tabla2013.loc[45, "S(x)"] = tabla2013.loc[40, "S(x)"] * tabla2013.loc[45, "P(x+5)"]
    
    if tabla2013.loc[50, "P(x+5)"] == 1:
        tabla2013.loc[45, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[45, "FACTOR ANUAL"] = (tabla2013.loc[45, "S(x)"] / ((tabla2013.loc[45, "S(x)"] * tabla2013.loc[50, "P(x+5)"]))) ** (1/5)    

    for i in range(46, 50):
        if tabla2013.loc[50, "P(x+5)"] == 1 or tabla2013.loc[45, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[45, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2013.loc[50, "P(x+5)"] == 1:
        tabla2013.loc[50, "S(x)"] = tabla2013.loc[49, "S(x)"] * tabla2013.loc[50, "P(x+5)"]
    else: tabla2013.loc[50, "S(x)"] = tabla2013.loc[45, "S(x)"] * tabla2013.loc[50, "P(x+5)"]

    if tabla2013.loc[55, "P(x+5)"] == 1:
        tabla2013.loc[50, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[50, "FACTOR ANUAL"] = (tabla2013.loc[50, "S(x)"] / ((tabla2013.loc[50, "S(x)"] * tabla2013.loc[55, "P(x+5)"]))) ** (1/5) 

    for i in range(51, 55):
        if tabla2013.loc[55, "P(x+5)"] == 1 or tabla2013.loc[50, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[50, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    

    if tabla2013.loc[55, "P(x+5)"] == 1:
        tabla2013.loc[55, "S(x)"] = tabla2013.loc[54, "S(x)"] * tabla2013.loc[55, "P(x+5)"]
    else: tabla2013.loc[55, "S(x)"] = tabla2013.loc[50, "S(x)"] * tabla2013.loc[55, "P(x+5)"]

    if tabla2013.loc[60, "P(x+5)"] == 1:
        tabla2013.loc[55, "FACTOR ANUAL"] = 1
    else: tabla2013.loc[55, "FACTOR ANUAL"] = (tabla2013.loc[55, "S(x)"] / ((tabla2013.loc[55, "S(x)"] * tabla2013.loc[60, "P(x+5)"]))) ** (1/5) 

    for i in range(56, 60):
        if tabla2013.loc[60, "P(x+5)"] == 1 or tabla2013.loc[55, "P(x+5)"] == 1:
            tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1, "S(x)"] * tabla2013.loc[i, "P(x+5)"]
        else: tabla2013.loc[i, "S(x)"] = tabla2013.loc[i-1 , "S(x)"] / tabla2013.loc[55, "FACTOR ANUAL"]

        #-------------------------------------------------------------------------------------------------------------------------------------------    
    if tabla2013.loc[60, "P(x+5)"] == 1:
        tabla2013.loc[60, "S(x)"] = tabla2013.loc[60, "P(x+5)"] * tabla2013.loc[59, "S(x)"]
    else: tabla2013.loc[60, "S(x)"] = tabla2013.loc[60, "P(x+5)"] * tabla2013.loc[55, "S(x)"]


    PROMEDIO_DE_GENERACIONES = pd.DataFrame({
        f"S(x) {anio}": TABLAS[anio]["S(x)"]
        for anio in range(1983, 2014)
    })

    PROMEDIO_DE_GENERACIONES["S(x) PROMEDIO"] = (
        PROMEDIO_DE_GENERACIONES.mean(axis=1)
    )

    edad = np.arange(0, 61)

    DATOS_PARA_REGRESION = pd.DataFrame({
        "EDAD(x)": edad,
        "Ln(x)": np.where(edad > 0, np.log(edad), np.nan),
        "S(x) PROMEDIO": PROMEDIO_DE_GENERACIONES["S(x) PROMEDIO"],
        "S(x) AJUSTADA": None
    })

    from sklearn.linear_model import LinearRegression

    # Variables
    X = DATOS_PARA_REGRESION[["Ln(x)"]].iloc[2:]      # Variable independiente
    y = DATOS_PARA_REGRESION["S(x) PROMEDIO"].iloc[2:]           # Variable dependiente

    # Modelo
    modelo = LinearRegression()
    modelo.fit(X, y)

    intercepto = modelo.intercept_
    coeficientes = modelo.coef_

    # Coeficientes
    #print(intercepto)
    #print(coeficientes)

    #print("R^2:", modelo.score(X, y))


    DATOS_PARA_REGRESION.iloc[2:, DATOS_PARA_REGRESION.columns.get_loc("S(x) AJUSTADA")] = (
        intercepto + (coeficientes * DATOS_PARA_REGRESION.iloc[2:]["Ln(x)"])
    )

    DATOS_PARA_REGRESION.loc[0:1, "S(x) AJUSTADA"] = DATOS_PARA_REGRESION.loc[0:1, "S(x) PROMEDIO"]

    #print(DATOS_PARA_REGRESION)

    TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA = pd.DataFrame({
        "(x)": DATOS_PARA_REGRESION["EDAD(x)"],
        "S(x)": DATOS_PARA_REGRESION["S(x) AJUSTADA"],
        "p(x)": None,
        "q(x)": None,
        "d(x)": None,
        "E(x)": None,
        "E(x)'": None
    })

    #========================================================================================================================
    #AQUÍ ES DONDE SE REALIZA LA DIMENSIÓN DE LAS TABLAS
    #========================================================================================================================
    def obtener_edad_limite(tabla):

        if tabla.iloc[-1]["P(x+5)"] != 1:
            return tabla.iloc[-1]["Edad"]
        for i in range(len(tabla) - 1, -1, -1):
            if tabla.loc[i, "P(x+5)"] != 1:
                return tabla.loc[i + 1, "Edad"]
        return None

    resumen = []

    for anio in range(1983, 2014):
        tabla = TABLAS[anio]

        edad_limite = obtener_edad_limite(tabla)
        
        resumen.append({
            "Tabla": f"tabla{anio}",
            "Edad_Limite": edad_limite
        })
        
    RESUMEN_EDADES = pd.DataFrame(resumen)

    numero_filas = RESUMEN_EDADES["Edad_Limite"].mean()
    numero_filas = round(numero_filas)
    #========================================================================================================================
    #numero_filas = round(resultados["INTERVALO_FINAL"].mean())
    #========================================================================================================================

    for i in range (0,(numero_filas + 1)):
        TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i, "p(x)"] = TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i+1, "S(x)"] / 100000
        TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i, "q(x)"] = 1 - TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i, "p(x)"]
        TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i, "d(x)"] = TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i, "S(x)"] - TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i+1, "S(x)"]
        TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i, "E(x)'"] = (TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i, "S(x)"] + TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i+1, "S(x)"]) / 2

    TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA = TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.drop(index=range((numero_filas + 1), 61))

    suma_promedios = TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[0: numero_filas-1]["E(x)'"].sum()
    TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[0, "E(x)"] = suma_promedios / 100000 
        
    for i in range (1, numero_filas):
        TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i, "E(x)"] = TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[i-1, "E(x)"] * ((numero_filas / TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[0, "E(x)"]) ** (1 / (numero_filas)))
        

    TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA = (
        TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.drop(
            columns=["E(x)'"],
            errors="ignore"
        )
    )

    TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[numero_filas, "p(x)"] = 0
    TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[numero_filas, "q(x)"] = 0
    TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[numero_filas, "d(x)"] = 0
    TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[numero_filas, "E(x)"] = numero_filas
    
    return TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA

    #print(TABLA_SUPERVIVENCIA_MORTALIDAD_ESPERANZA.loc[0: 40])


    #TABLAS DE PROBABILIDAD QUINQUENAL DE TODOS LOS AÑOS
    #columnas = {}

    #for anio in range(1983, 2014):
     #   CONCENTRACIÓN = GENERACIONES[anio]

      #  columnas[f"INTERVALO_{anio}"] = CONCENTRACIÓN["INTERVALOS DE PROBABILIDAD"]
       # columnas[f"PROBABILIDAD_QUINQUENAL_{anio}"] = CONCENTRACIÓN["PROBABILIDAD QUINQUENAL"]

    #CONCENTRACION_PROBABILIDADES = pd.DataFrame(columnas)


    #CONCENTRACIÓN DE PROMEDIOS DE LAS PROBABILIDAD QUINQUENALES
    #CONCENTRACION_PROMEDIOS = pd.DataFrame({
     #   "AÑO": range(1983, 2014),
      #  "PROMEDIO QUINQUENAL": [
       #     PROMEDIOS_QUINQUENALES[anio]
        #    for anio in range(1983, 2014)
        #]
    #})

    #for i in [1999, 2001, 2004, 2005, 2006, 2007, 2009, 2010, 2011, 2012, 2013]:
     #   CONCENTRACION_PROMEDIOS.loc[
      #      CONCENTRACION_PROMEDIOS["AÑO"] == i,
       #     "PROMEDIO QUINQUENAL"
        #] = PROMEDIOS_AJUSTADOS[i]

    #def guardar_excel(df, nombre):
     #   df.to_excel(
      #      CARPETA_RESULTADOS / nombre,
       #     index=False
        #)

