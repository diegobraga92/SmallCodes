#include <iostream>
#include <memory>

// Base interface
class Shape {
public:
    // Virtual destructor is REQUIRED for polymorphic base classes
    virtual ~Shape() = default;

    // Virtual function: dispatched at runtime
    virtual double area() const {
        return 0.0;
    }
};


class Rectangle : public Shape {
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}

    // override:
    //  - Compiler checks that this actually overrides a virtual function
    //  - Prevents subtle bugs (wrong signature)
    double area() const override {
        return w_ * h_;
    }

private:
    double w_;
    double h_;
};

class Square final : public Shape {
public:
    explicit Square(double side) : side_(side) {}

    double area() const override {
        return side_ * side_;
    }

private:
    double side_;
};

class Circle : public Shape {
public:
    explicit Circle(double r) : r_(r) {}

    double area() const final override {
        return 3.14159 * r_ * r_;
    }

private:
    double r_;
};


int main() {
    // Polymorphic container
    std::unique_ptr<Shape> shapes[] = {
        std::make_unique<Rectangle>(3.0, 4.0),
        std::make_unique<Square>(5.0),
        std::make_unique<Circle>(2.0)
    };

    for (const auto& s : shapes) {
        // Calls correct derived implementation at runtime
        std::cout << s->area() << "\n";
    }
}




