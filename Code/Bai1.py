import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


urls = [
    'https://fbref.com/en/squads/b8fd03ef/2023-2024/Manchester-City-Stats',
    'https://fbref.com/en/squads/18bb7c10/2023-2024/Arsenal-Stats',
    'https://fbref.com/en/squads/822bd0ba/2023-2024/Liverpool-Stats',
    'https://fbref.com/en/squads/8602292d/2023-2024/Aston-Villa-Stats',
    'https://fbref.com/en/squads/361ca564/2023-2024/Tottenham-Hotspur-Stats',
    'https://fbref.com/en/squads/cff3d9bb/2023-2024/Chelsea-Stats',
    'https://fbref.com/en/squads/b2b47a98/2023-2024/Newcastle-United-Stats',
    'https://fbref.com/en/squads/19538871/2023-2024/Manchester-United-Stats',
    'https://fbref.com/en/squads/7c21e445/2023-2024/West-Ham-United-Stats',
    'https://fbref.com/en/squads/47c64c55/2023-2024/Crystal-Palace-Stats',
    'https://fbref.com/en/squads/d07537b9/2023-2024/Brighton-and-Hove-Albion-Stats',
    'https://fbref.com/en/squads/4ba7cbea/2023-2024/Bournemouth-Stats',
    'https://fbref.com/en/squads/fd962109/2023-2024/Fulham-Stats',
    'https://fbref.com/en/squads/8cec06e1/2023-2024/Wolverhampton-Wanderers-Stats',
    'https://fbref.com/en/squads/d3fd31cc/2023-2024/Everton-Stats',
    'https://fbref.com/en/squads/cd051869/2023-2024/Brentford-Stats',
    'https://fbref.com/en/squads/e4a775cb/2023-2024/Nottingham-Forest-Stats',
    'https://fbref.com/en/squads/e297cd13/2023-2024/Luton-Town-Stats',
    'https://fbref.com/en/squads/943e8050/2023-2024/Burnley-Stats',
    'https://fbref.com/en/squads/1df6b87e/2023-2024/Sheffield-United-Stats'
]

player_data = {}  # luu player vao dict, key la ten, value la cac cot
for url in urls:
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.string
    titleWord = title.split()
    team_name = ""
    for i in range(1, len(titleWord)):  # bat dau tu 1 vi title co dinh dang: 2023-2024 <ten Team> Stats, ...
        if titleWord[i] == 'Stats,':
            break
        else:
            team_name += titleWord[i] + " "
    team_name = team_name.strip()

    # standard stats table
    table = soup.find('table', {'id': 'stats_standard_9'})

    rows = table.find_all('tr')
    # chay tu 2 de loai bo 2 dong chua ten cot du lieu, chay den len - 2 de bo 2 dong cuoi
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])  # tim cac the th va td
        player_row = [col.get_text(strip=True) for col in cols]  # tach du lieu tung cot

        player_name = player_row[0]  # cot du lieu dau tien la ten player
        player_key = player_name + "," + team_name
        # kiem tra co phai ten player khong, vi co 1 vai bang co 2 bang nho -> co nhieu dong chua ten cot du lieu
        if player_row[0] != '' and player_row[0] != 'Player':
            player_data[player_key] = []
            for i in range(1, 7):
                if i == 2: player_data[player_key].append(team_name)
                if player_row[i] != '':
                    player_data[player_key].append(player_row[i])
                else:
                    player_data[player_key].append('N/a')
            index = [11, 12, 9, 14, 15]
            for i in index:
                if player_row[i] != '':
                    player_data[player_key].append(player_row[i])
                else:
                    player_data[player_key].append('N/a')
            for i in range(16, len(player_row) - 1):
                if i == 19: continue
                if player_row[i] != '':
                    player_data[player_key].append(player_row[i])
                else:
                    player_data[player_key].append('N/a')

    # goalkeeping table
    table = soup.find('table', {'id': 'stats_keeper_9'})
    rows = table.find_all('tr')
    start = 8
    maxLen = 0
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])
        player_row = [col.get_text(strip=True) for col in cols]

        player_name = player_row[0]
        player_key = player_name + "," + team_name

        for i in range(start, len(player_row) - 1):
            if player_row[i] != '':
                player_data[player_key].append(player_row[i])
            else:
                player_data[player_key].append('N/a')
        maxLen = max(maxLen, len(player_data[player_key]))
    for player_notUpdated in player_data.keys():
        if len(player_data[player_notUpdated]) < maxLen:
            index = len(player_data[player_notUpdated])
            for x in range(maxLen - index):
                player_data[player_notUpdated].append('N/a')

    # shooting table
    table = soup.find('table', {'id': 'stats_shooting_9'})
    rows = table.find_all('tr')
    start = 5
    maxLen = 0
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])
        player_row = [col.get_text(strip=True) for col in cols]

        player_name = player_row[0]
        player_key = player_name + "," + team_name

        for i in range(start, len(player_row) - 1):
            if player_row[i] != '':
                player_data[player_key].append(player_row[i])
            else:
                player_data[player_key].append('N/a')
        maxLen = max(maxLen, len(player_data[player_key]))
    for player_notUpdated in player_data.keys():
        if len(player_data[player_notUpdated]) < maxLen:
            index = len(player_data[player_notUpdated])
            for x in range(maxLen - index):
                player_data[player_notUpdated].append('N/a')

    # passing table
    table = soup.find('table', {'id': 'stats_passing_9'})
    rows = table.find_all('tr')
    start = 5
    maxLen = 0
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])
        player_row = [col.get_text(strip=True) for col in cols]

        player_name = player_row[0]
        player_key = player_name + "," + team_name

        for i in range(start, len(player_row) - 1):
            if player_row[i] != '':
                player_data[player_key].append(player_row[i])
            else:
                player_data[player_key].append('N/a')
        maxLen = max(maxLen, len(player_data[player_key]))
    for player_notUpdated in player_data.keys():
        if len(player_data[player_notUpdated]) < maxLen:
            index = len(player_data[player_notUpdated])
            for x in range(maxLen - index):
                player_data[player_notUpdated].append('N/a')

    # pass types table
    table = soup.find('table', {'id': 'stats_passing_types_9'})
    rows = table.find_all('tr')
    start = 6
    maxLen = 0
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])
        player_row = [col.get_text(strip=True) for col in cols]

        player_name = player_row[0]
        player_key = player_name + "," + team_name

        for i in range(start, len(player_row) - 1):
            if player_row[i] != '':
                player_data[player_key].append(player_row[i])
            else:
                player_data[player_key].append('N/a')
        maxLen = max(maxLen, len(player_data[player_key]))
    for player_notUpdated in player_data.keys():
        if len(player_data[player_notUpdated]) < maxLen:
            index = len(player_data[player_notUpdated])
            for x in range(maxLen - index):
                player_data[player_notUpdated].append('N/a')

    # goal and shot creation table
    table = soup.find('table', {'id': 'stats_gca_9'})
    rows = table.find_all('tr')
    start = 5
    maxLen = 0
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])
        player_row = [col.get_text(strip=True) for col in cols]

        player_name = player_row[0]
        player_key = player_name + "," + team_name

        for i in range(start, len(player_row) - 1):
            if player_row[i] != '':
                player_data[player_key].append(player_row[i])
            else:
                player_data[player_key].append('N/a')
        maxLen = max(maxLen, len(player_data[player_key]))
    for player_notUpdated in player_data.keys():
        if len(player_data[player_notUpdated]) < maxLen:
            index = len(player_data[player_notUpdated])
            for x in range(maxLen - index):
                player_data[player_notUpdated].append('N/a')

    # defensive actions table
    table = soup.find('table', {'id': 'stats_defense_9'})
    rows = table.find_all('tr')
    start = 5
    maxLen = 0
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])
        player_row = [col.get_text(strip=True) for col in cols]

        player_name = player_row[0]
        player_key = player_name + "," + team_name

        for i in range(start, len(player_row) - 1):
            if player_row[i] != '':
                player_data[player_key].append(player_row[i])
            else:
                player_data[player_key].append('N/a')
        maxLen = max(maxLen, len(player_data[player_key]))
    for player_notUpdated in player_data.keys():
        if len(player_data[player_notUpdated]) < maxLen:
            index = len(player_data[player_notUpdated])
            for x in range(maxLen - index):
                player_data[player_notUpdated].append('N/a')

    # possession table
    table = soup.find('table', {'id': 'stats_possession_9'})
    rows = table.find_all('tr')
    start = 5
    maxLen = 0
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])
        player_row = [col.get_text(strip=True) for col in cols]

        player_name = player_row[0]
        player_key = player_name + "," + team_name

        for i in range(start, len(player_row) - 1):
            if player_row[i] != '':
                player_data[player_key].append(player_row[i])
            else:
                player_data[player_key].append('N/a')
        maxLen = max(maxLen, len(player_data[player_key]))
    for player_notUpdated in player_data.keys():
        if len(player_data[player_notUpdated]) < maxLen:
            index = len(player_data[player_notUpdated])
            for x in range(maxLen - index):
                player_data[player_notUpdated].append('N/a')

    # playing time table
    table = soup.find('table', {'id': 'stats_playing_time_9'})
    rows = table.find_all('tr')
    start = 9
    maxLen = 0
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])
        player_row = [col.get_text(strip=True) for col in cols]

        player_name = player_row[0]
        player_key = player_name + "," + team_name

        for i in range(start, len(player_row) - 4):
            if i == 18 or i == 19 or i == 20: continue
            if player_row[i] != '':
                player_data[player_key].append(player_row[i])
            else:
                player_data[player_key].append('N/a')
        maxLen = max(maxLen, len(player_data[player_key]))
    for player_notUpdated in player_data.keys():
        if len(player_data[player_notUpdated]) < maxLen:
            index = len(player_data[player_notUpdated])
            for x in range(maxLen - index):
                player_data[player_notUpdated].append('N/a')

    # miscellaneous table
    table = soup.find('table', {'id': 'stats_misc_9'})
    rows = table.find_all('tr')
    start = 8
    maxLen = 0
    for row in rows[2:len(rows) - 2]:
        cols = row.find_all(['th', 'td'])
        player_row = [col.get_text(strip=True) for col in cols]

        player_name = player_row[0]
        player_key = player_name + "," + team_name

        for i in range(start, len(player_row) - 1):
            if 12 <= i <= 15: continue
            if player_row[i] != '':
                player_data[player_key].append(player_row[i])
            else:
                player_data[player_key].append('N/a')
        maxLen = max(maxLen, len(player_data[player_key]))
    for player_notUpdated in player_data.keys():
        if len(player_data[player_notUpdated]) < maxLen:
            index = len(player_data[player_notUpdated])
            for x in range(maxLen - index):
                player_data[player_notUpdated].append('N/a')
    time.sleep(5)

player_list = []
for x, y in player_data.items():
    cur = [x.split(',')[0]] + y
    if cur[4] != 'N/a' and cur[7] != 'N/a' and (len(cur[7]) > 2 or int(cur[7]) > 90): player_list.append(cur)
player_list.sort(key=lambda p: (p[0].split()[0], -int(p[4])))
df = pd.DataFrame(player_list, columns=[
    'Player',
    'Nation',
    'Team',
    'Position',
    'Age',
    'Matches Played',
    'Starts',
    'Minutes',
    'non-Penalty Goals',
    'Penalty Goals',
    'Assists',
    'Yellow Cards',
    'Red Cards',
    'Expected xG',
    'Expected npxG',
    'Expected xAG',
    'Progression PrgC',
    'Progression PrgP',
    'Progression PrgR',
    'Per90Minutes Gls',
    'Per90Minutes Ast',
    'Per90Minutes G+A',
    'Per90Minutes G-PK',
    'Per90Minutes G+A-PK',
    'Per90Minutes xG',
    'Per90Minutes xAG',
    'Per90Minutes xG+xAG',
    'Per90Minutes npxG',
    'Per90Minutes npxG+xAG',
    'Goalkeeping_Performance GA',
    'Goalkeeping_Performance GA90',
    'Goalkeeping_Performance SoTA',
    'Goalkeeping_Performance Saves',
    'Goalkeeping_Performance Save%',
    'Goalkeeping_Performance W',
    'Goalkeeping_Performance D',
    'Goalkeeping_Performance L',
    'Goalkeeping_Performance CS',
    'Goalkeeping_Performance CS%',
    'Goalkeeping_PenaltyKicks PKAtt',
    'Goalkeeping_PenaltyKicks PKA',
    'Goalkeeping_PenaltyKicks PKsv',
    'Goalkeeping_PenaltyKicks PKm',
    'Goalkeeping_PenaltyKicks Save%',
    'Shooting_Standard Gls',
    'Shooting_Standard Sh',
    'Shooting_Standard SoT',
    'Shooting_Standard SoT%',
    'Shooting_Standard Sh/90',
    'Shooting_Standard SoT/90',
    'Shooting_Standard G/Sh',
    'Shooting_Standard G/SoT',
    'Shooting_Standard Dist',
    'Shooting_Standard FK',
    'Shooting_Standard PK',
    'Shooting_Standard PKatt',
    'Shooting_Expected xG',
    'Shooting_Expected npxG',
    'Shooting_Expected npxG/Sh',
    'Shooting_Expected G-xG',
    'Shooting_Expected np:G-xG',
    'Passing_Total Cmp',
    'Passing_Total Att',
    'Passing_Total Cmp%',
    'Passing_Total TotDist',
    'Passing_Total PrgDist',
    'Passing_Short Cmp',
    'Passing_Short Att',
    'Passing_Short Cmp%',
    'Passing_Medium Cmp',
    'Passing_Medium Att',
    'Passing_Medium Cmp%',
    'Passing_Long Cmp',
    'Passing_Long Att',
    'Passing_Long Cmp%',
    'Passing_Expected Ast',
    'Passing_Expected xAG',
    'Passing_Expected xA',
    'Passing_Expected A-xAG',
    'Passing_Expected KP',
    'Passing_Expected 1/3',
    'Passing_Expected PPA',
    'Passing_Expected CrsPA',
    'Passing_Expected PrgP',
    'PassTypes_PassTypes Live',
    'PassTypes_PassTypes Dead',
    'PassTypes_PassTypes FK',
    'PassTypes_PassTypes TB',
    'PassTypes_PassTypes Sw',
    'PassTypes_PassTypes Crs',
    'PassTypes_PassTypes TI',
    'PassTypes_PassTypes CK',
    'PassTypes_CornerKicks In',
    'PassTypes_CornerKicks Out',
    'PassTypes_CornerKicks Str',
    'PassTypes_Outcomes Cmp',
    'PassTypes_Outcomes Off',
    'PassTypes_Outcomes Blocks',
    'GoalAndShotCreation_SCA SCA',
    'GoalAndShotCreation_SCA SCA90',
    'GoalAndShotCreation_SCATypes PassLive',
    'GoalAndShotCreation_SCATypes PassDead',
    'GoalAndShotCreation_SCATypes TO',
    'GoalAndShotCreation_SCATypes Sh',
    'GoalAndShotCreation_SCATypes Fld',
    'GoalAndShotCreation_SCATypes Def',
    'GoalAndShotCreation_GCA GCA',
    'GoalAndShotCreation_GCA GCA90',
    'GoalAndShotCreation_GCATypes PassLive',
    'GoalAndShotCreation_GCATypes PassDead',
    'GoalAndShotCreation_GCATypes TO',
    'GoalAndShotCreation_GCATypes Sh',
    'GoalAndShotCreation_GCATypes Fld',
    'GoalAndShotCreation_GCATypes Def',
    'DefensiveActions_Tackles Tkl',
    'DefensiveActions_Tackles TklW',
    'DefensiveActions_Tackles Def 3rd',
    'DefensiveActions_Tackles Mid 3rd',
    'DefensiveActions_Tackles Att 3rd',
    'DefensiveActions_Challenges Tkl',
    'DefensiveActions_Challenges Att',
    'DefensiveActions_Challenges Tkl%',
    'DefensiveActions_Challenges Lost',
    'DefensiveActions_Blocks Blocks',
    'DefensiveActions_Blocks Sh',
    'DefensiveActions_Blocks Pass',
    'DefensiveActions_Blocks Int',
    'DefensiveActions_Blocks Tkl + Int',
    'DefensiveActions_Blocks Clr',
    'DefensiveActions_Blocks Err',
    'Possession_Touches Touches',
    'Possession_Touches Def Pen',
    'Possession_Touches Def 3rd',
    'Possession_Touches Mid 3rd',
    'Possession_Touches Att 3rd',
    'Possession_Touches Att Pen',
    'Possession_Touches Live',
    'Possession_TakeOns Att',
    'Possession_TakeOns Succ',
    'Possession_TakeOns Succ%',
    'Possession_TakeOns Tkld',
    'Possession_TakeOns Tkld%',
    'Possession_Carries Carries',
    'Possession_Carries TotDist',
    'Possession_Carries PrgDist',
    'Possession_Carries PrgC',
    'Possession_Carries 1/3',
    'Possession_Carries CPA',
    'Possession_Carries Mis',
    'Possession_Carries Dis',
    'Possession_Receiving Rec',
    'Possession_Receiving PrgR',
    'PlayingTime_Starts Starts',
    'PlayingTime_Starts Mn/Start',
    'PlayingTime_Starts Compl',
    'PlayingTime_Subs Subs',
    'PlayingTime_Subs Mn/Sub',
    'PlayingTime_Subs unSub',
    'PlayingTime_TeamSuccess PPM',
    'PlayingTime_TeamSuccess onG',
    'PlayingTime_TeamSuccess onGA',
    'PlayingTime_TeamSuccess_xG onxG',
    'PlayingTime_TeamSuccess_xG onxGA',
    'MiscellaneousStats_Performance Fls',
    'MiscellaneousStats_Performance Fld',
    'MiscellaneousStats_Performance Off',
    'MiscellaneousStats_Performance Crs',
    'MiscellaneousStats_Performance OG',
    'MiscellaneousStats_Performance Recov',
    'MiscellaneousStats_AerialDuels Won',
    'MiscellaneousStats_AerialDuels Lost',
    'MiscellaneousStats_AerialDuels Won%'
])

print(df)
df.to_csv('results.csv')
