# cab-pool-matcher
Cab Pool matcher project
Cab Pool Matcher helps students coordinate shared cab rides to Delhi and Jaipur by matching ride requests with available cabs. It uses a priority-based system to ensure that senior students receive preference when seats are limited.

Features
Ride Requests: Students can submit requests by providing their name, destination, time slot, and academic year.

Input Validation: Validates student details, destinations, time slots, and academic years.

Priority-Based Matching: Senior students receive higher priority (Year 5 → Year 1).

FIFO Ordering: Students from the same academic year are served in their submission order.

Cab Management: Supports multiple cabs with different seating capacities.

Match Preview: Preview potential cab assignments without modifying the waiting list.

Cab Dispatch: Dispatch available cabs even when they are not completely full.

Waiting List Management: Students who cannot be assigned a cab remain in the waiting list.

JSON Persistence: Saves and restores waiting requests, cab departure status, and assigned passengers across application restarts.

Error Handling: Handles missing or invalid saved state files.

Technologies used

Python 3

JSON

heapq – Priority queue implementation

datetime – Request submission timestamps

itertools – FIFO tie-breaking sequence
