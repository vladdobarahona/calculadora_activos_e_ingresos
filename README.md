Calculadora de Activos e Ingresos 

Aplicación desarrollada en Streamlit para la clasificación de productores según los criterios de ingresos, activos y monto de crédito definidos a partir del valor UVB (Unidad de Valor Básico) vigente.

La aplicación consulta automáticamente el valor UVB publicado en UVB Colombia, calcula los umbrales correspondientes y determina la clasificación del productor de acuerdo con las reglas parametrizadas.

Características
Consulta automática del UVB vigente.
Visualización de la resolución que soporta el valor UVB.
Tabla detallada de reglas de clasificación.
Cálculo automático de umbrales utilizando el UVB vigente.
Clasificación de productores según:
Pequeño Productor de Ingresos Bajos
Pequeño Productor
Mediano Productor
Gran Productor
MIPYMES Rurales Microempresa
Interfaz web sencilla desarrollada en Streamlit.
Actualización automática cuando cambie el UVB publicado.
Tecnologías utilizadas
Python 3.x
Streamlit
Pandas
Requests
BeautifulSoup4


Instalación local

Clonar repositorio

git clone https://github.com/usuario/calculadora-activos-ingresos.git

cd calculadora-activos-ingresos



Crear entorno virtual

Windows


python -m venv venv
venv\Scripts\activate


Linux / Mac

python -m venv venv
source venv/bin/activate



Instalar dependencias

pip install -r requirements.txt

Ejecución

streamlit run app.py


La aplicación estará disponible en:

http://localhost:8501


Dependencias

Archivo requirements.txt

streamlit
pandas
requests
beautifulsoup4
lxml



Funcionamiento

1. Obtención del UVB

Al iniciar la aplicación:

Se consulta automáticamente el portal UVB Colombia.
Se obtiene:
Título de la vigencia.
Valor UVB.
Resolución asociada.
Enlace oficial de consulta.

Ejemplo:

Valor UVB 2026 Colombia
$12.110
Resolución 3488 de 2025

2. Cálculo de umbrales

A partir del UVB vigente se calculan automáticamente los límites utilizados para la clasificación.

Ejemplo:

ingreso_bajo = 5302 * UVB
ingreso_medio = 14844 * UVB
ingreso_alto = 288402 * UVB


3. Clasificación

El usuario ingresa:

Ingresos brutos anuales
Activos totales
Monto de crédito (opcional)

La aplicación evalúa las condiciones y genera una clasificación.

Reglas de clasificación
Pequeño Productor de Ingresos Bajos
Ingresos ≤ Ingreso Bajo
Activos ≤ Activo Bajo
Pequeño Productor
Ingreso Bajo < Ingresos ≤ Ingreso Medio
Activos ≤ Activo Bajo
Mediano Productor

Condición 1:

Ingreso Medio < Ingresos ≤ Ingreso Alto
Activos ≤ Activo Medio

Condición 2:

Ingresos ≤ Ingreso Medio
Activo Bajo < Activos ≤ Activo Medio
Gran Productor

Condición 1:

Ingresos > Ingreso Alto

Condición 2:

Ingresos ≤ Ingreso Alto
Activos > Activo Medio
MIPYMES Rurales Microempresa
Ingresos ≤ Ingreso MIPYMES
Activos ≤ Activo MIPYMES
Crédito dentro del rango definido para Microempresa Rural


Estructura del proyecto

calculadora-activos-ingresos/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
└── config.toml



Despliegue en Streamlit Community Cloud
1.Publicar el proyecto en GitHub.
2. Ingresar a Streamlit Community Cloud.
3. Crear una nueva aplicación.
4. Seleccionar:
    Repositorio.
    Rama principal.
    Archivo app.py.
5. Desplegar.

No se requiere Selenium ni ChromeDriver para el funcionamiento de la aplicación.

Autor

Vladimir Alonso Barahona Palacios

Profesional Máster

Licencia

Este proyecto se distribuye para fines corporativos y académicos según las políticas internas de la organización.
