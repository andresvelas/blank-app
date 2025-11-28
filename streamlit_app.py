import streamlit as st
import random

st.title("🎲 Juego Monty Hall Extendido (10 Puertas)")
st.write("""
Bienvenida al experimento.  
Hay **10 puertas**: **1 premio** y **9 cabras**.  
Tu objetivo es decidir si **cambiar** o **mantener** tu elección después de que se revelen puertas vacías.
""")

# --- Inicialización del estado ---
if "puertas" not in st.session_state:
    st.session_state.puertas = None
if "eleccion" not in st.session_state:
    st.session_state.eleccion = None
if "puertas_abiertas" not in st.session_state:
    st.session_state.puertas_abiertas = None
if "otra_puerta" not in st.session_state:
    st.session_state.otra_puerta = None
if "fase" not in st.session_state:
    st.session_state.fase = "inicio"

# --- FASE 1: Elegir puerta ---
if st.session_state.fase == "inicio":
    puerta = st.number_input("Elige una puerta (1 a 10):", 1, 10, step=1)

    if st.button("Confirmar elección"):
        st.session_state.puertas = [0]*9 + [1]
        random.shuffle(st.session_state.puertas)

        st.session_state.eleccion = puerta - 1

        # Monty abre 8 puertas con cabra
        indices_posibles = [
            i for i in range(10)
            if i != st.session_state.eleccion and st.session_state.puertas[i] == 0
        ]
        st.session_state.puertas_abiertas = random.sample(indices_posibles, 8)

        # La única puerta cerrada que no es la elegida
        st.session_state.otra_puerta = [
            i for i in range(10)
            if i != st.session_state.eleccion and i not in st.session_state.puertas_abiertas
        ][0]

        st.session_state.fase = "mostrar"

# --- FASE 2: Mostrar información y probabilidades ---
if st.session_state.fase == "mostrar":
    st.subheader("🔍 Monty abre 8 puertas con cabras")
    st.write(f"Las puertas abiertas fueron: **{[p+1 for p in st.session_state.puertas_abiertas]}**")

    # Probabilidades iniciales
    st.markdown("""
    ### 📊 Probabilidades iniciales
    - La puerta que escogiste originalmente tenía **1/10 = 10%** de contener el premio.
    - Las otras 9 puertas juntas tenían **9/10 = 90%** de contener el premio.
    """)

    # Explicación automática de Monty Hall
    st.markdown(f"""
    ### 📘 Condición después de abrir puertas
    Monty solo abre puertas que **seguro** tienen cabras.  
    Toda la probabilidad **9/10** que estaba en las 9 puertas se concentra en **la única puerta que queda cerrada**,  
    la puerta **{st.session_state.otra_puerta + 1}**.

    👉 Probabilidad actual:
    - Mantener tu puerta (**{st.session_state.eleccion + 1}**) → **10%**
    - Cambiar a la puerta **{st.session_state.otra_puerta + 1}** → **90%**
    """)

    cambiar = st.radio(
        f"¿Quieres cambiar a la puerta {st.session_state.otra_puerta + 1}?",
        ("No, mantener mi puerta", "Sí, quiero cambiar")
    )

    if st.button("Ver resultado"):
        if cambiar == "Sí, quiero cambiar":
            st.session_state.eleccion = st.session_state.otra_puerta

        if st.session_state.puertas[st.session_state.eleccion] == 1:
            st.success(f"🎉 ¡Ganaste! El premio estaba en la puerta {st.session_state.eleccion + 1}.")
        else:
            st.error(f"🐐 Lo siento, era una cabra. La puerta {st.session_state.eleccion + 1} no tenía el premio.")

        st.session_state.fase = "final"

# --- FASE 3: Jugar otra vez ---
if st.session_state.fase == "final":
    if st.button("🔄 Jugar de nuevo"):
        st.session_state.fase = "inicio"
        st.session_state.puertas = None
        st.session_state.eleccion = None
        st.session_state.puertas_abiertas = None
        st.session_state.otra_puerta = None
