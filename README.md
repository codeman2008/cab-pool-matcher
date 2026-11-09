Cab Pool Matcher 

A Python-based command-line application that matches students travelling to Delhi or Jaipur with available shared cabs.

The application uses priority queues to allocate seats fairly, giving senior students preference while maintaining FIFO ordering among students in the same academic year.

Features

Ride Requests: Students can submit requests with their name, destination, time slot, and academic year.

Input Validation: Validates names, destinations, time slots, and academic years.

Priority-Based Matching: Students in higher academic years receive priority (Year 5 → Year 1).

FIFO Ordering: Among students in the same academic year, whoever submitted their request first gets priority.

Cab Management: Supports multiple cabs with different seating capacities.

Match Preview: Displays possible matches without modifying the waiting list.

Cab Dispatch: Assigns students to available cabs, even if the cab is not completely full.

Waiting List: Students who cannot be assigned a cab remain in the waiting list.

JSON Persistence: Saves and restores waiting requests, cab status, and assigned passengers across application restarts.

Technologies Used

Python 3

JSON

heapq – Priority queue implementation

datetime – Request submission timestamps

itertools.count – FIFO tie-breaking sequence

No external packages are required.

Project Structure

cab-pool-matcher/
│
├── main.py       # Main application and matching logic
├── model.py      # RideRequest and Cab classes
├── cabs.json     # Initial cab configuration
├── state.json    # Saved application state
└── README.md     # Project documentation

How to Run the Application

1. Install Python

Make sure Python 3 is installed on your system.

2. Clone the repository

git clone <YOUR-GITHUB-REPOSITORY-URL>

3. Navigate to the project directory

cd cab-pool-matcher

4. Run the application

python main.py

On some systems, you may need to use:

python3 main.py

The application loads the initial cab configuration from cabs.json when it starts.

Cab Configuration File

Cabs are loaded from an external JSON file instead of being hardcoded into the Python program.

The sample cabs.json file looks like this:

[
    {
        "driver": "Amit",
        "seats": 4,
        "destination": "Delhi",
        "time_slot": "Morning"
    },
    {
        "driver": "Rohan",
        "seats": 3,
        "destination": "Jaipur",
        "time_slot": "Evening"
    },
    {
        "driver": "Karan",
        "seats": 2,
        "destination": "Delhi",
        "time_slot": "Night"
    }
]

Each cab contains:

driver: Name of the cab driver.

seats: Total passenger capacity.

destination: Delhi or Jaipur.

time_slot: Morning, Afternoon, Evening, or Night.

Additional cabs can be added by following the same JSON structure.

Priority and Matching Logic

The application maintains separate priority queues for each destination and time-slot combination.

Students are prioritised according to:

Higher academic year receives higher priority.

Students belonging to the same academic year are served in FIFO order.

The priority queue is implemented using Python's heapq module.

Each heap entry contains:

Negative academic year, so higher years receive priority.

Submission timestamp, so earlier requests come first.

A unique sequence number, to prevent Python from comparing RideRequest objects when earlier values are equal.

The actual ride request.

Handling Tricky Situations

1. Half-Empty Cabs

A cab can be dispatched even if it is not completely full. The application assigns as many waiting students as possible, up to the cab's seating capacity.

2. No Cabs Available

If all matching cabs have already departed, the application displays a clear message and leaves the students in the waiting list. New requests are also preserved rather than discarded.
JSON Persistence

The application uses JSON to save and restore its state between executions.

The state.json file stores:

Waiting student requests.

Cab departure status.

Passengers assigned to each cab.

The priority queues are reconstructed when the application starts.

JSON was chosen because it is human-readable, lightweight, and supported by Python's built-in json module. Unlike binary formats such as Pickle, JSON files can be inspected and edited using an ordinary text editor, making debugging and maintenance easier.

If no saved state exists or the saved JSON is invalid, the application attempts to start with a fresh state.

Time Complexity Analysis

Let:

N = Number of waiting ride requests.

C = Number of cabs.

Adding one request — O(log N): Insertion into a binary heap using heapq.heappush() takes O(log N) time.

Adding 1,000 requests — O(N log N): Each request is inserted individually into its priority queue.

Dispatching one cab (up to 4 students) — O(N + C): Finding a matching cab takes O(C), while removing assigned students from the waiting list takes O(N) per removal; at most four students are removed.

Finding an open cab — O(C): The application scans the cab list until it finds a matching open cab or reaches the end.

JSON persistence adds the cost of serialising and writing the current application state after changes.
