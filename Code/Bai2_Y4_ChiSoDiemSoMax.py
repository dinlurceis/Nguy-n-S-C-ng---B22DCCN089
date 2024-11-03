import pandas as pd

df = pd.read_csv('results2.csv')

team_column_name = 'Team'

# lọc các cột chứa "mean of"
mean_columns = [col for col in df.columns if 'Mean of' in col]

results = []

for mean_col in mean_columns:
    max_value = df[mean_col].max()  # giá trị cao nhất trong cột mean
    best_team = df.loc[df[mean_col] == max_value, team_column_name].values[0]  # tên đội tương ứng
    attribute = "".join(x + " " for x in mean_col.split()[2:]).strip()
    results.append({'Attribute': attribute, 'Max Score': max_value, 'Best Team': best_team})

# chuyển kết quả thành DataFrame
results_df = pd.DataFrame(results)

# in kết quả
print("Đội bóng có chỉ số điểm số cao nhất ở mỗi chỉ số (lấy trung bình toàn đội):")
print(results_df)
