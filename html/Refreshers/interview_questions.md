# HTML Technical Interview Questions

Based on the HTML Refreshers series (files 00-11 + review), here is a comprehensive list of possible questions that could be asked in a conversational technical interview, organized by topic and difficulty level.

---

## 🟢 JUNIOR LEVEL (Fundamentals)

### HTML Syntax & Document Structure

1. **What does `<!DOCTYPE html>` do, and why is it important? What happens if you omit it?**

   *Key points: Declares the document as HTML5. Triggers standards mode in browsers. Without it, browsers render in quirks mode, causing inconsistent CSS rendering and layout bugs.*

2. **Explain the basic structure of an HTML document. What are the three main sections and their purposes?**

   *Key points: `<!DOCTYPE html>`, `<html>` (root element), `<head>` (metadata, title, links), `<body>` (visible content). The head contains non-visual metadata; the body contains all rendered content.*

3. **What is the difference between a void element (self-closing) and a container element? Give examples of each.**

   *Key points: Void elements have no content and no closing tag (e.g., `<br>`, `<img>`, `<input>`, `<hr>`). Container elements wrap content and have opening/closing tags (e.g., `<div>`, `<p>`, `<span>`).*

4. **What is the purpose of the `lang` attribute on the `<html>` element? Why is it important for accessibility and SEO?**

   *Key points: Declares the document's language. Screen readers use it for correct pronunciation. Search engines use it for language-specific indexing. Example: `<html lang="en">`.*

5. **Why should `<meta charset="UTF-8">` be placed within the first 1024 bytes of the document?**

   *Key points: The browser needs to know the character encoding before parsing the rest of the document. If placed too late, some characters may be misinterpreted. UTF-8 is the standard for web content.*

6. **What is the difference between an element's `id` and `class` attributes? When would you use each?**

   *Key points: `id` must be unique per page, used for fragment identifiers, JavaScript hooks, and label associations. `class` can be reused across multiple elements, used for CSS styling and grouping.*

7. **What are boolean attributes in HTML? Give examples of how they are written.**

   *Key points: Attributes that are true when present, false when absent. Examples: `disabled`, `required`, `checked`, `readonly`, `hidden`. Written as `<input disabled>` or `<input disabled="disabled">`.*

8. **How does HTML handle whitespace? What is "whitespace collapse" and how can you preserve whitespace?**

   *Key points: Multiple spaces, tabs, and newlines collapse into a single space. Preserve with `<pre>`, `white-space: pre` in CSS, or `&nbsp;` for non-breaking spaces.*

9. **What is the DOM tree, and how does the browser build it from HTML?**

   *Key points: The DOM (Document Object Model) is a tree representation of the HTML document. The browser parses HTML tokens, creates nodes, and builds a tree structure where each element is a node with parent-child relationships.*

10. **Why do `<script>` tags without `async` or `defer` block HTML parsing? Where should scripts be placed?**

    *Key points: Scripts can modify the DOM via `document.write()`, so the parser must wait. Place scripts just before `</body>` or use `defer`/`async` to avoid blocking.*

### Text Elements & Content

11. **What are the six heading levels in HTML, and what are the rules for using them properly?**

    *Key points: `<h1>` through `<h6>`. Rules: one `<h1>` per page, don't skip levels, use for hierarchy not size, headings should describe the content that follows.*

12. **Why should you never skip heading levels (e.g., h1 → h3)? What impact does this have on accessibility?**

    *Key points: Screen reader users navigate by heading levels. Skipping breaks the document outline and confuses users. Always maintain a logical hierarchy (h1 → h2 → h3).*

13. **What is the difference between `<strong>` and `<b>`? Between `<em>` and `<i>`? When should you use each?**

    *Key points: `<strong>` = strong importance (semantic), `<b>` = bold styling (presentational). `<em>` = emphasis (semantic, changes sentence meaning), `<i>` = italic (technical terms, foreign words). Prefer semantic elements.*

14. **When should you use `<br>` for line breaks, and when should you avoid it?**

    *Key points: Use for poems, addresses, or text where line breaks are part of the content. Avoid for creating spacing between blocks (use CSS margin/padding instead).*

15. **What is the difference between an ordered list (`<ol>`), an unordered list (`<ul>`), and a description list (`<dl>`)? When would you choose each?**

    *Key points: `<ol>` for sequential/ranked items (steps, rankings). `<ul>` for non-sequential items (features, navigation). `<dl>` for key-value pairs (glossary, metadata).*

16. **What attributes does `<ol>` support for controlling numbering (type, start, reversed)?**

    *Key points: `type` (1, A, a, I, i), `start` (starting number), `reversed` (descending order). Example: `<ol type="A" start="3" reversed>` starts at C and counts down.*

17. **How do you create a nested list in HTML?**

    *Key points: Place a new `<ul>` or `<ol>` inside a `<li>` element. The nested list is indented visually. Always close the parent `<li>` after the nested list.*

18. **What is the difference between `<blockquote>` and `<q>`? What does the `cite` attribute do?**

    *Key points: `<blockquote>` for long block-level quotations. `<q>` for short inline quotations (browsers add quotes automatically). `cite` attribute specifies the source URL of the quote.*

19. **What is the purpose of `<pre>` and how does it differ from `<code>`? When would you nest them?**

    *Key points: `<pre>` preserves whitespace and uses monospace font. `<code>` marks inline code snippets. Nest `<code>` inside `<pre>` for code blocks: `<pre><code>...</code></pre>`.*

20. **What is the semantic meaning of `<hr>`? When is it appropriate to use it vs. using CSS borders?**

    *Key points: `<hr>` represents a thematic break between content sections (e.g., scene change in a story). Use it semantically, not just for visual lines. Use CSS borders for purely decorative lines.*

### Links & Navigation

21. **What are the four URL types in HTML (absolute, relative, root-relative, protocol-relative)? When would you use each?**

    *Key points: Absolute (`https://example.com/page`) — external links. Relative (`page.html`, `../page.html`) — same-site links. Root-relative (`/page.html`) — same-site from root. Protocol-relative (`//example.com/page`) — matches current protocol (deprecated).*

22. **What does `target="_blank"` do, and what security vulnerability does it introduce? How do you mitigate it?**

    *Key points: Opens link in new tab. Vulnerability: the opened page can access `window.opener` to redirect the original page. Mitigate with `rel="noopener noreferrer"`.*

23. **What is the purpose of the `download` attribute on an anchor tag? What limitation does it have?**

    *Key points: Tells the browser to download the linked resource instead of navigating to it. Limitation: only works for same-origin URLs (CORS restriction).*

24. **How do you create an email link with a pre-filled subject and body?**

    *Key points: `<a href="mailto:user@example.com?subject=Hello&body=Message">`. Use URL encoding for special characters. Multiple recipients with comma separation.*

25. **What is a fragment identifier, and how do you link to a specific section on the same page or another page?**

    *Key points: `#id` links to an element with that `id`. Same page: `<a href="#section">`. Different page: `<a href="page.html#section">`. The browser scrolls to the target element.*

26. **What is a "skip link" and why is it important for accessibility?**

    *Key points: A hidden link at the top of the page that jumps to the main content. Allows keyboard and screen reader users to bypass repetitive navigation. Usually the first focusable element.*

27. **What is the LVHA order for styling link states in CSS, and why does the order matter?**

    *Key points: `:link` → `:visited` → `:hover` → `:active`. Order matters because later states override earlier ones. If `:hover` comes after `:active`, hover styles would persist during click.*

28. **What does `rel="nofollow"` tell search engines? When should you use it?**

    *Key points: Tells search engines not to pass link equity (PageRank) to the linked page. Use for: user-generated content, paid links, untrusted sources, login pages.*

29. **What is the difference between `rel="noopener"` and `rel="noreferrer"`? When should you use them together?**

    *Key points: `noopener` prevents `window.opener` access. `noreferrer` does the same + hides the referrer header. Use both with `target="_blank"` for maximum security and privacy.*

30. **How do you create a breadcrumb navigation using semantic HTML?**

    *Key points: Use `<nav aria-label="Breadcrumb">` with an `<ol>` containing `<li>` items. Use `<a>` for links and `<span aria-current="page">` for the current page. Separate with CSS, not characters.*

### Images & Media

31. **What are the two required attributes on every `<img>` element? What happens if you omit each one?**

    *Key points: `src` (source URL) and `alt` (alternative text). Without `src`, nothing renders. Without `alt`, screen readers read the filename, and the image is not accessible.*

32. **What should the `alt` text be for an informative image vs. a decorative image vs. a functional image (link/button)?**

    *Key points: Informative: describe the content/information conveyed. Decorative: `alt=""` (empty) so screen readers ignore it. Functional: describe the action/function (e.g., "Search" for a search icon).*

33. **What is the purpose of the `width` and `height` attributes on images? How do they help with Core Web Vitals?**

    *Key points: Set the intrinsic dimensions of the image. The browser reserves space before the image loads, preventing Cumulative Layout Shift (CLS). Always set them to the image's actual dimensions.*

34. **What is the `<figure>` element, and how does it differ from `<aside>`?**

    *Key points: `<figure>` wraps self-contained content (images, diagrams, code) with an optional `<figcaption>`. `<aside>` contains tangentially related content. `<figure>` content can be moved without affecting the main flow.*

35. **What attributes does the `<video>` element support (controls, autoplay, muted, loop, poster, preload)?**

    *Key points: `controls` — show browser controls. `autoplay` — start playing (requires `muted`). `muted` — start muted. `loop` — restart when finished. `poster` — placeholder image. `preload` — hint for loading (none/metadata/auto).*

36. **Why do most browsers block `autoplay` with audio? How do you create an autoplaying video background?**

    *Key points: Browsers block audible autoplay to prevent unwanted noise. For video backgrounds: add `autoplay muted loop playsinline`. The `muted` attribute allows autoplay.*

37. **What is the purpose of the `<track>` element inside `<video>`? What kinds of tracks can it specify?**

    *Key points: Provides timed text tracks. Types: `subtitles` (translation), `captions` (dialogue + sounds, for deaf users), `descriptions` (video description for blind users), `chapters`, `metadata`.*

38. **What is the difference between JPEG, PNG, GIF, WebP, AVIF, and SVG? When would you choose each format?**

    *Key points: JPEG — photos (lossy, small). PNG — screenshots, transparency (lossless). GIF — simple animations (limited colors). WebP — modern replacement for JPEG/PNG (better compression). AVIF — newest, best compression. SVG — icons, logos (vector, scalable).*

39. **What is the purpose of the `loading="lazy"` attribute on images and iframes?**

    *Key points: Defers loading offscreen images/iframes until the user scrolls near them. Improves initial page load performance and saves bandwidth. Supported natively in modern browsers.*

40. **How do you provide format fallbacks using the `<picture>` element?**

    *Key points: `<picture>` contains multiple `<source>` elements with different `srcset` and `type` attributes, followed by a fallback `<img>`. The browser picks the first supported format.*

### Tables

41. **What is the difference between `<th>` and `<td>`? When should you use each?**

    *Key points: `<th>` = table header (bold, centered by default, semantic). `<td>` = table data cell. Use `<th>` for column/row headers, `<td>` for data values.*

42. **What are the three semantic table sections (`<thead>`, `<tbody>`, `<tfoot>`) and what are their benefits?**

    *Key points: `<thead>` — header rows. `<tbody>` — data rows (can have multiple). `<tfoot>` — summary/footer rows. Benefits: semantic structure, CSS targeting, screen reader navigation, printing headers on each page.*

43. **Why must `<tfoot>` come before `<tbody>` in the HTML source order?**

    *Key points: The browser can render the footer before loading all data rows. This allows users to see totals/summaries without waiting for the entire table to download.*

44. **How do `colspan` and `rowspan` work? What happens if the total cell count doesn't match across rows?**

    *Key points: `colspan` merges cells horizontally, `rowspan` vertically. If cell counts don't match, the table layout breaks — cells may overflow or create unexpected gaps.*

45. **What is the purpose of `<colgroup>` and `<col>`? What CSS properties can they control?**

    *Key points: `<colgroup>` groups columns for styling. `<col>` represents individual columns. Can control: `width`, `background`, `border`, `visibility`. Cannot control: padding, text alignment.*

46. **What is the purpose of the `scope` attribute on `<th>`? What values can it take?**

    *Key points: Associates header cells with data cells. Values: `col` (column header), `row` (row header), `colgroup`, `rowgroup`. Helps screen readers understand table structure.*

47. **How do you use `headers` and `id` attributes to associate data cells with header cells in complex tables?**

    *Key points: Give each `<th>` a unique `id`. Add `headers="id1 id2"` to `<td>` cells to reference multiple headers. Used for complex tables with merged cells.*

48. **Why should you never use tables for page layout? What should you use instead?**

    *Key points: Tables are not responsive, create accessibility issues (screen readers read linearly), increase code complexity, and mix presentation with content. Use CSS Grid or Flexbox instead.*

49. **What techniques can you use to make tables responsive on small screens?**

    *Key points: Horizontal scroll (overflow-x), convert rows to cards (display: block on small screens), hide less important columns, use `data-label` attributes with `::before` to show headers inline.*

50. **What is the purpose of `<caption>` in a table?**

    *Key points: Provides a title/summary for the table. Helps screen reader users understand the table's purpose before navigating its cells. Should be the first child of `<table>`.*

### Forms & Input

51. **What is the difference between GET and POST form methods? When would you use each?**

    *Key points: GET — data in URL (visible, bookmarkable, cached). POST — data in request body (hidden, no size limit, not cached). Use GET for searches/filters, POST for mutations (create/update/delete).*

52. **When must you use `enctype="multipart/form-data"` on a form?**

    *Key points: Required when the form contains file uploads (`<input type="file">`). This encoding allows binary data to be sent. Other encodings can't handle file data.*

53. **What HTML5 input types are available, and what benefits do they provide over plain `<input type="text">`?**

    *Key points: `email`, `url`, `tel`, `number`, `date`, `time`, `color`, `range`, `search`. Benefits: built-in validation, mobile-friendly keyboards, native date pickers, semantic meaning.*

54. **What is the difference between `<button>` and `<input type="submit">`? Why is `<button>` generally preferred?**

    *Key points: `<button>` can contain HTML (icons, text formatting), is easier to style, and has better semantics. `<input type="submit">` can only show text. `<button>` is preferred for flexibility.*

55. **What is the purpose of `<fieldset>` and `<legend>`? When should you use them?**

    *Key points: `<fieldset>` groups related form controls. `<legend>` provides a label for the group. Use for: radio button groups, address sections, payment information. Improves form accessibility.*

56. **What are the two ways to associate a `<label>` with an input? Which is preferred and why?**

    *Key points: 1) Wrap input inside `<label>`. 2) Use `for` attribute matching input's `id`. Explicit `for`/`id` is preferred because it works even when label and input are not adjacent.*

57. **What HTML5 validation attributes are available (required, minlength, maxlength, min, max, pattern)?**

    *Key points: `required` — field must be filled. `minlength`/`maxlength` — text length limits. `min`/`max` — numeric/date range. `pattern` — regex validation. All trigger browser-native validation.*

58. **How do you use the `pattern` attribute for regex validation? Give an example for a US ZIP code.**

    *Key points: `<input pattern="[0-9]{5}(-[0-9]{4})?" title="5-digit ZIP or ZIP+4">`. The `title` attribute provides the error message. The regex is tested against the input value.*

59. **What is the difference between `disabled` and `readonly` on an input?**

    *Key points: `disabled` — input is not submitted, not focusable, grayed out. `readonly` — input is submitted, focusable, but not editable. Use `readonly` when the value should be sent but not changed.*

60. **What is a honeypot field, and how does it help prevent spam?**

    *Key points: A hidden form field that humans don't see but bots fill in. If the field has a value on submission, it's likely spam. Hide with CSS (not `type="hidden"` which bots can detect).*

---

## 🟡 MID-LEVEL (Intermediate)

### Semantic HTML & Document Architecture

61. **What is "divitis" and why is it a problem? How do you refactor non-semantic markup into semantic HTML?**

    *Key points: Overusing `<div>` and `<span>` instead of semantic elements. Problems: poor accessibility, unclear structure, harder maintenance. Refactor: replace `<div class="nav">` with `<nav>`, `<div class="main">` with `<main>`, etc.*

62. **What are the HTML5 landmark elements, and what ARIA roles do they map to automatically?**

    *Key points: `<header>` → `role="banner"`, `<nav>` → `role="navigation"`, `<main>` → `role="main"`, `<aside>` → `role="complementary"`, `<footer>` → `role="contentinfo"`, `<form>` → `role="form"` (when has accessible name).*

63. **What is the difference between `<article>` and `<section>`? When would you choose each?**

    *Key points: `<article>` is self-contained, independently distributable content (blog post, news story). `<section>` groups related content within a document. An article can contain sections; a section can contain articles.*

64. **What is the difference between `<section>` and `<div>`? When is it appropriate to use a `<div>`?**

    *Key points: `<section>` has semantic meaning (thematic grouping) and should have a heading. `<div>` has no semantic meaning. Use `<div>` only when no semantic element fits (purely for styling or scripting).*

65. **What is the purpose of `<aside>`? How does it differ from `<figure>`?**

    *Key points: `<aside>` contains content tangentially related to the main content (sidebar, pull quotes, related links). `<figure>` contains self-contained media with optional caption. `<aside>` content is related but not essential.*

66. **Why should there be only one `<main>` element per page? What should and shouldn't go inside it?**

    *Key points: `<main>` represents the primary content. Only one for accessibility (skip links, screen reader landmarks). Don't put: site-wide navigation, logos, copyright, sidebar content.*

67. **When should you use `<nav>` vs. just a group of links? Should footer links be wrapped in `<nav>`?**

    *Key points: Use `<nav>` for major navigation blocks (primary nav, table of contents). Footer links can be wrapped in `<nav>` if they represent significant navigation. Simple legal links don't need `<nav>`.*

68. **What is the document outline, and how do heading levels and sectioning elements affect it?**

    *Key points: The document outline is the hierarchical structure of headings. Sectioning elements (`<article>`, `<section>`, `<nav>`, `<aside>`) can restart heading numbering within them. A proper outline helps screen reader navigation.*

69. **How do you use `<time>` with the `datetime` attribute? Why is it beneficial for SEO?**

    *Key points: `<time datetime="2024-01-15">January 15</time>`. The `datetime` attribute provides a machine-readable format. Benefits: search engines can display dates in search results, calendar integration, better semantic meaning.*

70. **What is the purpose of `<address>`? Where should it be placed?**

    *Key points: Provides contact information for the page or article author (physical address, email, phone). Place inside `<footer>` or `<article>` footer. Not for arbitrary addresses (use `<p>` instead).*

### HTML5 APIs

71. **How does the Geolocation API work? What permissions does it require, and what protocol must the page use?**

    *Key points: `navigator.geolocation.getCurrentPosition(success, error)`. Requires user permission (browser prompt). Must use HTTPS (except localhost). Returns latitude, longitude, accuracy.*

72. **What is the difference between `localStorage` and `sessionStorage`? How do they compare to cookies in terms of capacity and scope?**

    *Key points: `localStorage` persists until explicitly cleared. `sessionStorage` clears when tab closes. Both have ~5-10MB capacity. Cookies have ~4KB. `localStorage`/`sessionStorage` are not sent with HTTP requests.*

73. **What event fires when localStorage changes in another tab? How can you use this for cross-tab communication?**

    *Key points: The `storage` event fires on other tabs/windows when localStorage changes. Use for: syncing settings across tabs, logout across all tabs, real-time data updates.*

74. **How does the History API's `pushState` differ from using hash-based routing? When would you choose each?**

    *Key points: `pushState` changes URL without hash, enables real URLs, requires server-side fallback. Hash-based routing uses `#/path`, works without server config, simpler. Choose `pushState` for SEO-friendly SPAs, hash for simple demos.*

75. **What events are involved in the Drag and Drop API? What does `e.preventDefault()` do in a `dragover` handler?**

    *Key points: Events: `dragstart`, `dragover`, `dragenter`, `dragleave`, `drop`, `dragend`. `e.preventDefault()` in `dragover` is required to allow dropping — without it, the `drop` event never fires.*

76. **How does the Clipboard API work? Why does it require a user gesture for write operations?**

    *Key points: `navigator.clipboard.writeText()` and `readText()`. Write requires user gesture (click/keypress) to prevent malicious sites from silently copying data. Read requires additional permission.*

77. **What is the Page Visibility API, and what are practical use cases for it?**

    *Key points: `document.visibilityState` (visible/hidden) and `visibilitychange` event. Use cases: pause video/animations when tab is hidden, stop polling, reduce resource usage, track user engagement.*

78. **What is the difference between a Web Worker and a Service Worker? What can each access?**

    *Key points: Web Worker: runs scripts in background threads, can use `XMLHttpRequest`/`fetch`, no DOM access. Service Worker: network proxy, intercepts fetch requests, enables offline support, no DOM access, requires HTTPS.*

79. **Describe the Service Worker lifecycle (install, waiting, activate, fetch).**

    *Key points: Install — cache assets. Waiting — waits until all tabs close. Activate — clean old caches, take control. Fetch — intercept network requests, serve cached or network responses.*

80. **Why do Service Workers require HTTPS (except localhost)?**

    *Key points: Service Workers are powerful network proxies that can intercept and modify all requests. HTTPS ensures the SW code hasn't been tampered with (man-in-the-middle protection).*

### Accessibility (A11y)

81. **What are the four WCAG POUR principles? Give an example of each.**

    *Key points: Perceivable — content must be presentable to senses (alt text on images). Operable — UI must be usable (keyboard navigation). Understandable — content and UI must be clear (predictable behavior). Robust — content must work with assistive technologies (valid HTML).*

82. **What are the three WCAG conformance levels (A, AA, AAA)? Which should most sites target?**

    *Key points: A — minimum (must have). AA — recommended (most legal requirements). AAA — highest (not all content can meet this). Most sites should target AA.*

83. **What is the first rule of ARIA? Why should you prefer native HTML elements over ARIA roles?**

    *Key points: "Don't use ARIA if you can use a native HTML element." Native elements have built-in keyboard handling, focus management, and screen reader support. ARIA adds complexity and can introduce bugs.*

84. **What is the difference between `aria-label`, `aria-labelledby`, and `aria-describedby`? When would you use each?**

    *Key points: `aria-label` — provides an accessible name directly. `aria-labelledby` — references another element for the name. `aria-describedby` — provides additional description. Use `aria-label` for icon buttons, `aria-labelledby` for form groups.*

85. **What does `aria-expanded` indicate, and how should it be used with expandable content?**

    *Key points: Indicates whether a collapsible element is expanded (true) or collapsed (false). Must be toggled via JavaScript when the content expands/collapses. Used on the triggering button.*

86. **What is the difference between `aria-live="polite"` and `aria-live="assertive"`? When should you use each?**

    *Key points: `polite` — announces changes when user is idle (chat messages, notifications). `assertive` — interrupts immediately (critical errors, time warnings). Use `polite` by default, `assertive` sparingly.*

87. **What is the purpose of `aria-current`? What values can it take?**

    *Key points: Indicates the current item in a set. Values: `page` (current page in nav), `step` (current step in wizard), `location` (current item in a flow), `date`, `time`, `true`. Used in navigation menus.*

88. **How do you implement a skip navigation link? What CSS is needed to show it on focus?**

    *Key points: Add `<a href="#main" class="skip-link">Skip to content</a>` at the top. CSS: position off-screen by default, `:focus` brings it into view. Use `position: absolute; transform: translateX(-100%)` and `:focus { transform: translateX(0) }`.*

89. **What is focus trapping, and why is it important for modal dialogs?**

    *Key points: Keeping keyboard focus within a modal while it's open. Prevents users from tabbing to background content. When modal closes, return focus to the triggering element. Essential for keyboard accessibility.*

90. **Why should you never use `*:focus { outline: none; }`? What should you use instead?**

    *Key points: Removes visible focus indicators, making the site unusable for keyboard users. Instead: use `:focus-visible` to show focus only when needed (keyboard navigation), or create custom focus styles with sufficient contrast.*

91. **What is the minimum color contrast ratio for normal text (WCAG AA)? For large text?**

    *Key points: Normal text: 4.5:1. Large text (≥18px bold or ≥24px regular): 3:1. AAA requires 7:1 for normal text, 4.5:1 for large text.*

92. **How do you test a website for accessibility? What tools and manual tests should you use?**

    *Key points: Automated tools: axe DevTools, Lighthouse, WAVE. Manual tests: keyboard-only navigation, screen reader (VoiceOver/NVDA), zoom to 200%, color contrast checkers. No automated tool catches everything.*

### SEO & Metadata

93. **What is the most important SEO element in the `<head>`? What are best practices for writing it?**

    *Key points: The `<title>` element. Best practices: unique per page, 50-60 characters, include primary keyword near the start, descriptive and compelling, include brand name at the end.*

94. **What is the ideal length for a meta description, and what should it include?**

    *Key points: 150-160 characters. Include: primary keyword, value proposition, call to action. Should be unique per page and accurately describe the content. Appears in search results below the title.*

95. **What is the Open Graph protocol, and what are the four required OG meta tags?**

    *Key points: Protocol that controls how content appears when shared on social media (Facebook, LinkedIn). Required tags: `og:title`, `og:description`, `og:image`, `og:url`. Also `og:type` is recommended.*

96. **What are the recommended dimensions for an Open Graph image?**

    *Key points: 1200×630 pixels (1.91:1 aspect ratio). Minimum: 600×315. Maximum: 8MB. Use PNG or JPEG. Include text overlay for context when shared without description.*

97. **What is the difference between `summary` and `summary_large_image` Twitter Card types?**

    *Key points: `summary` — small square image (120×120) next to title/description. `summary_large_image` — large image (280×150) at top with title/description below. Use `summary_large_image` for visually rich content.*

98. **What is a canonical URL, and when should you use it?**

    *Key points: `<link rel="canonical" href="https://example.com/page">`. Tells search engines which URL is the preferred version. Use for: duplicate content, WWW vs non-WWW, HTTP vs HTTPS, paginated content, URL parameters.*

99. **What is hreflang, and what are the rules for implementing it correctly?**

    *Key points: `<link rel="alternate" hreflang="es" href="...">`. Tells search engines which language/region version to show. Rules: must be bidirectional (page A links to B, B links to A), include self-referencing tag, use ISO language codes.*

100. **What is structured data (JSON-LD / Schema.org)? Give examples of common schema types (Article, Product, FAQ, BreadcrumbList).**

     *Key points: JSON-LD structured data helps search engines understand content. Examples: `Article` (news/blog), `Product` (price, availability), `FAQPage` (Q&A pairs), `BreadcrumbList` (navigation path). Enables rich snippets in search results.*

101. **What is the difference between `noindex` and `nofollow`? When would you use each?**

     *Key points: `noindex` — prevents page from appearing in search results. `nofollow` — prevents following links on the page. Use `noindex` for admin/login pages, `nofollow` for user-generated content links.*

102. **What is the purpose of a sitemap.xml and robots.txt?**

     *Key points: `sitemap.xml` lists all pages for search engines to discover and crawl. `robots.txt` tells crawlers which URLs they can/cannot access. Both are placed in the root directory.*

### Embedding & Iframes

103. **What is the `sandbox` attribute on an iframe? What restrictions does it apply, and how do you selectively allow capabilities?**

     *Key points: Applies restrictions to the iframe content. Default: all restrictions enabled. Allow selectively: `allow-scripts`, `allow-same-origin`, `allow-forms`, `allow-popups`. Without `allow-same-origin`, the iframe can't access its own cookies/storage.*

104. **Why is the `title` attribute required on every iframe for accessibility?**

     *Key points: Screen readers announce the iframe title so users know what content to expect. Without a title, users hear "frame" with no context. The title should describe the embedded content.*

105. **How does `postMessage` work for cross-origin communication? Why must you always verify `event.origin`?**

     *Key points: `iframe.contentWindow.postMessage(data, targetOrigin)` sends data. Parent listens with `window.addEventListener('message', handler)`. Always verify `event.origin` to prevent malicious sites from sending fake messages.*

106. **What is the padding-bottom technique for responsive iframes? How does it work?**

     *Key points: Wrap iframe in a container with `position: relative` and `padding-bottom: 56.25%` (16:9). Set iframe to `position: absolute; width: 100%; height: 100%`. The padding creates the aspect ratio box.*

107. **What is the modern `aspect-ratio` CSS property alternative for responsive iframes?**

     *Key points: Set `aspect-ratio: 16 / 9` on the iframe or its container with `width: 100%`. No padding hack needed. More intuitive and cleaner than the padding-bottom technique.*

108. **What is the difference between `<object>` and `<embed>`? Which supports fallback content?**

     *Key points: Both embed external content (PDFs, plugins). `<object>` supports fallback content between tags (shown if the resource fails). `<embed>` is a void element with no fallback. `<object>` is preferred.*

109. **How do you lazy-load iframes using native `loading="lazy"` and the Intersection Observer API?**

     *Key points: Native: `<iframe loading="lazy" src="...">`. Intersection Observer: observe when iframe enters viewport, then set `src` attribute. Native is simpler; Intersection Observer gives more control.*

110. **What performance considerations should you keep in mind when using iframes?**

     *Key points: Each iframe loads a separate document (extra HTTP requests, memory). Lazy-load iframes. Use `sandbox` to restrict capabilities. Consider the parent page's LCP/CLS impact. Avoid iframes for layout.*

### Performance Optimization

111. **What is the Critical Rendering Path? What are the steps from HTML to pixels?**

     *Key points: 1) HTML → DOM (parsing). 2) CSS → CSSOM (parsing). 3) Render Tree (DOM + CSSOM). 4) Layout (calculate geometry). 5) Paint (pixel filling). 6) Composite (layers). Optimizing each step improves performance.*

112. **What is the difference between `async` and `defer` on script tags? When would you use each?**

     *Key points: `async` — downloads while parsing, executes as soon as downloaded (order not guaranteed). `defer` — downloads while parsing, executes after parsing in order. Use `async` for independent scripts (analytics), `defer` for scripts that depend on DOM order.*

113. **What is the difference between `preload`, `prefetch`, `preconnect`, and `dns-prefetch`? When would you use each?**

     *Key points: `preload` — load current page resource urgently. `prefetch` — load for future navigation. `preconnect` — early connection to origin. `dns-prefetch` — early DNS resolution. Use `preload` for critical fonts/images, `preconnect` for third-party origins.*

114. **What are the three Core Web Vitals (LCP, FID, CLS)? What are the target thresholds for each?**

     *Key points: LCP (Largest Contentful Paint) — < 2.5s. FID (First Input Delay) — < 100ms. CLS (Cumulative Layout Shift) — < 0.1. Measure loading, interactivity, and visual stability.*

115. **How do you optimize LCP (Largest Contentful Paint)?**

     *Key points: Optimize images (compress, next-gen formats, preload hero image). Minimize render-blocking resources. Use CDN. Optimize server response time. Preload critical resources. Eliminate large layout shifts.*

116. **How do you optimize CLS (Cumulative Layout Shift)? What causes layout shifts?**

     *Key points: Causes: images without dimensions, dynamic content injection, web fonts causing FOIT/FOUT, ads. Fix: set explicit width/height on images, use `aspect-ratio`, reserve space for ads/dynamic content, use `font-display: optional`.*

117. **What is `font-display` and what values does it support (swap, block, fallback, optional)?**

     *Key points: Controls how custom fonts are displayed while loading. `swap` — show fallback, swap when loaded. `block` — hide text briefly (FOIT). `fallback` — short swap period. `optional` — use fallback if font doesn't load quickly.*

118. **How do you measure Core Web Vitals using the Performance Observer API?**

     *Key points: Use `new PerformanceObserver((list) => {...})` observing `'largest-contentful-paint'`, `'first-input'`, `'layout-shift'`. Report via `navigator.sendBeacon()` to analytics endpoint.*

119. **What is a performance budget, and what metrics might it include?**

     *Key points: A performance budget sets limits on metrics to prevent regressions. Metrics: JS bundle size (< 200KB), image weight (< 1MB), TTI (< 3s), LCP (< 2.5s), number of HTTP requests. Enforced in CI/CD.*

120. **How do you defer non-critical CSS using `rel="preload"` with an `onload` handler?**

     *Key points: `<link rel="preload" href="non-critical.css" as="style" onload="this.onload=null;this.rel='stylesheet'">`. The preload starts the download, then the onload handler converts it to a stylesheet. Fallback with `<noscript>`.*

---

## 🔴 UPPER-MID TO SENIOR LEVEL

### Architecture & Design Patterns

121. **How would you architect a large-scale web application's HTML structure for maintainability, accessibility, and performance?**

     *Key points: Use semantic HTML5 landmarks, component-based architecture (each component has its own template), consistent naming conventions (BEM), lazy-load below-fold content, use template literals or frameworks for dynamic content, implement proper heading hierarchy.*

122. **What considerations go into choosing between client-side rendering (SPA), server-side rendering (SSR), and static site generation (SSG) from an HTML perspective?**

     *Key points: SPA — minimal HTML, JS renders everything (slow initial load, poor SEO). SSR — full HTML on server (good SEO, faster FCP, higher server load). SSG — pre-built HTML (fastest, best for static content). Consider: SEO needs, content freshness, user interactivity.*

123. **How do you implement a design system using semantic HTML patterns that works across multiple teams?**

     *Key points: Create a component library with consistent semantic HTML templates. Document patterns with examples. Use web components or framework-agnostic templates. Enforce via linting (HTML-validate, axe). Provide accessible defaults.*

124. **What strategies do you use to ensure HTML quality across a large codebase with many developers?**

     *Key points: Automated linting (HTML-validate, markuplint), accessibility testing in CI (axe-core), code reviews with HTML checklist, component library with documented patterns, template audits, performance budgets.*

125. **How would you progressively enhance a page that must work without JavaScript while providing a rich experience with it?**

     *Key points: Start with semantic HTML that works without JS. Use `<noscript>` for fallbacks. Enhance with JS: add interactivity, animations, dynamic loading. Test with JS disabled. Use `href` on links even for JS handlers.*

### Advanced Accessibility

126. **How do you implement an accessible custom component (e.g., a tab panel, accordion, or modal dialog) using ARIA?**

     *Key points: Follow WAI-ARIA Authoring Practices. Tab panel: `role="tablist"`, `role="tab"` with `aria-selected`, `role="tabpanel"`. Manage focus with arrow keys. Use `aria-expanded` for accordions. Modal: `role="dialog"`, `aria-modal="true"`, focus trap.*

127. **What is the difference between `role="alert"` and `aria-live="assertive"`? When should you use each?**

     *Key points: `role="alert"` is a specialized live region that implies `aria-live="assertive"` and `role="alert"`. Use `role="alert"` for important time-sensitive messages. Use `aria-live="assertive"` for dynamic content updates that need immediate announcement.*

128. **How do you handle focus management in a single-page application when navigating between routes?**

     *Key points: Move focus to the main content area after route change. Use `document.querySelector('main').focus({ preventScroll: false })`. Announce route changes to screen readers. Manage focus for dynamic content. Return focus for modals.*

129. **What is the accessibility tree, and how do ARIA attributes affect it?**

     *Key points: The accessibility tree is a subset of the DOM that browsers expose to assistive technologies. ARIA attributes modify the accessibility tree (roles, states, properties) without changing the DOM. Screen readers use this tree for navigation.*

130. **How do you test for accessibility with screen readers (VoiceOver, NVDA, JAWS)? What common issues do you look for?**

     *Key points: Test with: VoiceOver (Mac), NVDA (Windows free), JAWS (Windows paid). Check: all interactive elements are reachable, focus order is logical, headings are announced, images have alt text, forms have labels, live regions announce updates.*

### Advanced Forms & Validation

131. **How do you implement a multi-step form (wizard) with validation at each step, preserving state on back navigation?**

     *Key points: Use a single `<form>` with hidden/shown sections. Validate each step before proceeding. Store data in JS object or sessionStorage. On back, restore previous values. Use `novalidate` attribute and custom validation. Maintain focus management.*

132. **How do you implement real-time validation with custom error messages while maintaining accessibility?**

     *Key points: Use `input`/`blur` events for real-time validation. Show errors with `aria-describedby` linking to error element. Use `aria-invalid="true"` on invalid inputs. Announce errors with `aria-live="polite"`. Don't validate before user interaction.*

133. **What is the `Constraint Validation API`, and how do you use `setCustomValidity()` for custom validation?**

     *Key points: API for HTML5 form validation. `element.setCustomValidity('message')` sets a custom error. Empty string means valid. `element.checkValidity()` returns boolean. `element.reportValidity()` shows the validation UI. `validationMessage` gets the current error.*

134. **How do you handle form autofill for credit cards, addresses, and passwords using the `autocomplete` attribute?**

     *Key points: Use appropriate `autocomplete` values: `cc-number`, `cc-exp`, `cc-csc`, `street-address`, `postal-code`, `current-password`, `new-password`. Group related fields in `<fieldset>`. Use `webauthn` for passwordless auth.*

135. **How would you design a form that gracefully handles network failures and prevents duplicate submissions?**

     *Key points: Disable submit button on first click. Show loading state. Store form data in sessionStorage. On network failure, show error with retry option. Use `navigator.onLine` to check connectivity. Implement idempotency keys for server-side dedup.*

### Advanced Performance

136. **How do you implement code-splitting and lazy-loading for JavaScript in an HTML-first way?**

     *Key points: Use `<script type="module">` with dynamic `import()`. Use `loading="lazy"` for images/iframes. Use Intersection Observer for component loading. Use `rel="preload"` for critical resources. Framework tools: React.lazy, Vue async components.*

137. **What is the difference between `requestIdleCallback` and `requestAnimationFrame`? When would you use each for performance?**

     *Key points: `requestAnimationFrame` runs before next paint (60fps) — use for visual updates (animations). `requestIdleCallback` runs when browser is idle — use for non-critical tasks (analytics, prefetching). Both help avoid jank.*

138. **How do you implement a service worker caching strategy (Cache First, Network First, Stale While Revalidate)?**

     *Key points: Cache First — serve from cache, fetch to update cache (static assets). Network First — try network, fall back to cache (API calls). Stale While Revalidate — serve cached immediately, fetch update in background (content pages).*

139. **What is the Navigation and Resource Timing API, and how do you use it for real user monitoring (RUM)?**

     *Key points: `performance.getEntriesByType('navigation')` gives page load metrics (DNS, TCP, TTFB, DOMContentLoaded). `performance.getEntriesByType('resource')` gives individual resource timing. Send to analytics for RUM dashboards.*

140. **How do you optimize the Critical Rendering Path for a page with third-party scripts (analytics, ads, widgets)?**

     *Key points: Load third-party scripts with `async` or `defer`. Use `preconnect`/`dns-prefetch` for third-party origins. Lazy-load non-critical widgets. Use `rel="preload"` for critical resources. Consider using a tag manager with loading priorities.*

### Security

141. **What is Content Security Policy (CSP), and how do you implement it via a `<meta>` tag or HTTP header?**

     *Key points: CSP restricts which resources can load. Implement via `Content-Security-Policy` HTTP header or `<meta http-equiv="Content-Security-Policy">`. Example: `default-src 'self'; script-src 'self' https://analytics.example.com`. Start with report-only mode.*

142. **What is the `sandbox` attribute's security model for iframes? What attacks does it prevent?**

     *Key points: Sandbox restricts iframe capabilities. Prevents: form submission, script execution, popups, same-origin access, navigation. Add specific permissions: `allow-scripts`, `allow-same-origin`, `allow-forms`. Without `allow-same-origin`, the iframe is treated as unique origin.*

143. **How do you prevent clickjacking? What's the difference between the `X-Frame-Options` header and CSP's `frame-ancestors`?**

     *Key points: `X-Frame-Options: DENY` or `SAMEORIGIN` — older, simpler. CSP `frame-ancestors 'self'` — newer, more flexible (supports multiple origins, more precise). CSP is preferred as it's more powerful and supersedes X-Frame-Options.*

144. **What is a CSRF token, and how is it implemented in HTML forms?**

     *Key points: A unique, server-generated token embedded in forms. Server validates the token on submission. Implementation: `<input type="hidden" name="csrf_token" value="random-token">`. Token is tied to user session. Prevents cross-site request forgery.*

145. **What is Subresource Integrity (SRI), and how do you use the `integrity` attribute on `<script>` and `<link>` tags?**

     *Key points: SRI ensures fetched resources haven't been tampered with. Add `integrity="sha384-hash"` to `<script>` or `<link>`. Browser computes hash of downloaded file and compares. If mismatch, resource is blocked. Generate hash with `openssl dgst -sha384 -binary file.js | base64`.*

### Emerging Standards & Future

146. **What is the `<dialog>` element, and how does it compare to implementing modals with ARIA?**

     *Key points: `<dialog>` provides native modal functionality. `.showModal()` opens as modal (with backdrop, focus trap). `.close()` closes. Built-in accessibility. Compared to ARIA: less code, native focus management, but less styling control. Use with caution for older browser support.*

147. **What is the `<search>` element (new in HTML 5.3)? How does it differ from using `<div role="search">`?**

     *Key points: `<search>` is a semantic element for search functionality. It implicitly has `role="search"`. Benefits: cleaner markup, built-in semantics, easier for screen readers. Use instead of `<div role="search">` for better semantics.*

148. **What is the `inert` attribute, and how does it help with focus management in modals and off-canvas navigation?**

     *Key points: `inert` makes an element and its children unfocusable and invisible to assistive technologies. Use on background content when a modal is open — prevents tabbing to background. More robust than manual focus trapping.*

149. **What is the `popover` API (the `popover` attribute and `<dialog>` integration)?**

     *Key points: `popover` attribute creates lightweight overlay content. `popover="auto"` (dismisses on outside click/Esc) or `popover="manual"` (must be closed programmatically). Can be used with `<dialog>` for enhanced modal behavior. No JS needed for basic show/hide.*

150. **How do you use the `loading="lazy"` attribute for iframes and images, and what is the `fetchpriority` attribute?**

     *Key points: `loading="lazy"` defers offscreen resources. `fetchpriority="high"` hints the browser to prioritize a resource (hero image, critical iframe). Combine: hero image gets `fetchpriority="high"`, below-fold images get `loading="lazy"`. Use sparingly.*

---

## 💡 BONUS: Behavioral & Problem-Solving Questions

151. **Describe a time you had to debug a cross-browser HTML rendering issue. What was the root cause and how did you fix it?**

     *Key points: Common issues: missing DOCTYPE (quirks mode), unsupported HTML5 elements in old IE, CSS vendor prefixes, different box-model interpretations. Fix: use feature detection, polyfills, normalize.css, test in multiple browsers, use caniuse.com.*

152. **How would you approach migrating a legacy website that uses tables for layout to modern semantic HTML?**

     *Key points: Audit current layout, plan new structure with semantic elements, replace tables with CSS Grid/Flexbox, ensure content is preserved, test accessibility, do incrementally (page by page), use feature detection for fallbacks.*

153. **You're tasked with improving the Lighthouse performance score of a slow page from 40 to 90+. What steps do you take?**

     *Key points: 1) Measure current performance. 2) Optimize images (compress, next-gen formats). 3) Minify CSS/JS/HTML. 4) Remove render-blocking resources. 5) Implement lazy-loading. 6) Add preload/preconnect. 7) Optimize fonts. 8) Reduce server response time. 9) Use CDN. 10) Re-measure and iterate.*

154. **How do you handle the trade-off between shipping HTML quickly and ensuring it's fully accessible?**

     *Key points: Use semantic HTML by default (it's free accessibility). Use automated tools in CI (axe-core). Prioritize critical accessibility (keyboard nav, screen reader support). Ship accessible components from a library. Fix issues iteratively. Never ship inaccessible forms or navigation.*

155. **Describe your HTML review process. What do you look for when reviewing a pull request that includes HTML changes?**

     *Key points: Check: semantic elements used correctly, proper heading hierarchy, images have alt text, forms have labels, ARIA is correct, no divitis, valid HTML, responsive patterns, performance considerations (lazy-loading), security (CSP, SRI).*

156. **How would you explain the importance of semantic HTML to a junior developer who only uses `<div>` and `<span>`?**

     *Key points: Semantic HTML is like labeling containers — it tells everyone (browsers, screen readers, search engines, other developers) what each part of the page means. It improves accessibility, SEO, and maintainability with zero extra effort.*

157. **You need to embed a third-party widget that doesn't support accessibility. What do you do?**

     *Key points: 1) Contact vendor for accessible version. 2) Wrap in iframe with sandbox. 3) Add `aria-label` and `role` attributes. 4) Provide accessible alternative (text version). 5) If critical, consider building custom accessible version. 6) Document accessibility limitations.*

158. **How do you approach making an existing single-page application work without JavaScript (progressive enhancement)?**

     *Key points: Start with server-rendered HTML for core content/functionality. Use `<noscript>` for fallbacks. Ensure forms work with traditional POST. Add JS enhancements on top. Use SSR for initial page load. Test with JS disabled.*

159. **What metrics do you track for HTML performance in production, and how do you set up alerting for regressions?**

     *Key points: Track: LCP, CLS, FID, TTFB, DOM Content Loaded, Time to Interactive, JS bundle size, image weight. Use: Lighthouse CI, Web Vitals library, RUM analytics (Google Analytics, Datadog). Alert on 20% degradation from baseline.*

160. **How would you design a component library's HTML API to be both flexible for developers and accessible for users?**

     *Key points: Use semantic HTML as foundation. Provide sensible defaults for accessibility. Allow customization via props/attributes while maintaining ARIA requirements. Document accessibility expectations. Include automated tests. Use web components for encapsulation.*
