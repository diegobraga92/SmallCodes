/**
 * REACT STYLING
 * ==============
 * CSS Modules, Styled Components, Tailwind CSS, CSS-in-JS, theming
 */

import React, { useState, useContext, createContext } from 'react';

console.log("=".repeat(80));
console.log("REACT STYLING");
console.log("=".repeat(80));

// ============================================================================
// 1. INLINE STYLES
// ============================================================================

/*
   Inline styles use JavaScript objects with camelCase properties.
   Useful for dynamic styles, but limited (no pseudo-classes, media queries).
*/

function InlineStyles() {
    const [isHovered, setIsHovered] = useState(false);

    const buttonStyle = {
        backgroundColor: isHovered ? '#0056b3' : '#007bff',
        color: 'white',
        padding: '10px 20px',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px',
        transition: 'background-color 0.2s'
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial' }}>
            <button
                style={buttonStyle}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
            >
                Hover me
            </button>
        </div>
    );
}

// ============================================================================
// 2. CSS MODULES
// ============================================================================

/*
   CSS Modules scope styles locally by default.
   Each class name is hashed to avoid collisions.
   
   // Button.module.css
   // .button { background: blue; }
   // .primary { background: green; }
   
   import styles from './Button.module.css';
*/

// function Button({ variant = 'default', children }) {
//     return (
//         <button
//             className={`${styles.button} ${variant === 'primary' ? styles.primary : ''}`}
//         >
//             {children}
//         </button>
//     );
// }

// Multiple classes with classnames library
// import cn from 'classnames';
//
// function Alert({ type, show }) {
//     return (
//         <div className={cn(styles.alert, styles[type], { [styles.hidden]: !show })}>
//             Alert message
//         </div>
//     );
// }

// ============================================================================
// 3. STYLED COMPONENTS (CSS-in-JS)
// ============================================================================

/*
   Styled Components lets you write actual CSS in JavaScript.
   Styles are scoped to the component and support props-based styling.
   
   // install: npm install styled-components
   
   import styled from 'styled-components';
*/

// --- Basic styled component ---
// const Button = styled.button`
//     background-color: #007bff;
//     color: white;
//     padding: 10px 20px;
//     border: none;
//     border-radius: 4px;
//     font-size: 16px;
//     cursor: pointer;
//
//     &:hover {
//         background-color: #0056b3;
//     }
// `;

// --- With props ---
// const StyledButton = styled.button`
//     background-color: ${props => props.$primary ? '#007bff' : '#6c757d'};
//     color: white;
//     padding: ${props => props.$size === 'large' ? '15px 30px' : '10px 20px'};
//     border: none;
//     border-radius: 4px;
//     cursor: pointer;
//
//     &:disabled {
//         opacity: 0.5;
//         cursor: not-allowed;
//     }
// `;

// --- Extending styles ---
// const DangerButton = styled(StyledButton)`
//     background-color: #dc3545;
// `;

// --- Animations ---
// import styled, { keyframes } from 'styled-components';
//
// const fadeIn = keyframes`
//     from { opacity: 0; transform: translateY(10px); }
//     to { opacity: 1; transform: translateY(0); }
// `;
//
// const AnimatedDiv = styled.div`
//     animation: ${fadeIn} 0.3s ease-in;
// `;

// ============================================================================
// 4. TAILWIND CSS
// ============================================================================

/*
   Tailwind is a utility-first CSS framework.
   You compose styles using predefined class names.
   
   // install: npm install tailwindcss
   // configure: npx tailwindcss init
   
   // tailwind.config.js
   // module.exports = {
   //     content: ['./src/**/*.{js,jsx,ts,tsx}'],
   //     theme: { extend: {} },
   //     plugins: [],
   // }
*/

// function TailwindCard() {
//     return (
//         <div className="max-w-sm rounded overflow-hidden shadow-lg">
//             <img
//                 className="w-full h-48 object-cover"
//                 src="card-image.jpg"
//                 alt="Card"
//             />
//             <div className="px-6 py-4">
//                 <div className="font-bold text-xl mb-2">Card Title</div>
//                 <p className="text-gray-700 text-base">
//                     Card description text here.
//                 </p>
//             </div>
//             <div className="px-6 pt-4 pb-2">
//                 <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
//                     #tag
//                 </span>
//             </div>
//         </div>
//     );
// }

// --- Conditional classes with Tailwind ---
// function StatusBadge({ status }) {
//     const colors = {
//         active: 'bg-green-100 text-green-800',
//         pending: 'bg-yellow-100 text-yellow-800',
//         inactive: 'bg-red-100 text-red-800'
//     };
//
//     return (
//         <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
//             {status}
//         </span>
//     );
// }

// ============================================================================
// 5. THEMING WITH CONTEXT
// ============================================================================

/*
   Use React Context to provide a theme to all components.
   Works with any styling approach (CSS Modules, Styled Components, Tailwind).
*/

const ThemeContext = createContext({
    colors: {
        primary: '#007bff',
        secondary: '#6c757d',
        background: '#ffffff',
        text: '#333333'
    },
    spacing: {
        sm: '8px',
        md: '16px',
        lg: '24px'
    },
    borderRadius: '4px'
});

function ThemedCard({ title, children }) {
    const theme = useContext(ThemeContext);

    return (
        <div style={{
            backgroundColor: theme.colors.background,
            color: theme.colors.text,
            padding: theme.spacing.lg,
            borderRadius: theme.borderRadius,
            border: `1px solid ${theme.colors.secondary}`
        }}>
            <h2 style={{ color: theme.colors.primary }}>{title}</h2>
            {children}
        </div>
    );
}

function ThemedApp() {
    const customTheme = {
        colors: {
            primary: '#6610f2',
            secondary: '#20c997',
            background: '#f8f9fa',
            text: '#212529'
        },
        spacing: { sm: '8px', md: '16px', lg: '24px' },
        borderRadius: '8px'
    };

    return (
        <ThemeContext.Provider value={customTheme}>
            <ThemedCard title="Themed Card">
                <p>This card uses theme values from Context.</p>
            </ThemedCard>
        </ThemeContext.Provider>
    );
}

// ============================================================================
// 6. COMPONENT LIBRARIES
// ============================================================================

/*
   Pre-built component libraries provide consistent, accessible UI components.
   
   Material UI (MUI):
   // install: npm install @mui/material @emotion/react @emotion/styled
   // import Button from '@mui/material/Button';
   // import { ThemeProvider, createTheme } from '@mui/material/styles';
   
   Chakra UI:
   // install: npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion
   // import { Button, ChakraProvider } from '@chakra-ui/react';
   
   Ant Design:
   // install: npm install antd
   // import { Button, ConfigProvider } from 'antd';
*/

// --- MUI example ---
// import { ThemeProvider, createTheme } from '@mui/material/styles';
// import Button from '@mui/material/Button';
//
// const theme = createTheme({
//     palette: {
//         primary: { main: '#1976d2' },
//         secondary: { main: '#dc004e' }
//     }
// });
//
// function MUIApp() {
//     return (
//         <ThemeProvider theme={theme}>
//             <Button variant="contained" color="primary">
//                 MUI Button
//             </Button>
//         </ThemeProvider>
//     );
// }

// ============================================================================
// 7. BEST PRACTICES
// ============================================================================

/*
   1. Choose one approach and be consistent (don't mix inline + modules + CSS-in-JS)
   2. CSS Modules: good for team projects, no runtime overhead
   3. Styled Components: good for dynamic styles, component-scoped
   4. Tailwind: fast prototyping, consistent design system
   5. Use CSS variables for theming (works with any approach)
   6. Extract repeated style patterns into reusable components
   7. Use responsive design patterns (media queries, container queries)
   8. Consider bundle size when adding CSS-in-JS libraries
   9. Use CSS custom properties for runtime theme switching
   10. Test for accessibility (contrast, focus states, reduced motion)
*/

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Inline styles for dynamic values, limited capabilities");
console.log("2. CSS Modules: scoped styles, zero runtime cost");
console.log("3. Styled Components: CSS-in-JS with props-based styling");
console.log("4. Tailwind: utility-first, fast prototyping");
console.log("5. Context API for theming across approaches");
console.log("6. Component libraries (MUI, Chakra) for rapid development");
console.log("7. Choose one approach and stay consistent");
console.log("=".repeat(80));

export default InlineStyles;

