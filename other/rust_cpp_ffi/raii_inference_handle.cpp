extern "C" {
    void* engine_create();
    void  engine_destroy(void*);
    int   engine_run(void*, const char* input);
}

class Engine {
public:
    Engine() : handle_(engine_create()) {}

    ~Engine() {
        if (handle_) {
            engine_destroy(handle_);
        }
    }

    // Non-copyable
    Engine(const Engine&) = delete;
    Engine& operator=(const Engine&) = delete;

    // Movable
    Engine(Engine&& other) noexcept : handle_(other.handle_) {
        other.handle_ = nullptr;
    }

    Engine& operator=(Engine&& other) noexcept {
        if (this != &other) {
            if (handle_) {
                engine_destroy(handle_);
            }
            handle_ = other.handle_;
            other.handle_ = nullptr;
        }
        return *this;
    }

    int run(const char* input) {
        return engine_run(handle_, input);
    }

private:
    void* handle_;
};
