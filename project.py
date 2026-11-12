import webbrowser
from urllib.parse import urlencode
import heapq

# Shortest Path Finder Using Dijkstra's Algorithm
# Road distances are approximate and used for academic demonstration.

ROADS = [
    ("Delhi", "Jaipur", 280),
    ("Delhi", "Agra", 230),
    ("Delhi", "Lucknow", 555),
    ("Delhi", "Chandigarh", 245),
    ("Delhi", "Amritsar", 450),
    ("Chandigarh", "Amritsar", 230),
    ("Jaipur", "Ahmedabad", 660),
    ("Jaipur", "Udaipur", 395),
    ("Jaipur", "Agra", 240),
    ("Udaipur", "Ahmedabad", 260),
    ("Agra", "Lucknow", 335),
    ("Agra", "Bhopal", 600),
    ("Lucknow", "Varanasi", 320),
    ("Varanasi", "Kolkata", 680),
    ("Varanasi", "Bhopal", 790),
    ("Bhopal", "Nagpur", 350),
    ("Bhopal", "Indore", 195),
    ("Indore", "Ahmedabad", 400),
    ("Indore", "Mumbai", 590),
    ("Ahmedabad", "Mumbai", 525),
    ("Mumbai", "Pune", 150),
    ("Pune", "Hyderabad", 560),
    ("Pune", "Bengaluru", 840),
    ("Nagpur", "Hyderabad", 500),
    ("Nagpur", "Kolkata", 1100),
    ("Hyderabad", "Bengaluru", 570),
    ("Hyderabad", "Chennai", 625),
    ("Bengaluru", "Chennai", 345),
    ("Kolkata", "Bhubaneswar", 440),
    ("Bhubaneswar", "Hyderabad", 1050),
    ("Bhubaneswar", "Chennai", 1200),
]


def build_graph(roads):
    graph = {}

    for city1, city2, distance in roads:
        graph.setdefault(city1, {})[city2] = distance
        graph.setdefault(city2, {})[city1] = distance

    return graph


def dijkstra(graph, source, target=None):
    distances = {city: float("inf") for city in graph}
    previous = {city: None for city in graph}

    distances[source] = 0
    priority_queue = [(0, source)]
    visited = set()
    steps = []

    while priority_queue:
        current_distance, current_city = heapq.heappop(
            priority_queue
        )

        if current_city in visited:
            continue

        visited.add(current_city)

        steps.append(
            f"Visited {current_city}: "
            f"{current_distance} km"
        )

        if current_city == target:
            break

        for neighbor, road_distance in graph[current_city].items():
            if neighbor in visited:
                continue

            new_distance = current_distance + road_distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_city

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

                steps.append(
                    f"Updated {neighbor}: {new_distance} km"
                )

    return distances, previous, steps, visited


def reconstruct_path(previous, source, target):
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    if path[0] != source:
        return []

    return path


def find_shortest_path(graph, source, target):
    distances, previous, steps, visited = dijkstra(
        graph, source, target
    )

    if distances[target] == float("inf"):
        return [], float("inf"), steps, visited

    path = reconstruct_path(previous, source, target)

    return path, distances[target], steps, visited


def open_google_maps(path):
    if not path:
        print("No route available to display.")
        return

    origin = path[0]
    destination = path[-1]

    params = {
        "api": "1",
        "origin": origin + ", India",
        "destination": destination + ", India",
        "travelmode": "driving"
    }

    # Include intermediate cities as waypoints
    if len(path) > 2:
        params["waypoints"] = "|".join(
            city + ", India" for city in path[1:-1]
        )

    url = "https://www.google.com/maps/dir/?" + urlencode(params)
    webbrowser.open(url)


def show_route(graph, source, target):
    path, distance, steps, visited = find_shortest_path(
        graph, source, target
    )

    print("\n" + "=" * 55)
    print("SHORTEST PATH RESULT")
    print("=" * 55)

    if not path:
        print(f"No route exists from {source} to {target}.")
        return

    print(f"Source city      : {source}")
    print(f"Destination city : {target}")
    print("Shortest route   : " + " -> ".join(path))
    print(f"Total distance   : {distance} km")
    print(f"Intermediate stops: {max(0, len(path) - 2)}")
    print(f"Cities visited   : {len(visited)}")

    # Estimated time at an assumed average speed of 60 km/h
    estimated_hours = distance / 60

    print(
        f"Estimated travel time: {estimated_hours:.2f} hours"
    )

    print("\nDistance between consecutive cities:")

    for city1, city2 in zip(path, path[1:]):
        road_distance = graph[city1][city2]
        print(f"{city1} -> {city2}: {road_distance} km")

    print("=" * 55)

    show_steps = input(
        "\nShow algorithm execution steps? (y/n): "
    ).strip().lower()

    if show_steps == "y":
        print("\nAlgorithm execution:")

        for step in steps:
            print(step)
        open_map = input(
        "\nOpen this route in Google Maps? (y/n): "
    ).strip().lower()

    if open_map == "y":
        params = {
            "api": "1",
            "origin": path[0] + ", India",
            "destination": path[-1] + ", India",
            "travelmode": "driving"
        }

        if len(path) > 2:
            params["waypoints"] = "|".join(
                city + ", India" for city in path[1:-1]
            )

        url = (
            "https://www.google.com/maps/dir/?"
            + urlencode(params)
        )

        webbrowser.open(url)
        print("Opening Google Maps...")

def show_all_distances(graph, source):
    distances, _, _, _ = dijkstra(graph, source)

    print(f"\nShortest distances from {source}")
    print("-" * 40)

    for city, distance in sorted(distances.items()):
        if distance == float("inf"):
            print(f"{city:15} Unreachable")
        else:
            print(f"{city:15} {distance:8.0f} km")


def show_cities(graph):
    print("\nAvailable cities:")
    print("-" * 40)

    for index, city in enumerate(sorted(graph), start=1):
        print(f"{index:2}. {city}")


def get_city(graph, message):
    lookup = {city.lower(): city for city in graph}

    while True:
        city = input(message).strip().lower()

        if city in lookup:
            return lookup[city]

        print("Invalid city. Please select a listed city.")


def main():
    graph = build_graph(ROADS)

    while True:
        print("\n" + "=" * 55)
        print("       DIJKSTRA SHORTEST PATH FINDER")
        print("=" * 55)
        print("1. Find shortest route")
        print("2. Find distances to all cities")
        print("3. Display available cities")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            show_cities(graph)

            source = get_city(
                graph, "\nEnter source city: "
            )
            target = get_city(
                graph, "Enter destination city: "
            )

            show_route(graph, source, target)

        elif choice == "2":
            show_cities(graph)

            source = get_city(
                graph, "\nEnter source city: "
            )

            show_all_distances(graph, source)

        elif choice == "3":
            show_cities(graph)

        elif choice == "4":
            print("Thank you for using Shortest Path Finder!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
