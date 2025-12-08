#Uses python3

# Given the revenue an ad generates by click and the amount of clicks each ad spot generate per day, maximize profit

def max_dot_product(ads, slotClicks):
    ads = sorted(ads, reverse=True)
    slotClicks = sorted(slotClicks, reverse=True)
    revenue = 0

    for i in range(len(ads)):
        revenue = revenue + ads[i] * slotClicks[i]

    return revenue

if __name__ == '__main__':
    n = int(input())
    ads = list(map(int, input().split()))
    slotClicks = list(map(int, input().split()))

    print(max_dot_product(ads, slotClicks))
    
