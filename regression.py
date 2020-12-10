import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def linear_regression(df, x_col, y_col):
    data = df[df[x_col].notnull()]
    data = data[data[y_col].notnull()]

    X = data[x_col].values.reshape(-1, 1)
    Y = data[y_col].values.reshape(-1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X_train, y_train)
    y_pred = linear_regressor.predict(X_test)
    y_pred_train = linear_regressor.predict(X_train)

    # The coefficients
    # print('Coefficients: \n', linear_regressor.coef_)
    # The mean squared error
    res_mean_squared_error = mean_squared_error(y_test, y_pred)
    # print('Mean squared error: %.2f' % res_mean_squared_error)
    # The coefficient of determination: 1 is perfect prediction
    r2 = r2_score(y_test, y_pred)
    # print('Coefficient of determination: %.2f'  % r2)

    fig = go.Figure()

    x_plot_test = X_test.flatten().tolist()
    y_plot_test = y_test.flatten().tolist()
    y_pred_plot_test = y_pred.flatten().tolist()

    x_plot_train = X_train.flatten().tolist()
    y_plot_train = y_train.flatten().tolist()
    y_pred_plot_train = y_pred_train.flatten().tolist()

    fig = make_subplots(rows=2, cols=1, subplot_titles=("Test", "Train"))

    fig.append_trace(go.Scatter(x=x_plot_test, y=y_plot_test, mode='markers', name='test data',
                                marker=dict(color='#8923a5')), row=1, col=1)
    fig.append_trace(go.Scatter(x=x_plot_test, y=y_pred_plot_test, mode='lines', name='test regression',
                                line=dict(color='#21928c')), row=1, col=1)

    fig.append_trace(go.Scatter(x=x_plot_train, y=y_plot_train, mode='markers', name='train data',
                                marker=dict(color='#3c1c9b')), row=2, col=1)
    fig.append_trace(go.Scatter(x=x_plot_train, y=y_pred_plot_train, mode='lines', name='train regression',
                                line=dict(color='#b0dd2e')), row=2, col=1)

    fig.update_xaxes(title_text=x_col)
    fig.update_yaxes(title_text=y_col)

    return dict(fig=fig, mean_squared_error=res_mean_squared_error, r2_score=r2)
