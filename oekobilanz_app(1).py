import pandas as pd
import streamlit as st

# Datei-Upload über Streamlit
st.sidebar.header("📂 Datei-Upload")
uploaded_file = st.sidebar.file_uploader("Bitte Excel-Datei hochladen", type=["xlsx"])

def load_data(file):
    if file is not None:
        xls = pd.ExcelFile(file)
        oekobilanz_df = xls.parse("Ökobilanzrechner")
        auswahlfelder_df = xls.parse("Auswahlfelder")
        baumaterialien_df = xls.parse("Baumaterialien Matériaux")
        return oekobilanz_df, auswahlfelder_df, baumaterialien_df
    else:
        return None, None, None

# Daten laden
oekobilanz_df, auswahlfelder_df, baumaterialien_df = load_data(uploaded_file)

# Streamlit-App
def main():
    st.title("Interaktiver Ökobilanzrechner für Holzbau")
    
    if oekobilanz_df is None:
        st.warning("Bitte eine gültige Excel-Datei hochladen.")
        return
    
    # Auswahlfelder für Materialien
    st.sidebar.header("Bauteilschichten")
    schichten = ["Bauteilschicht 1", "Bauteilschicht 2", "Bauteilschicht 3"]
    material_auswahl = {}
    
    for schicht in schichten:
        material_auswahl[schicht] = st.sidebar.selectbox(
            f"Material für {schicht}", 
            baumaterialien_df.iloc[:, 2].dropna().unique()
        )
    
    # Berechnung der Ökobilanz
    st.subheader("Ergebnisse der Ökobilanz")
    ergebnis_df = pd.DataFrame(columns=["Bauteilschicht", "Material", "CO₂-Emissionen (kg CO₂-eq)", "Graue Energie (kWh)"])
    
    for schicht, material in material_auswahl.items():
        material_daten = oekobilanz_df[oekobilanz_df["Produkt KBOB"] == material]
        if not material_daten.empty:
            co2_emissionen = material_daten.iloc[0]["Treibhausgas-\nemissionen"]
            graue_energie = material_daten.iloc[0]["nicht erneuerbar (Graue Energie)"]
            ergebnis_df = ergebnis_df.append({
                "Bauteilschicht": schicht,
                "Material": material,
                "CO₂-Emissionen (kg CO₂-eq)": co2_emissionen,
                "Graue Energie (kWh)": graue_energie
            }, ignore_index=True)
    
    st.dataframe(ergebnis_df)
    
    # Exportfunktion
    st.download_button("Ergebnisse als CSV herunterladen", ergebnis_df.to_csv(index=False), "oekobilanz_ergebnisse.csv")

if __name__ == "__main__":
    main()
