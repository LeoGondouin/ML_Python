import dash_html_components as html
import dash_core_components as dcc

sidebar = html.Div(
                    [
                        html.Div(
                        [
                            html.H1("Menu",style={"text-decoration":"underline"}),
                            html.H2(id="homepage",children = ["Accueil"],style={"cursor":"pointer"},className="active"),
                            html.H2(id="menu-dashboard",children = ["Visualisation"],style={"cursor":"pointer"}),
                            html.Div(id="submenus-visualization",
                                     children=[
                                        html.H3(id="sub-menu-dashboard",children=["Tableau de bord"],style={"cursor":"pointer"}),
                                        html.H3(id="sub-menu-map",children=["Cartographie"],style={"cursor":"pointer"})
                                    ]
                            ,hidden=True),
                            html.H2(id="menu-prediction",children = ["Modèle"],style={"cursor":"pointer"}
                            ),
                            html.Div(id="submenus-prediction",
                                     children = [
                                        html.H3(id="sub-menu-prediction",children=["Prédire"],style={"cursor":"pointer"}),
                                        html.H3(id="sub-menu-train",children=["Entrainer"],style={"cursor":"pointer"})
                                     ]
                            ,hidden=True),
                            html.H2(id="menu-history",children = ["Historique"],style={"cursor":"pointer"}),
                                                        html.Div(id="submenus-history",
                                                                children=[
                                                                    html.H3(id="sub-menu-history-predict",children=["Historique des prédictions sauvegardées"],style={"cursor":"pointer"}),
                                                                    html.H3(id="sub-menu-history-train",children=["Historique des données insérées"],style={"cursor":"pointer"})
                                                                ]
                                                        ,hidden=True),
                            html.H2(id="menu-parameters",children=["Paramètres"],style={"cursor":"pointer"})
                        ],style={"margin-top": "50%"}
                        )
                    ]
          ,id="sidebar")