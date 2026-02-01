/*
================================================================================
GOLANG REFLECTION & UNSAFE - JUNIOR TO SENIOR CONCEPTS
================================================================================
This comprehensive example demonstrates reflection and unsafe package usage
with emphasis on when, why, and how to use them judiciously.
Reflection should be avoided when possible; unsafe should be used extremely rarely.
*/

package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"reflect"
	"strings"
	"time"
	"unsafe"
)

/*
-------------------------------------------------------------------------------
1. REFLECT PACKAGE BASICS
-------------------------------------------------------------------------------
Reflection allows programmatic inspection and manipulation of types at runtime.
Core concepts: Type, Value, Kind.
*/

func reflectBasics() {
	fmt.Println("\n=== Reflection Basics ===")

	var x int = 42
	var s string = "hello"
	var f float64 = 3.14
	var arr [3]int = [3]int{1, 2, 3}
	var slc []string = []string{"a", "b", "c"}
	var m map[string]int = map[string]int{"one": 1}
	var ch chan int = make(chan int)

	// TypeOf returns the type of a value
	fmt.Printf("Type of x: %v\n", reflect.TypeOf(x))     // int
	fmt.Printf("Type of s: %v\n", reflect.TypeOf(s))     // string
	fmt.Printf("Type of f: %v\n", reflect.TypeOf(f))     // float64
	fmt.Printf("Type of arr: %v\n", reflect.TypeOf(arr)) // [3]int
	fmt.Printf("Type of slc: %v\n", reflect.TypeOf(slc)) // []string
	fmt.Printf("Type of m: %v\n", reflect.TypeOf(m))     // map[string]int
	fmt.Printf("Type of ch: %v\n", reflect.TypeOf(ch))   // chan int

	// ValueOf returns the reflect.Value wrapper
	v := reflect.ValueOf(x)
	fmt.Printf("\nValue of x: %v\n", v)
	fmt.Printf("Value type: %v\n", v.Type())
	fmt.Printf("Value kind: %v\n", v.Kind()) // int
	fmt.Printf("Can set?: %v\n", v.CanSet()) // false - value is not addressable

	// Working with pointers
	px := &x
	pv := reflect.ValueOf(px)
	fmt.Printf("\nPointer value: %v\n", pv)
	fmt.Printf("Pointer type: %v\n", pv.Type())           // *int
	fmt.Printf("Pointer kind: %v\n", pv.Kind())           // ptr
	fmt.Printf("Pointer elem: %v\n", pv.Elem())           // 42
	fmt.Printf("Elem can set?: %v\n", pv.Elem().CanSet()) // true - addressable through pointer

	// Modifying values through reflection
	if pv.Elem().CanSet() {
		pv.Elem().SetInt(100)
		fmt.Printf("x after modification: %d\n", x) // 100
	}
}

/*
-------------------------------------------------------------------------------
2. TYPE INTROSPECTION
-------------------------------------------------------------------------------
Inspecting struct fields, methods, tags, and other type information.
*/

// Struct tags example
type User struct {
	ID        int    `json:"id" db:"user_id" validate:"required,gt=0"`
	Name      string `json:"name" db:"user_name" validate:"required,min=2"`
	Email     string `json:"email,omitempty" db:"email" validate:"email"`
	Age       int    `json:"age" db:"-" validate:"gte=0,lte=150"` // - means don't store in DB
	CreatedAt time.Time
	private   string // Unexported field
}

// Method for demonstration
func (u User) GetFullName() string {
	return u.Name
}

func (u *User) UpdateName(name string) {
	u.Name = name
}

func typeIntrospection() {
	fmt.Println("\n=== Type Introspection ===")

	u := User{
		ID:        1,
		Name:      "John Doe",
		Email:     "john@example.com",
		Age:       30,
		CreatedAt: time.Now(),
		private:   "hidden",
	}

	// Get type information
	t := reflect.TypeOf(u)
	fmt.Printf("Type name: %v\n", t.Name())        // User
	fmt.Printf("Type kind: %v\n", t.Kind())        // struct
	fmt.Printf("Num fields: %v\n", t.NumField())   // 5 (includes private)
	fmt.Printf("Num methods: %v\n", t.NumMethod()) // 1 (GetFullName, not UpdateName)

	// Inspect fields
	fmt.Println("\n=== Field Inspection ===")
	for i := 0; i < t.NumField(); i++ {
		field := t.Field(i)
		fmt.Printf("Field %d: %s\n", i, field.Name)
		fmt.Printf("  Type: %v\n", field.Type)
		fmt.Printf("  Tag: %v\n", field.Tag)
		fmt.Printf("  PkgPath (exported?): %v\n", field.PkgPath) // Empty = exported
		fmt.Printf("  Anonymous: %v\n", field.Anonymous)

		// Parse specific tags
		if jsonTag := field.Tag.Get("json"); jsonTag != "" {
			fmt.Printf("  JSON tag: %s\n", jsonTag)
		}
		if dbTag := field.Tag.Get("db"); dbTag != "" {
			fmt.Printf("  DB tag: %s\n", dbTag)
		}
		if validateTag := field.Tag.Get("validate"); validateTag != "" {
			fmt.Printf("  Validate tag: %s\n", validateTag)
		}
	}

	// Inspect methods
	fmt.Println("\n=== Method Inspection ===")
	for i := 0; i < t.NumMethod(); i++ {
		method := t.Method(i)
		fmt.Printf("Method %d: %s\n", i, method.Name)
		fmt.Printf("  Type: %v\n", method.Type)
		fmt.Printf("  PkgPath: %v\n", method.PkgPath)
	}

	// Pointer type methods
	pt := reflect.TypeOf(&u)
	fmt.Printf("\nPointer type num methods: %v\n", pt.NumMethod()) // 2 (includes UpdateName)

	// Get field by name
	if field, ok := t.FieldByName("Name"); ok {
		fmt.Printf("\nField 'Name' found: %v\n", field.Type)
	}

	// Check if type implements interface
	var writer interface{} = &strings.Builder{}
	writerType := reflect.TypeOf(writer)
	bytesType := reflect.TypeOf((*fmt.Stringer)(nil)).Elem()
	fmt.Printf("\nDoes %v implement Stringer? %v\n",
		writerType, writerType.Implements(bytesType))
}

// Tag parsing utility
func parseStructTags(obj interface{}) map[string]map[string]string {
	result := make(map[string]map[string]string)

	t := reflect.TypeOf(obj)
	if t.Kind() == reflect.Ptr {
		t = t.Elem()
	}

	if t.Kind() != reflect.Struct {
		return result
	}

	for i := 0; i < t.NumField(); i++ {
		field := t.Field(i)
		fieldName := field.Name
		result[fieldName] = make(map[string]string)

		// Get all tag key-value pairs
		tag := string(field.Tag)
		if tag == "" {
			continue
		}

		// Simple tag parsing (reflect.StructTag has built-in Get method)
		result[fieldName]["json"] = field.Tag.Get("json")
		result[fieldName]["db"] = field.Tag.Get("db")
		result[fieldName]["validate"] = field.Tag.Get("validate")
		result[fieldName]["xml"] = field.Tag.Get("xml")
	}

	return result
}

/*
-------------------------------------------------------------------------------
3. PERFORMANCE COSTS OF REFLECTION
-------------------------------------------------------------------------------
Reflection is significantly slower than direct code. Always benchmark.
*/

type Data struct {
	ID   int
	Name string
	Tags []string
}

// Direct field access
func directAccess(d Data) (int, string) {
	return d.ID, d.Name
}

// Reflection field access
func reflectAccess(d Data) (int, string, error) {
	v := reflect.ValueOf(d)
	idField := v.FieldByName("ID")
	nameField := v.FieldByName("Name")

	if !idField.IsValid() || !nameField.IsValid() {
		return 0, "", errors.New("field not found")
	}

	id := idField.Interface().(int)
	name := nameField.Interface().(string)

	return id, name, nil
}

// Optimized reflection with caching
var (
	dataType     reflect.Type
	idFieldIdx   int
	nameFieldIdx int
)

func init() {
	dataType = reflect.TypeOf(Data{})
	idFieldIdx = getFieldIndex(dataType, "ID")
	nameFieldIdx = getFieldIndex(dataType, "Name")
}

func getFieldIndex(t reflect.Type, fieldName string) int {
	field, ok := t.FieldByName(fieldName)
	if !ok {
		return -1
	}
	return field.Index[0]
}

func cachedReflectAccess(d Data) (int, string, error) {
	v := reflect.ValueOf(d)

	if idFieldIdx == -1 || nameFieldIdx == -1 {
		return 0, "", errors.New("field not found")
	}

	id := v.Field(idFieldIdx).Interface().(int)
	name := v.Field(nameFieldIdx).Interface().(string)

	return id, name, nil
}

func measurePerformance() {
	fmt.Println("\n=== Reflection Performance Costs ===")

	data := Data{
		ID:   1,
		Name: "Test",
		Tags: []string{"a", "b", "c"},
	}

	// Warm up
	for i := 0; i < 1000; i++ {
		directAccess(data)
		reflectAccess(data)
		cachedReflectAccess(data)
	}

	// Benchmark direct access
	start := time.Now()
	for i := 0; i < 1000000; i++ {
		_, _ = directAccess(data)
	}
	directTime := time.Since(start)
	fmt.Printf("Direct access (1M iterations): %v\n", directTime)

	// Benchmark reflection access
	start = time.Now()
	for i := 0; i < 1000000; i++ {
		_, _, _ = reflectAccess(data)
	}
	reflectTime := time.Since(start)
	fmt.Printf("Reflection access (1M iterations): %v\n", reflectTime)

	// Benchmark cached reflection access
	start = time.Now()
	for i := 0; i < 1000000; i++ {
		_, _, _ = cachedReflectAccess(data)
	}
	cachedTime := time.Since(start)
	fmt.Printf("Cached reflection (1M iterations): %v\n", cachedTime)

	fmt.Printf("\nPerformance ratios:\n")
	fmt.Printf("Reflection / Direct: %.0fx slower\n",
		float64(reflectTime.Nanoseconds())/float64(directTime.Nanoseconds()))
	fmt.Printf("Cached Reflection / Direct: %.0fx slower\n",
		float64(cachedTime.Nanoseconds())/float64(directTime.Nanoseconds()))
}

// More realistic example: JSON serialization
func jsonSerializationComparison() {
	fmt.Println("\n=== JSON Serialization Comparison ===")

	users := make([]User, 1000)
	for i := range users {
		users[i] = User{
			ID:   i,
			Name: fmt.Sprintf("User %d", i),
			Age:  20 + i%50,
		}
	}

	// Using encoding/json (uses reflection internally)
	start := time.Now()
	jsonData, err := json.Marshal(users)
	if err != nil {
		log.Fatal(err)
	}
	jsonTime := time.Since(start)
	fmt.Printf("JSON Marshal (reflection-based): %v\n", jsonTime)
	fmt.Printf("Data size: %d bytes\n", len(jsonData))

	// Alternative: code generation (e.g., easyjson, ffjson) would be faster
	// but requires external tools
}

/*
-------------------------------------------------------------------------------
4. UNSAFE PACKAGE (WHEN AND WHY TO AVOID)
-------------------------------------------------------------------------------
The unsafe package allows bypassing Go's type safety guarantees.
Use only when absolutely necessary and fully understand the implications.
*/

// ⚠️ WARNING: unsafe usage can lead to memory corruption, security vulnerabilities,
// and breaks Go's memory safety guarantees. Use with extreme caution.

func unsafeBasics() {
	fmt.Println("\n=== Unsafe Package Basics ===")

	// Sizeof returns the size in bytes of a type
	fmt.Printf("Size of int: %d bytes\n", unsafe.Sizeof(int(0)))      // 8 on 64-bit
	fmt.Printf("Size of string: %d bytes\n", unsafe.Sizeof(""))       // 16 (pointer + length)
	fmt.Printf("Size of []byte: %d bytes\n", unsafe.Sizeof([]byte{})) // 24 (pointer + length + capacity)

	// Alignof returns the required alignment
	fmt.Printf("Align of int: %d\n", unsafe.Alignof(int(0)))
	fmt.Printf("Align of struct: %d\n", unsafe.Alignof(Data{}))

	// Offsetof returns the offset of a field within a struct
	var d Data
	fmt.Printf("Offset of ID field: %d\n", unsafe.Offsetof(d.ID))
	fmt.Printf("Offset of Name field: %d\n", unsafe.Offsetof(d.Name))

	// Pointer arithmetic (VERY DANGEROUS)
	d1 := Data{ID: 42, Name: "Test"}
	ptr := unsafe.Pointer(&d1)

	// Convert to uintptr for arithmetic (uintptr is just an integer, not a pointer)
	base := uintptr(ptr)
	idPtr := (*int)(unsafe.Pointer(base + unsafe.Offsetof(d1.ID)))
	namePtr := (*string)(unsafe.Pointer(base + unsafe.Offsetof(d1.Name)))

	fmt.Printf("ID via unsafe pointer: %d\n", *idPtr)
	fmt.Printf("Name via unsafe pointer: %s\n", *namePtr)
}

// When unsafe might be justified (advanced use cases):

// 1. Zero-copy string to []byte conversion (DANGEROUS - breaks immutability guarantee)
func unsafeStringToBytes(s string) []byte {
	// ⚠️ This is dangerous: modifying the returned []byte modifies the string,
	// which violates Go's guarantee that strings are immutable.
	// Only use if you can guarantee the string won't be used after.
	return *(*[]byte)(unsafe.Pointer(&struct {
		string
		Cap int
	}{s, len(s)}))
}

func safeStringToBytes(s string) []byte {
	// Safe version - allocates new memory
	return []byte(s)
}

// 2. Zero-copy []byte to string conversion (less dangerous but still risky)
func unsafeBytesToString(b []byte) string {
	// ⚠️ The returned string shares memory with the byte slice.
	// If the slice is modified, the string changes (breaking immutability).
	return *(*string)(unsafe.Pointer(&b))
}

// 3. Interacting with C libraries or system calls
type SystemStruct struct {
	Field1 uint32
	Field2 uint64
	// Must match C struct layout exactly
}

// 4. High-performance, allocation-free operations
func sumIntSliceUnsafe(slice []int) int {
	if len(slice) == 0 {
		return 0
	}

	// Get pointer to first element
	ptr := unsafe.Pointer(&slice[0])
	sum := 0

	// Iterate through memory directly
	for i := 0; i < len(slice); i++ {
		// Calculate pointer to element i
		elemPtr := (*int)(unsafe.Pointer(uintptr(ptr) + uintptr(i)*unsafe.Sizeof(slice[0])))
		sum += *elemPtr
	}

	return sum
}

func sumIntSliceSafe(slice []int) int {
	sum := 0
	for _, v := range slice {
		sum += v
	}
	return sum
}

/*
-------------------------------------------------------------------------------
PRACTICAL REFLECTION EXAMPLES
-------------------------------------------------------------------------------
*/

// 1. Generic deep copy (simplified)
func deepCopy(src interface{}) interface{} {
	if src == nil {
		return nil
	}

	srcVal := reflect.ValueOf(src)
	srcType := reflect.TypeOf(src)

	// Handle pointers
	if srcType.Kind() == reflect.Ptr {
		elem := srcVal.Elem()
		dst := reflect.New(elem.Type())
		deepCopyValue(elem, dst.Elem())
		return dst.Interface()
	}

	// Handle non-pointers
	dst := reflect.New(srcType).Elem()
	deepCopyValue(srcVal, dst)
	return dst.Interface()
}

func deepCopyValue(src, dst reflect.Value) {
	switch src.Kind() {
	case reflect.Ptr:
		if src.IsNil() {
			return
		}
		elem := src.Elem()
		newVal := reflect.New(elem.Type())
		deepCopyValue(elem, newVal.Elem())
		dst.Set(newVal)

	case reflect.Interface:
		if src.IsNil() {
			return
		}
		srcElem := src.Elem()
		dstElem := reflect.New(srcElem.Type()).Elem()
		deepCopyValue(srcElem, dstElem)
		dst.Set(dstElem)

	case reflect.Struct:
		for i := 0; i < src.NumField(); i++ {
			if !src.Field(i).CanSet() && src.Type().Field(i).PkgPath != "" {
				continue // Skip unexported fields
			}
			deepCopyValue(src.Field(i), dst.Field(i))
		}

	case reflect.Slice:
		if src.IsNil() {
			return
		}
		dst.Set(reflect.MakeSlice(src.Type(), src.Len(), src.Cap()))
		for i := 0; i < src.Len(); i++ {
			deepCopyValue(src.Index(i), dst.Index(i))
		}

	case reflect.Map:
		if src.IsNil() {
			return
		}
		dst.Set(reflect.MakeMap(src.Type()))
		for _, key := range src.MapKeys() {
			srcVal := src.MapIndex(key)
			dstVal := reflect.New(srcVal.Type()).Elem()
			deepCopyValue(srcVal, dstVal)
			dst.SetMapIndex(key, dstVal)
		}

	default:
		// For basic types (int, string, etc.), just copy
		dst.Set(src)
	}
}

// 2. Struct field validator using tags
func validateStruct(obj interface{}) []string {
	var errors []string

	v := reflect.ValueOf(obj)
	t := reflect.TypeOf(obj)

	// Handle pointers
	if v.Kind() == reflect.Ptr {
		v = v.Elem()
		t = t.Elem()
	}

	if v.Kind() != reflect.Struct {
		return []string{"not a struct"}
	}

	for i := 0; i < v.NumField(); i++ {
		field := t.Field(i)
		fieldValue := v.Field(i)

		// Get validation tag
		validateTag := field.Tag.Get("validate")
		if validateTag == "" {
			continue
		}

		// Simple validation rules parsing
		rules := strings.Split(validateTag, ",")
		for _, rule := range rules {
			switch {
			case rule == "required":
				if isEmptyValue(fieldValue) {
					errors = append(errors,
						fmt.Sprintf("%s: field is required", field.Name))
				}
			case strings.HasPrefix(rule, "min="):
				var min int
				fmt.Sscanf(rule, "min=%d", &min)
				if str, ok := fieldValue.Interface().(string); ok {
					if len(str) < min {
						errors = append(errors,
							fmt.Sprintf("%s: must be at least %d characters",
								field.Name, min))
					}
				}
			case strings.HasPrefix(rule, "max="):
				var max int
				fmt.Sscanf(rule, "max=%d", &max)
				if str, ok := fieldValue.Interface().(string); ok {
					if len(str) > max {
						errors = append(errors,
							fmt.Sprintf("%s: must be at most %d characters",
								field.Name, max))
					}
				}
			case rule == "email":
				if email, ok := fieldValue.Interface().(string); ok {
					if !strings.Contains(email, "@") {
						errors = append(errors,
							fmt.Sprintf("%s: must be a valid email", field.Name))
					}
				}
			}
		}
	}

	return errors
}

func isEmptyValue(v reflect.Value) bool {
	switch v.Kind() {
	case reflect.String:
		return v.Len() == 0
	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
		return v.Int() == 0
	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64:
		return v.Uint() == 0
	case reflect.Float32, reflect.Float64:
		return v.Float() == 0
	case reflect.Bool:
		return !v.Bool()
	case reflect.Ptr, reflect.Interface, reflect.Slice, reflect.Map, reflect.Chan:
		return v.IsNil()
	default:
		return false
	}
}

// 3. Dynamic function invocation
type Calculator struct{}

func (c Calculator) Add(a, b int) int {
	return a + b
}

func (c Calculator) Multiply(a, b int) int {
	return a * b
}

func (c *Calculator) Subtract(a, b int) int {
	return a - b
}

func invokeMethod(obj interface{}, methodName string, args ...interface{}) ([]interface{}, error) {
	v := reflect.ValueOf(obj)
	method := v.MethodByName(methodName)

	if !method.IsValid() {
		// Try pointer receiver methods
		if v.Kind() != reflect.Ptr {
			pv := reflect.New(v.Type())
			pv.Elem().Set(v)
			v = pv
			method = v.MethodByName(methodName)
		}
	}

	if !method.IsValid() {
		return nil, fmt.Errorf("method %s not found", methodName)
	}

	// Convert args to reflect.Values
	in := make([]reflect.Value, len(args))
	for i, arg := range args {
		in[i] = reflect.ValueOf(arg)
	}

	// Call the method
	out := method.Call(in)

	// Convert results back to interface{}
	results := make([]interface{}, len(out))
	for i, val := range out {
		results[i] = val.Interface()
	}

	return results, nil
}

/*
-------------------------------------------------------------------------------
SAFE ALTERNATIVES TO REFLECTION
-------------------------------------------------------------------------------
*/

// 1. Code generation (compile-time alternative)
// Use go:generate with tools like stringer, easyjson, etc.

//go:generate stringer -type=Status
type Status int

const (
	Pending Status = iota
	Processing
	Completed
	Failed
)

// 2. Interface-based solutions
type Validator interface {
	Validate() error
}

type RegistrationForm struct {
	Username string
	Email    string
	Password string
}

func (r RegistrationForm) Validate() error {
	if len(r.Username) < 3 {
		return errors.New("username too short")
	}
	if !strings.Contains(r.Email, "@") {
		return errors.New("invalid email")
	}
	if len(r.Password) < 8 {
		return errors.New("password too short")
	}
	return nil
}

// 3. Map-based configuration (when structure is dynamic)
type DynamicConfig map[string]interface{}

func (dc DynamicConfig) GetString(key string) (string, error) {
	val, ok := dc[key]
	if !ok {
		return "", fmt.Errorf("key %s not found", key)
	}
	str, ok := val.(string)
	if !ok {
		return "", fmt.Errorf("key %s is not a string", key)
	}
	return str, nil
}

// 4. Visitor pattern for complex structures
type Visitor interface {
	VisitString(key string, value string)
	VisitInt(key string, value int)
	VisitSlice(key string, value []interface{})
}

type ConfigWalker struct {
	visitor Visitor
}

func (cw *ConfigWalker) Walk(config map[string]interface{}) {
	for k, v := range config {
		switch val := v.(type) {
		case string:
			cw.visitor.VisitString(k, val)
		case int:
			cw.visitor.VisitInt(k, val)
		case []interface{}:
			cw.visitor.VisitSlice(k, val)
		}
	}
}

/*
-------------------------------------------------------------------------------
MEMORY LAYOUT EXAMPLES WITH UNSAFE
-------------------------------------------------------------------------------
*/

type MemoryLayout struct {
	Bool1   bool   // 1 byte
	Int1    int32  // 4 bytes
	Bool2   bool   // 1 byte + 2 bytes padding (alignment to 4)
	Int2    int64  // 8 bytes
	Bool3   bool   // 1 byte + 7 bytes padding (alignment to 8)
	String1 string // 16 bytes
}

func showMemoryLayout() {
	fmt.Println("\n=== Memory Layout Analysis ===")

	var ml MemoryLayout
	t := reflect.TypeOf(ml)

	fmt.Printf("Total size: %d bytes\n", unsafe.Sizeof(ml))
	fmt.Printf("Alignment: %d bytes\n", unsafe.Alignof(ml))

	fmt.Println("\nField offsets and sizes:")
	for i := 0; i < t.NumField(); i++ {
		field := t.Field(i)
		offset := unsafe.Offsetof(reflect.ValueOf(ml).Field(i).Interface())
		size := unsafe.Sizeof(reflect.ValueOf(ml).Field(i).Interface())
		fmt.Printf("  %s: offset %d, size %d\n",
			field.Name, offset, size)
	}

	// Show actual memory addresses
	ptr := unsafe.Pointer(&ml)
	fmt.Printf("\nStarting address: %p\n", ptr)
}

/*
-------------------------------------------------------------------------------
MAIN DEMONSTRATION
-------------------------------------------------------------------------------
*/

func main() {
	fmt.Println("=== Go Reflection & Unsafe Examples ===")

	// Reflection basics
	reflectBasics()

	// Type introspection
	typeIntrospection()

	// Parse struct tags
	tags := parseStructTags(User{})
	fmt.Printf("\n=== Parsed Tags ===\n")
	for field, fieldTags := range tags {
		fmt.Printf("%s: %v\n", field, fieldTags)
	}

	// Performance measurement
	measurePerformance()

	// JSON serialization comparison
	jsonSerializationComparison()

	// Unsafe basics (commented for safety - uncomment to test)
	// unsafeBasics()

	// Validation example
	user := User{
		Name:  "J",
		Email: "invalid-email",
		Age:   200,
	}
	errors := validateStruct(user)
	fmt.Println("\n=== Validation Errors ===")
	for _, err := range errors {
		fmt.Println(err)
	}

	// Dynamic method invocation
	calc := Calculator{}
	results, err := invokeMethod(calc, "Add", 10, 5)
	if err == nil {
		fmt.Printf("\nCalculator Add result: %v\n", results[0])
	}

	// Memory layout
	showMemoryLayout()

	// Deep copy example
	original := Data{
		ID:   1,
		Name: "Original",
		Tags: []string{"a", "b"},
	}
	copied := deepCopy(original).(Data)
	copied.Tags[0] = "modified"
	fmt.Printf("\n=== Deep Copy Test ===\n")
	fmt.Printf("Original tags: %v\n", original.Tags)
	fmt.Printf("Copied tags: %v\n", copied.Tags)

	// Safe vs unsafe string conversion
	str := "hello"
	unsafeBytes := unsafeStringToBytes(str)
	safeBytes := safeStringToBytes(str)
	fmt.Printf("\n=== String Conversion ===\n")
	fmt.Printf("Original string: %s\n", str)
	fmt.Printf("Unsafe bytes length: %d\n", len(unsafeBytes))
	fmt.Printf("Safe bytes length: %d\n", len(safeBytes))

	// Sum comparison
	slice := make([]int, 1000000)
	for i := range slice {
		slice[i] = i % 100
	}

	start := time.Now()
	safeSum := sumIntSliceSafe(slice)
	safeTime := time.Since(start)

	start = time.Now()
	unsafeSum := sumIntSliceUnsafe(slice)
	unsafeTime := time.Since(start)

	fmt.Printf("\n=== Sum Performance ===\n")
	fmt.Printf("Safe sum: %d, time: %v\n", safeSum, safeTime)
	fmt.Printf("Unsafe sum: %d, time: %v\n", unsafeSum, unsafeTime)
	fmt.Printf("Unsafe is %.2fx faster\n",
		float64(safeTime.Nanoseconds())/float64(unsafeTime.Nanoseconds()))

	printGuidelines()
}

func printGuidelines() {
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("REFLECTION & UNSAFE GUIDELINES")
	fmt.Println(strings.Repeat("=", 70))

	guidelines := []struct {
		Topic    string
		Guidance string
	}{
		{"Reflection Usage", "Avoid when possible. 10-100x slower than direct code."},
		{"When to Use Reflection", "JSON/XML marshaling, ORM, dependency injection, plugins."},
		{"Reflection Optimization", "Cache reflect.Type and reflect.Value, avoid in hot loops."},
		{"Unsafe Package", "RARELY needed. Breaks memory safety guarantees."},
		{"When to Use Unsafe", "Zero-copy conversions, C interop, extreme performance needs."},
		{"Unsafe Safety", "Never modify strings. Validate all offsets. Test thoroughly."},
		{"Alternatives", "Code generation, interfaces, maps, generics (Go 1.18+)."},
		{"Testing", "Always test reflection/unsafe code with race detector enabled."},
		{"Production", "Wrap unsafe operations in safe APIs with proper validation."},
		{"Team Policy", "Establish clear guidelines and code review requirements."},
	}

	for _, g := range guidelines {
		fmt.Printf("\n%-25s: %s", g.Topic, g.Guidance)
	}

	fmt.Println("\n\n" + strings.Repeat("=", 70))
	fmt.Println("KEY PRINCIPLES")
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("1. Reflection is for generic programming, not routine operations")
	fmt.Println("2. Unsafe is for system programming, not application logic")
	fmt.Println("3. Always measure performance before and after optimization")
	fmt.Println("4. Document why reflection/unsafe is necessary")
	fmt.Println("5. Consider future maintenance and team understanding")
}

/*
-------------------------------------------------------------------------------
ADDITIONAL RESOURCES
-------------------------------------------------------------------------------

Reflection Best Practices:
- Use reflect.DeepEqual for comparing complex structures
- Use reflect.Select for dynamic channel operations
- Use reflect.MakeFunc for creating functions dynamically
- Always handle panics when using reflection

Unsafe Pitfalls:
- Pointer arithmetic can cause segmentation faults
- Type punning violates Go's type safety
- Memory alignment issues on different architectures
- Garbage collector can't see through unsafe.Pointer

Performance Tips:
- Prefer switch on reflect.Kind over multiple if statements
- Reuse reflect.Value objects when possible
- Use reflect.Zero for creating zero values
- Consider code generation for performance-critical paths

Security Considerations:
- Reflection can bypass access controls on unexported fields
- Unsafe can read/write arbitrary memory locations
- Always validate user input before using in reflection
- Use the race detector when testing unsafe code
*/
