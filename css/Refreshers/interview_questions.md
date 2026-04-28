# CSS Interview Questions (Junior to Mid-Level)

Based on the CSS Refreshers series — covering topics from fundamentals through responsive design, layout, and modern CSS features.

---

## 🟢 JUNIOR LEVEL (Fundamentals)

### CSS Basics & Syntax

1. What are the three ways to include CSS in an HTML document? When would you use each?
2. Explain the structure of a CSS rule. What are the parts of a declaration block?
3. What is the difference between an element selector, a class selector, and an ID selector? When should you use each?
4. What does the universal selector (`*`) do, and why should it be used sparingly?
5. Explain the difference between a descendant selector (`div span`) and a child selector (`div > span`).
6. What is the difference between an adjacent sibling selector (`h2 + p`) and a general sibling selector (`h2 ~ p`)?
7. What are the different CSS unit types? Explain the difference between absolute units (px, pt) and relative units (%, em, rem, vw, vh).
8. When would you use `em` vs `rem` for font sizing? What are the practical implications of each?
9. What is the `currentColor` keyword and when is it useful?
10. What are the benefits of using shorthand properties like `margin`, `padding`, `border`, and `background`?

### Box Model

11. Explain the four components of the CSS box model from inside to outside.
12. What is the difference between `padding` and `margin`? When would you use each?
13. What is margin collapsing? Give an example of when it occurs and how to prevent it.
14. What is the difference between `box-sizing: content-box` and `box-sizing: border-box`? Why is `border-box` generally recommended?
15. If an element has `width: 300px`, `padding: 20px`, and `border: 1px solid`, what is the total rendered width with `content-box` vs `border-box`?
16. Explain the difference between `display: block`, `display: inline`, and `display: inline-block`. Which properties does each respect?
17. Why doesn't `width` and `height` work on inline elements? How do you work around this?
18. What is the difference between `display: none` and `visibility: hidden`?
19. What does `overflow: hidden` do? How is it different from `overflow: scroll` and `overflow: auto`?
20. How do you horizontally center a block element using `margin`?

### Typography

21. What is the purpose of providing fallback fonts in the `font-family` property?
22. What is the difference between `serif` and `sans-serif` fonts? When would you choose one over the other?
23. Why is it recommended to use a unitless `line-height` value? What does `line-height: 1.5` mean?
24. What is the difference between `font-weight: bold` and `font-weight: 700`? When would you use numeric values?
25. How do you create a text truncation effect that shows an ellipsis (`...`) when text overflows?
26. What is the `@font-face` rule and how do you use it to load custom fonts?
27. What does `font-display: swap` do and why is it important for web font loading?
28. What is the difference between `text-transform: uppercase` and `text-transform: capitalize`?
29. How do you remove the default underline from links? How do you add it back only on hover?
30. What is the `font` shorthand and what is the minimum required information?

### Colors & Backgrounds

31. What are the different ways to specify colors in CSS? Compare hex, RGB, RGBA, HSL, and HSLA.
32. What is the difference between using `opacity: 0.5` and `background: rgba(0, 0, 0, 0.5)`?
33. How do you set a background image that covers the entire element without stretching?
34. What is the difference between `background-size: cover` and `background-size: contain`?
35. How do you create a linear gradient? How do you control the direction and color stops?
36. What is the difference between a linear gradient and a radial gradient?
37. How do you use `background-clip: text` to create gradient text?
38. What is the `background` shorthand and what properties does it include?
39. How do you create a hard stop gradient (no blending between colors)?
40. What is a conic gradient and when would you use one?

### Display & Positioning

41. Explain the five values of the `position` property: `static`, `relative`, `absolute`, `fixed`, and `sticky`.
42. What does `position: relative` do? How does it differ from `position: static`?
43. When using `position: absolute`, what is the element positioned relative to?
44. How do you create a full-cover overlay using absolute positioning?
45. How do you center an absolutely positioned element using `transform: translate()`?
46. What is `position: sticky` and how does it work? What is required for it to function?
47. What is a stacking context? What properties create a new stacking context?
48. How does `z-index` work? Why doesn't `z-index` work on elements with `position: static`?
49. What is the `float` property used for in modern CSS? When is it still appropriate to use?
50. What is the clearfix hack and why was it needed? What is the modern alternative?

### Cascade, Specificity & Inheritance

51. Explain how the CSS cascade determines which rule wins when multiple rules target the same element.
52. How is specificity calculated? Walk through the four-part calculation with examples.
53. Which selector has higher specificity: a class selector (`.text`) or an element selector (`p`)? What about an ID selector (`#unique`)?
54. What is `!important` and why should it be used sparingly? What are better alternatives?
55. Which CSS properties are inherited by default? Which are not? Give examples of each.
56. What do the keywords `inherit`, `initial`, `unset`, and `revert` do?
57. What does `all: unset` do and when would you use it?
58. What are `@layer` cascade layers and how do they help manage specificity?
59. What is the BEM naming convention and how does it help keep specificity flat?
60. What is the difference between `:is()` and `:where()` in terms of specificity?

---

## 🟡 MID-LEVEL (Intermediate)

### Flexbox

61. What is the difference between `display: flex` and `display: inline-flex`?
62. Explain the main axis and cross axis in flexbox. How does `flex-direction` affect them?
63. What is the difference between `justify-content` and `align-items`? Which axis does each work on?
64. What does `flex-wrap: wrap` do? How is it different from the default `nowrap`?
65. What is the difference between `align-items` and `align-content`? When does `align-content` actually work?
66. Explain the `flex` shorthand. What do `flex: 1`, `flex: none`, and `flex: auto` mean?
67. What is the difference between `flex-grow`, `flex-shrink`, and `flex-basis`?
68. How do you create equal-width columns using flexbox?
69. How do you create a sticky footer using flexbox?
70. What is the `gap` property in flexbox and how is it better than using margins?
71. How does the `order` property work in flexbox? What are the accessibility concerns with using it?
72. How do you center an element both horizontally and vertically using flexbox?

### CSS Grid

73. What is the difference between flexbox and CSS Grid? When would you choose one over the other?
74. What are `fr` units in CSS Grid and how do they differ from percentages?
75. How does `grid-template-columns: repeat(3, 1fr)` work?
76. What is the difference between `grid-template-columns: repeat(auto-fill, minmax(250px, 1fr))` and `repeat(auto-fit, minmax(250px, 1fr))`?
77. How do you place an item on a specific grid line? Explain `grid-column` and `grid-row`.
78. What is `grid-template-areas` and how do you use it to create a page layout?
79. How do you create a responsive grid that automatically adjusts columns without media queries?
80. What is the difference between `justify-items` and `justify-content` in CSS Grid?
81. What does `place-items: center` do in a grid container?
82. What is `grid-auto-flow: dense` and when would you use it?
83. What is `minmax()` and how does it create flexible track sizing?
84. What is `subgrid` and what problem does it solve?

### Responsive Design

85. What is the mobile-first approach to responsive design? Why is it recommended?
86. What is the difference between `min-width` and `max-width` media queries? Which is used in mobile-first design?
87. What are common breakpoints? Should you use device-specific or content-based breakpoints?
88. How does `clamp()` work? Give an example of fluid typography using `clamp()`.
89. How do you make images responsive so they never overflow their container?
90. What is the `srcset` attribute on `<img>` and how does it work with `sizes`?
91. What does `object-fit: cover` do? How is it different from `object-fit: contain`?
92. How do you use `prefers-color-scheme` to implement dark mode?
93. What is `prefers-reduced-motion` and why is it important for accessibility?
94. What are container queries (`@container`) and how are they different from media queries?
95. How do you create a responsive layout pattern like "column drop" or "mostly fluid" using flexbox?

### Transitions & Animations

96. What is the difference between a CSS transition and a CSS animation? When would you use each?
97. What are the four transition sub-properties? Write the shorthand syntax.
98. What is the difference between `ease`, `linear`, `ease-in`, `ease-out`, and `ease-in-out` timing functions?
99. Why should you prefer animating `transform` and `opacity` over `width`, `height`, `top`, or `left`?
100. How do you create a staggered animation effect where items animate one after another?
101. What is `@keyframes` and how do you define multi-step animations?
102. What does `animation-fill-mode: forwards` do? Why is it often used with fade-in animations?
103. What is the difference between `animation-direction: normal`, `reverse`, `alternate`, and `alternate-reverse`?
104. How do you create an infinite spinning animation?
105. How do you pause and resume a CSS animation?

### Transforms

106. What does the `transform` property do? How is it different from using `top`/`left` for positioning?
107. What is the centering trick using `transform: translate(-50%, -50%)` and why does it work?
108. Why does the order of transform functions matter? Give an example.
109. What is `transform-origin` and how does it affect rotation?
110. What is the difference between 2D and 3D transforms? What is required to see 3D effects?
111. What does `perspective` do in 3D transforms? How does a smaller vs larger value affect the visual result?
112. How do you create a card flip effect using `rotateY()` and `backface-visibility`?
113. What does `transform-style: preserve-3d` do and when is it needed?
114. How do you create a hover lift effect using `translateY()` and `scale()`?
115. Why is `transform` considered a performant property for animations?

### Custom Properties (CSS Variables)

116. How do you define and use a CSS custom property? What is the `var()` syntax?
117. What is the scope of a custom property defined on `:root` vs on a specific element?
118. How do you provide a fallback value in `var()`?
119. How do you implement dark mode theming using custom properties?
120. Can custom properties be used inside `calc()`? Give an example.
121. How do you override custom properties in media queries?
122. What is the `@property` rule and what does it add beyond regular custom properties?
123. How do you create a design token system using custom properties?
124. What happens if you reference a custom property that doesn't exist (without a fallback)?
125. How do custom properties enable component-level style encapsulation?

### Pseudo-Classes & Pseudo-Elements

126. What is the difference between a pseudo-class (`:`) and a pseudo-element (`::`)? Give examples of each.
127. What is the difference between `:focus` and `:focus-visible`? Why is `:focus-visible` better for accessibility?
128. What does `:focus-within` do and when would you use it?
129. How does `:nth-child(2n+1)` work? Explain the `an+b` formula syntax.
130. What is the difference between `:nth-child()` and `:nth-of-type()`?
131. What does `:not()` do? How can you select all children except the last one?
132. What is `:has()` and why is it considered a "parent selector"? Give an example.
133. What is the `::before` and `::after` pseudo-element? What is the `content` property and why is it required?
134. How do you create a tooltip using `::after` and `attr()`?
135. What form-related pseudo-classes exist for validation styling (`:valid`, `:invalid`, `:required`, `:disabled`)?
136. What does `::selection` do and how can you customize text selection appearance?
137. How do you style the placeholder text of an input using `::placeholder`?
138. What does `::marker` allow you to style?
139. How do you combine pseudo-classes and pseudo-elements? Give an example.
140. What is the difference between `:first-child` and `:first-of-type`?

### Advanced Selectors

141. What are attribute selectors and how do you use `[attr^="value"]`, `[attr$="value"]`, and `[attr*="value"]`?
142. How would you style all external links that start with `https`?
143. How would you style all links to PDF files?
144. What is the lobotomized owl selector (`* + *`) and what problem does it solve?
145. How do you use compound selectors (chaining) to target elements with multiple classes?
146. What is the difference between `:is()` and a regular comma-separated selector list?
147. How do you select elements that are NOT the first child AND NOT the last child?
148. How do you select items 4 through 6 using `:nth-child()`?
149. How do you use `:has()` to style a form that contains invalid inputs?
150. What is the `[attr~="value"]` selector and how is it different from `[attr*="value"]`?

---

## 💡 BONUS: Problem-Solving & Best Practices

151. You have a layout with three columns that should stack vertically on mobile. Walk through how you would implement this using both flexbox and grid.
152. A button has a hover effect that transitions its background color. The animation is janky. What could be the cause and how would you fix it?
153. How would you implement a responsive card grid where cards are at least 280px wide and fill the available space?
154. You need to add spacing between all children of a container except the last one. What are different ways to achieve this?
155. How would you implement dark mode support in an existing stylesheet with minimal code changes?
156. A third-party CSS library is overriding your styles. How would you fix this without using `!important`?
157. How would you create a sticky header that stays at the top when scrolling, without using JavaScript?
158. You have a form with validation. How would you show green borders on valid inputs and red borders on invalid inputs?
159. How would you create a print stylesheet that hides navigation, shows URLs after links, and uses black text on white background?
160. A colleague wrote `z-index: 9999` on an element and it's still not appearing on top. What could be the issue and how would you debug it?
