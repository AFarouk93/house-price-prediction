import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

# Load dataset
DATA_PATH = 'kc_house_data.csv'

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    # Drop columns that are not useful for prediction
    df = df.drop(['id', 'date'], axis=1)
    # Handle categorical zipcode by treating it as numeric
    df['zipcode'] = pd.to_numeric(df['zipcode'], errors='coerce')
    df = df.dropna()
    X = df.drop('price', axis=1).values
    y = df['price'].values
    return train_test_split(X, y, test_size=0.2, random_state=42)

def build_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(input_shape,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def main():
    X_train, X_test, y_train, y_test = load_data()
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    model = build_model(X_train.shape[1])
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=2)
    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    print(f'Test MAE: {mae:.2f}')

if __name__ == '__main__':
    main()
