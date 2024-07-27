# *******************************************************
# Nom ......... : Applications streamlit avec image
# Auteur ...... : Léa MOULINNEUF
# Version ..... : V0.1 du 11/05/2024
# Licence ..... : réalisé dans le cadre du cours des Outils collaboratifs
# Compilation : 
# Pour exécuter : uvicorn selenium_api:app --reload
#********************************************************/

from PIL import Image
import streamlit as st
import pandas as pd

# Charge l'image
image = Image.open("./streamlit/photo_lea.jpg")

# Obtiens les métadonnées EXIF
exif_data = image._getexif()

# Crée un DataFrame à partir des métadonnées EXIF
metadata_df = pd.DataFrame(exif_data.items(), columns=["Attribut", "Valeur"])

# Affiche le DataFrame dans le widget st.data_editor
st.data_editor(metadata_df)