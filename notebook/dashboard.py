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
    df['first_observation_year'] = df['first_observation_date'].dt.year
    df['last_observation_year'] = df['last_observation_date'].dt.year
    return df

df = load_data()


# Thay đổi layout chính thành 2 hàng với 3 cột mỗi hàng
row1_col1, row1_col2 = st.columns([1, 2])  # Dòng 1: 1 biểu đồ tròn + 1 biểu đồ cột
row2_col1, row2_col2 = st.columns([1, 2])  # Dòng 2: 1 biểu đồ tròn + 1 biểu đồ cột
row3_col1, row3_col2 = st.columns([1, 2])  # Dòng 3: 1 biểu đồ tròn + 1 biểu đồ line
row4_col1 = st.columns([1])[0]

# Dòng 1
with row1_col1:
    st.subheader('Phân bố thiên thạch nguy hiểm')
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    df['is_potentially_hazardous_asteroid'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Phân bố thiên thạch nguy hiểm')
    plt.legend(['Không nguy hiểm', 'Nguy hiểm'], loc='upper right')
    st.pyplot(fig1)

with row1_col2:
    st.subheader('Phân bố loại quỹ đạo theo mức độ nguy hiểm')
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.countplot(data=df, x='orbit_class_type', hue='is_potentially_hazardous_asteroid',
                  palette=['lightgreen', 'red'])
    plt.title('Phân bố loại quỹ đạo theo mức độ nguy hiểm')
    plt.xlabel('Loại quỹ đạo')
    plt.ylabel('Số lượng')
    plt.xticks(rotation=45)
    plt.legend(title='Mức độ nguy hiểm', labels=['Không nguy hiểm', 'Nguy hiểm'])
    plt.gca().bar_label(plt.gca().containers[0])
    plt.gca().bar_label(plt.gca().containers[1])
    plt.tight_layout()
    st.pyplot(fig2)

# Dòng 2
with row2_col1:
    st.subheader('Phân bố đối tượng Sentry')
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    plt.pie(df['is_sentry_object'].value_counts(), autopct='%1.1f%%', colors=sns.color_palette("pastel"))
    plt.title('Phân bố đối tượng Sentry')
    plt.legend(['Không phải Sentry', 'Sentry'], loc='upper right')
    st.pyplot(fig3)

with row2_col2:
    st.subheader('Phân bố đối tượng có khả năng va chạm')
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.countplot(data=df, x='is_collidable', hue='is_potentially_hazardous_asteroid',
                  palette=['blue', 'orange'])
    plt.title('Phân bố đối tượng có khả năng va chạm theo mức độ nguy hiểm')
    plt.xlabel('Khả năng va chạm')
    plt.ylabel('Số lượng')
    plt.legend(title='Mức độ nguy hiểm', labels=['Không nguy hiểm', 'Nguy hiểm'])
    plt.gca().bar_label(plt.gca().containers[0])
    plt.gca().bar_label(plt.gca().containers[1])
    st.pyplot(fig4)

# Dòng 3
with row3_col1:
    st.subheader('Phân bố khả năng va chạm')
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    plt.pie(df['is_collidable'].value_counts(), autopct='%1.1f%%', colors=sns.color_palette("pastel"))
    plt.title('Phân bố khả năng va chạm')
    plt.legend(['Không thể va chạm', 'Có thể va chạm'], loc='upper right')
    st.pyplot(fig5)

with row3_col2:
    st.subheader('Trung bình cận nhật, viễn nhật theo loại quỹ đạo')
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    avg_distances = df.groupby('orbit_class_type')[['perihelion_distance', 'aphelion_distance']].mean()
    plt.plot(avg_distances.index, avg_distances['perihelion_distance'], marker='o', label='Cận nhật')
    plt.plot(avg_distances.index, avg_distances['aphelion_distance'], marker='o', label='Viễn nhật')
    plt.title('Trung bình cận nhật, viễn nhật theo loại quỹ đạo')
    plt.xlabel('Loại quỹ đạo')
    plt.ylabel('Khoảng cách (AU)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig6)


with row4_col1:
    st.subheader('Tần suất phát hiện vật thể theo năm từ sau năm 1980')
    fig7, ax7 = plt.subplots(figsize=(15, 6))
    
    # Trích xuất năm từ cột first_observation_date
    df['first_observation_year'] = pd.to_datetime(df['first_observation_date']).dt.year

    df_filtered = df[df['first_observation_year'] >= 1980]
    
    # Vẽ histogram
    sns.histplot(data=df_filtered, 
                x='first_observation_year', 
                hue='is_potentially_hazardous_asteroid',
                multiple="stack",
                palette=['lightgreen', 'red'],
                bins=50,
                edgecolor='white')
    
    plt.title('Tần suất phát hiện vật thể theo năm')
    plt.xlabel('Năm phát hiện đầu tiên')
    plt.ylabel('Số lượng vật thể')
    
    # Điều chỉnh legend
    plt.legend(title='Potentially Hazardous',
              labels=['Nguy hiểm', 'Không nguy hiểm'])
    
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
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