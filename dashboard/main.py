# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Judul
st.title("Bike Sharing Analysis Dashboard")
st.write("This dashboard provides insights into bike sharing data, exploring factors that affect bike rentals and usage patterns.")

# Load data
df_hour = pd.read_csv("../data/hour.csv")
df_day = pd.read_csv("../data/day.csv")

# Show dataset information
st.header("Data Overview")
st.write("Bike Sharing Data (Hourly):")
st.dataframe(df_hour.head())

st.write("Bike Sharing Data (Daily):")
st.dataframe(df_day.head())

# Exploratory Data Analysis
st.header("Exploratory Data Analysis")

# Grouping average count per hour
average_cnt_per_hour = df_hour.groupby('hr')['cnt'].mean()

# Konversi temperature menjadi temperature aktual dan melakukan binning
t_max = 39
t_min = -8
df_hour['actual_temp'] = (df_hour['temp'] * (t_max - t_min) + t_min).round(2)
df_hour['temp_bin'] = pd.cut(df_hour['actual_temp'], bins=5)
average_cnt_per_temp = df_hour.groupby('temp_bin')['cnt'].mean()

# Korelasi
df_corr = df_day.copy()
df_corr.drop(columns=['casual', 'registered', 'instant', 'dteday', 'yr'], inplace=True)
correlation_matrix = df_corr.corr()

# Grouping average count per day
df_weekday = df_day[df_day['holiday'] != 1]
average_cnt_per_day = df_weekday.groupby('weekday')['cnt'].mean()

# Visualization
st.subheader("1. Correlation Heatmap")
st.write("This heatmap shows the correlation between variables and bike rental counts.")
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
st.pyplot(plt)

st.subheader("2. Average Bike Rentals by Temperature")
st.write("This bar chart shows the average number of bike rentals across different temperature bins.")
plt.figure(figsize=(8, 5))
average_cnt_per_temp.plot(kind='bar')
plt.xlabel('Temperature Bins')
plt.ylabel('Average Total Count')
plt.title('Average Total Count per Temperature Bin')
st.pyplot(plt)

st.subheader("3. Average Bike Rentals by Hour")
st.write("This line chart shows the average number of bike rentals at different hours of the day.")
plt.figure(figsize=(8, 5))
plt.plot(average_cnt_per_hour)
plt.xlabel('Hour')
plt.ylabel('Average Count')
plt.title('Average Count per Hour')
st.pyplot(plt)

st.subheader("4. Average Bike Rentals by Weekday")
st.write("This line chart shows the average number of bike rentals across different weekdays.")
plt.figure(figsize=(8, 5))
plt.plot(average_cnt_per_day)
plt.xlabel('Day')
plt.ylabel('Average Count')
plt.title('Average Count per Day')
st.pyplot(plt)

# Kesimpulan
st.header("Conclusion")
st.write("""
- **Parameter yang Paling Mempengaruhi Jumlah Penyewaan Sepeda:** Dari heatmap korelasi, temperatur (dan apparent temperature) memiliki korelasi tertinggi dengan jumlah penyewaan sepeda. Korelasi mencapai sekitar 0,63, menunjukkan bahwa semakin tinggi suhu, semakin banyak orang yang menyewa sepeda.
- **Pengaruh Temperatur terhadap Jumlah Penyewaan Sepeda:** Analisis grafik menunjukkan bahwa jumlah penyewaan sepeda meningkat seiring dengan meningkatnya temperatur.
- **Pola Jumlah Penyewaan Sepeda:** Penyewaan tertinggi terjadi pada jam 8 pagi dan 17-18 sore, sesuai dengan waktu orang berangkat dan pulang kerja. Penyewaan tertinggi per hari terjadi pada hari Kamis dan Jumat, dengan penurunan signifikan pada hari Minggu.
""")
