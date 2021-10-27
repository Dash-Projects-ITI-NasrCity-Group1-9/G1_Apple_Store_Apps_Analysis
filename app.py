import pandas as pd 
import dash
import dash_html_components as html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output


# img = base64.b64encode(open('apple2.png', 'rb').read())

df = pd.read_csv('AppleStore.csv')
df_1 = pd.DataFrame(df.prime_genre.value_counts())
df_1.columns = ["Count"]
chart1 = px.bar(df_1, x=df_1.index, y='Count', color = 'Count', color_continuous_scale='ice', title= "Count Apps per genres")


chart2 = px.violin(df, x="user_rating", orientation='h', title= "The apps rating distribution")

agg = df.groupby("prime_genre").agg("user_rating").mean()
df_2 = pd.DataFrame(agg)
df_2.columns = ["Rating"]

chart3 =  px.bar(df_2, x="Rating", y=df_2.index, orientation='h', 
        color="Rating", color_continuous_scale='ice',  title= "Average rating per genre")

df_3 = df.sort_values(["price"], ascending=False)

app = dash.Dash(external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ])
app.layout = html.Div(className='row', children=[
    html.Div(children=[
    html.H1("Apple App Store analysis", className = "six columns", style = {"height": "20%"}),
    html.H4("Top Rated Free Head Soccer", className = "two columns",style = {"text-align" : "center"}),
    html.H4("Top Rated Paid Plants Vs Zombies", className = "two columns",style = {"text-align" : "center"}),
    html.H4("Most downloaded FaceBook", className = "two columns",style = {"text-align" : "center"})
    ]),
    
    dcc.Graph(id="g5", figure=chart1, className = "twelve columns"),
    html.Div(children=[
        dcc.Graph(id="g6", figure = chart2,style={'display': 'inline-block'}),
        dcc.Graph(id="g7", figure = chart3,style={'display': 'inline-block'})
    ], className = "twelve columns")
    ,
    dcc.Dropdown(
                   id='demo-dropdown',
                    options=[ 
                    {'label': str(category), 'value': str(category)}  for category in df['prime_genre'].unique()
                    ],
                    value='Games',
                    placeholder='Choose a genere .....',className = "twelve columns"
                                    ),
    html.Div(children=[
        dcc.Graph(id="g1", style={'display': 'inline-block'}),
        dcc.Graph(id="g2", style={'display': 'inline-block'}),
        
    ],className = "twelve columns"),
    
    dcc.Graph(id="g3", className = "twelve columns")
    
])

@app.callback(
    Output("g3", "figure"), 
    [Input("demo-dropdown", "value")])
def update_bar_chart_1(dropdownvalue):
    mask = df["prime_genre"] == dropdownvalue
    fig = px.bar(df_3[mask].iloc[0:10], x='track_name', y='price', title= "Most expensive apps")
    return fig

@app.callback(
    Output("g1", "figure"), 
    [Input("demo-dropdown", "value")])
def update_bar_chart_2(dropdownvalue):
    ages=df[df.prime_genre==dropdownvalue]
    ages = ages['cont_rating'].value_counts()
    ages = pd.DataFrame(ages)
    ages['Ages'] = ages.index
        
    fig = px.bar(ages, x='cont_rating', y="Ages", orientation='h', title= "App count per age restriction")
    return fig

@app.callback(
    Output("g2", "figure"), 
    [Input("demo-dropdown", "value")])
def update_bar_chart_3(dropdownvalue):
    top_size=df[(df.prime_genre==dropdownvalue)]
    top_size.rename(columns={"track_name":"App Name"},inplace=True)
    top_size.sort_values(by=['size_bytes'],ascending=False,inplace=True)
    top_size = top_size.head(10)
    
    top_size.rename(columns={"size_bytes":"Size MB"},inplace=True)
    fig = px.bar(top_size, x="Size MB", y="App Name", orientation='h', 
        color="Size MB", color_continuous_scale='ice', title= "Biggest Apps in size")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)