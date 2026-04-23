# Angular Refreshers

Comprehensive Angular guide with TypeScript.

## 📚 Topics Covered

### Fundamentals
- **00_angular_basics.ts** - Components, templates, modules
- **01_components.ts** - Component creation, decorators, lifecycle
- **02_templates.html** - Template syntax, interpolation, directives
- **03_data_binding.ts** - Property, event, two-way binding
- **04_directives.ts** - ngIf, ngFor, ngSwitch, custom directives
- **05_pipes.ts** - Built-in pipes, custom pipes, async pipe

### Intermediate
- **06_services.ts** - Services, dependency injection, providers
- **07_http_client.ts** - HttpClient, observables, interceptors
- **08_routing.ts** - Router, routes, parameters, guards
- **09_forms_template.ts** - Template-driven forms, validation
- **10_forms_reactive.ts** - Reactive forms, FormBuilder, validators
- **11_rxjs.ts** - Observables, operators, subjects
- **12_modules.ts** - NgModules, feature modules, lazy loading
- **13_component_interaction.ts** - Input, Output, ViewChild

### Advanced
- **14_state_management.ts** - NgRx, store, actions, effects
- **15_testing.ts** - Jasmine, Karma, TestBed, mocking
- **16_performance.ts** - Change detection, OnPush, trackBy
- **17_animations.ts** - Angular animations, triggers, states
- **18_i18n.ts** - Internationalization, translation
- **19_pwa.ts** - Progressive Web App, service workers
- **20_ssr.ts** - Server-side rendering, Angular Universal
- **21_advanced_patterns.ts** - Custom decorators, dynamic components

## 🎯 Learning Path

1. **Angular Basics** (00-05)
2. **Core Concepts** (06-09)
3. **Forms & HTTP** (10-13)
4. **Advanced Topics** (14-21)

## 💡 Best Practices

### Component Design
- Use OnPush change detection
- Unsubscribe from observables
- Use trackBy with ngFor
- Keep components small
- Use smart/dumb component pattern

### Services
- Single responsibility
- Provide in root when possible
- Use interfaces for types
- Handle errors properly
- Use dependency injection

### RxJS
- Unsubscribe in ngOnDestroy
- Use async pipe in templates
- Avoid nested subscriptions
- Use operators for transformations
- Handle errors in streams

## 🚀 Quick Start

```bash
# Install Angular CLI
npm install -g @angular/cli

# Create new project
ng new my-app
cd my-app

# Run development server
ng serve

# Generate components/services
ng generate component my-component
ng generate service my-service

# Build for production
ng build --prod
```

## 📖 Key Concepts

### Architecture
- **Modules**: NgModule groups related code
- **Components**: UI building blocks
- **Services**: Business logic, data access
- **Dependency Injection**: Service provision
- **Routing**: Navigation between views

### Lifecycle Hooks
1. `ngOnChanges` - Input properties change
2. `ngOnInit` - Component initialization
3. `ngDoCheck` - Change detection
4. `ngAfterContentInit` - Content projection
5. `ngAfterContentChecked` - After content checked
6. `ngAfterViewInit` - View initialization
7. `ngAfterViewChecked` - After view checked
8. `ngOnDestroy` - Component cleanup

### Data Binding
- **Interpolation**: `{{ value }}`
- **Property Binding**: `[property]="value"`
- **Event Binding**: `(event)="handler()"`
- **Two-Way Binding**: `[(ngModel)]="value"`

### Common Decorators
- `@Component` - Define component
- `@Injectable` - Mark service
- `@Input` - Accept data from parent
- `@Output` - Emit events to parent
- `@ViewChild` - Access child component
- `@HostListener` - Listen to host events

---

Happy Angular development! 🅰️
