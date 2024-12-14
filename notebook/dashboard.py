import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Thiết lập trang
st.set_page_config(layout="wide")

# Tiêu đề chính
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem;
    }
    h1 {
        color: #1E88E5;
        text-align: center;
        padding-bottom: 2rem;
    }
    .stSubheader {
        color: #424242;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1E88E5; font-size: 24px; padding: 0.5rem;'>NASA Near-Earth Objects Analysis Dashboard</h1><br>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('../data/NASA Near-Earth Objects-Sampling.csv', index_col=0)
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
row4_col1, row4_col2 = st.columns([1, 2])

# Dòng 1
with row1_col1:
    # st.subheader('Phân bố thiên thạch nguy hiểm')
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    df['is_potentially_hazardous_asteroid'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Phân bố thiên thạch nguy hiểm')
    plt.legend(['Không nguy hiểm', 'Nguy hiểm'], loc='upper right')
    st.pyplot(fig1)

with row1_col2:
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    # Vẽ KDE với fill
    sns.kdeplot(data=df[df['is_potentially_hazardous_asteroid']]['absolute_magnitude_h'],
                color='red', label='Nguy hiểm', linewidth=2,
                fill=True, alpha=0.3)
    
    sns.kdeplot(data=df[~df['is_potentially_hazardous_asteroid']]['absolute_magnitude_h'],
                color='lightgreen', label='Không nguy hiểm', linewidth=2,
                fill=True, alpha=0.3)
    
    sns.kdeplot(data=df['absolute_magnitude_h'],
                color='blue', label='Trung bình chung', 
                linestyle='--', linewidth=2)
    
    plt.title('Phân phối độ sáng tuyệt đối của các thiên thể')
    plt.xlabel('Độ sáng tuyệt đối (H)')
    plt.ylabel('Mật độ')
    plt.legend(title='Mức độ nguy hiểm')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)

# Dòng 2
with row2_col1:
    # st.subheader('Phân bố đối tượng Sentry')
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    plt.pie(df['is_sentry_object'].value_counts(), autopct='%1.1f%%', colors=sns.color_palette("pastel"))
    plt.title('Phân bố đối tượng Sentry')
    plt.legend(['Không phải Sentry', 'Sentry'], loc='upper right')
    st.pyplot(fig3)

with row2_col2:
    # st.subheader('Tương quan giữa khả năng va chạm và mức độ nguy hiểm')
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    
    # Tạo bảng crosstab
    ct = pd.crosstab(df['is_collidable'], df['is_potentially_hazardous_asteroid'], 
                     normalize='index') * 100
    
    # Đổi tên index và columns để dễ đọc
    ct.index = ['Không va chạm', 'Có thể va chạm']
    ct.columns = ['Không nguy hiểm', 'Nguy hiểm']
    
    # Vẽ stacked bar chart
    ct.plot(kind='bar', stacked=True, 
           color=['lightblue', 'coral'],
           width=0.5,   
           ax=ax4)
    
    plt.title('Phân tích mối quan hệ giữa\nkhả năng va chạm và mức độ nguy hiểm')
    plt.xlabel('Khả năng va chạm')
    plt.ylabel('Phần trăm (%)')
    plt.legend(title='Mức độ nguy hiểm',
              bbox_to_anchor=(1.05, 1),
              loc='upper left')
    
    # Thêm label phần trăm với vị trí điều chỉnh
    for i, container in enumerate(ax4.containers):
        # Vị trí label sẽ khác nhau cho từng phần của stack
        if i == 0:  # Phần đầu tiên (không nguy hiểm)
            ax4.bar_label(container, fmt='%.1f%%', label_type='center')
        else:  # Phần thứ hai (nguy hiểm)
            ax4.bar_label(container, fmt='%.1f%%', label_type='center')
    
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig4)

# Dòng 3
with row3_col1:
    # st.subheader('Phân bố khả năng va chạm')
    fig5, ax5 = plt.subplots(figsize=(6, 6))
    plt.pie(df['is_collidable'].value_counts(), autopct='%1.1f%%', colors=sns.color_palette("pastel"))
    plt.title('Phân bố khả năng va chạm')
    plt.legend(['Không thể va chạm', 'Có thể va chạm'], loc='upper right')
    st.pyplot(fig5)

with row3_col2:
    # st.subheader('Trung bình cận nhật, viễn nhật theo loại quỹ đạo')
    earth_aphelion = 1.0167103 
    earth_perihelion = 0.9832899
    delta = 0.0001943 
    
    perihelion_min = earth_perihelion - delta
    aphelion_max = earth_aphelion + delta
    
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    
    # Tính trung bình cho từng nhóm (nguy hiểm/không nguy hiểm)
    avg_distances_hazardous = df[df['is_potentially_hazardous_asteroid']].groupby('orbit_class_type')[['perihelion_distance', 'aphelion_distance']].mean()
    avg_distances_non_hazardous = df[~df['is_potentially_hazardous_asteroid']].groupby('orbit_class_type')[['perihelion_distance', 'aphelion_distance']].mean()
    
    # Vẽ đường tham chiếu
    plt.axhline(y=aphelion_max, color='red', linestyle='--', label='Đường viễn nhật của Trái đất')
    plt.axhline(y=perihelion_min, color='blue', linestyle='--', label='Đường cận nhật của Trái đất')
    
    # Vẽ đường cho vật thể nguy hiểm
    plt.plot(avg_distances_hazardous.index, avg_distances_hazardous['perihelion_distance'], 
            marker='o', label='Cận nhật (Nguy hiểm)', color='darkred', linestyle='-')
    plt.plot(avg_distances_hazardous.index, avg_distances_hazardous['aphelion_distance'], 
            marker='o', label='Viễn nhật (Nguy hiểm)', color='red', linestyle='-')
    
    # Vẽ đường cho vật thể không nguy hiểm
    plt.plot(avg_distances_non_hazardous.index, avg_distances_non_hazardous['perihelion_distance'], 
            marker='o', label='Cận nhật (Không nguy hiểm)', color='darkblue', linestyle='-')
    plt.plot(avg_distances_non_hazardous.index, avg_distances_non_hazardous['aphelion_distance'], 
            marker='o', label='Viễn nhật (Không nguy hiểm)', color='blue', linestyle='-')
    
    plt.title('Trung bình cận nhật, viễn nhật theo loại quỹ đạo và mức độ nguy hiểm')
    plt.xlabel('Loại quỹ đạo')
    plt.ylabel('Khoảng cách (AU)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig6)


with row4_col1:
    # st.subheader('Phân bố kích thước thiên thể')
    fig8, ax8 = plt.subplots(figsize=(6, 6))
    
    # Tạo các nhóm kích thước
    def size_category(diameter):
        if diameter < 0.1:
            return 'Rất nhỏ (<0.1km)'
        elif diameter < 0.5:
            return 'Nhỏ (0.1-0.5km)'
        elif diameter < 1:
            return 'Trung bình (0.5-1km)'
        else:
            return 'Lớn (>1km)'

    df['size_category'] = df['kilometers_estimated_diameter_max'].apply(size_category)
    size_ratio = df['size_category'].value_counts()

    plt.pie(size_ratio,
            labels=size_ratio.index,
            autopct='%1.1f%%',
            pctdistance=0.85,
            wedgeprops=dict(width=0.5))
    plt.title('Phân bố kích thước thiên thể')
    plt.legend(title='Kích thước', loc='upper left')
    plt.tight_layout()
    st.pyplot(fig8)

with row4_col2:
    # st.subheader('Tần suất phát hiện vật thể từ năm 1980')
    fig7, ax7 = plt.subplots(figsize=(15, 7))
    
    # Lọc dữ liệu từ năm 1980
    df_filtered = df[df['first_observation_year'] >= 1980]
    
    sns.histplot(data=df_filtered, 
                x='first_observation_year', 
                hue='is_potentially_hazardous_asteroid',
                multiple="stack",
                palette=['lightgreen', 'red'],
                bins=40,
                edgecolor='white',
                kde=True)
    
    plt.title('Tần suất phát hiện vật thể từ năm 1980')
    plt.xlabel('Năm phát hiện đầu tiên')
    plt.ylabel('Số lượng vật thể')
    plt.legend(title='Mức độ nguy hiểm',
              labels=['Nguy hiểm', 'Không nguy hiểm'])
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig7)


# # Filters sidebar
# with st.sidebar:
#     st.header('Filters')
    
#     # Magnitude range slider
#     mag_range = st.slider('Magnitude Range', 
#                          float(df['absolute_magnitude_h'].min()),
#                          float(df['absolute_magnitude_h'].max()),
#                          (float(df['absolute_magnitude_h'].min()),
#                           float(df['absolute_magnitude_h'].max())))
    
#     # Hazard filter
#     hazard_filter = st.multiselect('Hazard Status',
#                                   ['Hazardous', 'Non-hazardous'],
#                                   ['Hazardous', 'Non-hazardous'])
    
#     # Orbit class filter
#     orbit_filter = st.multiselect('Orbit Class',
#                                  df['orbit_class_type'].unique(),
#                                  df['orbit_class_type'].unique())

# Add some spacing at the bottom
st.markdown('---')
