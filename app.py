import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df1=pd.read_csv('IPL_Ball_by_Ball_2008_2022.csv')
df2=pd.read_csv('IPL_Matches_2008_2022.csv')
df=df1.merge(df2,on='ID',how='left')
# data cleaning
df.replace(to_replace='Rising Pune Supergiants',value='Rising Pune Supergiant',inplace=True)
df.replace(to_replace='Delhi Daredevils',value='Delhi Capitals',inplace=True)
df.replace(to_replace='Kings XI Punjab',value='Punjab Kings',inplace=True)
df2.replace(to_replace='Rising Pune Supergiants',value='Rising Pune Supergiant',inplace=True)
df2.replace(to_replace='Delhi Daredevils',value='Delhi Capitals',inplace=True)
df2.replace(to_replace='Kings XI Punjab',value='Punjab Kings',inplace=True)
df['extra_type']=df['extra_type'].fillna('legal delivery')
df['player_out'] = df['player_out'].fillna('no wicket')
df['kind'] = df['kind'].fillna('dot ball')
df['fielders_involved'] =df['fielders_involved'].fillna('no')
df['Margin'] =df['Margin'].fillna(0)
df2['Margin'] =df2['Margin'].fillna(0)
# adding 1 column named as losingteam
df2['losing_team'] = df2.apply(lambda row: row['Team2'] if row['WinningTeam'] == row['Team1'] else row['Team1'], axis=1)
# extracting all the players name from Team1Players

data=df2['Team1Players']

# Concatenate all strings into one string
all_data = ','.join(data)

# Remove square brackets, single quotes, and leading/trailing spaces
cleaned_data = all_data.replace("[", "").replace("]", "").replace("'", "").strip()

# Split the string into a list of player names
player_names_list = cleaned_data.split(',')
cleaned_player_names = [name.strip() for name in player_names_list]
# extracting all the players name from Team2Players
data1= df2['Team2Players']
# Provided data

# Concatenate all strings into one string
all_data1 = ','.join(data1)

# Remove square brackets, single quotes, and leading/trailing spaces
cleaned_data1 = all_data1.replace("[", "").replace("]", "").replace("'", "").strip()

# Split the string into a list of player names
player_names_list1 = cleaned_data1.split(',')
cleaned_player_names1 = [name.strip() for name in player_names_list1]
# now concatenating both the player list and extract unique name
unique_players = sorted(set(cleaned_player_names + cleaned_player_names1))

def load_player_details(player):
    st.title(player)
    if df['batter'].isin([player]).sum() >= 1:
        runs = df.groupby('batter')['batsman_run'].sum()[player]
    else:
        runs = 0
    if df[df['kind']=='caught']['fielders_involved'].isin([player]).sum()>=1:
        catch = df[df['kind'] == 'caught'].groupby('fielders_involved')['ID'].count()[player]
    else:
        catch = 0

    if df[df['kind']=='run out']['fielders_involved'].isin([player]).sum()>=1:
        run_out = df[df['kind'] == 'run out'].groupby('fielders_involved')['ID'].count()[player]
    else:
        run_out = 0

    if df['bowler'].isin([player]).sum() >= 1:
        wicket = df[df['kind'].isin(['caught','bowled','lbw','stumped','caught and bowled','hit wicket','dot ball'])].groupby('bowler')['isWicketDelivery'].sum()[player]
    else:
        wicket = 0

    if df2['Player_of_Match'].isin([player]).sum() >= 1:
        mvp = df2['Player_of_Match'].value_counts()[player]
    else:
        mvp = 0

    if df['batter'].isin([player]).sum() >= 1:
        total_runs = df.groupby('batter')['batsman_run'].sum()[player]
        df_without_noball = df[df['extra_type'] != 'noballs']
        df_without_noball_and_wides = df_without_noball[df_without_noball['extra_type'] != 'wides']
        ball_faced = df_without_noball_and_wides.groupby('batter')['extra_type'].count()[player]
        strikerate = round((total_runs / ball_faced) * 100, 2)
    else:
        strikerate = 0


    if df[df['batsman_run'] == 6]['batter'].isin([player]).sum() >= 1:
        df_6 = df[df['batsman_run'] == 6]
        total_six = df_6.groupby('batter')['batsman_run'].count()[player]
    else:
        total_six=0

    if df[df['batsman_run'] == 6]['batter'].isin([player]).sum() >= 1:
        df_4 = df[df['batsman_run'] == 4]
        total_four = df_4.groupby('batter')['batsman_run'].count()[player]
    else:
        total_four=0

    st.subheader('_Player_ _Statistics_',divider='rainbow')
    st.metric('Total Runs',runs)
    st.metric('Strike Rate',strikerate)
    st.metric('Total Six',total_six)
    st.metric('Total Four', total_four)
    st.metric('Total Wickets ',wicket)
    st.metric('Total Catches ',catch)
    st.metric('Total No of Runouts ',run_out)
    st.metric('Man of the match awards',mvp)

    if df['batter'].isin([player]).sum() >= 1:
        season_player_runs = df.groupby(['Season', 'batter'])['batsman_run'].sum().reset_index()
        season_player_pivot = season_player_runs.pivot(index='Season', columns='batter', values='batsman_run').fillna(0)
        a=season_player_pivot[player].sort_values(ascending=False).head()
        #plot = sns.barplot(x=a.index, y=a)

        st.subheader('Top 5 best seasons with bat',divider='violet')
        st.bar_chart(a)
    else:
        pass

    if df['bowler'].isin([player]).sum() >= 1:
        season_player_wicket = df[df['isWicketDelivery'] == 1 & df['kind'].isin(
            ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket', 'dot'])]
        season_player_wicket1 = season_player_wicket.groupby(['Season', 'bowler'])['isWicketDelivery'].sum().reset_index()
        season_player_wicket_pivot = season_player_wicket1.pivot(index='Season', columns='bowler',
                                                                 values='isWicketDelivery').fillna(0)
        b = season_player_wicket_pivot[player].sort_values(ascending=False).head()

        st.subheader('Top 5 best seasons with bowl', divider='violet')
        st.bar_chart(b)
    else:
        pass


def load_overall_analysis():
    st.title('Overall IPL Analysis')
    st.image('ipl-trophy.jpg')
    st.write("""
            The Indian Premier League (IPL) (also known as the TATA IPL for sponsorship reasons) is a men's Twenty20 (T20) cricket league that is annually held in India. The league is contested by ten city-based franchise teams.The BCCI founded the league in 2007. The competition is usually held in summer between March and May every year. It has an exclusive window in the ICC Future Tours Programme due to fewer international cricket tours happening during IPL seasons worldwide.
            The IPL is the most-popular cricket league in the world; in 2014, it was ranked sixth by average attendance among all sports leagues.[6] In 2010, the IPL became the first sporting event to be broadcast live on YouTube.Other Indian sports leagues have been established based on the success of the IPL.The brand value of the league in 2022 was ₹90,038 crore. According to BCCI, the 2015 IPL season contributed ₹1,150 crore to the GDP of the economy of India.In December 2022, the IPL became a decacorn valued at 10.9 billion , registering a 75% growth in dollar terms since 2020 when it was valued at 6.2 billion, according to a report by consulting firm D and P Advisory.
            """)

    top_5_df = df2[df2['WonBy'] == 'Runs'].sort_values('Margin', ascending=False,ignore_index=True).head()[['Date','WinningTeam','losing_team', 'Margin']]
    st.subheader('Top 5 highest wins while defending',divider='violet')
    st.dataframe(top_5_df,column_config={'losing_team':'LosingTeam'})

    chase_overall = df2[df2['WonBy'] == 'Wickets'].sort_values('Margin', ascending=False,ignore_index=True).head()[['Date','WinningTeam','losing_team', 'Margin']]
    st.subheader('Top 5 highest wins while chasing',divider='violet')
    st.dataframe(chase_overall,column_config={'losing_team':'LosingTeam'})

    col3,col4= st.columns(2)
    with col3:

        top5_batter = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False)[0:5]
        st.subheader('Top 5 batsman of IPL',divider='violet')
        st.dataframe(top5_batter,column_config={'batter':'Batsman','batsman_run':'Runs'})

    with col4:

        top5_bowler = df[df['kind'].isin(['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket'])].groupby('bowler')[
        'isWicketDelivery'].sum().sort_values(ascending=False)[0:5]
        st.subheader('Top Bowler of IPL', divider='violet')
        st.dataframe(top5_bowler,column_config={'bowler':'Bowler','isWicketDelivery':'Wickets'})


    col1,col2= st.columns(2)
    with col1:
        finals = df2[df2['MatchNumber'] == "Final"]
        winners = finals[['Season', 'WinningTeam']].sort_values('Season', ignore_index=True)
        st.subheader('IPL Winners',divider='violet')
        st.dataframe(winners)
    with col2:
        top_2_teams=finals['WinningTeam'].value_counts().head(2)
        st.subheader('Top 2 most successful teams',divider='violet')
        st.dataframe(top_2_teams)

    final_matches = df2[df2['MatchNumber']=='Final']
    final_winners = final_matches['WinningTeam'].value_counts().sort_values(ascending=False)
    st.subheader('IPL Final Winners',divider='violet')
    st.bar_chart(final_winners)


    overall_mvp=df2['Player_of_Match'].value_counts().sort_values(ascending=False)[0:5]
    st.subheader('Top 5 players with most man of the match awards',divider='violet')
    st.dataframe(overall_mvp,column_config={'Player_of_Match':'Player'})


    st.subheader('Total number of matches played by each team',divider='violet')
    st.bar_chart(df2['Team1'].value_counts()+df2['Team2'].value_counts())

    st.markdown("""
    ### Insights from Overall Analysis
    - Mumbai Indians has won with the highest margin of 146 runs while defending
    - Royal Challengers Bangalore has 3 highest margin in top 5 margins while defensing and chasing as well
    - Total 15 Teams has played till now in 14 seasons of IPL
    - Mumbai Indians has played most number of matches
    - Mumbai Indians has won most number of seasons till now(5) followed by Chennai Super Kings (4)
    - AB de Villiers has won the most Player of the Match award - 25
    
    
    
    
    """)
def load_team_details(team):
    st.title(team)
    if team == 'Chennai Super Kings':
        st.image('CSK.webp')
    elif team == 'Deccan Chargers':
        st.image('Deccan Chargers.webp')
    elif team == 'Delhi Capitals':
        st.image('DC.webp')
    elif team == 'Gujarat Lions':
        st.image('Gujrat Lions.webp')
    elif team == 'Gujarat Titans':
        st.image('GujratTitans.webp')
    elif team == 'Kochi Tuskers Kerala':
        st.image('Kochi Tuskers.webp')
    elif team == 'Kolkata Knight Riders':
        st.image('KKR.webp')
    elif team == 'Lucknow Super Giants':
        st.image('LSG.webp')
    elif team == 'Mumbai Indians':
        st.image('MI.webp')
    elif team == 'Pune Warriors':
        st.image('Sahara Pune.webp')
    elif team == 'Punjab Kings':
        st.image('Punjab.webp')
    elif team == 'Rajasthan Royals':
        st.image('RR.webp')
    elif team == 'Rising Pune Supergiant':
        st.image('Rising pune.webp')
    elif team == 'Royal Challengers Bangalore':
        st.image('RCB new.webp')
    else:
        st.image('SRH.webp')


    total_no_of_matches = df2[df2['Team1'].isin([team]) | df2['Team2'].isin([team])][
        'MatchNumber'].count()
    wins = df2[df2['WinningTeam'] == team]['MatchNumber'].count()
    win_percentage = round((wins / total_no_of_matches) * 100, 2)
    total_wins = df2[df2['WinningTeam'] == team]
    defend= total_wins[total_wins['WonBy'] == 'Runs']['MatchNumber'].count()
    chase = total_wins[total_wins['WonBy'] == 'Wickets']['MatchNumber'].count()
    superover_wins = total_wins[total_wins['SuperOver'] == 'Y']['MatchNumber'].count()
    st.metric('Total matches played',total_no_of_matches)
    st.metric('Total wins',wins)
    st.metric('Total wins while chasing',chase)
    st.metric('Total wins while defending',defend)
    st.metric('Super Over wins',superover_wins)
    st.metric('Winning Percentage',win_percentage)

    top5_wins = df2[df2['WinningTeam'] == team].sort_values(by='Margin', ascending=False,
                                                                       ignore_index=True).head()
    top5_winsdf = top5_wins[['Date','WinningTeam','losing_team','Margin']]
    st.subheader('Top 5 wins while defending',divider='violet')
    st.dataframe(top5_winsdf,column_config={'losing_team':'LosingTeam'})

    chase_wins = df2[(df2['WinningTeam'] == team) & (df2['WonBy'] == 'Wickets')].sort_values(by='Margin',
                                                                                             ascending=False,
                                                                                             ignore_index=True).head()
    chase_winsdf = chase_wins[['Date', 'WinningTeam', 'losing_team', 'Margin']]
    st.subheader('Top 5 wins while chasing',divider='violet')
    st.dataframe(chase_winsdf,column_config={'losing_team':'LosingTeam'})

    a = df2[df2['TossWinner'] == team]
    xy = a[a['TossDecision'] == 'bat']
    abcd = df2[df2['Team1'].isin([team]) | df2['Team2'].isin([team])]
    b = abcd[abcd['TossWinner'] != team]
    yz = b[b['TossDecision'] == 'field']
    xyz = pd.concat([xy, yz], ignore_index=True)
    xyz['winner1'] = xyz.apply(lambda i: team if i['WinningTeam'] == team else 'others',
                               axis=1)

    cd = df2[df2['TossWinner'] == team]
    ba = cd[cd['TossDecision'] == 'bowl']
    efgh = df2[df2['Team1'].isin([team]) | df2['Team2'].isin([team])]
    mn = efgh[efgh['TossWinner'] != team]
    pq = mn[mn['TossDecision'] == 'bat']
    sp = pd.concat([ba, pq], ignore_index=True)
    sp['winner1'] = sp.apply(lambda i: team if i['WinningTeam'] == team else 'others',
                             axis=1)
    col7, col8 = st.columns(2)

    with col7:

        st.subheader('Winning percentage while defending')
        fig, ax = plt.subplots()
        ax.pie(
            xyz['winner1'].value_counts(),
            autopct="%1.1f%%",
            explode=(0, 0.1),
            labels=xyz['winner1'].value_counts().index,
            colors=['purple', 'lightcoral']
        )
        ax.axis('equal')
        st.pyplot(fig)

    with col8:
        st.subheader('Winning percentage while chasing')
        fig, ax = plt.subplots()
        ax.pie(
            sp['winner1'].value_counts(),
            autopct="%1.1f%%",
            explode=(0, 0.1),
            labels=sp['winner1'].value_counts().index,
            colors=['purple', 'lightcoral']
        )
        ax.axis('equal')
        st.pyplot(fig)

    col1,col2=st.columns(2)
    with col1:

        total_no_of_matches_overall = df[df['Team1'].isin([team]) | df['Team2'].isin([team])]
        top5_bowlerteam=total_no_of_matches_overall[total_no_of_matches_overall['kind'].isin(
            ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket'])].groupby('bowler')[
            'isWicketDelivery'].sum().sort_values(ascending=False)[0:5]
        st.subheader('Top 5 Bowler', divider='violet')
        st.dataframe(top5_bowlerteam,column_config={'bowler':'Bowler','isWicketDelivery':'Wickets'})

    with col2:
        top5_batterteam = total_no_of_matches_overall.groupby('batter')['batsman_run'].sum().sort_values(
            ascending=False)[0:5]
        st.subheader('Top 5 Batsman', divider='violet')
        st.dataframe(top5_batterteam,column_config={'batter':'Batsman','batsman_run':'Runs'})


    mvp_team = df2[df2['WinningTeam'] == team]['Player_of_Match'].value_counts().head()
    st.subheader('Top 5 player who won most number of man of the match awards',divider='violet')
    st.dataframe(mvp_team,column_config={'Player_of_Match':'Player'})

    df3 = df2[df2['TossWinner'] == team]
    df3['winner'] = df3.apply(lambda i: team if i['WinningTeam'] == team else 'Other',
                          axis=1)
    abc = df2[
        df2['Team1'].isin([team]) | df2['Team2'].isin([team])]
    df4 = abc[abc['TossWinner'] != team]
    df4['winner'] = df4.apply(
        lambda i: team if i['WinningTeam'] == team else 'Other',
        axis=1)
    col5,col6 = st.columns(2)
    with col5:
        st.subheader('Winning percentage while winning the toss')
        fig, ax = plt.subplots()
        ax.pie(
            df3['winner'].value_counts(),
            autopct="%1.1f%%",
            explode=(0, 0.1),
            labels=df3['winner'].value_counts().index,
            colors=['purple', 'lightcoral']
        )
        ax.axis('equal')
        st.pyplot(fig)

    with col6:
        st.subheader('Winning percentage while losing the toss')
        fig, ax = plt.subplots()
        ax.pie(
            df4['winner'].value_counts(),
            autopct="%1.1f%%",
            explode=(0, 0.1),
            labels=df4['winner'].value_counts().index,
            colors=['purple', 'lightcoral']
        )
        ax.axis('equal')
        st.pyplot(fig)






st.sidebar.title('IPL Analysis')
option = st.sidebar.selectbox('Select One',['Team','Player','Overall Analysis'])

if option == 'Overall Analysis':
    btn0 = st.sidebar.button('Show Overall Analysis')
    if btn0:
        load_overall_analysis()



elif option =='Team':
    selected_team = st.sidebar.selectbox('Select Team',sorted(df['Team1'].unique().tolist()))
    btn1=st.sidebar.button('Find Team Details')
    if btn1:
        load_team_details(selected_team)


else:
    selected_player= st.sidebar.selectbox('Select Player', unique_players)
    btn2=st.sidebar.button('Find Player Details')
    if btn2:
        load_player_details(selected_player)

