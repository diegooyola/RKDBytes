
import numpy as np
import pandas as pd
import streamlit as st
import importlib
import os
import sys
import time



def file_selector(folder_path='.'):

    filenames = os.listdir(folder_path)
    filenames_ = [f for f in filenames if f[-3:] == "txt"]
    selected_filename = st.selectbox('Select a file', filenames_)
    return os.path.join(folder_path, selected_filename)



st.header("Rocking Data Bytes")

modo = st.sidebar.radio("Modo", options=["Buscar contenido", "Subir contenido", "Configuración"], index=0)

if "METADATA.csv" in os.listdir(".") and "TAGS.csv" in os.listdir("."):

    METADATA = pd.read_csv("./METADATA.csv", index_col=0)
    TAGS = pd.read_csv("./TAGS.csv", index_col=0)

else:

    METADATA = pd.DataFrame(np.zeros((1, 5)), index=["INIT"], columns=["TAG_{}".format(i) for i in range(1,6)])
    METADATA.to_csv("./METADATA.csv")

    TAGS = pd.DataFrame({"TAGS":["funciones", "machine learning", "visualizacion", "estadistica"]})
    TAGS.to_csv("./TAGS.csv")


if modo == "Buscar contenido":

    METADATA = pd.read_csv("./METADATA.csv", index_col=0)
    TAGS = pd.read_csv("./TAGS.csv", index_col=0)

    search_tags = st.multiselect("Tags", options=[_[0] for _ in TAGS.values])

    available_bytes = []

    for byte in METADATA.index:

        if sum([tag_ in METADATA.loc[byte].values for tag_ in search_tags]) == len(search_tags):
            print(sum([tag_ in METADATA.loc[byte] for tag_ in search_tags]))
            available_bytes.append(byte)

    if search_tags == []:

        selection = st.selectbox("Índice", options=METADATA.index[1:])

    else:

        selection = st.selectbox("Índice", options=available_bytes)

    if st.button("Ver"):

        importlib.import_module("{}".format(selection))
        del sys.modules["{}".format(selection)]



elif modo == "Subir contenido":

    METADATA = pd.read_csv("./METADATA.csv", index_col=0)
    TAGS = pd.read_csv("./TAGS.csv", index_col=0)

    nombre = st.text_input("Nombre")
    tags = st.multiselect("Tags", options=[_[0] for _ in TAGS.values])
    path = file_selector()

    base = open(os.getcwd() + "/{}.py".format(nombre), "w", encoding="utf-8")
    base.write("import streamlit as st\nwith st.echo():\n")
    base.close()

    flag_1 = nombre is not None
    flag_2 = tags is not None

    FLAGS = flag_1 + flag_2

    if FLAGS == 2 and st.button("Guardar"):

        temp = open(path, "r", encoding="utf-8")

        base_ = open(os.getcwd() + "/{}.py".format(nombre), "a", encoding="utf-8")
        for line in temp:
            base_.write("\t"+line)

        temp.close()
        base_.close()

        for i in range(5-len(tags)):
            tags.extend([0])

        print({nombre:tags})

        METADATA.loc[nombre, :] = tags
        METADATA.to_csv("./METADATA.csv")

else:

    st.empty().text(" ")
    st.info("Actualmente existen {} bytes almacenados y {} tags".format(METADATA.shape[0]-1, len(TAGS.values)))
    st.empty().text(" ")
    st.subheader("Metadata")
    st.empty().text(" ")

    if st.button("Resetear metadata"):

        METADATA = pd.DataFrame(np.zeros((1, 5)), index=["INIT"], columns=["TAG_{}".format(i) for i in range(1, 6)])
        METADATA.to_csv("./METADATA.csv")

    if st.button("Ver metadata"):

        st.write(METADATA.iloc[1:, :])

    st.subheader("Tags")

    new_tag = st.text_input("Agregar un nuevo tag")

    if new_tag is not None and st.button("Agregar tag"):

        redundancia = False

        if new_tag in TAGS.values:
            redundancia = True

        if redundancia is False:

            TAGS = pd.concat([TAGS, pd.DataFrame({"TAGS":new_tag}, index=[0])], axis=0, sort=False)
            st.write(TAGS)
            TAGS.to_csv("./TAGS.csv")

        else:

            with st.spinner("{} ya se encuentra entre los tags!".format(new_tag)):
                time.sleep(1.5)

#    if st.button("Ver tags"):

#        TAGS = pd.read_csv("./TAGS.csv", index_col=0)
#        st.write(TAGS)






