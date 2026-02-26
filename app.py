import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Cátedra Arriola: Tutor de Derivadas", layout="wide")

# --- BARRA LATERAL (LEYENDA DE SÍMBOLOS) ---
with st.sidebar:
    st.header("⌨️ Guía de Escritura")
    st.markdown("""
    **Símbolos para el Estudiante:**
    * **`*` :** Multiplicación (ej: `5*x`)
    * **`^` :** Potencia (ej: `x^2`)
    * **`/` :** División o Fracción (ej: `(x+1)/x`)
    
    **Ejemplos recomendados:**
    * `x^2 * cos(3*x)` (Producto)
    * `(5*x + 1) / x` (División)
    * `5*x + sin(x/3)` (Suma + Forma General)
    """)
    st.info("Nota: El sistema detecta automáticamente la técnica necesaria para cada término.")

st.title("🏛️ Tutor de Derivación Detallada")
st.subheader("Facultad de Arquitectura | Profe Karina Arriola")

# --- BLOQUE 1: EDITOR Y VISTA PREVIA ---
st.write("### ✍️ Editor de Funciones")
col_input, col_preview = st.columns([1, 1])

with col_input:
    u_input = st.text_input("Digita tu función aquí:", value="5*x + sin(x/3)")

x = sp.symbols('x')

try:
    # Procesamos la entrada para que acepte ^ y e^
    input_proc = u_input.replace("^", "**").replace("e**", "exp")
    h = sp.sympify(input_proc)
    
    with col_preview:
        st.markdown("#### 👁️ Interpretación Matemática:")
        st.latex(f"f(x) = {sp.latex(h)}")

except Exception as e:
    with col_preview:
        st.error("⚠️ Error de escritura. Revisa los asteriscos (*) o paréntesis.")
    st.stop()

st.markdown("---")

# --- BLOQUE 2: DESARROLLO PASO A PASO ---
if h:
    st.write("### 🔍 Desarrollo del Cálculo")
    
    # Separamos la función en sus términos (Suma/Resta)
    terminos = sp.Add.make_args(h)
    
    if len(terminos) > 1:
        st.markdown("#### **Estructura Identificada: Suma / Resta**")
        st.write("Aplicamos la propiedad de linealidad (derivamos cada término por separado):")
        st.latex(f"f'(x) = " + " + ".join([f"\\frac{{d}}{{dx}}({sp.latex(t)})" for t in terminos]))
        st.write("---")

    resultados_parciales = []
    
    for i, t in enumerate(terminos):
        st.write(f"#### **Término {i+1}:**")
        st.latex(f"f_{i+1}(x) = {sp.latex(t)}")
        
        # 1. ¿ES UN COCIENTE?
        num, den = sp.fraction(t)
        if den != 1 and den.has(x):
            st.info("📐 Técnica: Regla del Cociente")
            st.latex(r"\left[\frac{f}{g}\right]' = \frac{f'g - fg'}{g^2}")
            
            
            f_p, g_p = num, den
            df_p, dg_p = sp.diff(f_p, x), sp.diff(g_p, x)
            
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Componentes:**")
                st.latex(f"f(x) = {sp.latex(f_p)}")
                st.latex(f"g(x) = {sp.latex(g_p)}")
            with c2:
                st.write("**Derivadas:**")
                st.latex(f"f'(x) = {sp.latex(df_p)}")
                st.latex(f"g'(x) = {sp.latex(dg_p)}")
            
            der_t = sp.diff(t, x)
            st.write("**Ensamblaje del cociente:**")
            st.latex(f"\\frac{{({sp.latex(df_p)})({sp.latex(g_p)}) - ({sp.latex(f_p)})({sp.latex(dg_p)})}}{{({sp.latex(g_p)})^2}}")

        # 2. ¿ES UN PRODUCTO?
        elif t.is_Mul and len([arg for arg in t.args if arg.has(x)]) > 1:
            factores_x = [arg for arg in t.args if arg.has(x)]
            constante = t.as_coefficient(sp.Mul(*factores_x))
            
            st.info("📐 Técnica: Regla del Producto")
            st.latex(r"[f \cdot g]' = f'g + fg'")
            
            
            f_p = factores_x[0]
            g_p = sp.Mul(*factores_x[1:])
            df_p, dg_p = sp.diff(f_p, x), sp.diff(g_p, x)
            
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Componentes:**")
                st.latex(f"f(x) = {sp.latex(f_p)}")
                st.latex(f"g(x) = {sp.latex(g_p)}")
            with c2:
                st.write("**Derivadas:**")
                st.latex(f"f'(x) = {sp.latex(df_p)}")
                st.latex(f"g'(x) = {sp.latex(dg_p)}")
            
            st.write("**Ensamblaje del producto:**")
            if constante != 1:
                st.latex(f"{sp.latex(constante)} \\cdot [({sp.latex(df_p)})({sp.latex(g_p)}) + ({sp.latex(f_p)})({sp.latex(dg_p)})]")
            else:
                st.latex(f"({sp.latex(df_p)})({sp.latex(g_p)}) + ({sp.latex(f_p)})({sp.latex(dg_p)})")

        # 3. ¿ES UNA FORMA GENERALIZADA (sin, cos, exp)?
        elif any(t.has(getattr(sp, name)) for name in ["sin", "cos", "exp"]):
            func_obj = None
            for name in ["sin", "cos", "exp"]:
                if t.has(getattr(sp, name)): func_obj = name; break
            
            f_interna = list(t.atoms(sp.Function))[0] if t.atoms(sp.Function) else list(t.atoms(sp.exp))[0]
            arg_ax = f_interna.args[0]
            a_val = sp.diff(arg_ax, x)
            
            if func_obj == "sin":
                st.info("📐 Técnica: Forma General $\sin(ax)$")
                st.latex(r"[\sin(ax)]' = a \cdot \cos(ax)")
                
            elif func_obj == "cos":
                st.info("📐 Técnica: Forma General $\cos(ax)$")
                st.latex(r"[\cos(ax)]' = -a \cdot \sin(ax)")
            elif func_obj == "exp":
                st.info("📐 Técnica: Forma General $e^{ax}$")
                st.latex(r"[e^{ax}]' = a \cdot e^{ax}")
                
                
            st.write(f"Identificamos que el coeficiente $a = {sp.latex(a_val)}$")
            st.latex(f"\\text{{Derivada: }} {sp.latex(sp.diff(t, x))}")

        # 4. CASO BASE (Potencia o constante)
        else:
            st.info("📐 Técnica: Regla de la Potencia / Directa")
            st.latex(f"\\text{{Derivada: }} {sp.latex(sp.diff(t, x))}")
        
        resultados_parciales.append(sp.diff(t, x))
        st.write("---")

    # --- RESULTADO FINAL ---
    st.success("### ✅ Resultado Final Ensamblado")
    final_res = sum(resultados_parciales)
    st.latex(f"f'(x) = {sp.latex(final_res)}")
    
    st.write("**Resultado Simplificado:**")
    st.latex(f"f'(x) = {sp.latex(sp.simplify(final_res))}")
