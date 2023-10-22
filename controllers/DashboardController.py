from views.visualization.dashboard import dashboard
from views.visualization.map import map
from dash import Input, Output, State
from dash import dcc
from dash import html
from server import app
import plotly.express as px
import numpy as np
from controllers.process.ImportController import *
import os 
import json
import plotly.graph_objs as go
import geopandas as gpd

#region Import
path = "C:/Users/leogo/Documents/Prediction/Python_ML"
os.chdir(path)
cleaned = pd.read_csv("assets/data/cube.csv")
#endregion
#region Menu
@app.callback(
    Output("menu-dashboard", "className",allow_duplicate=True),
    Output("submenus-visualization", "hidden",allow_duplicate=True),
    Output("sub-menu-dashboard", "className",allow_duplicate=True),
    Output("sub-menu-map", "className",allow_duplicate=True),

    Output("menu-prediction", "className",allow_duplicate=True),
    Output("menu-history", "className",allow_duplicate=True),
    Output("menu-parameters", "className",allow_duplicate=True),

    Output("submenus-prediction", "hidden",allow_duplicate=True), 
    Output("submenus-history", "hidden",allow_duplicate=True),
    Output("homepage", "className",allow_duplicate=True),
    
    Input("menu-dashboard", "n_clicks"),
    State("submenus-visualization", "hidden"),

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
#endregion
#region Map
def getVentes(data):
    return data[data["Nature mutation"].str.startswith("Vente")]

def getScatterGeo(data):
    if params["mapDetail"]=="Region":
        mean_values = data.groupby('nom_region')[['latitude', 'longitude']].transform('mean')
        data['mean_latitude'] = mean_values['latitude']
        data['mean_longitude'] = mean_values['longitude']
        data = pd.DataFrame(data.groupby(['nom_region','mean_latitude','mean_longitude'])["Valeur fonciere"].mean().reset_index())
        data.columns = ["Region","Latitude","Longitude","Valeur fonciere"]
        data['text'] = 'Region : ' + data['Region'] + '<br>' + 'Valeur foncière : ' + data['Valeur fonciere'].astype(str) + '€'
        bubbleSize = 50
    if params["mapDetail"]=="Departement":
        mean_values = data.groupby('nom_departement')[['latitude', 'longitude']].transform('mean')
        data['mean_latitude'] = mean_values['latitude']
        data['mean_longitude'] = mean_values['longitude']
        data = pd.DataFrame(data.groupby(['nom_departement','mean_latitude','mean_longitude'])["Valeur fonciere"].mean().reset_index())
        data.columns = ["Departement","Latitude","Longitude","Valeur fonciere"]
        data['text'] = 'Departement : ' + data['Departement'] + '<br>' + 'Valeur foncière : ' + data['Valeur fonciere'].astype(str) + '€'
        bubbleSize = 25
    if params["mapDetail"]=="Commune":
        mean_values = data.groupby('Commune')[['latitude', 'longitude']].transform('mean')
        data['mean_latitude'] = mean_values['latitude']
        data['mean_longitude'] = mean_values['longitude']
        data = pd.DataFrame(data.groupby(['Commune','mean_latitude','mean_longitude'])["Valeur fonciere"].mean().reset_index())
        data.columns = ["Commune","Latitude","Longitude","Valeur fonciere"]
        data['text'] = 'Commune : ' + data['Commune'] + '<br>' + 'Valeur foncière : ' + data['Valeur fonciere'].astype(str) + '€'
        bubbleSize = 10
    fig = px.scatter_geo(data_frame=data, lat='Latitude', lon='Longitude',hover_data="text",hover_name=None,
                    color='Valeur fonciere',  # Utilisez la valeur foncière pour la couleur des points
                    color_continuous_scale='plasma',  # Palette de couleur
                    custom_data=[params["mapDetail"], 'Valeur fonciere'])
    # Spécifier les limites de la carte pour centrer sur la France
    fig.update_geos(lonaxis_range=[-5.142, 9.662], lataxis_range=[41.303, 51.124], bgcolor='lightblue')
    

    # Personnaliser le texte affiché au survol du point
    fig.update_traces(textposition='top center',marker=dict(size=bubbleSize))

    fig.update_layout(
        title='Ventes Immobilières en France par '+params["mapDetail"],
        coloraxis_colorbar=dict(title='Valeur Foncière'),
        geo=dict(
            lonaxis_range=[-5.142, 9.662],
            lataxis_range=[41.303, 51.124],
            showland=True,
            landcolor='forestgreen',  #ici meilleur couleur
            showcountries=True,
            countrycolor='White'
        )
    )
    return fig

@app.callback(
    Output("screen-menu", "children",allow_duplicate=True),
    Output("sub-menu-map", "className",allow_duplicate=True),
    Output("sub-menu-dashboard", "className",allow_duplicate=True),

    Input("sub-menu-map", "n_clicks"),
    prevent_initial_call=True   
)
def displayMap(n_clicks):
    if n_clicks is not None and n_clicks>0:
        global params
        with open("assets/settings/saved_settings.json")as f:
            params = json.load(f) 
        cleaned_copy = cleaned.copy()
        Q1 = cleaned_copy['Valeur fonciere'].quantile(0.25)
        Q3 = cleaned_copy['Valeur fonciere'].quantile(0.75)

        IQR = Q3 - Q1
        cleaned_copy = cleaned_copy[(cleaned_copy['Valeur fonciere'] < Q3 + (1.5 * IQR)) & (cleaned_copy['Valeur fonciere'] > Q1 - (1.5 * IQR))]
        cleaned_copy = getVentes(cleaned_copy)
        libMonthOrdered = pd.DataFrame(data={"libMois":cleaned_copy["Lib mois"].unique(),"Mois":cleaned_copy["Mois"].unique()}).sort_values(by="Mois")
        uniqueLocal = np.sort(cleaned_copy[cleaned_copy["Type local"].notnull()]["Type local"].unique())
        uniqueNbLots = np.sort(cleaned_copy[cleaned_copy["Nombre de lots"].notnull()]["Nombre de lots"].unique())
        uniqueCatSurf = np.sort(cleaned_copy[cleaned_copy["Catégorie Surface terrain"].notnull()]["Catégorie Surface terrain"].unique())
        uniqueNbPieces = np.sort(cleaned_copy[cleaned_copy["Nombre pieces principales"].notnull()]["Nombre pieces principales"].unique())
        uniqueYears = np.sort(cleaned_copy[cleaned_copy["Année"].notnull()]["Année"].unique())
        uniqueMonths = libMonthOrdered["libMois"]
        uniqueDays = np.sort(cleaned_copy[cleaned_copy["Jour"].notnull()]["Jour"].unique())
        filters = html.Div([
            dcc.Dropdown(
                id="cb-type-local",
                options=[{'label': local, 'value': local} for local in uniqueLocal],
                placeholder="Type de local",
                multi=params["multi"],
                className="filters",
                style={"padding-left":"3%"}
            ),
            dcc.Dropdown(
                id="cb-nb-lots",
                options=[{'label': nbLot, 'value': nbLot} for nbLot in uniqueNbLots],
                placeholder="Nombre de lots",
                multi=params["multi"],
                className="filters",
            ),
            dcc.Dropdown(
                id="cb-cat-surfaces",
                options=[{'label': cat, 'value': cat} for cat in uniqueCatSurf],
                placeholder="Catégorie de surface",    
                multi=params["multi"]  ,
                className="filters"       
            ),
            dcc.Dropdown(
                id="cb-nb-pieces",
                options=[{'label': nbPieces, 'value': nbPieces} for nbPieces in uniqueNbPieces],
                placeholder="Nombre de pièces",
                multi=params["multi"],
                className="filters"
            ),
            dcc.Dropdown(
                id="cb-years",
                options=[{'label': year, 'value': year} for year in uniqueYears],
                placeholder="Année",
                multi=params["multi"],
                className="filters"
            ),
            dcc.Dropdown(
                id="cb-months",
                options=[{'label': month, 'value': month} for month in uniqueMonths],
                placeholder="Mois",
                multi=params["multi"],
                className="filters"
            ),
            dcc.Dropdown(
                id="cb-days",
                options=[{'label': day, 'value': day} for day in uniqueDays],
                placeholder="Jour",
                multi=params["multi"],
                className="filters"
            ),
            html.Br(),
        ],className="filters-container")
        btnFilter = html.Button(id="btn-filter-map",children="Filtrer",style={"top":"150px","position":"absolute"})
        btnClear = html.Button(id="btn-clear-map-filters",children="Effacer",style={"top":"150px","margin-left":"60px","position":"absolute"})
        franceMap = [filters,btnFilter,btnClear,dcc.Graph(id="france-map",figure=getScatterGeo(cleaned_copy),style={"height":"550px"})]

        return [map]+franceMap,"active",""
#endregion
#region Dashboard
@app.callback(
    Output("screen-menu", "children",allow_duplicate=True),
    Output("sub-menu-dashboard", "className",allow_duplicate=True),
    Output("sub-menu-map", "className",allow_duplicate=True),
    Input("sub-menu-dashboard", "n_clicks"),
    prevent_initial_call=True   
)



def loadDashboard(n_clicks):
    if n_clicks is not None and n_clicks>0:
        global params
        with open("assets/settings/saved_settings.json")as f:
            params = json.load(f) 
        ventes = getVentes(cleaned)
        libMonthOrdered = pd.DataFrame(data={"libMois":ventes["Lib mois"].unique(),"Mois":ventes["Mois"].unique()}).sort_values(by="Mois")
        uniqueLocal = np.sort(ventes[ventes["Type local"].notnull()]["Type local"].unique())
        uniqueNbLots = np.sort(ventes[ventes["Nombre de lots"].notnull()]["Nombre de lots"].unique())
        uniqueCatSurf = np.sort(ventes[ventes["Catégorie Surface terrain"].notnull()]["Catégorie Surface terrain"].unique())
        uniqueNbPieces = np.sort(ventes[ventes["Nombre pieces principales"].notnull()]["Nombre pieces principales"].unique())
        uniqueYears = np.sort(ventes[ventes["Année"].notnull()]["Année"].unique())
        uniqueMonths = libMonthOrdered["libMois"]
        uniqueDays = np.sort(ventes[ventes["Jour"].notnull()]["Jour"].unique())
        
        if params["displayInScreen"]:
            graphs = html.Div([html.Div(
                children=[
                    dcc.Graph(
                        id="pie-logement",
                        figure=generate_PieLogement(getVentes(cleaned)),
                        className="graphs",
                    ),
                    dcc.Graph(
                        id="pie-surface",
                        figure=generate_BarSurface(getVentes(cleaned)),
                        className="graphs"
                    )
                ],
                style={"display":"flex"}
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="bar-rooms",
                        figure=generate_BarNbPiece(getVentes(cleaned)),
                        className="graphs"
                    ),
                    html.Button(id="btn-drill-up",children="Roll up",style={"display":"none"}),
                    dcc.Graph(
                        id="bar-sales-by-temp",
                        figure=generate_BarSalesByYear(getVentes(cleaned)),
                        className="graphs"
                    )
                ],
                style={"display":"flex"}
            )
            ])
        else:
            graphs = html.Div(
                children=[
                    dcc.Graph(
                        id="pie-logement",
                        figure=generate_PieLogement(getVentes(cleaned)),
                    ),
                    dcc.Graph(
                        id="pie-surface",
                        figure=generate_BarSurface(getVentes(cleaned)),
                    ),
                    dcc.Graph(
                        id="bar-rooms",
                        figure=generate_BarNbPiece(getVentes(cleaned)),
                    ),
                    html.Button(id="btn-drill-up",children="Roll up",style={"display":"none"}),
                    dcc.Graph(
                        id="bar-sales-by-temp",
                        figure=generate_BarSalesByYear(getVentes(cleaned)),
                    )
                ],
            )
        dashboard_components = [
            html.Div([
                dcc.Dropdown(
                    id="cb-type-local",
                    options=[{'label': local, 'value': local} for local in uniqueLocal],
                    placeholder="Type de local",
                    multi=params["multi"],
                    className="filters",
                    style={"padding-left":"3%"}
                ),
                dcc.Dropdown(
                    id="cb-nb-lots",
                    options=[{'label': nbLot, 'value': nbLot} for nbLot in uniqueNbLots],
                    placeholder="Nombre de lots",
                    multi=params["multi"],
                    className="filters",
                ),
                dcc.Dropdown(
                    id="cb-cat-surfaces",
                    options=[{'label': cat, 'value': cat} for cat in uniqueCatSurf],
                    placeholder="Catégorie de surface",    
                    multi=params["multi"]  ,
                    className="filters"       
                ),
                dcc.Dropdown(
                    id="cb-nb-pieces",
                    options=[{'label': nbPieces, 'value': nbPieces} for nbPieces in uniqueNbPieces],
                    placeholder="Nombre de pièces",
                    multi=params["multi"],
                    className="filters"
                ),
                dcc.Dropdown(
                    id="cb-years",
                    options=[{'label': year, 'value': year} for year in uniqueYears],
                    placeholder="Année",
                    multi=params["multi"],
                    className="filters"
                ),
                dcc.Dropdown(
                    id="cb-months",
                    options=[{'label': month, 'value': month} for month in uniqueMonths],
                    placeholder="Mois",
                    multi=params["multi"],
                    className="filters"
                ),
                dcc.Dropdown(
                    id="cb-days",
                    options=[{'label': day, 'value': day} for day in uniqueDays],
                    placeholder="Jour",
                    multi=params["multi"],
                    className="filters"
                ),
                html.Br(),
            ],className="filters-container"),
            html.Button(id="btn-filter",children="Filtrer",style={"top":"150px","position":"absolute"}),
            html.Button(id="btn-clear-filters",children="Effacer",style={"top":"150px","margin-left":"60px","position":"absolute"}),
            graphs
        ]
        return [dashboard]+dashboard_components,"active",""

def generate_PieLogement(ventes):
    ventes_copy = ventes[ventes["Type local"].notna()]
    return px.pie(ventes_copy, names='Type local', color_discrete_sequence=px.colors.sequential.RdBu)

def generate_BarSurface(ventes):
    count_data = ventes['Catégorie Surface terrain'].value_counts().reset_index()
    count_data.columns = ['Catégorie Surface terrain', 'Nombre de ventes']
    return px.bar(count_data, x='Catégorie Surface terrain',y='Nombre de ventes',color_discrete_sequence=px.colors.sequential.RdBu,category_orders={'Catégorie Surface terrain': ["Petite","Moyenne","Grande"]})

def generate_BarNbPiece(ventes):
    count_data = ventes['Nombre pieces principales'].value_counts().reset_index()
    count_data.columns = ['Nombre pieces principales', 'Nombre de ventes']
    return px.bar(count_data, x='Nombre pieces principales', y='Nombre de ventes', color_discrete_sequence=px.colors.sequential.RdBu)

def generate_BarSalesByYear(ventes):
    count_data = ventes['Année'].value_counts().reset_index()
    count_data.columns = ['Année', 'Nombre de ventes']
    return px.bar(count_data, x='Année', y='Nombre de ventes', color_discrete_sequence=px.colors.sequential.RdBu,title="Ventes par Année")

level = 1
drilledMonth= ""
drilledYear= ""

@app.callback(
    Output("bar-sales-by-temp", "figure",allow_duplicate=True),
    Output("btn-drill-up", "style",allow_duplicate=True), 

    Input("bar-sales-by-temp", "clickData"),

    State("cb-type-local","value"),
    State("cb-nb-lots","value"),
    State("cb-cat-surfaces","value"),
    State("cb-nb-pieces","value"),
    State("cb-years","value"),
    prevent_initial_call=True   
)
def drillDownSalesByYear(value,typeLocal,nbLots,catSurface,nbPiece,year):
    global level
    global drilledMonth
    global drilledYear

    if value is not None:
        clickedElem = value['points'][0]['x']
        ventes = getFilteredData(typeLocal,nbLots,catSurface,nbPiece,year,None,None)
        if level==1:
            level=2
            drilledYear = clickedElem
            drilled = drillDownMonths(ventes,clickedElem)
        elif level==2:
            level=3
            drilledMonth = clickedElem
            drilled = drillDownDays(ventes,clickedElem)
        else:
            drilled = drillDownDays(ventes,drilledMonth)
        return drilled,{"display":"block"}
    
def drillDownMonths(ventes,year):
    ventes = ventes[ventes["Année"]==year]
    count_data = ventes['Lib mois'].value_counts().reset_index()
    count_data.columns = ['Lib mois', 'Nombre de ventes']
    return px.bar(count_data, x='Lib mois', y='Nombre de ventes', color_discrete_sequence=px.colors.sequential.RdBu,title=f"Ventes par Mois pour l'année {drilledYear}",category_orders={'Lib mois': ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]})

def drillDownDays(ventes,month):
    ventes = ventes[(ventes["Année"]==drilledYear) & (ventes["Lib mois"]==month)]
    count_data = ventes['Jour'].value_counts().reset_index()
    count_data.columns = ['Jour', 'Nombre de ventes']
    return px.bar(count_data, x='Jour', y='Nombre de ventes', color_discrete_sequence=px.colors.sequential.RdBu,title=f"Ventes par Jour pour le mois {drilledMonth} de l'année {drilledYear}")

@app.callback(
    Output("bar-sales-by-temp", "figure",allow_duplicate=True),
    Output("btn-drill-up", "style",allow_duplicate=True), 

    Input("btn-drill-up", "n_clicks"),
    State("cb-type-local","value"),
    State("cb-nb-lots","value"),
    State("cb-cat-surfaces","value"),
    State("cb-nb-pieces","value"),
    State("cb-years","value"),
    prevent_initial_call=True   
)
def drillUpSalesByYear(n_clicks,typeLocal,nbLots,catSurface,nbPiece,cbYear):
    if n_clicks is not None:
        global level
        global drilledYear
        style={"display":"none"}
        if level==3:
            level=2
            drilled = drillUpMonth(drilledYear,typeLocal,nbLots,catSurface,nbPiece)
            style={"display":"block"}
        elif level==2:
            level=1
            drilled = drillUpYear(typeLocal,nbLots,catSurface,nbPiece,cbYear)
        else:
            drilled = drillUpYear(typeLocal,nbLots,catSurface,nbPiece,cbYear)
        print(level)
        return drilled,style

def drillUpMonth(year,typeLocal,nbLots,catSurface,nbPiece):
    return drillDownMonths(getFilteredData(typeLocal,nbLots,catSurface,nbPiece,year,None,None),year)

def drillUpYear(typeLocal,nbLots,catSurface,nbPiece,year):
    return generate_BarSalesByYear(getFilteredData(typeLocal,nbLots,catSurface,nbPiece,year,None,None))

@app.callback(
    Output("pie-logement","figure",allow_duplicate=True),
    Output("pie-surface","figure",allow_duplicate=True),
    Output("bar-rooms","figure",allow_duplicate=True),
    Output("bar-sales-by-temp","figure",allow_duplicate=True),
    Output("btn-drill-up", "style",allow_duplicate=True), 

    Input("btn-filter","n_clicks"),
    State("cb-type-local","value"),
    State("cb-nb-lots","value"),
    State("cb-cat-surfaces","value"),
    State("cb-nb-pieces","value"),
    State("cb-years","value"),
    # State("cb-months","value"),
    # State("cb-days","value"),

    prevent_initial_call=True   
)
def filter(n_clicks,typeLocal,nbLots,catSurface,nbPieces,year):
    global level
    global drilledYear
    global drilledMonth
    if n_clicks is not None:
        level=1
        drilledYear=""
        drilledMonth=""
        ventes = getFilteredData(typeLocal,nbLots,catSurface,nbPieces,year,None,None)
        return generate_PieLogement(ventes),generate_BarSurface(ventes),generate_BarNbPiece(ventes),generate_BarSalesByYear(ventes),{"display":"none"}
    
def getFilteredData(type_local,nb_lots,cat_surface,nb_pieces,annee,mois,jour):
    ventes = getVentes(cleaned)
    if(type_local is not None):
        ventes = ventes[ventes["Type local"].isin(type_local)] if(params["multi"]) else  ventes[ventes["Type local"]==type_local]
    if(nb_lots is not None):
        ventes = ventes[ventes["Nombre de lots"].isin(nb_lots)] if(params["multi"]) else  ventes[ventes["Nombre de lots"].isin([nb_lots])]
    if(cat_surface is not None):
        ventes = ventes[ventes["Catégorie Surface terrain"].isin(cat_surface)] if(params["multi"]) else ventes[ventes["Catégorie Surface terrain"] == cat_surface]     
    if(nb_pieces is not None):
        ventes = ventes[ventes["Nombre pieces principales"].isin(nb_pieces)] if(params["multi"]) else ventes[ventes["Nombre pieces principales"] == nb_pieces]     
    if(annee is not None):
        ventes = ventes[ventes["Année"].isin([annee])] if(params["multi"]) else ventes[ventes["Année"] == annee]     
    if(mois is not None):
        ventes = ventes[ventes["Lib mois"].isin(mois)] if(params["multi"]) else ventes[ventes["Lib mois"] == mois]     
    if(jour is not None):
        ventes = ventes[ventes["Jour"].isin(jour)] if(params["multi"]) else ventes[ventes["Jour"] == jour] 
    return ventes

@app.callback(
    Output("france-map","figure",allow_duplicate=True),

    Input("btn-filter-map","n_clicks"),
    State("cb-type-local","value"),
    State("cb-nb-lots","value"),
    State("cb-cat-surfaces","value"),
    State("cb-nb-pieces","value"),
    State("cb-years","value"),
    # State("cb-months","value"),
    # State("cb-days","value"),

    prevent_initial_call=True   
)

def filterMap(n_clicks,typeLocal,nbLots,catSurface,nbPieces,year):
    if n_clicks is not None:
        ventes = getFilteredData(typeLocal,nbLots,catSurface,nbPieces,year,None,None)
        return getScatterGeo(ventes)
@app.callback(
    Output("pie-logement","figure",allow_duplicate=True),
    Output("pie-surface","figure",allow_duplicate=True),
    Output("bar-rooms","figure",allow_duplicate=True),
    Output("bar-sales-by-temp","figure",allow_duplicate=True),
    Output("cb-type-local","value",allow_duplicate=True),
    Output("cb-nb-lots","value",allow_duplicate=True),
    Output("cb-cat-surfaces","value",allow_duplicate=True),
    Output("cb-nb-pieces","value",allow_duplicate=True),
    Output("cb-years","value",allow_duplicate=True),
    Output("cb-months","value",allow_duplicate=True),
    Output("cb-days","value",allow_duplicate=True),
    Output("btn-drill-up", "style",allow_duplicate=True), 
    Input("btn-clear-filters","n_clicks"),

    # State("cb-months","value"),
    # State("cb-days","value"),

    prevent_initial_call=True   
)  
def clearFilters(n_clicks):
    global level
    global drilledYear
    global drilledMonth
    if n_clicks is not None:
        level=1
        drilledYear=""
        drilledMonth=""
        ventes = getFilteredData(None,None,None,None,None,None,None)
        return generate_PieLogement(ventes),generate_BarSurface(ventes),generate_BarNbPiece(ventes),generate_BarSalesByYear(ventes),None,None,None,None,None,None,None,{"display":"none"}
@app.callback(
    Output("cb-type-local","value"),
    Output("cb-nb-lots","value"),
    Output("cb-cat-surfaces","value"),
    Output("cb-nb-pieces","value"),
    Output("cb-years","value"),
    Output("cb-months","value"),
    Output("cb-days","value"),
    Output("france-map","figure",allow_duplicate=True),
    Input("btn-clear-map-filters","n_clicks"),

    # State("cb-months","value"),
    # State("cb-days","value"),

    prevent_initial_call=True   
)
def clearMapFilters(n_clicks):
    if n_clicks is not None:
        cleaned_copy = cleaned.copy()
        Q1 = cleaned_copy['Valeur fonciere'].quantile(0.25)
        Q3 = cleaned_copy['Valeur fonciere'].quantile(0.75)

        IQR = Q3 - Q1
        cleaned_copy = cleaned_copy[(cleaned_copy['Valeur fonciere'] < Q3 + (1.5 * IQR)) & (cleaned_copy['Valeur fonciere'] > Q1 - (1.5 * IQR))]
        cleaned_copy = getVentes(cleaned_copy)
        return None,None,None,None,None,None,None,getScatterGeo(getVentes(cleaned_copy))

@app.callback(
    Output("cb-nb-lots","options",allow_duplicate=True),
    Output("cb-cat-surfaces","options",allow_duplicate=True),
    Output("cb-nb-pieces","options",allow_duplicate=True),
    Output("cb-years","options",allow_duplicate=True),
    Output("cb-months","options",allow_duplicate=True),
    Output("cb-days","options",allow_duplicate=True),

    Input("cb-type-local","value"),
    State("cb-cat-surfaces","options"),
    State("cb-nb-pieces","options"),
    State("cb-years","options"),
    State("cb-months","options"),
    State("cb-days","options"),
    prevent_initial_call=True   
)

def filteredcbLotOpt(typeLocal,selectedCatSurface,selectedNbPieces,selectedYear,selectedMonth,selectedDay):
    if params["filterCb"]:
        ventes = getFilteredData(typeLocal,None,None,None,None,None,None)
        uniqueNbLots = np.sort(ventes[ventes["Nombre de lots"].notnull()]["Nombre de lots"].unique())
        tuple = uniqueNbLots,[],[],[],[],[]
    else:
        tuple = np.sort(getVentes(cleaned)["Nombre de lots"].unique()),selectedCatSurface,selectedNbPieces,selectedYear,selectedMonth,selectedDay
    return tuple

@app.callback(
    Output("cb-cat-surfaces","options",allow_duplicate=True),
    Output("cb-nb-pieces","options",allow_duplicate=True),
    Output("cb-years","options",allow_duplicate=True),
    Output("cb-months","options",allow_duplicate=True),
    Output("cb-days","options",allow_duplicate=True),

    Input("cb-nb-lots","value"),  
    State("cb-type-local","value"),
    State("cb-nb-pieces","options"),
    State("cb-years","options"),
    State("cb-months","options"),
    State("cb-days","options"),
    prevent_initial_call=True   
)
def filteredcbCatSurfOpt(nbLots,typeLocal,nbPieces,annee,mois,jour):
    if params["filterCb"]:
        ventes = getFilteredData(typeLocal,nbLots,None,None,None,None,None)
        uniqueCatSurf = np.sort(ventes[ventes["Catégorie Surface terrain"].notnull()]["Catégorie Surface terrain"].unique())
        tuple=uniqueCatSurf,[],[],[],[]
    else:
        tuple = np.sort(getVentes(cleaned)["Catégorie Surface terrain"].unique()),nbPieces,annee,mois,jour
    return tuple

@app.callback(
    Output("cb-nb-pieces","options",allow_duplicate=True),
    Output("cb-years","options",allow_duplicate=True),
    Output("cb-months","options",allow_duplicate=True),
    Output("cb-days","options",allow_duplicate=True),

    Input("cb-cat-surfaces","value"), 
    State("cb-nb-lots","value"), 
    State("cb-type-local","value"),
    State("cb-years","options"),
    State("cb-months","options"),
    State("cb-days","options"),
    prevent_initial_call=True   
)
def filteredcbNbPieces(catSurf,nbLots,typeLocal,annee,mois,jour):
    if params["filterCb"]:
        ventes = getFilteredData(typeLocal,nbLots,catSurf,None,None,None,None)
        uniqueNbPieces = np.sort(ventes[ventes["Nombre pieces principales"].notnull()]["Nombre pieces principales"].unique())
        tuple = uniqueNbPieces,[],[],[]
    else:
        tuple=np.sort(getVentes(cleaned)["Nombre pieces principales"].unique()),annee,mois,jour
    return tuple

@app.callback(
    Output("cb-years","options",allow_duplicate=True),
    Output("cb-months","options",allow_duplicate=True),
    Output("cb-days","options",allow_duplicate=True),

    Input("cb-nb-pieces","value"), 
    State("cb-cat-surfaces","value"), 
    State("cb-nb-lots","value"), 
    State("cb-type-local","value"),
    prevent_initial_call=True   
)
def filteredcbAnnee(nbPieces,catSurf,nbLots,typeLocal):
    if params["filterCb"]:
        ventes = getFilteredData(typeLocal,nbLots,catSurf,nbPieces,None,None,None)
        uniqueYear = np.sort(ventes[ventes["Année"].notnull()]["Année"].unique())
        tuple = uniqueYear,[],[]
    else:
        tuple = np.sort(getVentes(cleaned)["Année"].unique()),[],[]
    return tuple

@app.callback(
    Output("cb-months","options",allow_duplicate=True),
    Output("cb-days","options",allow_duplicate=True),

    Input("cb-years","value"), 
    State("cb-nb-pieces","value"), 
    State("cb-cat-surfaces","value"), 
    State("cb-nb-lots","value"), 
    State("cb-type-local","value"),
    prevent_initial_call=True   
)
def filteredcbMois(year,nbPieces,catSurf,nbLots,typeLocal):
    if params["filterCb"]:
        ventes = getFilteredData(typeLocal,nbLots,catSurf,nbPieces,year,None,None)
        uniqueMonth = np.sort(ventes[ventes["Lib mois"].notnull()]["Lib mois"].unique())
        tuple = uniqueMonth,[]
    else:
        ventes = getVentes(cleaned)
        libMonthOrdered = pd.DataFrame(data={"libMois":ventes["Lib mois"].unique(),"Mois":ventes["Mois"].unique()}).sort_values(by="Mois")

        tuple=libMonthOrdered["libMois"],[]
    return tuple    
@app.callback(
    Output("cb-days","options",allow_duplicate=True),

    Input("cb-months","value"),
    State("cb-years","value"), 
    State("cb-nb-pieces","value"), 
    State("cb-cat-surfaces","value"), 
    State("cb-nb-lots","value"), 
    State("cb-type-local","value"),
    prevent_initial_call=True   
)
def filteredcbMois(months,year,nbPieces,catSurf,nbLots,typeLocal):
    if params["filterCb"]:
        ventes = getFilteredData(typeLocal,nbLots,catSurf,nbPieces,year,months,None)
    else:
        ventes = getFilteredData(None,None,None,None,None,months,None)

    uniqueDay = np.sort(ventes[ventes["Jour"].notnull()]["Jour"].unique())
    return uniqueDay


# def filteredcbNbPiece(nbLots,typeLocal,catSurf):
#     ventes = getFilteredData(typeLocal,nbLots,catSurf,nbPieces,None,None,None)
#     uniqueNbPieces = np.sort(ventes[ventes["Année"].notnull()]["Année"].unique())
#     return uniqueNbPieces
#endregion