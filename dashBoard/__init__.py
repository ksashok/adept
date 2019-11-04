# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask.helpers import get_root_path
import dash

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Setting the Secret Key for the SQLite DB
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Initiating the Database
    db.init_app(app)

    # Setting up the Flask Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    ### Dash Start
    #register_dashapps(app)

    # Calling the Function which creates the Dash Pages
    # Multiple Dash Pages can be called from here for each url
    dashapp2(app)
    # dashapp2 = dash.Dash(
    # __name__,
    # server=app,
    # url_base_pathname='/dashapp2/'
    # )

    # dashapp2.layout = html.Div("My Dash app")
    
    ### Dash End

    # Importing the User Model
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


# def register_dashapps(app):
#     from flasklogin.dashapp1.layout import layout
#     from flasklogin.dashapp1.callbacks import register_callbacks

#     # Meta tags for viewport responsiveness
#     meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

#     dashapp1 = dash.Dash(__name__,
#                          server=app,
#                          url_base_pathname='/dashboard/',
#                          assets_folder=get_root_path(__name__) + '/dashboard/assets/',
#                          meta_tags=[meta_viewport])

#     with app.app_context():
#         dashapp1.title = 'Dashapp 1'
#         dashapp1.layout = layout
#         register_callbacks(dashapp1)

#     _protect_dashviews(dashapp1)

# Function which protects the Dash apps from unauthorised access
def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])

# Dash Application which is for the /dashboard page
# The page would have Menu bar containing links to Home Page and Logout
# The page contains Data table which has the data source as a Google Sheet
# The Data table is editable and also contains formulas for calculated fields in callback
def dashapp2(app):
    import pandas as pd
    import dash_table
    import dash
    import dash_html_components as html
    import dash_core_components as dcc
    import dash_bootstrap_components as dbc
    from dash.dependencies import Input, Output, State

    # Importing the CSS Stylesheet 
    external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css', dbc.themes.BOOTSTRAP]
    
    # URL for the Google Sheet data source from where the data should be loaded
    url = 'https://docs.google.com/spreadsheets/d/1wqbzgPm-1mJbYL8Tqfh3AQSV4ytxBQuPJ7pEg4BOy-w/edit#gid=0'
    csv_export_url = url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(csv_export_url)
    
    # Creating the Dash application
    dashapp2 = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dashboard/',
    external_stylesheets=external_stylesheets
    )


    # Setting the layout for the dash
    dashapp2.layout = html.Div(
        className="hero is-primary is-fullheight",
        children = [
            
            # MenuBar 
            html.Div(
                className="hero-head",
                children=[
                        html.Nav(
                className="navbar",
                children=[
                    html.Div(
                        className="container",
                        children=[
                                html.Div(
                                id="navbarMenuHeroA",
                                className="navbar-menu",
                                children=[
                                    html.Div(
                                        className="navbar-end",
                                        children=[
                                            html.A("Home",href="/",className="navbar-item"),
                                            html.A("Logout",href="/logout",className="navbar-item")
                                        ]
                                    )
                        ]

                    )

                        ]
                    )

                ]

        )
                ]
            )

        ,
        # Header Text 
        html.Div(className="container has-text-centered",
                                children=[
                                    html.H1("Dashboard of the Table", className="title")
                                ])
        ,
        # Dash Data Table
        html.Div(
                children=[
                        dash_table.DataTable(
                                id='dashboardTable',
                                columns=[{"name": i, "id": i} for i in df.columns],
                                data=df.to_dict('records'),
                                editable=True,
                                style_cell={
                                'backgroundColor': 'white',
                                'color': 'black',
                                 # all three widths are needed
                                # 'minWidth': '30px', 'width': '30px', 'maxWidth': '90px',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                },

                                style_table={'overflowX': 'scroll'},

                                filter_action="native",
                                sort_action="native",
                                sort_mode="multi",
                                export_format='xlsx',
                                export_headers='display',
                                merge_duplicate_headers=True

                                
                                )

                ])

        

        ]

        )

    # Callback for the Data Table to make reactive cells
    # Update here to add new formulas for the columns
    @dashapp2.callback(
    Output('dashboardTable', 'data'),
    [Input('dashboardTable', 'data_timestamp')],
    [State('dashboardTable', 'data')])
    def update_columns(timestamp, rows):
        for row in rows:
            try:
                # Column CHARGE should be a product of QUANTITY AMOUNT and RATE
                row['CHARGE'] = float(row['QUANTITY AMOUNT']) * float(row['RATE'])

                # Column TOTAL RATE would be a sum of RATE and TAX CHARGE
                row['TOTAL CHARGE'] = float(row['CHARGE']) + float(row['TAX CHARGE'])
            except:
                row['TOTAL CHARGE'] = 'NA'
        return rows

    # Calling the function to protect the Dash page from unauthorised access
    _protect_dashviews(dashapp2)
