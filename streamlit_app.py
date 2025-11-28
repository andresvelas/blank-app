import streamlit as st
import random

st.title("Juego Monty Hall Interactivo y Probabilístico")
st.write("""
Bienvenida/o al juego de Monty Hall con **10 puertas**.  
Detrás de **9 puertas hay una cabra** y detrás de **1 el premio**.  
Vamos a explorar **probabilidades paso a paso**.
""")

# Inicializamos el estado de la app
if 'estado' not in st.session_state:
    st.session_state.estado = 'inicio'
    st.session_state.puertas = []
    st.session_state.eleccion = None
    st.session_state.puertas_abiertas = []
    st.session_state.otra_puerta = None

# Paso 1: Elegir puerta
if st.session_state.estado == 'inicio':
    puerta = st.number_input("Elige una puerta del 1 al 10:", min_value=1, max_value=10, step=1)
    if st.button("Confirmar elección"):
        st.session_state.eleccion = puerta - 1
        # Crear puertas
        st.session_state.puertas = [0]*9 + [1]
        random.shuffle(st.session_state.puertas)
        st.session_state.estado = 'pregunta_prob1'

# Paso 2: Preguntar probabilidad de la puerta escogida
if st.session_state.estado == 'pregunta_prob1':
    st.write(f"Elegiste la puerta {st.session_state.eleccion+1}.")
    prob_elegida = st.number_input("¿Cuál crees que es la probabilidad de que el premio esté en tu puerta elegida?", min_value=0.0, max_value=1.0, step=0.01, key='prob1')
    if st.button("Siguiente paso"):
        st.session_state.estado = 'pregunta_prob2'

# Paso 3: Preguntar probabilidad de las puertas restantes
if st.session_state.estado == 'pregunta_prob2':
    prob_restantes = st.number_input("¿Cuál crees que es la probabilidad de que el premio esté en las **otras 9 puertas**?", min_value=0.0, max_value=1.0, step=0.01, key='prob2')
    if st.button("Abrir 8 puertas sin premio"):
        # Monty abre 8 puertas sin premio
        indices_posibles = [i for i in range(10) if i != st.session_state.eleccion and st.session_state.puertas[i] == 0]
        st.session_state.puertas_abiertas = random.sample(indices_posibles, 8)
        # Determinar la única puerta cerrada restante
        st.session_state.otra_puerta = [i for i in range(10) if i != st.session_state.eleccion and i not in st.session_state.puertas_abiertas][0]
        st.session_state.estado = 'pregunta_prob_condicional'

# Paso 4: Preguntar probabilidad condicional
if st.session_state.estado == 'pregunta_prob_condicional':
    st.write(f"Se abren las puertas { [i+1 for i in st.session_state.puertas_abiertas] } y todas tienen cabras.")
    st.write("Ahora solo quedan 2 puertas cerradas: tu elección inicial y una otra puerta.")
    prob_condicional = st.number_input("¿Cuál crees que es la probabilidad de que el premio esté en cada una de estas 2 puertas condicionada a que esté en las cerradas?", min_value=0.0, max_value=1.0, step=0.01, key='prob_cond')
    if st.button("Revelar resultado y explicación"):
        # Explicación de la redistribución de probabilidades
        st.write("✅ Explicación:")
        st.write("Originalmente tu puerta tenía probabilidad 1/10, y las otras 9 puertas 9/10.")
        st.write("Monty abrió 8 puertas sin premio. Esto **no cambia la probabilidad inicial de tu puerta**, pero toda la probabilidad de las 9 puertas restantes se concentra en la única puerta cerrada que no elegiste.")
        st.write(f"Por tanto, ahora tu puerta sigue con probabilidad **1/10** y la otra puerta cerrada tiene **9/10**.")
        st.session_state.estado = 'resultado'

# Paso 5: Mostrar resultado y opción de cambiar
if st.session_state.estado == 'resultado':
    cambiar = st.radio(
        f"Tu puerta actual es {st.session_state.eleccion+1}. La otra puerta cerrada es {st.session_state.otra_puerta+1}. ¿Deseas cambiar?",
        ('No', 'Sí')
    )
    if st.button("Mostrar resultado final"):
        if cambiar == 'Sí':
            st.session_state.eleccion = st.session_state.otra_puerta
        # Mostrar resultado
        if st.session_state.puertas[st.session_state.eleccion] == 1:
            st.success(f"🎉 ¡Felicidades! Has ganado el premio en la puerta {st.session_state.eleccion+1}.")
        else:
            st.error(f"🐐 Lo siento, hay una cabra detrás de la puerta {st.session_state.eleccion+1}.")
        st.session_state.estado = 'reinicio'

# Paso 6: Preguntar si quiere volver a jugar
if st.session_state.estado == 'reinicio':
    if st.button("Volver a jugar"):
        st.session_state.estado = 'inicio'
        st.session_state.puertas = []
        st.session_state.eleccion = None
        st.session_state.puertas_abiertas = []
        st.session_state.otra_puerta = None
