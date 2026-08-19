import requests
from bs4 import BeautifulSoup
import re
import streamlit as st
import pandas as pd 

# ==============================
# Estilos personalizados
# ==============================
st.markdown("""
<style>
    /* Fondo de toda la aplicación */
    .stApp {
        background: #ffffff !important;
        font-family: "Segoe UI", "Cochin bold", "Helvetica Neue", sans-serif;
        padding-top: 20px;
    }

    /* Título principal */
    .main-title {
        color: rgb(120,154,61);
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.25;
        margin-top: 15px;
        margin-bottom: 0px;
    }

    /* Subtítulo */
    .sub-title {
        color: #4a4a4a;
        font-size: 1.1rem;
        margin-top: -5px;
        margin-bottom: 25px;
    }

    /* Fondo general de la página (fuera del contenedor blanco) */
    body {
        background-color: rgb(171,190,76) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==============================
# LOGO + TÍTULO
# ==============================
col1, col2 = st.columns([1, 3])

with col1:
    st.image(
        "https://www.finagro.com.co/sites/default/files/logo-front-finagro.png",
        width=180
    )

with col2:
    st.markdown(
        """
        <h1 class="main-title">
            Calculadora Activos e Ingresos FINAGRO 2026
        </h1>
        <div class="sub-title">
            ⚠️ Este calculo es indicativo y no obliga a ninguna entidad a que se obtenga el mismo resultado cuando se registre el crédito.
        </div>
        """,
        unsafe_allow_html=True
    )


def obtener_uvb():

    url = "https://uvb.com.co/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    container = soup.select_one(
        "#genesis-content article > div > div:nth-of-type(1) > div:nth-of-type(1)"
    )

    if not container:
        raise Exception("No fue posible localizar el contenedor UVB")

    texto = container.get_text("\n", strip=True)

    parts = texto.split("\n")

    title = parts[0] if len(parts) > 0 else ""
    value = parts[1] if len(parts) > 1 else ""
    resolution = parts[2] if len(parts) > 2 else ""

    uvb = int(re.sub(r"\D", "", value))

    link = container.find("a")

    resolution_title = link.get_text(strip=True) if link else resolution
    resolution_url = link.get("href") if link else ""

    return {
        "title": title,
        "value": value,
        "uvb": uvb,
        "resolution": resolution,
        "resolution_title": resolution_title,
        "resolution_url": resolution_url,
    }

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
# Condiciones
# ----------------------------------------------------
st.markdown("""
<style>
.reglas table {
    font-size: 18px;
    width: 100%;
}

.reglas th {
    font-size: 16;
    font-weight: bold;
    text-align: center;
}

.reglas td {
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)


condiciones = pd.DataFrame(
    [
        [
            "Pequeño Productor de Ingresos Bajos",
            f"≤ ${ingreso_bajo:,.0f}",
            f"≤ ${activo_bajo:,.0f}",
            "No aplica"
        ],
        [
            "Pequeño Productor",
            f"> ${ingreso_bajo:,.0f} y ≤ ${ingreso_medio:,.0f}",
            f"≤ ${activo_bajo:,.0f}",
            "No aplica"
        ],
        [
            "Mediano Productor",
            f"> ${ingreso_medio:,.0f} y ≤ ${ingreso_alto:,.0f}",
            f"≤ ${activo_medio:,.0f}",
            "No aplica"
        ],
        [
            "Mediano Productor",
            f"≤ ${ingreso_medio:,.0f}",
            f"> ${activo_bajo:,.0f} y ≤ ${activo_medio:,.0f}",
            "No aplica"
        ],
        [
            "Gran Productor",
            f"> ${ingreso_alto:,.0f}",
            "Cualquiera",
            "No aplica"
        ],
        [
            "Gran Productor",
            f"≤ ${ingreso_alto:,.0f}",
            f"> ${activo_medio:,.0f}",
            "No aplica"
        ],
        [
            "MIPYMES Rurales Microempresa",
            f"≤ ${ingreso_Mipymes_rurales:,.0f}",
            f"≤ ${activo_Mipymes_rurales:,.0f}",
            f"> ${monto_bajo_Mipymes_rurales:,.0f} y < ${monto_alto_Mipymes_rurales:,.0f}"
        ]
    ],
    columns=[
        "Clasificación",
        "Ingresos",
        "Activos",
        "Monto Crédito"
    ]
)

st.subheader("📋 Reglas de Clasificación")

st.markdown(
    f"""
    <div class="reglas">
        {condiciones.to_html(index=False)}
    </div>
    """,
    unsafe_allow_html=True
)
# ----------------------------------------------------
# Calculadora
# ----------------------------------------------------
st.markdown("""
<h1 style="
    font-size:42px;
    color:#0068c9;
">
🧮 Calculadora
</h1>
""", unsafe_allow_html=True)

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
