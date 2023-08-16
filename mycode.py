import pandas as pd
import numpy as np
import time

# dictionary containing cities data
city_data = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv"
}

# months array
months_array = ["all", "january", "february", "march", "april", "may", "june"]

day_list = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "all",
]


# read user inputs (city, month, and day)
def choose_filter():
    print("\nWelcome to the program.\n")

    # choosing city
    city = ""
    while city not in city_data.keys():
        print("\nplease choose your city:\n")

        city = input("1- Chicago 2- New York City 3- Washington\n").lower()

        if city not in city_data.keys():
            print("\nplease check your input, select one of the mentioned cities.")
            print("try again")
    print(f"\nyou have chosen {city.title()}.")

    # choosing month
    month = ""
    while month not in months_array:
        print("\nplease choose a month between January to June, or 'all' for all months:")
        month = input().lower()

        if month not in months_array:
            print("\nplease check your input, select one of the mentioned month.")
            print("try again")
    print(f"\nYou have chosen {month.title()} as your month.")

    # choosing day
    day = ""

    while day not in day_list:
        print("\nplease enter a day in the week, or 'all' for all days:")
        day = input().lower()

        if day not in day_list:
            print("\nplease check your input, select one of the week days.")
            print("try again")

    # print all user inputs
    print(
        f"\nYou have chosen to view data for city: {city.title()}, month: {month.title()} and day: {day.title()}."
    )
    return city, month, day


# get data from .csv files
def filtering_data(city, month, day):
    # getting data from files
    print("\nfetching data...")
    df = pd.read_csv(city_data[city])

    # Convert the Start Time column to datetime and adding month ,day , and hour
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.dayofweek
    df["hour"] = df["Start Time"].dt.hour

    # create new data frame for the filtered data
    if month != "all":
        df = df[df["month"] == months_array.index(month)]

    if day != "all":
        df = df[df["day_of_week"] == day_list.index(day)]
    
    return df


# display data
def display_data(df):
    expected_responses = ["yes", "no"]
    response = ""

    # counting displayed rows
    counter = 0
    print("\nDo you wish to view the raw data?")
    while response not in expected_responses:
        response = input("Accepted responses: 'yes' or 'no'\n").lower()

        if response == "yes":
            print(df.head())
        elif response not in expected_responses:
            print("please choose 'yes' or 'no'.")
            print("try agian")

    while response == "yes":
        print("\nDo you want to see the next 5 rows?")
        response = input("Accepted responses: 'yes' or 'no'\n").lower()
        counter += 5

        if response == "yes":
            print(df[counter : counter + 5])
        elif response == "no":
            break
        else:
            print("please choose 'yes' or 'no'.")
            print("try agian")


# displaying the most popular (month, day, hour)
def popular_time(df):
    print("\nMost Popular Time")
    # most popular month
    popular_month = df["month"].mode()[0]
    print(f"Most popular month: {months_array[popular_month].title()}")

    # most popular day
    popular_day = df["day_of_week"].mode()[0]
    print(f"Most popular day: {day_list[popular_day].title()}")

    # most popular month
    popular_hour = df["month"].mode()[0]
    print(f"Most popular starting hour: {popular_hour}\n")


# display the most popular stations (start, end, and combined)
def popular_stations(df):
    print("\nMost Popular Stations")
    # start station
    popular = df["Start Station"].mode()[0]
    print(f"The most popular start station: {popular}")

    # end station
    popular1 = df["End Station"].mode()[0]
    print(f"The most popular end station: {popular1}")

    # combined stations
    df["Start To End"] = df["Start Station"].str.cat(df["End Station"], sep=" to ")
    combo = df["Start To End"].mode()[0]
    print(f"The most frequent combination of trips are from {combo}.\n")


# display total and avg trip duraion
def trip_stats(df):
    print("\nTotal and Avg Trips duration")

    # sum total trip durations in seconds
    total_duartion = df["Trip Duration"].sum()
    # find minutes and seconds
    min, sec = divmod(total_duartion, 60)
    # find hours and minutes
    hours, min = divmod(min, 60)
    # print results
    print(f"Total trips duration: {hours} hours, {min} minutes, and {sec} seconds.")

    # calculating avg trip duration
    avg_duration = round(df["Trip Duration"].mean())
    # find minutes and seconds
    min, sec = divmod(avg_duration, 60)
    # find hours and minutes
    hours, min = divmod(min, 60)
    print(f"Average trip duration: {hours} hours, {min} minutes, and {sec} seconds.\n")


# display user states
def user_stats(df):
    print("\nUser Stats...")
    user_type = df["User Type"].value_counts()
    print(f"The types of users by number are given below:\n\n{user_type}")

    try:
        gender = df["Gender"].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    try:
        earliest = int(df["Birth Year"].min())
        recent = int(df["Birth Year"].max())
        common_year = int(df["Birth Year"].mode()[0])
        print(
            f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}"
        )
    except:
        print("There are no birth year details in this file.")


# main Function
def main():
    while True:
        city, month, day = choose_filter()
        print("*" * 80)
        df = filtering_data(city, month, day)
        print("*" * 80)
        display_data(df)
        print("*" * 80)
        popular_time(df)
        print("*" * 80)
        popular_stations(df)
        print("*" * 80)
        trip_stats(df)
        print("*" * 80)
        user_stats(df)
        print("*" * 80)

        response = input("if you want to restart the program, enter 'yes'\n").lower()
        if response != "yes":
            break


if __name__ == "__main__":
    main()
