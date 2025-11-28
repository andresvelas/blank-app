import streamlit as st
import random

# Inicializamos el estado de la app para mantener variables entre interacciones
if 'jugando' not in st.session_state:
    st.session_state.jugando = False
if 'puertas' not in st.session_state:
    st.session_state.puertas = []
if 'eleccion' not in st.session_state:
    st.session_state.eleccion = None
if 'otra_puerta' not in st.session_state:
    st.session_state.otra_puerta = None
if 'resultado_mostrado' not in st.session_state:
    st.session_state.resultado_mostrado = False

st.title("Juego Monty Hall con 10 puertas")
st.write("Detrás de 9 puertas hay una cabra y detrás de 1 el premio.")

# Si no estamos jugando, seleccionar puerta
if not st.session_state.jugando:
    puerta = st.number_input("Elige una puerta del 1 al 10:", min_value=1, max_value=10, step=1)
    if st.button("Confirmar elección"):
        # Iniciar juego
        st.session_state.jugando = True
        st.session_state.eleccion = puerta - 1
        # Crear puertas y barajar
        st.session_state.puertas = [0]*9 + [1]
        random.shuffle(st.session_state.puertas)
        # Monty abre 8 puertas sin premio
        indices_posibles = [i for i in range(10) if i != st.session_state.eleccion and st.session_state.puertas[i] == 0]
        st.session_state.puertas_abiertas = random.sample(indices_posibles, 8)
        # Determinar la única puerta cerrada restante
        st.session_state.otra_puerta = [i for i in range(10) if i != st.session_state.eleccion and i not in st.session_state.puertas_abiertas][0]

# Si estamos jugando, mostrar info y preguntar si quiere cambiar
if st.session_state.jugando and not st.session_state.resultado_mostrado:
    st.write(f"Se abren las puertas { [i+1 for i in st.session_state.puertas_abiertas] } y todas tienen cabras.")
    
    cambiar = st.radio(
        f"Tu puerta actual es {st.session_state.eleccion+1}. Si cambias, irías a la puerta {st.session_state.otra_puerta+1}. ¿Deseas cambiar?",
        ('No', 'Sí')
    )
    
    if st.button("Mostrar resultado"):
        if cambiar == 'Sí':
            st.session_state.eleccion = st.session_state.otra_puerta
        # Mostrar resultado
        if st.session_state.puertas[st.session_state.eleccion] == 1:
            st.success(f"¡Felicidades! Has ganado el premio en la puerta {st.session_state.eleccion+1}.")
        else:
            st.error(f"Lo siento, hay una cabra detrás de la puerta {st.session_state.eleccion+1}. Mejor suerte la próxima vez.")
        st.session_state.resultado_mostrado = True

# Preguntar si quiere volver a jugar
if st.session_state.resultado_mostrado:
    if st.button("Volver a jugar"):
        # Resetear el estado
        st.session_state.jugando = False
        st.session_state.resultado_mostrado = False
        st.session_state.eleccion = None
        st.session_state.puertas = []
        st.session_state.otra_puerta = None
