import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


dropdown_axis_x_options = {'gdp_per_capita': 'GDP per Capita',
                           'gdp_volume': 'GDP Volume',
                           'hdi': 'HDI',
                           'ECI': 'ECI',
                           'country_population_2018': 'Country Population 2018'}

dropdown_axis_y_options = {'gdp_per_capita': 'GDP per Capita',
                           'gdp_volume': 'GDP Volume',
                           'hdi': 'HDI',
                           'ECI': 'ECI',
                           'country_population_2018': 'Country Population 2018',
                           'count': 'Count',
                           'relative_1M_count': 'Relative per 1M count'}


def linear_regression(df, x_col, y_col):
    data = df[df[x_col].notnull()]
    data = data[data[y_col].notnull()]

    X = data[x_col].values.reshape(-1, 1)
    Y = data[y_col].values.reshape(-1, 1)

    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    y_pred_train = linear_regressor.predict(X)

    fig = go.Figure()

    x_plot_train = X.flatten().tolist()
    y_plot_train = Y.flatten().tolist()
    y_pred_plot_train = y_pred_train.flatten().tolist()

    fig.add_trace(go.Scatter(x=x_plot_train, y=y_plot_train, mode='markers', name='Data',
                  marker=dict(
                      size=5,
                      color=y_plot_train,  # set color equal to a variable
                      colorscale='Viridis',  # one of plotly colorscales
                      showscale=True
                  )))
    fig.add_trace(go.Scatter(x=x_plot_train, y=y_pred_plot_train, mode='lines', name='Linear regression',
                             line=dict(color='black', width=2, dash='dot')))

    fig.update_layout(autosize=False, width=1000, height=350, showlegend=False,
                      template="plotly_white", font=dict(family="Tahoma", size=12, color='black'))

    fig.update_xaxes(title=dropdown_axis_x_options[x_col], showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(title=dropdown_axis_y_options[y_col], showline=True, linewidth=1, linecolor='black',
                     gridcolor='lightgray')

    return fig
