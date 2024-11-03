import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('results.csv')

# chọn tất cả các cột số, loại bỏ cột không phải số và giá trị thiếu
numeric_data = data.select_dtypes(include=['float64', 'int64']).dropna()

# chuẩn hóa dữ liệu
scaler = StandardScaler()
numeric_data_scaled = scaler.fit_transform(numeric_data)

# chạy K-means
kmeans = KMeans(n_clusters=5)  # chọn số nhóm, ở đây em chọn 5
kmeans.fit(numeric_data_scaled)

data['Cluster'] = kmeans.labels_

# in ra thông tin chi tiết theo từng nhóm
for cluster in range(5):  # giả sử có 5 nhóm
    print(f"\n--- Nhóm {cluster + 1} ---")
    cluster_data = data[data['Cluster'] == cluster]
    print(cluster_data[['Player', 'Nation', 'Team', 'Position', 'Age']])