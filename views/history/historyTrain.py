import dash_html_components as html


historyTrain=html.Div([html.H1("Historique des données insérées"),html.Span("Historique > Historique des données insérées",className="breadcrumb"),html.Br(),html.Div(id="div-details",style={"float":"right","width":"600px","height":"600px","overflow":"auto"})])