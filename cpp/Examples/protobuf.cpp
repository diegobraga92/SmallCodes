#ifndef SIMPLE_CLIENT_H
#define SIMPLE_CLIENT_H

#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include <grpcpp/grpcpp.h>
#include "user.grpc.pb.h"
#include "todo.grpc.pb.h"

class SimpleGrpcClient {
public:
    // Constructor
    SimpleGrpcClient(const std::string& server_address);
    
    // User service methods
    bool GetUser(const std::string& user_id, simple::User* user);
    bool ListUsers(int page, int page_size, std::vector<simple::User>* users);
    bool CreateUser(const std::string& name, const std::string& email, 
                    int age, simple::User* created_user);
    
    // Todo service methods
    bool AddTodo(const std::string& title, const std::string& description, 
                 simple::Todo* todo);
    bool GetTodos(bool show_completed, std::vector<simple::Todo>* todos);
    bool CompleteTodo(const std::string& todo_id, simple::Todo* todo);
    
    // Health check
    bool CheckConnection();
    
private:
    std::shared_ptr<grpc::Channel> channel_;
    std::unique_ptr<simple::UserService::Stub> user_stub_;
    std::unique_ptr<simple::TodoService::Stub> todo_stub_;
    
    // Helper method to create context with timeout
    std::unique_ptr<grpc::ClientContext> CreateContext(int timeout_seconds = 10);
};

#endif // SIMPLE_CLIENT_H

#include "simple_client.h"
#include <chrono>

using grpc::Channel;
using grpc::ClientContext;
using grpc::ClientReader;
using grpc::Status;

SimpleGrpcClient::SimpleGrpcClient(const std::string& server_address) {
    // Create insecure channel (use SSL in production)
    channel_ = grpc::CreateChannel(server_address, 
                                   grpc::InsecureChannelCredentials());
    
    // Create stubs
    user_stub_ = simple::UserService::NewStub(channel_);
    todo_stub_ = simple::TodoService::NewStub(channel_);
    
    std::cout << "Connected to gRPC server at: " << server_address << std::endl;
}

bool SimpleGrpcClient::CheckConnection() {
    auto state = channel_->GetState(true);
    return state == GRPC_CHANNEL_READY;
}

std::unique_ptr<grpc::ClientContext> SimpleGrpcClient::CreateContext(int timeout_seconds) {
    auto context = std::make_unique<grpc::ClientContext>();
    auto deadline = std::chrono::system_clock::now() + 
                    std::chrono::seconds(timeout_seconds);
    context->set_deadline(deadline);
    return context;
}

// =============== User Service Methods ===============

bool SimpleGrpcClient::GetUser(const std::string& user_id, simple::User* user) {
    simple::GetUserRequest request;
    request.set_user_id(user_id);
    
    auto context = CreateContext();
    
    Status status = user_stub_->GetUser(context.get(), request, user);
    
    if (!status.ok()) {
        std::cerr << "GetUser RPC failed: " 
                  << status.error_code() << ": " 
                  << status.error_message() << std::endl;
        return false;
    }
    
    return true;
}

bool SimpleGrpcClient::ListUsers(int page, int page_size, 
                                std::vector<simple::User>* users) {
    simple::ListUsersRequest request;
    request.set_page(page);
    request.set_page_size(page_size);
    
    simple::ListUsersResponse response;
    auto context = CreateContext();
    
    Status status = user_stub_->ListUsers(context.get(), request, &response);
    
    if (!status.ok()) {
        std::cerr << "ListUsers RPC failed: " 
                  << status.error_code() << ": " 
                  << status.error_message() << std::endl;
        return false;
    }
    
    // Copy users to vector
    users->clear();
    for (const auto& user : response.users()) {
        users->push_back(user);
    }
    
    return true;
}

bool SimpleGrpcClient::CreateUser(const std::string& name, 
                                 const std::string& email, 
                                 int age,
                                 simple::User* created_user) {
    simple::CreateUserRequest request;
    request.set_name(name);
    request.set_email(email);
    request.set_age(age);
    
    auto context = CreateContext();
    
    Status status = user_stub_->CreateUser(context.get(), request, created_user);
    
    if (!status.ok()) {
        std::cerr << "CreateUser RPC failed: " 
                  << status.error_code() << ": " 
                  << status.error_message() << std::endl;
        return false;
    }
    
    return true;
}

// =============== Todo Service Methods ===============

bool SimpleGrpcClient::AddTodo(const std::string& title, 
                              const std::string& description, 
                              simple::Todo* todo) {
    simple::AddTodoRequest request;
    request.set_title(title);
    request.set_description(description);
    
    auto context = CreateContext();
    
    Status status = todo_stub_->AddTodo(context.get(), request, todo);
    
    if (!status.ok()) {
        std::cerr << "AddTodo RPC failed: " 
                  << status.error_code() << ": " 
                  << status.error_message() << std::endl;
        return false;
    }
    
    return true;
}

bool SimpleGrpcClient::GetTodos(bool show_completed, 
                               std::vector<simple::Todo>* todos) {
    simple::GetTodosRequest request;
    request.set_show_completed(show_completed);
    
    auto context = CreateContext();
    
    // This is a server streaming RPC
    std::unique_ptr<ClientReader<simple::Todo>> reader(
        todo_stub_->GetTodos(context.get(), request)
    );
    
    simple::Todo todo;
    todos->clear();
    
    while (reader->Read(&todo)) {
        todos->push_back(todo);
    }
    
    Status status = reader->Finish();
    
    if (!status.ok()) {
        std::cerr << "GetTodos RPC failed: " 
                  << status.error_code() << ": " 
                  << status.error_message() << std::endl;
        return false;
    }
    
    return true;
}

bool SimpleGrpcClient::CompleteTodo(const std::string& todo_id, 
                                   simple::Todo* todo) {
    simple::CompleteTodoRequest request;
    request.set_todo_id(todo_id);
    
    auto context = CreateContext();
    
    Status status = todo_stub_->CompleteTodo(context.get(), request, todo);
    
    if (!status.ok()) {
        std::cerr << "CompleteTodo RPC failed: " 
                  << status.error_code() << ": " 
                  << status.error_message() << std::endl;
        return false;
    }
    
    return true;
}

#include "simple_client.h"
#include <iostream>
#include <iomanip>
#include <chrono>

void PrintUser(const simple::User& user) {
    std::cout << "┌─────────────────────┐" << std::endl;
    std::cout << "│ User Details        │" << std::endl;
    std::cout << "├─────────────────────┤" << std::endl;
    std::cout << "│ ID:    " << std::setw(12) << user.id() << " │" << std::endl;
    std::cout << "│ Name:  " << std::setw(12) << user.name() << " │" << std::endl;
    std::cout << "│ Email: " << std::setw(12) << user.email() << " │" << std::endl;
    std::cout << "│ Age:   " << std::setw(12) << user.age() << " │" << std::endl;
    std::cout << "└─────────────────────┘" << std::endl;
}

void PrintTodo(const simple::Todo& todo) {
    std::cout << (todo.completed() ? "✓ " : "○ ") 
              << todo.title() 
              << " - " << todo.description() 
              << " [" << todo.id() << "]" << std::endl;
}

void DemoUserService(SimpleGrpcClient& client) {
    std::cout << "\n=== User Service Demo ===\n" << std::endl;
    
    // 1. Create a user
    simple::User new_user;
    std::cout << "Creating user John Doe..." << std::endl;
    
    if (client.CreateUser("John Doe", "john@example.com", 30, &new_user)) {
        std::cout << "User created successfully!" << std::endl;
        PrintUser(new_user);
    }
    
    // 2. Get user by ID
    simple::User retrieved_user;
    std::cout << "\nRetrieving user with ID " << new_user.id() << "..." << std::endl;
    
    if (client.GetUser(new_user.id(), &retrieved_user)) {
        PrintUser(retrieved_user);
    }
    
    // 3. List users
    std::vector<simple::User> users;
    std::cout << "\nListing users (page 1, 10 per page)..." << std::endl;
    
    if (client.ListUsers(1, 10, &users)) {
        std::cout << "Found " << users.size() << " users:" << std::endl;
        for (const auto& user : users) {
            std::cout << "  - " << user.name() << " (" << user.email() << ")" << std::endl;
        }
    }
}

void DemoTodoService(SimpleGrpcClient& client) {
    std::cout << "\n=== Todo Service Demo ===\n" << std::endl;
    
    // 1. Add todos
    simple::Todo todo1, todo2;
    
    std::cout << "Adding todos..." << std::endl;
    client.AddTodo("Buy groceries", "Milk, Eggs, Bread", &todo1);
    client.AddTodo("Finish report", "Quarterly sales report", &todo2);
    
    std::cout << "Added todos:" << std::endl;
    PrintTodo(todo1);
    PrintTodo(todo2);
    
    // 2. Get all todos (streaming)
    std::vector<simple::Todo> todos;
    std::cout << "\nStreaming todos from server..." << std::endl;
    
    if (client.GetTodos(true, &todos)) {
        std::cout << "Received " << todos.size() << " todos:" << std::endl;
        for (const auto& todo : todos) {
            PrintTodo(todo);
        }
    }
    
    // 3. Complete a todo
    std::cout << "\nCompleting todo: " << todo1.title() << "..." << std::endl;
    simple::Todo completed_todo;
    if (client.CompleteTodo(todo1.id(), &completed_todo)) {
        std::cout << "Todo completed!" << std::endl;
        PrintTodo(completed_todo);
    }
    
    // 4. Get only incomplete todos
    std::cout << "\nGetting incomplete todos..." << std::endl;
    std::vector<simple::Todo> incomplete_todos;
    if (client.GetTodos(false, &incomplete_todos)) {
        std::cout << "Incomplete todos: " << incomplete_todos.size() << std::endl;
        for (const auto& todo : incomplete_todos) {
            PrintTodo(todo);
        }
    }
}

void InteractiveMode(SimpleGrpcClient& client) {
    std::cout << "\n=== Interactive Mode ===\n" << std::endl;
    std::cout << "Commands:" << std::endl;
    std::cout << "  get_user <id>     - Get user by ID" << std::endl;
    std::cout << "  create_user       - Create new user" << std::endl;
    std::cout << "  list_users        - List all users" << std::endl;
    std::cout << "  add_todo          - Add new todo" << std::endl;
    std::cout << "  list_todos        - List all todos" << std::endl;
    std::cout << "  complete_todo <id>- Mark todo as complete" << std::endl;
    std::cout << "  help              - Show this help" << std::endl;
    std::cout << "  exit              - Exit program" << std::endl;
    
    std::string command;
    
    while (true) {
        std::cout << "\n> ";
        std::getline(std::cin, command);
        
        if (command == "exit") {
            break;
        } else if (command == "help") {
            // Help already shown
        } else if (command.find("get_user ") == 0) {
            std::string user_id = command.substr(9);
            simple::User user;
            if (client.GetUser(user_id, &user)) {
                PrintUser(user);
            }
        } else if (command == "create_user") {
            std::string name, email;
            int age;
            
            std::cout << "Name: ";
            std::getline(std::cin, name);
            std::cout << "Email: ";
            std::getline(std::cin, email);
            std::cout << "Age: ";
            std::cin >> age;
            std::cin.ignore(); // Clear newline
            
            simple::User new_user;
            if (client.CreateUser(name, email, age, &new_user)) {
                std::cout << "User created with ID: " << new_user.id() << std::endl;
                PrintUser(new_user);
            }
        } else if (command == "list_users") {
            std::vector<simple::User> users;
            if (client.ListUsers(1, 10, &users)) {
                std::cout << "Users (" << users.size() << "):" << std::endl;
                for (const auto& user : users) {
                    std::cout << "  - " << user.name() << " (" << user.email() 
                              << ") ID: " << user.id() << std::endl;
                }
            }
        } else if (command == "add_todo") {
            std::string title, description;
            
            std::cout << "Title: ";
            std::getline(std::cin, title);
            std::cout << "Description: ";
            std::getline(std::cin, description);
            
            simple::Todo todo;
            if (client.AddTodo(title, description, &todo)) {
                std::cout << "Todo added with ID: " << todo.id() << std::endl;
                PrintTodo(todo);
            }
        } else if (command == "list_todos") {
            std::vector<simple::Todo> todos;
            if (client.GetTodos(true, &todos)) {
                std::cout << "Todos (" << todos.size() << "):" << std::endl;
                for (const auto& todo : todos) {
                    PrintTodo(todo);
                }
            }
        } else if (command.find("complete_todo ") == 0) {
            std::string todo_id = command.substr(14);
            simple::Todo todo;
            if (client.CompleteTodo(todo_id, &todo)) {
                std::cout << "Todo completed!" << std::endl;
                PrintTodo(todo);
            }
        } else {
            std::cout << "Unknown command. Type 'help' for commands." << std::endl;
        }
    }
}

int main(int argc, char* argv[]) {
    // Default server address
    std::string server_address = "localhost:50051";
    
    // Parse command line arguments
    if (argc > 1) {
        server_address = argv[1];
    }
    
    std::cout << "=========================================" << std::endl;
    std::cout << "   Simple gRPC C++ Client" << std::endl;
    std::cout << "   Server: " << server_address << std::endl;
    std::cout << "=========================================\n" << std::endl;
    
    try {
        // Create client
        SimpleGrpcClient client(server_address);
        
        // Check connection
        std::cout << "Checking connection..." << std::endl;
        if (!client.CheckConnection()) {
            std::cout << "Failed to connect to server. Is it running?" << std::endl;
            return 1;
        }
        std::cout << "Connected successfully!\n" << std::endl;
        
        // Run demos or interactive mode based on command line
        if (argc > 2 && std::string(argv[2]) == "demo") {
            DemoUserService(client);
            DemoTodoService(client);
        } else if (argc > 2 && std::string(argv[2]) == "interactive") {
            InteractiveMode(client);
        } else {
            // Default: run both demos
            DemoUserService(client);
            DemoTodoService(client);
        }
        
    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
        return 1;
    }
    
    std::cout << "\n=========================================" << std::endl;
    std::cout << "   Client shutdown complete" << std::endl;
    std::cout << "=========================================" << std::endl;
    
    return 0;
}