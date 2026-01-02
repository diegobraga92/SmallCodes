#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>

// ============================================================================
// 1. PROBLEM: TEMPORARY OBJECTS IN VECTOR OPERATIONS
// ============================================================================

void demonstrate_problem() {
    std::cout << "\n=== PROBLEM: TEMPORARY OBJECTS ===\n";
    
    std::vector<double> a = {1, 2, 3, 4, 5};
    std::vector<double> b = {2, 3, 4, 5, 6};
    std::vector<double> c = {3, 4, 5, 6, 7};
    
    // Traditional approach: Creates temporaries
    std::vector<double> result1(a.size());
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // This creates temporary vectors for intermediate results
    for (size_t i = 0; i < a.size(); ++i) {
        result1[i] = a[i] * 2 + b[i] * 3 + c[i] * 4;
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Traditional: " << duration.count() << " microseconds\n";
    std::cout << "Result: ";
    for (double x : result1) std::cout << x << " ";
    std::cout << "\n";
    
    // Problem: Expression like (a + b) * c creates temporaries
    // Inefficient for large vectors or complex expressions
}

// ============================================================================
// 2. EXPRESSION TEMPLATES SOLUTION
// ============================================================================

// Base class for all expressions
template<typename E>
class VecExpression {
public:
    double operator[](size_t i) const { 
        return static_cast<const E&>(*this)[i];
    }
    
    size_t size() const { 
        return static_cast<const E&>(*this).size();
    }
};

// Concrete vector class
template<typename T>
class Vec : public VecExpression<Vec<T>> {
    std::vector<T> data;
    
public:
    Vec() = default;
    
    explicit Vec(size_t n) : data(n) {}
    
    Vec(std::initializer_list<T> init) : data(init) {}
    
    // Construction from any expression
    template<typename E>
    Vec(const VecExpression<E>& expr) : data(expr.size()) {
        for (size_t i = 0; i < data.size(); ++i) {
            data[i] = expr[i];
        }
    }
    
    // Assignment from any expression
    template<typename E>
    Vec& operator=(const VecExpression<E>& expr) {
        data.resize(expr.size());
        for (size_t i = 0; i < data.size(); ++i) {
            data[i] = expr[i];
        }
        return *this;
    }
    
    T& operator[](size_t i) { return data[i]; }
    const T& operator[](size_t i) const { return data[i]; }
    
    size_t size() const { return data.size(); }
};

// Binary operation expression template
template<typename E1, typename E2, typename Op>
class VecBinaryOp : public VecExpression<VecBinaryOp<E1, E2, Op>> {
    const E1& lhs;
    const E2& rhs;
    Op op;
    
public:
    VecBinaryOp(const E1& l, const E2& r, Op o = Op{}) 
        : lhs(l), rhs(r), op(o) {}
    
    auto operator[](size_t i) const {
        return op(lhs[i], rhs[i]);
    }
    
    size_t size() const { 
        return lhs.size();  // Assume same size
    }
};

// Unary operation expression template
template<typename E, typename Op>
class VecUnaryOp : public VecExpression<VecUnaryOp<E, Op>> {
    const E& expr;
    Op op;
    
public:
    VecUnaryOp(const E& e, Op o = Op{}) : expr(e), op(o) {}
    
    auto operator[](size_t i) const {
        return op(expr[i]);
    }
    
    size_t size() const { return expr.size(); }
};

// Scalar multiplication expression
template<typename E>
class VecScalarMul : public VecExpression<VecScalarMul<E>> {
    const E& expr;
    double scalar;
    
public:
    VecScalarMul(const E& e, double s) : expr(e), scalar(s) {}
    
    auto operator[](size_t i) const {
        return expr[i] * scalar;
    }
    
    size_t size() const { return expr.size(); }
};

// Function objects for operations
struct AddOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a + b; }
};

struct SubOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a - b; }
};

struct MulOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a * b; }
};

struct DivOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a / b; }
};

struct SqrtOp {
    template<typename T>
    auto operator()(T a) const { return std::sqrt(a); }
};

struct SinOp {
    template<typename T>
    auto operator()(T a) const { return std::sin(a); }
};

// Operator overloads to create expression templates
template<typename E1, typename E2>
auto operator+(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, AddOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator-(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, SubOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator*(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, MulOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator/(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, DivOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E>
auto sqrt(const VecExpression<E>& expr) {
    return VecUnaryOp<E, SqrtOp>(static_cast<const E&>(expr));
}

template<typename E>
auto sin(const VecExpression<E>& expr) {
    return VecUnaryOp<E, SinOp>(static_cast<const E&>(expr));
}

// Scalar-vector operations
template<typename E>
auto operator*(double scalar, const VecExpression<E>& expr) {
    return VecScalarMul<E>(static_cast<const E&>(expr), scalar);
}

template<typename E>
auto operator*(const VecExpression<E>& expr, double scalar) {
    return VecScalarMul<E>(static_cast<const E&>(expr), scalar);
}

void demonstrate_expression_templates() {
    std::cout << "\n=== EXPRESSION TEMPLATES SOLUTION ===\n";
    
    Vec<double> a = {1, 2, 3, 4, 5};
    Vec<double> b = {2, 3, 4, 5, 6};
    Vec<double> c = {3, 4, 5, 6, 7};
    Vec<double> result(a.size());
    
    // Complex expression - NO temporaries created!
    auto start = std::chrono::high_resolution_clock::now();
    
    // Expression template builds computation graph
    // Evaluation happens only when assigned to result
    result = 2.0 * a + 3.0 * b + 4.0 * c;
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Expression Templates: " << duration.count() << " microseconds\n";
    std::cout << "Result: ";
    for (size_t i = 0; i < result.size(); ++i) {
        std::cout << result[i] << " ";
    }
    std::cout << "\n";
    
    // More complex expressions
    std::cout << "\nMore complex expressions:\n";
    
    Vec<double> d = {1, 4, 9, 16, 25};
    Vec<double> result2(a.size());
    
    result2 = sqrt(d) + sin(a) * b;
    
    std::cout << "sqrt(d) + sin(a) * b = ";
    for (size_t i = 0; i < result2.size(); ++i) {
        std::cout << result2[i] << " ";
    }
    std::cout << "\n";
    
    // Chained operations
    Vec<double> result3 = a + b - c * 2.0;
    std::cout << "\na + b - c * 2.0 = ";
    for (size_t i = 0; i < result3.size(); ++i) {
        std::cout << result3[i] << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 3. LAZY EVALUATION WITH EXPRESSION TEMPLATES
// ============================================================================

template<typename T>
class LazyVector {
    mutable std::vector<T>* data = nullptr;
    
    // Expression type
    template<typename E>
    class Expression {
        const E& expr;
        
    public:
        Expression(const E& e) : expr(e) {}
        
        operator std::vector<T>() const {
            std::vector<T> result(expr.size());
            for (size_t i = 0; i < result.size(); ++i) {
                result[i] = expr[i];
            }
            return result;
        }
    };
    
public:
    template<typename E>
    LazyVector(const VecExpression<E>& expr) 
        : data(new std::vector<T>(Expression<E>(static_cast<const E&>(expr)))) {}
    
    ~LazyVector() { delete data; }
    
    const T& operator[](size_t i) const {
        return (*data)[i];
    }
    
    size_t size() const { return data->size(); }
};

void demonstrate_lazy_evaluation() {
    std::cout << "\n=== LAZY EVALUATION ===\n";
    
    Vec<double> x = {1, 2, 3, 4, 5};
    Vec<double> y = {2, 3, 4, 5, 6};
    
    // Expression is stored, not evaluated
    auto expr = x + y * 2.0;
    
    // Evaluation happens only when needed
    LazyVector<double> lazy_result(expr);
    
    std::cout << "Lazy evaluated result: ";
    for (size_t i = 0; i < lazy_result.size(); ++i) {
        std::cout << lazy_result[i] << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 4. REAL-WORLD EXAMPLE: LINEAR ALGEBRA
// ============================================================================

template<typename T>
class Matrix {
    std::vector<std::vector<T>> data;
    size_t rows, cols;
    
public:
    Matrix(size_t r, size_t c) : rows(r), cols(c), data(r, std::vector<T>(c)) {}
    
    std::vector<T>& operator[](size_t i) { return data[i]; }
    const std::vector<T>& operator[](size_t i) const { return data[i]; }
    
    size_t num_rows() const { return rows; }
    size_t num_cols() const { return cols; }
    
    // Matrix multiplication using expression templates
    template<typename E1, typename E2>
    static Matrix multiply(const E1& a, const E2& b) {
        size_t n = a.num_rows();
        size_t m = a.num_cols();
        size_t p = b.num_cols();
        
        Matrix result(n, p);
        
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < p; ++j) {
                T sum = 0;
                for (size_t k = 0; k < m; ++k) {
                    sum += a[i][k] * b[k][j];
                }
                result[i][j] = sum;
            }
        }
        
        return result;
    }
};

void demonstrate_matrix_operations() {
    std::cout << "\n=== MATRIX OPERATIONS ===\n";
    
    Matrix<double> A(2, 3);
    Matrix<double> B(3, 2);
    
    // Initialize matrices
    A[0] = {1, 2, 3};
    A[1] = {4, 5, 6};
    
    B[0] = {7, 8};
    B[1] = {9, 10};
    B[2] = {11, 12};
    
    // Matrix multiplication
    auto C = Matrix<double>::multiply(A, B);
    
    std::cout << "Matrix multiplication result:\n";
    for (size_t i = 0; i < C.num_rows(); ++i) {
        for (size_t j = 0; j < C.num_cols(); ++j) {
            std::cout << C[i][j] << " ";
        }
        std::cout << "\n";
    }
}

// ============================================================================
// 5. BENEFITS AND USE CASES
// ============================================================================

void explain_benefits() {
    std::cout << "\n=== EXPRESSION TEMPLATES BENEFITS ===\n";
    
    std::cout << "\nBenefits:\n";
    std::cout << "1. Eliminates temporary objects\n";
    std::cout << "2. Enables lazy evaluation\n";
    std::cout << "3. Fuses operations for better cache locality\n";
    std::cout << "4. Compile-time expression optimization\n";
    std::cout << "5. Clean, mathematical syntax\n";
    
    std::cout << "\nUse Cases:\n";
    std::cout << "1. Numerical libraries (Eigen, Blaze)\n";
    std::cout << "2. Vector/matrix operations\n";
    std::cout << "3. Domain-specific languages\n";
    std::cout << "4. Query optimization in databases\n";
    std::cout << "5. Image processing pipelines\n";
    
    std::cout << "\nExample from Eigen library:\n";
    std::cout << "VectorXd x(100), y(100), z(100);\n";
    std::cout << "// No temporaries created:\n";
    std::cout << "z = 2 * x + 3 * y;\n";
    
    std::cout << "\nKey Insight:\n";
    std::cout << "- Templates create expression trees at compile time\n";
    std::cout << "- Evaluation happens in a single pass\n";
    std::cout << "- Each element computed once, not stored intermediately\n";
}


#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>

// ============================================================================
// 1. PROBLEM: TEMPORARY OBJECTS IN VECTOR OPERATIONS
// ============================================================================

void demonstrate_problem() {
    std::cout << "\n=== PROBLEM: TEMPORARY OBJECTS ===\n";
    
    std::vector<double> a = {1, 2, 3, 4, 5};
    std::vector<double> b = {2, 3, 4, 5, 6};
    std::vector<double> c = {3, 4, 5, 6, 7};
    
    // Traditional approach: Creates temporaries
    std::vector<double> result1(a.size());
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // This creates temporary vectors for intermediate results
    for (size_t i = 0; i < a.size(); ++i) {
        result1[i] = a[i] * 2 + b[i] * 3 + c[i] * 4;
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Traditional: " << duration.count() << " microseconds\n";
    std::cout << "Result: ";
    for (double x : result1) std::cout << x << " ";
    std::cout << "\n";
    
    // Problem: Expression like (a + b) * c creates temporaries
    // Inefficient for large vectors or complex expressions
}

// ============================================================================
// 2. EXPRESSION TEMPLATES SOLUTION
// ============================================================================

// Base class for all expressions
template<typename E>
class VecExpression {
public:
    double operator[](size_t i) const { 
        return static_cast<const E&>(*this)[i];
    }
    
    size_t size() const { 
        return static_cast<const E&>(*this).size();
    }
};

// Concrete vector class
template<typename T>
class Vec : public VecExpression<Vec<T>> {
    std::vector<T> data;
    
public:
    Vec() = default;
    
    explicit Vec(size_t n) : data(n) {}
    
    Vec(std::initializer_list<T> init) : data(init) {}
    
    // Construction from any expression
    template<typename E>
    Vec(const VecExpression<E>& expr) : data(expr.size()) {
        for (size_t i = 0; i < data.size(); ++i) {
            data[i] = expr[i];
        }
    }
    
    // Assignment from any expression
    template<typename E>
    Vec& operator=(const VecExpression<E>& expr) {
        data.resize(expr.size());
        for (size_t i = 0; i < data.size(); ++i) {
            data[i] = expr[i];
        }
        return *this;
    }
    
    T& operator[](size_t i) { return data[i]; }
    const T& operator[](size_t i) const { return data[i]; }
    
    size_t size() const { return data.size(); }
};

// Binary operation expression template
template<typename E1, typename E2, typename Op>
class VecBinaryOp : public VecExpression<VecBinaryOp<E1, E2, Op>> {
    const E1& lhs;
    const E2& rhs;
    Op op;
    
public:
    VecBinaryOp(const E1& l, const E2& r, Op o = Op{}) 
        : lhs(l), rhs(r), op(o) {}
    
    auto operator[](size_t i) const {
        return op(lhs[i], rhs[i]);
    }
    
    size_t size() const { 
        return lhs.size();  // Assume same size
    }
};

// Unary operation expression template
template<typename E, typename Op>
class VecUnaryOp : public VecExpression<VecUnaryOp<E, Op>> {
    const E& expr;
    Op op;
    
public:
    VecUnaryOp(const E& e, Op o = Op{}) : expr(e), op(o) {}
    
    auto operator[](size_t i) const {
        return op(expr[i]);
    }
    
    size_t size() const { return expr.size(); }
};

// Scalar multiplication expression
template<typename E>
class VecScalarMul : public VecExpression<VecScalarMul<E>> {
    const E& expr;
    double scalar;
    
public:
    VecScalarMul(const E& e, double s) : expr(e), scalar(s) {}
    
    auto operator[](size_t i) const {
        return expr[i] * scalar;
    }
    
    size_t size() const { return expr.size(); }
};

// Function objects for operations
struct AddOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a + b; }
};

struct SubOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a - b; }
};

struct MulOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a * b; }
};

struct DivOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a / b; }
};

struct SqrtOp {
    template<typename T>
    auto operator()(T a) const { return std::sqrt(a); }
};

struct SinOp {
    template<typename T>
    auto operator()(T a) const { return std::sin(a); }
};

// Operator overloads to create expression templates
template<typename E1, typename E2>
auto operator+(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, AddOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator-(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, SubOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator*(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, MulOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator/(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, DivOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E>
auto sqrt(const VecExpression<E>& expr) {
    return VecUnaryOp<E, SqrtOp>(static_cast<const E&>(expr));
}

template<typename E>
auto sin(const VecExpression<E>& expr) {
    return VecUnaryOp<E, SinOp>(static_cast<const E&>(expr));
}

// Scalar-vector operations
template<typename E>
auto operator*(double scalar, const VecExpression<E>& expr) {
    return VecScalarMul<E>(static_cast<const E&>(expr), scalar);
}

template<typename E>
auto operator*(const VecExpression<E>& expr, double scalar) {
    return VecScalarMul<E>(static_cast<const E&>(expr), scalar);
}

void demonstrate_expression_templates() {
    std::cout << "\n=== EXPRESSION TEMPLATES SOLUTION ===\n";
    
    Vec<double> a = {1, 2, 3, 4, 5};
    Vec<double> b = {2, 3, 4, 5, 6};
    Vec<double> c = {3, 4, 5, 6, 7};
    Vec<double> result(a.size());
    
    // Complex expression - NO temporaries created!
    auto start = std::chrono::high_resolution_clock::now();
    
    // Expression template builds computation graph
    // Evaluation happens only when assigned to result
    result = 2.0 * a + 3.0 * b + 4.0 * c;
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Expression Templates: " << duration.count() << " microseconds\n";
    std::cout << "Result: ";
    for (size_t i = 0; i < result.size(); ++i) {
        std::cout << result[i] << " ";
    }
    std::cout << "\n";
    
    // More complex expressions
    std::cout << "\nMore complex expressions:\n";
    
    Vec<double> d = {1, 4, 9, 16, 25};
    Vec<double> result2(a.size());
    
    result2 = sqrt(d) + sin(a) * b;
    
    std::cout << "sqrt(d) + sin(a) * b = ";
    for (size_t i = 0; i < result2.size(); ++i) {
        std::cout << result2[i] << " ";
    }
    std::cout << "\n";
    
    // Chained operations
    Vec<double> result3 = a + b - c * 2.0;
    std::cout << "\na + b - c * 2.0 = ";
    for (size_t i = 0; i < result3.size(); ++i) {
        std::cout << result3[i] << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 3. LAZY EVALUATION WITH EXPRESSION TEMPLATES
// ============================================================================

template<typename T>
class LazyVector {
    mutable std::vector<T>* data = nullptr;
    
    // Expression type
    template<typename E>
    class Expression {
        const E& expr;
        
    public:
        Expression(const E& e) : expr(e) {}
        
        operator std::vector<T>() const {
            std::vector<T> result(expr.size());
            for (size_t i = 0; i < result.size(); ++i) {
                result[i] = expr[i];
            }
            return result;
        }
    };
    
public:
    template<typename E>
    LazyVector(const VecExpression<E>& expr) 
        : data(new std::vector<T>(Expression<E>(static_cast<const E&>(expr)))) {}
    
    ~LazyVector() { delete data; }
    
    const T& operator[](size_t i) const {
        return (*data)[i];
    }
    
    size_t size() const { return data->size(); }
};

void demonstrate_lazy_evaluation() {
    std::cout << "\n=== LAZY EVALUATION ===\n";
    
    Vec<double> x = {1, 2, 3, 4, 5};
    Vec<double> y = {2, 3, 4, 5, 6};
    
    // Expression is stored, not evaluated
    auto expr = x + y * 2.0;
    
    // Evaluation happens only when needed
    LazyVector<double> lazy_result(expr);
    
    std::cout << "Lazy evaluated result: ";
    for (size_t i = 0; i < lazy_result.size(); ++i) {
        std::cout << lazy_result[i] << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 4. REAL-WORLD EXAMPLE: LINEAR ALGEBRA
// ============================================================================

template<typename T>
class Matrix {
    std::vector<std::vector<T>> data;
    size_t rows, cols;
    
public:
    Matrix(size_t r, size_t c) : rows(r), cols(c), data(r, std::vector<T>(c)) {}
    
    std::vector<T>& operator[](size_t i) { return data[i]; }
    const std::vector<T>& operator[](size_t i) const { return data[i]; }
    
    size_t num_rows() const { return rows; }
    size_t num_cols() const { return cols; }
    
    // Matrix multiplication using expression templates
    template<typename E1, typename E2>
    static Matrix multiply(const E1& a, const E2& b) {
        size_t n = a.num_rows();
        size_t m = a.num_cols();
        size_t p = b.num_cols();
        
        Matrix result(n, p);
        
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < p; ++j) {
                T sum = 0;
                for (size_t k = 0; k < m; ++k) {
                    sum += a[i][k] * b[k][j];
                }
                result[i][j] = sum;
            }
        }
        
        return result;
    }
};

void demonstrate_matrix_operations() {
    std::cout << "\n=== MATRIX OPERATIONS ===\n";
    
    Matrix<double> A(2, 3);
    Matrix<double> B(3, 2);
    
    // Initialize matrices
    A[0] = {1, 2, 3};
    A[1] = {4, 5, 6};
    
    B[0] = {7, 8};
    B[1] = {9, 10};
    B[2] = {11, 12};
    
    // Matrix multiplication
    auto C = Matrix<double>::multiply(A, B);
    
    std::cout << "Matrix multiplication result:\n";
    for (size_t i = 0; i < C.num_rows(); ++i) {
        for (size_t j = 0; j < C.num_cols(); ++j) {
            std::cout << C[i][j] << " ";
        }
        std::cout << "\n";
    }
}

// ============================================================================
// 5. BENEFITS AND USE CASES
// ============================================================================

void explain_benefits() {
    std::cout << "\n=== EXPRESSION TEMPLATES BENEFITS ===\n";
    
    std::cout << "\nBenefits:\n";
    std::cout << "1. Eliminates temporary objects\n";
    std::cout << "2. Enables lazy evaluation\n";
    std::cout << "3. Fuses operations for better cache locality\n";
    std::cout << "4. Compile-time expression optimization\n";
    std::cout << "5. Clean, mathematical syntax\n";
    
    std::cout << "\nUse Cases:\n";
    std::cout << "1. Numerical libraries (Eigen, Blaze)\n";
    std::cout << "2. Vector/matrix operations\n";
    std::cout << "3. Domain-specific languages\n";
    std::cout << "4. Query optimization in databases\n";
    std::cout << "5. Image processing pipelines\n";
    
    std::cout << "\nExample from Eigen library:\n";
    std::cout << "VectorXd x(100), y(100), z(100);\n";
    std::cout << "// No temporaries created:\n";
    std::cout << "z = 2 * x + 3 * y;\n";
    
    std::cout << "\nKey Insight:\n";
    std::cout << "- Templates create expression trees at compile time\n";
    std::cout << "- Evaluation happens in a single pass\n";
    std::cout << "- Each element computed once, not stored intermediately\n";
}


#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>

// ============================================================================
// 1. PROBLEM: TEMPORARY OBJECTS IN VECTOR OPERATIONS
// ============================================================================

void demonstrate_problem() {
    std::cout << "\n=== PROBLEM: TEMPORARY OBJECTS ===\n";
    
    std::vector<double> a = {1, 2, 3, 4, 5};
    std::vector<double> b = {2, 3, 4, 5, 6};
    std::vector<double> c = {3, 4, 5, 6, 7};
    
    // Traditional approach: Creates temporaries
    std::vector<double> result1(a.size());
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // This creates temporary vectors for intermediate results
    for (size_t i = 0; i < a.size(); ++i) {
        result1[i] = a[i] * 2 + b[i] * 3 + c[i] * 4;
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Traditional: " << duration.count() << " microseconds\n";
    std::cout << "Result: ";
    for (double x : result1) std::cout << x << " ";
    std::cout << "\n";
    
    // Problem: Expression like (a + b) * c creates temporaries
    // Inefficient for large vectors or complex expressions
}

// ============================================================================
// 2. EXPRESSION TEMPLATES SOLUTION
// ============================================================================

// Base class for all expressions
template<typename E>
class VecExpression {
public:
    double operator[](size_t i) const { 
        return static_cast<const E&>(*this)[i];
    }
    
    size_t size() const { 
        return static_cast<const E&>(*this).size();
    }
};

// Concrete vector class
template<typename T>
class Vec : public VecExpression<Vec<T>> {
    std::vector<T> data;
    
public:
    Vec() = default;
    
    explicit Vec(size_t n) : data(n) {}
    
    Vec(std::initializer_list<T> init) : data(init) {}
    
    // Construction from any expression
    template<typename E>
    Vec(const VecExpression<E>& expr) : data(expr.size()) {
        for (size_t i = 0; i < data.size(); ++i) {
            data[i] = expr[i];
        }
    }
    
    // Assignment from any expression
    template<typename E>
    Vec& operator=(const VecExpression<E>& expr) {
        data.resize(expr.size());
        for (size_t i = 0; i < data.size(); ++i) {
            data[i] = expr[i];
        }
        return *this;
    }
    
    T& operator[](size_t i) { return data[i]; }
    const T& operator[](size_t i) const { return data[i]; }
    
    size_t size() const { return data.size(); }
};

// Binary operation expression template
template<typename E1, typename E2, typename Op>
class VecBinaryOp : public VecExpression<VecBinaryOp<E1, E2, Op>> {
    const E1& lhs;
    const E2& rhs;
    Op op;
    
public:
    VecBinaryOp(const E1& l, const E2& r, Op o = Op{}) 
        : lhs(l), rhs(r), op(o) {}
    
    auto operator[](size_t i) const {
        return op(lhs[i], rhs[i]);
    }
    
    size_t size() const { 
        return lhs.size();  // Assume same size
    }
};

// Unary operation expression template
template<typename E, typename Op>
class VecUnaryOp : public VecExpression<VecUnaryOp<E, Op>> {
    const E& expr;
    Op op;
    
public:
    VecUnaryOp(const E& e, Op o = Op{}) : expr(e), op(o) {}
    
    auto operator[](size_t i) const {
        return op(expr[i]);
    }
    
    size_t size() const { return expr.size(); }
};

// Scalar multiplication expression
template<typename E>
class VecScalarMul : public VecExpression<VecScalarMul<E>> {
    const E& expr;
    double scalar;
    
public:
    VecScalarMul(const E& e, double s) : expr(e), scalar(s) {}
    
    auto operator[](size_t i) const {
        return expr[i] * scalar;
    }
    
    size_t size() const { return expr.size(); }
};

// Function objects for operations
struct AddOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a + b; }
};

struct SubOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a - b; }
};

struct MulOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a * b; }
};

struct DivOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a / b; }
};

struct SqrtOp {
    template<typename T>
    auto operator()(T a) const { return std::sqrt(a); }
};

struct SinOp {
    template<typename T>
    auto operator()(T a) const { return std::sin(a); }
};

// Operator overloads to create expression templates
template<typename E1, typename E2>
auto operator+(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, AddOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator-(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, SubOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator*(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, MulOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator/(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, DivOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E>
auto sqrt(const VecExpression<E>& expr) {
    return VecUnaryOp<E, SqrtOp>(static_cast<const E&>(expr));
}

template<typename E>
auto sin(const VecExpression<E>& expr) {
    return VecUnaryOp<E, SinOp>(static_cast<const E&>(expr));
}

// Scalar-vector operations
template<typename E>
auto operator*(double scalar, const VecExpression<E>& expr) {
    return VecScalarMul<E>(static_cast<const E&>(expr), scalar);
}

template<typename E>
auto operator*(const VecExpression<E>& expr, double scalar) {
    return VecScalarMul<E>(static_cast<const E&>(expr), scalar);
}

void demonstrate_expression_templates() {
    std::cout << "\n=== EXPRESSION TEMPLATES SOLUTION ===\n";
    
    Vec<double> a = {1, 2, 3, 4, 5};
    Vec<double> b = {2, 3, 4, 5, 6};
    Vec<double> c = {3, 4, 5, 6, 7};
    Vec<double> result(a.size());
    
    // Complex expression - NO temporaries created!
    auto start = std::chrono::high_resolution_clock::now();
    
    // Expression template builds computation graph
    // Evaluation happens only when assigned to result
    result = 2.0 * a + 3.0 * b + 4.0 * c;
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Expression Templates: " << duration.count() << " microseconds\n";
    std::cout << "Result: ";
    for (size_t i = 0; i < result.size(); ++i) {
        std::cout << result[i] << " ";
    }
    std::cout << "\n";
    
    // More complex expressions
    std::cout << "\nMore complex expressions:\n";
    
    Vec<double> d = {1, 4, 9, 16, 25};
    Vec<double> result2(a.size());
    
    result2 = sqrt(d) + sin(a) * b;
    
    std::cout << "sqrt(d) + sin(a) * b = ";
    for (size_t i = 0; i < result2.size(); ++i) {
        std::cout << result2[i] << " ";
    }
    std::cout << "\n";
    
    // Chained operations
    Vec<double> result3 = a + b - c * 2.0;
    std::cout << "\na + b - c * 2.0 = ";
    for (size_t i = 0; i < result3.size(); ++i) {
        std::cout << result3[i] << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 3. LAZY EVALUATION WITH EXPRESSION TEMPLATES
// ============================================================================

template<typename T>
class LazyVector {
    mutable std::vector<T>* data = nullptr;
    
    // Expression type
    template<typename E>
    class Expression {
        const E& expr;
        
    public:
        Expression(const E& e) : expr(e) {}
        
        operator std::vector<T>() const {
            std::vector<T> result(expr.size());
            for (size_t i = 0; i < result.size(); ++i) {
                result[i] = expr[i];
            }
            return result;
        }
    };
    
public:
    template<typename E>
    LazyVector(const VecExpression<E>& expr) 
        : data(new std::vector<T>(Expression<E>(static_cast<const E&>(expr)))) {}
    
    ~LazyVector() { delete data; }
    
    const T& operator[](size_t i) const {
        return (*data)[i];
    }
    
    size_t size() const { return data->size(); }
};

void demonstrate_lazy_evaluation() {
    std::cout << "\n=== LAZY EVALUATION ===\n";
    
    Vec<double> x = {1, 2, 3, 4, 5};
    Vec<double> y = {2, 3, 4, 5, 6};
    
    // Expression is stored, not evaluated
    auto expr = x + y * 2.0;
    
    // Evaluation happens only when needed
    LazyVector<double> lazy_result(expr);
    
    std::cout << "Lazy evaluated result: ";
    for (size_t i = 0; i < lazy_result.size(); ++i) {
        std::cout << lazy_result[i] << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 4. REAL-WORLD EXAMPLE: LINEAR ALGEBRA
// ============================================================================

template<typename T>
class Matrix {
    std::vector<std::vector<T>> data;
    size_t rows, cols;
    
public:
    Matrix(size_t r, size_t c) : rows(r), cols(c), data(r, std::vector<T>(c)) {}
    
    std::vector<T>& operator[](size_t i) { return data[i]; }
    const std::vector<T>& operator[](size_t i) const { return data[i]; }
    
    size_t num_rows() const { return rows; }
    size_t num_cols() const { return cols; }
    
    // Matrix multiplication using expression templates
    template<typename E1, typename E2>
    static Matrix multiply(const E1& a, const E2& b) {
        size_t n = a.num_rows();
        size_t m = a.num_cols();
        size_t p = b.num_cols();
        
        Matrix result(n, p);
        
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < p; ++j) {
                T sum = 0;
                for (size_t k = 0; k < m; ++k) {
                    sum += a[i][k] * b[k][j];
                }
                result[i][j] = sum;
            }
        }
        
        return result;
    }
};

void demonstrate_matrix_operations() {
    std::cout << "\n=== MATRIX OPERATIONS ===\n";
    
    Matrix<double> A(2, 3);
    Matrix<double> B(3, 2);
    
    // Initialize matrices
    A[0] = {1, 2, 3};
    A[1] = {4, 5, 6};
    
    B[0] = {7, 8};
    B[1] = {9, 10};
    B[2] = {11, 12};
    
    // Matrix multiplication
    auto C = Matrix<double>::multiply(A, B);
    
    std::cout << "Matrix multiplication result:\n";
    for (size_t i = 0; i < C.num_rows(); ++i) {
        for (size_t j = 0; j < C.num_cols(); ++j) {
            std::cout << C[i][j] << " ";
        }
        std::cout << "\n";
    }
}

// ============================================================================
// 5. BENEFITS AND USE CASES
// ============================================================================

void explain_benefits() {
    std::cout << "\n=== EXPRESSION TEMPLATES BENEFITS ===\n";
    
    std::cout << "\nBenefits:\n";
    std::cout << "1. Eliminates temporary objects\n";
    std::cout << "2. Enables lazy evaluation\n";
    std::cout << "3. Fuses operations for better cache locality\n";
    std::cout << "4. Compile-time expression optimization\n";
    std::cout << "5. Clean, mathematical syntax\n";
    
    std::cout << "\nUse Cases:\n";
    std::cout << "1. Numerical libraries (Eigen, Blaze)\n";
    std::cout << "2. Vector/matrix operations\n";
    std::cout << "3. Domain-specific languages\n";
    std::cout << "4. Query optimization in databases\n";
    std::cout << "5. Image processing pipelines\n";
    
    std::cout << "\nExample from Eigen library:\n";
    std::cout << "VectorXd x(100), y(100), z(100);\n";
    std::cout << "// No temporaries created:\n";
    std::cout << "z = 2 * x + 3 * y;\n";
    
    std::cout << "\nKey Insight:\n";
    std::cout << "- Templates create expression trees at compile time\n";
    std::cout << "- Evaluation happens in a single pass\n";
    std::cout << "- Each element computed once, not stored intermediately\n";
}

#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>

// ============================================================================
// 1. PROBLEM: TEMPORARY OBJECTS IN VECTOR OPERATIONS
// ============================================================================

void demonstrate_problem() {
    std::cout << "\n=== PROBLEM: TEMPORARY OBJECTS ===\n";
    
    std::vector<double> a = {1, 2, 3, 4, 5};
    std::vector<double> b = {2, 3, 4, 5, 6};
    std::vector<double> c = {3, 4, 5, 6, 7};
    
    // Traditional approach: Creates temporaries
    std::vector<double> result1(a.size());
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // This creates temporary vectors for intermediate results
    for (size_t i = 0; i < a.size(); ++i) {
        result1[i] = a[i] * 2 + b[i] * 3 + c[i] * 4;
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Traditional: " << duration.count() << " microseconds\n";
    std::cout << "Result: ";
    for (double x : result1) std::cout << x << " ";
    std::cout << "\n";
    
    // Problem: Expression like (a + b) * c creates temporaries
    // Inefficient for large vectors or complex expressions
}

// ============================================================================
// 2. EXPRESSION TEMPLATES SOLUTION
// ============================================================================

// Base class for all expressions
template<typename E>
class VecExpression {
public:
    double operator[](size_t i) const { 
        return static_cast<const E&>(*this)[i];
    }
    
    size_t size() const { 
        return static_cast<const E&>(*this).size();
    }
};

// Concrete vector class
template<typename T>
class Vec : public VecExpression<Vec<T>> {
    std::vector<T> data;
    
public:
    Vec() = default;
    
    explicit Vec(size_t n) : data(n) {}
    
    Vec(std::initializer_list<T> init) : data(init) {}
    
    // Construction from any expression
    template<typename E>
    Vec(const VecExpression<E>& expr) : data(expr.size()) {
        for (size_t i = 0; i < data.size(); ++i) {
            data[i] = expr[i];
        }
    }
    
    // Assignment from any expression
    template<typename E>
    Vec& operator=(const VecExpression<E>& expr) {
        data.resize(expr.size());
        for (size_t i = 0; i < data.size(); ++i) {
            data[i] = expr[i];
        }
        return *this;
    }
    
    T& operator[](size_t i) { return data[i]; }
    const T& operator[](size_t i) const { return data[i]; }
    
    size_t size() const { return data.size(); }
};

// Binary operation expression template
template<typename E1, typename E2, typename Op>
class VecBinaryOp : public VecExpression<VecBinaryOp<E1, E2, Op>> {
    const E1& lhs;
    const E2& rhs;
    Op op;
    
public:
    VecBinaryOp(const E1& l, const E2& r, Op o = Op{}) 
        : lhs(l), rhs(r), op(o) {}
    
    auto operator[](size_t i) const {
        return op(lhs[i], rhs[i]);
    }
    
    size_t size() const { 
        return lhs.size();  // Assume same size
    }
};

// Unary operation expression template
template<typename E, typename Op>
class VecUnaryOp : public VecExpression<VecUnaryOp<E, Op>> {
    const E& expr;
    Op op;
    
public:
    VecUnaryOp(const E& e, Op o = Op{}) : expr(e), op(o) {}
    
    auto operator[](size_t i) const {
        return op(expr[i]);
    }
    
    size_t size() const { return expr.size(); }
};

// Scalar multiplication expression
template<typename E>
class VecScalarMul : public VecExpression<VecScalarMul<E>> {
    const E& expr;
    double scalar;
    
public:
    VecScalarMul(const E& e, double s) : expr(e), scalar(s) {}
    
    auto operator[](size_t i) const {
        return expr[i] * scalar;
    }
    
    size_t size() const { return expr.size(); }
};

// Function objects for operations
struct AddOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a + b; }
};

struct SubOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a - b; }
};

struct MulOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a * b; }
};

struct DivOp {
    template<typename T1, typename T2>
    auto operator()(T1 a, T2 b) const { return a / b; }
};

struct SqrtOp {
    template<typename T>
    auto operator()(T a) const { return std::sqrt(a); }
};

struct SinOp {
    template<typename T>
    auto operator()(T a) const { return std::sin(a); }
};

// Operator overloads to create expression templates
template<typename E1, typename E2>
auto operator+(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, AddOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator-(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, SubOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator*(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, MulOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E1, typename E2>
auto operator/(const VecExpression<E1>& lhs, const VecExpression<E2>& rhs) {
    return VecBinaryOp<E1, E2, DivOp>(static_cast<const E1&>(lhs), 
                                       static_cast<const E2&>(rhs));
}

template<typename E>
auto sqrt(const VecExpression<E>& expr) {
    return VecUnaryOp<E, SqrtOp>(static_cast<const E&>(expr));
}

template<typename E>
auto sin(const VecExpression<E>& expr) {
    return VecUnaryOp<E, SinOp>(static_cast<const E&>(expr));
}

// Scalar-vector operations
template<typename E>
auto operator*(double scalar, const VecExpression<E>& expr) {
    return VecScalarMul<E>(static_cast<const E&>(expr), scalar);
}

template<typename E>
auto operator*(const VecExpression<E>& expr, double scalar) {
    return VecScalarMul<E>(static_cast<const E&>(expr), scalar);
}

void demonstrate_expression_templates() {
    std::cout << "\n=== EXPRESSION TEMPLATES SOLUTION ===\n";
    
    Vec<double> a = {1, 2, 3, 4, 5};
    Vec<double> b = {2, 3, 4, 5, 6};
    Vec<double> c = {3, 4, 5, 6, 7};
    Vec<double> result(a.size());
    
    // Complex expression - NO temporaries created!
    auto start = std::chrono::high_resolution_clock::now();
    
    // Expression template builds computation graph
    // Evaluation happens only when assigned to result
    result = 2.0 * a + 3.0 * b + 4.0 * c;
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Expression Templates: " << duration.count() << " microseconds\n";
    std::cout << "Result: ";
    for (size_t i = 0; i < result.size(); ++i) {
        std::cout << result[i] << " ";
    }
    std::cout << "\n";
    
    // More complex expressions
    std::cout << "\nMore complex expressions:\n";
    
    Vec<double> d = {1, 4, 9, 16, 25};
    Vec<double> result2(a.size());
    
    result2 = sqrt(d) + sin(a) * b;
    
    std::cout << "sqrt(d) + sin(a) * b = ";
    for (size_t i = 0; i < result2.size(); ++i) {
        std::cout << result2[i] << " ";
    }
    std::cout << "\n";
    
    // Chained operations
    Vec<double> result3 = a + b - c * 2.0;
    std::cout << "\na + b - c * 2.0 = ";
    for (size_t i = 0; i < result3.size(); ++i) {
        std::cout << result3[i] << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 3. LAZY EVALUATION WITH EXPRESSION TEMPLATES
// ============================================================================

template<typename T>
class LazyVector {
    mutable std::vector<T>* data = nullptr;
    
    // Expression type
    template<typename E>
    class Expression {
        const E& expr;
        
    public:
        Expression(const E& e) : expr(e) {}
        
        operator std::vector<T>() const {
            std::vector<T> result(expr.size());
            for (size_t i = 0; i < result.size(); ++i) {
                result[i] = expr[i];
            }
            return result;
        }
    };
    
public:
    template<typename E>
    LazyVector(const VecExpression<E>& expr) 
        : data(new std::vector<T>(Expression<E>(static_cast<const E&>(expr)))) {}
    
    ~LazyVector() { delete data; }
    
    const T& operator[](size_t i) const {
        return (*data)[i];
    }
    
    size_t size() const { return data->size(); }
};

void demonstrate_lazy_evaluation() {
    std::cout << "\n=== LAZY EVALUATION ===\n";
    
    Vec<double> x = {1, 2, 3, 4, 5};
    Vec<double> y = {2, 3, 4, 5, 6};
    
    // Expression is stored, not evaluated
    auto expr = x + y * 2.0;
    
    // Evaluation happens only when needed
    LazyVector<double> lazy_result(expr);
    
    std::cout << "Lazy evaluated result: ";
    for (size_t i = 0; i < lazy_result.size(); ++i) {
        std::cout << lazy_result[i] << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 4. REAL-WORLD EXAMPLE: LINEAR ALGEBRA
// ============================================================================

template<typename T>
class Matrix {
    std::vector<std::vector<T>> data;
    size_t rows, cols;
    
public:
    Matrix(size_t r, size_t c) : rows(r), cols(c), data(r, std::vector<T>(c)) {}
    
    std::vector<T>& operator[](size_t i) { return data[i]; }
    const std::vector<T>& operator[](size_t i) const { return data[i]; }
    
    size_t num_rows() const { return rows; }
    size_t num_cols() const { return cols; }
    
    // Matrix multiplication using expression templates
    template<typename E1, typename E2>
    static Matrix multiply(const E1& a, const E2& b) {
        size_t n = a.num_rows();
        size_t m = a.num_cols();
        size_t p = b.num_cols();
        
        Matrix result(n, p);
        
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < p; ++j) {
                T sum = 0;
                for (size_t k = 0; k < m; ++k) {
                    sum += a[i][k] * b[k][j];
                }
                result[i][j] = sum;
            }
        }
        
        return result;
    }
};

void demonstrate_matrix_operations() {
    std::cout << "\n=== MATRIX OPERATIONS ===\n";
    
    Matrix<double> A(2, 3);
    Matrix<double> B(3, 2);
    
    // Initialize matrices
    A[0] = {1, 2, 3};
    A[1] = {4, 5, 6};
    
    B[0] = {7, 8};
    B[1] = {9, 10};
    B[2] = {11, 12};
    
    // Matrix multiplication
    auto C = Matrix<double>::multiply(A, B);
    
    std::cout << "Matrix multiplication result:\n";
    for (size_t i = 0; i < C.num_rows(); ++i) {
        for (size_t j = 0; j < C.num_cols(); ++j) {
            std::cout << C[i][j] << " ";
        }
        std::cout << "\n";
    }
}

// ============================================================================
// 5. BENEFITS AND USE CASES
// ============================================================================

void explain_benefits() {
    std::cout << "\n=== EXPRESSION TEMPLATES BENEFITS ===\n";
    
    std::cout << "\nBenefits:\n";
    std::cout << "1. Eliminates temporary objects\n";
    std::cout << "2. Enables lazy evaluation\n";
    std::cout << "3. Fuses operations for better cache locality\n";
    std::cout << "4. Compile-time expression optimization\n";
    std::cout << "5. Clean, mathematical syntax\n";
    
    std::cout << "\nUse Cases:\n";
    std::cout << "1. Numerical libraries (Eigen, Blaze)\n";
    std::cout << "2. Vector/matrix operations\n";
    std::cout << "3. Domain-specific languages\n";
    std::cout << "4. Query optimization in databases\n";
    std::cout << "5. Image processing pipelines\n";
    
    std::cout << "\nExample from Eigen library:\n";
    std::cout << "VectorXd x(100), y(100), z(100);\n";
    std::cout << "// No temporaries created:\n";
    std::cout << "z = 2 * x + 3 * y;\n";
    
    std::cout << "\nKey Insight:\n";
    std::cout << "- Templates create expression trees at compile time\n";
    std::cout << "- Evaluation happens in a single pass\n";
    std::cout << "- Each element computed once, not stored intermediately\n";
}


//// CUSTOM LITERALS ////

#include <iostream>
#include <cmath>
#include <string>
#include <chrono>

// Custom literal for distance in meters
long double operator"" _m(long double meters) {
    return meters;
}

// Custom literal for distance in kilometers
long double operator"" _km(long double kilometers) {
    return kilometers * 1000.0;
}

// Custom literal for binary numbers (string literal version)
unsigned long long operator"" _bin(const char* binaryStr, std::size_t) {
    unsigned long long value = 0;
    for (int i = 0; binaryStr[i] != '\0'; ++i) {
        value <<= 1;
        if (binaryStr[i] == '1') {
            value |= 1;
        } else if (binaryStr[i] != '0') {
            throw std::invalid_argument("Invalid binary string");
        }
    }
    return value;
}

// Custom literal for time in seconds
std::chrono::seconds operator"" _s(unsigned long long seconds) {
    return std::chrono::seconds(seconds);
}

// Custom literal for complex numbers (imaginary part)
std::complex<double> operator"" _i(long double imag) {
    return std::complex<double>(0.0, static_cast<double>(imag));
}

int main() {
    // Using custom literals
    long double distance1 = 5.5_m;      // 5.5 meters
    long double distance2 = 2.3_km;     // 2300 meters
    std::cout << "Distance 1: " << distance1 << " meters\n";
    std::cout << "Distance 2: " << distance2 << " meters\n";
    
    // Binary literal
    unsigned long long binaryNum = 1101_bin;  // Binary 1101 = Decimal 13
    std::cout << "Binary 1101 = Decimal " << binaryNum << "\n";
    
    // Time literal
    auto duration = 10_s;  // 10 seconds
    std::cout << "Duration: " << duration.count() << " seconds\n";
    
    // Complex number literal
    std::complex<double> z = 3.0 + 4.0_i;  // 3 + 4i
    std::cout << "Complex number: " << z.real() << " + " << z.imag() << "i\n";
    
    return 0;
}


//// ATTRIBUTE SPECIFIERS

#include <iostream>
#include <memory>
#include <vector>
#include <optional>

// [[nodiscard]] - warns if return value is ignored
class ResourceManager {
private:
    std::vector<int> resources;
    
public:
    // Constructor that allocates resources
    ResourceManager(size_t size) : resources(size, 0) {}
    
    // [[nodiscard]] on function - caller should use returned value
    [[nodiscard]] std::optional<int> allocateResource() {
        if (!resources.empty()) {
            int resource = resources.back();
            resources.pop_back();
            return resource;
        }
        return std::nullopt;
    }
    
    // [[nodiscard]] on type alias
    using Handle = std::unique_ptr<int>;
    [[nodiscard]] Handle createHandle(int value) {
        return std::make_unique<int>(value);
    }
};

// Function with [[nodiscard]] attribute
[[nodiscard]] int computeImportantValue(int x, int y) {
    return x * y + 42;
}

// [[likely]] and [[unlikely]] - hint to compiler about branch probability
void processData(int value) {
    // Most common case - value between 0 and 100
    if (value >= 0 && value <= 100) [[likely]] {
        std::cout << "Processing normal value: " << value << "\n";
        // Optimized code path for common case
    } 
    // Rare case - negative value (error condition)
    else if (value < 0) [[unlikely]] {
        std::cerr << "Error: Negative value encountered!\n";
        // Error handling code
    }
    // Less common case - very large value
    else [[unlikely]] {
        std::cout << "Processing large value: " << value << "\n";
        // Special handling for large values
    }
}

// Example with switch statement
void handleErrorCode(int errorCode) {
    switch (errorCode) {
        case 0: [[likely]]  // Success is most likely
            std::cout << "Operation successful\n";
            break;
        case 1: [[unlikely]]
            std::cerr << "Error: File not found\n";
            break;
        case 2: [[unlikely]]
            std::cerr << "Error: Permission denied\n";
            break;
        default: [[unlikely]]
            std::cerr << "Error: Unknown error code\n";
            break;
    }
}

// [[carries_dependency]] - for memory model optimization in concurrent code
#include <atomic>

std::atomic<int*> atomicPtr;

// Function that carries dependency
[[carries_dependency]] int* loadPointer() {
    return atomicPtr.load(std::memory_order_consume);
}

void processWithDependency(int* ptr) [[carries_dependency]] {
    if (ptr) {
        // Compiler knows dependency is carried through
        std::cout << "Value: " << *ptr << "\n";
    }
}

int main() {
    // [[nodiscard]] example
    ResourceManager manager(10);
    
    // Warning if return value is ignored (with proper compiler flags)
    // manager.allocateResource();  // This would generate warning
    
    // Correct usage
    auto resource = manager.allocateResource();
    if (resource) {
        std::cout << "Allocated resource: " << *resource << "\n";
    }
    
    // [[likely]]/[[unlikely]] example
    for (int i = -1; i < 102; ++i) {
        processData(i);
    }
    
    // [[carries_dependency]] example
    int value = 42;
    atomicPtr.store(&value, std::memory_order_release);
    int* ptr = loadPointer();
    processWithDependency(ptr);
    
    return 0;
}


//// ENABLE_IF

#include <iostream>
#include <type_traits>
#include <vector>
#include <list>
#include <string>

// Basic enable_if example
template<typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
addIntegral(T a, T b) {
    std::cout << "Integral addition\n";
    return a + b;
}

template<typename T>
typename std::enable_if<std::is_floating_point<T>::value, T>::type
addFloating(T a, T b) {
    std::cout << "Floating point addition\n";
    return a + b;
}

// Using enable_if in return type (alternative syntax)
template<typename T>
auto multiply(T a, T b) -> 
    typename std::enable_if<std::is_arithmetic<T>::value, T>::type {
    return a * b;
}

// enable_if in template parameter
template<typename T,
         typename = typename std::enable_if<std::is_integral<T>::value>::type>
T bitwiseAnd(T a, T b) {
    return a & b;
}

// Function overload using enable_if
template<typename T>
typename std::enable_if<std::is_pointer<T>::value, 
                        typename std::remove_pointer<T>::type>::type
dereferenceAndAdd(T a, T b) {
    std::cout << "Adding through pointers\n";
    return *a + *b;
}

template<typename T>
typename std::enable_if<!std::is_pointer<T>::value, T>::type
dereferenceAndAdd(T a, T b) {
    std::cout << "Adding directly\n";
    return a + b;
}

// Complex example: Container processing
template<typename Container>
typename std::enable_if<
    std::is_same<typename Container::value_type, int>::value,
    typename Container::value_type
>::type
sumContainer(const Container& cont) {
    std::cout << "Summing container of integers\n";
    typename Container::value_type sum = 0;
    for (const auto& elem : cont) {
        sum += elem;
    }
    return sum;
}

template<typename Container>
typename std::enable_if<
    std::is_same<typename Container::value_type, double>::value,
    typename Container::value_type
>::type
sumContainer(const Container& cont) {
    std::cout << "Summing container of doubles\n";
    typename Container::value_type sum = 0.0;
    for (const auto& elem : cont) {
        sum += elem;
    }
    return sum;
}

// enable_if with multiple conditions
template<typename T>
typename std::enable_if<
    std::is_arithmetic<T>::value && sizeof(T) <= 4,
    T
>::type
processSmallArithmetic(T value) {
    std::cout << "Processing small arithmetic type\n";
    return value * 2;
}

template<typename T>
typename std::enable_if<
    std::is_arithmetic<T>::value && sizeof(T) > 4,
    T
>::type
processSmallArithmetic(T value) {
    std::cout << "Processing large arithmetic type\n";
    return value / 2;
}

int main() {
    // Integral addition
    std::cout << "5 + 3 = " << addIntegral(5, 3) << "\n";
    
    // Floating point addition
    std::cout << "5.5 + 3.3 = " << addFloating(5.5, 3.3) << "\n";
    
    // Multiplication with arithmetic types
    std::cout << "4 * 2.5 = " << multiply(4, 2.5) << "\n";
    
    // Bitwise AND (only for integral types)
    std::cout << "5 & 3 = " << bitwiseAnd(5, 3) << "\n";
    
    // Pointer vs non-pointer overload
    int x = 10, y = 20;
    std::cout << "Direct add: " << dereferenceAndAdd(x, y) << "\n";
    std::cout << "Pointer add: " << dereferenceAndAdd(&x, &y) << "\n";
    
    // Container summation
    std::vector<int> intVec = {1, 2, 3, 4, 5};
    std::vector<double> doubleVec = {1.1, 2.2, 3.3};
    
    std::cout << "Sum of int vector: " << sumContainer(intVec) << "\n";
    std::cout << "Sum of double vector: " << sumContainer(doubleVec) << "\n";
    
    // Size-based processing
    std::cout << "Process int: " << processSmallArithmetic(10) << "\n";
    std::cout << "Process long long: " << processSmallArithmetic(10000000000LL) << "\n";
    
    return 0;
}


//// TYPE TRAITS

#include <iostream>
#include <type_traits>
#include <vector>
#include <string>
#include <complex>

// Function that behaves differently based on type traits
template<typename T>
void processType(const T& value) {
    std::cout << "Processing value: " << value << "\n";
    
    // Check if type is integral
    if constexpr (std::is_integral_v<T>) {
        std::cout << "  Type is integral\n";
        std::cout << "  Size: " << sizeof(T) << " bytes\n";
        
        // Check if signed or unsigned
        if constexpr (std::is_signed_v<T>) {
            std::cout << "  Type is signed\n";
        } else {
            std::cout << "  Type is unsigned\n";
        }
    }
    
    // Check if type is floating point
    if constexpr (std::is_floating_point_v<T>) {
        std::cout << "  Type is floating point\n";
        std::cout << "  Size: " << sizeof(T) << " bytes\n";
    }
    
    // Check if type is pointer
    if constexpr (std::is_pointer_v<T>) {
        std::cout << "  Type is pointer\n";
        std::cout << "  Points to: " << typeid(std::remove_pointer_t<T>).name() << "\n";
    }
    
    // Check if type is arithmetic (integral or floating point)
    if constexpr (std::is_arithmetic_v<T>) {
        std::cout << "  Type is arithmetic\n";
    }
    
    // Check if type is class
    if constexpr (std::is_class_v<T>) {
        std::cout << "  Type is a class\n";
    }
}

// Template specialization using type traits
template<typename T>
struct TypeInfo {
    static constexpr const char* name = "unknown";
};

template<typename T>
struct TypeInfo<typename std::enable_if<std::is_integral<T>::value, T>::type> {
    static constexpr const char* name = "integral";
};

template<typename T>
struct TypeInfo<typename std::enable_if<std::is_floating_point<T>::value, T>::type> {
    static constexpr const char* name = "floating point";
};

template<typename T>
struct TypeInfo<typename std::enable_if<std::is_pointer<T>::value, T>::type> {
    static constexpr const char* name = "pointer";
};

// Function using multiple type traits
template<typename Container>
typename std::enable_if<
    std::is_same_v<typename Container::value_type, int> &&
    std::is_same_v<typename Container::iterator, decltype(std::declval<Container>().begin())>,
    void
>::type
processIntContainer(const Container& cont) {
    std::cout << "Processing container of integers with size: " << cont.size() << "\n";
}

// Check for member types
template<typename T, typename = void>
struct HasValueType : std::false_type {};

template<typename T>
struct HasValueType<T, std::void_t<typename T::value_type>> : std::true_type {};

// Check for specific member function
template<typename T, typename = void>
struct HasSizeMethod : std::false_type {};

template<typename T>
struct HasSizeMethod<T, std::void_t<decltype(std::declval<T>().size())>> : std::true_type {};

// Composite type trait
template<typename T>
struct IsIterable {
private:
    template<typename U>
    static auto test(int) -> decltype(
        std::begin(std::declval<U&>()) != std::end(std::declval<U&>()),
        ++std::declval<decltype(std::begin(std::declval<U&>()))&>(),
        *std::begin(std::declval<U&>()),
        std::true_type{}
    );
    
    template<typename>
    static std::false_type test(...);
    
public:
    static constexpr bool value = decltype(test<T>(0))::value;
};

int main() {
    // Basic type trait checks
    std::cout << "Type trait checks:\n";
    std::cout << "int is integral: " << std::is_integral<int>::value << "\n";
    std::cout << "double is integral: " << std::is_integral<double>::value << "\n";
    std::cout << "float is floating point: " << std::is_floating_point<float>::value << "\n";
    std::cout << "int* is pointer: " << std::is_pointer<int*>::value << "\n";
    
    // Using variable templates (C++17)
    std::cout << "\nUsing variable templates:\n";
    std::cout << "int is arithmetic: " << std::is_arithmetic_v<int> << "\n";
    std::cout << "std::string is class: " << std::is_class_v<std::string> << "\n";
    
    // Process different types
    std::cout << "\nProcessing different types:\n";
    processType(42);
    processType(3.14);
    processType(2.5f);
    
    int x = 10;
    processType(&x);
    
    // TypeInfo struct
    std::cout << "\nTypeInfo:\n";
    std::cout << "Type of 42: " << TypeInfo<decltype(42)>::name << "\n";
    std::cout << "Type of 3.14: " << TypeInfo<decltype(3.14)>::name << "\n";
    std::cout << "Type of &x: " << TypeInfo<decltype(&x)>::name << "\n";
    
    // Custom type traits
    std::cout << "\nCustom type traits:\n";
    std::cout << "std::vector<int> has value_type: " << HasValueType<std::vector<int>>::value << "\n";
    std::cout << "std::vector<int> has size method: " << HasSizeMethod<std::vector<int>>::value << "\n";
    std::cout << "int is iterable: " << IsIterable<int>::value << "\n";
    std::cout << "std::vector<int> is iterable: " << IsIterable<std::vector<int>>::value << "\n";
    
    // Type transformations
    std::cout << "\nType transformations:\n";
    std::cout << "remove_const<const int>: " << typeid(std::remove_const_t<const int>).name() << "\n";
    std::cout << "remove_pointer<int*>: " << typeid(std::remove_pointer_t<int*>).name() << "\n";
    std::cout << "add_pointer<int>: " << typeid(std::add_pointer_t<int>).name() << "\n";
    std::cout << "make_signed<unsigned int>: " << typeid(std::make_signed_t<unsigned int>).name() << "\n";
    std::cout << "make_unsigned<int>: " << typeid(std::make_unsigned_t<int>).name() << "\n";
    
    return 0;
}


//// TEMPLATE METAPROGRAMMING PATTERNS

#include <iostream>
#include <type_traits>
#include <array>
#include <tuple>

// 1. CRTP (Curiously Recurring Template Pattern)
template<typename Derived>
class Base {
public:
    void interface() {
        static_cast<Derived*>(this)->implementation();
    }
    
    void implementation() {
        std::cout << "Default implementation in Base\n";
    }
};

class Derived1 : public Base<Derived1> {
public:
    void implementation() {
        std::cout << "Custom implementation in Derived1\n";
    }
};

class Derived2 : public Base<Derived2> {
    // Uses default implementation
};

// 2. Type List Pattern
template<typename... Types>
struct TypeList {};

// Get element at index
template<typename List, unsigned Index>
struct TypeAt;

template<typename Head, typename... Tail>
struct TypeAt<TypeList<Head, Tail...>, 0> {
    using type = Head;
};

template<typename Head, typename... Tail, unsigned Index>
struct TypeAt<TypeList<Head, Tail...>, Index> {
    using type = typename TypeAt<TypeList<Tail...>, Index - 1>::type;
};

// 3. Compile-time Fibonacci calculation
template<int N>
struct Fibonacci {
    static constexpr int value = Fibonacci<N - 1>::value + Fibonacci<N - 2>::value;
};

template<>
struct Fibonacci<0> {
    static constexpr int value = 0;
};

template<>
struct Fibonacci<1> {
    static constexpr int value = 1;
};

// 4. Compile-time factorial
template<int N>
struct Factorial {
    static constexpr long long value = N * Factorial<N - 1>::value;
};

template<>
struct Factorial<0> {
    static constexpr long long value = 1;
};

// 5. Compile-time prime number check
template<int N, int Divisor = N - 1>
struct IsPrime {
    static constexpr bool value = (N % Divisor != 0) && IsPrime<N, Divisor - 1>::value;
};

template<int N>
struct IsPrime<N, 1> {
    static constexpr bool value = true;
};

template<>
struct IsPrime<1, 1> {
    static constexpr bool value = false;
};

template<>
struct IsPrime<2, 1> {
    static constexpr bool value = true;
};

// 6. Tuple implementation using template metaprogramming
template<typename... Types>
class Tuple;

template<typename Head, typename... Tail>
class Tuple<Head, Tail...> {
private:
    Head head;
    Tuple<Tail...> tail;
    
public:
    Tuple(const Head& h, const Tail&... t) : head(h), tail(t...) {}
    
    template<unsigned Index>
    auto get() -> typename std::conditional_t<
        Index == 0,
        Head&,
        decltype(tail.template get<Index - 1>())
    > {
        if constexpr (Index == 0) {
            return head;
        } else {
            return tail.template get<Index - 1>();
        }
    }
    
    template<typename T>
    T& get() {
        if constexpr (std::is_same_v<Head, T>) {
            return head;
        } else {
            return tail.template get<T>();
        }
    }
};

template<>
class Tuple<> {
public:
    Tuple() {}
    
    template<unsigned Index>
    void get() = delete;
    
    template<typename T>
    void get() = delete;
};

// 7. Compile-time string manipulation
template<char... Chars>
struct CompileTimeString {
    static constexpr char value[] = {Chars..., '\0'};
    static constexpr int size = sizeof...(Chars);
};

// String concatenation
template<typename String1, typename String2>
struct ConcatStrings;

template<char... Chars1, char... Chars2>
struct ConcatStrings<CompileTimeString<Chars1...>, CompileTimeString<Chars2...>> {
    using type = CompileTimeString<Chars1..., Chars2...>;
};

// 8. Visitor Pattern using templates
template<typename... Types>
struct Visitor;

template<typename T>
struct Visitor<T> {
    virtual void visit(T&) = 0;
    virtual ~Visitor() = default;
};

template<typename T, typename... Rest>
struct Visitor<T, Rest...> : Visitor<Rest...> {
    using Visitor<Rest...>::visit;
    virtual void visit(T&) = 0;
};

// 9. Policy-based Design
template<typename StoragePolicy, typename LockingPolicy>
class Container : private StoragePolicy, private LockingPolicy {
public:
    template<typename T>
    void add(const T& value) {
        LockingPolicy::lock();
        StoragePolicy::add(value);
        LockingPolicy::unlock();
    }
    
    template<typename T>
    T get(size_t index) {
        LockingPolicy::lock();
        T value = StoragePolicy::template get<T>(index);
        LockingPolicy::unlock();
        return value;
    }
};

// Storage policies
class VectorStorage {
private:
    std::vector<int> data;
    
public:
    void add(const int& value) {
        data.push_back(value);
    }
    
    int get(size_t index) {
        return data.at(index);
    }
};

class ArrayStorage {
private:
    std::array<int, 100> data;
    size_t count = 0;
    
public:
    void add(const int& value) {
        if (count < data.size()) {
            data[count++] = value;
        }
    }
    
    int get(size_t index) {
        if (index < count) {
            return data[index];
        }
        throw std::out_of_range("Index out of range");
    }
};

// Locking policies
class NoLock {
public:
    void lock() {}
    void unlock() {}
};

class MockLock {
public:
    void lock() { std::cout << "Lock acquired\n"; }
    void unlock() { std::cout << "Lock released\n"; }
};

int main() {
    std::cout << "=== CRTP Example ===\n";
    Derived1 d1;
    Derived2 d2;
    d1.interface();  // Calls Derived1::implementation
    d2.interface();  // Calls Base::implementation
    
    std::cout << "\n=== Compile-time Calculations ===\n";
    std::cout << "Fibonacci(10) = " << Fibonacci<10>::value << "\n";
    std::cout << "Factorial(5) = " << Factorial<5>::value << "\n";
    std::cout << "Is 17 prime? " << IsPrime<17>::value << "\n";
    std::cout << "Is 15 prime? " << IsPrime<15>::value << "\n";
    
    std::cout << "\n=== Type List Example ===\n";
    using MyTypes = TypeList<int, double, std::string, char>;
    std::cout << "Type at index 2: " << typeid(TypeAt<MyTypes, 2>::type).name() << "\n";
    
    std::cout << "\n=== Tuple Implementation ===\n";
    Tuple<int, double, std::string> myTuple(42, 3.14, "Hello");
    std::cout << "Element 0: " << myTuple.get<0>() << "\n";
    std::cout << "Element 1: " << myTuple.get<1>() << "\n";
    std::cout << "Element 2: " << myTuple.get<2>() << "\n";
    std::cout << "String element: " << myTuple.get<std::string>() << "\n";
    
    std::cout << "\n=== Compile-time String ===\n";
    using Hello = CompileTimeString<'H', 'e', 'l', 'l', 'o'>;
    using World = CompileTimeString<' ', 'W', 'o', 'r', 'l', 'd', '!'>;
    using HelloWorld = ConcatStrings<Hello, World>::type;
    std::cout << "Concatenated string: " << HelloWorld::value << "\n";
    
    std::cout << "\n=== Policy-based Design ===\n";
    Container<VectorStorage, NoLock> vectorContainer;
    vectorContainer.add(1);
    vectorContainer.add(2);
    std::cout << "Vector element 0: " << vectorContainer.get<int>(0) << "\n";
    
    Container<ArrayStorage, MockLock> arrayContainer;
    arrayContainer.add(10);
    arrayContainer.add(20);
    std::cout << "Array element 1: " << arrayContainer.get<int>(1) << "\n";
    
    return 0;
}