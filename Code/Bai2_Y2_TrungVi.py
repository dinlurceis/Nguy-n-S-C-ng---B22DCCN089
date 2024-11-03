import pandas as pd

# đọc file csv từ bài 1
df = pd.read_csv('results.csv')

# gán attributes là các cột giá trị
attributes = df.columns[5:]  # bỏ 5 cột đầu: stt, player, nation, team, position
results = {'Team': ['all']}  # khởi tạo với 'all'

# tính toán cho từng chỉ số
for attribute in attributes:
    # chuyển đổi kiểu dữ liệu và xử lý chuỗi
    df[attribute] = df[attribute].astype(str)
    cleaned_data = df[attribute].str.replace("'", "", regex=False).str.replace(",", "", regex=False)

    # loại bỏ các giá trị 'N/a'
    cleaned_data = cleaned_data[cleaned_data != 'N/a']

    # chuyển đổi sang kiểu số
    cleaned_data = pd.to_numeric(cleaned_data, errors='coerce')

    # Tính toán các chỉ số
    results[f'Median of {attribute}'] = ["{:.2f}".format(cleaned_data.median())] if not cleaned_data.empty else ['N/a']
    results[f'Mean of {attribute}'] = ["{:.2f}".format(cleaned_data.mean())] if not cleaned_data.empty else ['N/a']
    results[f'Std of {attribute}'] = ["{:.2f}".format(cleaned_data.std())] if not cleaned_data.empty else ['N/a']

team_column_name = 'Team'

# thêm dữ liệu cho từng đội
teams = df[team_column_name].unique()  # lấy danh sách các đội

# khởi tạo list để lưu kết quả cho từng đội
team_results = []

for team in teams:
    team_data = df[df[team_column_name] == team].copy()  # sử dụng .copy() để tạo bản sao
    team_result = {team_column_name: team}  # khởi tạo cho đội này
    for attribute in attributes:
        # chuyển đổi kiểu dữ liệu và xử lý chuỗi
        team_data[attribute] = team_data[attribute].astype(str)
        cleaned_data = team_data[attribute].str.replace("'", "").str.replace(",", "")

        # loại bỏ các giá trị 'N/a'
        cleaned_data = cleaned_data[cleaned_data != 'N/a']

        # chuyển đổi sang kiểu số
        cleaned_data = pd.to_numeric(cleaned_data)

        # Tính toán các chỉ số
        team_result[f'Median of {attribute}'] = "{:.2f}".format(cleaned_data.median()) if not cleaned_data.empty else 'N/a'
        team_result[f'Mean of {attribute}'] = "{:.2f}".format(cleaned_data.mean()) if not cleaned_data.empty else 'N/a'
        team_result[f'Std of {attribute}'] = "{:.2f}".format(cleaned_data.std()) if not cleaned_data.empty else 'N/a'

    # thêm kết quả của đội vào danh sách
    team_results.append(team_result)

# chuyển đổi danh sách kết quả thành DataFrame
team_results_df = pd.DataFrame(team_results)

# thêm vào kết quả tổng
results_df = pd.DataFrame(results)
results_df = pd.concat([results_df, team_results_df])

results_df.to_csv('results2.csv')