# CSS Interview Questions (Junior to Mid-Level)

Based on the CSS Refreshers series — covering topics from fundamentals through responsive design, layout, and modern CSS features.

---

## 🟢 JUNIOR LEVEL (Fundamentals)

### CSS Basics & Syntax

1. **What are the three ways to include CSS in an HTML document? When would you use each?**

   *Key points: Inline (style attribute) for single-element overrides; Internal (<style> in <head>) for single-page styles; External (.css file via <link>) for multi-page consistency and caching.*

2. **Explain the structure of a CSS rule. What are the parts of a declaration block?**

   *Key points: Selector targets HTML elements; declaration block `{ }` contains property:value pairs separated by semicolons. Example: `p { color: red; font-size: 16px; }`.*

3. **What is the difference between an element selector, a class selector, and an ID selector? When should you use each?**

   *Key points: Element (`p`) targets all instances of that tag; Class (`.name`) targets multiple elements with same class; ID (`#name`) targets a single unique element. Prefer classes for reusability, IDs for unique page sections or JavaScript hooks.*

4. **What does the universal selector (`*`) do, and why should it be used sparingly?**

   *Key points: Matches every element. Can cause performance issues on large pages and unexpected inheritance. Use for CSS resets or very broad defaults only.*

5. **Explain the difference between a descendant selector (`div span`) and a child selector (`div > span`).**

   *Key points: Descendant matches any nested span inside div (any depth); Child matches only direct children (immediate nesting level).*

6. **What is the difference between an adjacent sibling selector (`h2 + p`) and a general sibling selector (`h2 ~ p`)?**

   *Key points: Adjacent (`+`) matches the first sibling immediately after; General (`~`) matches all siblings after, not just the first.*

7. **What are the different CSS unit types? Explain the difference between absolute units (px, pt) and relative units (%, em, rem, vw, vh).**

   *Key points: Absolute: px (1/96th inch), pt (1/72 inch) — fixed size. Relative: % (parent-relative), em (parent font-size), rem (root font-size), vw (1% viewport width), vh (1% viewport height). Prefer relative units for responsive design.*

8. **When would you use `em` vs `rem` for font sizing? What are the practical implications of each?**

   *Key points: `em` compounds with nesting (relative to parent); `rem` is always relative to root (`<html>`) font-size. Use `rem` for predictable sizing, `em` when you want sizing to scale with a component's own font-size.*

9. **What is the `currentColor` keyword and when is it useful?**

   *Key points: Represents the computed `color` value of the element. Useful for matching borders, shadows, or SVGs to text color without repeating the color value.*

10. **What are the benefits of using shorthand properties like `margin`, `padding`, `border`, and `background`?**

    *Key points: Less code, fewer chances for errors, easier maintenance. Order matters (top, right, bottom, left for margin/padding).*

### Box Model

11. **Explain the four components of the CSS box model from inside to outside.**

    *Key points: Content → Padding → Border → Margin. Content holds actual content; Padding clears space inside border; Border surrounds padding; Margin creates space outside border.*

12. **What is the difference between `padding` and `margin`? When would you use each?**

    *Key points: Padding is inside the border (affects element's background area); Margin is outside the border (creates space between elements). Use padding for internal spacing, margin for external spacing between elements.*

13. **What is margin collapsing? Give an example of when it occurs and how to prevent it.**

    *Key points: Adjacent vertical margins collapse into the larger one. Example: two `<p>` elements with `margin: 20px` have 20px gap, not 40px. Prevent with `overflow: hidden`, borders, padding, or flexbox/grid.*

14. **What is the difference between `box-sizing: content-box` and `box-sizing: border-box`? Why is `border-box` generally recommended?**

    *Key points: `content-box`: width/height = content only (padding/border add to total). `border-box`: width/height includes content + padding + border. `border-box` makes sizing predictable and easier.*

15. **If an element has `width: 300px`, `padding: 20px`, and `border: 1px solid`, what is the total rendered width with `content-box` vs `border-box`?**

    *Key points: `content-box`: 300 + 40 + 2 = 342px. `border-box`: 300px (content shrinks to 258px).*

16. **Explain the difference between `display: block`, `display: inline`, and `display: inline-block`. Which properties does each respect?**

    *Key points: Block: full width, respects width/height, starts new line. Inline: content width, no width/height, flows inline. Inline-block: inline flow but respects width/height and margin/padding.*

17. **Why doesn't `width` and `height` work on inline elements? How do you work around this?**

    *Key points: Inline elements flow with text — width/height would break text flow. Use `display: inline-block` or `display: block` to enable sizing.*

18. **What is the difference between `display: none` and `visibility: hidden`?**

    *Key points: `display: none` removes element from layout (not rendered, no space). `visibility: hidden` hides visually but preserves space in layout.*

19. **What does `overflow: hidden` do? How is it different from `overflow: scroll` and `overflow: auto`?**

    *Key points: `hidden` clips overflowing content. `scroll` always shows scrollbars. `auto` shows scrollbars only when content overflows.*

20. **How do you horizontally center a block element using `margin`?**

    *Key points: Set `margin: 0 auto` on the element. Requires a defined width. Works only for horizontal centering of block elements.*

### Typography

21. **What is the purpose of providing fallback fonts in the `font-family` property?**

    *Key points: Ensures text renders even if the primary font fails to load. Browser tries each font in order until one is available. Always end with a generic family (serif, sans-serif).*

22. **What is the difference between `serif` and `sans-serif` fonts? When would you choose one over the other?**

    *Key points: Serif has decorative strokes (feet) — traditional, formal, better for print. Sans-serif has clean lines — modern, better for screen readability at small sizes.*

23. **Why is it recommended to use a unitless `line-height` value? What does `line-height: 1.5` mean?**

    *Key points: Unitless value is relative to the element's font-size (1.5 = 1.5× font-size). Avoids inheritance issues where a fixed unit would compound incorrectly in nested elements.*

24. **What is the difference between `font-weight: bold` and `font-weight: 700`? When would you use numeric values?**

    *Key points: `bold` = 700. Numeric values (100-900) give finer control when the font supports multiple weights (e.g., 300 light, 500 medium, 900 black).*

25. **How do you create a text truncation effect that shows an ellipsis (`...`) when text overflows?**

    *Key points: `overflow: hidden; white-space: nowrap; text-overflow: ellipsis;`. Requires a defined width and works only on single-line text.*

26. **What is the `@font-face` rule and how do you use it to load custom fonts?**

    *Key points: Defines custom fonts by specifying `font-family` name and `src: url()` to font files. Supports multiple formats (woff2, woff, ttf) for browser compatibility.*

27. **What does `font-display: swap` do and why is it important for web font loading?**

    *Key points: Shows text immediately with fallback font, then swaps to custom font when loaded. Prevents invisible text (FOIT) and improves perceived performance.*

28. **What is the difference between `text-transform: uppercase` and `text-transform: capitalize`?**

    *Key points: `uppercase` converts all letters to uppercase. `capitalize` capitalizes the first letter of each word.*

29. **How do you remove the default underline from links? How do you add it back only on hover?**

    *Key points: `text-decoration: none` removes underline. `a:hover { text-decoration: underline }` adds it back on hover.*

30. **What is the `font` shorthand and what is the minimum required information?**

    *Key points: `font: style variant weight size/line-height family`. Minimum: `font: 16px sans-serif` (size and family required).*

### Colors & Backgrounds

31. **What are the different ways to specify colors in CSS? Compare hex, RGB, RGBA, HSL, and HSLA.**

    *Key points: Hex (#ff0000) — 6-digit; RGB (255,0,0) — decimal values; RGBA adds alpha transparency; HSL (0, 100%, 50%) — hue, saturation, lightness; HSLA adds alpha. HSL is most intuitive for adjusting shades.*

32. **What is the difference between using `opacity: 0.5` and `background: rgba(0, 0, 0, 0.5)`?**

    *Key points: `opacity` affects the entire element (including children). `rgba` only affects the background color, leaving children fully opaque.*

33. **How do you set a background image that covers the entire element without stretching?**

    *Key points: `background-size: cover` scales the image to cover the element while maintaining aspect ratio. May crop parts of the image.*

34. **What is the difference between `background-size: cover` and `background-size: contain`?**

    *Key points: `cover` fills entire element (may crop). `contain` fits entire image within element (may leave empty space).*

35. **How do you create a linear gradient? How do you control the direction and color stops?**

    *Key points: `background: linear-gradient(direction, color1, color2)`. Direction: `to right`, `45deg`, etc. Color stops: `red 20%, blue 80%` controls where colors transition.*

36. **What is the difference between a linear gradient and a radial gradient?**

    *Key points: Linear gradient transitions along a straight line. Radial gradient radiates from a center point outward in a circular/elliptical shape.*

37. **How do you use `background-clip: text` to create gradient text?**

    *Key points: Set gradient as background, `background-clip: text`, `-webkit-text-fill-color: transparent`. Text shows the gradient through letter shapes.*

38. **What is the `background` shorthand and what properties does it include?**

    *Key points: `background: color image repeat position/size attachment clip origin`. Order is flexible but size must follow position with `/`.*

39. **How do you create a hard stop gradient (no blending between colors)?**

    *Key points: Set adjacent color stops at the same position: `linear-gradient(red 50%, blue 50%)`. No transition zone between colors.*

40. **What is a conic gradient and when would you use one?**

    *Key points: Gradient that rotates around a center point (like a color wheel). Used for pie charts, color wheels, and circular progress indicators.*

### Display & Positioning

41. **Explain the five values of the `position` property: `static`, `relative`, `absolute`, `fixed`, and `sticky`.**

    *Key points: `static` — default, normal flow. `relative` — offset from normal position. `absolute` — positioned relative to nearest positioned ancestor. `fixed` — relative to viewport. `sticky` — toggles between relative and fixed based on scroll.*

42. **What does `position: relative` do? How does it differ from `position: static`?**

    *Key points: `relative` offsets element from its normal position using top/left/right/bottom. Unlike `static`, it creates a positioning context for absolute children.*

43. **When using `position: absolute`, what is the element positioned relative to?**

    *Key points: The nearest ancestor with a `position` value other than `static`. If none exists, it positions relative to the `<html>` element.*

44. **How do you create a full-cover overlay using absolute positioning?**

    *Key points: `position: absolute; top: 0; left: 0; width: 100%; height: 100%;` on the overlay element. Parent needs `position: relative`.*

45. **How do you center an absolutely positioned element using `transform: translate()`?**

    *Key points: `top: 50%; left: 50%; transform: translate(-50%, -50%);`. Centers regardless of element's own dimensions.*

46. **What is `position: sticky` and how does it work? What is required for it to function?**

    *Key points: Element scrolls normally until it reaches a threshold (top/left), then sticks. Requires a defined `top`, `left`, etc. value and a scrollable parent with defined overflow.*

47. **What is a stacking context? What properties create a new stacking context?**

    *Key points: A 3D conceptual space where elements stack in z-order. Created by: `position` + `z-index`, `opacity < 1`, `transform`, `filter`, `isolation: isolate`, etc.*

48. **How does `z-index` work? Why doesn't `z-index` work on elements with `position: static`?**

    *Key points: `z-index` controls stacking order of positioned elements. Static elements ignore `z-index` because they're in normal flow. Only works on `relative`, `absolute`, `fixed`, or `sticky` elements.*

49. **What is the `float` property used for in modern CSS? When is it still appropriate to use?**

    *Key points: Originally for text wrapping around images. Modern use: wrapping text around floated elements. For layouts, use flexbox or grid instead.*

50. **What is the clearfix hack and why was it needed? What is the modern alternative?**

    *Key points: Clearfix prevented container collapse when all children were floated. Modern alternative: `display: flow-root` on the parent, which creates a new block formatting context.*

### Cascade, Specificity & Inheritance

51. **Explain how the CSS cascade determines which rule wins when multiple rules target the same element.**

    *Key points: Priority order: 1) Origin & importance (user `!important` > author `!important` > author normal > user agent), 2) Specificity, 3) Source order (last wins).*

52. **How is specificity calculated? Walk through the four-part calculation with examples.**

    *Key points: (inline, IDs, classes/pseudo-classes/attributes, elements/pseudo-elements). Example: `#nav .item a` = (0,1,1,1). `style="color: red"` = (1,0,0,0).*

53. **Which selector has higher specificity: a class selector (`.text`) or an element selector (`p`)? What about an ID selector (`#unique`)?**

    *Key points: Class (0,0,1,0) beats element (0,0,0,1). ID (0,1,0,0) beats class. Inline styles beat IDs.*

54. **What is `!important` and why should it be used sparingly? What are better alternatives?**

    *Key points: `!important` overrides all specificity. Creates maintenance nightmares. Better alternatives: increase specificity, use more specific selectors, or restructure CSS.*

55. **Which CSS properties are inherited by default? Which are not? Give examples of each.**

    *Key points: Inherited: `color`, `font-family`, `font-size`, `line-height`, `text-align`. Not inherited: `margin`, `padding`, `border`, `width`, `height`, `background`.*

56. **What do the keywords `inherit`, `initial`, `unset`, and `revert` do?**

    *Key points: `inherit` forces inheritance. `initial` resets to CSS spec default. `unset` acts as `inherit` for inherited properties, `initial` otherwise. `revert` resets to browser's default style.*

57. **What does `all: unset` do and when would you use it?**

    *Key points: Resets all properties on an element to their initial/inherited values. Useful for resetting third-party widget styles to a clean slate.*

58. **What are `@layer` cascade layers and how do they help manage specificity?**

    *Key points: Layers let you control the order of precedence between groups of styles. Styles in later layers override earlier ones regardless of specificity. Helps organize large stylesheets.*

59. **What is the BEM naming convention and how does it help keep specificity flat?**

    *Key points: Block__Element--Modifier naming (e.g., `card__title--large`). Uses only class selectors (no nesting), keeping specificity consistently at (0,0,1,0).*

60. **What is the difference between `:is()` and `:where()` in terms of specificity?**

    *Key points: `:is()` takes the specificity of its most specific argument. `:where()` always has zero specificity. Use `:where()` when you want easy overrides.*

---

## 🟡 MID-LEVEL (Intermediate)

### Flexbox

61. **What is the difference between `display: flex` and `display: inline-flex`?**

    *Key points: `flex` creates a block-level flex container. `inline-flex` creates an inline-level flex container (only takes content width).*

62. **Explain the main axis and cross axis in flexbox. How does `flex-direction` affect them?**

    *Key points: Main axis = direction of `flex-direction` (row = horizontal, column = vertical). Cross axis is perpendicular. `justify-content` aligns on main axis, `align-items` on cross axis.*

63. **What is the difference between `justify-content` and `align-items`? Which axis does each work on?**

    *Key points: `justify-content` aligns items along the main axis (spacing). `align-items` aligns items along the cross axis (stretch/center).*

64. **What does `flex-wrap: wrap` do? How is it different from the default `nowrap`?**

    *Key points: `wrap` allows items to flow to the next line when they exceed container width. `nowrap` forces all items onto one line (may shrink them).*

65. **What is the difference between `align-items` and `align-content`? When does `align-content` actually work?**

    *Key points: `align-items` aligns single-line items on cross axis. `align-content` distributes space between multiple lines (rows). Only works when `flex-wrap: wrap` and there are multiple lines.*

66. **Explain the `flex` shorthand. What do `flex: 1`, `flex: none`, and `flex: auto` mean?**

    *Key points: `flex: grow shrink basis`. `flex: 1` = `1 1 0` (grow equally). `flex: none` = `0 0 auto` (fixed size). `flex: auto` = `1 1 auto` (grow based on content size).*

67. **What is the difference between `flex-grow`, `flex-shrink`, and `flex-basis`?**

    *Key points: `flex-grow` — how much item grows relative to others. `flex-shrink` — how much item shrinks when space is tight. `flex-basis` — initial size before growing/shrinking.*

68. **How do you create equal-width columns using flexbox?**

    *Key points: Set `flex: 1` on each child item. All items grow equally to fill the container width.*

69. **How do you create a sticky footer using flexbox?**

    *Key points: Set `display: flex; flex-direction: column; min-height: 100vh` on body. Set `flex: 1` on main content. Footer stays at bottom when content is short.*

70. **What is the `gap` property in flexbox and how is it better than using margins?**

    *Key points: `gap` creates consistent spacing between items without affecting outer edges. Avoids margin collapsing and the "last-child margin" problem.*

71. **How does the `order` property work in flexbox? What are the accessibility concerns with using it?**

    *Key points: `order` changes visual order without changing DOM order. Accessibility concern: screen readers follow DOM order, not visual order, causing disconnect.*

72. **How do you center an element both horizontally and vertically using flexbox?**

    *Key points: On parent: `display: flex; justify-content: center; align-items: center;`. Works for single or multiple items.*

### CSS Grid

73. **What is the difference between flexbox and CSS Grid? When would you choose one over the other?**

    *Key points: Flexbox is one-dimensional (row OR column). Grid is two-dimensional (rows AND columns). Use flexbox for linear layouts, grid for complex 2D layouts.*

74. **What are `fr` units in CSS Grid and how do they differ from percentages?**

    *Key points: `fr` distributes available space after fixed-size tracks. Unlike %, `fr` accounts for `gap` and doesn't cause overflow with combined fixed + flexible tracks.*

75. **How does `grid-template-columns: repeat(3, 1fr)` work?**

    *Key points: Creates 3 equal-width columns. `repeat(3, 1fr)` is shorthand for `1fr 1fr 1fr`. Each column gets equal share of available space.*

76. **What is the difference between `grid-template-columns: repeat(auto-fill, minmax(250px, 1fr))` and `repeat(auto-fit, minmax(250px, 1fr))`?**

    *Key points: `auto-fill` keeps empty tracks (preserves column structure). `auto-fit` collapses empty tracks to 0, allowing items to stretch. Use `auto-fit` for responsive layouts without empty space.*

77. **How do you place an item on a specific grid line? Explain `grid-column` and `grid-row`.**

    *Key points: `grid-column: 1 / 3` spans from line 1 to line 3. `grid-row: 2 / 4` spans rows 2-4. Can use `span N` instead of end line: `grid-column: 1 / span 2`.*

78. **What is `grid-template-areas` and how do you use it to create a page layout?**

    *Key points: Define named areas with strings: `"header header" "sidebar main" "footer footer"`. Assign items with `grid-area: header`. Creates visual, easy-to-read layouts.*

79. **How do you create a responsive grid that automatically adjusts columns without media queries?**

    *Key points: Use `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))`. Columns automatically wrap as viewport shrinks.*

80. **What is the difference between `justify-items` and `justify-content` in CSS Grid?**

    *Key points: `justify-items` aligns items within their grid cells (stretch/start/center/end). `justify-content` aligns the entire grid within the container (when grid is smaller than container).*

81. **What does `place-items: center` do in a grid container?**

    *Key points: Shorthand for `align-items: center; justify-items: center`. Centers all items both horizontally and vertically within their grid cells.*

82. **What is `grid-auto-flow: dense` and when would you use it?**

    *Key points: Fills gaps in the grid by placing items out of DOM order. Useful for masonry-like layouts where items have different sizes. Can cause accessibility issues (visual ≠ DOM order).*

83. **What is `minmax()` and how does it create flexible track sizing?**

    *Key points: `minmax(min, max)` sets a track's minimum and maximum size. Example: `minmax(200px, 1fr)` — track is at least 200px but can grow to 1fr.*

84. **What is `subgrid` and what problem does it solve?**

    *Key points: `subgrid` lets a grid item inherit its parent's grid tracks for its own children. Solves alignment issues where nested grids need to align with the parent grid.*

### Responsive Design

85. **What is the mobile-first approach to responsive design? Why is it recommended?**

    *Key points: Start with mobile styles (base), then add `min-width` media queries for larger screens. Recommended because it's simpler, performs better on mobile, and forces prioritization of core content.*

86. **What is the difference between `min-width` and `max-width` media queries? Which is used in mobile-first design?**

    *Key points: `min-width` applies styles above a breakpoint (mobile-first). `max-width` applies styles below a breakpoint (desktop-first). Mobile-first uses `min-width`.*

87. **What are common breakpoints? Should you use device-specific or content-based breakpoints?**

    *Key points: Common: 480px, 768px, 1024px, 1200px. Use content-based breakpoints — add a breakpoint when the design breaks, not based on specific devices.*

88. **How does `clamp()` work? Give an example of fluid typography using `clamp()`.**

    *Key points: `clamp(min, preferred, max)`. Example: `font-size: clamp(1rem, 2.5vw, 2rem)` — font scales between 1rem and 2rem based on viewport.*

89. **How do you make images responsive so they never overflow their container?**

    *Key points: `max-width: 100%; height: auto;`. Image scales down but never exceeds its container width while maintaining aspect ratio.*

90. **What is the `srcset` attribute on `<img>` and how does it work with `sizes`?**

    *Key points: `srcset` provides multiple image files for different resolutions. `sizes` tells the browser how wide the image will display. Browser picks the best image based on viewport and device pixel ratio.*

91. **What does `object-fit: cover` do? How is it different from `object-fit: contain`?**

    *Key points: `cover` fills the element while cropping excess. `contain` fits the entire element within the box (may leave empty space). Both maintain aspect ratio.*

92. **How do you use `prefers-color-scheme` to implement dark mode?**

    *Key points: `@media (prefers-color-scheme: dark) { ... }` applies dark styles when user's OS is in dark mode. Combine with CSS custom properties for easy theming.*

93. **What is `prefers-reduced-motion` and why is it important for accessibility?**

    *Key points: `@media (prefers-reduced-motion: reduce)` detects users who prefer less animation. Important for vestibular disorders — should disable or reduce non-essential animations.*

94. **What are container queries (`@container`) and how are they different from media queries?**

    *Key points: Container queries respond to the parent container's size, not the viewport. Enable truly reusable components that adapt to their placement context.*

95. **How do you create a responsive layout pattern like "column drop" or "mostly fluid" using flexbox?**

    *Key points: Use `flex-wrap: wrap` with `flex-basis` or `min-width` on items. As container shrinks, items wrap to new lines. Combine with `flex-grow` for fluid behavior.*

### Transitions & Animations

96. **What is the difference between a CSS transition and a CSS animation? When would you use each?**

    *Key points: Transitions go from state A to B (triggered by state change). Animations can have multiple keyframes and run automatically. Use transitions for hover effects, animations for complex sequences.*

97. **What are the four transition sub-properties? Write the shorthand syntax.**

    *Key points: `transition-property`, `transition-duration`, `transition-timing-function`, `transition-delay`. Shorthand: `transition: all 0.3s ease 0s`.*

98. **What is the difference between `ease`, `linear`, `ease-in`, `ease-out`, and `ease-in-out` timing functions?**

    *Key points: `ease` — slow start/end (default). `linear` — constant speed. `ease-in` — slow start, fast end. `ease-out` — fast start, slow end. `ease-in-out` — slow start and end.*

99. **Why should you prefer animating `transform` and `opacity` over `width`, `height`, `top`, or `left`?**

    *Key points: `transform` and `opacity` are composited on the GPU — no layout or paint triggers. Animating layout properties triggers expensive reflows.*

100. **How do you create a staggered animation effect where items animate one after another?**

     *Key points: Use `animation-delay` with increasing values: `nth-child(1) { animation-delay: 0s; } nth-child(2) { animation-delay: 0.1s; }` etc.*

101. **What is `@keyframes` and how do you define multi-step animations?**

     *Key points: `@keyframes name { 0% { ... } 50% { ... } 100% { ... } }`. Defines animation stages at percentage points. Applied with `animation: name duration`.*

102. **What does `animation-fill-mode: forwards` do? Why is it often used with fade-in animations?**

     *Key points: Retains the final keyframe state after animation ends. Used with fade-in so element stays visible instead of snapping back to hidden.*

103. **What is the difference between `animation-direction: normal`, `reverse`, `alternate`, and `alternate-reverse`?**

     *Key points: `normal` — 0% to 100%. `reverse` — 100% to 0%. `alternate` — normal then reverse. `alternate-reverse` — reverse then normal.*

104. **How do you create an infinite spinning animation?**

     *Key points: `@keyframes spin { to { transform: rotate(360deg); } }` with `animation: spin 1s linear infinite`.*

105. **How do you pause and resume a CSS animation?**

     *Key points: Set `animation-play-state: paused` (e.g., on hover). Toggle to `running` to resume. Can also use `animation-delay` with negative values.*

### Transforms

106. **What does the `transform` property do? How is it different from using `top`/`left` for positioning?**

     *Key points: `transform` modifies element appearance (rotate, scale, translate, skew) without affecting layout. `top`/`left` changes layout position and triggers reflow.*

107. **What is the centering trick using `transform: translate(-50%, -50%)` and why does it work?**

     *Key points: Combined with `top: 50%; left: 50%`, it centers an element regardless of its dimensions. `translate(-50%, -50%)` moves the element back by half its own width/height.*

108. **Why does the order of transform functions matter? Give an example.**

     *Key points: Transforms are applied right-to-left. `translate() rotate()` moves then rotates. `rotate() translate()` rotates the axis then moves — different result.*

109. **What is `transform-origin` and how does it affect rotation?**

     *Key points: Sets the pivot point for transforms. Default is `center`. `transform-origin: top left` rotates around the top-left corner instead of center.*

110. **What is the difference between 2D and 3D transforms? What is required to see 3D effects?**

     *Key points: 3D adds Z-axis (translateZ, rotateX, rotateY, perspective). Requires `perspective` on parent and `transform-style: preserve-3d` on the element.*

111. **What does `perspective` do in 3D transforms? How does a smaller vs larger value affect the visual result?**

     *Key points: `perspective` defines the distance from the viewer. Smaller values (100px) create dramatic 3D effect. Larger values (1000px) create subtle depth.*

112. **How do you create a card flip effect using `rotateY()` and `backface-visibility`?**

     *Key points: Two sides positioned absolutely. Front has `backface-visibility: hidden`. Back has `rotateY(180deg)`. On hover, container rotates 180deg to show back.*

113. **What does `transform-style: preserve-3d` do and when is it needed?**

     *Key points: Allows child elements to maintain their 3D position relative to each other. Needed for nested 3D transforms (like card flip). Default `flat` flattens children.*

114. **How do you create a hover lift effect using `translateY()` and `scale()`?**

     *Key points: `transform: translateY(-5px) scale(1.05)` on hover. Combine with `transition: transform 0.2s` for smooth effect.*

115. **Why is `transform` considered a performant property for animations?**

     *Key points: Composited on GPU, no layout or paint triggers. The browser only composites layers, making it 60fps-friendly.*

### Custom Properties (CSS Variables)

116. **How do you define and use a CSS custom property? What is the `var()` syntax?**

     *Key points: Define: `--color-primary: blue;`. Use: `color: var(--color-primary);`. Names are case-sensitive and prefixed with `--`.*

117. **What is the scope of a custom property defined on `:root` vs on a specific element?**

     *Key points: `:root` makes it globally available (entire document). On a specific element, it's only available to that element and its descendants.*

118. **How do you provide a fallback value in `var()`?**

     *Key points: `var(--custom, fallback-value)`. If `--custom` is not defined, `fallback-value` is used. Example: `var(--color, blue)`.*

119. **How do you implement dark mode theming using custom properties?**

     *Key points: Define colors as custom properties on `:root`. Override them inside `@media (prefers-color-scheme: dark) { :root { ... } }`. All usages update automatically.*

120. **Can custom properties be used inside `calc()`? Give an example.**

     *Key points: Yes. `width: calc(var(--spacing) * 2)`. Custom properties can hold any value type, including numbers for calculations.*

121. **How do you override custom properties in media queries?**

     *Key points: Re-declare the property inside the media query block. The new value applies only within that breakpoint. No need to change every usage.*

122. **What is the `@property` rule and what does it add beyond regular custom properties?**

     *Key points: `@property` defines typed custom properties with `syntax`, `inherits`, and `initial-value`. Enables animation of custom properties and type validation.*

123. **How do you create a design token system using custom properties?**

     *Key points: Define tokens as custom properties on `:root`: colors, spacing, typography, shadows. Reference them throughout CSS. Change tokens in one place to update entire design.*

124. **What happens if you reference a custom property that doesn't exist (without a fallback)?**

     *Key points: The property becomes invalid. The browser ignores the declaration and may use the inherited value or initial value. No error is thrown.*

125. **How do custom properties enable component-level style encapsulation?**

     *Key points: Define component-specific custom properties on the component's root element. Consumers override them to customize without knowing internal implementation.*

### Pseudo-Classes & Pseudo-Elements

126. **What is the difference between a pseudo-class (`:`) and a pseudo-element (`::`)? Give examples of each.**

     *Key points: Pseudo-class (`:hover`, `:focus`) selects element states. Pseudo-element (`::before`, `::after`) creates virtual elements. Pseudo-elements use `::` (CSS3), pseudo-classes use `:`.*

127. **What is the difference between `:focus` and `:focus-visible`? Why is `:focus-visible` better for accessibility?**

     *Key points: `:focus` applies on any focus. `:focus-visible` applies only when browser determines focus should be visible (keyboard navigation). Prevents ugly focus rings on mouse clicks while maintaining keyboard accessibility.*

128. **What does `:focus-within` do and when would you use it?**

     *Key points: Applies to an element when it or any of its descendants has focus. Useful for highlighting form sections or containers when an input inside is focused.*

129. **How does `:nth-child(2n+1)` work? Explain the `an+b` formula syntax.**

     *Key points: `an+b` selects every nth element starting from b. `2n+1` = odd elements (1, 3, 5...). `3n+2` = every 3rd starting from 2nd (2, 5, 8...).*

130. **What is the difference between `:nth-child()` and `:nth-of-type()`?**

     *Key points: `:nth-child` counts all siblings regardless of type. `:nth-of-type` counts only siblings of the same element type. Example: `p:nth-of-type(2)` selects the second `<p>`, ignoring other elements.*

131. **What does `:not()` do? How can you select all children except the last one?**

     *Key points: `:not(selector)` excludes matching elements. All children except last: `.container > *:not(:last-child)`.*

132. **What is `:has()` and why is it considered a "parent selector"? Give an example.**

     *Key points: `:has()` selects an element based on its descendants. Example: `div:has(img)` selects divs that contain an image. Enables parent selection, previously impossible in CSS.*

133. **What is the `::before` and `::after` pseudo-element? What is the `content` property and why is it required?**

     *Key points: `::before`/`::after` insert content before/after an element's content. `content` property is required — without it, the pseudo-element won't render. Can be empty string `""`.*

134. **How do you create a tooltip using `::after` and `attr()`?**

     *Key points: `content: attr(data-tooltip)` reads a custom attribute. Position `::after` absolutely relative to the element. Show on `:hover`. Example: `content: attr(data-tip)`.*

135. **What form-related pseudo-classes exist for validation styling (`:valid`, `:invalid`, `:required`, `:disabled`)?**

     *Key points: `:valid` — input passes validation. `:invalid` — input fails validation. `:required` — input has `required` attribute. `:disabled` — input is disabled. Use for real-time validation styling.*

136. **What does `::selection` do and how can you customize text selection appearance?**

     *Key points: Styles the portion of text selected by the user. Customize `background`, `color`, `text-shadow`. Example: `::selection { background: yellow; color: black; }`.*

137. **How do you style the placeholder text of an input using `::placeholder`?**

     *Key points: `input::placeholder { color: gray; }`. Only a subset of properties work: `color`, `font`, `opacity`, `text-decoration`.*

138. **What does `::marker` allow you to style?**

     *Key points: Styles the bullet/number of list items (`<li>`). Properties: `color`, `font-size`, `content` (to change the marker symbol).*

139. **How do you combine pseudo-classes and pseudo-elements? Give an example.**

     *Key points: Chain them: `.card:hover::before { ... }`. The pseudo-class comes first, then the pseudo-element. Example: styling a tooltip that appears on hover.*

140. **What is the difference between `:first-child` and `:first-of-type`?**

     *Key points: `:first-child` targets the first child element regardless of type. `:first-of-type` targets the first element of its type among siblings. `p:first-of-type` selects the first `<p>`, even if preceded by other elements.*

### Advanced Selectors

141. **What are attribute selectors and how do you use `[attr^="value"]`, `[attr$="value"]`, and `[attr*="value"]`?**

     *Key points: `^=` starts with, `$=` ends with, `*=` contains. Examples: `[href^="https"]` — secure links; `[src$=".jpg"]` — JPEG images; `[class*="btn"]` — elements with "btn" in class.*

142. **How would you style all external links that start with `https`?**

     *Key points: `a[href^="https"] { ... }`. Add an icon with `::after` and `content`. Exclude same-domain links by combining selectors.*

143. **How would you style all links to PDF files?**

     *Key points: `a[href$=".pdf"] { ... }`. Add a PDF icon using `::after`. Can also use `a[href*=".pdf"]` for URLs with query parameters.*

144. **What is the lobotomized owl selector (`* + *`) and what problem does it solve?**

     *Key points: Selects every element that follows another element. Creates consistent spacing between adjacent children without affecting the first child. Solves the "margin on first/last child" problem.*

145. **How do you use compound selectors (chaining) to target elements with multiple classes?**

     *Key points: `.class1.class2` targets elements with BOTH classes. No space between class selectors. Example: `.btn.primary` selects elements with both `btn` and `primary` classes.*

146. **What is the difference between `:is()` and a regular comma-separated selector list?**

     *Key points: `:is()` takes the specificity of its most specific argument. Comma-separated lists don't affect specificity. `:is()` also supports forgiving parsing (invalid selectors don't break the whole rule).*

147. **How do you select elements that are NOT the first child AND NOT the last child?**

     *Key points: `:not(:first-child):not(:last-child)`. Or use `:not(:first-child, :last-child)` with newer `:not()` syntax.*

148. **How do you select items 4 through 6 using `:nth-child()`?**

     *Key points: `:nth-child(n+4):nth-child(-n+6)`. First part selects from 4th onward, second part selects up to 6th. Intersection gives items 4, 5, 6.*

149. **How do you use `:has()` to style a form that contains invalid inputs?**

     *Key points: `form:has(:invalid) { border-color: red; }`. Styles the form container when any of its inputs are invalid. Previously required JavaScript.*

150. **What is the `[attr~="value"]` selector and how is it different from `[attr*="value"]`?**

     *Key points: `~=` matches whole words separated by spaces (like class list). `*=` matches substring anywhere. Example: `[class~="btn"]` matches `class="btn primary"` but not `class="btn-primary"`.*

---

## 💡 BONUS: Problem-Solving & Best Practices

151. **You have a layout with three columns that should stack vertically on mobile. Walk through how you would implement this using both flexbox and grid.**

     *Key points: Flexbox: `display: flex; gap: 1rem;` on container, `flex: 1` on items, `flex-wrap: wrap` with `min-width` for stacking. Grid: `grid-template-columns: repeat(3, 1fr)` on desktop, `grid-template-columns: 1fr` on mobile via media query.*

152. **A button has a hover effect that transitions its background color. The animation is janky. What could be the cause and how would you fix it?**

     *Key points: Cause: animating `background-color` triggers paint. Fix: use `transform` and `opacity` instead, or use `will-change: transform` and a pseudo-element for the background with opacity transition.*

153. **How would you implement a responsive card grid where cards are at least 280px wide and fill the available space?**

     *Key points: Grid: `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`. Flexbox: `display: flex; flex-wrap: wrap;` with `flex: 1 1 280px` on cards.*

154. **You need to add spacing between all children of a container except the last one. What are different ways to achieve this?**

     *Key points: 1) `gap` property (modern, best). 2) `* + * { margin-top: 1rem }` (lobotomized owl). 3) `:not(:last-child) { margin-right: 1rem }`. 4) `> * { margin-bottom: 1rem; } > *:last-child { margin-bottom: 0 }`.*

155. **How would you implement dark mode support in an existing stylesheet with minimal code changes?**

     *Key points: Define all colors as CSS custom properties on `:root`. Add `@media (prefers-color-scheme: dark) { :root { ... } }` overriding only the color values. No changes to component styles.*

156. **A third-party CSS library is overriding your styles. How would you fix this without using `!important`?**

     *Key points: Increase specificity (add ID or extra class). Use `@layer` to place your styles after the library. Use `:where()` to zero out library specificity. Restructure your selector chain.*

157. **How would you create a sticky header that stays at the top when scrolling, without using JavaScript?**

     *Key points: `position: sticky; top: 0; z-index: 100;` on the header. Works without JavaScript. Ensure no parent has `overflow: hidden` which breaks sticky positioning.*

158. **You have a form with validation. How would you show green borders on valid inputs and red borders on invalid inputs?**

     *Key points: `input:valid { border-color: green; } input:invalid { border-color: red; }`. Use `:focus:invalid` to only show red after user interaction. Add `:placeholder-shown` to avoid showing validation on empty fields.*

159. **How would you create a print stylesheet that hides navigation, shows URLs after links, and uses black text on white background?**

     *Key points: `@media print { nav { display: none; } a[href]::after { content: " (" attr(href) ")"; } body { color: black; background: white; } }`. Use `* { background: transparent !important; }` to save ink.*

160. **A colleague wrote `z-index: 9999` on an element and it's still not appearing on top. What could be the issue and how would you debug it?**

     *Key points: Issue: parent creates a new stacking context (via `opacity`, `transform`, `isolation`, etc.). The child's `z-index` only applies within that parent's stacking context. Debug: check DevTools for stacking contexts, look for `transform`, `opacity`, `isolation: isolate` on ancestors.*
