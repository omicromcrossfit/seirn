
import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

from CALCULOS import calcular_tabla

@st.cache_data 
def obtener_tabla(ruta_base):
    return calcular_tabla(ruta_base)

BASE_DIR = Path(__file__).resolve().parent
CARPETA_BASES = BASE_DIR / "BASES"

st.set_page_config(
    page_title="SUPERVIVENCIA, MORTALIDAD Y ESPERANZA DE VIDA DE LOS NEGOCIOS DE MÉXICO 1989 - 2024",
    layout="wide"
)

st.markdown("""
<h1 style='text-align: center;
            font-size: 60px;
            color: #0E4C92;
            font-weight: bold;'>
    SUPERVIVENCIA, MORTALIDAD Y ESPERANZA DE VIDA DE LOS NEGOCIOS DE MÉXICO 1989 - 2024
</h1>
""", unsafe_allow_html=True)

#st.subheader("Dominios de Análisis")

bases = {
    "NACIONAL": "NACIONAL_TOTAL.xlsx", "AGUASCALIENTES": "AGUASCALIENTES_TOTAL.xlsx", "BAJA CALIFORNIA": "BAJA_CALIFORNIA_TOTAL.xlsx", "BAJA CALIFORNIA SUR": "BAJA_CALIFORNIA_SUR_TOTAL.xlsx", "CAMPECHE": "CAMPECHE_TOTAL.xlsx", "COAHUILA DE ZARAGOZA": "COAHUILA_DE_ZARAGOZA_TOTAL.xlsx", "COLIMA": "COLIMA_TOTAL.xlsx", "CHIAPAS": "CHIAPAS_TOTAL.xlsx", "CHIHUAHUA": "CHIHUAHUA_TOTAL.xlsx", "CIUDAD DE MÉXICO": "CIUDAD_DE_MEXICO_TOTAL.xlsx", "DURANGO": "DURANGO_TOTAL.xlsx",
    "GUANAJUATO": "GUANAJUATO_TOTAL.xlsx", "GUERRERO": "GUERRERO_TOTAL.xlsx", "HIDALGO": "HIDALGO_TOTAL.xlsx", "JALISCO": "JALISCO_TOTAL.xlsx", "MÉXICO": "MEXICO_TOTAL.xlsx", "MICHOACÁN DE OCAMPO": "MICHOACAN_DE_OCAMPO_TOTAL.xlsx", "MORELOS": "MORELOS_TOTAL.xlsx", "NAYARIT": "NAYARIT_TOTAL.xlsx", "NUEVO LEÓN": "NUEVO_LEON_TOTAL.xlsx", "OAXACA": "OAXACA_TOTAL.xlsx", "PUEBLA": "PUEBLA_TOTAL.xlsx", "QUERÉTARO": "QUERETARO_TOTAL.xlsx", "QUINTANA ROO": "QUINTANA_ROO_TOTAL.xlsx",
    "SAN LUIS POTOSÍ": "SAN_LUIS_POTOSI_TOTAL.xlsx", "SINALOA": "SINALOA_TOTAL.xlsx", "SONORA": "SONORA_TOTAL.xlsx", "TABASCO": "TABASCO_TOTAL.xlsx", "TAMAULIPAS": "TAMAULIPAS_TOTAL.xlsx", "TLAXCALA" : "TLAXCALA_TOTAL.xlsx", "VERACRUZ DE IGNACIO DE LA LLAVE": "VERACRUZ_DE_IGNACIO_DE_LA_LLAVE_TOTAL.xlsx", "YUCATÁN": "YUCATAN_TOTAL.xlsx", "ZACATECAS": "ZACATECAS_TOTAL.xlsx"    
}

municipios_interes = {
    "AGUASCALIENTES": {"AGUASCALIENTES": "AGS_AGUASCALIENTES", "RESTO DE MUNICIPIOS": "AGS_RESTO"}, "BAJA CALIFORNIA": {"MEXICALI": "BC_MEXICALI", "TIJUANA": "BC_TIJUANA", "RESTO DE MUNICIPIOS": "BC_RESTO"}, "BAJA CALIFORNIA SUR": {"LA PAZ": "BCS_LA_PAZ", "RESTO DE MUNICIPIOS": "BCS_RESTO"}, "CAMPECHE": {"CAMPECHE": "CAM_CAMPECHE", "CARMEN": "CAM_CARMEN", "RESTO DE MUNICIPIOS": "CAM_RESTO"}, "CIUDAD DE MÉXICO": {"ÁLVARO OBREGÓN": "CDMX_ALVARO_OBREGON", "AZCAPOTZALCO": "CDMX_AZCAPOTZALCO", "BENITO JUÁREZ": "CDMX_BENITO_JUAREZ", "COYOACÁN": "CDMX_COYOACAN", "CUAJIMALPA DE MORELOS": "CDMX_CUAJIMALPA_DE_MORELOS", "CUAUHTÉMOC": "CDMX_CUAUHTEMOC", "GUSTAVO A. MADERO": "CDMX_GUSTAVO_A_MADERO", "IZTACALCO": "CDMX_IZTACALCO", "IZTAPALAPA": "CDMX_IZTAPALAPA", "LA MAGDALENA CONTRERAS": "CDMX_LA_MAGDALENA_CONTRERAS", "MIGUEL HIDALGO": "CDMX_MIGUEL_HIDALGO", "MILPA ALTA": "CDMX_MILPA_ALTA", "TLÁHUAC": "CDMX_TLAHUAC", "TLALPAN": "CDMX_TLALPAN", "VENUSTIANO CARRANZA": "CDMX_VENUSTIANO_CARRANZA", "XOCHIMILCO": "CDMX_XOCHIMILCO"},
    "CHIHUAHUA": {"CHIHUAHUA": "CHI_CHIHUAHUA", "JUÁREZ": "CHI_JUAREZ", "RESTO DE MUNICIPIOS": "CHI_RESTO"}, "CHIAPAS": {"SAN CRISTÓBAL DE LAS CASAS": "CHP_SAN_CRISTOBAL_DE_LAS_CASAS", "TAPACHULA": "CHP_TAPACHULA", "TUXTLA GUTIÉRREZ": "CHP_TUXTLA_GUTIERREZ", "RESTO DE MUNICIPIOS": "CHP_RESTO"}, "COAHUILA DE ZARAGOZA": {"SALTILLO": "COA_SALTILLO", "TORREÓN": "COA_TORREON", "RESTO DE MUNICIPIOS": "COA_RESTO"}, "COLIMA": {"COLIMA": "COL_COLIMA", "MANZANILLO": "COL_MANZANILLO", "RESTO DE MUNICIPIOS": "COL_RESTO"}, "DURANGO": {"DURANGO": "DGO_DURANGO", "GÓMEZ PALACIO": "DGO_GOMEZ_PALACIO", "LERDO": "DGO_LERDO", "RESTO DE MUNICIPIOS": "DGO_RESTO"}, "GUERRERO": {"ACAPULCO DE JUÁREZ": "GRO_ACAPULCO_DE_JUAREZ", "CHILPANCINGO DE LOS BRAVO": "GRO_CHILPANCINGO_DE_LOS_BRAVO", "RESTO DE MUNICIPIOS": "GRO_RESTO"}, "GUANAJUATO": {"CELAYA": "GTO_CELAYA", "GUANAJUATO": "GTO_GUANAJUATO", "IRAPUATO": "GTO_IRAPUATO", "LEÓN": "GTO_LEON", "SALAMANCA": "GTO_SALAMANCA", "SILAO DE LA VICTORIA": "GTO_SILAO_DE_LA_VICTORIA", "RESTO DE MUNICIPIOS": "GTO_RESTO"}, 
    "HIDALGO": {"PACHUCA DE SOTO": "HDO_PACHUCA_DE_SOTO", "TULANCINGO DE BRAVO": "HDO_TULANCINGO_DE_BRAVO", "RESTO DE MUNICIPIOS": "HDO_RESTO"}, "JALISCO": {"GUADALAJARA": "JCO_GUADALAJARA", "PUERTO VALLARTA": "JCO_PUERTO_VALLARTA", "SAN PEDRO TLAQUEPAQUE": "JCO_SAN_PEDRO_TLAQUEPAQUE", "TONALA": "JCO_TONALA", "ZAPOPAN": "JCO_ZAPOPAN", "RESTO DE MUNICIPIOS": "JCO_RESTO"}, "MICHOACÁN DE OCAMPO": {"APATZINGÁN": "MCH_APATZINGAN", "LA PIEDAD": "MCH_LA_PIEDAD", "LAZARO CÁRDENAS": "MCH_LAZARO_CARDENAS", "MORELIA": "MCH_MORELIA", "URUAPAN": "MCH_URUAPAN", "ZAMORA": "MCH_ZAMORA", "RESTO DE MUNICIPIOS": "MCH_RESTO"}, "MORELOS": {"CUAUTLA": "MOR_CUAUTLA", "CUERNAVACA": "MOR_CUERNAVACA", "RESTO DE MUNICIPIOS": "MOR_RESTO"}, "MÉXICO": {"ATIZAPÁN": "MX_ATIZAPAN", "CHALCO": "MX_CHALCO", "COACALCO DE BERRIOZABAL": "MX_COACALCO_DE_BERRIOZABAL", "ISCALLI": "MX_CUAUTITLAN_ISCALLI", "ECATEPEC DE MORELOS": "MX_ECATEPEC_DE_MORELOS", "NAUCALPAN DE JUÁREZ": "MX_NAUCALPAN_DE_JUAREZ", "NEZAHUALCOYOTL": "MX_NEZAHUALCOYOTL", "TEXCOCO": "MX_TEXCOCO", "TLALNEPANTLA DE BAZ": "MX_TLALNEPANTLA_DE_BAZ", "TOLUCA": "MX_TOLUCA", "TULTITLAN": "MX_TULTITLAN", "RESTO DE MUNICIPIOS": "MX_RESTO"}, 
    "NAYARIT": {"TEPIC": "NAY_TEPIC", "RESTO DE MUNICIPIOS": "NAY_RESTO"}, "NUEVO LEÓN": {"APODACA": "NLN_APODACA", "GENERAL ESCOBEDO": "NLN_GENERAL_ESCOBEDO", "MONTERREY": "NLN_MONTERREY", "SAN PEDRO GARZA GARCÍA": "NLN_SAN_PEDRO_GARZA_GARCIA", "SANTA CATARINA": "NLN_SANTA_CATARINA", "RESTO DE MUNICIPIOS": "NLN_RESTO"}, "OAXACA": {"OAXACA DE JUÁREZ": "OXA_OAXACA_DE_JUAREZ", "RESTO DE MUNICIPIOS": "OXA_RESTO"}, "PUEBLA": {"PUEBLA": "PUB_PUEBLA", "SAN PEDRO CHOLULA": "PUB_SAN_PEDRO_CHOLULA", "RESTO DE MUNICIPIOS": "PUB_RESTO"}, "QUINTANA ROO": {"BENITO JUÁREZ": "QRO_BENITO_JUAREZ", "OTHÓN P. BLANCO": "QRO_OTHON_P_BLANCO", "RESTO DE MUNICIPIOS": "QRO_RESTO"}, "QUERÉTARO": {"QUERÉTARO": "QTO_QUERETARO", "SAN JUAN DEL RÍO": "QTO_SAN_JUAN_DEL_RIO", "RESTO DE MUNICIPIOS": "QTO_RESTO"}, "SINALOA": {"CULIACÁN": "SIN_CULIACAN", "MAZATLÁN": "SIN_MAZATLAN", "RESTO DE MUNICIPIOS": "SIN_RESTO"}, "SAN LUIS POTOSÍ": {"CIUDAD VALLES": "SLP_CIUDAD_VALLES", "SAN LUIS POTOSÍ": "SLP_SAN_LUIS_POTOSI", "RESTO DE MUNICIPIOS": "SLP_RESTO"}, "SONORA": {"HERMOSILLO": "SON_HERMOSILLO", "RESTO DE MUNICIPIOS": "SON_RESTO"}, 
    "TAMAULIPAS": {"MATAMOROS": "TAM_MATAMOROS", "NUEVO LAREDO": "TAM_NUEVO_LAREDO", "REYNOSA": "TAM_REYNOSA", "VICTORIA": "TAM_VICTORIA", "RESTO DE MUNICIPIOS": "TAM_RESTO"}, "TABASCO": {"CENTRO": "TCO_CENTRO", "RESTO DE MUNICIPIOS": "TCO_RESTO"}, "TLAXCALA": {"TLAXCALA": "TXC_TLAXCALA", "RESTO DE MUNICIPIOS": "TXC_RESTO"}, "VERACRUZ DE IGNACIO DE LA LLAVE":{"ACAYUCAN": "VER_ACAYUCAN", "COATZACOALCOS": "VER_COATZACOALCOS", "VERACRUZ": "VER_VERACRUZ", "RESTO DE MUNICIPIOS": "VER_RESTO"}, "YUCATÁN": {"MÉRIDA": "YUC_MERIDA", "RESTO DE MUNICIPIOS": "YUC_RESTO"}, "ZACATECAS": {"FRESNILLO": "ZAC_FRESNILLO", "ZACATECAS": "ZAC_ZACATECAS", "RESTO DE MUNICIPIOS": "ZAC_RESTO"}
}

zonas_metropolitanas = {
    "AGUASCALIENTES": "AGS_AGUASCALIENTES_Z", "MEXICALI": "BC_MEXICALI_Z", "TIJUANA": "BC_TIJUANA_Z", "TUXTLA GUTIÉRREZ": "CHP_TUXTLA_GUTIERREZ_Z", "CHIHUAHUA": "CHI_CHIHUAHUA_Z", "JUÁREZ": "CHI_JUAREZ_Z", "VALLE DE MÉXICO": "CDMX_HDO_MX_VALLE_DE_MEXICO_Z", "MONCLOVA FRONTERA": "COA_MONCLOVA_FRONTERA_Z", "PIEDRAS NEGRAS": "COA_PIEDRAS_NEGRAS_Z", "SALTILLO": "COA_SALTILLO_Z", "COLIMA VILLA DE ÁLVAREZ": "COL_COLIMA_VILLA_DE_ALVAREZ_Z", "TECOMÁN": "COL_TECOMAN_Z", "LA LAGUNA": "DGO_COA_LA_LAGUNA_Z", "ACAPULCO": "GRO_ACAPULCO_Z", "CELAYA": "GTO_CELAYA_Z", "LEÓN": "GTO_LEON_Z", "LA PIEDAD PÉNJAMO": "GTO_MCH_LA_PIEDAD_PENJAMO_Z", "MOROLEÓN URIANGATO": "GTO_MOROLEON_URIANGATO_Z", "SAN FRANCISCO DEL RINCÓN": "GTO_SAN_FRANCISCO_DEL_RINCO_Z", "MORELIA": "MCH_MORELIA_Z", "ZAMORA JACONA": "MCH_ZAMORA_JACONA_Z",
    "PACHUCA": "HDO_PACHUCA_Z", "TULA": "HDO_TULA_Z", "TULANCINGO": "HDO_TULANCINGO_Z", "GUADALAJARA": "JCO_GUADALAJARA_Z", "PUERTO VALLARTA": "JCO_NAY_PUERTO_VAYARTA_Z", "OCOTLÁN": "JCO_OCOTLAN_Z", "CUAUTLA": "MOR_CUAUTLA_Z", "CUERNAVACA": "MOR_CUERNAVACA_Z", "TIANGUISTENCO": "MX_TIANGUISTENCO_Z", "TOLUCA": "MX_TOLUCA_Z", "TEPIC": "NAY_TEPIC_Z", "MONTERREY": "NLN_MONTERREY_Z", "OAXACA": "OXA_OAXACA_Z", "TEHUANTEPEC": "OXA_TEHUANTEPEC_Z", "TEHUACÁN": "PUB_TEHUACAN_Z", "PUEBLA TLAXCALA": "PUB_TLX_PUEBLA_TLAXCALA_Z", "CANCÚN": "QRO_CANCUN_Z", "QUERÉTARO": "QTO_QUERETARO_Z", "RÍOVERDE CIUDAD FERNÁNDEZ": "SLP_RIOVERDE_CIUDAD_FERNANDEZ_Z", "SOLEDAD DE GRACIANO SÁNCHEZ": "SLP_SOLEDAD_DE_LA_GRACIA_Z", 
    "GUAYMAS": "SON_GUAYMAS_Z", "MATAMOROS": "TAM_MATAMOROS_Z", "NUEVO LAREDO": "TAM_NUEVO_LAREDO_Z", "REYNOSA RÍO BRAVO": "TAM_REYNOSA_RIO_BRAVO_Z", "VILLAHERMOSA": "TCO_VILLAHERMOSA_Z", "TLAXCALA APIZACO": "TXC_TLAXCALA_APIZACO_Z", "ACAYUCAN": "VER_ACAYUCAN_Z", "COATZACOALCOS": "VER_COATZACOALCOS_Z", "CÓRDOBA": "VER_CORDOBA_Z", "MINATITLÁN": "VER_MINATITLAN_Z", "ORIZABA": "VER_ORIZABA_Z", "POZA RICA": "VER_POZA_RICA_Z", "XALAPA": "VER_XALAPA_Z", "TAMPICO": "TAM_VER_TAMPICO_Z", "MÉRIDA": "YUC_MERIDA_Z", "ZACATECAS GUADALUPE": "ZAC_ZACATECAS_GUADALUPE_Z"
}

municipios_zm = {
    "AGUASCALIENTES": {"AGUASCALIENTES", "JESÚS MARÍA", "SAN FRANCISCO DE LOS ROMO"}, "MEXICALI": {"MEXICALI"}, "TIJUANA": {"PLAYAS DE ROSARITO", "TECATE", "TIJUANA"}, "TUXTLA GUTIÉRREZ": {"BERRIOZÁBAL", "CHIAPA DE CORZO", "TUXTLA GUTIÉRREZ"}, "CHIHUAHUA": {"ALDAMA", "AQUILES SERDÁN", "CHIHUAHUA"}, "JUÁREZ": {"JUARÉZ"}, "VALLE DE MÉXICO": {"ALVARO OBREGÓN", "AZCAPOTZALCO", "BENITO JUAREZ", "COYOACÁN", "CUAJIMALPA DE MORELOS", "CUAUHTÉMOC", "GUSTAVO A. MADERO", "IZTACALCO", "IZTAPALAPA", "LA MAGDALENA CONTRERAS", "MIGUEL HIDALGO", "MILPA ALTA", "TLALPAN", "TLÁHUAC", "VENUSTIANO CARRANZA", "XOCHIMILCO", "TIZAYUCA", "ACOLMAN", "AMECAMECA", "APAXCO", "ATENCO", "ATIZAPÁN DE ZARAGOZA", "ATLAUTLA", "AXAPUSCO", "AYAPANGO", "CHALCO", "CHIAUTLA", "CHICOLOAPAN", "CHICONCUAC", "CHIMALHUACÁN", "COACALCO DE BERRIOZÁBAL", "COCOTITLÁN", "COYOTEPEC", "CUAUTITLÁN", "CUAUTITLÁN IZCALLI", "ECATEPEC DE MORELOS", "ECATZINGO", "HUEHUETOCA", "HUEYPOXTLA", "HUIXQUILUCAN", "ISIDRO FABELA", "IXTAPALUCA", "JALTENCO", "JILOTZINGO", "JUCHITEPEC", "LA PAZ", "MELCHOR OCAMPO", "NAUCALPAN DE JUÁREZ", "NEXTLALPAN", "NEZAHUALCÓYOTL", "NICOLÁS ROMERO", "NOPALTEPEC", "OTUMBA", "OZUMBA", "PAPALOTLA", "SAN MARTÍN DE LAS PIRÁMIDES", "TECÁMAC", "TEMAMATLA", "TEMASCALAPA", "TENANGO DEL AIRE", "TEOLOYUCAN", "TEOTIHUCÁN", "TEPETLAOXTOC", "TEPETLIXPA", "TEPOTZOTLÁN", "TEQUIXQUIAC", "TEXCOCO", "TEZOYUCA", "TLALMANALCO", "TLALNEPANTLA DE BAZ", "TONANITLA", "TULTEPEC", "TULTITLÁN", "VALLE DE CALCO SOLIDARIDAD", "VILLA DEL CARBÓN", "ZUMPANGO"}, 
    "LA LAGUNA": {"MATAMOROS", "TORREÓN", "GÓMEZ PALACIO", "LERDO"}, "MONCLOVA FRONTERA": {"CASTAÑOS", "FRONTERA", "MOCLOVA"}, "PIEDRAS NEGRAS": {"NAVA", "PIEDRAS NEGRAS"}, "SALTILLO": {"ARTEAGA", "RAMOS ARIZPE", "SALTILLO"}, "COLIMA VILLA DE ÁLVAREZ": {"COLIMA", "COMALA", "COQUIMATLÁN", "CUAUHTÉMOC", "VILLA ÁLVAREZ"}, "TECOMÁN": {"ARMERÍA", "TECOMÁN"}, "CELAYA": {"CELAYA", "COMONFORT", "VILLAGÁN"}, "LA PIEDAD PÉNJAMO": {"PÉNJAMO", "LA PIEDAD"}, "LEÓN": {"LEÓN", "SILAO DE LA VICTORIA"}, "MOROLEÓN URIANGATO": {"MOROLEÓN", "URIANGATO"}, "SAN FRANCISCO DEL RINCÓN": {"PURÍSIMA DEL RINCÓN", "SAN FRANCISCO DEL RINCÓN"}, "ACAPULCO": {"ACAPULCO DE JUÁREZ", "COYUCA DE BENÍTEZ"}, "PACHUCA": {"EPAZOYUCAN", "MINERA DE LA REFORMA", "MINERAL DEL MONTE", "PACHUCA DE SOTO", "SAN AGUSTÍN TLAXIACA", "ZAPOTLÁN DE JUÁREZ", "ZEMPOALA"}, "TULA": {"ATITALAQUIA", "ATOTONILCO DE TULA", "TLAHUELILPAN", "TLAXCOAPAN", "TULA DE ALLENDE"}, "TULANCINGO": {"CUAUTEPEC DE HINOJOSA", "SANTIAGO TULANTEPEC DE LUGO GUERRERO", "TULANCINGO DE BRAVO"}, "GUADALAJARA": {"EL SALTO", "GUADALAJARA", "IXTLAHUACÁN DE LOS MEMBRILLOS", "JUANACATLÁN", "SAN PEDRO TLAQUEPAQUE", "TLAJOMULCO DE ZÚÑIGA", "TONALÁ", "ZAPOPAN"}, "OCOTLÁN": {"OCOTLÁN", "PONCITLÁN"}, "PUERTO VALLARTA": {"PUERTO VALLARTA", "BAHÍA DE BANDERAS"}, "MORELIA": {"CHARO", "MORELIA", "TARÍMBARO"}, "ZAMORA JACONA": {"JACONA", "ZAMORA"}, "CUAUTLA": {"ATLATLAHUCAN", "AYALA", "CUAUTLA", "TLAYACAPAN", "YAUTEPEC", "YECAPIXTLA"}, "CUERNAVACA": {"CUERNAVA", "EMILIANO ZAPATA", "HUITZILAC", "JIUTEPEC", "TEMIXCO", "TEPOZTLÁN", "TLALTIZAPÁN DE ZAPATA", "XOCHITEPEC"}, 
    "TIANGUISTENCO": {"ALMOLOYA DEL RÍO", "ATIZAPAN", "CAPULHUAC", "TEXCALYACAC", "TIANGUISTENCO", "XALATLACO"}, "TOLUCA": {"ALMOLOYA DE JUÁREZ", "CALIMAYA", "CHAPULTEPEC", "LERMA", "METEPEC", "MEXICALTZINGO", "OCOYOACAC", "OTZOLOTEPEC", "RAYÓN", "SAN ANTONIO LA ISLA", "SAN MATEO ATENCO", "TEMOAYA", "TOLUCA", "XONACATLÁN", "ZINACANTEPEC"}, "TEPIC": {"TEPIC", "XALISCO"}, "MONTERREY": {"APODACA", "CADEREYTA JIMENÉZ", "EL CARMEN", "GARCÍA", "GENERAL ESCOBEDO", "GUADALUPE", "JUÁREZ", "MONTERREY", "SALINAS VICTORIA", "SAN NICOLÁS DE LOS GARZA", "SAN PEDRO GARZA GARCÍA", "SANTA CATARINA", "SANTIAGO"}, "OAXACA": {"OAXACA DE JUÁREZ", "SAN AGUSTÍN YATARENI", "SAN ANGUSTÍN DE LAS JUNTAS", "SAN ANDRÉS HUAYÁPAM", "SAN ANTONIO DE LA CAL", "SAN BARTOLO COYOTEPEC", "SAN JACINTO AMILPAS", "SAN LORENZO CACAOTEPEC", "SAN LPABLO ETLA", "SANTA CRUZ AMILPAS", "SANTA CRUZ XOXOCOTLÁN", "SANTA LUCÍA DEL CAMINO", "SANTA MARÍA ATZOMPA", "SANTA MARÍA COYOTEPEC", "SANTA MARÍA DEL TULE", "SANTO DOMINGO TOMALTEPEC", "SOLEDAD ETLA", "TLALIXTAC DE CABRERA", "VILLA DE ETLA", "VILLA DE ZAACHILA", "ÁNIMAS TRUJANO"}, "TEHUANTEPEC": {"HEROICA VILLA DE SAN BLAS ATEMPA", "SALINA CRUZ", "SANTO DOMINGO TEHUANTEPEC"}, "PUEBLA TLAXCALA": {"ACAJETE", "AMOZOC", "CHIAUTZINGO", "CORONANGO", "CUAUTLANCINGO", "DOMINGO ARENAS", "HUEJOTZINGO", "JUAN C. BONILLA", "OCOYUCAN", "PUEBLA", "SAN ÁNDRES CHOLULA", "SAN FELIPE TEOTLALCINGO", "SAN GREGORIO ATZOMPA", "SAN MARTÍN TEXMELUCAN", "SAN MIGUEL XOXTLA", "SAN PEDRO CHOLULA", "SAN SALVADOR EL VERDE", "TEPATLAXCO DE HIDALGO", "TLALTENAGO", "ACUAMANALA DE MIGUEL HIDALGO", "IXTACUIXTLA DE MARIANO MATAMOROS", "MAZATECOCHCO DE JOSÉ MARÍA MORELOS", "NATÍVITAS", "PAPALOTLA DE XICOHTÉCANTL", "SAN JERÓNIMO ZACUALPAN", "SAN JUAN HUACTZINCO", "SAN LORENZO AXOCOMANITLA", "SAN PABLO DEL MONTE", "SANTA ANA NOPALUCAN", "SANTA APOLONIA TEACALCO", "SANTA CATARINA AYOMETLA", "SANTA CRUZ QULEHTLA", "TENANCINGO", "TEOLOCHOLCO", "TEPETITLA DE LARDIZÁBAL", "TEPEYANCO", "TETLATLAHUCA", "XICOHTZINCO", "ZACATELCO"}, 
    "TEHUACÁN": {"SANTIAGO MIAHUATLÁN", "TEHUACÁN", "CHIGNAUTLA", "TEZIUTLÁN"}, "QUERÉTARO": {"CORREGIDORA", "EL MARQUÉS", "HUIMILPAN", "QUERÉTARO"}, "CANCÚN": {"BENITO JUÁREZ", "ISLA MUJERES"}, "RÍOVERDE CIUDAD FERNÁNDEZ": {"CIUDAD FERNÁNDEZ", "RIOVERDE"}, "SAN LUIS POTOSÍ-SOLEDAD DE GRACIANO SANCHÉZ": {"SAN LUIS POTOSÍ", "SOLEDAD DE GRACIANO SÁNCHEZ"}, "GUAYMAS": {"EMPALME", "GUAYMAS"}, "VILLAHERMOSA": {"CENTRO", "NACAJUCA"}, "MATAMOROS": {"MATAMOROS"}, "NUEVO LAREDO": {"NUEVO LAREDO"}, "REYNOSA RÍO BRAVO": {"REYNOSA", "RÍO BRAVO"}, "TAMPICO": {"ALTAMIRA", "CIUDAD MADERO", "TAMPICO", "PUEBLO VIEJO", "PÁNUCO"}, "TLAXCALA APIZACO": {"AMAXAC DE GUERRERO", "APETATITLÁN DE ANTONIO CARVAJAL", "APIZACO", "CHIAUTEMPAN", "CONTLA DE JUAN CUAMATZI", "CUAXOMULCO", "LA MAGDALENA TLATELULCO", "PANOTLA", "SAN DAMIÁN TEXÓLOC", "SAN FRANCISCO TETLANOHCAN", "SANTA CRUZ TLAXCALA", "TETLA DE LA SOLIDARIDAD", "TLAXCALA", "TOCATLÁN", "TOTOLAC", "TZOMPANTEPEC", "XALOZTOC", "YAUHQUEMEHCAN"}, "ACAYUCAN": {"ACAYUCAN", "OLUTA", "SOCONUSCO"}, "COATZACOALCOS": {"COATZACOALCOS", "IXHUATLÁN DEL SURESTE", "NANCHITAL DE LÁZARO CÁRDENAS DEL RÍO"}, "CÓRDOBA": {"CÓRDOBA", "FONRÍN", "YANGA"}, "MINATITLÁN": {"CHINAMECA", "COSOLEACAQUE", "JÁLTIPAN", "MINATITLÁN", "OTEAPAN", "ZARAGOZA"}, "ORIZABA": {"ATZACAN", "CAMERINO Z. MENDOZA", "HUILOAPAN DE CUAUHTÉMOC", "IXHUATLANCILLO", "IXTACZOQUITLÁN", "MALTRATA", "MARIANO ESCOBEDO", "NOGALES", "ORIZABA", "RAFAEL DELGADO", "RÍO BLANCO", "TLILAPAN"}, "POZA RICA": {"CAZONES DE HERRERA", "COATZINTLA", "PAPNTLA", "POZA RICA DE HIDALGO", "TIHUATLÁN"}, 
    "XALAPA": {"BANDERILLA", "COATEPEC", "EMILIANO ZAPATA", "JILOTEPEC", "RAFAEL LUCIO", "TLALNEHUAYOCAN", "XALAPA"}, "MÉRIDA": {"CONKAL", "KANASÍN", "MÉRIDA", "UCÚ", "UMÁN"}, "ZACATECAS GUADALUPE": {"GUADALUPE", "MORELOS", "ZACATECAS"}
}

entidad = st.selectbox(
    "ENTIDAD FEDERATIVA",
    options=list(bases.keys())
)

municipio = None
zona_metropolitana = None

#=======================================================================
#NACIONAL -> ZONAS METROPOLITANAS
#=======================================================================

if entidad == "NACIONAL":
    zona_metropolitana = st.selectbox(
        "ZONA METROPOLITANA",
        options=sorted(zonas_metropolitanas.keys()),
        index=None,
        placeholder="SELECCIONA UNA ZONA METROPOLITANA"
    )
    
    if zona_metropolitana:
        municipios = municipios_zm.get(zona_metropolitana, [])
        
        with st.container(border=True):
            st.markdown(
                f"**Municipios que conforman la Zona Metropolitana de {zona_metropolitana}**"
        )
        
            municipios_ordenados = sorted(municipios)
            columnas = st.columns(8)
            
            for i, mun in enumerate(sorted(municipios)):
                col = min(i // 10, 8)
                with columnas[col]:
                    st.markdown(f"- {mun}")

#=======================================================================
#ALCALDIAS
#=======================================================================
#if zona_metropolitana == "VALLE DE MÉXICO":
                    
 #   alcaldias = ["ALVARO OBREGÓN", "AZCAPOTZALCO", "BENITO JUAREZ", "COYOACÁN", "CUAJIMALPA DE MORELOS", "CUAUHTÉMOC", "GUSTAVO A. MADERO", "IZTACALCO", "IZTAPALAPA", "LA MAGDALENA CONTRERAS", "MIGUEL HIDALGO", "MILPA ALTA", "TLALPAN", "TLÁHUAC", "VENUSTIANO CARRANZA", "XOCHIMILCO"]

  #  st.markdown("")

   # with st.container(border=True):
    #    st.markdown(
     #       "*Alcaldías que conforman la Ciudad de México dentro de la Zona Metropolitana del Valle de México**"
      #  )
    
       # columnas_alc =  st.columns(4)
    
        #for i, alc in enumerate(sorted(alcaldias)):
         #   with columnas_alc[i % 4]:
          #      st.markdown(f"- {alc}")

#=======================================================================
#NACIONAL -> MUNICIPIOS DE INTERES
#=======================================================================

else:
    opciones_municipio = list(
        municipios_interes.get(entidad, {}).keys()
    )

    municipio = st.selectbox(
        "MUNICIPIOS DE INTERÉS",
        options=opciones_municipio,
        index=None,
        placeholder="SELECCIONES UN MUNICIPIO"
    )

#=======================================================================
#NACIONAL -> MUNICIPIOS DE INTERES
#=======================================================================
sectores_disponibles = ["TODOS LOS SECTORES", "MANUFACTURAS", "COMERCIO", "SERVICIOS PRIVADOS NO FINANCIEROS", "OTROS SECTORES"]

sectores_no_disponibles = {
    "AGUASCALIENTES": ["OTROS SECTORES"],
    "BAJA CALIFORNIA SUR": ["OTROS SECTORES"],
    "CAMPECHE": ["OTROS SECTORES"],
    "GUERRERO": ["OTROS SECTORES"],
    "HIDALGO": ["OTROS SECTORES"],
    "MORELOS": ["OTROS SECTORES"],
    "TLAXCALA": ["OTROS SECTORES"],
    "ZACATECAS": ["OTROS SECTORES"]
}

for s in sectores_no_disponibles.get(entidad, []):
    if s in sectores_disponibles:
        sectores_disponibles.remove(s)

deshabilitar = municipio is not None or zona_metropolitana is not None

sector = st.selectbox(
    "COBERTURA SECTORIAL",
    options=sectores_disponibles,
    disabled=deshabilitar
)

if deshabilitar:
    sector = "TODOS LOS SECTORES"

#=======================================================================
#FILTROS DEPENDIENDO DEL DOMINIO PARA LOS TAMAÑOS DEL ESTRATO
#=======================================================================
if entidad == "NACIONAL":
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31 y más PERSONAS OCUPADAS"
        ]
    
    elif sector =="MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101 y más PERSONAS OCUPADAS"
        ]

elif entidad == "AGUASCALIENTES":

    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
        ]
        
elif entidad == "BAJA CALIFORNIA":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]                               

elif entidad == "BAJA CALIFORNIA SUR":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
        ]

elif entidad == "CAMPECHE":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]

    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]

    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
        ]        
        
elif entidad == "COAHUILA DE ZARAGOZA":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]        

elif entidad == "COLIMA":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
elif entidad == "CHIAPAS":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
elif entidad == "CHIHUAHUA":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]

    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]

elif entidad == "CIUDAD DE MÉXICO":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101 y más PERSONAS OCUPADAS"
        ]

    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]

elif entidad == "DURANGO":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
elif entidad == "GUANAJUATO":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]         

elif entidad == "GUERRERO":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
        ]      

elif entidad == "HIDALGO":
            
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
        ]
        
elif entidad == "JALISCO":
    
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]    
        
elif entidad == "MÉXICO":

    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]     

elif entidad == "MICHOACÁN DE OCAMPO":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]   

elif entidad == "MORELOS":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
        ]

elif entidad == "NAYARIT":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
elif entidad == "NUEVO LEÓN":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"      
        ]
        
elif entidad == "OAXACA":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"      
        ]        

elif entidad == "PUEBLA":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"     
        ] 
        
elif entidad == "QUERÉTARO":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"   
        ]        

elif entidad == "QUINTANA ROO":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"     
        ]  
        
elif entidad == "SAN LUIS POTOSÍ":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"  
        ]        
        
elif entidad == "SINALOA":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS" 
        ]   
        
elif entidad == "SONORA":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS"   
        ]          

elif entidad == "TABASCO":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS" 
        ]   
        
elif entidad == "TAMAULIPAS":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS" 
        ]  
        
elif entidad == "TLAXCALA":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
        ]  
                       
elif entidad == "VERACRUZ DE IGNACIO DE LA LLAVE":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS" 
        ]                 

elif entidad == "YUCATÁN":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS" 
        ] 
                     
elif entidad == "ZACATECAS":
 
    if sector == "TODOS LOS SECTORES":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "COMERCIO":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "MANUFACTURAS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6 y más PERSONAS OCUPADAS"
        ]
        
    elif sector == "SERVICIOS PRIVADOS NO FINANCIEROS":
        opciones_tamaño = [
            "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3 y más PERSONAS OCUPADAS"
        ]
    
    elif sector == "OTROS SECTORES":
        opciones_tamaño = [
        ]                     
else:
    opciones_tamaño = [
        "TODOS LOS TAMAÑOS", "0-2 PERSONAS OCUPADAS", "3-5 PERSONAS OCUPADAS", "6-10 PERSONAS OCUPADAS", "11-15 PERSONAS OCUPADAS", "16-20 PERSONAS OCUPADAS", "21-30 PERSONAS OCUPADAS", "31-50 PERSONAS OCUPADAS", "51-100 PERSONAS OCUPADAS", "101-250 PERSONAS OCUPADAS", "251 y más PERSONAS OCUPADAS"
    ]
        
if deshabilitar:
    tamano = "TODOS LOS TAMAÑOS"
    
    st.selectbox(
        "PERSONAL OCUPADO",
        options=["TODOS LOS TAMAÑOS"],
        index=0,
        disabled=True
    )

else:
    tamano = st.selectbox(
        "PERSONAL OCUPADO",
        options=opciones_tamaño
    )

mostrar_matriz = st.checkbox("Mostrar Matriz")

if st.button("Construir Tabla"):
    st.session_state["ejecutando"] = True

if st.session_state.get("ejecutando", False):
    with st.spinner("Generando tabla..."):
        try:
            sector_archivo = {
                "TODOS LOS SECTORES": "TOTAL", "MANUFACTURAS": "MANUFACTURAS", "COMERCIO": "COMERCIO", "SERVICIOS PRIVADOS NO FINANCIEROS": "SERVICIOS", "OTROS SECTORES": "OTROS_SECTORES"
            }
            
            tamano_archivo = {
                "TODOS LOS TAMAÑOS": "TOTAL", 
                "0-2 PERSONAS OCUPADAS": "0_2", "3-5 PERSONAS OCUPADAS": "3_5", "6-10 PERSONAS OCUPADAS": "6_10", "11-15 PERSONAS OCUPADAS": "11_15", "16-20 PERSONAS OCUPADAS": "16_20", "21-30 PERSONAS OCUPADAS": "21_30", "31-50 PERSONAS OCUPADAS": "31_50", "51-100 PERSONAS OCUPADAS": "51_100", "101-250 PERSONAS OCUPADAS": "101_250",
                
                "3 y más PERSONAS OCUPADAS": "3_MAS", "6 y más PERSONAS OCUPADAS": "6_MAS", "11 y más PERSONAS OCUPADAS": "11_MAS", "16 y más PERSONAS OCUPADAS": "16_MAS", "21 y más PERSONAS OCUPADAS": "21_MAS", "31 y más PERSONAS OCUPADAS": "31_MAS", "51 y más PERSONAS OCUPADAS": "51_MAS", "101 y más PERSONAS OCUPADAS": "101_MAS", "251 y más PERSONAS OCUPADAS": "251_MAS"   
            }
                
            if municipio:
                codigo_municipios = municipios_interes[entidad][municipio]
                archivo_base = f"{codigo_municipios}.xlsx"
                
            elif zona_metropolitana:
                codigo_zm = zonas_metropolitanas[zona_metropolitana]
                archivo_base = f"{codigo_zm}.xlsx"
                
            else:
                entidad_archivo = bases[entidad].replace("_TOTAL.xlsx", "")
            
                if sector == "TODOS LOS SECTORES" and tamano == "TODOS LOS TAMAÑOS":
                    archivo_base = f"{entidad_archivo}_TOTAL.xlsx"
                else: 
                    archivo_base = (
                        f"{entidad_archivo}_"
                        f"{sector_archivo[sector]}_"
                        f"{tamano_archivo[tamano]}.xlsx"
                    )

            if mostrar_matriz:
                
                ruta_base = CARPETA_BASES / archivo_base
                
                BASE = pd.read_excel(ruta_base)
                
                if zona_metropolitana:
                    titulo_matriz = f"MATRIZ DE TRANSICIÓN - ZONA METROPOLITANA {zona_metropolitana}"
                elif municipio:
                    if entidad == "CIUDAD DE MÉXICO":
                        titulo_matriz = f"MATRIZ DE TRANSICIÓN - ALCALDÍA DE {municipio} DE LA ENTIDAD {entidad}"
                    else:
                        titulo_matriz = f"MATRIZ DE TRANSICIÓN - MUNICIPIO DE {municipio} DE LA ENTIDAD {entidad}"
                else:
                    titulo_matriz = f"MATRIZ DE TRANSICIÓN - {entidad}"
                    
                    if sector != "TODOS LOS SECTORES":
                        titulo_matriz += f" ,SECTOR {sector}"
                        
                    if tamano != "TODOS LOS TAMAÑOS":
                        titulo_matriz += f" ,CON {tamano}"
                        
                st.subheader(titulo_matriz)
                
                st.dataframe(
                    BASE,
                    width="stretch",
                    hide_index=True
                )
                
            #subprocess.run(
             #   [
              #      "python",
               #     str(BASE_DIR / "CALCULOS.py"),
                #    archivo_base
                #],
                #check=True
            #)
            ruta_base = CARPETA_BASES / archivo_base
            
            tabla = obtener_tabla(ruta_base)
            st.session_state["tabla_supervivencia"] = tabla           
            
            archivo_descarga = BytesIO()
            
            with pd.ExcelWriter(
                archivo_descarga,
                engine="openpyxl"
            )  as writer:
                
                tabla.to_excel(
                    writer,
                    sheet_name="Supervivencia",
                    index=False
                )
                
                definiciones = pd.DataFrame({
                    "Simbolo": [
                        "(x)",
                        "S(x)",
                        "p(x)",
                        "q(x)",
                        "d(x)",
                        "E(x)"
                        ],
                        "Definición": [
                        "Edad de los negocios",
                        "Supervivientes a la edad (x)",
                        "Probabilidad de supervivencia a la edad (x)",
                        "Probabilidad de muerte antes de cumplir la edad (x)",
                        "Muertos antes de cumplir la edad (x)",
                        "Esperanza de vida a partir de la edad (x)"
                        ]                        
                })
                
                definiciones.to_excel(
                    writer,
                    sheet_name="Definiciones",
                    index=False
                )
                
            archivo_descarga.seek(0)

        except Exception as e:

            st.error(f"Error: {e}")


        # ----------------------------------------------------------
        # VISUALIZACIÓN EN PANTALLA
        # ----------------------------------------------------------

        if zona_metropolitana:
            titulo = (
                "TABLA DE SUPERVIVENCIA, MORTALIDAD Y ESPERANZA DE VIDA DE LOS NEGOCIOS, "
                f"DE LA ZONA METROPOLITANA {zona_metropolitana.upper()}"
            )
            
        elif municipio:
            if municipio == "RESTO DE MUNICIPIOS":
                titulo = (
                    "TABLA DE SUPERVIVENCIA, MORTALIDAD Y ESPERANZA DE VIDA DE LOS NEGOCIOS, "
                    f"DEL RESTO DE MUNICIPIOS DE LA ENTIDAD "
                    f"{entidad.upper()}"
                )
        
            else: 
                if entidad == "CIUDAD DE MÉXICO":
                    titulo = (
                        "TABLA DE SUPERVIVENCIA, MORTALIDAD Y ESPERANZA DE VIDA DE LOS NEGOCIOS, "
                        f"DE LA ALCALDÍA {municipio.upper()}, "
                        f"DE LA ENTIDAD {entidad.upper()}"
                    )
                    
                else:
                    titulo = (
                        "TABLA DE SUPERVIVENCIA, MORTALIDAD Y ESPERANZA DE VIDA DE LOS NEGOCIOS, "
                        f"DEL MUNICIPIO DE {municipio.upper()}, "
                        f"DE LA ENTIDAD {entidad.upper()}"
                    )
        
        else:
            if entidad == "NACIONAL":
                titulo = (
                    "TABLA DE SUPERVIVENCIA, MORTALIDAD Y ESPERANZA DE VIDA DE LOS NEGOCIOS, "
                    "A NIVEL NACIONAL"
                )
                
            else:
                titulo = (
                    "TABLA DE SUPERVIVENCIA, MORTALIDAD Y ESPERANZA DE VIDA DE LOS NEGOCIOS, "
                    f"DE LA ENTIDAD {entidad.upper()}"                    
                )
            
            if sector != "TODOS LOS SECTORES":
                titulo += f", PERTENECIENTES AL SECTOR {sector.upper()}"
                
            if tamano != "TODOS LOS TAMAÑOS":
                titulo += f", CON {tamano.upper()}"

        st.subheader(titulo)

        st.dataframe(
            tabla.style.format({
                "S(x)": "{:.0f}",
                "d(x)": "{:.0f}",
                "p(x)": "{:.4f}",
                "q(x)": "{:.4f}",
                "E(x)": "{:.1f}",
            }),
            width="stretch",
            hide_index=True
        )
        
        #==============================================================================
        #INDICADORES CONDICIONALES
        #==============================================================================
        st.markdown("---")
        st.subheader("INDICADORES DEMOGRÁFICOS CONDICIONALES")

        indicador = st.selectbox(
            "Seleccione un indicador",
            [
                "1. Probabilidad de supervivencia",
                "2. Probabilidad de mortalidad",
                "3. Supervivencia y muerte al año siguiente",
                "4. Supervivencia en un intervalo futuro",
                "5. Mortalidad en un intervalo futuro",
                "6. Esperanza de vida futura"
            ],
            key="selector_indicador"
        )
        
        #========================================================
        #PRIMER INDICADOR "PROBABILIDAD DE SUPERVIVENCIA"
        #========================================================
        if indicador == "1. Probabilidad de supervivencia":
            col1, col2, col3 = st.columns(3)
            with col1:
                edad_actual = st.selectbox(
                    "Edad actual del negocio (x)",
                    options=tabla["(x)"].tolist(),
                    key="edad_supervivencia"
                )
        
            with col2:
                n = st.number_input(
                    "Años futuros (n)",
                    min_value=1,
                    value=1,
                    step=1,
                    key="n_supervivencia"
                )
                
            with col3:
                st.empty()
                
            edad_futura = edad_actual + n
            
            fila_x = tabla[tabla["(x)"] == edad_actual]
            fila_xn = tabla[tabla["(x)"] == edad_futura]
            
            if fila_x.empty or fila_xn.empty:
                st.warning(
                    f"No existe información para la edad {edad_futura}"
                )
            else: 
                sx = fila_x["S(x)"].iloc[0]
                sxn = fila_xn["S(x)"].iloc[0]
                
                probabilidad = sxn / sx
                
                st.metric(
                    label=f"Probabiliad de que un negocio sobreviva a una edad futura de {edad_futura} años, dado que actualmente tiene {edad_actual} años, es de:",
                    value=f"{probabilidad:.4f}"
                )
                
                #st.markdown(
                 #   f"""
                  #  **Fórmula**
                    
                   # P({edad_futura}|{edad_actual}) =
                    #S({edad_futura}) / S({edad_actual})
                    
                    #= {int(sxn):,} / {int(sx):,}
                    
                    #= {probabilidad:.4f}
                    #"""
                #)

        #========================================================
        #SEGUNDO INDICADOR "PROBABILIDAD DE MORTALIDAD"
        #========================================================                
        elif indicador == "2. Probabilidad de mortalidad":
            col1, col2, col3 = st.columns(3)
            with col1:
                edad_actual = st.selectbox(
                "Edad actual del negocio (x)",
                options=tabla["(x)"].tolist(),
                key="edad_mortalidad"
            )
                
            with col2:
                n = st.number_input(
                    "Años futuros (n)",
                    min_value=1,
                    value=1,
                    step=1,
                    key="n_mortalidad"
                )
            
            with col3:
                st.empty()
                
            edad_futura = edad_actual + n
            
            fila_x = tabla[tabla["(x)"] == edad_actual]
            fila_xn = tabla[tabla["(x)"] == edad_futura]
            
            if fila_x.empty or fila_xn.empty:
                st.warning(
                    f"No existe información para la edad {edad_futura}"
                )
                
            else:
                sx = fila_x["S(x)"].iloc[0]
                sxn = fila_xn["S(x)"].iloc[0]
                
                probabilidad_mortalidad = 1 - (sxn / sx)
                
                st.metric(
                    label=f"Probabilidad de que un negocio muera a una edad futura de {edad_futura} años, dado que actualmente tiene {edad_actual} años, es de:",
                    value=f"{probabilidad_mortalidad:.4f}"
                )
                
                #st.markdown(
                 #   f"""
                  #  **Fórmula**
                    
                   # q({edad_futura}|{edad_actual}) =
                   #1 - S({edad_futura}) / S({edad_actual})
                    
                   # = 1 - ({int(sxn):,} / {int(sx):,})
                    
                    #= {probabilidad_mortalidad:.4f}
                    #"""
                #)
                
        #========================================================
        #TERCER INDICADOR "SUPERVIVENCIA Y MUERTE AL AÑO SIGUIENTE"
        #========================================================                
        elif indicador == "3. Supervivencia y muerte al año siguiente":
            col1, col2, col3 = st.columns(3)
            with col1:
                edad_actual = st.selectbox(
                "Edad actual del negocio (x)",
                options=tabla["(x)"].tolist(),
                key="edad_muerte_intervalo"
            )
                
            with col2:
                n = st.number_input(
                    "Años futuros (n)",
                    min_value=1,
                    value=1,
                    step=1,
                    key="n_muerte_intervalo"
                )
                
            with col3:
                st.empty()
                
            edad_futura = edad_actual + n
            
            fila_x = tabla[tabla["(x)"] == edad_actual]
            fila_xn = tabla[tabla["(x)"] == edad_futura]
            
            if fila_x.empty or fila_xn.empty:
                st.warning(
                    f"No existe información para la edad {edad_futura}"
                )
                
            else:
                sx = fila_x["S(x)"].iloc[0]
                dxn = fila_xn["d(x)"].iloc[0]
                
                probabilidad_sup_mue = dxn / sx
                
                st.metric(
                    label=f"Probabilidad de que un negocio sobreviva a la edad futura de {edad_futura} años, y muera al año siguiente, dado que actualmente tiene {edad_actual} años, es de:",
                    value=f"{probabilidad_sup_mue:.4f}"
                )
                
                #st.markdown(
                 #   f"""
                  #  **Fórmula**
                    
                   # q({edad_futura}|{edad_actual}) =
                   # d({edad_futura}) / S({edad_actual})
                    
                   # = {int(dxn):,} / {int(sx):,}
                    
                   # = {probabilidad_sup_mue:.4f}
                    #"""
                #)   

        #========================================================
        #CUARTO INDICADOR "SUPERVIVENCIA EN UN INTERVALO FUTURO"
        #========================================================
        elif indicador == "4. Supervivencia en un intervalo futuro":
            col1, col2, col3 = st.columns(3)
            with col1:
                edad_actual = st.selectbox(
                "Edad actual del negocio (x)",
                options=tabla["(x)"].tolist(),
                key="edad_supervivencia_intervalo"
            )
                
            with col2:
                n = st.number_input(
                    "Años futuros (n)",
                    min_value=1,
                    value=1,
                    step=1,
                    key="n_supervivencia_intervalo"
                )
            
            with col3:
                m = st.number_input(
                "Amplitud del intervalo (m)",
                min_value=1,
                value=1,
                step=1,
                key="m_supervivencia_intervalo"
            )             

            edad_1 = edad_actual + n
            edad_2 = edad_actual + n + m
            
            fila_x = tabla[tabla["(x)"] == edad_actual]
            fila_x1 = tabla[tabla["(x)"] == edad_1]
            fila_x2 = tabla[tabla["(x)"] == edad_2]
            
            if fila_x.empty or fila_x1.empty or fila_x2.empty:
                st.warning("No se encontraron datos para alguna de las edades seleccionadas.")

            else:
                sx = fila_x["S(x)"].iloc[0]
                sxn = fila_x1["S(x)"].iloc[0]
                sxnm = fila_x2["S(x)"].iloc[0]
                
                probabilidad_supervivencia = ((sxn + sxnm) / 2) / sx
                
                st.metric(
                    label=f"Probabilidad de que un negocio sobreviva en un intervalo futuro de edades [{edad_1}, {edad_2}], dado que actualmente tiene {edad_actual} años, es de:",
                    value=f"{probabilidad_supervivencia:.4f}"
                )
                    
                #st.markdown(
                 #   f"""
                  #  **Fórmula**
                    
                   # P({edad_1},{edad_2}|{edad_actual}) =
                    #([S({edad_1}) + S({edad_2})] / 2) / S({edad_actual})
                    
                    #= (({int(sxn):,} + {int(sxnm):,}) / 2) / {int(sx):,}
                    
                    #= {probabilidad_supervivencia:.4f}
                    #"""
            #)
                
        #========================================================
        #QUINTO INDICADOR "MORTALIDAD EN UN INTERVALO FUTURO"
        #========================================================
        elif indicador == "5. Mortalidad en un intervalo futuro":
            col1, col2, col3 = st.columns(3)
            with col1:
                edad_actual = st.selectbox(
                "Edad actual del negocio (x)",
                options=tabla["(x)"].tolist(),
                key="edad_mortalidad_intervalo"
            )
                
            with col2:
                n = st.number_input(
                    "Años futuros (n)",
                    min_value=1,
                    value=1,
                    step=1,
                    key="n_mortalidad_intervalo"
                )
            
            with col3:
                m = st.number_input(
                "Amplitud del intervalo (m)",
                min_value=1,
                value=1,
                step=1,
                key="m_mortalidad_intervalo"
            )
            
            edad_1 = edad_actual + n
            edad_2 = edad_actual + n + m
            
            fila_x = tabla[tabla["(x)"] == edad_actual]
            fila_x1 = tabla[tabla["(x)"] == edad_1]
            fila_x2 = tabla[tabla["(x)"] == edad_2]
            
            if fila_x.empty or fila_x1.empty or fila_x2.empty:
                st.warning("No se encontraron datos para alguna de las edades seleccionadas.")
                
            else:
                sx = fila_x["S(x)"].iloc[0]
                sxn = fila_x1["S(x)"].iloc[0]
                sxnm = fila_x2["S(x)"].iloc[0]
                            
                probabilidad_mortalidad_2 = 1- (((sxn + sxnm) / 2) / sx)
                            
                st.metric(
                    label=f"Probabilidad de que un negocio muera en un intervalo futuro de edades [{edad_1}, {edad_2}], dado que actualmente tiene {edad_actual} años, es de:",
                    value=f"{probabilidad_mortalidad_2:.4f}"
                ) 
                
                #st.markdown(
                #    f"""
                 #   **Fórmula**
                    
                  #  q({edad_1},{edad_2}|{edad_actual}) =
                   # 1 - ([S({edad_1}) + S({edad_2})] / 2) / S({edad_actual})
                    #= 1 - (({int(sxn):,} + {int(sxnm):,}) / 2) / {int(sx):,}
                    
                    #= {probabilidad_mortalidad_2:.4f}
                    #"""
                #)
                
        #========================================================
        #SEXTO INDICADOR "ESPERANZA DE VIDA FUTURA"
        #========================================================
        elif indicador == "6. Esperanza de vida futura":
            col1, col2, col3 = st.columns(3)
            with col1:
                edad_actual = st.selectbox(
                "Edad actual del negocio (x)",
                options=tabla["(x)"].tolist(),
                key="edad_esperanza_futura"
            )
                
            with col2:
                n = st.number_input(
                    "Años futuros (n)",
                    min_value=1,
                    value=1,
                    step=1,
                    key="n_esperanza_futura"
                )
            
            with col3:
                st.empty()
                
            edad_futura = edad_actual + n

            fila_x = tabla[tabla["(x)"] == edad_actual]
            fila_xn = tabla[tabla["(x)"] == edad_futura]
                        
            if fila_x.empty or fila_xn.empty:
                
                st.warning(
                    f"No existe información para la edad {edad_futura}"
                )
            
            else:
                ex = fila_x["E(x)"].iloc[0]
                exn = fila_xn["E(x)"].iloc[0]
                
                nae = exn - ex
                
                st.metric(
                    label=f"Número de años futuros que se espera sobreviva un negocio entre la edad actual {edad_actual}, y la edad final {edad_futura}, es de:",
                    value=f"{nae:.2f}"
                )
                
                #st.markdown(
                 #   f"""
                  #  **Fórmula**
                    
                   # NAE = E({edad_futura}) - E({edad_actual})
                   # = {exn:.2f} - {ex:.2f}
                    #= {nae:.2f}
                    #"""
                #)
        #==============================================================================
        #==============================================================================

        st.markdown("---")

        col1, col2 = st.columns([1, 2])

        with col1:
            with st.container(border=True):

                st.markdown(
                    """
                    **Definiciones**
                    - **(x)** = Edad de los negocios
                    - **S(x)** = Supervivientes a la edad (x)
                    - **p(x)** = Probabilidad de supervivencia a la edad (x)
                    - **q(x)** = Probabilidad de muerte antes de cumplir la edad (x)
                    - **d(x)** = Muertos antes de cumplir la edad (x)
                    - **E(x)** = Esperanza de vida a partir de la edad (x)
                    """
                )

        st.download_button(
            label="Descargar Excel",
            data=archivo_descarga,
            file_name=(
                f"Supervivencia, mortalidad y esperanza de vida_{entidad}_{sector}_{tamano}.xlsx"
            ),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
elif "tabla_supervivencia" in st.session_state:
    tabla = st.session_state["tabla_supervivencia"]
