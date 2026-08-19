import requests
from bs4 import BeautifulSoup
import re
import streamlit as st
import pandas as pd 

st.set_page_config(layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

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

st.markdown("""
<style>
div.stButton > button {
    background-color: rgb(120,154,61);
    color: white;
    font-size: 20px;
    font-weight: 700;
    height: 60px;
    border-radius: 10px;
    border: none;
}

div.stButton > button:hover {
    background-color: rgb(100,134,41);
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

    # ----------------------------------------------------
    # Clasificación exclusiva para MIPYMES Rurales
    # ----------------------------------------------------
    if monto_credito is not None:

        if (
            activos_totales <= activo_Mipymes_rurales
            and ingresos_brutos_anuales <= ingreso_Mipymes_rurales
            and monto_bajo_Mipymes_rurales < monto_credito < monto_alto_Mipymes_rurales
        ):
            return "MIPYMES Rurales Microempresa"

        return "No clasificado"

    # ----------------------------------------------------
    # Clasificación tradicional
    # ----------------------------------------------------
    if (
        ingresos_brutos_anuales <= ingreso_bajo
        and activos_totales <= activo_bajo
    ):
        return "Pequeño Productor de Ingresos Bajos"

    elif (
        ingreso_bajo < ingresos_brutos_anuales <= ingreso_medio
        and activos_totales <= activo_bajo
    ):
        return "Pequeño Productor"

    elif (
        (
            ingreso_medio < ingresos_brutos_anuales <= ingreso_alto
            and activos_totales <= activo_medio
        )
        or
        (
            ingresos_brutos_anuales <= ingreso_medio
            and activo_bajo < activos_totales <= activo_medio
        )
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

st.markdown("""
<h1 style="
    font-size:38px;
    color:#edb946;
">
📋 Reglas de Clasificación
</h1>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="reglas">
        {condiciones.to_html(index=False)}
    </div>
    """,
    unsafe_allow_html=True
)


# ----------------------------------------------------
# Estilos de la Calculadora y Resultado
# ----------------------------------------------------
st.markdown("""
<style>

/* Valor principal dentro del input */
div[data-testid="stNumberInput"] input {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #002646 !important;
}

/* Botones + y - */
div[data-testid="stNumberInput"] button {
    font-size: 22px !important;
    font-weight: bold !important;
}

/* Etiquetas de los campos */
.label-calculadora {
    font-size: 18px;
    font-weight: 600;
    color: rgb(120,154,61);
    margin-bottom: 10px;
}

/* Resultado */
.resultado-card {
    background-color: #eef7ec;
    border-left: 8px solid rgb(120,154,61);
    border-radius: 12px;
    padding: 25px;
    margin-top: 20px;
}

.resultado-titulo {
    font-size: 36px;
    font-weight: 700;
    color: rgb(120,154,61);
    margin-bottom: 15px;
}

.resultado-info {
    font-size: 22px;
    font-weight: 600;
    color: #002646;
    line-height: 2;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# Tarjeta de la Calculadora
# ----------------------------------------------------
with st.container(border=True):

    st.markdown("""
    <h1 style="
        font-size:38px;
        color:#edb946;
        margin-bottom:25px;
    ">
        🧮 Calculadora
    </h1>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="label-calculadora">Ingresos Brutos Anuales</div>',
            unsafe_allow_html=True
        )

        ingresos = st.number_input(
            "Ingresos",
            min_value=0.0,
            step=1_000_000.0,
            format="%.0f",
            label_visibility="collapsed"
        )

    with col2:

        st.markdown(
            '<div class="label-calculadora">Activos Totales</div>',
            unsafe_allow_html=True
        )

        activos = st.number_input(
            "Activos",
            min_value=0.0,
            step=1_000_000.0,
            format="%.0f",
            label_visibility="collapsed"
        )

    with col3:

        st.markdown(
            '<div class="label-calculadora">Monto Crédito (Aplica para evaluar Mipymes)</div>',
            unsafe_allow_html=True
        )

        monto_credito = st.number_input(
            "Monto",
            min_value=0.0,
            step=1_000_000.0,
            format="%.0f",
            label_visibility="collapsed"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🚀 CLASIFICAR PRODUCTOR",
        use_container_width=True
    ):

        monto = None if monto_credito == 0 else monto_credito

        resultado = clasificar_productor(
            ingresos,
            activos,
            monto
        )

        st.success(f"✅ {resultado}")

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="💰 Ingresos",
                value=f"${ingresos:,.0f}"
            )
        
        with col2:
            st.metric(
                label="🏦 Activos",
                value=f"${activos:,.0f}"
            )
        
        with col3:
            st.metric(
                label="📋 Monto crédito",
                value=f"${monto_credito:,.0f}"
            )
