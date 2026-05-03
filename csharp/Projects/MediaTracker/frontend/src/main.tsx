import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'

/*
 * This is the entry point of the React application.
 *
 * createRoot is the React 18+ API for rendering. It replaces ReactDOM.render().
 * The "!" (non-null assertion) tells TypeScript that getElementById won't return
 * null — we know the element exists in index.html.
 *
 * StrictMode is a development-only wrapper that:
 * 1. Double-invokes effects to detect side-effect bugs
 * 2. Checks for deprecated API usage
 * 3. Highlights potential problems
 *
 * StrictMode doesn't affect production builds.
 */
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
