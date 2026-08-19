import streamlit as st
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# ----------------------------------------------------
# Obtener UVB vigente
# ----------------------------------------------------
@st.cache_data(ttl=86400)
def obtener_uvb():

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://uvb.com.co/")
        driver.implicitly_wait(10)

        container = driver.find_element(
            By.XPATH,
            '//*[@id="genesis-content"]/article/div/div[1]/div[1]'
        )

        parts = container.text.split("\n")

        title = parts[0] if len(parts) > 0 else ""
        value = parts[1] if len(parts) > 1 else ""
        resolution = parts[2] if len(parts) > 2 else ""

        uvb = int(''.join(filter(str.isdigit, value)))

        link_element = container.find_element(By.TAG_NAME, "a")

        resolution_title = link_element.text
        resolution_url = link_element.get_attribute("href")

        return {
            "title": title,
            "value": value,
            "uvb": uvb,
            "resolution": resolution,
            "resolution_title": resolution_title,
            "resolution_url": resolution_url
        }

    finally:
        driver.quit()


# ----------------------------------------------------
# Clasificación
# ----------------------------------------------------
def clasificar_productor(
        ingresos_brutos_anuales,
        activos_totales,
        monto_credito=None):

    if ingresos_brutos_anuales <= ingreso_bajo and activos_totales <= activo_bajo:
        return "Pequeño Productor de Ingresos Bajos"

    elif ingreso_bajo < ingresos_brutos_anuales <= ingreso_medio and activos_totales <= activo_bajo:
        return "Pequeño Productor"

    elif (
        ingreso_medio < ingresos_brutos_anuales <= ingreso_alto
        and activos_totales <= activo_medio
    ) or (
        ingresos_brutos_anuales <= ingreso_medio
        and activo_bajo < activos_totales <= activo_medio
    ):
        return "Mediano Productor"

    elif (
        ingresos_brutos_anuales > ingreso_alto
        or (
            ingresos_brutos_anuales <= ingreso_alto
            and activos_totales > activo_medio
        )
    ):
        return "Gran Productor"

    elif (
        monto_credito is not None
        and activos_totales <= activo_Mipymes_rurales
        and ingresos_brutos_anuales <= ingreso_Mipymes_rurales
        and monto_bajo_Mipymes_rurales < monto_credito < monto_alto_Mipymes_rurales
    ):
        return "MIPYMES Rurales Microempresa"

    return "No clasificado"


# ----------------------------------------------------
# Interfaz
# ----------------------------------------------------
st.set_page_config(
    page_title="Calculadora Activos e Ingresos Enterprise",
    layout="wide"
)

st.title("📊 Calculadora de Activos e Ingresos Enterprise")

data = obtener_uvb()

st.success(f"Vigencia: {data['title']}")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Valor UVB",
        data["value"]
    )

with col2:
    st.link_button(
        data["resolution_title"],
        data["resolution_url"]
    )

uvb = data["uvb"]

# ----------------------------------------------------
# Umbrales
# ----------------------------------------------------
ingreso_bajo = 5302 * uvb
ingreso_medio = 14844 * uvb
ingreso_alto = 288402 * uvb

activo_bajo = 47714 * uvb
activo_medio = 530150 * uvb

ingreso_Mipymes_rurales = 101907 * uvb
activo_Mipymes_rurales = 47714 * uvb

monto_bajo_Mipymes_rurales = 712 * uvb
monto_alto_Mipymes_rurales = 2968 * uvb


# ----------------------------------------------------
# Tabla resumen
# ----------------------------------------------------
st.subheader(
    f"Resumen de umbrales - {data['title']}"
)

tabla = pd.DataFrame(
    [
        ["Ingreso Bajo", f"${ingreso_bajo:,.0f}"],
        ["Ingreso Medio", f"${ingreso_medio:,.0f}"],
        ["Ingreso Alto", f"${ingreso_alto:,.0f}"],
        ["Activo Bajo", f"${activo_bajo:,.0f}"],
        ["Activo Medio", f"${activo_medio:,.0f}"],
        ["Ingreso MIPYMES Rurales", f"${ingreso_Mipymes_rurales:,.0f}"],
        ["Activo MIPYMES Rurales", f"${activo_Mipymes_rurales:,.0f}"],
        ["Monto mínimo MIPYMES", f"${monto_bajo_Mipymes_rurales:,.0f}"],
        ["Monto máximo MIPYMES", f"${monto_alto_Mipymes_rurales:,.0f}"],
    ],
    columns=["Concepto", "Valor"]
)

st.dataframe(
    tabla,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------
# Condiciones
# ----------------------------------------------------
st.subheader("Reglas de Clasificación")

condiciones = pd.DataFrame(
    [
        [
            "Pequeño Productor de Ingresos Bajos",
            f"Ingresos ≤ ${ingreso_bajo:,.0f} y Activos ≤ ${activo_bajo:,.0f}"
        ],
        [
            "Pequeño Productor",
            f"Ingresos > ${ingreso_bajo:,.0f} y ≤ ${ingreso_medio:,.0f} con Activos ≤ ${activo_bajo:,.0f}"
        ],
        [
            "Mediano Productor",
            "Ingresos o activos dentro de rangos medios"
        ],
        [
            "Gran Productor",
            "Ingresos o activos superiores a los límites medios"
        ],
        [
            "MIPYMES Rurales Microempresa",
            f"Ingresos ≤ ${ingreso_Mipymes_rurales:,.0f}, Activos ≤ ${activo_Mipymes_rurales:,.0f} y Crédito entre ${monto_bajo_Mipymes_rurales:,.0f} y ${monto_alto_Mipymes_rurales:,.0f}"
        ]
    ],
    columns=["Clasificación", "Condición"]
)

st.dataframe(
    condiciones,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------
# Calculadora
# ----------------------------------------------------
st.subheader("Calculadora")

col1, col2, col3 = st.columns(3)

with col1:
    ingresos = st.number_input(
        "Ingresos Brutos Anuales",
        min_value=0.0,
        step=1000000.0
    )

with col2:
    activos = st.number_input(
        "Activos Totales",
        min_value=0.0,
        step=1000000.0
    )

with col3:
    monto_credito = st.number_input(
        "Monto Crédito (Opcional)",
        min_value=0.0,
        value=0.0,
        step=1000000.0
    )

if st.button("Clasificar"):

    monto = (
        None
        if monto_credito == 0
        else monto_credito
    )

    resultado = clasificar_productor(
        ingresos,
        activos,
        monto
    )

    st.success(
        f"Clasificación obtenida: {resultado}"
    )
