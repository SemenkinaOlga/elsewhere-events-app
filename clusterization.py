import pandas as pd
from sklearn.cluster import KMeans


def clusterization_K_Means_1dim(df, text_col, value_col, n_clusters):
    y = df[text_col].values
    X = df[value_col].values.reshape(-1, 1)

    prediction = KMeans(n_clusters=n_clusters).fit_predict(X)

    data = {'value': X[:, 0],
            'name': y,
            'cluster': prediction,
            'code': df['code']
            }

    df_prediction = pd.DataFrame(data, columns=['value', 'name', 'cluster', 'code'])

    return df_prediction


def add_indexation_by_events_amount_for_clusters(df):
    means = df.groupby('cluster').mean()
    means = means.sort_values(by=['value'])
    indexes = [x for x in range(len(means))]
    means['index'] = indexes
    df = pd.merge(df, means, how='left', on='cluster')
    return df
