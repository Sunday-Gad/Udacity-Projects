import time
import pandas as pd
import calendar as cal
import datetime

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def design_pat(row, text):
    """Prints a pattern of stars with a given number of rows and a text message."""
    stars = "*"
    for i in range(row):
        print(stars * (i + 1))
    print(text)
    for i in range(row, 0, -1):
        print(stars * i)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Welcome graphics
    design_pat(3, 'Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        user_city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if user_city not in CITY_DATA:
            print('Wrong input, please enter a selection from these cities (chicago, new york city, washington)\n')
        else:
            design_pat(2, f'You are interested in: {user_city.title()}')
            user_cities = CITY_DATA[user_city]
            break
    user_day = None
    user_month = None

    # get user input for month, day, both, or none
    while True:
        user_filter = input(
            'Would you like to filter the data by month, day, both, or not at all? Type "none" for no '
            'time filter\n').lower()
        if user_filter not in ['month', 'day', 'both', 'none']:
            print('Invalid selection, Please select from these options (month, day, both,  none)\n')
        else:
            break

    # get user input for both month and day
    if user_filter == 'both':
        while True:
            user_month = input('\nWhich month - January, February, March, April, May,  June?\n').lower()
            if user_month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                print('Invalid selection, Please select from these options (January, February, March, April, May,  '
                      'June)\n')
            else:
                break
        while True:
            user_day = input('\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, '
                             'or Sunday?\n').lower()
            if user_day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                print('Invalid selection, Please select from these options (Monday, Tuesday, Wednesday, Thursday, '
                      'Friday, '
                      'Saturday, or Sunday)\n')
            else:
                design_pat(2, f'showing data for filter: {user_city}---{user_filter} (by Month:by day)--> {user_month},'
                              f' {user_day}')
                break

    # get user input for month (all, january, february, ... , june)
    elif user_filter == 'month':
        while True:
            user_month = input('\nWhich month - January, February, March, April, May,  June?\n').lower()
            if user_month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                print('Invalid selection, Please select from these options (January, February, March, April, May,  '
                      'June)')
            else:
                design_pat(2, f'showing data with filter: {user_city}---{user_filter}---> {user_month}')
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif user_filter == 'day':
        while True:
            user_day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
            if user_day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                print('Invalid selection, Please select from these options (Monday, Tuesday, Wednesday, Thursday, '
                      'Friday, '
                      'Saturday, or Sunday)')
            else:
                design_pat(2, f'showing data with filter: {user_city}---{user_filter}---> {user_day}')
                break

    print('-' * 40)
    return user_cities, user_month, user_day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month is not None:
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week if applicable
    if day is not None:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    # Rename a column with a more descriptive name
    df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)

    # creating new column for age
    df['Age'] = datetime.date.today().year - df['Birth Year']

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nJust wait a moment.... Loading the data')
    print('\nData Loaded Successfully. Now applying filters...\n')
    start_time = time.time()

    # display the most common month
    print('Calculating this statistic...\n')

    popular_month = df['month'].mode()[0]
    print(f"What is the most popular month for Traveling?\n--- {cal.month_name[popular_month]}")
    print("That took %s seconds." % (time.time() - start_time))

    # display the most common day of week
    print('\nCalculating this statistic...\n')

    popular_day = df['day_of_week'].mode()[0]
    print(f"What is the most popular day for traveling?\n--- {popular_day}")
    print("That took %s seconds." % (time.time() - start_time))

    # display the most common start hour
    print('\nCalculating this statistic...\n')

    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print(f"What is the most popular hour of the day to start your travels?\n--- {popular_hour}")

    print("That took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    design_pat(2, 'Calculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    print('Calculating this statistic...\n')

    popular_start = df['Start Station'].mode()[0]
    print(f"What is the most popular Start station for Traveling?\n--- {popular_start}")
    print("That took %s seconds.\n" % (time.time() - start_time))

    # display most commonly used end station
    print('Calculating this statistic...\n')

    popular_end = df['End Station'].mode()[0]
    print(f"What is the most popular End station for Traveling?\n--- {popular_end}")
    print("That took %s seconds.\n" % (time.time() - start_time))

    # display most frequent combination of start station and end station trip
    print('Calculating this statistic...\n')

    frequent_comb = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'What is the most popular start station to end station:\nStart Station----End Station\n'
          f'{frequent_comb[0]}----{frequent_comb[1]}')
    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    design_pat(2, 'Calculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    print('Calculating this statistic...\n')

    total_time = datetime.timedelta(seconds=int(df['Trip Duration'].sum()))
    print(f"What is the total trip duration?\n--- {total_time}")
    print("That took %s seconds.\n" % (time.time() - start_time))

    # display mean travel time
    print('Calculating this statistic...\n')

    average_time = datetime.timedelta(seconds=int(df['Trip Duration'].mean()))
    print(f"What is the average time spent of each trip?\n--- {average_time}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    design_pat(2, 'Calculating User Stats...')
    start_time = time.time()

    # Display counts of gender
    print('Calculating this statistic...\n')

    try:
        gender = df['Gender'].value_counts()
        print(f"What is the breakdown of users?\n--- {gender}")
    except KeyError:
        print('No gender data to display')

    print("\nThis took %s seconds." % (time.time() - start_time))

    # Display earliest, most recent, most common year of birth and respective age
    print('Calculating this statistic...\n')
    try:
        oldest = df['Birth Year'].min()
        oldest_age = df['Age'].max()
        youngest = df['Birth Year'].max()
        youngest_age = df['Age'].min()
        popular_year = df['Birth Year'].mode()[0]
        popular_age = df['Age'].mode()[0]
        print(f"What is the oldest, youngest, popular year of birth, and age respectively?"
              f"\n{int(oldest)}  age: {int(oldest_age)} years\n{int(youngest)}  age: {int(youngest_age)} years"
              f"\n{int(popular_year)} age: {int(popular_age)} years")
    except KeyError:
        print("No birth year data to display")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """Displays consecutive five rows of raw data per request"""
    design_pat(2, 'Display Raw Data')
    start_time = time.time()
    count = 0
    while True:
        user_reply = input("Will you like to see five rows of raw data, enter (Yes or No)?\n").lower()
        if user_reply not in ['yes', 'no']:
            print(f"Wrong input, please select 'yes' to see data or 'no' to quit ")
        elif user_reply == 'yes':
            count += 1
            print('Calculating this statistic...\n')
            dic = df.iloc[(count - 1) * 5:count * 5].to_dict('index')
            for index, col_val in dic.items():
                print(f"\nNo.{index}")
                for col, values in col_val.items():
                    print(f"{col} : {values}")
            print("\nThis took %s seconds." % (time.time() - start_time))
        else:
            break

    print("\nTotal time: %s seconds." % (time.time() - start_time))

    print('-' * 40)


def restart_program():
    """Checks if the user wants to restart the program and prompts accordingly."""
    restart = input("\nWould you like to restart program? Enter yes or no.\n").lower()
    while restart not in ['yes', 'no']:
        print('you entered a wrong input, type "Yes" to continue or "No" to quit Program')
        restart = input("\nWould you like to restart program? Enter yes or no.\n").lower()
    if restart == 'yes':
        return True
    else:
        design_pat(5, 'Thank you for your time')
        return False


def main():
    city, month, day = get_filters()
    df = load_data(city, month, day)
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    display_data(df)
    should_restart = restart_program()
    if should_restart:
        main()


if __name__ == "__main__":
    main()
