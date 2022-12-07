import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash, dcc
import dash
from dash_bootstrap_components._components.Container import Container
import plotly.express as px
import subprocess
import numpy as np

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# Instantiate app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# Create placeholder rule coverage figure
df = px.data.gapminder().query("year == 2007")
fig = px.treemap(df, path=[px.Constant("world"), 'continent', 'country'], values='pop',
                  color='lifeExp', hover_data=['iso_alpha'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)')
fig.update(layout_coloraxis_showscale=False)

# Create styles for tab setup
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# Add navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("rAIMEE", className="ms-2")),
                    ],
                    align="left",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            )
        ],
        fluid=True
    ),
    color="dark",
    dark=True,
)

# introduction tab
introCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Relational AIMEE - A.I Model Explorer and Editor for Relational Datasets", className="card-title"),
                html.P("AIMEE is an interactive tool for exploring and editing machine learning models. \
                    It uses sets of generated rules in order to create a model surrogate, which can then \
                    be edited and compared.", 
                    className="card-text"),
                
                html.H4("Inductive Logic Programming (ILP)", className="card-title"),
                html.P("After inspecting the model logic through decision rules, AIMEE allows users to add \
                    new rules to change the decision boundaries through using a pre-processing algorithm. \
                    This underlying algorithm first selects a base population from the original dataset \
                    based on the user-provided rules. It then generates instances using this base population\
                    through a method similar to the well known oversampling technique, SMOTE (Synthetic \
                    Minority Oversampling Technique). Once the data is pre-processed to reflect new \
                    rules, AIMEE retrains the model using the new dataset, and the users can\
                    inspect the new decision boundaries.", 
                    className="card-text"),
                
                html.H4("Interactive Rule Editing", className="card-title"),
                html.P("After inspecting the model logic through decision rules, AIMEE allows users to add \
                    new rules to change the decision boundaries through using a pre-processing algorithm. \
                    This underlying algorithm first selects a base population from the original dataset \
                    based on the user-provided rules. It then generates instances using this base population\
                    through a method similar to the well known oversampling technique, SMOTE (Synthetic \
                    Minority Oversampling Technique). Once the data is pre-processed to reflect new \
                    rules, AIMEE retrains the model using the new dataset, and the users can\
                    inspect the new decision boundaries.", 
                    className="card-text"),
                
                html.H4("Model Comparison", className="card-title"),
                html.P("After inspecting the model logic through decision rules, AIMEE allows users to add \
                    new rules to change the decision boundaries through using a pre-processing algorithm. \
                    This underlying algorithm first selects a base population from the original dataset \
                    based on the user-provided rules. It then generates instances using this base population\
                    through a method similar to the well known oversampling technique, SMOTE (Synthetic \
                    Minority Oversampling Technique). Once the data is pre-processed to reflect new \
                    rules, AIMEE retrains the model using the new dataset, and the users can\
                    inspect the new decision boundaries.", 
                    className="card-text"),
                
                html.H4("References", className="card-title"),
                html.P(["Alkan, Öznur, Dennis Wei, Massimiliano Matteti, Rahul Nair, Elizabeth M. Daly, \
                        and Diptikalyan Saha. 'FROTE: Feedback Rule-Driven Oversampling for Editing Models.' \
                        arXiv preprint arXiv:2201.01070 (2022).", html.Br(),
                    "Nair, Rahul, Massimiliano Mattetti, Elizabeth Daly, Dennis Wei, Oznur Alkan, and \
                            Yunfeng Zhang. 'What Changed? Interpretable Model Comparison.' IJCAI, 2021.", html.Br(),
                    "Alkan, Öznur, Dennis Wei, Massimiliano Matteti, Rahul Nair, Elizabeth M. Daly, \
                        and Diptikalyan Saha. 'FROTE: Feedback Rule-Driven Oversampling for Editing Models.' \
                        arXiv preprint arXiv:2201.01070 (2022).", html.Br(),
                    "Nair, Rahul, Massimiliano Mattetti, Elizabeth Daly, Dennis Wei, Oznur Alkan, and \
                            Yunfeng Zhang. 'What Changed? Interpretable Model Comparison.' IJCAI, 2021.", html.Br(),
                    "Alkan, Öznur, Dennis Wei, Massimiliano Matteti, Rahul Nair, Elizabeth M. Daly, \
                        and Diptikalyan Saha. 'FROTE: Feedback Rule-Driven Oversampling for Editing Models.' \
                        arXiv preprint arXiv:2201.01070 (2022).", html.Br(),], 
                    className="card-text")
                
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "margin-right":"1rem", "width": "103rem", "height":"45rem"},
)
intro = html.Div([introCard])

# Dataset Overview
dataset_overview = html.Div([
    html.Div([
        html.H3("Select Dataset"),
        html.P("Use the toggle to select a preloaded dataset or upload a file.")
    ]),
])

# Rule extraction tab
hypothesisCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Generated Rules", className="card-title"),
                dbc.Switch(
                    value=True,
                    id='restricted_search',
                    label='Display rules in natural language',
                    input_class_name='bg-success'
                    ),
                html.Div(id = 'hypothesis-box', children = []),
                
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "width": "30rem", "height":"36rem", "overflow-y":"scroll"},
)
induceCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Induce Rules", className="card-title"),
                dbc.Button('Induce', id = 'induce-button', color = "primary", className='me-2', n_clicks=0),
                dcc.Store(id='hypothesis-store', data=[], storage_type='memory'),
                dbc.Button('Reset', id = 'reset-button', color = "secondary", className='me-2', n_clicks=0),
                html.H4("Model Information", className="card-title", style={"margin-top":"1rem"}),
                html.Div(id = 'modelInfo-box', children = [html.P(html.Br())]),
                html.H4("Dataset Information", className="card-title", style={"margin-top":"1rem"}),
                html.Div(id = 'datasetInfo-box', children = [])
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "width": "30rem", "height":"18rem", "overflow-y":"scroll"},
)
ruleCoverageCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Rule Coverage", className="card-title"),
                html.P("Visualization of the induced rule set", className="card-text"),
                html.Div(id = 'ruleCoverageGraph-box', children=[])
            
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"2rem", "margin-right":"2rem", "width": "68rem", "height":"55rem"}
)

induced_rules = html.Div([
    dbc.Row([
        dbc.Col([
            induceCard,
            hypothesisCard
        ]),
        
        dbc.Col([
            ruleCoverageCard
        ])
    
    ])
])

compare_model = html.Div([
                    html.H3("Model Comparison ()")
                ])

# Main app layout
app.layout = html.Div([
    html.Div(navbar),
    html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Introduction', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Dataset Overview', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Induced Rules', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Model Editer', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
    ])

])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return intro
    elif tab == 'tab-2':
        return dataset_overview
    elif tab == 'tab-3':
        return induced_rules
    elif tab == 'tab-4':
        return compare_model

@app.callback(
    dash.dependencies.Output('hypothesis-store', 'data'),
    [dash.dependencies.Input('induce-button', 'n_clicks')])
def induce_onClick(n_clicks):
    
    if not n_clicks:
        return dash.no_update

    result = subprocess.check_output('python inferenceScript.py', shell=True)  
    theory = subprocess.check_output('python hypothesisScript.py', shell=True)
    
    # convert bytes to string
    output = theory.decode()  
    print(output)
    returnable = {'hypothesis':output}
    # return output
    return returnable

@app.callback(
    Output('hypothesis-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_hypothesis(data):
    print(type(data))
    print(data)
    hypothesis_text = data["hypothesis"]
    print(hypothesis_text)

    return html.P(children=[
        f"{hypothesis_text}"
    ])

@app.callback(
    Output('modelInfo-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_modelInfo(data):
    return html.P(
        html.P("Accuracy: 100.00%", className="card-text")
    )

@app.callback(
    Output('datasetInfo-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_datasetInfo(data):

    if data:
        return html.P(
            html.P("Total count: 10 | Label T : 5 (50%) |  Label F : 5 (50%)", 
            className="card-text")
        )

@app.callback(
    Output('ruleCoverageGraph-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_ruleCoverageGraph(data):

    if data:
        return dcc.Graph(figure=fig, style={'width':"65rem", 'height':"45rem"})


if __name__ == '__main__':
    app.run_server(debug=True)