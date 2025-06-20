import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_log(file):
    return pd.read_csv(file, sep='|', header=None, names=['timestamp', 'transmissor', 'frame', 'tentativa'], parse_dates=['timestamp'])

st.title("Monitoramento CSMA/CD")

if st.button("Atualizar gráficos"):
    try:
        collisions = load_log("logs/collisions.log")
        success = load_log("logs/success.log")
    except FileNotFoundError:
        st.error("Arquivos de log não encontrados.")
        st.stop()

    col_counts = collisions['transmissor'].value_counts()
    suc_counts = success['transmissor'].value_counts()
    df = pd.DataFrame({'Colisões': col_counts, 'Sucessos': suc_counts}).fillna(0)

    st.bar_chart(df)

    st.write("Detalhes das colisões")
    st.dataframe(collisions)

    st.write("Detalhes dos sucessos")
    st.dataframe(success)
