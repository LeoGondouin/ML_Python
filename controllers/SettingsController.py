from views.settings.settings import appSettings
from dash import Input, Output,State,html,dcc
from server import app
import json



#Pour afficher le menu "Tableau de Bord"
@app.callback(
    Output("screen-menu", "children",allow_duplicate=True),

    Output("menu-parameters", "className",allow_duplicate=True),
    Output("menu-history", "className",allow_duplicate=True),    
    Output("menu-dashboard", "className",allow_duplicate=True),
    Output("menu-prediction", "className",allow_duplicate=True),

    Output("submenus-visualization", "hidden",allow_duplicate=True),
    Output("submenus-prediction", "hidden",allow_duplicate=True),
    Output("submenus-history", "hidden",allow_duplicate=True),
    Output("homepage", "className",allow_duplicate=True),

    Input("menu-parameters", "n_clicks"),

    prevent_initial_call=True      
)
def display(n_clicks):
    if n_clicks is not None and n_clicks > 0:       
        with open("assets/settings/saved_settings.json")as f:
            params = json.load(f) 
        parameter = [
            html.Div(id="div-success",style={"background-color":"green"}),
            html.H2("Filtrage"),html.Br(),
            dcc.Checklist(
                id="chk-list-filtrage",
                options=["Filtres multi-selection","Filtres intelligents"],
                value=["Filtres multi-selection" if params["multi"] else None, "Filtres intelligents" if params["filterCb"] else None]
            ),
            html.H2("Visualisation"),dcc.Checklist(),html.Br(),
            dcc.Checklist(
                id="chk-list-viz",
                options=["Ordonner les graphiques"],
                value=["Ordonner les graphiques" if params["displayInScreen"] else None]
            ),
            html.Br(),
            html.H2("Cartographie"),
            html.Div([
                        "Niveau de détail",
                        dcc.Dropdown(
                            id="cb-map-settings",
                            options=["Region","Departement","Commune"],
                            value=params["mapDetail"]
                        ,style={"width":"180px","margin":"0 auto"}),
                    ]),
            html.Br(),
            html.Span(id="div-save-settings",children="Sauvegarder",style={"border":"solid 1px"})
        ]
        return [appSettings]+parameter,"active","","","",True,True,True,""
    
@app.callback(
    Output("div-success","children",allow_duplicate=True),

    Input("div-save-settings","n_clicks"),
    State("chk-list-filtrage","value"),
    State("chk-list-viz","value"),
    State("cb-map-settings","value"),
    prevent_initial_call=True      
)
def saveSettings(n_clicks,filtrageChecked,vizChecked,mapDetail):
    if n_clicks is not None:
        paramstoSave = {
                            "multi" : "Filtres multi-selection" in filtrageChecked,
                            "filterCb" : "Filtres intelligents" in filtrageChecked,
                            "displayInScreen" : "Ordonner les graphiques" in vizChecked,
                            "mapDetail" : mapDetail
                        }
        with open("assets/settings/saved_settings.json", "w") as f:
            json.dump(paramstoSave, f)
        return "Paramètres sauvegardés avec Succès !"


