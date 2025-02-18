import pandas as pd
import streamlit as st

# Lade die Excel-Datei
def load_data():
    file_path = "/mnt/data/Lignum Ökobilanzdatenrechner nach KBOB HS250218.xlsx"
    xls = pd.ExcelFile(file_path)
    oekobilanz_df = xls.parse("Ökobilanzrechner")
    auswahlfelder_df = xls.parse("Auswahlfelder")
    baumaterialien_df = xls.parse("Baumaterialien Matériaux")
    return oekobilanz_df, auswahlfelder_df, baumaterialien_df

# Daten laden
oekobilanz_df, auswahlfelder_df, baumaterialien_df = load_data()

# Streamlit-App
def main():
    st.title("Interaktiver Ökobilanzrechner für Holzbau")
    
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
