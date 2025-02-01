import pandas
import csv
import datetime
import random

def league_table():
    print("\n\nHere is the league table as it stands:\n")
    df = pandas.read_csv('table.csv')
    df = df.astype({"Games": 'int', "Wins": 'int', "Draws": 'int', "Losses": 'int'
                       , "GF": 'int', "GA": 'int', "Pts": 'int'})
    df['GD'] = df.GF - df.GA
    df = df.sort_values(by=['Pts','GD','GF'], ascending=False)
    df['Pos'] = df.reset_index().index + 1
    df.set_index('Pos', inplace=True)
    df = df[['Team', 'Games', 'Wins', 'Draws', 'Losses', 'GF', 'GA', 'GD', 'Pts']]
    print(df)

def archive():
    print("\n\nHere is a full list of all results from this league:\n")
    f = open('results.txt', 'r')
    results_archive = f.read()
    print(results_archive)

def get_goals(team_name):
    while True:
        user_input = input(f"How many goals did {team_name} score? ")
        try:
            value = int(user_input)
            if value >= 0:
                return value
            else:
                print("That's not a valid number of goals. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number of goals.")

def play_game():
    home = input("Who is the home team? Either choose a team from the league,\n"
                 "or type 'random' to get a team chosen at random: ").title()
    if home == 'Random':
        df = pandas.read_csv('table.csv')
        teams_list = df['Team'].tolist()
        home = random.choice(teams_list)
        print(f"{home} has been randomly chosen as the home team.")
    away = input("Who is the away team? Either choose a team from the league,\n"
                 "or type 'random' to get a team chosen at random: ").title()
    if away == 'Random':
        df = pandas.read_csv('table.csv')
        teams_list = df['Team'].tolist()
        teams_list.remove(home)
        away = random.choice(teams_list)
        print(f"{away} has been randomly chosen as the away team.")
    if home == away:
        print("Error: A team cannot play itself")
    else:
        home_goals = get_goals(home)
        away_goals = get_goals(away)
        result = f"{home} {home_goals}-{away_goals} {away}"
        check = input(f"{result}. Is this correct? Type y or n: ")
        if check == 'y':
            home_valid = False
            away_valid = False
            with open('table.csv', newline='') as f:
                reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
                data = list(reader)
                for i in data:
                    if i[0] == home:
                        home_valid = True
                        i[1] += 1
                        i[5] += home_goals
                        i[6] += away_goals
                        if home_goals > away_goals:
                            i[2] += 1
                            i[7] += 3
                        elif home_goals < away_goals:
                            i[4] += 1
                        elif away_goals == home_goals:
                            i[3] += 1
                            i[7] += 1
                    if i[0] == away:
                        away_valid = True
                        i[1] += 1
                        i[5] += away_goals
                        i[6] += home_goals
                        if away_goals > home_goals:
                            i[2] += 1
                            i[7] += 3
                        elif away_goals < home_goals:
                            i[4] += 1
                        elif away_goals == home_goals:
                            i[3] += 1
                            i[7] += 1
                if home_valid == True and away_valid == True:
                    print("The table will now be updated")
                    with open('table.csv', 'w', newline='') as f:
                        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC,
                                            delimiter=',')
                        writer.writerows(data)
                    with open('results.txt', 'a') as f2:
                        f2.write(f"{datetime.date.today()} {result}\n")

                else:
                    print("One or more of the teams are not part of the league."
                          " The table will not be updated")
        else:
            pass

def add_new_team():
    new_team_name = input("What is the name of the new team to be added? ").title()
    with open('table.csv', 'a', newline='') as file2:
        new_team_append = csv.writer(file2, quoting=csv.QUOTE_NONNUMERIC)
        new_team_append.writerow([new_team_name,0,0,0,0,0,0,0])
    print(f"{new_team_name} have been added to the league")

def delete_team():
    team_to_delete = input("What is the name of the new team to be deleted? ").title()
    confirm = input(f"Are you sure that you want to delete {team_to_delete} from the records."
                    " There is no way to undo this action."
                    "\nType 'delete' to confirm. Type anything else to cancel this request: ")
    if confirm == 'delete':
        df = pandas.read_csv('table.csv')
        df = df[df.Team != team_to_delete]
        df.to_csv('table.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
        print(f"{team_to_delete} have been removed from the league records")
    else:
        print("You have aborted this action. No team will be deleted.")

f = open('title.txt', 'r')
title = f.read()
print(title)
print("Here are the current teams taking part:")
with open('table.csv', mode ='r') as file:
  csvFile = csv.reader(file)
  for lines in csvFile:
        print(lines[0])

program_continues = True

while program_continues:
    action = input("\n\n\nWhat would you like to do? \n"
                   "Type either:\n"
                   "    'result' to add a new match result,\n"
                   "    'add team' to add a new team to the league,\n"
                   "    'delete team' to delete a team from the records,\n"
                   "    'table' to see the league table,\n"
                   "    'results archive' to see a full list of league results,\n"
                   " or 'exit' to close the program.\n")
    if action == "result":
        play_game()
    elif action == "add team":
        add_new_team()
    elif action == "delete team":
        delete_team()
    elif action == "table":
        league_table()
    elif action == "results archive":
        archive()
    elif action == "exit":
        exit()
    else:
        print("That was not a valid input")

