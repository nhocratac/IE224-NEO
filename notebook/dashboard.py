import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Thiết lập trang
st.set_page_config(layout="wide")

# Tiêu đề chính
st.title('NASA Near-Earth Objects Analysis Dashboard')

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('../data/NASA Near-Earth Objects-CleanbyThang.csv', index_col=0)
    df['first_observation_date'] = pd.to_datetime(df['first_observation_date'])
    df['last_observation_date'] = pd.to_datetime(df['last_observation_date'])
    return df

df = load_data()

# Layout chính với 3 cột
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header('Basic Statistics')
    # Hiển thị thống kê cơ bản
    st.write(df.describe())

    # Pie chart cho Hazardous vs Non-hazardous
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    df['is_potentially_hazardous_asteroid'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Hazardous Asteroids')
    st.pyplot(fig1)

with col2:
    st.header('Size Distribution')
    # Scatter plot cho diameter vs magnitude
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x='kilometers_estimated_diameter_max', 
                    y='absolute_magnitude_h', 
                    hue='is_potentially_hazardous_asteroid')
    plt.title('Size vs Magnitude')
    st.pyplot(fig2)

    # Distribution plot
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.histplot(data=df, x='absolute_magnitude_h', 
                hue='is_potentially_hazardous_asteroid', multiple="stack")
    plt.title('Magnitude Distribution')
    st.pyplot(fig3)

with col3:
    st.header('Orbital Characteristics')
    # Scatter plot cho orbit distances
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x='perihelion_distance', 
                    y='aphelion_distance',
                    hue='is_potentially_hazardous_asteroid')
    plt.title('Orbital Distances')
    st.pyplot(fig4)

# Tạo tabs cho phân tích chi tiết
tab1, tab2 = st.tabs(["Detailed Analysis", "Time Series"])

with tab1:
    # 2 cột cho phân tích chi tiết
    det_col1, det_col2 = st.columns(2)
    
    with det_col1:
        st.subheader('Correlation Matrix')
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        corr = df[numeric_cols].corr()
        fig5, ax5 = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        st.pyplot(fig5)

    with det_col2:
        st.subheader('Orbit Class Distribution')
        fig6, ax6 = plt.subplots(figsize=(10, 8))
        df['orbit_class_type'].value_counts().plot(kind='bar')
        plt.xticks(rotation=45)
        st.pyplot(fig6)

with tab2:
    st.subheader('Observations Over Time')
    # Time series plot
    fig7, ax7 = plt.subplots(figsize=(15, 6))
    df['first_observation_date'].value_counts().sort_index().plot()
    plt.title('Number of First Observations Over Time')
    st.pyplot(fig7)

# Filters sidebar
with st.sidebar:
    st.header('Filters')
    
    # Magnitude range slider
    mag_range = st.slider('Magnitude Range', 
                         float(df['absolute_magnitude_h'].min()),
                         float(df['absolute_magnitude_h'].max()),
                         (float(df['absolute_magnitude_h'].min()),
                          float(df['absolute_magnitude_h'].max())))
    
    # Hazard filter
    hazard_filter = st.multiselect('Hazard Status',
                                  ['Hazardous', 'Non-hazardous'],
                                  ['Hazardous', 'Non-hazardous'])
    
    # Orbit class filter
    orbit_filter = st.multiselect('Orbit Class',
                                 df['orbit_class_type'].unique(),
                                 df['orbit_class_type'].unique())

# Add some spacing at the bottom
st.markdown('---')
st.markdown('Dashboard created by [Your Name]')