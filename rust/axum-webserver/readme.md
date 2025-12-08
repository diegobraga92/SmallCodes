# Rust Axum Server

## Dependencies:

1. Install Diesel:

`sudo apt install libpq-dev`

`cargo install diesel_cli --no-default-features --features postgres`

2. Install Docker (steps for WSL2):

`sudo apt install -y apt-transport-https ca-certificates curl software-properties-common`

`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`

`echo "deb [signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`

`sudo apt update`

`sudo apt install -y docker-ce docker-ce-cli containerd.io`

`sudo usermod -aG docker $USER`

`docker --version`

## Dev Environment:

From Linux, run 'dev_start.sh' to start Postgres in docker and the server

## TO-DO

1. To-Do List API (REST)

2. Basic Auth

3. Support File Upload

4. Rate-Limiting Middleware (limit requests)

5. Docker Image

6. OAuth 2.0 (Google)

7. Move To-Do to Module

8. Basic Expense Tracking as main app

9. Add To-Do List Module

10. Expense API (gRPC)

11. Distributed Task Queue (Redis, async workers)

12. Basic User Registration

13. User Management

14. Expense Categories

15. Support Custom Categories

16. Export to CSV & PDF

17. Import CSV

18. Search & Filter Expenses

19. Recurring Expenses (split expenses)

20. Add Currencies

21. Add Budgets

22. Add Notifications

23. Documentation

24. Unit Tests

25. Integration Tests

26. CI/CD Pipeline

27. Encryption at rest

28. Deployment

