#Exploratory Data Analysis on IPL data collected from 2008-2019 
!wget https://github.com/Bhavan-Naik/TSF_GRIP-IPL_EDA/raw/main/Indian%20Premier%20League.zip
!unzip "Indian Premier League.zip"

#Import Libraries and Read Data
print("The conclusions in this project are based on data in the IPL from 2008-2019")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

#Read Data
matches=pd.read_csv("matches.csv")
all_deliveries=pd.read_csv("deliveries.csv")

print("Teams:\n",(matches["team1"]).unique())

#Data Cleaning
matches["team1"].replace({"Rising Pune Supergiant": "Rising Pune Supergiants", "Delhi Capitals": "Delhi Daredevils", "Sunrisers Hyderabad": "SunRisers Hyderabad", "Pune Warriors":"Pune Warriors India"}, inplace=True)
matches["team2"].replace({"Rising Pune Supergiant": "Rising Pune Supergiants", "Delhi Capitals": "Delhi Daredevils", "Sunrisers Hyderabad": "SunRisers Hyderabad", "Pune Warriors":"Pune Warriors India"}, inplace=True)
matches["winner"].replace({"Rising Pune Supergiant": "Rising Pune Supergiants", "Delhi Capitals": "Delhi Daredevils", "Sunrisers Hyderabad": "SunRisers Hyderabad", "Pune Warriors":"Pune Warriors India"}, inplace=True)
matches["toss_winner"].replace({"Rising Pune Supergiant": "Rising Pune Supergiants", "Delhi Capitals": "Delhi Daredevils", "Sunrisers Hyderabad": "SunRisers Hyderabad", "Pune Warriors":"Pune Warriors India"}, inplace=True)
teams=matches["team1"].unique()
teams.sort()
#To consider only the main 8 teams, uncomment the next line:
#teams=["Chennai Super Kings","Delhi Daredevils","Kings XI Punjab","Kolkata Knight Riders","Mumbai Indians","Rajasthan Royals","Royal Challengers Bangalore","SunRisers Hyderabad"]
print("Teams:\n",(teams))

#Assign Short-Forms of Teams
teams_1=[]
for i in teams:
    teams_1.append(''.join([c for c in i if c.isupper()]))
print(teams_1)

#Assigning Colors to Teams
if len(teams_1)==8:
  cols=['#F9CD05','#282968','#DC143C','#3A225D','#004BA0','#FFC0CB','#FF0000','#FF822A']
  edge=['#1D418C','#C02826','#A7A9AC','#B3A123','#D1AB3E','#254AA5','#000000','#000000']
else:
  cols=['#F9CD05','#366293','#282968','#E04F16','#DC143C','#FF4500','#3A225D','#004BA0','#2F9BE3','#FFC0CB','#D11D9B','#FF0000','#FF822A']
  edge=['#1D418C','#D9E3EF','#C02826','#18089C','#A7A9AC','#7F3F98','#B3A123','#D1AB3E','#C0D6EB','#254AA5','#FF8209','#000000','#000000']

#Finding the most successful team
winners=matches[matches["season"].diff(-1)!=0].sort_values(by="season")
trophies_won=[]
for i in teams:
  trophies_won.append(winners["winner"].str.count(i).sum())
print(trophies_won)

#Most Successful Team in terms of Trophies Won
success=dict(zip(teams,trophies_won))
success=dict(sorted(success.items(), key=lambda x: x[1], reverse=True))
print("Trophies Won by Teams:")
print("{:<30} {:<30}".format('TEAM', 'TROPHIES'))
for key, value in success.items():
  if value!=0:
    print("{:<30} {:<30}".format(key, value))

plt.bar(teams_1,trophies_won,color=cols,edgecolor=edge)

successful=next(iter((success.items())))
print("The Most Successful Team is **"+successful[0]+"**\nThey have won "+str(successful[1])+" IPL trophies.")

#Count number of Home Matches
home_matches_count=[]
for i in teams:
  home_matches_count.append(matches['team1'].str.count(str(i)).sum())
print(home_matches_count)

#Count number of Away Matches
away_matches_count=[]
for i in teams:
  away_matches_count.append((matches['team2'].str.count(i).sum()))
print(away_matches_count)

#Add both arrays to find Total Matches
total_matches=[]
for i in range(len(teams)):
  total_matches.append(home_matches_count[i]+away_matches_count[i])
print(total_matches)

#Count number of Matches Won
won_matches_count=[]
for i in teams:
  won_matches_count.append(matches['winner'].str.count(i).sum())
print(won_matches_count)

#Winning percentage of each team
winning_percentage=[]
for i in range(len(teams)):
  winning_percentage.append(float('{0:.4g}'.format(won_matches_count[i]*100/total_matches[i])))
print(winning_percentage)

#Overall Records
overall=dict(zip(teams,winning_percentage))
overall=dict(sorted(overall.items(), key=lambda x: x[1], reverse=True))
print("Overall Winning Percentage for Teams:")
print("{:<30} {:<30}".format('TEAM', 'WIN %'))
for key, value in overall.items():
  print("{:<30} {:<30}".format(key, value))

plt.bar(teams_1,winning_percentage,color=cols,edgecolor=edge)

consistent=next(iter((overall.items())))
print("The Most Consistent Team is: **"+consistent[0]+"** \nWith win percentage of "+str(consistent[1])+" overall.")

#Super Overs Records for Teams
super_overs=matches[matches["result"]=="tie"]
total_super_overs_played=[]
super_overs_won=[]
for i in teams:
  total_super_overs_played.append(len(super_overs[(super_overs["team1"]==i) | (super_overs["team2"]==i)]))
  super_overs_won.append(len(super_overs[super_overs["winner"]==i]))
print(total_super_overs_played)
print(super_overs_won)

#Super Over Win Percentage
super_over_percentage=[]
super_over_teams=[]
super_over_abb=[]
super_over_cols=[]
super_over_edge=[]
for i in range(len(teams)):
  if total_super_overs_played[i]!=0:
    super_over_percentage.append(float('{0:.4g}'.format(super_overs_won[i]*100/total_super_overs_played[i])))
    super_over_teams.append(teams[i])
    super_over_abb.append(teams_1[i])
    super_over_cols.append(cols[i])
    super_over_edge.append(edge[i])
print(super_over_percentage)

#Super Over Records
super_over_records=dict(zip(super_over_teams,super_over_percentage))
super_over_records=dict(sorted(super_over_records.items(), key=lambda x: x[1], reverse=True))
print("Super Overs Winning Percentage for Teams:")
print("{:<30} {:<30}".format('TEAM', 'WIN %'))
for key, value in super_over_records.items():
  print("{:<30} {:<30}".format(key, value))

plt.bar(super_over_abb,super_over_percentage,color=super_over_cols,edgecolor=super_over_edge)

sup=[]
for i in range(len(super_over_percentage)):
  if super_over_percentage[i]==100:
    sup.append(super_over_teams[i])
print("Two teams have "+str(max(super_over_percentage))+"% win ratio in super overs.\nThey are: "+str(sup[0])+" and "+str(sup[1])+".")

#Count number of Home Matches Won
home_matches_won=[]
for i in teams:
  df_i=matches[matches["team1"]==i]
  home_matches_won.append(df_i["winner"].str.count(i).sum())
print(home_matches_won)

#Home Winning Percentage
home_win_percentage=[]
for i in range(len(teams)):
  home_win_percentage.append(float('{0:.4g}'.format(home_matches_won[i]*100/home_matches_count[i])))
print(home_win_percentage)

#Home Records
home_records=dict(zip(teams,home_win_percentage))
home_records=dict(sorted(home_records.items(), key=lambda x: x[1], reverse=True))
print("Home Winning Records for Teams:")
print("{:<30} {:<30}".format('TEAM', 'HOME WIN %'))
for key, value in home_records.items():
  print("{:<30} {:<30}".format(key, value))

plt.bar(teams_1,home_win_percentage,color=cols,edgecolor=edge)

fortress=next(iter((home_records.items())))
print("Best Team at Home: **"+fortress[0]+"** \nWith win percentage of "+str(fortress[1])+" when they play at home.")

#Count number of Away Matches Won
away_matches_won=[]
for i in teams:
  df_i=matches[matches["team2"]==i]
  away_matches_won.append(df_i["winner"].str.count(i).sum())
print(away_matches_won)

#Away Winning Percentage
away_win_percentage=[]
for i in range(len(teams)):
  away_win_percentage.append(float('{0:.4g}'.format(away_matches_won[i]*100/away_matches_count[i])))
print(away_win_percentage)

#Away Records
away_records=dict(zip(teams,away_win_percentage))
away_records=dict(sorted(away_records.items(), key=lambda x: x[1], reverse=True))
print("Away Winning Records for Teams:")
print("{:<30} {:<30}".format('TEAM', 'AWAY WIN %'))
for key, value in away_records.items():
  print("{:<30} {:<30}".format(key, value))

plt.bar(teams_1,away_win_percentage,color=cols,edgecolor=edge)

attacker=next(iter((away_records.items())))
print("Best Touring Team: **"+attacker[0]+"** \nWith win percentage of "+str(attacker[1])+" when they are the visiting team.")

#Count Number of Toss Wins
toss_wins_count=[]
toss_and_match_wins=[]
for i in teams:
  df_i=matches[matches["toss_winner"]==i]
  toss_wins_count.append(len(df_i))
  toss_and_match_wins.append(df_i["winner"].str.count(i).sum())
print(toss_wins_count)
print(toss_and_match_wins)

#Toss Winning Percentage
toss_win_match_win_percentage=[]
for i in range(len(teams)):
  toss_win_match_win_percentage.append(float('{0:.4g}'.format(toss_and_match_wins[i]*100/toss_wins_count[i])))
print(toss_win_match_win_percentage)

#Toss Win Records
toss_win_records=dict(zip(teams,toss_win_match_win_percentage))
toss_win_records=dict(sorted(toss_win_records.items(), key=lambda x: x[1], reverse=True))
print("Toss Win and Match Win Records for Teams:")
print("{:<30} {:<30}".format('TEAM', 'TOSS WIN MATCH WIN %'))
for key, value in toss_win_records.items():
  print("{:<30} {:<30}".format(key, value))

plt.bar(teams_1,toss_win_match_win_percentage,color=cols,edgecolor=edge)

win_toss=next(iter((toss_win_records.items())))
print("The team which is most likely to win if they win the toss is: **"+win_toss[0]+"**\nWith a win percentage of "+str(win_toss[1])+" when they win the toss.")

#Count Number of Toss Loss
toss_loss_count=[0]*len(teams)
toss_loss_and_match_wins=[0]*len(teams)
for i in range(len(teams)):
  toss_loss_count[i]=total_matches[i]-toss_wins_count[i]
  toss_loss_and_match_wins[i]=won_matches_count[i]-toss_and_match_wins[i]
print(toss_loss_count)
print(toss_loss_and_match_wins)

#Toss Lost and Match Win Percentage
toss_loss_match_win_percentage=[]
for i in range(len(teams)):
  toss_loss_match_win_percentage.append(float('{0:.4g}'.format(toss_loss_and_match_wins[i]*100/toss_loss_count[i])))
print(toss_loss_match_win_percentage)

#Toss Loss Records
toss_loss_records=dict(zip(teams,toss_loss_match_win_percentage))
toss_loss_records=dict(sorted(toss_loss_records.items(), key=lambda x: x[1], reverse=True))
print("Toss Loss but Match Win Records for Teams:")
print("{:<30} {:<30}".format('TEAM', 'TOSS LOSS MATCH WIN %'))
for key, value in toss_loss_records.items():
  print("{:<30} {:<30}".format(key, value))

plt.bar(teams_1, toss_loss_match_win_percentage,color=cols,edgecolor=edge)

lose_toss=next(iter((toss_loss_records.items())))
print("The team which is most likely to win if they win the toss is: **"+lose_toss[0]+"**\nWith a win percentage of "+str(lose_toss[1])+" when they lose the toss.")

#Count Number of First Batting Instances
total_bat_first_count=[]
bat_first_wins=[]
for i in teams:
  df_team=matches[(matches["team1"]==i) | (matches["team2"]==i)]
  df_i=df_team[((df_team["toss_winner"]==i) & (df_team["toss_decision"]=="bat"))] 
  df_j=df_team[((df_team["toss_winner"]!=i) & (df_team["toss_decision"]=="field"))]
  total_bat_first_count.append(len(df_i)+len(df_j))
  bat_first_wins.append(int(df_i["winner"].str.count(i).sum()+(df_j["winner"].str.count(i).sum())))
print(total_bat_first_count)
print(bat_first_wins)

#Batting First and Winning Percentage
bat_first_match_win_percentage=[]
for i in range(len(teams)):
  bat_first_match_win_percentage.append(float('{0:.4g}'.format(bat_first_wins[i]*100/total_bat_first_count[i])))
print(bat_first_match_win_percentage)

#Batting First Records
bat_first_records=dict(zip(teams,bat_first_match_win_percentage))
bat_first_records=dict(sorted(bat_first_records.items(), key=lambda x: x[1], reverse=True))
print("Batting First Win Records for Teams:")
print("{:<30} {:<30}".format('TEAM', 'BAT FIRST MATCH WIN %'))
for key, value in bat_first_records.items():
  print("{:<30} {:<30}".format(key, value))

plt.bar(teams_1,bat_first_match_win_percentage,color=cols,edgecolor=edge)

bat_first=next(iter((bat_first_records.items())))
print("The Best Target Defending Team is: **"+bat_first[0]+"**\nWith a win percentage of "+str(bat_first[1])+" when they bat first.")

#Count Number of Second Batting Instances
total_bat_second_count=[]
bat_second_wins=[]
for i in teams:
  df_team=matches[(matches["team1"]==i) | (matches["team2"]==i)]
  df_i=df_team[((df_team["toss_winner"]==i) & (df_team["toss_decision"]=="field"))]
  df_j=df_team[((df_team["toss_winner"]!=i) & (df_team["toss_decision"]=="bat"))]
  total_bat_second_count.append(len(df_i)+len(df_j))
  bat_second_wins.append(int(df_i["winner"].str.count(i).sum()+(df_j["winner"].str.count(i).sum())))
print(total_bat_second_count)
print(bat_second_wins)

#Batting Second and Winning Percentage
bat_second_match_win_percentage=[]
for i in range(len(teams)):
  bat_second_match_win_percentage.append(float('{0:.4g}'.format(bat_second_wins[i]*100/total_bat_second_count[i])))
print(bat_second_match_win_percentage)

#Batting Second Records
bat_second_records=dict(zip(teams,bat_second_match_win_percentage))
bat_second_records=dict(sorted(bat_second_records.items(), key=lambda x: x[1], reverse=True))
print("Batting Second Win Records for Teams:")
print("{:<30} {:<30}".format('TEAM', 'BAT SECOND MATCH WIN %'))
for key, value in bat_second_records.items():
  print("{:<30} {:<30}".format(key, value))

plt.bar(teams_1,bat_second_match_win_percentage,color=cols,edgecolor=edge)

bat_second=next(iter((bat_second_records.items())))
print("The Best Chasing Team is: **"+bat_second[0]+"**\nWith a win percentage of "+str(bat_second[1])+" when they chase a target.")

#Stats of players only during overs 1-20 is considered during their IPL careers
deliveries=all_deliveries[(all_deliveries["inning"]==1) | (all_deliveries["inning"]==2)]

#Total Batsmen
batsmen=deliveries["batsman"].unique()
print("Total Number of Batsmen: ",len(batsmen))

#Total Batsmen
bowlers=deliveries["bowler"].unique()
print("Total Number of Bowlers: ",len(bowlers))

#Total Balls faced by all Batsmen
balls_batted=[]
for i in batsmen:
  balls_batted.append([deliveries["batsman"].str.count(i).sum(),i])

#Total Runs scored by Top Batsmen
balls_batted.sort(reverse=True)
best_batsmen=balls_batted[0:25]
high_runs=[]
for i in best_batsmen:
  df_i=deliveries[deliveries["batsman"]==i[1]]
  high_runs.append([df_i["batsman_runs"].sum(),i[1]])

#Highest Runs List
high_runs.sort(reverse=True)
high_runs=high_runs[0:10]
high_runs_batsmen=[]
runs_scored=[]
print("Highest Run Scorers in IPL from 2008-2019:")
for i in high_runs:
  high_runs_batsmen.append(i[1])
  runs_scored.append(i[0])
  print(i)

plt.barh(high_runs_batsmen[::-1], runs_scored[::-1])

print("The Highest Run Scorer in IPL till 2019 is: "+str(high_runs[0][1])+" with "+str(high_runs[0][0])+" runs.")

#Total Balls bowled by All Bowlers
balls_bowled=[]
for i in bowlers:
  balls_bowled.append([deliveries["bowler"].str.count(i).sum(),i])

#Total Wickets taken by Top Bowlers
balls_bowled.sort(reverse=True)
best_bowlers=balls_bowled[0:25]
bowler_deliveries=deliveries[(deliveries["dismissal_kind"]=="caught") | (deliveries["dismissal_kind"]=="bowled") 
| (deliveries["dismissal_kind"]=="lbw") | (deliveries["dismissal_kind"]=="stumped") 
| (deliveries["dismissal_kind"]=="caught and bowled") | (deliveries["dismissal_kind"]=="hit wicket")]
high_wickets=[]
for i in best_bowlers:
  df_i=bowler_deliveries[bowler_deliveries["bowler"]==i[1]]
  high_wickets.append([df_i["dismissal_kind"].count().sum(),i[1]])

#Highest Wickets List
high_wickets.sort(reverse=True)
high_wickets=high_wickets[0:10]
high_wickets_bowlers=[]
wickets_taken=[]
print("Highest Wicket Takers in IPL from 2008-2019:")
for i in high_wickets:
  high_wickets_bowlers.append(i[1])
  wickets_taken.append(i[0])
  print(i)

plt.barh(high_wickets_bowlers[::-1],wickets_taken[::-1])

print("The Highest Wicket Taker in IPL till 2019 is: "+str(high_wickets[0][1])+" with "+str(high_wickets[0][0])+" wickets.")

#Total Number of Wicket Keepers
stumping_records=deliveries[deliveries["dismissal_kind"]=="stumped"]
keepers=stumping_records["fielder"].unique()
keepers=keepers.tolist()
keepers=[a for a in keepers if (isinstance(a,str))]
print("Total Number of Wicket Keepers: ",len(keepers))
print(keepers)

#Dismissal Records for Wicket Keepers
catch_records=deliveries[(deliveries["dismissal_kind"]=="caught") | (deliveries["dismissal_kind"]=="run out")]
keeping_total=[]
for i in range(len(keepers)):
  keeping_total.append([int((stumping_records["fielder"].str.count(str(keepers[i])).sum())+(catch_records["fielder"].str.count(str(keepers[i])).sum())),keepers[i]])
print("The Best Wicket-Keepers are: ")
keeping_total.sort(reverse=True)
best_keepers=keeping_total[0:10]
best_keeps=[]
keeps_total=[]
for i in best_keepers:
  keeps_total.append(i[0])
  best_keeps.append(i[1])
  print(i)

plt.barh(best_keeps[::-1],keeps_total[::-1])

print("The Best Wicket-Keeper in IPL till 2019 is: "+str(best_keepers[0][1])+" with "+str(best_keepers[0][0])+" dismissals.")

#Total Number of Fielders:
fielders=catch_records["fielder"].unique()
fielders=[a for a in fielders if (isinstance(a,str))]
for i in range(len(fielders)):
  if fielders[i].endswith("(sub)"):
    fielders[i]=fielders[i][:-6]
fielders=list(set(fielders))
fielders=[x for x in fielders if x not in keepers]
print("Total Number of Fielders: ",len(fielders))

#Catching Records for Fielders
catches_total=[]
for i in fielders:
  catches_total.append([int(catch_records["fielder"].str.contains(str(i)).sum()),i])
print("The Best Fielders are: ")
catches_total.sort(reverse=True)
best_fielders=catches_total[0:10]
best_fielders_1=[]
catches=[]
for i in best_fielders:
  catches.append(i[0])
  best_fielders_1.append(i[1])
  print(i)

plt.barh(best_fielders_1[::-1],catches[::-1])

print("The Best Fielder in IPL till 2019 is: "+str(best_fielders[0][1])+" with "+str(best_fielders[0][0])+" dismissals.")

#Calculating Batsman Stats for Each Year 
years=[2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
runs_per_year=[0]*12
batsman="V Kohli" #Enter batsman name here
bats_stats=deliveries[deliveries["batsman"]==batsman]
matches_batted=bats_stats["match_id"].unique()
match_runs=[]
for i in matches_batted:
  df_i=bats_stats[bats_stats["match_id"]==i]
  season_row=matches[matches["id"]==i]
  season=season_row.iloc[0]['season']
  season%=2008
  runs_per_year[season]+=df_i["batsman_runs"].sum()
plt.figure()
plt.title(batsman)
plt.bar(years,runs_per_year)
plt.show()

#Calculating Bowler Stats for Each Year
wickets_per_year=[0]*12
bowler="SL Malinga" #Enter bowler name here
bowler_stats=bowler_deliveries[bowler_deliveries["bowler"]==bowler]
matches_bowled=bowler_stats["match_id"].unique()
match_wickets=[]
for i in matches_bowled:
  df_i=bowler_stats[bowler_stats["match_id"]==i]
  season_row=matches[matches["id"]==i]
  season=season_row.iloc[0]['season']
  season%=2008
  wickets_per_year[season]+=len(df_i)
plt.figure()
plt.title(bowler)
plt.bar(years,wickets_per_year)
plt.show()

#Considering that we are a company that wants teams to endorse products
teams_eight=["Chennai Super Kings","Delhi Capitals","Kings XI Punjab","Kolkata Knight Riders","Mumbai Indians","Rajasthan Royals","Royal Challengers Bangalore","Sunrisers Hyderabad"]
endorse_teams=[]
endorse_teams.append(successful[0])
endorse_teams.append(consistent[0])
endorse_teams.append(fortress[0])
endorse_teams.append(attacker[0])
endorse_teams.append(win_toss[0])
endorse_teams.append(lose_toss[0])
endorse_teams=list(set(endorse_teams))
endorse_teams=[x for x in endorse_teams if x in teams_eight]

#Considering that we are a company that wants players to endorse products
endorse_players=[]
for i in range(0,5):
  endorse_players.append(high_runs_batsmen[i])
for i in range(0,5):
  endorse_players.append(high_wickets_bowlers[i])
for i in range(0,5):
  endorse_players.append(best_keeps[i])
for i in range(0,5):
  endorse_players.append(best_fielders_1[i])
endorse_players=list(set(endorse_players))

print("The Best Teams for endorsing products are: ")
for i in endorse_teams:
  print(i)
print("\nThe Best Players for endorsing products are: ")
endorse_players.sort()
for i in endorse_players:
  print(i)
