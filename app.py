import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Cátedra Arriola: Cálculo de Derivadas", layout="wide")

st.title("🏛️ Tutor de Derivación Detallada")
st.subheader("Facultad de Arquitectura | Profe Karina Arriola")

# --- BLOQUE 1: EDITOR Y VISTA PREVIA ---
st.write("### ✍️ Editor de Funciones")
with st.container():
    # El estudiante digita aquí
    u_input = st.text_input("Ingresa la función (ej. x**2 * sin(x)):", value="x**2 * sin(x)")
    
    x = sp.symbols('x')
    
    try:
        # Procesamos la entrada
        expr_clean = u_input.replace("^", "**")
        h = sp.sympify(expr_clean)
        
        # ESTA ES LA VISTA PREVIA QUE BUSCAMOS:
        st.info("#### 👁️ Confirmación de entrada:")
        st.write("El sistema interpretó tu función como:")
        st.latex(f"f(x) = {sp.latex(h)}")
        
    except Exception as e:
        st.error("⚠️ Error de escritura. Revisa los asteriscos (*) y paréntesis.")
        st.stop() # Detiene la ejecución si hay error en la entrada

st.markdown("---")

# --- BLOQUE 2: PROCESAMIENTO Y REGLAS ---
if h:
    st.write("### 🔍 Desglose del Procedimiento")
    
    # 1. IDENTIFICACIÓN DE REGLA DEL PRODUCTO
    if h.is_Mul and any(arg.has(x) for arg in h.args):
        args = [arg for arg in h.args if arg.has(x)]
        if len(args) > 1:
            f = args[0]
            g = sp.Mul(*args[1:])
            df = sp.diff(f, x)
            dg = sp.diff(g, x)
            
            st.markdown("#### **Regla Aplicada: Producto**")
            st.latex(r"\frac{d}{dx}[f(x) \cdot g(x)] = f'(x)g(x) + f(x)g'(x)")
            
            
            
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Funciones:**")
                st.latex(f"f(x) = {sp.latex(f)}")
                st.latex(f"g(x) = {sp.latex(g)}")
            with c2:
                st.write("**Derivadas:**")
                st.latex(f"f'(x) = {sp.latex(df)}")
                st.latex(f"g'(x) = {sp.latex(dg)}")
            
            st.write("**Ensamblaje:**")
            st.latex(f"h'(x) = ({sp.latex(df)})({sp.latex(g)}) + ({sp.latex(f)})({sp.latex(dg)})")

    # 2. IDENTIFICACIÓN DE REGLA DEL COCIENTE
    elif sp.fraction(h)[1] != 1:
        num, den = sp.fraction(h)
        f, g = num, den
        df, dg = sp.diff(f, x), sp.diff(g, x)

        st.markdown("#### **Regla Aplicada: Cociente**")
        st.latex(r"\frac{d}{dx}\left[\frac{f(x)}{g(x)}\right] = \frac{f'(x)g(x) - f(x)g'(x)}{[g(x)]^2}")
        
        

        c1, c2 = st.columns(2)
        with c1:
            st.write("**Funciones:**")
            st.latex(f"f(x) = {sp.latex(f)}")
            st.latex(f"g(x) = {sp.latex(g)}")
        with c2:
            st.write("**Derivadas:**")
            st.latex(f"f'(x) = {sp.latex(df)}")
            st.latex(f"g'(x) = {sp.latex(dg)}")

        st.write("**Ensamblaje:**")
        st.latex(f"h'(x) = \\frac{({sp.latex(df)})({sp.latex(g)}) - ({sp.latex(f)})({sp.latex(dg)})}{({sp.latex(g)})^2}")

    # 3. REGLAS GENERALES (SENO, COSENO, EXP)
    elif any(func in str(h) for func in ["sin", "cos", "exp"]):
        g = h.args[0]
        dg = sp.diff(g, x)
        
        st.markdown("#### **Regla Aplicada: Función Compuesta (Cadena)**")
        st.write(f"Derivada externa de la función base con respecto a su argumento:")
        st.latex(f"h'(x) = {sp.latex(sp.diff(h, x))}")

    # 4. POTENCIA O SUMA
    else:
        st.markdown("#### **Regla Aplicada: Potencia / Suma**")
        st.latex(f"h'(x) = {sp.latex(sp.diff(h, x))}")

    # --- RESULTADO FINAL ---
    st.markdown("---")
    st.success("### ✅ Resultado Final Simplificado")
    st.latex(f"h'(x) = {sp.latex(sp.simplify(sp.diff(h, x)))}")
