from dash import Input, Output
from server import app
from views.home.homepage import home

@app.callback(
    Output("screen-menu", "children",allow_duplicate=True),

    Output("homepage", "className",allow_duplicate=True),
    Output("menu-history", "className",allow_duplicate=True),    
    Output("menu-dashboard", "className",allow_duplicate=True),
    Output("menu-prediction", "className",allow_duplicate=True),
    Output("menu-parameters", "className",allow_duplicate=True),

    Output("submenus-visualization", "hidden",allow_duplicate=True),
    Output("submenus-prediction", "hidden",allow_duplicate=True),
    Output("submenus-history", "hidden",allow_duplicate=True),

    Input("homepage", "n_clicks"),

    prevent_initial_call=True      
)
def display(n_clicks):
    if n_clicks is not None:
        return home,"active","","","","",True,True,True