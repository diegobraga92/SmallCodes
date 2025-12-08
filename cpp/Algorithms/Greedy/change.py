# Uses python3

# Count the minimum amount of coins of value 1, 5 or 10 that can be used for change

def get_change(m):

    coinsCount = 0
    coinValues = [10, 5, 1]
    while m != 0:
        for v in range(0,3):
            if(m >= coinValues[v]):
                m = m - coinValues[v]
                coinsCount = coinsCount + 1
                break

    return coinsCount

if __name__ == '__main__':
    m = int(input())
    print(get_change(m))
