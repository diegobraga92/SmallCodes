# Next.js Refreshers

Comprehensive Next.js guide for React framework with SSR/SSG.

## 📚 Topics Covered

### Fundamentals
- **00_next_basics.jsx** - Pages, routing, file-based routing
- **01_navigation.jsx** - Link, router, navigation methods
- **02_dynamic_routes.jsx** - Dynamic segments, catch-all routes
- **03_data_fetching.jsx** - getStaticProps, getServerSideProps
- **04_api_routes.js** - API endpoints, request handlers
- **05_styling.jsx** - CSS modules, styled-jsx, Tailwind

### Intermediate
- **06_image_optimization.jsx** - Next/Image, image optimization
- **07_head_metadata.jsx** - Meta tags, SEO, title
- **08_environment_vars.js** - env variables, configuration
- **09_middleware.js** - Middleware, redirects, rewrites
- **10_layouts.jsx** - Shared layouts, nested layouts
- **11_error_handling.jsx** - Error pages, error boundaries
- **12_authentication.jsx** - NextAuth.js, auth patterns
- **13_app_router.jsx** - App router (Next.js 13+), server components

### Advanced
- **14_server_components.jsx** - RSC, streaming, suspense
- **15_server_actions.js** - Server actions, mutations
- **16_static_generation.jsx** - ISR, on-demand revalidation
- **17_internationalization.jsx** - i18n, locales, translations
- **18_performance.jsx** - Performance optimization, code splitting
- **19_testing.js** - Jest, Playwright, E2E testing
- **20_deployment.js** - Vercel, Docker, self-hosting
- **21_advanced_patterns.jsx** - Parallel routes, intercepting routes

## 🎯 Learning Path

1. **Next.js Basics** (00-05)
2. **Core Features** (06-12)
3. **App Router** (13-17)
4. **Production** (18-21)

## 💡 Best Practices

### Rendering Strategies
- **SSG (Static)**: Pre-render at build time
  - Best for: Blog posts, docs, marketing pages
  - Use: `getStaticProps`

- **ISR (Incremental Static Regeneration)**: Regenerate on demand
  - Best for: E-commerce, frequently updated content
  - Use: `getStaticProps` with `revalidate`

- **SSR (Server-Side)**: Render on each request
  - Best for: Personalized pages, real-time data
  - Use: `getServerSideProps`

- **CSR (Client-Side)**: Render in browser
  - Best for: Dashboards, private pages
  - Use: `useEffect` or SWR

### File Structure (App Router)
```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page
├── error.tsx           # Error boundary
├── loading.tsx         # Loading UI
├── api/                # API routes
│   └── users/
│       └── route.ts
├── blog/
│   ├── page.tsx        # /blog
│   └── [slug]/
│       └── page.tsx    # /blog/[slug]
└── dashboard/
    └── @analytics/     # Parallel route
        └── page.tsx
```

## 🚀 Quick Start

```bash
# Create Next.js app
npx create-next-app@latest my-app
cd my-app

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 📖 Key Concepts

### Data Fetching (Pages Router)
```javascript
// Static Generation
export async function getStaticProps() {
  const data = await fetchData();
  return { props: { data } };
}

// Server-Side Rendering
export async function getServerSideProps(context) {
  const data = await fetchData();
  return { props: { data } };
}

// Incremental Static Regeneration
export async function getStaticProps() {
  return {
    props: { data },
    revalidate: 60 // Revalidate every 60 seconds
  };
}
```

### Data Fetching (App Router)
```javascript
// Server Component (default)
async function Page() {
  const data = await fetch('https://api.example.com/data');
  return <div>{data}</div>;
}

// Client Component
'use client'
import { useState, useEffect } from 'react';

function ClientPage() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch('/api/data').then(r => r.json()).then(setData);
  }, []);
  return <div>{data}</div>;
}
```

### API Routes
```javascript
// pages/api/users.js or app/api/users/route.ts
export async function GET(request) {
  const users = await getUsers();
  return Response.json(users);
}

export async function POST(request) {
  const body = await request.json();
  const user = await createUser(body);
  return Response.json(user, { status: 201 });
}
```

---

Happy Next.js development! ▲
