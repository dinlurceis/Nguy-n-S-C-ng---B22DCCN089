import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

data = pd.read_csv('results.csv')

# loại bỏ cột không phải số và giá trị thiếu
numeric_data = data.select_dtypes(include=['float64', 'int64']).dropna()

# chuẩn hóa dữ liệu
scaler = StandardScaler()
numeric_data_scaled = scaler.fit_transform(numeric_data)

# phương pháp Elbow để xác định số nhóm tối ưu
inertia = []
K = range(1, 11)  # thử nghiệm với số nhóm từ 1 đến 10

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(numeric_data_scaled)
    inertia.append(kmeans.inertia_)

# vẽ đồ thị Elbow
plt.figure(figsize=(10, 6))
plt.plot(K, inertia, 'bx-')
plt.xlabel('Số nhóm k')
plt.ylabel('Độ biến thiên')
plt.title('Phương pháp Elbow để xác định số nhóm tối ưu')
plt.grid()
plt.show()

# tính chỉ số Silhouette
silhouette_scores = []
for k in K[1:]:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(numeric_data_scaled)
    silhouette_scores.append(silhouette_score(numeric_data_scaled, labels))

# vẽ đồ thị Silhouette
plt.figure(figsize=(10, 6))
plt.plot(K[1:], silhouette_scores, 'bx-')
plt.xlabel('Số nhóm k')
plt.ylabel('Chỉ số Silhouette ')
plt.title('Chỉ số Silhouette để xác định số nhóm tối ưu')
plt.grid()
plt.show()

# xác định số nhóm tối ưu
optimal_k = 5  # Thay đổi theo điểm khuỷu trong đồ thị Elbow và giá trị cao nhất trong Silhouette Score

# Bước 4: Chạy K-means với số nhóm tối ưu
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
labels = kmeans.fit_predict(numeric_data_scaled)

# Thêm nhãn nhóm vào dữ liệu gốc
data['Cluster'] = labels

# Bước 5: Hiển thị kết quả
for cluster in range(optimal_k):
    print(f"\n--- Nhóm {cluster + 1} ---")
    cluster_data = data[data['Cluster'] == cluster]
    print(cluster_data[['Player', 'Nation', 'Team', 'Position', 'Age', 'Matches Played'] + list(numeric_data.columns)])