import streamlit as st
import pandas as pd
import os

# Configuración de página
st.set_page_config(page_title="Outland Logistics - Cotizador", page_icon="📦", layout="wide")

# Estilos CSS - Modo Oscuro Ejecutivo Outland Logistics
st.markdown("""
<style>
/* Fondo principal negro profundo */
.stApp {
    background-color: #121212 !important;
    color: #FFFFFF !important;
}

/* Sidebar en tono gris oscuro contrastante */
[data-testid="stSidebar"] {
    background-color: #1E1E1E !important;
}

/* Títulos y encabezados en blanco puro y tipografía limpia */
h1, h2, h3, h4, h5, h6, label, p, span {
    color: #FFFFFF !important;
    font-family: 'Segoe UI', Roboto, Helvetica, sans-serif !important;
}

/* Subtítulos de ayuda / capturas en gris claro */
.stCaption {
    color: #B0B0B0 !important;
}

/* Botón Principal en Naranja Oficial Outland */
.stButton>button {
    background-color: #F38218 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    height: 3.2em !important;
    width: 100% !important;
    box-shadow: 0px 4px 10px rgba(243, 130, 24, 0.3);
}
.stButton>button:hover {
    background-color: #FF9429 !important;
    color: #FFFFFF !important;
    box-shadow: 0px 6px 15px rgba(243, 130, 24, 0.5);
}

/* Ajuste de cajas de texto e inputs para modo oscuro */
input {
    background-color: #2A2A2A !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
}

/* Tarjetas de Métricas / Resultados */
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    color: #F38218 !important;
    font-weight: bold !important;
}
[data-testid="stMetricLabel"] {
    color: #E0E0E0 !important;
}
</style>
""", unsafe_allow_html=True)

# Detección del logo oficial (Outland)
logo_file = None
for item in os.listdir("."):
    if item.lower().startswith("outland") and (item.lower().endswith(".png") or item.lower().endswith(".jpg") or item.lower().endswith(".jpeg")):
        logo_file = item
        break
if not logo_file:
    for item in os.listdir("."):
        if item.lower() == "outland":
            logo_file = item
            break

# Encabezado corporativo
col_logo, col_title = st.columns([1.5, 4])
with col_logo:
    if logo_file:
        st.image(logo_file, width=230)
    else:
        st.markdown("## 🌐 **OUTLAND**\n##### *LOGISTICS*")

with col_title:
    st.title("Cotizador de Cargas Aéreas y Marítimas (LCL)")
    st.caption("Herramienta Oficial de Cotización - Outland Logistics")

st.markdown("---")

# Menú lateral
st.sidebar.header("⚙️ Configuración del Envío")
tipo_transporte = st.sidebar.radio("Tipo de Transporte:", ["Marítimo LCL", "Aéreo"])

modo_ingreso = st.sidebar.radio(
    "Modo de ingreso de carga:", 
    [
        "Por totales directos (m³ y kg)", 
        "Bulto único / uniformes", 
        "Múltiples bultos (Packing List)"
    ]
)

# Factores de conversión de dimensiones a Metros
factores_medida = {
    "Centímetros (cm)": 0.01,
    "Milímetros (mm)": 0.001,
    "Metros (m)": 1.0,
    "Pulgadas (in)": 0.0254
}

# Inicialización de variables generales
m3_total = 0.0
peso_bruto_kg = 0.0

st.subheader("📏 Datos de la Carga")

# --- MODO 1: TOTALES DIRECTOS ---
if modo_ingreso == "Por totales directos (m³ y kg)":
    col1, col2, col3 = st.columns(3)
    with col1:
        m3_directos = st.number_input("Volumen Total (m³)", min_value=0.0, value=1.2, step=0.1)
    with col2:
        peso_directo_kg = st.number_input("Peso Bruto Total (kg)", min_value=0.0, value=1000.0, step=10.0)
    with col3:
        tarifa_label = "Tarifa Flete (USD por m³ / W/M)" if tipo_transporte == "Marítimo LCL" else "Tarifa Flete (USD por kg cargable)"
        val_default = 85.0 if tipo_transporte == "Marítimo LCL" else 4.5
        tarifa = st.number_input(tarifa_label, min_value=0.0, value=val_default, step=0.5)

# --- MODO 2: BULTO ÚNICO / UNIFORMES ---
elif modo_ingreso == "Bulto único / uniformes":
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        unidad_medida = st.selectbox("Unidad de dimensión:", list(factores_medida.keys()), index=0)
    with col_u2:
        unidad_peso = st.selectbox("Unidad de peso:", ["Kilogramos (kg)", "Libras (lb)"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        largo = st.number_input("Largo", min_value=0.0, value=100.0, step=1.0)
    with col2:
        ancho = st.number_input("Ancho", min_value=0.0, value=100.0, step=1.0)
    with col3:
        alto = st.number_input("Alto", min_value=0.0, value=100.0, step=1.0)
    with col4:
        bultos = st.number_input("Cantidad de bultos", min_value=1, value=1, step=1)

    col5, col6 = st.columns(2)
    with col5:
        peso_input = st.number_input(f"Peso Bruto Total ({unidad_peso.split()[-1]})", min_value=0.0, value=150.0, step=5.0)
    with col6:
        tarifa_label = "Tarifa Flete (USD por m³ / W/M)" if tipo_transporte == "Marítimo LCL" else "Tarifa Flete (USD por kg cargable)"
        val_default = 85.0 if tipo_transporte == "Marítimo LCL" else 4.5
        tarifa = st.number_input(tarifa_label, min_value=0.0, value=val_default, step=0.5)

# --- MODO 3: MÚLTIPLES BULTOS (PACKING LIST) ---
else:
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        unidad_medida = st.selectbox("Unidad de dimensión para la tabla:", list(factores_medida.keys()), index=0)
    with col_p2:
        tarifa_label = "Tarifa Flete (USD por m³ / W/M)" if tipo_transporte == "Marítimo LCL" else "Tarifa Flete (USD por kg cargable)"
        val_default = 85.0 if tipo_transporte == "Marítimo LCL" else 4.5
        tarifa = st.number_input(tarifa_label, min_value=0.0, value=val_default, step=0.5)

    st.caption("✍️ Edita las celdas directamente o presiona el botón '+' abajo para agregar más tipos de bultos:")
    
    # Tabla editable de bultos
    df_inicial = pd.DataFrame([
        {"Cant. Bultos": 1, "Largo": 120.0, "Ancho": 80.0, "Alto": 100.0, "Peso Unitario (kg)": 150.0},
        {"Cant. Bultos": 2, "Largo": 50.0, "Ancho": 40.0, "Alto": 30.0, "Peso Unitario (kg)": 15.0}
    ])
    
    df_edited = st.data_editor(
        df_inicial, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "Cant. Bultos": st.column_config.NumberColumn(min_value=1, step=1, default=1),
            "Largo": st.column_config.NumberColumn(min_value=0.0, step=1.0),
            "Ancho": st.column_config.NumberColumn(min_value=0.0, step=1.0),
            "Alto": st.column_config.NumberColumn(min_value=0.0, step=1.0),
            "Peso Unitario (kg)": st.column_config.NumberColumn(min_value=0.0, step=1.0),
        }
    )

# --- CÁLCULO GENERAL ---
if st.button("🧮 Calcular Cotización Outland"):
    
    if modo_ingreso == "Por totales directos (m³ y kg)":
        m3_total = m3_directos
        peso_bruto_kg = peso_directo_kg

    elif modo_ingreso == "Bulto único / uniformes":
        f_medida = factores_medida[unidad_medida]
        l_m, a_m, h_m = largo * f_medida, ancho * f_medida, alto * f_medida
        m3_total = (l_m * a_m * h_m) * bultos
        peso_bruto_kg = peso_input if "Kilogramos" in unidad_peso else peso_input * 0.453592

    else: # Múltiples bultos
        f_medida = factores_medida[unidad_medida]
        m3_total = 0.0
        peso_bruto_kg = 0.0
        
        for idx, row in df_edited.iterrows():
            cant = row["Cant. Bultos"]
            l_m = row["Largo"] * f_medida
            a_m = row["Ancho"] * f_medida
            h_m = row["Alto"] * f_medida
            peso_u = row["Peso Unitario (kg)"]
            
            vol_unit = l_m * a_m * h_m
            m3_total += (vol_unit * cant)
            peso_bruto_kg += (peso_u * cant)

    # Resultados según transporte
    if tipo_transporte == "Marítimo LCL":
        peso_ton = peso_bruto_kg / 1000.0
        unidades_facturables = max(m3_total, peso_ton)
        costo_total = unidades_facturables * tarifa
        
        st.success("### 📊 Resumen de Cotización - Marítimo LCL")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Volumen Total", f"{m3_total:.3f} m³")
        m2.metric("Peso Bruto Total", f"{peso_bruto_kg:.1f} kg")
        m3.metric("Unidades W/M", f"{unidades_facturables:.3f}")
        m4.metric("💰 Costo Flete", f"${costo_total:,.2f} USD")
    else:
        peso_volumetrico_kg = m3_total * 166.667
        peso_tasable_kg = max(peso_bruto_kg, peso_volumetrico_kg)
        costo_total = peso_tasable_kg * tarifa
        
        st.success("### 📊 Resumen de Cotización - Carga Aérea")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Volumen Total", f"{m3_total:.3f} m³")
        m2.metric("Peso Volumétrico", f"{peso_volumetrico_kg:.2f} kg")
        m3.metric("Peso Cargable", f"{peso_tasable_kg:.2f} kg")
        m4.metric("💰 Costo Flete", f"${costo_total:,.2f} USD")
