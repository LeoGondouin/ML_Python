import dash_html_components as html
import dash_core_components as dcc
from datetime import date
from controllers.process.ImportController import *
import os

path = "C:/Users/leogo/Documents/Prediction/Python_ML"
os.chdir(path)
cleaned = pd.read_csv("assets/data/cube.csv")

predictionForm=html.Div([html.H1("Prediction"),html.Span("Modèle > Prédire",className="breadcrumb"),html.Br(),
                            html.Div([
                                html.H1("Formulaire de prédiction de valeurs foncières"),
                                html.Label(id="output-error",style={"font-size":"20px","font-weight":"bold","color":"red"}),
                                html.Br(),
                                html.Br(),
                                html.Div([
                                    html.Label("Surface réelle du batiment",style={"font-weight":"bold"}),
                                    dcc.Input(id="txt-surface-bati",placeholder="Saisissez la surface du bâtiment désirée",style={"width":"240px","margin-left":"10px"}),
                                    html.Br(),
                                    html.Label("Surface terrain",style={"font-weight":"bold"}),
                                    dcc.Input(id="txt-surface-terrain", placeholder="Saisissez la surface du terrain désirée",style={"width":"230px","margin-left":"10px","margin-top":"10px"}),
                                    html.Br(),
                                    html.Label("Nombre pieces principales",style={"font-weight":"bold"}),
                                    dcc.Input(id="txt-surface-nb-pieces", placeholder="Saisissez le nombre de pièces principales désirée",style={"width":"300px","margin-left":"10px","margin-top":"10px"}),
                                    html.Br(),
                                    html.Br(),
                                    html.Label("Région",style={"margin-top":"10px","font-weight":"bold"}),
                                    dcc.Dropdown(
                                        id="cb-Region",
                                        options=[{'label': region, 'value': region} for region in sorted(cleaned['nom_region'].unique())],
                                        style={"width":"300px","margin": "0 auto"}
                                    ),
                                    html.Br(),
                                    html.Label("Département",style={"margin-top":"10px","margin-top":"10px","font-weight":"bold"}),
                                    dcc.Dropdown(
                                        id="cb-Department",
                                        style={"width":"300px","margin": "0 auto"}
                                    ),
                                    html.Br(),
                                    html.Label("Commune",style={"font-weight":"bold"}),
                                    dcc.Dropdown(
                                        id="cb-Commune",
                                        style={"width":"300px","margin": "0 auto","margin-bottom":"20px",}
                                    ),
                                    html.Button("Prédire", id="btn-predict",style={"margin-bottom":"20px","width":"300px","height":"30px","font-size":"20px"}),
                                    html.Div(id="output-prediction"),
                                    html.Button(id="btn-save-prediction",children="Sauvegarder",style={"width":"130px","height":"30px","font-size":"20px","margin-top":"10px","display":"none"})
                                ]),
                            ],style={'width': '600px', 'margin': '0 auto', 'padding': '20px', 'border': '1px solid #ccc', 'border-radius': '5px', 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)'}),
                        ])