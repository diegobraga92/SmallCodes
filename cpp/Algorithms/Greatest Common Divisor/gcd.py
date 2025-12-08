# Uses python3
import sys

def gcd_euc(a, b):
    
    big = max(a,b)
    small = min(a,b)

    if small > 0:
        return gcd_euc(small, big % small)
    else:
        return big

if __name__ == "__main__":
    a, b = map(int, input().split())
    print(gcd_euc(a, b))
