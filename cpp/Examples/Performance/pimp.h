#pragma once

#include <memory>
#include <string>

class Widget {
public:
    // Constructors / Destructor
    Widget();
    ~Widget();                     // must be defined in .cpp

    // Copy semantics
    Widget(const Widget&);          // deep copy
    Widget& operator=(const Widget&);

    // Move semantics
    Widget(Widget&&) noexcept;      // cheap move
    Widget& operator=(Widget&&) noexcept;

    // Public API
    void set_name(std::string name);
    const std::string& name() const;

private:
    // Forward declaration only — no headers leaked
    struct Impl;

    std::unique_ptr<Impl> impl_;    // owning pointer
};
