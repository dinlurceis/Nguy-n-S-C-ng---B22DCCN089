import pandas as pd

df = pd.read_csv('results2.csv')

team_column_name = 'Team'

# lọc các cột chứa "mean of"
# lọc cột chứa Yellow Cards và Red Cards vì 2 chỉ số này mang tính tiêu cực
# lọc cột Age, Matches Played, Starts và Minutes vì những chỉ số này không nói lên hiệu suất
mean_columns = [col for col in df.columns if 'Mean of' in col and 'Cards' not in col and 'Age' not in col
                and 'Matches Played' not in col and 'Starts' not in col and 'Minutes' not in col]

# chuẩn hóa các chỉ số về thang 10
normalized_scores = pd.DataFrame()

# tạo dataframe cho tên đội
normalized_scores[team_column_name] = df[team_column_name].copy()

# tạo một list để lưu trữ các cột đã chuẩn hóa
normalized_columns = []

# chuẩn hóa từng chỉ số và thêm vào danh sách
for mean_col in mean_columns:
    # tính giá trị tối đa và tối thiểu của mỗi cột
    max_value = df[mean_col].max()
    min_value = df[mean_col].min()

    # chuẩn hóa về thang 10
    normalized_col = ((df[mean_col] - min_value) / (max_value - min_value)) * 10
    normalized_columns.append(normalized_col.copy())

# kết hợp tất cả các cột chuẩn hóa vào DataFrame
normalized_scores = pd.concat([normalized_scores] + normalized_columns, axis=1)

# đặt tên cho các cột đã chuẩn hóa
normalized_scores.columns = [team_column_name] + mean_columns

# tính điểm trung bình cho mỗi đội
normalized_scores = normalized_scores.copy()
normalized_scores['Average Score'] = normalized_scores[mean_columns].mean(axis=1)

# xác định đội bóng có phong độ tốt nhất
best_team_index = normalized_scores['Average Score'].idxmax()
best_team_name = normalized_scores.loc[best_team_index, team_column_name]
best_team_score = normalized_scores.loc[best_team_index, 'Average Score']

# in kết quả
print("Điểm số đã chuẩn hóa trên thang 10:")
print(normalized_scores)

print(f"\nĐội bóng có phong độ tốt nhất là: {best_team_name} với điểm số trung bình là {best_team_score:.2f}.")