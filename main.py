from parking_spot import ParkingSpot
from file_processors import read_from_csv, read_txt_keys
from constants import DATE_TIME, KEY_FILE, NEW_CSV, ELEMKEY, PARKING_SPACES,\
    SIDE, STUDY_AREA, TOTAL_VEHICLES, UNITDESC


def get_keys():
    keys = read_txt_keys(KEY_FILE)
    return keys


def generate_dictionary_element(key):
    parking_spot_instances = []
    data_points = read_from_csv(NEW_CSV, ELEMKEY, key)
    try:
        for obj in data_points:
            spot = ParkingSpot(key, obj[STUDY_AREA], obj[DATE_TIME], obj[SIDE],
                            obj[UNITDESC], obj[PARKING_SPACES], obj[TOTAL_VEHICLES])
            parking_spot_instances.append(spot)
        return parking_spot_instances
    except ValueError:
        print(f"{obj[UNITDESC]} at {obj[DATE_TIME]} is missing a vital data point.")


def create_parking_dictionary(keys):
    all_spot_data = {}
    for key in keys:
        spot_list = generate_dictionary_element(key)
        all_spot_data[key] = spot_list
    return all_spot_data


def get_occupancy_average(collection):
    occupancy_sum = 0
    for instance in collection:
        occupancy_sum += instance.spaces_taken
    return occupancy_sum / len(collection)


def get_specified_time_data(collection, time):
    data_points = []
    time = time_standardizer(time)
    for item in collection:
        if time in item.date_time:
            data_points.append(item)
    if len(data_points) == 0:
        return None
    return data_points


def get_all_available_space_values(collection):
    all_available_spaces_values = []
    for item in collection:
        available_spaces = item.total_spaces - item.spaces_taken
        if available_spaces < 0:
            available_spaces = 0
        all_available_spaces_values.append(available_spaces)
    return all_available_spaces_values


def get_possible_available_space_values(collection):
    values = []
    for item in collection:
        if item not in values:
            values.append(item)
    values.sort()
    set(values)
    return values


def get_value_frequencies(all_values, possible_values):
    frequencies = {}
    # Turn each possible value into a dictionary key
    for value in possible_values:
        frequencies[value] = 0
    # Increase the value of a given key by 1 for each time it occurs
    for value in all_values:
        frequencies[value] += 1
    return frequencies


def confidence_level(frequencies, possibe_values):
    VERY_HIGH = 90
    HIGH = 75
    MEDIUM = 50
    LOW = 25

    # Minimum number of open spaces required for there to be considered open spots
    minimum_spaces = 2
    if max(possibe_values) <= minimum_spaces:
        minimum_spaces = 1
    # Total number of open space measurements
    total_measurements = 0
    # Total number of times the minimum number of open spaces was measured
    min_req_met = 0
    for value in possibe_values:
        total_measurements += frequencies[value]
        if value >= minimum_spaces:
            min_req_met += frequencies[value]

    # Calculate a percentage of how many times there was open parking
    percent_open_space = (min_req_met / total_measurements) * 100

    # Conversion of percentage into confidence level 
    if percent_open_space >= VERY_HIGH:
        return "VERY HIGH" 
    elif percent_open_space >= HIGH:
        return "HIGH"
    elif percent_open_space >= MEDIUM:
        return "MEDIUM"
    elif percent_open_space >= LOW:
        return "LOW"
    elif percent_open_space < LOW:
        return "VERY LOW"


def time_standardizer(time):
    middle = time.find(":")
    hour = int(time[:middle])
    minutes = int(time[middle+1:])

    if minutes > 30:
        minutes = 0
        hour += 1
    elif minutes > 0:
        minutes = 0

    if hour == 24:
        hour = 0

    return f"{hour}:{minutes}"


def main():
    keys = get_keys()
    finished = False

    all_spots_data = create_parking_dictionary(keys)

    while not finished:
        # Prompt user to pick a parking zone
        user_key = input("Please enter the ID of the spot you would like to check or type 'quit' to exit: ").lower()
        if user_key in keys:
            # Element key for specified zone
            key = user_key
            # Collection of all data points for specified zone
            chosen_spot_data = all_spots_data[key]
            # Specified street location
            location = chosen_spot_data[0].unit_description
            # Side of the street zone is on
            side_of_street = chosen_spot_data[0].side
            # Estimated total parking spaces at specified zone
            total_spaces = chosen_spot_data[0].total_spaces
            # Average number of spots occupied for all times at specified zone
            avg_spots_taken = round(get_occupancy_average(chosen_spot_data), 1)

            # Inform the user of some basic stats about that zone
            print(f"Your chosen parking zone is located on the {side_of_street} side of {location}.")
            print(f"Estimated total possible parking spaces: {total_spaces}")
            print(f"Average number of spots taken: {avg_spots_taken}")

            # Access data about that zone at a user-specified time
            time_chosen = False
            while not time_chosen:
                # Prompt user to pick a time
                user_time = input("Please enter an estimated time using 24 hour format or type 'back' to check a different zone: ").lower()
                # List of all data points for specified time
                chosen_time_data = get_specified_time_data(chosen_spot_data, user_time)
                if chosen_time_data is not None:
                    # List of all available space values
                    all_values = get_all_available_space_values(chosen_time_data)
                    # Set of possible available space values
                    possible_values = get_possible_available_space_values(all_values)
                    # Dictionary specifying num of times each value occurs
                    frequencies = get_value_frequencies(all_values, possible_values)
                    # Confidence level of finding parking at specified zone at specified time
                    confidence = confidence_level(frequencies, possible_values)
                    # Tell user their likelihood of finding parking
                    print(f"You have a {confidence} likelihood of finding parking there at that time!")

                    # Prompt user to either check another time or choose another zone
                    user_continue = input("Would you like to check another time (Y/N)? ").lower()
                    if user_continue == "n" or user_continue == "no":
                        time_chosen = True

                elif user_time == "back" or user_time == "b":
                    time_chosen = True
                else:
                    print("Sorry! There is no data for that specified time.")

        elif user_key == "quit" or user_key == "q":
            finished = True
        else:
            print("Sorry! We don't have data on that zone.")

if __name__ == "__main__":
    main()
