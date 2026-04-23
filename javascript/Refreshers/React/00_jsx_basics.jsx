/*
    REACT JSX BASICS
    Covering: JSX syntax, expressions, attributes, fragments, comments
    
    JSX is a syntax extension for JavaScript that looks like HTML but
    compiles to JavaScript function calls.
*/

import React from 'react';

console.log("=== React JSX Basics ===\n");

// ============================================================================
// 1. WHAT IS JSX?
// ============================================================================

/*
    JSX (JavaScript XML):
    - Syntax extension that looks like HTML
    - Transpiled by Babel to React.createElement() calls
    - Makes component structure more readable
    - Not required (can use React.createElement directly)
    
    JSX: <h1>Hello</h1>
    Compiles to: React.createElement('h1', null, 'Hello')
*/

// Basic JSX element
const basicElement = <h1>Hello, World!</h1>;

// Without JSX (equivalent)
const withoutJSX = React.createElement('h1', null, 'Hello, World!');


// ============================================================================
// 2. JSX EXPRESSIONS
// ============================================================================

/*
    EXPRESSIONS IN JSX:
    - Use curly braces {} to embed JavaScript expressions
    - Can include variables, calculations, function calls
    - Automatically escapes values (XSS protection)
*/

function JSXExpressions() {
    const name = "Alice";
    const age = 30;
    const numbers = [1, 2, 3, 4, 5];
    
    return (
        <div>
            {/* Simple expression */}
            <h1>Hello, {name}!</h1>
            
            {/* Calculation */}
            <p>You are {age} years old</p>
            <p>Next year you'll be {age + 1}</p>
            
            {/* Function call */}
            <p>Random: {Math.random()}</p>
            
            {/* Ternary operator */}
            <p>{age >= 18 ? "Adult" : "Minor"}</p>
            
            {/* Logical AND */}
            {age >= 21 && <p>Can drink in the US</p>}
            
            {/* Array method */}
            <p>Sum: {numbers.reduce((a, b) => a + b, 0)}</p>
            
            {/* Template literal */}
            <p>{`${name} is ${age} years old`}</p>
        </div>
    );
}


// ============================================================================
// 3. JSX ATTRIBUTES
// ============================================================================

/*
    JSX ATTRIBUTES:
    - Use camelCase for attributes (className, htmlFor)
    - Can use expressions in attributes
    - Boolean attributes: presence = true
    - Style attribute takes an object
*/

function JSXAttributes() {
    const imageUrl = "https://example.com/image.jpg";
    const altText = "Description";
    const isActive = true;
    const customClass = "highlight";
    
    // Inline styles (object with camelCase properties)
    const divStyle = {
        backgroundColor: 'blue',
        color: 'white',
        padding: '10px',
        borderRadius: '5px'
    };
    
    return (
        <div>
            {/* className instead of class */}
            <div className="container">Content</div>
            
            {/* Expression in attribute */}
            <div className={customClass}>Highlighted</div>
            
            {/* Conditional class */}
            <div className={isActive ? "active" : "inactive"}>Status</div>
            
            {/* Multiple classes */}
            <div className={`base ${isActive && 'active'}`}>Multi</div>
            
            {/* Image attributes */}
            <img src={imageUrl} alt={altText} width="200" />
            
            {/* Boolean attribute (disabled = true) */}
            <button disabled>Disabled</button>
            <button disabled={true}>Also Disabled</button>
            <button disabled={false}>Enabled</button>
            
            {/* htmlFor instead of for (label) */}
            <label htmlFor="email">Email:</label>
            <input id="email" type="email" />
            
            {/* Style object */}
            <div style={divStyle}>Styled div</div>
            
            {/* Inline style */}
            <div style={{ fontSize: '20px', marginTop: '10px' }}>
                Inline styled
            </div>
            
            {/* Data attributes */}
            <div data-id="123" data-category="tech">
                Data attributes
            </div>
            
            {/* Spread attributes */}
            <input {...{type: 'text', placeholder: 'Enter text'}} />
        </div>
    );
}


// ============================================================================
// 4. JSX CHILDREN
// ============================================================================

/*
    JSX CHILDREN:
    - Elements can contain other elements (nesting)
    - Can be text, elements, expressions, or arrays
    - Must have one root element (or use Fragment)
*/

function JSXChildren() {
    const items = ['Apple', 'Banana', 'Orange'];
    
    return (
        <div>
            {/* Text children */}
            <h1>Hello</h1>
            
            {/* Nested elements */}
            <div>
                <h2>Subtitle</h2>
                <p>Paragraph</p>
            </div>
            
            {/* Expression as child */}
            <p>{2 + 2}</p>
            
            {/* Array of elements */}
            <ul>
                {items.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ul>
            
            {/* Mixed children */}
            <div>
                Text
                <span>Element</span>
                {' More text '}
                <strong>Bold</strong>
            </div>
        </div>
    );
}


// ============================================================================
// 5. FRAGMENTS
// ============================================================================

/*
    FRAGMENTS:
    - Group multiple elements without adding extra DOM node
    - <React.Fragment> or shorthand <>
    - Key prop only available on <React.Fragment>
*/

function Fragments() {
    return (
        <>
            {/* Shorthand syntax */}
            <h1>Title</h1>
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
        </>
    );
}

function FragmentsWithKey() {
    const items = ['Item 1', 'Item 2', 'Item 3'];
    
    return (
        <div>
            {items.map((item, index) => (
                <React.Fragment key={index}>
                    <dt>{item}</dt>
                    <dd>Description</dd>
                </React.Fragment>
            ))}
        </div>
    );
}


// ============================================================================
// 6. JSX COMMENTS
// ============================================================================

function JSXComments() {
    return (
        <div>
            {/* Single line comment */}
            
            {/* 
                Multi-line
                comment
            */}
            
            <h1>Content</h1>
            
            {/* Comment inside JSX */}
            <p>
                Some text
                {/* Can comment here too */}
            </p>
            
            {/* 
                Cannot use // comments in JSX!
                // This won't work
                Must use {  } syntax
            */}
        </div>
    );
}


// ============================================================================
// 7. CONDITIONAL RENDERING
// ============================================================================

function ConditionalRendering({ isLoggedIn, role, count }) {
    return (
        <div>
            {/* Ternary operator */}
            {isLoggedIn ? (
                <h1>Welcome back!</h1>
            ) : (
                <h1>Please log in</h1>
            )}
            
            {/* Logical AND */}
            {isLoggedIn && <p>You are logged in</p>}
            
            {/* Multiple conditions */}
            {isLoggedIn && role === 'admin' && (
                <button>Admin Panel</button>
            )}
            
            {/* Nullish coalescing for default values */}
            <p>Count: {count ?? 0}</p>
            
            {/* Early return pattern (in component body) */}
            {!isLoggedIn && <div>Not logged in</div>}
            
            {/* Switch-like pattern with object */}
            {
                {
                    admin: <div>Admin Dashboard</div>,
                    user: <div>User Dashboard</div>,
                    guest: <div>Guest View</div>
                }[role]
            }
        </div>
    );
}


// ============================================================================
// 8. LISTS AND KEYS
// ============================================================================

/*
    LISTS IN JSX:
    - Use map() to render arrays
    - Each element needs unique 'key' prop
    - Keys help React identify which items changed
    - Don't use array index as key if list can change
*/

function Lists() {
    const users = [
        { id: 1, name: 'Alice', age: 30 },
        { id: 2, name: 'Bob', age: 25 },
        { id: 3, name: 'Carol', age: 35 }
    ];
    
    return (
        <div>
            {/* Simple list */}
            <ul>
                {users.map(user => (
                    <li key={user.id}>
                        {user.name} ({user.age})
                    </li>
                ))}
            </ul>
            
            {/* List with complex content */}
            <div>
                {users.map(user => (
                    <div key={user.id} className="user-card">
                        <h3>{user.name}</h3>
                        <p>Age: {user.age}</p>
                        <button>View Profile</button>
                    </div>
                ))}
            </div>
            
            {/* Filtered list */}
            <ul>
                {users
                    .filter(user => user.age >= 30)
                    .map(user => (
                        <li key={user.id}>{user.name}</li>
                    ))
                }
            </ul>
        </div>
    );
}


// ============================================================================
// 9. JSX GOTCHAS AND BEST PRACTICES
// ============================================================================

/*
    JSX BEST PRACTICES:
    
    1. Always use keys in lists (unique, stable)
    2. className not class
    3. htmlFor not for
    4. Self-closing tags need /
    5. Style attribute takes object
    6. Event handlers are camelCase (onClick not onclick)
    7. Always sanitize user input (React does this automatically)
    8. Use fragments to avoid extra divs
    9. Extract complex JSX into variables or components
    10. Keep JSX expressions simple
*/

function BestPractices() {
    // Good: Extract complex JSX
    const userProfile = (
        <div className="profile">
            <img src="avatar.jpg" alt="User" />
            <span>Username</span>
        </div>
    );
    
    // Good: Extract conditional logic
    const renderStatus = (status) => {
        if (status === 'active') return <span>🟢 Active</span>;
        if (status === 'inactive') return <span>🔴 Inactive</span>;
        return <span>⚪ Unknown</span>;
    };
    
    return (
        <div>
            {/* Good: Self-closing tags */}
            <img src="image.jpg" alt="Description" />
            <br />
            <input type="text" />
            
            {/* Good: Use extracted JSX */}
            {userProfile}
            
            {/* Good: Use helper function */}
            {renderStatus('active')}
            
            {/* Bad: Long nested ternary */}
            {/* Avoid: status === 'active' ? ... : status === 'inactive' ? ... : ... */}
        </div>
    );
}


// ============================================================================
// 10. COMPLETE EXAMPLE
// ============================================================================

function CompleteExample() {
    const user = {
        name: 'Alice',
        age: 30,
        avatar: 'https://i.pravatar.cc/150?img=1',
        isActive: true,
        role: 'admin'
    };
    
    const posts = [
        { id: 1, title: 'First Post', likes: 10 },
        { id: 2, title: 'Second Post', likes: 25 },
        { id: 3, title: 'Third Post', likes: 15 }
    ];
    
    return (
        <div className="container">
            <header className="header">
                <h1>Dashboard</h1>
                {user.isActive && (
                    <span className="status-badge">Online</span>
                )}
            </header>
            
            <div className="user-profile">
                <img 
                    src={user.avatar} 
                    alt={user.name}
                    className="avatar"
                />
                <div className="user-info">
                    <h2>{user.name}</h2>
                    <p>Age: {user.age}</p>
                    <p>Role: {user.role.toUpperCase()}</p>
                </div>
            </div>
            
            <section className="posts">
                <h3>Recent Posts ({posts.length})</h3>
                {posts.length > 0 ? (
                    <ul>
                        {posts.map(post => (
                            <li key={post.id} className="post-item">
                                <span>{post.title}</span>
                                <span className="likes">
                                    ❤️ {post.likes}
                                </span>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No posts yet</p>
                )}
            </section>
            
            <footer>
                <p>&copy; 2024 Dashboard</p>
            </footer>
        </div>
    );
}


// Export components for use
export {
    JSXExpressions,
    JSXAttributes,
    JSXChildren,
    Fragments,
    FragmentsWithKey,
    JSXComments,
    ConditionalRendering,
    Lists,
    BestPractices,
    CompleteExample
};

/*
    KEY TAKEAWAYS:
    
    1. JSX looks like HTML but is JavaScript
    2. Use {} for expressions
    3. camelCase for attributes (className, onClick)
    4. Fragments group elements without extra DOM nodes
    5. Keys required for list items
    6. Conditional rendering with &&, ?:, or if statements
    7. Comments use { } syntax
    8. Keep JSX simple and readable
    9. Extract complex logic
    10. React automatically escapes values (XSS protection)
*/
