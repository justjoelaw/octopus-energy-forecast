import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def create_regression_model(df, energy_type):
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()

    df_dummies = pd.get_dummies(df)

    y = df_dummies[f'consumption_{energy_type}']
    X = df_dummies[['avg_temperature', 'day_of_week_Friday',
        'day_of_week_Monday', 'day_of_week_Saturday', 'day_of_week_Sunday',
            'day_of_week_Thursday', 'day_of_week_Tuesday', 'day_of_week_Wednesday']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    return regressor