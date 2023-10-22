import pandas as pd

def importData(file_name:str):
    return pd.read_csv(file_name,sep="|",decimal=",",nrows=200000)

def combineData(datasets):
    combined = pd.DataFrame()
    for dataset in datasets:
        combined = pd.concat([combined,dataset])
    return combined

def processDataforDashBoard(combined,log_lat):
    #Séparation par Jour,Mois,Année
    try:
        combined['Date mutation'] = pd.to_datetime(combined['Date mutation'], format='%d/%m/%Y')
    except ValueError as e:
        print(f"Error: {e}")

    combined["Année"] = combined["Date mutation"].dt.year
    combined["Mois"] = combined["Date mutation"].dt.month
    combined["Lib mois"] = ["Janvier" if x==1  else "Février" if x==2 else "Mars" if x==3 else "Avril" if x==4 else "Mai" if x==5 else "Juin" if x==6 else "Juillet" if x==7 else "Août" if x==8 else "Septembre" if x==9 else "Octobre" if x==10 else "Novembre" if x==11 else "Décembre" if x==12 else x for x in combined["Mois"]]
    combined["Jour"] = combined["Date mutation"].dt.day
    #Suppression des colonnes completement nulles
    combined.dropna(axis=1, how='all')
    #Suppression des lignes ou il y a une référence à la même vente (Même addresse à une même date)
    combined = combined.drop_duplicates(subset=["Jour","Mois","Année","Code departement","Code commune","Code voie"],keep=False)
    combined["Catégorie Surface terrain"] = ["Petite" if x<=100  else "Moyenne" if x<=10000 else "Grande" for x in combined["Surface terrain"]]
    combined["Id"] = combined.index
    #Dataframe ventilé en fonction des différents axes d'analyse intéressants

    # Suppression des lignes sans valeur foncière
    combined["Valeur fonciere"] = combined["Valeur fonciere"].replace(",",".").astype(float)
    combined = combined[combined["Valeur fonciere"] >1 & combined["Valeur fonciere"].notna()]
    log_lat = log_lat[['nom_departement', 'nom_region','code_commune_INSEE', 'nom_commune_postal', 'latitude', 'longitude']]
    combined = pd.merge(combined, log_lat, left_on='Commune', right_on='nom_commune_postal')
    return combined

def processDataforPrediction(combined:pd.DataFrame):
    #Suppression des colonnes completement nulles
    cleaned = combined.dropna(axis=1, how='all')
    cleaned = cleaned.drop_duplicates(subset=["Jour","Mois","Année","Code departement","Code commune","Code voie"])
    cleaned.drop(["Année","Mois","Jour","Date mutation"])
    cleaned = cleaned[cleaned["Valeur fonciere"] != 0 & cleaned["Valeur fonciere"] != 1 & cleaned["Valeur fonciere"].notna()]
    percentage_missing = (cleaned.isna().sum() / len(cleaned)) * 100
    for colonne in cleaned:
        if percentage_missing[colonne] > 80 & colonne != "Type local":
            cleaned.drop(colonne, axis=1, inplace=True) 
    
    return cleaned
