# python3

# Calculate the minimum amount of stops needed to refuel, considering inputs: total Distance, Miles traveled with a full tank, and distances until gas stations

def compute_min_refills(distance, tank, stops, currentStop, timesStopped):
    capacity = tank + currentStop
    
    if distance <= capacity:
        return timesStopped
    elif len(stops) == 0 or capacity < stops[0]:
        return -1

    curStopsLen = len(stops)
    while (len(stops) != 0 and capacity >= stops[0]):
        currentStop = stops[0]
        stops.pop(0)

    if(len(stops) != curStopsLen):
        timesStopped = timesStopped + 1

    return compute_min_refills(distance, tank, stops, currentStop, timesStopped)

if __name__ == '__main__':
    d = int(input())
    m = int(input())
    i = int(input())
    stops = []
    for str in input().split():
        stops.append(int(str))
    print(compute_min_refills(d, m, stops, 0, 0))
