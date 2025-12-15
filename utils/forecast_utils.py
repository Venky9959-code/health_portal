from prophet import Prophet
import pandas as pd


def run_forecast(df, periods=14):
    """
    Runs time-series forecasting using Facebook Prophet
    """
    # Rename columns as required by Prophet
    df = df.rename(columns={"date": "ds", "cases": "y"})

    # Convert date column to datetime
    df["ds"] = pd.to_datetime(df["ds"])

    # Initialize and train model
    model = Prophet()
    model.fit(df[["ds", "y"]])

    # Create future dataframe
    future = model.make_future_dataframe(periods=periods)

    # Generate forecast
    forecast = model.predict(future)

    return model, forecast
