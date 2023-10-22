import dash_html_components as html,dash_core_components as dcc
import dash_bootstrap_components as dbc
training=html.Div([
            html.H1("Entrainement"),
            html.Span("Modèle > Entrainer",className="breadcrumb"),html.Br(),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Insérez un jeu de données à insérer pour améliorer le modèle',
                    html.Span("Choisir un fichier", style={"margin-left":"20px","border":"solid 1px","font-weight":"bold"})
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=False,
                accept='.txt,.csv,.xlsx'
            ),            
            html.Div(
                [
                    html.Label(id="lbl-separator"),
                    dcc.Input(id="txt-separator",type="text",placeholder="Renseignez un séparateur"),
                    html.Button(id="btn-show-preview",children="Montrer l'aperçu",style={"display":"none"})
                ],
            style={"display":"flex","margin-left":"30%"}
            ),
            html.Label(id="test")
        ,html.Div(id='output-data-upload',style={'margin': '10px'})])