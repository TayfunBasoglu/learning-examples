import os
import sys
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Habit database file and path ---------
file = "database.csv"

### Time Now
time_now =  str(datetime.now())

# Terminal Clear
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# Setup Habits and File
def start_control():
    if not os.path.isfile(file):
        clear()
        print("Which habits would you like to track?\nPlease separate each of them by using comma. (e.g., Reading, Sport, Studying...)")
        habits = str(input("\n-> "))
        if set(habits) == {','} or habits == "" or habits.isspace():
            sys.exit("\n\tempty value\n\n")
        habits = list(set(habits.split(",")))
        habits_end = list()
        for i in habits:
            habits_end.append(empty_value_cleaner(i))
        habits_end = ("date"+"".join(habits_end)).replace(",,",",")
        with open(file,"w", encoding='utf8') as d_file:
            d_file.write(habits_end)

# Empty Value Cleaner
def empty_value_cleaner(x):
    if x.isspace():
        sys.exit("\n\tempty value\n\n")
    elif x.startswith(" "):
        return ","+x[1:]
    elif x.endswith(" "):
        return ","+x[:-1]
    elif x.endswith(" ") or x.startswith(" "):
        return ","+x[1:-1]
    else:
        return ","+x

### New Habit
def new_habit():
    read = pd.read_csv(file)
    clear()
    print("enter a habit (don't use commas | 'q' for exit)")
    new_habit_input = input("-> ")
    if "," in new_habit_input:
        print("\n\tdon't use commas")
        time.sleep(1.5)
        new_habit()
    elif new_habit_input.isspace() or new_habit_input == "":
        print("\n\tit's empty")
        time.sleep(1.5)
        new_habit()
    elif new_habit_input == "q":
        menu()
    elif new_habit_input in read.columns:
        print("this habit already exists")
        time.sleep(1)
        new_habit()
    else:
        if new_habit_input.startswith(" "):
            new_habit_input = new_habit_input[1:]
        read[new_habit_input] = ""
        print("\n","habit added","\n")
        read.to_csv(file,mode="w",encoding="utf-8",index=False)
        time.sleep(1)

# Habit Delete
def habit_delete():
    clear()
    read = pd.read_csv(file)
    print("\nWhich habit would you like to delete? (q for back)")
    print(list(read.columns)[1:])
    delete_habit_input = input("\n -> ")
    if delete_habit_input.startswith(" "):
        delete_habit_input = delete_habit_input[1:]
    elif delete_habit_input == "q":
        menu()
    if delete_habit_input not in read.columns:
        print("\n\tthis habit not exists\n\n")
        time.sleep(1.5)
        habit_delete()
    else:
        del read[delete_habit_input]
        print("\n\t",delete_habit_input,"deleted","\n")
        read.to_csv(file,mode="w",encoding="utf-8",index=False)
    time.sleep(1.5)

### Habit List
def habit_list():
    clear()
    read = pd.read_csv(file)
    print("\n\n"+" "*12+"#"+(len(max(list(read.columns),key=len))*"##")+"#")
    print(" "*8+" "*(len(max(list(read.columns),key=len)))+"Habits List")
    print(" "*12+"#"+(len(max(list(read.columns),key=len))*"##")+"#")
    for i in read.columns:
        if i == "date":
            pass
        else:
            print(" "*12+"+"+(len(max(list(read.columns),key=len))*"--")+"+")
            print(" "*15+i)
            if i == read.columns[-1]:
                print(" "*12+"+"+(len(max(list(read.columns),key=len))*"--")+"+")
    input("\n\nPress 'Enter' to go back")

# Add Activity
def add_activity():
    clear()
    read = pd.read_csv(file)
    if len(read[read["date"].str[:10] == time_now[:10]]) > 0:
        print("\n+"+"-"*75+"+")
        print('"',time_now[:10],'"')
        print("Activity has already been added today.\nIf you want to change it, delete of the day’s activity and add it again.")
        print("+"+"-"*75+"+")
        input("Press 'Enter' to go back")
        menu()
    else:
        print("\n+"+"-"*58+"+")
        print("-------------------->   Add Activity   <--------------------")
        print("+"+"-"*58+"+")
        print("\nPlease input the all habits data together at the end of the day\notherwise you’ll need to delete all data of the day in case of a correction.\n")
        print("!! Warning -> [Y/N or y/n] -> 'Y' for done, 'N' for not done, 'q' for exit\n")
        daily_activity = [[time_now]]
        for habits in read.columns[1:]:
            get_ac = input(habits+" -> ")
            if get_ac not in ["y","Y","N","n","q"]:
                print("Value Error")
                time.sleep(1.5)
                add_activity()
            elif get_ac == "q":
                menu()
            elif get_ac in ["Y","y"]:
                daily_activity[0].append("Y")
            else:
                daily_activity[0].append("N")
        add_data = pd.DataFrame(data=daily_activity, columns=read.columns)
        ac_end = pd.concat([read,add_data],axis=0,ignore_index=True)
        ac_end.to_csv(file,mode="w",encoding="utf-8",index=False)
        clear()
        print("\n\n\tadded...")
        menu()

# Delete Activity Menu
def delete_activity():
    clear()
    print("\n\n    +"+"-"*35+"+")
    print("    |"+" "*35+"|")
    print("    |  1)Delete Last Activity"+" "*11+"|")
    print("    |  2)Search and Delete Activity"+" "*5+"|")
    print("    |  3)Exit"+" "*27+"|")
    print("    |"+" "*35+"|")
    print("    +"+"-"*35+"+")
    delete_choice = input("\n-> ")
    if delete_choice not in ["1","2","3"]:
        print("\n\tValue Error")
        time.sleep(1)
        delete_activity()
    elif delete_choice == "3":
        menu()
    elif delete_choice == "1":
        delete_last_ac()
    else:
        search_and_delete()

# Delete Last Activity
def delete_last_ac():
    clear()
    read = pd.read_csv(file)
    read2 = pd.read_csv(file,index_col=["date"])
    last_row = read.shape[0]-1
    print(read2.iloc[last_row,:].fillna("-").to_markdown(tablefmt="fancy_grid"))
    delete_last_input = input("\n\nWould you like to delete it?  (Y/N)\n\n -> ")
    if delete_last_input not in ["y","Y","n","N"]:
        delete_last_ac()
    elif delete_last_input in ["Y","y"]:
        read = read.drop(last_row)
        read.to_csv(file,mode="w",encoding="utf-8",index=False)
        print("\n\nLast activity deleted.\n\n")
        time.sleep(1)
        menu()
    else:
        menu()

# Search and delete
def search_and_delete():
    clear()
    read = pd.read_csv(file).fillna("-")
    search_date = input("Enter it like -> 2021-01-30 (q for back)\n-> ")
    if search_date == "q":
        menu()
    elif len(search_date) < 9:
        print("Value Error")
        time.sleep(1)
        search_and_delete()
    elif (search_date[4]=="-") and (search_date[7]=="-"):
        if len(read[read["date"].str[:10] == search_date]) < 1:
            print("Not found")
            time.sleep(1.5)
            search_and_delete()
        else:
            clear()
            print(read[read["date"].str[:10]==search_date].to_markdown(index=False,tablefmt="fancy_grid"))
            search_date_delete = input("\n\nWould you like to delete it?  (Y/N)\n\n -> ")
            if search_date_delete in ["N","n"]:
                menu()
            elif search_date_delete in ["y","Y"]:
                read_end = read[read["date"].str[:10] != search_date[:10]]
                read_end.to_csv(file,mode="w",encoding="utf-8",index=False)
                print("\t\nDeleted\n\n")
                time.sleep(1.2)
                menu()
            else:
                print("Value Error")
                time.sleep(1.5)
                search_and_delete()
    else:
        print("Not found.")
        time.sleep(1.2)
        search_and_delete()

# See Specific Date
def see_specific_date():
    clear()
    read = pd.read_csv(file)
    search_date = input("Enter it like -> 2021-01-30 (q for back)\n-> ")
    if search_date == "q":
        menu()
    elif len(search_date) < 9:
        print("Value Error")
        time.sleep(1)
        see_specific_date()
    elif len(read[read["date"].str[:10] == search_date]) > 0:
        print(read[read["date"].str[:10] == search_date].dropna(axis=1).to_markdown(index=False,tablefmt="fancy_grid"))
        input("\n\nPress 'Enter' to go back")
    else:
        print("Value Error")
        time.sleep(1)
        see_specific_date()

# Export HTML
def export_html():
    read = pd.read_csv(file)
    html_data = """
<html>
<style>
.datastyle {
    font-size: 11pt; 
    font-family: Verdana;
    border-collapse: collapse; 
    border: 1px solid silver;
    margin:0 auto;
    width:70%;
}
.datastyle td, th {
    padding: 20px;
}
.datastyle tr:nth-child(even) {
    background: #E0E0E0;
}
.datastyle tr:hover {
    background: silver;
}
</style><body></br></br>
    """
    html_data2 = "</br></br></body></html>"
    print("\n\tSaving..\n")
    time.sleep(1)
    readhtml = read.fillna("-")
    readhtml = readhtml.to_html(index=False,classes='datastyle')
    end = html_data + readhtml + html_data2
    with open("habit_data.html","w") as case:
        case.write(end)
    menu()

#specific date range
def specific_date_range():
    clear()
    read = pd.read_csv(file)
    search_date = input("Starting date | Enter it like -> 2021-01-30 (q for back)\n-> ")
    if search_date == "q":
        menu()
    elif len(search_date) < 9:
        print("Value Error")
        time.sleep(1)
        specific_date_range()
    search_date2 = input("End date | Enter it like -> 2021-01-30 (q for back)\n-> ")
    if search_date2 == "q":
        menu()
    elif len(search_date2) < 9:
        print("Value Error")
        time.sleep(1)
        specific_date_range()
    elif len(read[read["date"].str[:10] == search_date]) > 0 and len(read[read["date"].str[:10] == search_date2]) > 0:
        clear()
        start = read[read["date"].str[:10] == search_date].index.values
        start_str = int(str(start)[1])
        end = read[read["date"].str[:10] == search_date2].index.values
        end_str = int(str(end)[1])
        endend = read.iloc[start_str:end_str+1,:].dropna(axis=1,how="all")
        endend = endend.fillna("-")
        print(endend.to_markdown(index=False,tablefmt="fancy_grid"))
        input("\n\nPress 'Enter' to go back ")
    else:
        print("Value Error")
        time.sleep(1)
        specific_date_range()

# See Activities
def see_activities():
    clear()
    read = pd.read_csv(file)
    print("\n\n    +"+"-"*35+"+")
    print("    |"+" "*35+"|")
    print("    |  1)See a Specific Date"+" "*12+"|")
    print("    |  2)Specific Date Range"+" "*12+"|")
    print("    |  3)Last 10 Activities"+" "*13+"|")
    print("    |  4)Export to html (All data)"+" "*6+"|")
    print("    |  5)Exit"+" "*27+"|")
    print("    |"+" "*35+"|")
    print("    +"+"-"*35+"+")
    see_activities_input = input("\n\n-> ")
    if see_activities_input not in ["1","2","3","4","5"]:
        print("\n\tValue Error\n\n")
        time.sleep(1)
        see_activities()
    elif see_activities_input == "5":
        menu()
    elif see_activities_input == "3":
        clear()
        read = read.dropna(axis=1,how="all").fillna("-")
        print(read.tail(10).to_markdown(index=False,tablefmt="fancy_grid"))
        input("\t\nenter for back\n\n")
        menu()
    elif see_activities_input == "1":
        see_specific_date()
    elif see_activities_input == "4":
        export_html()
    elif see_activities_input == "2":
        specific_date_range()

def terminal():
    clear()
    read = pd.read_csv(file,na_filter=False)
    print("\n╒══════════════════════════════════════╕")
    print("│                First Date            │")
    print("════════════════════════════════════════")
    print("│                Last Date             │")
    print("╘══════════════════════════════════════╛\n\n")
    print("\n\n# Total Habits -> ",len(read.columns[1:]))
    print("-"*80+"\n")
    for i in read.columns:
        if len(read[(read[i]=="N") | (read[i]=="Y")][["date",i]])<1:
            pass
        else:
            firstdate = read[(read[i]=="N") | (read[i]=="Y")][["date",i]].head(1)
            lastdate = read[(read[i]=="N") | (read[i]=="Y")][["date",i]].tail(1)
            totalcount = len(read[read[i]=="Y"])+len(read[read[i]=="N"])
            yescount = len(read[read[i]=="Y"])
            nocount = len(read[read[i]=="N"])
            if firstdate.to_markdown() == lastdate.to_markdown():
                print(firstdate.to_markdown(index=False,tablefmt="fancy_grid"))
                print("\n  Total Days  : ",totalcount)
                print("\n  Total 'Y'   : ",yescount)
                print("  Total 'N'   : ",nocount)
                print("\n  Total Ratio of YES :",round((yescount*100)/totalcount,2))
                print("\n"+"-"*80+"\n")
            else:
                print(firstdate.merge(lastdate,how="outer").to_markdown(index=False,tablefmt="fancy_grid"))
                print("\n  Total Days  : ",totalcount)
                print("\n  Total 'Y'   : ",yescount)
                print("  Total 'N'   : ",nocount)
                print("\n  Total Ratio of YES :",round((yescount*100)/totalcount,2))
                print("\n"+"-"*80+"\n")
    input("\n\nEnter for back")
    menu()

def savepng():
    read = pd.read_csv(file)
    for i in read.columns[1:]:
        firstdate = read[(read[i]=="N") | (read[i]=="Y")][["date",i]].head(1)
        lastdate = read[(read[i]=="N") | (read[i]=="Y")][["date",i]].tail(1)
        yescount = len(read[read[i]=="Y"])
        nocount = len(read[read[i]=="N"])
        totalcount = len(read[read[i]=="Y"])+len(read[read[i]=="N"])
        if totalcount < 1:
            pass
        elif firstdate.to_markdown() == lastdate.to_markdown():
            fig = plt.figure(figsize=(12,6))
            ax1 = fig.add_subplot(1,2,1)
            ax1.pie([yescount,nocount],autopct='%1.2f%%',explode=[0.02,0.0])
            ax1.legend(["Yes","No"],loc=[0.005,0.0002])
            ax2 = fig.add_subplot(1,2,2)
            ax2.axis('off')
            ax2.text(0,.85,'Habit : '+i,fontsize=15)
            ax2.text(0,0.75,"Total Yes : "+str(yescount),fontsize = 12)
            ax2.text(0,0.65,"Total No : "+str(nocount),fontsize = 12)
            ax2.text(0,0.55,"Total Activity : "+str(totalcount),fontsize = 12)
            ax2.text(0,0.45,"One Activity : "+str(str(firstdate.values[0][0])),fontsize = 12)
            plt.savefig(i+"_graph.png")
            print(i+"_graph.png")
        else:
            fig = plt.figure(figsize=(12,6))
            ax1 = fig.add_subplot(1,2,1)
            ax1.pie([yescount,nocount],autopct='%1.2f%%',explode=[0.02,0.0])
            ax1.legend(["Yes","No"],loc=[0.005,0.0002])
            ax2 = fig.add_subplot(1,2,2)
            ax2.axis('off')
            ax2.text(0,.85,'Habit : '+i,fontsize=15)
            ax2.text(0,0.75,"Total Yes : "+str(yescount),fontsize = 12)
            ax2.text(0,0.65,"Total No : "+str(nocount),fontsize = 12)
            ax2.text(0,0.55,"Total Activity : "+str(totalcount),fontsize = 12)
            ax2.text(0,0.45,"First Activity : "+str(str(firstdate.values[0][0])),fontsize = 12)
            ax2.text(0,0.35,"Last Activity : "+str(str(lastdate.values[0][0])),fontsize = 12)
            plt.savefig(i+"_graph.png")
            print(i+"_graph.png")
    time.sleep(0.5)
    print("\n#files saved...")
    input("\n\tenter for back\n")
    menu()

def statistics():
    clear()
    print("\n\n    +"+"-"*35+"+")
    print("    |"+" "*35+"|")
    print("    |  1)See in Terminal"+" "*16+"|")
    print("    |  2)Save .png file"+" "*17+"|")
    print("    |  3)Exit"+" "*27+"|")
    print("    |"+" "*35+"|")
    print("    +"+"-"*35+"+")
    statistics_input = input("\n-> ")
    if statistics_input not in ["1","2","3"]:
        print("\n\tValue Error\n\n")
        time.sleep(1)
        statistics()
    elif statistics_input == "3":
        menu()
    elif statistics_input == "1":
        terminal()
    elif statistics_input == "2":
        savepng()

# DB Control
start_control()

# Menu
def menu():
    while True:
        clear() # Clear
        print("""
    +---------------------------------------+
    |                                       |
    |  1)Add Habit                          |
    |  2)Delete Habit                       |
    |  3)Habit List                         |
    |  4)Add Activity                       |
    |  5)Delete Activity                    |
    |  6)See & Save Activities              |
    |  7)Statistics                         |
    |  8)Exit                               |
    |                                       |
    +---------------------------------------+
        """)
        panel_number = input("Enter a number -> ")
        if panel_number == "1":
            #add habit
            new_habit()
        elif panel_number == "2":
            #Delete Habit
            habit_delete()
        elif panel_number == "3":
            #Habit List
            habit_list()
        elif panel_number == "4":
            #Add Activity
            add_activity()
        elif panel_number == "5":
            #Delete Activity
            delete_activity()
        elif panel_number == "6":
            #See activities
            see_activities()
        elif panel_number == "7":
            #Statistics
            statistics()
        elif panel_number == "8":
            sys.exit("Exit")
        else:
            menu()
# start menu
menu()
