// ============================================
// GO STANDARD LIBRARY MASTERY
// ============================================

package main

import (
	"bufio"
	"bytes"
	"container/heap"
	"container/list"
	"container/ring"
	"context"
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"io/fs"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

// ============================================
// 1. fmt - FORMATTING AND PRINTING
// ============================================

func fmtPackage() {
	fmt.Println("\n=== 1. fmt Package ===")

	// Basic printing
	fmt.Print("Print: no newline")
	fmt.Println("Println: with newline")
	fmt.Printf("Printf: formatted %s\n", "output")

	// String formatting
	name := "Alice"
	age := 30
	pi := 3.14159

	// Common verbs
	fmt.Printf("String: %s, Integer: %d, Float: %.2f\n", name, age, pi)
	fmt.Printf("Boolean: %t, Pointer: %p, Type: %T\n", true, &name, name)
	fmt.Printf("Binary: %b, Hex: %x, Scientific: %e\n", 255, 255, pi)
	fmt.Printf("Width: %10s, Left align: %-10s\n", name, name)

	// Sprintf (format to string)
	formatted := fmt.Sprintf("Hello, %s. You are %d years old.", name, age)
	fmt.Println("Formatted string:", formatted)

	// Errorf (create formatted error)
	err := fmt.Errorf("value %q is invalid", "test")
	fmt.Println("Formatted error:", err)

	// Fprintf (write to writer)
	var buf bytes.Buffer
	fmt.Fprintf(&buf, "Writing to buffer: %d\n", 42)
	fmt.Print("Buffer content:", buf.String())

	// Scanning input (though bufio is often better)
	input := "42 Golang"
	var num int
	var lang string
	fmt.Sscanf(input, "%d %s", &num, &lang)
	fmt.Printf("Scanned: %d, %s\n", num, lang)
}

// ============================================
// 2. strings - STRING MANIPULATION
// ============================================

func stringsPackage() {
	fmt.Println("\n=== 2. strings Package ===")

	s := "Hello, Go Developers!"

	// Basic operations
	fmt.Println("Contains:", strings.Contains(s, "Go"))
	fmt.Println("Count:", strings.Count(s, "e"))
	fmt.Println("HasPrefix:", strings.HasPrefix(s, "Hello"))
	fmt.Println("HasSuffix:", strings.HasSuffix(s, "!"))
	fmt.Println("Index:", strings.Index(s, "Go"))
	fmt.Println("LastIndex:", strings.LastIndex(s, "e"))

	// Transformation
	fmt.Println("ToUpper:", strings.ToUpper(s))
	fmt.Println("ToLower:", strings.ToLower(s))
	fmt.Println("Title:", strings.ToTitle(s))
	fmt.Println("TrimSpace:", strings.TrimSpace("  hello  "))
	fmt.Println("Trim:", strings.Trim("!!!Hello!!!", "!"))

	// Splitting and joining
	parts := strings.Split("a,b,c,d", ",")
	fmt.Println("Split:", parts)
	fmt.Println("Join:", strings.Join(parts, "-"))

	// Fields (splits on whitespace)
	words := strings.Fields("The quick brown fox")
	fmt.Println("Fields:", words)

	// Repeats and replacement
	fmt.Println("Repeat:", strings.Repeat("Go", 3))
	fmt.Println("Replace:", strings.Replace(s, "Go", "Golang", 1))
	fmt.Println("ReplaceAll:", strings.ReplaceAll(s, "e", "E"))

	// Builder for efficient string concatenation
	var builder strings.Builder
	builder.WriteString("Hello")
	builder.WriteByte(' ')
	builder.WriteString("World")
	fmt.Println("Builder:", builder.String())

	// Reader for reading strings as io.Reader
	reader := strings.NewReader("String as Reader")
	b := make([]byte, 8)
	n, _ := reader.Read(b)
	fmt.Println("Read from string:", string(b[:n]))
}

// ============================================
// 3. bytes - BYTE SLICE MANIPULATION
// ============================================

func bytesPackage() {
	fmt.Println("\n=== 3. bytes Package ===")

	// Similar to strings but for byte slices
	data := []byte("Hello, Go!")

	// Most functions mirror strings package
	fmt.Println("Contains:", bytes.Contains(data, []byte("Go")))
	fmt.Println("Count:", bytes.Count(data, []byte("l")))
	fmt.Println("HasPrefix:", bytes.HasPrefix(data, []byte("Hello")))

	// Transformation (returns new slice)
	fmt.Println("ToUpper:", string(bytes.ToUpper(data)))
	fmt.Println("ToLower:", string(bytes.ToLower(data)))
	fmt.Println("TrimSpace:", string(bytes.TrimSpace([]byte("  hello  "))))

	// Splitting
	parts := bytes.Split([]byte("a,b,c"), []byte(","))
	fmt.Printf("Split: %q\n", parts)

	// Buffer - versatile byte buffer
	var buf bytes.Buffer

	// Write methods
	buf.WriteString("Hello")
	buf.WriteByte(' ')
	buf.Write([]byte("World!"))
	fmt.Println("Buffer:", buf.String())

	// Read methods
	p := make([]byte, 5)
	n, _ := buf.Read(p)
	fmt.Println("Read from buffer:", string(p[:n]))

	// Reset and grow
	buf.Reset()
	buf.Grow(100) // Pre-allocate capacity
	buf.WriteString("Reset content")
	fmt.Println("After reset:", buf.String())

	// Reader for reading bytes
	reader := bytes.NewReader([]byte("Byte Reader"))
	remaining := reader.Len()
	fmt.Println("Bytes remaining:", remaining)

	// Compare
	b1 := []byte("abc")
	b2 := []byte("abd")
	fmt.Println("Compare:", bytes.Compare(b1, b2)) // -1 (b1 < b2)
}

// ============================================
// 4. strconv - STRING CONVERSION
// ============================================

func strconvPackage() {
	fmt.Println("\n=== 4. strconv Package ===")

	// String to numbers
	i, err := strconv.Atoi("42")
	if err == nil {
		fmt.Println("Atoi:", i)
	}

	// Parse with base
	num, _ := strconv.ParseInt("FF", 16, 64)
	fmt.Println("ParseInt (hex):", num)

	// Parse floats
	f, _ := strconv.ParseFloat("3.14159", 64)
	fmt.Println("ParseFloat:", f)

	// Parse bool
	b, _ := strconv.ParseBool("true")
	fmt.Println("ParseBool:", b)

	// Numbers to string
	fmt.Println("Itoa:", strconv.Itoa(123))
	fmt.Println("FormatInt:", strconv.FormatInt(255, 16)) // hex
	fmt.Println("FormatFloat:", strconv.FormatFloat(3.14159, 'f', 2, 64))
	fmt.Println("FormatBool:", strconv.FormatBool(true))

	// Append functions (efficient concatenation)
	dst := []byte("Value: ")
	dst = strconv.AppendInt(dst, 42, 10)
	dst = strconv.AppendBool(dst, true)
	fmt.Println("Append:", string(dst))

	// Quote functions
	fmt.Println("Quote:", strconv.Quote("Hello\nWorld"))
	fmt.Println("QuoteRune:", strconv.QuoteRune('☺'))
	fmt.Println("QuoteToASCII:", strconv.QuoteToASCII("Hello 世界"))

	// Unquote
	unquoted, _ := strconv.Unquote(`"Hello\nWorld"`)
	fmt.Println("Unquote:", unquoted)
}

// ============================================
// 5. time - TIME AND DATE
// ============================================

func timePackage() {
	fmt.Println("\n=== 5. time Package ===")

	// Current time
	now := time.Now()
	fmt.Println("Current time:", now)
	fmt.Println("Unix timestamp:", now.Unix())
	fmt.Println("Unix nano:", now.UnixNano())

	// Time components
	fmt.Println("Year:", now.Year())
	fmt.Println("Month:", now.Month())
	fmt.Println("Day:", now.Day())
	fmt.Println("Hour:", now.Hour())
	fmt.Println("Minute:", now.Minute())
	fmt.Println("Second:", now.Second())
	fmt.Println("Weekday:", now.Weekday())

	// Creating specific times
	t1 := time.Date(2024, time.January, 1, 0, 0, 0, 0, time.UTC)
	fmt.Println("Specific time:", t1)

	// Parsing time
	t2, _ := time.Parse(time.RFC3339, "2024-01-01T12:00:00Z")
	fmt.Println("Parsed RFC3339:", t2)

	// Formatting time
	fmt.Println("Custom format:", now.Format("2006-01-02 15:04:05"))
	fmt.Println("RFC1123:", now.Format(time.RFC1123))
	fmt.Println("Kitchen:", now.Format(time.Kitchen))

	// Duration
	duration := 2*time.Hour + 30*time.Minute
	fmt.Println("Duration:", duration)
	fmt.Println("Hours:", duration.Hours())
	fmt.Println("Minutes:", duration.Minutes())

	// Time arithmetic
	tomorrow := now.Add(24 * time.Hour)
	fmt.Println("Tomorrow:", tomorrow)

	diff := tomorrow.Sub(now)
	fmt.Println("Difference:", diff)

	// Ticker and Timer
	fmt.Println("\nTimers and Tickers:")
	timer := time.NewTimer(100 * time.Millisecond)
	go func() {
		<-timer.C
		fmt.Println("Timer fired!")
	}()

	ticker := time.NewTicker(200 * time.Millisecond)
	go func() {
		for i := 0; i < 3; i++ {
			<-ticker.C
			fmt.Println("Ticker tick", i+1)
		}
		ticker.Stop()
	}()

	// Sleep
	time.Sleep(700 * time.Millisecond)

	// Time zones
	loc, _ := time.LoadLocation("America/New_York")
	nyTime := now.In(loc)
	fmt.Println("\nNew York time:", nyTime)
}

// ============================================
// 6. context - REQUEST CONTEXT AND CANCELLATION
// ============================================

func contextPackage() {
	fmt.Println("\n=== 6. context Package ===")

	// Background and TODO contexts
	ctx := context.Background()
	fmt.Println("Background context created")

	// WithCancel - manual cancellation
	ctx1, cancel1 := context.WithCancel(ctx)
	defer cancel1()

	// WithTimeout - automatic cancellation after duration
	ctx2, cancel2 := context.WithTimeout(ctx, 100*time.Millisecond)
	defer cancel2()

	// WithDeadline - cancellation at specific time
	deadline := time.Now().Add(200 * time.Millisecond)
	ctx3, cancel3 := context.WithDeadline(ctx, deadline)
	defer cancel3()

	// WithValue - carrying request-scoped values
	type key string
	requestIDKey := key("requestID")
	ctx4 := context.WithValue(ctx, requestIDKey, "12345")

	// Accessing values
	if reqID, ok := ctx4.Value(requestIDKey).(string); ok {
		fmt.Println("Request ID:", reqID)
	}

	// Example: goroutine with cancellation
	fmt.Println("\nCancellation example:")
	ctx5, cancel5 := context.WithTimeout(ctx, 50*time.Millisecond)
	defer cancel5()

	go func(ctx context.Context) {
		select {
		case <-time.After(100 * time.Millisecond):
			fmt.Println("Work completed")
		case <-ctx.Done():
			fmt.Println("Work cancelled:", ctx.Err())
		}
	}(ctx5)

	time.Sleep(60 * time.Millisecond)

	// Checking context status
	fmt.Println("\nContext checks:")
	fmt.Println("ctx1 error:", ctx1.Err())
	fmt.Println("ctx2 deadline:", ctx2.Deadline())
	fmt.Println("ctx3 done:", ctx3.Done())
}

// ============================================
// 7. os, io, io/fs - OPERATING SYSTEM AND I/O
// ============================================

func osIoPackage() {
	fmt.Println("\n=== 7. os, io, io/fs Packages ===")

	// os - Operating system interface
	fmt.Println("\n=== os Package ===")

	// Environment variables
	os.Setenv("MY_VAR", "test")
	fmt.Println("Env MY_VAR:", os.Getenv("MY_VAR"))

	// Working with files
	f, err := os.CreateTemp("", "example-*.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer os.Remove(f.Name())

	// Write to file
	content := []byte("Hello, file!")
	if _, err := f.Write(content); err != nil {
		log.Fatal(err)
	}
	f.Close()

	// Read file
	data, _ := os.ReadFile(f.Name())
	fmt.Println("File content:", string(data))

	// File info
	fi, _ := os.Stat(f.Name())
	fmt.Println("File size:", fi.Size())
	fmt.Println("File mode:", fi.Mode())
	fmt.Println("Is dir?", fi.IsDir())

	// Directory operations
	os.MkdirAll("testdir/subdir", 0755)
	defer os.RemoveAll("testdir")

	// Walk directory (deprecated in favor of filepath.WalkDir)
	filepath.WalkDir(".",
		func(path string, d fs.DirEntry, err error) error {
			if err != nil {
				return err
			}
			if !d.IsDir() {
				fmt.Println("Found file:", path)
			}
			return nil
		})

	fmt.Println("\n=== io Package ===")
	// io - Basic I/O interfaces
	var src io.Reader = strings.NewReader("source data")
	var dst bytes.Buffer

	// Copy data from reader to writer
	io.Copy(&dst, src)
	fmt.Println("Copied:", dst.String())

	// MultiWriter writes to multiple writers
	var buf1, buf2 bytes.Buffer
	mw := io.MultiWriter(&buf1, &buf2)
	mw.Write([]byte("multi write"))
	fmt.Println("Buffer1:", buf1.String())
	fmt.Println("Buffer2:", buf2.String())

	// TeeReader reads and writes simultaneously
	src2 := strings.NewReader("tee test")
	tr := io.TeeReader(src2, &dst)
	io.ReadAll(tr)
	fmt.Println("Tee result:", dst.String())

	fmt.Println("\n=== io/fs Package ===")
	// io/fs - File system interfaces
	type myFS struct{}

	// Implement fs.FS interface
	// (simplified example)
	var fsys fs.FS = os.DirFS(".")
	if entries, err := fs.ReadDir(fsys, "."); err == nil {
		for _, entry := range entries {
			fmt.Println("FS entry:", entry.Name())
		}
	}

	// Glob patterns
	matches, _ := fs.Glob(os.DirFS("."), "*.go")
	fmt.Println("Go files:", matches)
}

// ============================================
// 8. net/http - HTTP CLIENT AND SERVER
// ============================================

func httpPackage() {
	fmt.Println("\n=== 8. net/http Package ===")

	// HTTP Server
	server := &http.Server{
		Addr:         ":8080",
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	// Handlers
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello, %s!", r.URL.Path[1:])
	})

	http.HandleFunc("/api/data", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	// Start server in background
	go func() {
		fmt.Println("Server starting on :8080")
		server.ListenAndServe()
	}()
	defer server.Shutdown(context.Background())

	time.Sleep(100 * time.Millisecond)

	// HTTP Client
	fmt.Println("\nHTTP Client Examples:")

	// GET request
	resp, err := http.Get("http://localhost:8080/")
	if err == nil {
		body, _ := io.ReadAll(resp.Body)
		fmt.Println("GET Response:", string(body))
		resp.Body.Close()
	}

	// POST request with JSON
	jsonData := `{"name": "John"}`
	resp, err = http.Post(
		"http://localhost:8080/api",
		"application/json",
		strings.NewReader(jsonData),
	)

	// Custom request
	req, _ := http.NewRequest("PUT", "http://localhost:8080/resource", nil)
	req.Header.Set("Authorization", "Bearer token")
	client := &http.Client{Timeout: 5 * time.Second}
	client.Do(req)

	// Serve static files
	fs := http.FileServer(http.Dir("."))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	// Middleware pattern
	middleware := func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			fmt.Println("Middleware:", r.URL.Path)
			next.ServeHTTP(w, r)
		})
	}
	_ = middleware // Used in actual server
}

// ============================================
// 9. encoding/json - JSON ENCODING/DECODING
// ============================================

func jsonPackage() {
	fmt.Println("\n=== 9. encoding/json Package ===")

	// Marshal (Go struct to JSON)
	type Person struct {
		Name    string   `json:"name"`
		Age     int      `json:"age,omitempty"`
		Email   string   `json:"email,omitempty"`
		private string   // Unexported fields are ignored
		Tags    []string `json:"tags"`
	}

	p := Person{
		Name: "Alice",
		Age:  30,
		Tags: []string{"golang", "backend"},
	}

	jsonBytes, err := json.Marshal(p)
	if err == nil {
		fmt.Println("Marshal:", string(jsonBytes))
	}

	// Pretty print (indented)
	jsonIndented, _ := json.MarshalIndent(p, "", "  ")
	fmt.Println("Pretty JSON:\n", string(jsonIndented))

	// Unmarshal (JSON to Go struct)
	jsonStr := `{"name": "Bob", "age": 25, "tags": ["dev"]}`
	var p2 Person
	json.Unmarshal([]byte(jsonStr), &p2)
	fmt.Printf("Unmarshal: %+v\n", p2)

	// Streaming encoder/decoder
	var buf bytes.Buffer
	encoder := json.NewEncoder(&buf)
	encoder.SetIndent("", "  ")
	encoder.Encode(p)
	fmt.Println("Encoder output:", buf.String())

	decoder := json.NewDecoder(&buf)
	var p3 Person
	decoder.Decode(&p3)
	fmt.Printf("Decoder result: %+v\n", p3)

	// RawMessage for delayed unmarshaling
	type Message struct {
		Type string          `json:"type"`
		Data json.RawMessage `json:"data"`
	}

	msgJSON := `{"type": "user", "data": {"name": "Charlie"}}`
	var msg Message
	json.Unmarshal([]byte(msgJSON), &msg)

	// Unmarshal data based on type
	if msg.Type == "user" {
		var user Person
		json.Unmarshal(msg.Data, &user)
		fmt.Println("Delayed unmarshal:", user.Name)
	}

	// Custom marshaling
	type CustomTime struct {
		time.Time
	}

	// Implementing json.Marshaler interface
	// (commented as it requires full implementation)
	/*
		func (ct CustomTime) MarshalJSON() ([]byte, error) {
			return json.Marshal(ct.Format("2006-01-02"))
		}
	*/
}

// ============================================
// 10. regexp - REGULAR EXPRESSIONS
// ============================================

func regexpPackage() {
	fmt.Println("\n=== 10. regexp Package ===")

	// Compile regex (returns *Regexp)
	re := regexp.MustCompile(`\b\w{4}\b`) // 4-letter words
	text := "The quick brown fox jumps over the lazy dog"

	// Find first match
	match := re.FindString(text)
	fmt.Println("First match:", match)

	// Find all matches
	allMatches := re.FindAllString(text, -1)
	fmt.Println("All matches:", allMatches)

	// Find index positions
	indices := re.FindAllStringIndex(text, -1)
	fmt.Println("Match indices:", indices)

	// Replace
	replaced := re.ReplaceAllString(text, "****")
	fmt.Println("Replaced:", replaced)

	// Using capture groups
	emailRe := regexp.MustCompile(`(\w+)@(\w+\.\w+)`)
	email := "user@example.com"
	groups := emailRe.FindStringSubmatch(email)
	if groups != nil {
		fmt.Printf("Email groups: %q\n", groups)
		fmt.Println("Username:", groups[1])
		fmt.Println("Domain:", groups[2])
	}

	// Split using regex
	splitRe := regexp.MustCompile(`\s+`) // Whitespace
	words := splitRe.Split(text, -1)
	fmt.Println("Split by whitespace:", words)

	// Compiled regex are safe for concurrent use
	var wg sync.WaitGroup
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			re.MatchString(text)
		}()
	}
	wg.Wait()
}

// ============================================
// 11. sort - SORTING
// ============================================

func sortPackage() {
	fmt.Println("\n=== 11. sort Package ===")

	// Sorting slices
	nums := []int{4, 2, 8, 1, 3}
	sort.Ints(nums)
	fmt.Println("Sorted ints:", nums)

	strings := []string{"banana", "apple", "cherry"}
	sort.Strings(strings)
	fmt.Println("Sorted strings:", strings)

	// Custom sorting
	type Person struct {
		Name string
		Age  int
	}

	people := []Person{
		{"Alice", 30},
		{"Bob", 25},
		{"Charlie", 35},
	}

	// Sort by age
	sort.Slice(people, func(i, j int) bool {
		return people[i].Age < people[j].Age
	})
	fmt.Println("Sorted by age:")
	for _, p := range people {
		fmt.Printf("  %s: %d\n", p.Name, p.Age)
	}

	// Sort with stable sort (preserves equal elements order)
	sort.SliceStable(people, func(i, j int) bool {
		return len(people[i].Name) < len(people[j].Name)
	})

	// Search in sorted slice
	x := 3
	pos := sort.SearchInts(nums, x)
	fmt.Printf("Position of %d: %d\n", x, pos)

	// IsSorted check
	fmt.Println("Is sorted?", sort.IntsAreSorted(nums))

	// Reverse sorting
	sort.Sort(sort.Reverse(sort.IntSlice(nums)))
	fmt.Println("Reverse sorted:", nums)
}

// ============================================
// 12. container - DATA CONTAINERS
// ============================================

func containerPackage() {
	fmt.Println("\n=== 12. container Package ===")

	fmt.Println("\n=== list (doubly linked list) ===")
	// List - doubly linked list
	l := list.New()
	l.PushBack("first")
	l.PushFront("second")
	l.PushBack("third")

	fmt.Print("List: ")
	for e := l.Front(); e != nil; e = e.Next() {
		fmt.Print(e.Value, " ")
	}
	fmt.Println()

	// Remove element
	mid := l.Front().Next()
	l.Remove(mid)
	fmt.Print("After remove: ")
	for e := l.Front(); e != nil; e = e.Next() {
		fmt.Print(e.Value, " ")
	}
	fmt.Println()

	fmt.Println("\n=== ring (circular list) ===")
	// Ring - circular list
	r := ring.New(5)
	for i := 0; i < 5; i++ {
		r.Value = i
		r = r.Next()
	}

	fmt.Print("Ring: ")
	r.Do(func(x interface{}) {
		fmt.Print(x, " ")
	})
	fmt.Println()

	fmt.Println("\n=== heap (priority queue) ===")
	// Heap - priority queue
	pq := &PriorityQueue{
		{value: "orange", priority: 1},
		{value: "apple", priority: 2},
		{value: "banana", priority: 3},
	}
	heap.Init(pq)

	heap.Push(pq, &Item{value: "grape", priority: 4})
	for pq.Len() > 0 {
		item := heap.Pop(pq).(*Item)
		fmt.Printf("%s (priority: %d)\n", item.value, item.priority)
	}
}

// Heap implementation
type Item struct {
	value    string
	priority int
	index    int
}

type PriorityQueue []*Item

func (pq PriorityQueue) Len() int           { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].priority < pq[j].priority }
func (pq PriorityQueue) Swap(i, j int)      { pq[i], pq[j] = pq[j], pq[i]; pq[i].index = i; pq[j].index = j }
func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	*pq = old[0 : n-1]
	return item
}

// ============================================
// 13. path/filepath - PATH MANIPULATION
// ============================================

func filepathPackage() {
	fmt.Println("\n=== 13. path/filepath Package ===")

	// Join paths (OS-specific separator)
	path := filepath.Join("dir", "subdir", "file.txt")
	fmt.Println("Joined path:", path)

	// Split into directory and file
	dir, file := filepath.Split(path)
	fmt.Printf("Dir: %q, File: %q\n", dir, file)

	// Base and directory
	fmt.Println("Base:", filepath.Base(path))
	fmt.Println("Dir:", filepath.Dir(path))

	// Extension
	fmt.Println("Ext:", filepath.Ext(path))

	// Clean path
	clean := filepath.Clean("/a/b/../c/./d")
	fmt.Println("Clean path:", clean)

	// Absolute path
	abs, _ := filepath.Abs(".")
	fmt.Println("Absolute path:", abs)

	// Rel returns relative path
	rel, _ := filepath.Rel("/a/b", "/a/b/c/d")
	fmt.Println("Relative path:", rel)

	// Walk directory tree
	fmt.Println("\nWalking directory:")
	filepath.Walk(".", func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() && filepath.Ext(path) == ".go" {
			fmt.Println("  Go file:", path)
		}
		return nil
	})

	// Glob pattern matching
	matches, _ := filepath.Glob("*.go")
	fmt.Println("\nGo files:", matches)

	// OS-specific path separators
	fmt.Println("Separator:", string(filepath.Separator))
	fmt.Println("List separator:", string(filepath.ListSeparator))
}

// ============================================
// 14. io/util (now io and os) - UTILITIES
// ============================================

func ioUtilReplacement() {
	fmt.Println("\n=== 14. io/util Functions (now in io and os) ===")

	// Note: io/ioutil was deprecated in Go 1.16
	// Functions moved to io and os packages

	// ReadAll (now in io)
	fmt.Println("\n=== io.ReadAll ===")
	reader := strings.NewReader("Hello, world!")
	data, _ := io.ReadAll(reader)
	fmt.Println("ReadAll:", string(data))

	// ReadFile (now in os)
	fmt.Println("\n=== os.ReadFile ===")
	tmpFile, _ := os.CreateTemp("", "test-*.txt")
	tmpFile.WriteString("File content")
	tmpFile.Close()

	content, _ := os.ReadFile(tmpFile.Name())
	fmt.Println("ReadFile:", string(content))
	os.Remove(tmpFile.Name())

	// WriteFile (now in os)
	fmt.Println("\n=== os.WriteFile ===")
	os.WriteFile("test.txt", []byte("Written by os.WriteFile"), 0644)
	os.Remove("test.txt")

	// ReadDir (now in os)
	fmt.Println("\n=== os.ReadDir ===")
	entries, _ := os.ReadDir(".")
	fmt.Println("Directory entries:")
	for _, entry := range entries {
		fmt.Println("  ", entry.Name())
	}

	// NopCloser (now in io)
	fmt.Println("\n=== io.NopCloser ===")
	reader2 := strings.NewReader("NopCloser test")
	rc := io.NopCloser(reader2)
	rc.Close() // No-op

	// Discard (now in io)
	fmt.Println("\n=== io.Discard ===")
	io.Copy(io.Discard, strings.NewReader("discarded"))

	// TempDir/TempFile (now in os)
	fmt.Println("\n=== os.CreateTemp/os.MkdirTemp ===")
	tempFile, _ := os.CreateTemp("", "prefix-*.txt")
	fmt.Println("Temp file:", tempFile.Name())
	tempFile.Close()
	os.Remove(tempFile.Name())

	tempDir, _ := os.MkdirTemp("", "dir-*")
	fmt.Println("Temp dir:", tempDir)
	os.RemoveAll(tempDir)
}

// ============================================
// ADDITIONAL IMPORTANT PACKAGES
// ============================================

func additionalPackages() {
	fmt.Println("\n=== Additional Important Packages ===")

	fmt.Println("\n=== encoding/csv ===")
	// CSV processing
	csvData := `name,age,city
Alice,30,NYC
Bob,25,LA`

	reader := csv.NewReader(strings.NewReader(csvData))
	records, _ := reader.ReadAll()
	fmt.Println("CSV records:")
	for _, record := range records {
		fmt.Println("  ", record)
	}

	fmt.Println("\n=== flag ===")
	// Command-line flags
	var port int
	var host string
	flag.IntVar(&port, "port", 8080, "Port number")
	flag.StringVar(&host, "host", "localhost", "Host address")
	// Parse would be called in main: flag.Parse()

	fmt.Println("\n=== log ===")
	// Logging
	log.Println("Standard log message")
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
	log.Printf("Formatted log: %s", "test")

	fmt.Println("\n=== bufio ===")
	// Buffered I/O
	input := "line1\nline2\nline3"
	scanner := bufio.NewScanner(strings.NewReader(input))
	lineNum := 1
	for scanner.Scan() {
		fmt.Printf("Line %d: %s\n", lineNum, scanner.Text())
		lineNum++
	}

	fmt.Println("\n=== sync ===")
	// Synchronization primitives
	var mu sync.Mutex
	var wg sync.WaitGroup
	var once sync.Once

	mu.Lock()
	// critical section
	mu.Unlock()

	wg.Add(2)
	go func() { defer wg.Done() }()
	go func() { defer wg.Done() }()
	wg.Wait()

	once.Do(func() { fmt.Println("This runs once") })
}

// ============================================
// MAIN FUNCTION
// ============================================

func main() {
	fmt.Println("=== GO STANDARD LIBRARY MASTERY ===\n")

	// Run demonstrations
	fmtPackage()
	stringsPackage()
	bytesPackage()
	strconvPackage()
	timePackage()
	contextPackage()
	osIoPackage()
	httpPackage()
	jsonPackage()
	regexpPackage()
	sortPackage()
	containerPackage()
	filepathPackage()
	ioUtilReplacement()
	additionalPackages()

	fmt.Println("\n=== END OF DEMONSTRATION ===")

	// Cleanup
	os.Remove("test.txt")
}

// ============================================
// KEY TAKEAWAYS FOR DEVELOPERS
// ============================================

// JUNIOR DEVELOPERS:
// 1. Learn fmt for all output formatting needs
// 2. Master strings package for text manipulation
// 3. Use time package correctly for dates/times
// 4. Understand json.Marshal/Unmarshal for APIs
// 5. Use filepath.Join for cross-platform paths

// MID-LEVEL DEVELOPERS:
// 1. Implement proper context handling for cancellation
// 2. Use bytes.Buffer for efficient string building
// 3. Master net/http for both client and server
// 4. Understand io.Reader/Writer interfaces
// 5. Use sort.Slice for custom sorting
// 6. Implement proper error handling with strconv

// SENIOR DEVELOPERS:
// 1. Design with interfaces (io.Reader, http.Handler)
// 2. Implement efficient streaming with io.Copy
// 3. Use context for propagation and timeouts
// 4. Create custom json.Marshaler implementations
// 5. Design concurrent-safe packages
// 6. Use container packages for specialized data structures

// PERFORMANCE TIPS:
// 1. Use strings.Builder over + for concatenation
// 2. Precompile regexp patterns with MustCompile
// 3. Use json.Encoder/Decoder for streaming
// 4. Use bufio for buffered I/O operations
// 5. Reuse bytes.Buffer with Reset()

// SECURITY BEST PRACTICES:
// 1. Always validate regexp patterns
// 2. Use filepath for safe path manipulation
// 3. Set timeouts in http.Client and http.Server
// 4. Validate JSON input before unmarshaling
// 5. Use context deadlines for operations

// COMMON PITFALLS:
// 1. Forgetting to check errors from strconv
// 2. Misusing time.Format (use 2006-01-02 reference)
// 3. Not closing response bodies in http
// 4. Ignoring context cancellation
// 5. Using ioutil (deprecated - use io/os instead)

// PRODUCTION READY PATTERNS:
// 1. Structured logging with log/slog (Go 1.21+)
// 2. HTTP middleware chains
// 3. Graceful shutdown with context
// 4. Connection pooling for databases/HTTP
// 5. Circuit breakers for external services
