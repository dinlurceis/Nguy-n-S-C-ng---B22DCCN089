import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# đường dẫn lưu hình ảnh
output_dir = 'D:\\Coding\\PycharmProjects\\pythonProject\\Python PTIT\\histograms'
os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

df = pd.read_csv('results.csv')


attributes = df.columns[5:]

cur_out_dir = output_dir + "\\All Team"
os.makedirs(cur_out_dir, exist_ok=True)  # tạo thư mục nếu chưa tồn tại

for attribute in attributes:
    df[attribute] = df[attribute].astype(str)
    cleaned_data = df[attribute].str.replace("'", "").str.replace(",", "")

    # loại bỏ 'N/a'
    cleaned_data = cleaned_data.str.strip()
    cleaned_data = cleaned_data[cleaned_data != 'N/a']

    # chuyển đổi sang kiểu số
    cleaned_data = pd.to_numeric(cleaned_data)

    # vẽ histogram cho toàn bộ dữ liệu
    plt.figure(figsize=(10, 6))
    sns.histplot(cleaned_data.dropna(), bins=20, kde=True)
    plt.title(f'Histogram of {attribute} for All Players')
    plt.xlabel(attribute)
    plt.ylabel('Frequency')
    plt.grid()

    # lưu file, loại bỏ ký tự '%' trong tên file
    safe_attribute = attribute.replace('%', 'percent').replace('/', 'out of').replace(' ', '_')
    plt.savefig(os.path.join(cur_out_dir, f'histogram_all_{safe_attribute}.png'))
    plt.show()
    plt.close()  # đóng hình ảnh sau khi lưu

# thêm dữ liệu cho từng đội
team_column_name = 'Team'  # cập nhật nếu tên cột khác
if team_column_name in df.columns:
    teams = df[team_column_name].unique()  # lấy danh sách các đội

    for team in teams:
        team_data = df[df[team_column_name] == team].copy()  # sử dụng .copy() để tạo bản sao
        cur_out_dir = output_dir + "\\" + team
        os.makedirs(cur_out_dir, exist_ok=True)  # tạo thư mục nếu chưa tồn tại

        for attribute in attributes:
            team_data[attribute] = team_data[attribute].astype(str)
            cleaned_data = team_data[attribute].str.replace("'", "").str.replace(",", "")

            # loại bỏ 'N/a'
            cleaned_data = cleaned_data.str.strip()
            cleaned_data = cleaned_data[cleaned_data != 'N/a']

            # chuyển đổi sang kiểu số
            cleaned_data = pd.to_numeric(cleaned_data)

            # vẽ histogram cho từng đội
            plt.figure(figsize=(10, 6))
            sns.histplot(cleaned_data.dropna(), bins=20, kde=True)
            plt.title(f'Histogram of {attribute} for Team {team}')
            plt.xlabel(attribute)
            plt.ylabel('Frequency')
            plt.grid()

            # lưu file, loại bỏ ký tự '%' trong tên file
            safe_attribute = attribute.replace('%', 'percent').replace('/', 'out of').replace(' ', '_')
            plt.savefig(os.path.join(cur_out_dir, f'histogram_{team}_{safe_attribute}.png'))
            plt.close()  # đóng hình ảnh sau khi lưu