from views.history.historyPred import historyPred
from views.history.historyTrain import historyTrain
from dash import Input, Output,State,html
from server import app
import dash_core_components as dcc,dash_table
import pandas as pd
#Pour afficher le menu "Tableau de Bord"
@app.callback(
    Output("menu-history", "className",allow_duplicate=True),

    Output("submenus-history", "hidden",allow_duplicate=True),
    Output("sub-menu-dashboard", "className",allow_duplicate=True),
    Output("sub-menu-map", "className",allow_duplicate=True),

    Output("menu-dashboard", "className",allow_duplicate=True),
    Output("menu-prediction", "className",allow_duplicate=True),
    Output("menu-parameters", "className",allow_duplicate=True),

    Output("submenus-prediction", "hidden",allow_duplicate=True), 
    Output("submenus-visualization", "hidden",allow_duplicate=True),
    Output("homepage", "className",allow_duplicate=True),

    Input("menu-history", "n_clicks"),
    State("submenus-history", "hidden"),

    prevent_initial_call=True       
)
def toggleMenu(n_clicks,isDisplayed):
    tuple = ()
    if n_clicks is not None:
        if(not(isDisplayed)):
            tuple = "active",True,"","","","","",True,True,""
        else:
            tuple = "active",False,"","","","","",True,True,""
        return tuple
    
@app.callback(
    Output("screen-menu", "children",allow_duplicate=True),
    Output("sub-menu-history-predict", "className",allow_duplicate=True),
    Output("sub-menu-history-train", "className",allow_duplicate=True),

    Input("sub-menu-history-predict", "n_clicks"),
    prevent_initial_call=True   
)
def displayPredictionHistory(n_clicks):
    if n_clicks is not None and n_clicks>0:
        df=pd.read_csv("assets/data/history/predict/savedPrediction.csv")
        savedPrediction = [
            html.Div(id="div-saved-predictions",
                children=[dash_table.DataTable(
                    id="preview-table-prediction",
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                )],style={"padding-left":"20px","overflow":"auto","width":"1100px","height":"600px"}
            )            
        ]  if len(df)>0 else [html.Label("Aucune donnée historisée",style={"font-size":"30px","font-weight":"bold"})]
        return [historyPred]+savedPrediction,"active",""
  
df = pd.DataFrame()  
@app.callback(
    Output("screen-menu", "children",allow_duplicate=True),
    Output("sub-menu-history-train", "className",allow_duplicate=True),
    Output("sub-menu-history-predict", "className",allow_duplicate=True),

    Input("sub-menu-history-train", "n_clicks"),
    prevent_initial_call=True   
)

def displayTrainingHistory(n_clicks):
    if n_clicks is not None and n_clicks>0:
        global df
        df=pd.read_csv("C:/Users/leogo/Documents/Prediction/Python_ML/assets/data/history/train/train.csv")
        train = [html.Div(id="table-uploaded-files",children=
                                        dash_table.DataTable(
                                            id="preview-table",
                                            data=df.to_dict('records'),
                                            columns=[{'name': i, 'id': i} for i in df.columns],
                                        )                            
                        ,style={"padding-top":"10px","overflow-y":"auto","height":"1000px","width":"500px"})] if len(df)>0 else [html.Label("Aucune donnée historisée",style={"font-size":"30px","font-weight":"bold"})]

        return [historyTrain]+train,"active",""
    
@app.callback(
    Output('div-details', 'children'),
    Input('preview-table', 'active_cell'),
    prevent_initial_callback=True
)
def displayDetails(selected):
    if selected is not None:
        index = selected['row']
        dfDetails = pd.read_csv("C:/Users/leogo/Documents/Prediction/Python_ML/assets/data/history/train-details/"+str(df.at[index,"index"])+".csv")
        return dash_table.DataTable(
                    id="preview-details",
                    data=dfDetails.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in dfDetails]
                )