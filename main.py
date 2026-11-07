
from datetime import datetime

import heapq
from itertools import count

import json
from model import RideRequest, Cab

priority_queues = {}
sequence = count()

# Stores all waiting student requests
requests = []


def add_to_priority_queue(request):
    key = (request.destination, request.time_slot)

    if key not in priority_queues:
        priority_queues[key] = []

    entry = (
        -request.year,
        request.submitted_at,
        next(sequence),
        request
    )

    heapq.heappush(priority_queues[key], entry)



# Load cabs from cabs.json
def load_cabs():
    with open("cabs.json", "r") as file:
        cab_data = json.load(file)

    loaded_cabs = []

    for item in cab_data:
        cab = Cab(
            item["driver"],
            item["seats"],
            item["destination"],
            item["time_slot"]
        )

        loaded_cabs.append(cab)

    return loaded_cabs


# Load cabs when the program starts
cabs = load_cabs()

def save_state():

    print("DEBUG: save_state() was called!")

    
    state = {
        "requests": [],
        "cabs": []
    }

    # Save all waiting requests
    for request in requests:
        state["requests"].append({
            "name": request.name,
            "destination": request.destination,
            "time_slot": request.time_slot,
            "year": request.year,
            "submitted_at": request.submitted_at.isoformat()
        })

    # Save the current status of every cab
    for cab in cabs:
        cab_data = {
            "has_left": cab.has_left,
            "passengers": []
        }

        for student in cab.passengers:
            cab_data["passengers"].append({
                "name": student.name,
                "destination": student.destination,
                "time_slot": student.time_slot,
                "year": student.year,
                "submitted_at": student.submitted_at.isoformat()
            })

        state["cabs"].append(cab_data)

    with open("state.json", "w") as file:
        json.dump(state, file, indent=4)

    print("Application state saved.")


def load_state():
    global requests, priority_queues, sequence

    try:
        with open("state.json", "r") as file:
            state = json.load(file)

        # Reset the in-memory data
        requests = []
        priority_queues = {}
        sequence = count()

        # Restore waiting requests
        for data in state["requests"]:
            request = RideRequest(
                data["name"],
                data["destination"],
                data["time_slot"],
                data["year"]
            )

            request.submitted_at = datetime.fromisoformat(
                data["submitted_at"]
            )

            requests.append(request)
            add_to_priority_queue(request)

        

        # Restore cab status and passengers
        if len(state["cabs"]) != len(cabs):
            raise ValueError("Cab configuration does not match.")

        for cab, cab_data in zip(cabs, state["cabs"]):
            cab.has_left = cab_data["has_left"]
            cab.passengers = []

            for data in cab_data["passengers"]:
                student = RideRequest(
                    data["name"],
                    data["destination"],
                    data["time_slot"],
                    data["year"]
                )

                student.submitted_at = datetime.fromisoformat(
                    data["submitted_at"]
                )

                cab.passengers.append(student)

        print("Previous application state loaded.")

    except FileNotFoundError:
        print("No previous state found. Starting fresh.")

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print("Could not load saved state:", error)
        print("Starting with a fresh application.")
        requests = []
        priority_queues = {}
        sequence = count()

load_state()


# Take and validate a ride request
def get_ride_request():

    name = input("Enter student name: ").strip()

    while not name:
        print("Name cannot be empty.")
        name = input("Enter student name: ").strip()

    # Validate destination
    while True:
        destination = input(
            "Enter destination (Delhi/Jaipur): "
        ).strip().title()

        if destination in ["Delhi", "Jaipur"]:
            break
        else:
            print("Invalid destination. Try again.")

    # Validate time slot
    while True:
        time_slot = input(
            "Enter time (Morning/Afternoon/Evening/Night): "
        ).strip().title()

        if time_slot in ["Morning", "Afternoon", "Evening", "Night"]:
            break
        else:
            print("Invalid time slot. Try again.")

    # Validate academic year
    while True:
        try:
            year = int(input("Enter academic year (1-5): "))

            if 1 <= year <= 5:
                break
            else:
                print("Year must be between 1 and 5.")

        except ValueError:
            print("Please enter a valid number.")

    return RideRequest(name, destination, time_slot, year)


# Display waiting students
def display_requests():

    print("\n--- WAITING STUDENTS ---")

    if len(requests) == 0:
        print("No students are waiting.")

    else:
        for student in requests:
            print(
                student.name,
                "|", student.destination,
                "|", student.time_slot,
                "| Year:", student.year
            )


# Display all cabs
def display_cabs():

    print("\n--- ALL CABS ---")

    for cab in cabs:
        status = "Departed" if cab.has_left else "Open"

        print(
            cab.driver,
            "|", cab.destination,
            "|", cab.time_slot,
            "| Seats:", len(cab.passengers), "/", cab.seats,
            "| Status:", status
        )


# Main menu

def main():
    while True:
        print("\n===== CAB POOL MATCHER =====")
        print("1. Add a ride request")
        print("2. View waiting students and cabs")
        print("3. Find Matches")
        print("4. Dispatch Cab")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            request = get_ride_request()
            requests.append(request)
            add_to_priority_queue(request)

            save_state()
            
            print("\nRequest successfully added!")

        elif choice == "2":
            display_requests()
            display_cabs()

        elif choice == "3":
            find_matches()

        elif choice == "4":
            dispatch_cab()

        elif choice == "5":
            print("Thank you for using Cab Pool Matcher!")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, 4 or 5.")


       
                                                  



def find_matches():
    print("\n--- FIND MATCHES ---")

    for cab in cabs:
        if cab.has_left:
            continue

        key = (cab.destination, cab.time_slot)

        if key not in priority_queues:
            continue

        # Copy the queue so preview doesn't change it
        temporary_queue = priority_queues[key].copy()

        selected = []

        while temporary_queue and len(selected) < cab.seats:
            entry = heapq.heappop(temporary_queue)
            selected.append(entry[3])

        print("\nDriver:", cab.driver)
        print("Destination:", cab.destination)
        print("Time slot:", cab.time_slot)
        print("Available seats:", cab.seats)

        if not selected:
            print("No matching students.")
        else:
            for student in selected:
                print(student.name, "| Year:", student.year)


def dispatch_cab():

    print("\n--- DISPATCH CAB ---")

    # Ask user to select destination
    print("1. Delhi")
    print("2. Jaipur")

    destination_choice = input("Choose destination: ")

    if destination_choice == "1":
        destination = "Delhi"
    elif destination_choice == "2":
        destination = "Jaipur"
    else:
        print("Invalid destination.")
        return

    # Ask user to select time slot
    print("\n1. Morning")
    print("2. Afternoon")
    print("3. Evening")
    print("4. Night")

    slots = {
        "1": "Morning",
        "2": "Afternoon",
        "3": "Evening",
        "4": "Night"
    }

    slot_choice = input("Choose time slot: ")

    if slot_choice not in slots:
        print("Invalid time slot.")
        return

    time_slot = slots[slot_choice]

    # Find the priority queue for this trip
    key = (destination, time_slot)

    if key not in priority_queues or not priority_queues[key]:
        print("No students waiting for this trip.")
        return

    # Find the first open cab for this trip
    selected_cab = None

    for cab in cabs:
        if (not cab.has_left
                and cab.destination == destination
                and cab.time_slot == time_slot):
            selected_cab = cab
            break

    if selected_cab is None:
        print("No open cab available for this trip.")
        return

    # Select students according to priority
    selected_requests = []

    while (priority_queues[key]
           and len(selected_requests) < selected_cab.seats):

        entry = heapq.heappop(priority_queues[key])
        selected_requests.append(entry[3])

    # Assign students to cab
    selected_cab.passengers.extend(selected_requests)

    # Remove dispatched students from waiting list
    for student in selected_requests:
        requests.remove(student)

    # Mark cab as departed
    selected_cab.has_left = True

    # Display dispatch information
    print("\nCab successfully dispatched!")
    print("Driver:", selected_cab.driver)
    print("Destination:", selected_cab.destination)
    print("Time slot:", selected_cab.time_slot)
    print("Passengers:", len(selected_cab.passengers),
          "/", selected_cab.seats)

    print("Students travelling:")

    for student in selected_requests:
        print(student.name, "| Year:", student.year)


    save_state()


# Start the program
if __name__ == "__main__":
    main()
