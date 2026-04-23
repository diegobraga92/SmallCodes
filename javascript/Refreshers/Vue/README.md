# Vue.js Refreshers

Comprehensive Vue 3 guide with Composition API and Options API.

## 📚 Topics Covered

### Fundamentals (Options API & Composition API)
- **00_vue_basics.vue** - Template syntax, directives, interpolation
- **01_components.vue** - Component basics, props, emit
- **02_reactive_data.vue** - ref, reactive, data options
- **03_computed_watchers.vue** - Computed properties, watchers
- **04_event_handling.vue** - v-on, event modifiers, methods
- **05_conditional_rendering.vue** - v-if, v-else, v-show

### Intermediate
- **06_list_rendering.vue** - v-for, keys, array methods
- **07_forms.vue** - v-model, form handling, validation
- **08_component_communication.vue** - Props, emit, provide/inject
- **09_slots.vue** - Default, named, scoped slots
- **10_lifecycle_hooks.vue** - Lifecycle methods, onMounted, onUnmounted
- **11_composables.vue** - Creating reusable composition functions
- **12_directives.vue** - Built-in and custom directives
- **13_transitions.vue** - Transition, TransitionGroup, animations

### Advanced
- **14_composition_api_advanced.vue** - Advanced patterns, script setup
- **15_pinia_state.js** - Pinia store, state management
- **16_vue_router.js** - Routing, navigation, guards
- **17_typescript_vue.vue** - Vue with TypeScript
- **18_performance.vue** - v-once, v-memo, async components
- **19_testing.js** - Vitest, Vue Test Utils
- **20_ssr.js** - Server-side rendering with Nuxt
- **21_advanced_patterns.vue** - Render functions, JSX, teleport

## 🎯 Learning Path

1. **Vue Basics** (00-05)
2. **Component Patterns** (06-09)
3. **Composition API** (10-13)
4. **Production Apps** (14-21)

## 💡 Best Practices

### Composition API (Vue 3)
- Use `<script setup>` for cleaner code
- Group related logic with composables
- Prefer `ref` for primitives, `reactive` for objects
- Use computed for derived state
- Clean up side effects in lifecycle hooks

### Component Design
- Keep components small and focused
- Use props for data down, emit for events up
- Provide/Inject for deep prop drilling
- Slots for flexible content
- Define prop types properly

## 🚀 Quick Start

```bash
# Create Vue 3 project with Vite
npm create vite@latest my-vue-app -- --template vue
cd my-vue-app
npm install
npm run dev

# Or with Vue CLI
npm install -g @vue/cli
vue create my-app
cd my-app
npm run serve
```

## 📖 Key Concepts

### Composition API vs Options API

**Composition API** (Recommended):
```vue
<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)
</script>
```

**Options API** (Legacy):
```vue
<script>
export default {
  data() {
    return { count: 0 }
  },
  computed: {
    doubled() {
      return this.count * 2
    }
  }
}
</script>
```

### Reactivity
- `ref()` - Reactive primitive or object (needs `.value`)
- `reactive()` - Reactive object (direct access)
- `computed()` - Derived state with caching
- `watch()` - React to data changes
- `watchEffect()` - Auto-track dependencies

### Common Directives
- `v-bind` or `:` - Bind attributes
- `v-on` or `@` - Event handling
- `v-model` - Two-way binding
- `v-if/v-else/v-show` - Conditional rendering
- `v-for` - List rendering
- `v-slot` or `#` - Slot content

---

Happy Vue coding! 💚
