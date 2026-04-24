/**
 * JAVASCRIPT REGULAR EXPRESSIONS
 * ================================
 * Comprehensive guide to RegEx in JavaScript
 * Patterns, flags, methods, and common use cases
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT REGULAR EXPRESSIONS");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. REGEX BASICS
// ============================================================================

console.log("\n=== RegEx Basics ===");

// Creating regex
const regex1 = /hello/;           // Literal notation
const regex2 = new RegExp("hello"); // Constructor

// Test if pattern matches
console.log("Test:", regex1.test("hello world"));  // true
console.log("Test:", regex1.test("goodbye"));      // false

// Execute (returns match details)
const result = regex1.exec("hello world");
console.log("Exec:", result);  // ["hello", index: 0, ...]


// ============================================================================
// 2. REGEX FLAGS
// ============================================================================

console.log("\n=== Flags ===");

/**
 * FLAGS:
 * g - Global (find all matches)
 * i - Case-insensitive
 * m - Multiline (^ and $ match line boundaries)
 * s - Dotall (. matches newlines)
 * u - Unicode
 * y - Sticky (match from lastIndex)
 */

const text = "Hello HELLO hello";

console.log("No flags:", /hello/.test(text));      // true (first match)
console.log("Case-insensitive:", /hello/i.test(text)); // true
console.log("Global:", text.match(/hello/g));      // ["hello"] (only lowercase)
console.log("Global + i:", text.match(/hello/gi)); // ["Hello", "HELLO", "hello"]


// ============================================================================
// 3. CHARACTER CLASSES
// ============================================================================

console.log("\n=== Character Classes ===");

// . - Any character except newline
console.log("Dot:", /h.llo/.test("hello"));    // true
console.log("Dot:", /h.llo/.test("hallo"));    // true

// \d - Digit [0-9]
console.log("Digit:", /\d+/.exec("abc123"));   // ["123"]

// \D - Not digit [^0-9]
console.log("Not digit:", /\D+/.exec("abc123")); // ["abc"]

// \w - Word character [a-zA-Z0-9_]
console.log("Word:", /\w+/.exec("hello_123")); // ["hello_123"]

// \W - Not word character
console.log("Not word:", /\W+/.exec("hello world")); // [" "]

// \s - Whitespace (space, tab, newline)
console.log("Whitespace:", /\s+/.exec("hello world")); // [" "]

// \S - Not whitespace
console.log("Not whitespace:", /\S+/.exec("  hello")); // ["hello"]

// Custom character class
console.log("Custom [aeiou]:", /[aeiou]/.exec("hello")); // ["e"]
console.log("Range [a-z]:", /[a-z]+/.exec("Hello123"));  // ["ello"]
console.log("Negated [^0-9]:", /[^0-9]+/.exec("abc123")); // ["abc"]


// ============================================================================
// 4. QUANTIFIERS
// ============================================================================

console.log("\n=== Quantifiers ===");

// * - 0 or more
console.log("Zero or more:", /he*llo/.test("hllo"));    // true
console.log("Zero or more:", /he*llo/.test("hello"));   // true
console.log("Zero or more:", /he*llo/.test("heeeello")); // true

// + - 1 or more
console.log("One or more:", /he+llo/.test("hllo"));   // false
console.log("One or more:", /he+llo/.test("hello"));  // true

// ? - 0 or 1
console.log("Optional:", /colou?r/.test("color"));  // true
console.log("Optional:", /colou?r/.test("colour")); // true

// {n} - Exactly n
console.log("Exactly 3:", /\d{3}/.test("12"));   // false
console.log("Exactly 3:", /\d{3}/.test("123"));  // true

// {n,} - n or more
console.log("3 or more:", /\d{3,}/.test("12"));   // false
console.log("3 or more:", /\d{3,}/.test("1234")); // true

// {n,m} - Between n and m
console.log("2 to 4:", /\d{2,4}/.exec("12345"));  // ["1234"]

// Greedy vs Lazy quantifiers
const html = "<div>content</div>";
console.log("Greedy:", /<.*>/.exec(html));   // ["<div>content</div>"]
console.log("Lazy:", /<.*?>/.exec(html));    // ["<div>"]


// ============================================================================
// 5. ANCHORS
// ============================================================================

console.log("\n=== Anchors ===");

// ^ - Start of string (or line with m flag)
console.log("Start:", /^hello/.test("hello world")); // true
console.log("Start:", /^world/.test("hello world")); // false

// $ - End of string (or line with m flag)
console.log("End:", /world$/.test("hello world")); // true
console.log("End:", /hello$/.test("hello world")); // false

// \b - Word boundary
console.log("Word boundary:", /\bcat\b/.test("cat"));      // true
console.log("Word boundary:", /\bcat\b/.test("category")); // false

// \B - Not word boundary
console.log("Not boundary:", /\Bcat/.test("category")); // true


// ============================================================================
// 6. GROUPS AND CAPTURING
// ============================================================================

console.log("\n=== Groups and Capturing ===");

// Capturing groups ()
const date = "2024-04-23";
const dateRegex = /(\d{4})-(\d{2})-(\d{2})/;
const match = date.match(dateRegex);
console.log("Full match:", match[0]);  // "2024-04-23"
console.log("Year:", match[1]);        // "2024"
console.log("Month:", match[2]);       // "04"
console.log("Day:", match[3]);         // "23"

// Named capturing groups (?<name>)
const dateRegex2 = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
const match2 = date.match(dateRegex2);
console.log("Named groups:", match2.groups);  // {year: "2024", month: "04", day: "23"}

// Non-capturing groups (?:)
const regex = /(?:https?):\/\/([^\/]+)/;
const url = "https://example.com";
const urlMatch = url.match(regex);
console.log("Non-capturing:", urlMatch);  // ["https://example.com", "example.com"]

// Backreferences \1, \2, etc.
const repeated = /(\w+)\s+\1/;  // Matches repeated words
console.log("Backreference:", repeated.test("hello hello")); // true
console.log("Backreference:", repeated.test("hello world")); // false


// ============================================================================
// 7. ALTERNATION AND LOOKAHEAD
// ============================================================================

console.log("\n=== Alternation and Lookahead ===");

// | - OR
console.log("Alternation:", /(cat|dog)/.test("I have a cat")); // true
console.log("Alternation:", /(cat|dog)/.test("I have a bird")); // false

// Positive lookahead (?=)
console.log("Lookahead:", /\d+(?= dollars)/.exec("100 dollars")); // ["100"]
console.log("Lookahead:", /\d+(?= dollars)/.exec("100 euros"));   // null

// Negative lookahead (?!)
console.log("Negative lookahead:", /\d+(?! dollars)/.exec("100 euros"));  // ["100"]
console.log("Negative lookahead:", /\d+(?! dollars)/.exec("100 dollars")); // null

// Positive lookbehind (?<=) - ES2018
console.log("Lookbehind:", /(?<=\$)\d+/.exec("$100"));  // ["100"]
console.log("Lookbehind:", /(?<=\$)\d+/.exec("€100"));  // null

// Negative lookbehind (?<!) - ES2018
console.log("Negative lookbehind:", /(?<!\$)\d+/.exec("€100")); // ["100"]


// ============================================================================
// 8. STRING METHODS WITH REGEX
// ============================================================================

console.log("\n=== String Methods ===");

const str = "The quick brown fox jumps over the lazy dog";

// match() - Returns array of matches
console.log("match:", str.match(/\b\w{5}\b/g));  // All 5-letter words

// matchAll() - Returns iterator of all matches (ES2020)
const regex3 = /\b(\w{5})\b/g;
for (const match of str.matchAll(regex3)) {
    console.log("matchAll:", match[0], "at", match.index);
}

// search() - Returns index of first match
console.log("search:", str.search(/fox/));  // 16

// replace() - Replace matches
console.log("replace:", str.replace(/fox/, "cat"));
console.log("replace all:", str.replace(/o/g, "0"));

// replace with function
const result2 = str.replace(/\b\w{4}\b/g, (match) => match.toUpperCase());
console.log("replace function:", result2);

// replaceAll() - Replace all matches (ES2021)
console.log("replaceAll:", str.replaceAll("o", "0"));

// split() - Split by regex
console.log("split:", str.split(/\s+/));  // Split by whitespace


// ============================================================================
// 9. COMMON PATTERNS
// ============================================================================

console.log("\n=== Common Patterns ===");

// Email validation (simple)
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
console.log("Email:", emailRegex.test("user@example.com"));

// Phone number (US format)
const phoneRegex = /^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$/;
console.log("Phone:", phoneRegex.test("(123) 456-7890"));
console.log("Phone:", phoneRegex.test("123-456-7890"));

// URL
const urlRegex = /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b/;
console.log("URL:", urlRegex.test("https://example.com"));

// Hex color
const hexRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
console.log("Hex:", hexRegex.test("#FF5733"));
console.log("Hex:", hexRegex.test("#F57"));

// Username (alphanumeric, 3-16 chars)
const usernameRegex = /^[a-zA-Z0-9_]{3,16}$/;
console.log("Username:", usernameRegex.test("user_123"));

// Password (min 8 chars, 1 uppercase, 1 lowercase, 1 number)
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
console.log("Password:", passwordRegex.test("Password123"));

// Extract hashtags
const tweetRegex = /#\w+/g;
const tweet = "Learning #JavaScript and #RegEx today!";
console.log("Hashtags:", tweet.match(tweetRegex));

// Remove HTML tags
const htmlRegex = /<[^>]*>/g;
const html2 = "<p>Hello <strong>World</strong></p>";
console.log("Strip HTML:", html2.replace(htmlRegex, ""));


// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

console.log("\n=== Best Practices ===");

/**
 * BEST PRACTICES:
 * 
 * 1. USE REGEX FOR PATTERN MATCHING, NOT PARSING
 *    - Don't parse HTML/XML with regex
 *    - Use proper parsers for complex formats
 * 
 * 2. ESCAPE SPECIAL CHARACTERS
 *    function escapeRegex(str) {
 *        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
 *    }
 * 
 * 3. TEST YOUR REGEX
 *    - Use online tools (regex101.com)
 *    - Test edge cases
 * 
 * 4. PREFER SIMPLE REGEX
 *    - Complex regex is hard to maintain
 *    - Sometimes multiple simple checks are better
 * 
 * 5. USE NON-CAPTURING GROUPS WHEN NOT NEEDED
 *    - (?:...) instead of (...)
 *    - Better performance
 * 
 * 6. BE CAREFUL WITH GREEDY QUANTIFIERS
 *    - Use lazy quantifiers (*?, +?, ??) when appropriate
 * 
 * 7. VALIDATE BUT DON'T OVER-VALIDATE
 *    - Email regex can be extremely complex
 *    - Often simple validation + real check is better
 */

// Escape special characters
function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const userInput = "How much? $100";
const escaped = escapeRegex(userInput);
console.log("Escaped:", escaped);


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Use /pattern/flags for regex literals");
console.log("2. Common flags: g (global), i (case-insensitive), m (multiline)");
console.log("3. Character classes: \\d (digit), \\w (word), \\s (space)");
console.log("4. Quantifiers: * (0+), + (1+), ? (0-1), {n,m} (range)");
console.log("5. Anchors: ^ (start), $ (end), \\b (word boundary)");
console.log("6. Groups: () capture, (?:) non-capture, (?<name>) named");
console.log("7. Use test() to check, match() to extract");
console.log("8. Escape special chars in user input");
console.log("=".repeat(80));
