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

# Charger l'image (remplacez 'votre_image.jpg' par le chemin de votre image)
image_path = 'photo_lea.jpg'
image = Image.open(image_path)

# Extraire les métadonnées EXIF (par exemple, la date de création, l'appareil photo, etc.)
exif_data = image._getexif()

# Créer un dataframe pandas avec les métadonnées
df = pd.DataFrame(exif_data.items(), columns=['Attribut', 'Valeur'])

# Afficher le widget st.data_editor
st.data_editor(df)

