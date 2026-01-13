#include "pimpl.h"

#include <iostream>   // heavy includes hidden here

// Full definition now visible
struct Widget::Impl {
    std::string name;

    Impl() = default;
    Impl(const Impl& other) : name(other.name) {}

    void set_name(std::string n) {
        name = std::move(n);
    }
};

// Public interface implementations

Widget::Widget()
    : impl_(std::make_unique<Impl>()) {}

Widget::~Widget() = default;

Widget::Widget(const Widget& other)
    : impl_(std::make_unique<Impl>(*other.impl_)) {}

Widget& Widget::operator=(const Widget& other) {
    if (this != &other) {
        impl_ = std::make_unique<Impl>(*other.impl_);
    }
    return *this;
}

Widget::Widget(Widget&& other) noexcept
    : impl_(std::move(other.impl_)) {}

Widget& Widget::operator=(Widget&& other) noexcept {
    if (this != &other) {
        impl_ = std::move(other.impl_);
    }
    return *this;
}

void Widget::set_name(std::string name) {
    impl_->set_name(std::move(name));
}

const std::string& Widget::name() const {
    return impl_->name;
}
