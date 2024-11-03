import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

data = pd.read_csv('results.csv')

# chọn tất cả các cột số, loại bỏ cột không phải số và giá trị thiếu
numeric_data = data.select_dtypes(include=['float64', 'int64']).dropna()

# chuẩn hóa dữ liệu
scaler = StandardScaler()
numeric_data_scaled = scaler.fit_transform(numeric_data)

# áp dụng PCA để giảm số chiều xuống 2 chiều
pca = PCA(n_components=2)
principal_components = pca.fit_transform(numeric_data_scaled)

# thực hiện K-means với số nhóm tối ưu (k = 5)
optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
labels = kmeans.fit_predict(numeric_data_scaled)

# vẽ hình phân cụm
plt.figure(figsize=(10, 6))
scatter = plt.scatter(principal_components[:, 0], principal_components[:, 1], c=labels, cmap='viridis', alpha=0.7)
plt.title('Phân cụm cầu thủ trên không gian 2D (PCA)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(scatter, label='Nhóm')
plt.grid()
plt.show()