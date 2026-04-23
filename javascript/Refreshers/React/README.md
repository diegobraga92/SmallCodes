# React Refreshers

Comprehensive React guide from basics to advanced patterns.

## 📚 Topics Covered

### Fundamentals
- **00_jsx_basics.jsx** - JSX syntax, expressions, attributes
- **01_components.jsx** - Function components, props, composition
- **02_state_hooks.jsx** - useState, state management, updates
- **03_effect_hooks.jsx** - useEffect, lifecycle, cleanup
- **04_event_handling.jsx** - Events, synthetic events, form handling
- **05_conditional_rendering.jsx** - if/else, ternary, &&, switch

### Intermediate
- **06_lists_keys.jsx** - Rendering lists, key prop, array methods
- **07_forms.jsx** - Controlled components, form validation, submission
- **08_lifting_state.jsx** - State lifting, prop drilling, data flow
- **09_composition_children.jsx** - children prop, composition patterns
- **10_ref_hook.jsx** - useRef, DOM refs, focus management
- **11_context_api.jsx** - Context creation, Provider, Consumer, useContext
- **12_custom_hooks.jsx** - Creating reusable hooks, hook rules
- **13_reducer_hook.jsx** - useReducer, complex state, actions

### Advanced
- **14_memo_optimization.jsx** - useMemo, useCallback, React.memo
- **15_error_boundaries.jsx** - Error handling, fallback UI
- **16_portals.jsx** - ReactDOM.createPortal, modals, overlays
- **17_code_splitting.jsx** - React.lazy, Suspense, dynamic imports
- **18_routing.jsx** - React Router, navigation, params, guards
- **19_state_management.jsx** - Redux, Zustand, Recoil patterns
- **20_testing.jsx** - Jest, React Testing Library, test patterns
- **21_typescript_react.tsx** - TypeScript with React, types, props
- **22_server_components.jsx** - RSC patterns (if using Next.js)
- **23_advanced_patterns.jsx** - HOCs, Render Props, Compound Components

## 🎯 Learning Path

1. **Start with Fundamentals** (00-05)
2. **Build Interactive Apps** (06-09)
3. **Master Hooks** (10-13)
4. **Optimize Performance** (14-17)
5. **Production Apps** (18-23)

## 💡 Best Practices

- Use functional components with hooks
- Keep components small and focused
- Prop-types or TypeScript for type checking
- Lift state only when needed
- Use keys properly in lists
- Avoid inline functions in render
- Memoize expensive computations
- Split code for better performance
- Test components thoroughly

## 🚀 Quick Start

```bash
# Create new React app
npx create-react-app my-app
cd my-app
npm start

# Or with Vite (faster)
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

## 📖 Key Concepts

### Component Lifecycle
1. Mount (useEffect with empty deps)
2. Update (useEffect with deps)
3. Unmount (useEffect cleanup)

### State Management Options
- **Local State**: useState, useReducer
- **Context**: useContext for shared state
- **External**: Redux, Zustand, Recoil, Jotai

### Performance Optimization
- React.memo - Prevent unnecessary re-renders
- useMemo - Memoize expensive calculations
- useCallback - Memoize functions
- Code splitting - Lazy load components
- Virtual scrolling - Large lists

---

Happy React coding! ⚛️
