from django.shortcuts import render
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
from plotly.offline import plot
import plotly.graph_objects as go


# Create your views here.
def home(request):
    # Plot-1
    df = pd.read_csv('datasets/matches.csv')
    new_df = df[['season']]
    year_counts = new_df['season'].value_counts()
    final_df = pd.DataFrame({'Year': year_counts.index, 'Matches Played': year_counts.values})
    final_df = final_df.sort_values(by=['Year'],ascending=True)

    fig1 = go.Figure([go.Bar(x=final_df['Year'], y=final_df['Matches Played'])])
    fig1.update_layout(title='Number of Matches Played per Year in IPL',
                    xaxis_title='Year',
                    yaxis_title='Matches Played')
    
    fianl_plot1 = plot(fig1, output_type="div")
    
    
    
    # Plot-2
    df['winner'] = pd.Categorical(df['winner'])
    teams = df['winner'].unique()
    teams = teams.dropna()
    teams = list(teams)
    teams.sort()
    team_wins_by_year = df.groupby(['season', 'winner']).agg(matches_won=('winner', 'count')).reset_index()
    team_wins_by_year = team_wins_by_year.sort_values(by=['season'],ascending=True)

    fig2 = go.Figure()
    for team in teams:
        fig2.add_trace(go.Bar(x=team_wins_by_year.loc[team_wins_by_year['winner'] == team]['season'],
                                y=team_wins_by_year.loc[team_wins_by_year['winner'] == team]['matches_won'],
                                name=team))
    fig2.update_layout(title='Matches Won by Team in IPL',
                    xaxis_title='Year',
                    yaxis_title='Matches Won',
                    barmode='stack')

    fianl_plot2 = plot(fig2, output_type="div")

    data = {
        "css_file" : "home",
        "plot_div1" : fianl_plot1,
        "plot_div2" : fianl_plot2,
    }
    
    return render(request, 'index.html', data)


