# *******************************************************
# Nom ......... : Applications streamlit avec image
# Auteur ...... : Léa MOULINNEUF
# Version ..... : V0.1 du 11/05/2024
# Licence ..... : réalisé dans le cadre du cours des Outils collaboratifs
# Compilation : 
# Pour exécuter : uvicorn selenium_api:app --reload
#********************************************************/

import streamlit as st
from PIL import Image
import piexif

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

        # Mettre à jour les métadonnées
        exif_dict["0th"][271] = new_make
        exif_dict["0th"][272] = new_model
        exif_dict["0th"][315] = new_artist
        exif_dict["0th"][33432] = new_copyright
        exif_dict["0th"][40093] = tuple(ord(c) for c in new_xp_author) + (0,)

        # Affichage des nouvelles valeurs
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

        # Bouton d'enregistrement
        if st.button("Enregistrer l'image"):
            exif_bytes = piexif.dump(exif_dict)
            image.save("image_modifiee.jpg", "jpeg", exif=exif_bytes)
            st.success("Image enregistrée avec succès !")

if __name__ == "__main__":
    main()
