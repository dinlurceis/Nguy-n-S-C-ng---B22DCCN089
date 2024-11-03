import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse


def radar_chart(player1, player2, attributes):
    # đọc dữ liệu từ file CSV
    df = pd.read_csv(r'D:\Coding\PycharmProjects\pythonProject\Python Ptit\results.csv')
    # lấy thông tin của cầu thủ
    player1_data = df[df['Player'] == player1][attributes].values.flatten()
    player2_data = df[df['Player'] == player2][attributes].values.flatten()

    # kiểm tra xem cầu thủ có tồn tại trong dữ liệu
    if player1_data.size == 0 or player2_data.size == 0:
        print("Một trong hai cầu thủ không tồn tại.")
        return

    # số lượng thuộc tính
    num_vars = len(attributes)

    # tạo góc cho biểu đồ radar
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # đưa dữ liệu về dạng khép kín
    player1_data = np.concatenate((player1_data, [player1_data[0]]))
    player2_data = np.concatenate((player2_data, [player2_data[0]]))
    angles += angles[:1]

    # tạo biểu đồ
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, player1_data, color='red', alpha=0.25, label=player1)
    ax.fill(angles, player2_data, color='blue', alpha=0.25, label=player2)

    # thiết lập nhãn cho các thuộc tính
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)

    # thêm tiêu đề và legend
    plt.title('So sánh cầu thủ')
    plt.legend(loc='upper right')

    # Hiển thị biểu đồ
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vẽ biểu đồ radar so sánh cầu thủ.')
    parser.add_argument('--p1', required=True, help='Tên cầu thủ 1')
    parser.add_argument('--p2', required=True, help='Tên cầu thủ 2')
    parser.add_argument('--Attribute', required=True, help='Danh sách thuộc tính (cách nhau bằng dấu phẩy)')

    args = parser.parse_args()

    # tạo danh sách thuộc tính
    attributes = [attr.strip() for attr in args.Attribute.split(',')]

    # gọi hàm vẽ biểu đồ radar
    radar_chart(args.p1, args.p2, attributes)