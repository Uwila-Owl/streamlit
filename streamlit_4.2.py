# *******************************************************
# Nom ......... : Applications streamlit avec image
# Auteur ...... : Léa MOULINNEUF
# Version ..... : V0.1 du 11/05/2024
# Licence ..... : réalisé dans le cadre du cours des Outils collaboratifs
# Compilation : 
# Pour exécuter : uvicorn selenium_api:app --reload
#********************************************************/

import streamlit as st
import pandas as pd
from PIL import Image

# Chargez l'image
uploaded_image = st.file_uploader("Téléchargez une image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # Ouvrez l'image avec Pillow
    image = Image.open(uploaded_image)

    # Extrayez les métadonnées EXIF (par exemple, le nom de l'auteur, la date de création, etc.)
    # Créez un DataFrame avec ces métadonnées
    metadata_df = pd.DataFrame({
        "Nom de l'auteur": ["John Doe"],
        "Date de création": ["2023-07-28"],
        "Version": ["1.0"]
    })

    # Affichez le DataFrame dans le widget st.data_editor
    st.data_editor(metadata_df)
