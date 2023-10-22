from views.model.prediction import predictionForm
from views.model.training import training
from dash import Input, Output,State,html,dash_table
import pandas as pd
from server import app
from datetime import date
from controllers.process.ImportController import *
import os
import pickle
path = "C:/Users/leogo/Documents/Prediction/Python_ML"
os.chdir(path)

cleaned = pd.read_csv("assets/data/cube.csv")
#Pour afficher le menu "Tableau de Bord"
@app.callback(
    Output("menu-prediction", "className",allow_duplicate=True),

    Output("submenus-prediction", "hidden",allow_duplicate=True),
    Output("sub-menu-prediction", "className",allow_duplicate=True),
    Output("sub-menu-train", "className",allow_duplicate=True),

    Output("menu-dashboard", "className",allow_duplicate=True),
    Output("menu-history", "className",allow_duplicate=True),
    Output("menu-parameters", "className",allow_duplicate=True),

    Output("submenus-history", "hidden",allow_duplicate=True), 
    Output("submenus-visualization", "hidden",allow_duplicate=True),
    Output("homepage", "className",allow_duplicate=True),

    Input("menu-prediction", "n_clicks"),
    State("submenus-prediction", "hidden"),

    prevent_initial_call=True       
)
def toggleMenu(n_clicks,isDisplayed):
    tuple = ()
    if n_clicks is not None and n_clicks>0:
        if(not(isDisplayed)):
            tuple = "active",True,"","","","","",True,True,""
        else:
            tuple = "active",False,"","","","","",True,True,""
        return tuple

@app.callback(
    Output("screen-menu", "children",allow_duplicate=True),
    Output("sub-menu-prediction", "className",allow_duplicate=True),
    Output("sub-menu-train", "className",allow_duplicate=True),

    Input("sub-menu-prediction", "n_clicks"),
    prevent_initial_call=True   
)
def displayPredictionForm(n_clicks):
    if n_clicks is not None and n_clicks>0:
        return predictionForm,"active",""

@app.callback(
    Output("screen-menu", "children",allow_duplicate=True),
    Output("sub-menu-train", "className",allow_duplicate=True),
    Output("sub-menu-prediction", "className",allow_duplicate=True),

    Input("sub-menu-train", "n_clicks"),
    prevent_initial_call=True   
)
def displayTrainModel(n_clicks):
    if n_clicks is not None and n_clicks>0:
        return training,"active",""
    
@app.callback(
    Output("cb-Department", "options",allow_duplicate=True),
    Output("cb-Commune", "options",allow_duplicate=True),
    Input("cb-Region", "value"),
    prevent_initial_call=True   
)   
def filterDepartement(region):
    if region is not None:
        cleaned_copy = cleaned.copy()
        cleaned_copy = cleaned_copy[cleaned_copy["nom_region"]==region]
        return sorted(cleaned_copy["nom_departement"].unique()),[]

@app.callback(
    Output("cb-Commune", "options",allow_duplicate=True),
    Input("cb-Department", "value"),
    prevent_initial_call=True   
)   
def filterDepartement(department):
    if department is not None:
        cleaned_copy = cleaned.copy()
        cleaned_copy = cleaned_copy[cleaned_copy["nom_departement"]==department]
        return sorted(cleaned_copy["Commune"].unique())
    
val_fonc=None
@app.callback(
    Output("output-error", "children",allow_duplicate=True),
    Output("output-prediction", "children",allow_duplicate=True),
    Output("output-prediction", "style",allow_duplicate=True),
    Output("btn-save-prediction", "style",allow_duplicate=True),

    Input("btn-predict", "n_clicks"),

    State("txt-surface-bati", "value"),
    State("txt-surface-terrain", "value"),
    State("txt-surface-nb-pieces", "value"),
    State("cb-Commune", "value"),
    prevent_initial_call=True   
)  

def predictValeurFonciere(n_clicks,surface_bati,surface_terrain,nbpiece,commune):
    if n_clicks is not None:
        global val_fonc
        if surface_bati is None:
            return 'Veuillez renseigner une surface batiment','',{},{}
        if surface_terrain is None:
            return 'Veuillez renseigner une surface terrain','',{},{}
        if nbpiece is None:
            return 'Veuillez renseigner un nombre de pièce','',{},{}
        if commune is None:
            return 'Veuillez renseigner une commune','',{},{}
        try:
            surface_bati = float(surface_bati)
        except ValueError:
            return 'Veuillez renseigner une surface batiment en format décimal avec des . comme séparateurs de décimales','',{},{}
        try:
            surface_terrain = float(surface_terrain)
        except ValueError:
            return 'Veuillez renseigner une surface terrain en format décimal avec des . comme séparateurs de décimales','',{},{}     
        try:
            nbpiece = int(nbpiece)
        except ValueError:
            return 'Veuillez renseigner un nombre de piece en format nombre entier','',{},{}
        
        ref_commune = pd.read_csv("assets/data/ref_Commune.csv")
        line = ref_commune[ref_commune["Commune"]==commune]
        prix_m2 = line["Prix_m2"]         
        nb_ecoles = line["nombre_ecoles"]  

        data = {"Surface reelle bati":[surface_bati],"Surface terrain":[surface_terrain],"Nombre pieces principales":[nbpiece],"nombre_ecoles":[nb_ecoles],"Prix_m2":[prix_m2]}
        Xtest = pd.DataFrame(data=data)
        model = pickle.load(open("assets/data/model_prediction_valeur_fonciere.pkl","rb"))
        
        val_fonc = model.predict(Xtest)

        return '',html.Div([f'Valeur foncière prédite : {val_fonc} €',html.Br()]),{"border":"solid 1px","text-align":"center","font-weight":"bold","justify-content": "center","display":"flex","align-items": "center","height":"60px","padding-bottom":"4px"},{"width":"130px","height":"30px","font-size":"20px","margin-top":"10px","display":"block","margin":"0 auto","top":"-35px"}

@app.callback(
    Output("output-error", "children",allow_duplicate=True),
    Output("output-error", "style",allow_duplicate=True),

    Input("btn-save-prediction", "n_clicks"),

    State("txt-surface-bati", "value"),
    State("txt-surface-terrain", "value"),
    State("txt-surface-nb-pieces", "value"),
    State("cb-Region", "value"),
    State("cb-Department", "value"),
    State("cb-Commune", "value"),
    prevent_initial_call=True   
)  
def savePrediction(n_clicks,surface_bati,surface_terrain,nbpiece,region,departement,commune):
    if n_clicks is not None:
        if surface_bati != "" and surface_terrain != "" and nbpiece != "" and region != "" and departement != "" and commune!="":
            data = {"Surface reelle bati":[surface_bati],"Surface terrain":[surface_terrain],"Nombre pieces principales":[nbpiece],"Region":[region],"Departement":[departement],"Commune":[commune],"Valeur fonciere":[val_fonc],"Date creation" : [date.today()]}
            line = pd.DataFrame(data=data)
            df=pd.read_csv("assets/data/history/predict/savedPrediction.csv")
            new_df = pd.concat([df,line],axis=0,ignore_index=True)
            new_df.to_csv("assets/data/history/predict/savedPrediction.csv",index=False)
            return "Sauvegardé avec succès",{"color":"green"}
        else:
            return "La sauvegarde ne peut pas être faite avec des valeurs manquantes",{"color":"red"}


import base64
import io
def parse_content(contents, filename,sep):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')),sep=sep)
    if 'txt' in filename:
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')),sep=sep)
    if 'xlsx' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))

    return html.Div(id="div-output",children=[html.Div([html.Div(id="options",children=[html.H2(id="h2-preview",children="Voici l'aperçu du jeu de donnée à insérer, souhaitez-vous valider son ajout ?"),html.Button(id="btn-validate",children="Valider l'insertion",style={"margin-left":"5px"}),html.Button(id="btn-cancel",children="Annuler",style={"margin-left":"5px"})])],style={"border":"solid 1px","height":"90px","background-color":"lightblue"}),
            html.Div(dash_table.DataTable(id="preview-table",
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns]
                ),
                style={"padding-top":"10px","overflow":"auto","height":"500px","width":"1150px"})
            ])
@app.callback(
    Output("lbl-separator", "style"),
    Output("txt-separator", "style"),
    Output("btn-show-preview","style"),
    Output("lbl-separator", "children"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_callback = True
)
def update_output(content,name):
    if content is not None:
        if name.split(".")[1] in ["csv","txt"]:
            return {"display":"block","padding-right":"10px"},{"display":"block"},{"display":"block","margin-left":"5px"},f"Fichier .{name.split('.')[1]} détecté ({name}), renseignez un séparateur de colonne"   
        if name.split(".")[1] in "xlsx":
            return {"display":"block"},{"display":"none"},{"display":"block","margin-left":"5px"},f"Fichier .xlsx détecté ({name})"  
    return {"display":"block"},{"display":"none"},{"display":"none"},"Aucun fichier détecté (si vous avez inséré un fichier assurez vous qu'il soit en extension .xlsx/.txt/.csv)" 
        # return parse_content(content, name)
file_name = ""
@app.callback(
    Output("output-data-upload","children"),

    Input('btn-show-preview', 'n_clicks'),

    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('txt-separator', 'value'),
    prevent_initial_callback = True
)

def showDataPreview(n_clicks,content,name,sep):
    if n_clicks is not None:
        global file_name
        file_name=name
        return parse_content(content,name,sep)

#return True si le jeu de données est intègre
def checkTrainingIntegrity(data):
    #Vérifier qu'il y ait bien des noms de colonnes et qu'ils soient les même que le template, vérifier qu'il y ait au moins une ligne, vérifier si le type de chacun des données est le même que le template    
    checkCols = [item.strip() in data.columns for item in ["Valeur fonciere", "Surface reelle bati", "Nombre pieces principales", "Surface terrain", "Commune"]]
    if not(all(checkCols)):
        return False,"Jeu de données non valide, veuillez suivre le template"
    if len(data)==0:
        return False,"Aucune donnée renseignée"
    for col in ["Valeur fonciere", "Surface reelle bati","Surface terrain"]:
        if not(data[col].astype(str).str.match(r'^-?\d+(\.\d+)?$').any()):
            return False,f"Le format renseigné de \"{col}\" n'est pas le bon, veuillez renseigner des nombres à décimales (avec un \".\" comme séparateur)"
    if not(data["Nombre pieces principales"].astype(str).str.match(r'^[0-9]+$').any()):
        return False,f"Le format renseigné de \"Nombre pieces principales\" n'est pas le bon, veuillez renseigner des nombres à décimales (avec un \".\" comme séparateur)"  
    if data.isna().sum().sum()>0:
        return False,"Il ne faut aucune donnée manquante dans le jeu de données"
    ref_commune = cleaned["Commune"].unique()
    if (~data['Commune'].isin(ref_commune)).any():
        return False,"Veuillez renseigner des communes existantes dans le jeu de donnée"
    return True,"Sauvegardé avec succès !"

@app.callback(
    Output("h2-preview","children"),
    Input("btn-validate","n_clicks"),
    State("preview-table","data"),
    prevent_initial_callback = True
)
def saveData(n_clicks,df):
    if n_clicks is not None:
        data = [{key.strip('\ufeff'): value for key, value in dfDict.items()} for dfDict in df]
        finalDf=pd.DataFrame(data=data)
        if "Commune" in finalDf.columns:
            finalDf['Commune'] = finalDf['Commune'].str.upper()
        result,message=checkTrainingIntegrity(finalDf)
        if(not(result)):
            return message       
        dfImported = pd.read_csv("C:/Users/leogo/Documents/Prediction/Python_ML/assets/data/history/train/train.csv")
        index = max(dfImported.iloc[:,0])+1 if len(dfImported)>0 else 1
        line = pd.DataFrame(data={"index":[index],"Nom_de_fichier":[file_name],"Date_creation":[date.today()]})
        pd.concat([dfImported,line]).to_csv("C:/Users/leogo/Documents/Prediction/Python_ML/assets/data/history/train/train.csv",index=False)
        finalDf.to_csv("C:/Users/leogo/Documents/Prediction/Python_ML/assets/data/history/train-details/"+str(index)+".csv",index=False)
        return message
    else:
        return "Voici l'aperçu du jeu de donnée à insérer, souhaitez-vous valider son ajout ?" 
    
@app.callback(
    Output("div-output","style"),
    Input("btn-cancel","n_clicks"),
    prevent_initial_callback = True
)
def saveData(n_clicks):
    if n_clicks is not None:
        return {"display":"none"}
    
