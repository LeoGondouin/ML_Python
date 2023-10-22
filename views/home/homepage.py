import dash_html_components as html

# home=html.Div([html.H1("Accueil"),html.Span("Accueil",className="breadcrumb"),
#                html.H2("Introduction"),
#                html.Label(children="Cette application a pour but d'analyser les ventes immobilières et",style={"font-size":"20px"}),
#                html.Br(),
#                html.Label(children=" de prédire les valeurs foncières d'immobilier, il y a plusieurs fonctionnalités :",style={"font-size":"20px"}),
#                html.Br(),
#                html.Label("test",style={"padding-left":"10px","float":"right"})
#             ])

home=html.Div([
            html.H1("Accueil"),
            html.H2("Introduction"),
            html.Label("Le but de cette application est d'avoir une vision globale des ventes et prédiction de l'immobilier en France. Elle contient différents menus :",style={"font-size":"20px"}),
            html.H2("Menu \"Visualisation\""),
            html.Div(
                html.Ul([
                    html.Li("Sous menu \"Tableau de bord\" : Un rapport avec filtre dynamique décrivant les ventes",style={"font-size":"18px",'list-style-position': 'inside',"margin-left":"0"}),
                    html.Li("Sous menu \"Cartographie\" : Une carte de la France avec les répartitions de valeurs foncière à différents niveaux de détails",style={"font-size":"18px",'list-style-position': 'inside',"margin-left":"0"}),
                ])
            ,style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around'}),
            html.H2("Menu \"Modèle\""),
            html.Div(
                html.Ul([
                    html.Li("Sous menu \"Prédire\" : Un formulaire à remplir avec des prédictions de valeur foncière après envoi",style={"font-size":"18px",'list-style-position': 'inside',"margin-left":"0"}),
                    html.Li("Sous menu \"Entrainer\" : Une zone pour transverser des données \" vérifiées\" afin d'améliorer la qualité de prédictions",style={"font-size":"18px",'list-style-position': 'inside',"margin-left":"0"}),
                ])
            ),
            html.H2("Menu \"Historique\""),
            html.Div(
                html.Ul([
                    html.Li("Sous menu \"Historique des prédictions sauvegardées\" afin de tracer vos prédictions antérieures",style={"font-size":"18px",'list-style-position': 'inside',"margin-left":"0"}),
                    html.Li("Sous menu \"Historique des prédictions sauvegardées\" afin de tracer vos transversement de données antérieurs",style={"font-size":"18px",'list-style-type': 'none'}),
                ]),style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around'}
            ),
            html.H2("Menu \"Paramètres\""),
            html.Div(
                html.Ul([
                    html.Li("Configurations à customiser par vos soin afin d'adapter l'application pour une expérience plus agréable",style={"font-size":"18px",'list-style-position': 'inside',"margin-left":"0"}),
                ]),style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around'}
            ),
    ])