# Uses python3

# Classical fractional knapsack problem, given a list of item values and weights, try and maximize the value that can fit in the knapsack

def get_optimal_value(capacity, weights, values):
    value = 0.
    
    # Uses a dictionary to map with v/w belongs to which index
    itemsDict = {}
    for i in range(0,len(weights)):
        itemsDict[i] = values[i] / weights[i]

    # Sorts v/w in crescent order so we know the last value is the one with the biggest cost/benefit
    itemsDictSorted = sorted(itemsDict.items(), key = lambda kv: kv[1])

    while capacity != 0 and len(itemsDictSorted) != 0:
        
        lastDictKey = itemsDictSorted[-1][0]

        if weights[lastDictKey] <= capacity:
            value = value + values[lastDictKey]
            capacity = capacity - weights[lastDictKey]
            itemsDictSorted.pop()
        else:
            frac = capacity / weights[lastDictKey]
            value = value + (values[lastDictKey] * frac)
            capacity = capacity - (weights[lastDictKey] * frac)

    return value


if __name__ == "__main__":
    n, capacity = map(int, input().split())
    values = []
    weights = []
    for i in range(n):
        v, w = map(int, input().split())
        values.append(v)
        weights.append(w)
    opt_value = get_optimal_value(capacity, weights, values)
    print("{:.4f}".format(opt_value))
