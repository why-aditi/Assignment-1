import pandas as pd
import pytz

df = pd.read_csv('AirQualityUCI.csv', delimiter=';')

df['Time'] = df['Time'].str.replace('.', ':')

df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')

italy_tz = pytz.timezone('Europe/Rome')

df['Datetime'] = df['Datetime'].dt.tz_localize(italy_tz, ambiguous='NaT', nonexistent='shift_forward').dt.tz_convert(pytz.UTC)

df['Datetime'] = df['Datetime'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

df.drop(columns=['Date', 'Time'], inplace=True)

df = df.applymap(lambda x: str(x).replace(',', '.') if isinstance(x, str) else x)

df.to_csv('updated_file_utc.csv', index=False, sep=';')

print(df.head())
