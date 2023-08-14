import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWould you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city in CITY_DATA:
            break
        else:
            print("\nYou can only choose Chicago, New York City or Washington. Please try again:\n")

    # get user input for filter type (month, day, both, none)
    while True:
        choice = input("\nWould you like to filter the data by month, day, both, or not at all? Type 'none' for no "
                       "time filter.\n").lower()
        if choice not in ('month', 'day', 'both', 'none'):
            choice = input("\nYou can only choose month, day or both. Please try again:\n").lower()
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'may', 'june']
    if choice == 'month' or choice == 'both':
        while True:
            month = input("\nWhich month? January, February, March, April, May, or June?\n").lower()
            if month not in months:
                month = input("\nYou can only choose month between: January, February, March, April, May, "
                              "June. Please try again:\n").lower()
                continue
            else:
                break
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['1', '2', '3', '4', '5', '6', '7', 'all']
    if choice == 'day' or choice == 'both':
        while True:
            day = input("\nWhich day? Please type your response as an integer (e.g., 1=Sunday, 2=Monday, 3=Tuesday, "
                        "4=Wednesday, 5=Thursday, 6=Friday, 7=Saturday). Or 'all'\n").lower()
            if day not in days:
                day = input("\nYou can only choose an integer: 1=Sunday, 2=Monday, 3=Tuesday, 4=Wednesday, "
                            "5=Thursday, 6=Friday, 7=Saturday. Or 'all'. Please choose again.\n")
                continue
            else:
                break
    else:
        day = 'all'
    print('-' * 40)
    return city, month, day


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

    # Load data into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert columns Start Time, End Time to format yyyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create month and day of week column from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%w")

    # filter the input (month, day)
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]  # create new dataframe by filter day

    # Create hour from Start Time
    df['hour'] = df['Start Time'].dt.hour
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month: ', common_month, ". ")

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week: ', common_day, ". ")

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Hour: ', common_hour, ". ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most Commonly used start station: ', start_station, ". ")

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', end_station, ". ")

    # display most frequent combination of start station and end station trip
    comb_station = df.groupby(['Start Station', 'End Station']).count()
    print("\nMost frequent combination of start station and end station trip: ", start_station, " & ", end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 3600.0
    print('Total travel time: ', total_travel_time, ' hours. ')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 3600.0
    print('Mean travel time: ', mean_travel_time, ' hours. ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types count: ', user_types, '\n')

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nGender Types: ', gender)
    except KeyError:
        print('Gender information not available.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print('\nEarliest Year: ', earliest_year)
    except KeyError:
        print('Earliest Year: No data available for this month.')

    try:
        recent_year = df['Birth Year'].max()
        print('\nMost Recent Year: ', recent_year)
    except KeyError:
        print('\nMost Recent Year: No data available for this month.')

    try:
        common_year = df['Birth Year'].mode()[0]
        print('\nMost Common Year: ', common_year)
    except KeyError:
        print('\nMost Common Year: No data available for this month.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_five_raw_data(df):
    """ Display 5 rows of data """
    five_row_display = input("\nDo you want to see the first five raws of data? Yes or No:\n").lower()
    if five_row_display == 'yes':
        row = 0
        while True:
            print(df.iloc[row: row + 5])
            row = row + 5
            more_five_row = input("\nDo you want to see more five rows ? Yes or No: \n").lower()
            if more_five_row != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_five_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    print("\nDone\n")
if __name__ == "__main__":
    main()
