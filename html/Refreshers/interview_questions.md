# HTML Technical Interview Questions

Based on the HTML Refreshers series (files 00-11 + review), here is a comprehensive list of possible questions that could be asked in a conversational technical interview, organized by topic and difficulty level.

---

## 🟢 JUNIOR LEVEL (Fundamentals)

### HTML Syntax & Document Structure

1. What does `<!DOCTYPE html>` do, and why is it important? What happens if you omit it?
2. Explain the basic structure of an HTML document. What are the three main sections and their purposes?
3. What is the difference between a void element (self-closing) and a container element? Give examples of each.
4. What is the purpose of the `lang` attribute on the `<html>` element? Why is it important for accessibility and SEO?
5. Why should `<meta charset="UTF-8">` be placed within the first 1024 bytes of the document?
6. What is the difference between an element's `id` and `class` attributes? When would you use each?
7. What are boolean attributes in HTML? Give examples of how they are written.
8. How does HTML handle whitespace? What is "whitespace collapse" and how can you preserve whitespace?
9. What is the DOM tree, and how does the browser build it from HTML?
10. Why do `<script>` tags without `async` or `defer` block HTML parsing? Where should scripts be placed?

### Text Elements & Content

11. What are the six heading levels in HTML, and what are the rules for using them properly?
12. Why should you never skip heading levels (e.g., h1 → h3)? What impact does this have on accessibility?
13. What is the difference between `<strong>` and `<b>`? Between `<em>` and `<i>`? When should you use each?
14. When should you use `<br>` for line breaks, and when should you avoid it?
15. What is the difference between an ordered list (`<ol>`), an unordered list (`<ul>`), and a description list (`<dl>`)? When would you choose each?
16. What attributes does `<ol>` support for controlling numbering (type, start, reversed)?
17. How do you create a nested list in HTML?
18. What is the difference between `<blockquote>` and `<q>`? What does the `cite` attribute do?
19. What is the purpose of `<pre>` and how does it differ from `<code>`? When would you nest them?
20. What is the semantic meaning of `<hr>`? When is it appropriate to use it vs. using CSS borders?

### Links & Navigation

21. What are the four URL types in HTML (absolute, relative, root-relative, protocol-relative)? When would you use each?
22. What does `target="_blank"` do, and what security vulnerability does it introduce? How do you mitigate it?
23. What is the purpose of the `download` attribute on an anchor tag? What limitation does it have?
24. How do you create an email link with a pre-filled subject and body?
25. What is a fragment identifier, and how do you link to a specific section on the same page or another page?
26. What is a "skip link" and why is it important for accessibility?
27. What is the LVHA order for styling link states in CSS, and why does the order matter?
28. What does `rel="nofollow"` tell search engines? When should you use it?
29. What is the difference between `rel="noopener"` and `rel="noreferrer"`? When should you use them together?
30. How do you create a breadcrumb navigation using semantic HTML?

### Images & Media

31. What are the two required attributes on every `<img>` element? What happens if you omit each one?
32. What should the `alt` text be for an informative image vs. a decorative image vs. a functional image (link/button)?
33. What is the purpose of the `width` and `height` attributes on images? How do they help with Core Web Vitals?
34. What is the `<figure>` element, and how does it differ from `<aside>`?
35. What attributes does the `<video>` element support (controls, autoplay, muted, loop, poster, preload)?
36. Why do most browsers block `autoplay` with audio? How do you create an autoplaying video background?
37. What is the purpose of the `<track>` element inside `<video>`? What kinds of tracks can it specify?
38. What is the difference between JPEG, PNG, GIF, WebP, AVIF, and SVG? When would you choose each format?
39. What is the purpose of the `loading="lazy"` attribute on images and iframes?
40. How do you provide format fallbacks using the `<picture>` element?

### Tables

41. What is the difference between `<th>` and `<td>`? When should you use each?
42. What are the three semantic table sections (`<thead>`, `<tbody>`, `<tfoot>`) and what are their benefits?
43. Why must `<tfoot>` come before `<tbody>` in the HTML source order?
44. How do `colspan` and `rowspan` work? What happens if the total cell count doesn't match across rows?
45. What is the purpose of `<colgroup>` and `<col>`? What CSS properties can they control?
46. What is the purpose of the `scope` attribute on `<th>`? What values can it take?
47. How do you use `headers` and `id` attributes to associate data cells with header cells in complex tables?
48. Why should you never use tables for page layout? What should you use instead?
49. What techniques can you use to make tables responsive on small screens?
50. What is the purpose of `<caption>` in a table?

### Forms & Input

51. What is the difference between GET and POST form methods? When would you use each?
52. When must you use `enctype="multipart/form-data"` on a form?
53. What HTML5 input types are available, and what benefits do they provide over plain `<input type="text">`?
54. What is the difference between `<button>` and `<input type="submit">`? Why is `<button>` generally preferred?
55. What is the purpose of `<fieldset>` and `<legend>`? When should you use them?
56. What are the two ways to associate a `<label>` with an input? Which is preferred and why?
57. What HTML5 validation attributes are available (required, minlength, maxlength, min, max, pattern)?
58. How do you use the `pattern` attribute for regex validation? Give an example for a US ZIP code.
59. What is the difference between `disabled` and `readonly` on an input?
60. What is a honeypot field, and how does it help prevent spam?

---

## 🟡 MID-LEVEL (Intermediate)

### Semantic HTML & Document Architecture

61. What is "divitis" and why is it a problem? How do you refactor non-semantic markup into semantic HTML?
62. What are the HTML5 landmark elements, and what ARIA roles do they map to automatically?
63. What is the difference between `<article>` and `<section>`? When would you choose each?
64. What is the difference between `<section>` and `<div>`? When is it appropriate to use a `<div>`?
65. What is the purpose of `<aside>`? How does it differ from `<figure>`?
66. Why should there be only one `<main>` element per page? What should and shouldn't go inside it?
67. When should you use `<nav>` vs. just a group of links? Should footer links be wrapped in `<nav>`?
68. What is the document outline, and how do heading levels and sectioning elements affect it?
69. How do you use `<time>` with the `datetime` attribute? Why is it beneficial for SEO?
70. What is the purpose of `<address>`? Where should it be placed?

### HTML5 APIs

71. How does the Geolocation API work? What permissions does it require, and what protocol must the page use?
72. What is the difference between `localStorage` and `sessionStorage`? How do they compare to cookies in terms of capacity and scope?
73. What event fires when localStorage changes in another tab? How can you use this for cross-tab communication?
74. How does the History API's `pushState` differ from using hash-based routing? When would you choose each?
75. What events are involved in the Drag and Drop API? What does `e.preventDefault()` do in a `dragover` handler?
76. How does the Clipboard API work? Why does it require a user gesture for write operations?
77. What is the Page Visibility API, and what are practical use cases for it?
78. What is the difference between a Web Worker and a Service Worker? What can each access?
79. Describe the Service Worker lifecycle (install, waiting, activate, fetch).
80. Why do Service Workers require HTTPS (except localhost)?

### Accessibility (A11y)

81. What are the four WCAG POUR principles? Give an example of each.
82. What are the three WCAG conformance levels (A, AA, AAA)? Which should most sites target?
83. What is the first rule of ARIA? Why should you prefer native HTML elements over ARIA roles?
84. What is the difference between `aria-label`, `aria-labelledby`, and `aria-describedby`? When would you use each?
85. What does `aria-expanded` indicate, and how should it be used with expandable content?
86. What is the difference between `aria-live="polite"` and `aria-live="assertive"`? When should you use each?
87. What is the purpose of `aria-current`? What values can it take?
88. How do you implement a skip navigation link? What CSS is needed to show it on focus?
89. What is focus trapping, and why is it important for modal dialogs?
90. Why should you never use `*:focus { outline: none; }`? What should you use instead?
91. What is the minimum color contrast ratio for normal text (WCAG AA)? For large text?
92. How do you test a website for accessibility? What tools and manual tests should you use?

### SEO & Metadata

93. What is the most important SEO element in the `<head>`? What are best practices for writing it?
94. What is the ideal length for a meta description, and what should it include?
95. What is the Open Graph protocol, and what are the four required OG meta tags?
96. What are the recommended dimensions for an Open Graph image?
97. What is the difference between `summary` and `summary_large_image` Twitter Card types?
98. What is a canonical URL, and when should you use it?
99. What is hreflang, and what are the rules for implementing it correctly?
100. What is structured data (JSON-LD / Schema.org)? Give examples of common schema types (Article, Product, FAQ, BreadcrumbList).
101. What is the difference between `noindex` and `nofollow`? When would you use each?
102. What is the purpose of a sitemap.xml and robots.txt?

### Embedding & Iframes

103. What is the `sandbox` attribute on an iframe? What restrictions does it apply, and how do you selectively allow capabilities?
104. Why is the `title` attribute required on every iframe for accessibility?
105. How does `postMessage` work for cross-origin communication? Why must you always verify `event.origin`?
106. What is the padding-bottom technique for responsive iframes? How does it work?
107. What is the modern `aspect-ratio` CSS property alternative for responsive iframes?
108. What is the difference between `<object>` and `<embed>`? Which supports fallback content?
109. How do you lazy-load iframes using native `loading="lazy"` and the Intersection Observer API?
110. What performance considerations should you keep in mind when using iframes?

### Performance Optimization

111. What is the Critical Rendering Path? What are the steps from HTML to pixels?
112. What is the difference between `async` and `defer` on script tags? When would you use each?
113. What is the difference between `preload`, `prefetch`, `preconnect`, and `dns-prefetch`? When would you use each?
114. What are the three Core Web Vitals (LCP, FID, CLS)? What are the target thresholds for each?
115. How do you optimize LCP (Largest Contentful Paint)?
116. How do you optimize CLS (Cumulative Layout Shift)? What causes layout shifts?
117. What is `font-display` and what values does it support (swap, block, fallback, optional)?
118. How do you measure Core Web Vitals using the Performance Observer API?
119. What is a performance budget, and what metrics might it include?
120. How do you defer non-critical CSS using `rel="preload"` with an `onload` handler?

---

## 🔴 UPPER-MID TO SENIOR LEVEL

### Architecture & Design Patterns

121. How would you architect a large-scale web application's HTML structure for maintainability, accessibility, and performance?
122. What considerations go into choosing between client-side rendering (SPA), server-side rendering (SSR), and static site generation (SSG) from an HTML perspective?
123. How do you implement a design system using semantic HTML patterns that works across multiple teams?
124. What strategies do you use to ensure HTML quality across a large codebase with many developers?
125. How would you progressively enhance a page that must work without JavaScript while providing a rich experience with it?

### Advanced Accessibility

126. How do you implement an accessible custom component (e.g., a tab panel, accordion, or modal dialog) using ARIA?
127. What is the difference between `role="alert"` and `aria-live="assertive"`? When should you use each?
128. How do you handle focus management in a single-page application when navigating between routes?
129. What is the accessibility tree, and how do ARIA attributes affect it?
130. How do you test for accessibility with screen readers (VoiceOver, NVDA, JAWS)? What common issues do you look for?

### Advanced Forms & Validation

131. How do you implement a multi-step form (wizard) with validation at each step, preserving state on back navigation?
132. How do you implement real-time validation with custom error messages while maintaining accessibility?
133. What is the `Constraint Validation API`, and how do you use `setCustomValidity()` for custom validation?
134. How do you handle form autofill for credit cards, addresses, and passwords using the `autocomplete` attribute?
135. How would you design a form that gracefully handles network failures and prevents duplicate submissions?

### Advanced Performance

136. How do you implement code-splitting and lazy-loading for JavaScript in an HTML-first way?
137. What is the difference between `requestIdleCallback` and `requestAnimationFrame`? When would you use each for performance?
138. How do you implement a service worker caching strategy (Cache First, Network First, Stale While Revalidate)?
139. What is the Navigation and Resource Timing API, and how do you use it for real user monitoring (RUM)?
140. How do you optimize the Critical Rendering Path for a page with third-party scripts (analytics, ads, widgets)?

### Security

141. What is Content Security Policy (CSP), and how do you implement it via a `<meta>` tag or HTTP header?
142. What is the `sandbox` attribute's security model for iframes? What attacks does it prevent?
143. How do you prevent clickjacking? What's the difference between the `X-Frame-Options` header and CSP's `frame-ancestors`?
144. What is a CSRF token, and how is it implemented in HTML forms?
145. What is Subresource Integrity (SRI), and how do you use the `integrity` attribute on `<script>` and `<link>` tags?

### Emerging Standards & Future

146. What is the `<dialog>` element, and how does it compare to implementing modals with ARIA?
147. What is the `<search>` element (new in HTML 5.3)? How does it differ from using `<div role="search">`?
148. What is the `inert` attribute, and how does it help with focus management in modals and off-canvas navigation?
149. What is the `popover` API (the `popover` attribute and `<dialog>` integration)?
150. How do you use the `loading="lazy"` attribute for iframes and images, and what is the `fetchpriority` attribute?

---

## 💡 BONUS: Behavioral & Problem-Solving Questions

151. Describe a time you had to debug a cross-browser HTML rendering issue. What was the root cause and how did you fix it?
152. How would you approach migrating a legacy website that uses tables for layout to modern semantic HTML?
153. You're tasked with improving the Lighthouse performance score of a slow page from 40 to 90+. What steps do you take?
154. How do you handle the trade-off between shipping HTML quickly and ensuring it's fully accessible?
155. Describe your HTML review process. What do you look for when reviewing a pull request that includes HTML changes?
156. How would you explain the importance of semantic HTML to a junior developer who only uses `<div>` and `<span>`?
157. You need to embed a third-party widget that doesn't support accessibility. What do you do?
158. How do you approach making an existing single-page application work without JavaScript (progressive enhancement)?
159. What metrics do you track for HTML performance in production, and how do you set up alerting for regressions?
160. How would you design a component library's HTML API to be both flexible for developers and accessible for users?
