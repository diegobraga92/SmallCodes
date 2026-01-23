import redis

def main():
    # Connect to Redis (localhost:6379)
    client = redis.Redis(host='localhost', port=6379, db=0)

    # Set a key
    client.set("name", "Diego")

    # Get the key
    value = client.get("name")
    print("Value from Redis:", value.decode())  # decode bytes → string

    # Increment a counter
    client.incr("counter")
    print("Counter:", client.get("counter").decode())

if __name__ == "__main__":
    main()
