/**
 * REACT FORMS
 * ============
 * Controlled components, validation, React Hook Form, form libraries
 */

import React, { useState, useRef } from 'react';

console.log("=".repeat(80));
console.log("REACT FORMS");
console.log("=".repeat(80));

// ============================================================================
// 1. CONTROLLED COMPONENTS
// ============================================================================

/*
   In controlled components, form data is handled by React state.
   The input's value is controlled by state, and changes update state.
*/

function ControlledForm() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        age: '',
        role: 'user',
        subscribe: true,
        gender: ''
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Form submitted:', formData);
    };

    return (
        <form onSubmit={handleSubmit}>
            {/* Text input */}
            <input
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Name"
            />

            {/* Email input */}
            <input
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Email"
            />

            {/* Number input */}
            <input
                name="age"
                type="number"
                value={formData.age}
                onChange={handleChange}
                placeholder="Age"
            />

            {/* Select dropdown */}
            <select name="role" value={formData.role} onChange={handleChange}>
                <option value="user">User</option>
                <option value="admin">Admin</option>
                <option value="moderator">Moderator</option>
            </select>

            {/* Checkbox */}
            <label>
                <input
                    name="subscribe"
                    type="checkbox"
                    checked={formData.subscribe}
                    onChange={handleChange}
                />
                Subscribe to newsletter
            </label>

            {/* Radio buttons */}
            <div>
                <label>
                    <input
                        name="gender"
                        type="radio"
                        value="male"
                        checked={formData.gender === 'male'}
                        onChange={handleChange}
                    />
                    Male
                </label>
                <label>
                    <input
                        name="gender"
                        type="radio"
                        value="female"
                        checked={formData.gender === 'female'}
                        onChange={handleChange}
                    />
                    Female
                </label>
            </div>

            {/* Textarea */}
            <textarea
                name="bio"
                value={formData.bio || ''}
                onChange={handleChange}
                placeholder="Bio"
            />

            <button type="submit">Submit</button>
        </form>
    );
}

// ============================================================================
// 2. UNCONTROLLED COMPONENTS (useRef)
// ============================================================================

/*
   Uncontrolled components store their own state in the DOM.
   Use refs to access values when needed (e.g., on submit).
   Useful for simple forms or integrating with non-React code.
*/

function UncontrolledForm() {
    const nameRef = useRef(null);
    const emailRef = useRef(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Name:', nameRef.current.value);
        console.log('Email:', emailRef.current.value);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input ref={nameRef} defaultValue="" placeholder="Name" />
            <input ref={emailRef} defaultValue="" placeholder="Email" />
            <button type="submit">Submit</button>
        </form>
    );
}

// ============================================================================
// 3. FORM VALIDATION
// ============================================================================

function ValidatedForm() {
    const [values, setValues] = useState({ email: '', password: '', confirmPassword: '' });
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});

    const validate = (fieldValues = values) => {
        const newErrors = {};

        if (!fieldValues.email) {
            newErrors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(fieldValues.email)) {
            newErrors.email = 'Email is invalid';
        }

        if (!fieldValues.password) {
            newErrors.password = 'Password is required';
        } else if (fieldValues.password.length < 6) {
            newErrors.password = 'Password must be at least 6 characters';
        }

        if (fieldValues.confirmPassword !== fieldValues.password) {
            newErrors.confirmPassword = 'Passwords do not match';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        const newValues = { ...values, [name]: value };
        setValues(newValues);

        // Validate on change if field was touched
        if (touched[name]) {
            validate(newValues);
        }
    };

    const handleBlur = (e) => {
        const { name } = e.target;
        setTouched(prev => ({ ...prev, [name]: true }));
        validate();
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setTouched({ email: true, password: true, confirmPassword: true });

        if (validate()) {
            console.log('Form is valid, submitting:', values);
        }
    };

    return (
        <form onSubmit={handleSubmit} noValidate>
            <div>
                <input
                    name="email"
                    type="email"
                    value={values.email}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    placeholder="Email"
                    className={errors.email && touched.email ? 'error' : ''}
                />
                {errors.email && touched.email && <span className="error-msg">{errors.email}</span>}
            </div>

            <div>
                <input
                    name="password"
                    type="password"
                    value={values.password}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    placeholder="Password"
                />
                {errors.password && touched.password && <span>{errors.password}</span>}
            </div>

            <div>
                <input
                    name="confirmPassword"
                    type="password"
                    value={values.confirmPassword}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    placeholder="Confirm Password"
                />
                {errors.confirmPassword && touched.confirmPassword && <span>{errors.confirmPassword}</span>}
            </div>

            <button type="submit">Register</button>
        </form>
    );
}

// ============================================================================
// 4. REACT HOOK FORM (Library)
// ============================================================================

/*
   React Hook Form is a performant form library with minimal re-renders.
   
   // install: npm install react-hook-form
   
   import { useForm } from 'react-hook-form';
*/

// function HookFormExample() {
//     const {
//         register,        // Register inputs
//         handleSubmit,    // Form submit handler
//         watch,           // Watch field values
//         formState: { errors, isSubmitting },
//         reset            // Reset form
//     } = useForm({
//         defaultValues: { name: '', email: '' }
//     });
//
//     const onSubmit = async (data) => {
//         await fetch('/api/users', { method: 'POST', body: JSON.stringify(data) });
//         reset();
//     };
//
//     return (
//         <form onSubmit={handleSubmit(onSubmit)}>
//             <input
//                 {...register('name', {
//                     required: 'Name is required',
//                     minLength: { value: 2, message: 'Min 2 characters' }
//                 })}
//             />
//             {errors.name && <span>{errors.name.message}</span>}
//
//             <input
//                 {...register('email', {
//                     required: 'Email is required',
//                     pattern: {
//                         value: /\S+@\S+\.\S+/,
//                         message: 'Invalid email'
//                     }
//                 })}
//             />
//             {errors.email && <span>{errors.email.message}</span>}
//
//             <button disabled={isSubmitting} type="submit">
//                 {isSubmitting ? 'Submitting...' : 'Submit'}
//             </button>
//         </form>
//     );
// }

// ============================================================================
// 5. VALIDATION WITH ZOD (Schema Validation)
// ============================================================================

/*
   Zod is a TypeScript-first schema validation library.
   Works great with React Hook Form via @hookform/resolvers.
   
   // install: npm install zod @hookform/resolvers
   
   import { z } from 'zod';
   import { zodResolver } from '@hookform/resolvers/zod';
*/

// const schema = z.object({
//     email: z.string().email('Invalid email'),
//     password: z.string().min(6, 'Min 6 characters'),
//     age: z.number().min(18, 'Must be 18+').max(120),
//     terms: z.literal(true, { errorMap: () => ({ message: 'Must accept terms' }) })
// });
//
// function ZodForm() {
//     const { register, handleSubmit, formState: { errors } } = useForm({
//         resolver: zodResolver(schema)
//     });
//
//     return (
//         <form onSubmit={handleSubmit(data => console.log(data))}>
//             <input {...register('email')} />
//             {errors.email && <span>{errors.email.message}</span>}
//
//             <input type="password" {...register('password')} />
//             {errors.password && <span>{errors.password.message}</span>}
//
//             <input type="number" {...register('age', { valueAsNumber: true })} />
//             {errors.age && <span>{errors.age.message}</span>}
//
//             <input type="checkbox" {...register('terms')} /> Accept terms
//             {errors.terms && <span>{errors.terms.message}</span>}
//
//             <button type="submit">Submit</button>
//         </form>
//     );
// }

// ============================================================================
// 6. FILE UPLOAD
// ============================================================================

function FileUploadForm() {
    const [files, setFiles] = useState([]);
    const [preview, setPreview] = useState(null);

    const handleFileChange = (e) => {
        const selectedFiles = Array.from(e.target.files);
        setFiles(selectedFiles);

        // Preview image
        if (selectedFiles[0]?.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => setPreview(e.target.result);
            reader.readAsDataURL(selectedFiles[0]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));

        // await fetch('/api/upload', { method: 'POST', body: formData });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="file"
                multiple
                accept="image/*, .pdf"
                onChange={handleFileChange}
            />
            {preview && <img src={preview} alt="Preview" width="200" />}
            <button type="submit">Upload ({files.length} files)</button>
        </form>
    );
}

// ============================================================================
// 7. BEST PRACTICES
// ============================================================================

/*
   1. Prefer controlled components for complex forms
   2. Use uncontrolled (refs) for simple, one-off inputs
   3. Validate on blur for better UX (not on every keystroke)
   4. Use React Hook Form or Formik for complex forms
   5. Use Zod or Yup for schema validation
   6. Show validation errors after blur (not on every keystroke)
   7. Disable submit button while submitting
   8. Handle loading, error, and success states
   9. Use FormData for file uploads
   10. Reset form after successful submission
*/

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Controlled components: state drives input values");
console.log("2. Uncontrolled components: DOM stores values, refs access them");
console.log("3. Validate on blur + submit for good UX");
console.log("4. React Hook Form reduces re-renders and boilerplate");
console.log("5. Zod provides TypeScript-first schema validation");
console.log("6. File uploads need multipart/form-data (FormData)");
console.log("7. Always prevent default form submission");
console.log("=".repeat(80));

export default ControlledForm;
