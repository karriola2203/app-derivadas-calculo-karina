import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Cátedra Arriola: Tutor de Derivadas", layout="wide")

# --- BARRA LATERAL (LEYENDA Y GUÍA) ---
with st.sidebar:
    st.header("⌨️ Guía de Escritura")
    st.markdown("""
    **Símbolos obligatorios:**
    * **`*` :** Multiplicación (ej: `5*x`)
    * **`^` :** Potencia (ej: `x^2`)
    * **`/` :** División (ej: `x/3`)
    
    **Ejemplos para esta sesión:**
    * `5*x + sin(x/3)`
    * `x^2 - cos(2*x)`
    * `exp(4*x) + x/2`
    """)
    st.info("Sugerencia: El tutor ahora analiza cada parte de la suma por separado.")

st.title("🏛️ Tutor de Derivación Detallada")
st.subheader("Facultad de Arquitectura | Profe Karina Arriola")

# --- BLOQUE 1: EDITOR Y VISTA PREVIA ---
st.write("### ✍️ Editor de Funciones")
col_input, col_preview = st.columns([1, 1])

with col_input:
    u_input = st.text_input("Digita tu función:", value="5*x + sin(x/3)")

x = sp.symbols('x')

try:
    # Procesamiento flexible de entrada
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

# --- BLOQUE 2: DESGLOSE TÉRMINO A TÉRMINO ---
if h:
    st.write("### 🔍 Desarrollo Paso a Paso")
    
    # Obtenemos los términos (si es suma o resta)
    terminos = sp.Add.make_args(h)
    
    if len(terminos) > 1:
        st.markdown("#### **1. Identificación de la Estructura: Suma / Resta**")
        st.write("La función es una combinación de varios términos. Derivaremos cada uno por separado:")
        st.latex(f"h'(x) = " + " + ".join([f"\\frac{{d}}{{dx}}({sp.latex(t)})" for t in terminos]))
        st.write("---")

    # Analizamos cada término individualmente
    resultados_parciales = []
    
    for i, t in enumerate(terminos):
        st.write(f"**Analizando el término {i+1}:**")
        st.latex(f"f_{i+1}(x) = {sp.latex(t)}")
        
        # CASO: FORMAS GENERALES (sin, cos, exp)
        # Buscamos si el término contiene alguna de estas funciones
        func_base = None
        for name in ["sin", "cos", "exp"]:
            if t.has(getattr(sp, name)) or (name == "exp" and t.has(sp.exp)):
                func_base = name
                break
        
        if func_base:
            # Extraer el argumento ax para identificar 'a'
            # Buscamos el objeto de la función dentro del término
            f_interna = [a for a in t.atoms(sp.Function) if a.func.__name__.lower() == func_base]
            if not f_interna and func_base == "exp": # Caso especial e^x
                f_interna = [a for a in t.atoms(sp.exp)]
            
            if f_interna:
                instancia = f_interna[0]
                arg = instancia.args[0]
                a_coef = sp.diff(arg, x)
                
                # Si el término es algo como 3*sin(2x), rescatar el coeficiente externo
                coef_externo = t.as_coefficient(instancia)
                
                if func_base == "sin":
                    st.info("Técnica: Forma Generalizada $\\sin(ax)$")
                    st.latex(r"[\sin(ax)]' = a \cdot \cos(ax)")
                    st.write(f"Identificamos $a = {sp.latex(a_coef)}$.")
                elif func_base == "cos":
                    st.info("Técnica: Forma Generalizada $\\cos(ax)$")
                    st.latex(r"[\cos(ax)]' = -a \cdot \sin(ax)")
                    st.write(f"Identificamos $a = {sp.latex(a_coef)}$.")
                elif func_base == "exp":
                    st.info("Técnica: Forma Generalizada $e^{ax}$")
                    st.latex(r"[e^{ax}]' = a \cdot e^{ax}")
                    st.write(f"Identificamos $a = {sp.latex(a_coef)}$.")
            
            der_t = sp.diff(t, x)
            st.latex(f"\\text{{Derivada del término: }} {sp.latex(der_t)}")
            resultados_parciales.append(der_t)

        # CASO: PRODUCTO (Sin funciones trig/exp complejas)
        elif t.is_Mul and not func_base:
            args_mul = [a for a in t.args if a.has(x)]
            if len(args_mul) > 1:
                st.info("Técnica: Regla del Producto")
                f_p, g_p = args_mul[0], sp.Mul(*args_mul[1:])
                st.latex(f"f={sp.latex(f_p)}, g={sp.latex(g_p)} \\implies f'={sp.latex(sp.diff(f_p,x))}, g'={sp.latex(sp.diff(g_p,x))}")
            der_t = sp.diff(t, x)
            st.latex(f"\\text{{Derivada del término: }} {sp.latex(der_t)}")
            resultados_parciales.append(der_t)

        # CASO: POTENCIA / LINEAL
        else:
            st.info("Técnica: Regla de la Potencia / Constante")
            der_t = sp.diff(t, x)
            st.latex(f"\\text{{Derivada del término: }} {sp.latex(der_t)}")
            resultados_parciales.append(der_t)
        
        st.write("---")

    # --- RESULTADO FINAL ---
    st.success("### ✅ Resultado Final Ensamblado")
    final_sum = sum(resultados_parciales)
    st.latex(f"f'(x) = {sp.latex(final_sum)}")
    
    st.write("**Simplificación final:**")
    st.latex(f"f'(x) = {sp.latex(sp.simplify(final_sum))}")
