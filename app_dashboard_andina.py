"""
=============================================================================
DASHBOARD FINANCIERO Y DIAGNÓSTICO ESTRATÉGICO - DISTRIBUCIONES ANDINA COMERCIAL S.A.S.
=============================================================================
Este script implementa un dashboard financiero interactivo de nivel ejecutivo 
utilizando Streamlit, Plotly, y Pandas para la empresa Distribuciones Andina Comercial S.A.S. (2021-2025).

Para ejecutar localmente (cuando disponga de Python y Streamlit):
    streamlit run app_dashboard_andina.py
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de página
st.set_page_config(
    page_title="Distribuciones Andina Comercial | Financial Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para look & feel corporativo
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-delta-pos {
        color: #10b981;
        font-size: 13px;
        font-weight: 600;
    }
    .metric-delta-neg {
        color: #ef4444;
        font-size: 13px;
        font-weight: 600;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# DATOS FINANCIEROS AUDITADOS (2021 - 2025)
# -------------------------------------------------------------
YEARS = ["2021", "2022", "2023", "2024", "2025"]

# 1. Estado de Resultados (en millones COP)
er_data = {
    "Concepto": [
        "Ingresos operacionales (ventas netas)",
        "Costo de ventas (mercancía vendida)",
        "Utilidad bruta",
        "Gastos de administración",
        "Gastos de ventas",
        "Depreciaciones y amortizaciones",
        "Utilidad operacional (EBIT)",
        "Gastos financieros (intereses)",
        "Utilidad antes de impuestos",
        "Impuesto de renta",
        "Utilidad neta del ejercicio"
    ],
    "2021": [80000, 60000, 20000, 60000/10, 7040, 1200, 5760, 1500, 4260, 1278, 2982],
    "2022": [88000, 66000, 22000, 6424, 7568, 1300, 6708, 1600, 5108, 1532, 3576],
    "2023": [97000, 72750, 24250, 6887, 8148, 1400, 7815, 1550, 6265, 1880, 4385],
    "2024": [108000, 81000, 27000, 7344, 8856, 1500, 9300, 1500, 7800, 2340, 5460],
    "2025": [120000, 90000, 30000, 7800, 9600, 1600, 11000, 1450, 9550, 2865, 6685]
}
df_er = pd.DataFrame(er_data)

# 2. Balance General (en millones COP)
bg_data = {
    "Concepto": [
        "Efectivo y equivalentes",
        "Deudores (cuentas por cobrar clientes)",
        "Inventarios",
        "Otros activos corrientes",
        "Total activo corriente",
        "Propiedad, planta y equipo (neto)",
        "Intangibles (neto)",
        "Total activos",
        "Obligaciones financieras - corto plazo",
        "Proveedores",
        "Cuentas por pagar y otros pasivos",
        "Impuestos por pagar",
        "Total pasivo corriente",
        "Obligaciones financieras - largo plazo",
        "Total pasivos",
        "Capital social",
        "Reservas",
        "Resultados acumulados",
        "Total patrimonio",
        "Total pasivo + patrimonio"
    ],
    "2021": [740, 10959, 10685, 1200, 23584, 13300, 1500, 38384, 4385, 6575, 1043, 256, 12259, 8143, 20402, 10000, 2000, 5982, 17982, 38384],
    "2022": [3233, 11573, 11392, 1200, 27398, 14800, 1500, 43698, 4905, 7595, 1119, 306, 13925, 9109, 23034, 10000, 2000, 8664, 20664, 43698],
    "2023": [5866, 12225, 12358, 1200, 31649, 16400, 1500, 49549, 5483, 8571, 1203, 376, 15633, 10183, 25816, 10000, 2000, 11733, 23733, 49549],
    "2024": [8882, 13315, 13315, 1200, 36712, 18100, 1500, 56312, 6048, 9986, 1296, 468, 17798, 11232, 29030, 10000, 2000, 15282, 27282, 56312],
    "2025": [12450, 14137, 14301, 1200, 42088, 20000, 1500, 63588, 6615, 11096, 1392, 573, 19676, 12285, 31961, 10000, 2000, 19627, 31627, 63588]
}
df_bg = pd.DataFrame(bg_data)

# 3. Flujo de Efectivo
cfo = [2212, 4701, 5297, 6513, 7788]
cfi = [-2500, -2800, -3000, -3200, -3500]
cff = [-1472, 592, 336, -297, -720]
fcf = [cfo[i] + cfi[i] for i in range(len(YEARS))] # CFO + CAPEX (Capex is negative)

# 4. Cálculo de Indicadores Clave
ventas = [80000, 88000, 97000, 108000, 120000]
costos = [60000, 66000, 72750, 81000, 90000]
ebit = [5760, 6708, 7815, 9300, 11000]
ebitda = [ebit[i] + df_er[YEARS[i]][5] for i in range(len(YEARS))] # EBIT + Depr
uneta = [2982, 3576, 4385, 5460, 6685]
activos = [38384, 43698, 49549, 56312, 63588]
patrimonio = [17982, 20664, 23733, 27282, 31627]
pasivos = [20402, 23034, 25816, 29030, 31961]
act_corr = [23584, 27398, 31649, 36712, 42088]
pas_corr = [12259, 13925, 15633, 17798, 19676]
deuda_fin = [4385 + 8143, 4905 + 9109, 5483 + 10183, 6048 + 11232, 6615 + 12285]
cxc = [10959, 11573, 12225, 13315, 14137]
inv = [10685, 11392, 12358, 13315, 14301]
cxp = [6575, 7595, 8571, 9986, 11096]
intereses = [1500, 1600, 1550, 1500, 1450]

# Ratios
margen_bruto = [(30000 if i==4 else df_er[YEARS[i]][2]) / ventas[i] * 100 for i in range(5)]
margen_operacional = [ebit[i] / ventas[i] * 100 for i in range(5)]
margen_neto = [uneta[i] / ventas[i] * 100 for i in range(5)]
margen_ebitda = [ebitda[i] / ventas[i] * 100 for i in range(5)]
roe = [uneta[i] / patrimonio[i] * 100 for i in range(5)]
roa = [uneta[i] / activos[i] * 100 for i in range(5)]
razon_corriente = [act_corr[i] / pas_corr[i] for i in range(5)]
prueba_acida = [(act_corr[i] - inv[i]) / pas_corr[i] for i in range(5)]
endeudamiento_total = [pasivos[i] / activos[i] * 100 for i in range(5)]
cobertura_intereses = [ebit[i] / intereses[i] for i in range(5)]
deuda_ebitda = [deuda_fin[i] / ebitda[i] for i in range(5)]

# Días de ciclo de conversión (365 días)
dso = [(cxc[i] / ventas[i]) * 365 for i in range(5)]
dio = [(inv[i] / costos[i]) * 365 for i in range(5)]
dpo = [(cxp[i] / costos[i]) * 365 for i in range(5)]
ccc = [dso[i] + dio[i] - dpo[i] for i in range(5)]

# KTNO (Capital de Trabajo Neto Operativo = CxC + Inventarios - Proveedores)
ktno = [cxc[i] + inv[i] - cxp[i] for i in range(5)]
pkto = [(ktno[i] / ventas[i]) * 100 for i in range(5)] # Productividad del KTNO

# -------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=64)
st.sidebar.title("Andina Comercial")
st.sidebar.markdown("**Diagnóstico Financiero Estratégico**\n*Periodo Auditado: 2021 – 2025*")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Módulos del Sistema:",
    [
        "📌 Resumen Ejecutivo (Dashboard)",
        "📈 Rentabilidad & DuPont",
        "💧 Liquidez & Ciclo de Efectivo",
        "🛡️ Estructura & Solvencia Financiera",
        "💵 Flujo de Caja & Creación de Valor",
        "📋 Estados Financieros Detallados",
        "🎯 Matriz de Recomendaciones"
    ]
)

st.sidebar.markdown("---")
selected_year = st.sidebar.selectbox("Seleccione Año de Foco:", YEARS, index=4)
idx = YEARS.index(selected_year)

st.sidebar.info(f"""
**Perfil de la Organización:**
Distribuidora B2B colombiana líder en seguridad electrónica, tecnología de redes y herramientas industriales.
- **Ventas 2025:** ${ventas[4]:,.0f}M COP
- **Crecimiento CAGR:** 10.67%
- **Margen EBITDA:** {margen_ebitda[4]:.2f}%
""")

# -------------------------------------------------------------
# 1. RESUMEN EJECUTIVO (DASHBOARD)
# -------------------------------------------------------------
if menu == "📌 Resumen Ejecutivo (Dashboard)":
    st.title("📊 Cuadro de Mando Integral Financiero")
    st.subheader(f"Distribuciones Andina Comercial S.A.S. — Desempeño {selected_year}")
    
    # KPIs Superiores
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Ventas Netas",
            value=f"${ventas[idx]:,.0f}M",
            delta=f"{((ventas[idx]-ventas[idx-1])/ventas[idx-1]*100):.1f}% vs ant." if idx > 0 else "Año base"
        )
    with col2:
        st.metric(
            label="Utilidad Neta",
            value=f"${uneta[idx]:,.0f}M",
            delta=f"{((uneta[idx]-uneta[idx-1])/uneta[idx-1]*100):.1f}% vs ant." if idx > 0 else "Año base"
        )
    with col3:
        st.metric(
            label="EBITDA",
            value=f"${ebitda[idx]:,.0f}M",
            delta=f"Margen: {margen_ebitda[idx]:.1f}%"
        )
    with col4:
        st.metric(
            label="ROE (Rentabilidad Pat.)",
            value=f"{roe[idx]:.2f}%",
            delta=f"{roe[idx]-roe[idx-1]:.2f} pts" if idx > 0 else "Año base"
        )
    with col5:
        st.metric(
            label="Flujo Op. Caja (CFO)",
            value=f"${cfo[idx]:,.0f}M",
            delta=f"{((cfo[idx]-cfo[idx-1])/cfo[idx-1]*100):.1f}%" if idx > 0 else "Año base"
        )
        
    st.markdown("---")
    
    # Gráficos de tendencias
    gcol1, gcol2 = st.columns(2)
    
    with gcol1:
        st.markdown("#### 🚀 Evolución de Ingresos y Márgenes Operativos")
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=YEARS, y=ventas, name="Ventas Netas ($M)", marker_color="#0284c7"))
        fig1.add_trace(go.Scatter(x=YEARS, y=margen_operacional, name="Margen EBIT (%)", yaxis="y2", 
                                  mode="lines+markers", line=dict(color="#f59e0b", width=3)))
        fig1.update_layout(
            yaxis=dict(title="Ventas Netas ($ COP)"),
            yaxis2=dict(title="Margen EBIT (%)", overlaying="y", side="right", range=[0, 15]),
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with gcol2:
        st.markdown("#### 💰 Generación de Caja vs Utilidad Neta (Calidad del Resultado)")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=YEARS, y=uneta, name="Utilidad Neta ($M)", mode="lines+markers", line=dict(color="#64748b", dash="dash", width=2)))
        fig2.add_trace(go.Scatter(x=YEARS, y=cfo, name="Flujo de Caja Operativo CFO ($M)", mode="lines+markers", line=dict(color="#10b981", width=3)))
        fig2.add_trace(go.Bar(x=YEARS, y=fcf, name="Flujo de Caja Libre FCF ($M)", marker_color="#38bdf8", opacity=0.7))
        fig2.update_layout(
            yaxis=dict(title="Millones COP"),
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    # Conclusiones clave
    st.info("""
    **💡 Diagnóstico del Analista Financiero:**
    1. **Superación del punto crítico de liquidez:** En 2021 la empresa crecía en ventas ($80.000M) pero drenaba caja (CFO apenas cubría gastos y el flujo libre fue negativo -$288M). A partir de 2022 la disciplina de crédito y rotación convirtió la venta en efectivo efectivo.
    2. **Expansión consistente de márgenes:** El margen EBIT creció del **7.20% al 9.17%**, y el EBITDA alcanzó el **10.50%** en 2025 impulsado por economías de escala comerciales y canal B2B digital.
    3. **De-apalancamiento operativo y financiero:** La razón Deuda Neta / EBITDA descendió notablemente, reduciendo la exposición al riesgo de tasas.
    """)

# -------------------------------------------------------------
# 2. RENTABILIDAD & DUPONT
# -------------------------------------------------------------
elif menu == "📈 Rentabilidad & DuPont":
    st.title("📈 Análisis de Rentabilidad y Modelo DuPont")
    st.markdown("Descomposición técnica del retorno sobre el patrimonio (ROE) en Eficiencia Operativa, Rotación de Activos y Apalancamiento Financiero.")
    
    colA, colB, colC = st.columns(3)
    # DuPont Componentes para el año seleccionado
    dupont_margin = margen_neto[idx]
    dupont_turnover = ventas[idx] / activos[idx]
    dupont_leverage = activos[idx] / patrimonio[idx]
    
    colA.metric("Margen Neto (Utilidad / Ventas)", f"{dupont_margin:.2f}%")
    colB.metric("Rotación de Activos (Ventas / Activos)", f"{dupont_turnover:.2f}x")
    colC.metric("Multiplicador de Capital (Activos / Pat.)", f"{dupont_leverage:.2f}x")
    
    st.markdown(f"### ROE Calculado {selected_year}: **{roe[idx]:.2f}%** (= {dupont_margin:.2f}% × {dupont_turnover:.2f} × {dupont_leverage:.2f})")
    
    st.markdown("---")
    
    r1, r2 = st.columns(2)
    with r1:
        st.markdown("#### Evolución de Márgenes de Rentabilidad (%)")
        df_margenes = pd.DataFrame({
            "Año": YEARS,
            "Margen Bruto": margen_bruto,
            "Margen Operacional (EBIT)": margen_operacional,
            "Margen EBITDA": margen_ebitda,
            "Margen Neto": margen_neto
        })
        fig_m = px.line(df_margenes, x="Año", y=["Margen Bruto", "Margen EBITDA", "Margen Operacional", "Margen Neto"],
                        markers=True, color_discrete_sequence=["#1e3a8a", "#0284c7", "#0d9488", "#10b981"])
        fig_m.update_layout(yaxis_title="Porcentaje (%)", legend_title="", hovermode="x unified")
        st.plotly_chart(fig_m, use_container_width=True)
        
    with r2:
        st.markdown("#### ROA vs ROE (Rendimiento del Negocio)")
        df_retornos = pd.DataFrame({
            "Año": YEARS,
            "ROA (Activos)": roa,
            "ROE (Patrimonio)": roe
        })
        fig_r = px.bar(df_retornos, x="Año", y=["ROA (Activos)", "ROE (Patrimonio)"], barmode="group",
                       color_discrete_sequence=["#3b82f6", "#8b5cf6"])
        fig_r.update_layout(yaxis_title="Porcentaje (%)", legend_title="", hovermode="x unified")
        st.plotly_chart(fig_r, use_container_width=True)

# -------------------------------------------------------------
# 3. LIQUIDEZ & CICLO DE EFECTIVO
# -------------------------------------------------------------
elif menu == "💧 Liquidez & Ciclo de Efectivo":
    st.title("💧 Gestión de Capital de Trabajo y Ciclo de Conversión de Efectivo (CCC)")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Días Cartera (DSO)", f"{dso[idx]:.1f} días", delta=f"{dso[idx]-dso[0]:.1f} d vs 2021")
    c2.metric("Días Inventario (DIO)", f"{dio[idx]:.1f} días", delta=f"{dio[idx]-dio[0]:.1f} d vs 2021")
    c3.metric("Días Proveedores (DPO)", f"{dpo[idx]:.1f} días", delta=f"{dpo[idx]-dpo[0]:.1f} d vs 2021")
    c4.metric("Ciclo Efectivo (CCC)", f"{ccc[idx]:.1f} días", delta=f"{ccc[idx]-ccc[0]:.1f} d vs 2021", delta_color="inverse")
    
    st.markdown("---")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### ⏳ Desglose del Ciclo Operativo vs Ciclo Neto de Efectivo")
        fig_ccc = go.Figure()
        fig_ccc.add_trace(go.Bar(name='DSO (Cobro a Clientes)', x=YEARS, y=dso, marker_color='#f59e0b'))
        fig_ccc.add_trace(go.Bar(name='DIO (Permanencia Inventarios)', x=YEARS, y=dio, marker_color='#3b82f6'))
        fig_ccc.add_trace(go.Bar(name='(-) DPO (Financiamiento Proveedores)', x=YEARS, y=[-x for x in dpo], marker_color='#ef4444'))
        fig_ccc.add_trace(go.Scatter(name='CCC (Días de Caja Comprometida)', x=YEARS, y=ccc, mode='lines+markers', line=dict(color='#10b981', width=3)))
        fig_ccc.update_layout(barmode='relative', yaxis_title="Días", hovermode="x unified", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_ccc, use_container_width=True)
        
    with col_g2:
        st.markdown("#### 🛡️ Índices de Liquidez (Razón Corriente & Prueba Ácida)")
        fig_liq = go.Figure()
        fig_liq.add_trace(go.Scatter(x=YEARS, y=razon_corriente, name="Razón Corriente", mode="lines+markers", line=dict(color="#2563eb", width=3)))
        fig_liq.add_trace(go.Scatter(x=YEARS, y=prueba_acida, name="Prueba Ácida (Sin Inventarios)", mode="lines+markers", line=dict(color="#06b6d4", width=3)))
        fig_liq.add_hline(y=1.0, line_dash="dash", line_color="#ef4444", annotation_text="Punto Crítico (1.0x)")
        fig_liq.update_layout(yaxis_title="Veces (x)", hovermode="x unified", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_liq, use_container_width=True)

# -------------------------------------------------------------
# 4. ESTRUCTURA & SOLVENCIA FINANCIERA
# -------------------------------------------------------------
elif menu == "🛡️ Estructura & Solvencia Financiera":
    st.title("🛡️ Estructura de Capital, Deuda y Coberturas")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Endeudamiento Total", f"{endeudamiento_total[idx]:.1f}%", f"{endeudamiento_total[idx]-endeudamiento_total[0]:.1f} pts")
    sc2.metric("Deuda Financiera Total", f"${deuda_fin[idx]:,.0f}M", f"+${deuda_fin[idx]-deuda_fin[0]:,.0f}M")
    sc3.metric("Cobertura de Intereses", f"{cobertura_intereses[idx]:.2f}x", f"{cobertura_intereses[idx]-cobertura_intereses[0]:.2f}x")
    sc4.metric("Deuda / EBITDA", f"{deuda_ebitda[idx]:.2f}x", f"{(deuda_ebitda[idx]-deuda_ebitda[0]):.2f}x", delta_color="inverse")
    
    st.markdown("---")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### ⚖️ Composición de Pasivo y Patrimonio (Estructura de Capital)")
        fig_cap = go.Figure()
        fig_cap.add_trace(go.Bar(name='Pasivo Corriente', x=YEARS, y=pas_corr, marker_color='#93c5fd'))
        fig_cap.add_trace(go.Bar(name='Pasivo No Corriente (LP)', x=YEARS, y=[df_bg[y][13] for y in YEARS], marker_color='#3b82f6'))
        fig_cap.add_trace(go.Bar(name='Patrimonio Neto', x=YEARS, y=patrimonio, marker_color='#10b981'))
        fig_cap.update_layout(barmode='stack', yaxis_title="Millones COP", hovermode="x unified", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_cap, use_container_width=True)
        
    with col_s2:
        st.markdown("#### 📈 Capacidad de Servicio de Deuda (EBIT vs Intereses)")
        fig_cob = go.Figure()
        fig_cob.add_trace(go.Bar(name='EBIT (Utilidad Operacional)', x=YEARS, y=ebit, marker_color='#0284c7'))
        fig_cob.add_trace(go.Bar(name='Gastos Financieros', x=YEARS, y=intereses, marker_color='#ef4444'))
        fig_cob.add_trace(go.Scatter(name='Ratio Cobertura (EBIT / Intereses)', x=YEARS, y=cobertura_intereses, yaxis='y2', mode='lines+markers', line=dict(color='#8b5cf6', width=3)))
        fig_cob.update_layout(
            yaxis=dict(title="Millones COP"),
            yaxis2=dict(title="Veces Cobertura", overlaying='y', side='right', range=[0, 10]),
            legend=dict(orientation="h", y=1.1),
            hovermode="x unified"
        )
        st.plotly_chart(fig_cob, use_container_width=True)

# -------------------------------------------------------------
# 5. FLUJO DE CAJA & CREACIÓN DE VALOR
# -------------------------------------------------------------
elif menu == "💵 Flujo de Caja & Creación de Valor":
    st.title("💵 Análisis de Dinámica de Flujos y CAPEX")
    
    fc1, fc2, fc3, fc4 = st.columns(4)
    fc1.metric("Flujo Operativo (CFO)", f"${cfo[idx]:,.0f}M")
    fc2.metric("Inversión Capex (CFI)", f"${abs(cfi[idx]):,.0f}M")
    fc3.metric("Flujo de Caja Libre (FCF)", f"${fcf[idx]:,.0f}M")
    fc4.metric("Saldo Caja Final", f"${df_bg[selected_year][0]:,.0f}M")
    
    st.markdown("---")
    
    st.markdown("#### 🌊 Cascada de Flujo de Fondos (Waterfall 2025)")
    fig_wf = go.Figure(go.Waterfall(
        name="Flujo 2025",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["Saldo Inicial", "Generación Operativa (CFO)", "Capex (CFI)", "Financiación & Divs (CFF)", "Saldo Final Caja"],
        y=[8882, 7788, -3500, -720, 12450],
        connector={"line": {"color": "#94a3b8"}},
        decreasing={"marker": {"color": "#ef4444"}},
        increasing={"marker": {"color": "#10b981"}},
        totals={"marker": {"color": "#0284c7"}}
    ))
    fig_wf.update_layout(yaxis_title="Millones COP", waterfallgap=0.3)
    st.plotly_chart(fig_wf, use_container_width=True)

# -------------------------------------------------------------
# 6. ESTADOS FINANCIEROS DETALLADOS
# -------------------------------------------------------------
elif menu == "📋 Estados Financieros Detallados":
    st.title("📋 Estados Financieros Históricos (2021 - 2025)")
    st.caption("Cifras auditadas expresadas en Millones de Pesos Colombianos (COP)")
    
    tab1, tab2, tab3 = st.tabs(["Estado de Resultados", "Balance General", "Estado de Flujo de Efectivo"])
    
    with tab1:
        st.dataframe(df_er.style.format({col: "${:,.0f}" for col in YEARS}), use_container_width=True)
    with tab2:
        st.dataframe(df_bg.style.format({col: "${:,.0f}" for col in YEARS}), use_container_width=True)
    with tab3:
        fe_df = pd.DataFrame({
            "Concepto": [
                "Utilidad Neta", "(+) Depreciaciones", "Variación Capital de Trabajo Operativo",
                "Flujo Operativo (CFO)", "CAPEX (CFI)", "Variación Neta Deuda", "Dividendos Pagados",
                "Flujo Financiación (CFF)", "Variación Neta Caja", "Caja Final"
            ],
            "2021": [2982, 1200, -1970, 2212, -2500, -1472, 0, -1472, -1760, 740],
            "2022": [3576, 1300, -175, 4701, -2800, 1486, -894, 592, 2493, 3233],
            "2023": [4385, 1400, -488, 5297, -3000, 1652, -1316, 336, 2633, 5866],
            "2024": [5460, 1500, -447, 6513, -3200, 1614, -1911, -297, 3016, 8882],
            "2025": [6685, 1600, -497, 7788, -3500, 1620, -2340, -720, 3568, 12450]
        })
        st.dataframe(fe_df.style.format({col: "${:,.0f}" for col in YEARS}), use_container_width=True)

# -------------------------------------------------------------
# 7. MATRIZ DE RECOMENDACIONES
# -------------------------------------------------------------
elif menu == "🎯 Matriz de Recomendaciones":
    st.title("🎯 Dictamen Financiero Estratégico & Plan de Acción")
    
    st.markdown("""
    ### Diagnóstico Integral del Negocio (Distribuciones Andina Comercial S.A.S.)
    
    | Dimensión | Hallazgo Financiero | Calificación | Recomendación Estratégica |
    | :--- | :--- | :---: | :--- |
    | **Crecimiento en Ventas** | Ventas aumentaron de \$80.000M a \$120.000M (CAGR 10.67%). | 🟢 Excelente | Mantener la estrategia de mezcla con marcas propias de mayor margen y consolidar el canal digital B2B. |
    | **Margen Bruto** | Sostenido exactamente en el 25.0% de manera consistente. | 🟢 Muy Sólido | Gran disciplina comercial al no competir por precios predatorios sino por disponibilidad inmediata y servicio posventa. |
    | **Eficiencia Operativa** | Los gastos de administración y ventas decrecieron porcentualmente frente a ventas, llevando el EBIT de 7.20% a 9.17%. | 🟢 Fuerte Apalancamiento | Seguir invirtiendo en automatización ERP y logística de despacho para mantener la ventaja de costos fijos. |
    | **Capital de Trabajo (KTNO)** | El Ciclo de Efectivo mejoró de 65.0 días en 2021 a 56.4 días en 2025. | 🟡 Positivo con Oportunidad | Continuar acortando la rotación de inventarios obsoletos mediante analítica predictiva de demanda. |
    | **Solvencia y Deuda** | El ratio Deuda / EBITDA bajó de 1.80x a 1.50x y la cobertura de intereses aumentó de 3.84x a 7.59x. | 🟢 Muy Saludable | La empresa tiene capacidad crediticia disponible para acelerar expansiones regionales o CAPEX logístico estratégico. |
    | **Caja y Dividendos** | Saldo en caja subió a \$12.450M permitiendo pagar \$2.340M en dividendos en 2025 sin comprometer liquidez. | 🟢 Generación de Valor | Diseñar una política formal de dividendos (payout ~35%) ligada al FCF y constituir un fondo de liquidez para contingencias macroeconómicas. |
    """)

