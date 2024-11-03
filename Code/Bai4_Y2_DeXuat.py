import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = pd.read_csv("results.csv")

numeric_data = data[['non-Penalty Goals', 'Assists']].dropna()

x = numeric_data[['non-Penalty Goals']]  # chỉ số đầu vào
y = numeric_data['Assists']                # chỉ số mục tiêu

model = LinearRegression()
model.fit(x, y)

predictions = model.predict(x)

# vẽ biểu đồ phân tán và đường hồi quy
plt.figure(figsize=(10, 6))

# biểu đồ phân tán
plt.scatter(x, y, color='blue', label='Data Points', alpha=0.7)

# đường hồi quy
plt.plot(x, predictions, color='red', label='Regression Line')

# thêm tiêu đề và nhãn
plt.title('Non-Penalty Goals vs Assists with Linear Regression')
plt.xlabel('Non-Penalty Goals')
plt.ylabel('Assists')
plt.xlim(0, numeric_data['non-Penalty Goals'].max() + 5)
plt.ylim(0, numeric_data['Assists'].max() + 5)
plt.legend()
plt.grid()
plt.show()