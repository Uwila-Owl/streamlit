# *******************************************************
# Nom ......... : Applications streamlit avec image
# Auteur ...... : Léa MOULINNEUF
# Version ..... : V0.1 du 27/07/2024
# Licence ..... : réalisé dans le cadre du cours des Outils collaboratifs
# Compilation : 
# Pour exécuter : streamlit run streamlit_4.2.py
#********************************************************/

import streamlit as st
from PIL import Image
import piexif
import pandas as pd
from streamlit_folium import st_folium
import folium

#
# Modification des métadonnées d'une image 
#

def main():
    st.title("Modification des métadonnées EXIF")

    # Téléchargement de l'image
    uploaded_image = st.file_uploader("Téléchargez votre image", type=["jpg", "png"])

    if uploaded_image:
        image = Image.open(uploaded_image)

        # Affichage des métadonnées EXIF
        st.subheader("Métadonnées EXIF actuelles :")
        exif_dict = piexif.load(image.info["exif"])
        for ifd in ("0th", "Exif", "GPS", "1st"):
            for tag in exif_dict[ifd]:
                tag_name = piexif.TAGS[ifd][tag]["name"]
                value = exif_dict[ifd][tag]
                if isinstance(value, bytes):
                    value = value.decode("utf-8", errors="ignore")
                elif isinstance(value, tuple):
                    value = "".join(chr(i) for i in value if i != 0)
                st.write(f"{tag_name}: {value}")

        # Modification des métadonnées
        st.subheader("Modifier les métadonnées EXIF :")
        new_make = st.text_input("Nouvelle valeur pour 'Make'", exif_dict["0th"][271])
        new_model = st.text_input("Nouvelle valeur pour 'Model'", exif_dict["0th"][272])
        new_artist = st.text_input("Nouvelle valeur pour 'Artist'", exif_dict["0th"][315])
        new_copyright = st.text_input("Nouvelle valeur pour 'Copyright'", exif_dict["0th"][33432])
        new_xp_author = st.text_input("Nouvelle valeur pour 'XPAuthor'", "".join(chr(i) for i in exif_dict["0th"][40093] if i != 0))

        # Mise à jour de ces dernières
        exif_dict["0th"][271] = new_make
        exif_dict["0th"][272] = new_model
        exif_dict["0th"][315] = new_artist
        exif_dict["0th"][33432] = new_copyright
        exif_dict["0th"][40093] = tuple(ord(c) for c in new_xp_author) + (0,)

        # Affichage des nouvelles valeurs afin de montrer la prise en compte
        st.subheader("Nouvelles valeurs des métadonnées :")
        for ifd in ("0th", "Exif", "GPS", "1st"):
            for tag in exif_dict[ifd]:
                tag_name = piexif.TAGS[ifd][tag]["name"]
                value = exif_dict[ifd][tag]
                if isinstance(value, bytes):
                    value = value.decode("utf-8", errors="ignore")
                elif isinstance(value, tuple):
                    value = "".join(chr(i) for i in value if i != 0)
                st.write(f"{tag_name}: {value}")

        # Modification des données GPS
        st.subheader("Modifier les données GPS :")
        new_gps_latitude = st.text_input("Nouvelle latitude", "43.296482")
        new_gps_longitude = st.text_input("Nouvelle longitude", "5.36978")
        new_gps_altitude = st.text_input("Nouvelle altitude", "0")

        # Mise à jour des données GPS
        if new_gps_latitude and new_gps_longitude and new_gps_altitude:
            latitude = float(new_gps_latitude)
            longitude = float(new_gps_longitude)
            altitude = int(new_gps_altitude)
    
            latitude_degres = int(latitude)
            latitude_minutes = int((latitude - latitude_degres) * 60)
            latitude_secondes = int(((latitude - latitude_degres) * 3600) % 60)
    
            longitude_degres = int(longitude)
            longitude_minutes = int((longitude - longitude_degres) * 60)
            longitude_secondes = int(((longitude - longitude_degres) * 3600) % 60)
    
            exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = ((latitude_degres, 1), (latitude_minutes, 1), (latitude_secondes, 1))
            exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = ((longitude_degres, 1), (longitude_minutes, 1), (longitude_secondes, 1))
            exif_dict["GPS"][piexif.GPSIFD.GPSAltitude] = (altitude, 1)
        else:
            st.error("Veuillez remplir tous les champs de données GPS")

        # Affichage des coordonnées GPS sur une carte
        map_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
        st.map(map_data)

        # Bouton d'enregistrement de l'image
        if st.button("Enregistrer l'image"):
            exif_bytes = piexif.dump(exif_dict)
            image.save("image_modifiee.jpg", "jpeg", exif=exif_bytes)
            st.success("Image enregistrée avec succès !")

if __name__ == "__main__":
    main()

        
#
# Carte sur les pays visités et à visiter 
#
# Les lieux que j'ai visités 
def map_visited_places():
    st.title("Carte des pays visités")

    # Création de la carte
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=4)

    # Ajout des POI pour les lieux visités
    places = ["Heraklion", "Punta Cana", "Rome", "Londres"]
    latitudes = [35.34336, 18.582010, 41.891930, 54.633221] 
    longitudes = [25.13608, -68.405473, 12.511330, -3.32277]
    points = list(zip(latitudes, longitudes))
    folium.PolyLine(points, color='green').add_to(m)
    for i, place in enumerate(places):
        folium.Marker(location=[latitudes[i], longitudes[i]], popup=place).add_to(m)

    # Affichage de la carte
    st_folium(m, width=800, height=600, key="visited_map")

# Les lieux que je désire visiter
def map_wanted_places():
    st.title("Carte des pays à visiter")

    # Création de la carte
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=4)

    # Ajout des POI pour les lieux à visiter
    places = ["Tokyo", "Séoul", "Athènes", "Wellington"]
    latitudes = [34.886306, 37.566535, 38.275283, -40.900557]  
    longitudes = [134.39711, 126.9779692, 23.810343, 174.885971]  
    points = list(zip(latitudes, longitudes))
    folium.PolyLine(points, color='red').add_to(m)
    for i, place in enumerate(places):
        folium.Marker(location=[latitudes[i], longitudes[i]], popup=place).add_to(m)

    # Affichage de la carte
    st_folium(m, width=800, height=600, key="wanted_map")

st.title("Carte sur les pays visités et à visiter")
st.write("")

# Gestion des cartes par un système d'onglet
tab1, tab2 = st.tabs(["Pays visités", "Pays à visiter"])

with tab1:
    map_visited_places()

with tab2:
    map_wanted_places()
