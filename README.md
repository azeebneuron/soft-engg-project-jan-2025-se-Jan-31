# Team 31 Design System Documentation
Version 1.0 - February 2024

## 🎨 Color Palette

### Theme Colors
- Primary Gradient: `linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247))`
- Dark Background: `#030303`
- Light Background: `#ffffff`

### Text Colors
Dark Mode:
- Primary Text: `rgba(255, 255, 255, 0.9)`
- Secondary Text: `rgba(255, 255, 255, 0.5)`

Light Mode:
- Primary Text: `#1a1a1a`
- Secondary Text: `rgba(0, 0, 0, 0.6)`

### UI Element Colors
- Grid Color: `rgba(99, 102, 241, 0.4)`
- Border Light: `rgba(255, 255, 255, 0.1)` (dark mode)
- Border Dark: `rgba(0, 0, 0, 0.1)` (light mode)

## 📝 Typography

### Font Families
- Primary Font: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Accent Font: `'Pacifico', cursive` (for special headings)

### Font Sizes
- Hero Title: `clamp(2rem, 8vw, 6rem)`
- Section Titles: `clamp(1.5rem, 4vw, 2.5rem)`
- Regular Text: `1rem`
- Secondary Text: `0.95rem`
- Small Text: `0.9rem`
- Badge Text: `0.875rem` (14px)

## 🎯 Spacing System

### Padding
- Container Padding: `2rem`
- Card Padding: `2.5rem`
- Button Padding: `0.75rem 1.5rem`
- Input Field Padding: `0.75rem 1rem`
- Navigation Padding: `1.5rem 2rem`

### Margins
- Section Spacing: `2rem`
- Element Spacing: `1.5rem`
- Text Block Spacing: `0.5rem`

### Gaps
- Form Elements: `1.5rem`
- Navigation Items: `2rem`
- Grid Items: `1rem`

## 🔲 UI Components

### Cards
```css
background: rgba(255, 255, 255, 0.05);
backdrop-filter: blur(10px);
border-radius: 1rem;
border: 1px solid rgba(255, 255, 255, 0.1);
```

### Buttons
Primary:
```css
background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
border-radius: 0.5rem;
padding: 0.75rem 1.5rem;
color: white;
```

### Input Fields
```css
padding: 0.75rem 1rem;
border-radius: 0.5rem;
border: 1px solid rgba(255, 255, 255, 0.1);
background: rgba(255, 255, 255, 0.05);
```

### Navigation
```css
backdrop-filter: blur(10px);
background: rgba(3, 3, 3, 0.5);
border-bottom: 1px solid rgba(255, 255, 255, 0.1);
```

## 🎭 Theme Switching

All components should support both dark and light modes. Use CSS variables for theme-dependent values:

```css
:root {
  --bg-dark: #030303;
  --bg-light: #ffffff;
  --text-dark: rgba(255, 255, 255, 0.9);
  --text-light: #1a1a1a;
  /* ... other theme variables ... */
}
```

## 📱 Responsive Design

### Breakpoints
- Mobile: `max-width: 480px`
- Tablet: `max-width: 768px`
- Desktop: `max-width: 1024px`
- Wide: `max-width: 1280px`

### Mobile Adjustments
- Reduce padding: `1.5rem` for containers
- Stack navigation items
- Adjust font sizes using clamp
- Implement hamburger menu
- Full-width buttons and forms

## 🎨 UI Elements to Build

Based on the requirements document, we need to implement:

1. **Dashboard Components**
   - Learning progress charts
   - Performance metrics displays
   - Deadline tracking widgets
   - Course material navigation

2. **Learning Interface**
   - Query input system
   - Response display area
   - Resource recommendation cards
   - Progress indicators

3. **Management Interfaces**
   - Course resource management
   - Student progress tracking
   - Query routing system
   - Feedback collection forms

4. **Notification System**
   - Alert components
   - Reminder cards
   - Progress notification badges
   - Status indicators

5. **Administrative Tools**
   - Report generation interface
   - System metrics dashboard
   - User management console
   - Resource approval system

## 🔄 Animation Guidelines

### Transitions
- Default Duration: `0.3s`
- Timing Function: `ease`
- Properties to Animate:
  - opacity
  - transform
  - background-color
  - color

### Effects
```css
/* Fade Up Animation */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Grid Movement Animation */
@keyframes grid-move {
  0% {
    transform: perspective(500px) rotateX(60deg) translateY(0);
  }
  100% {
    transform: perspective(500px) rotateX(60deg) translateY(30px);
  }
}
```

## 🛠 Development Practices

1. Use Vue.js composition API for component logic
2. Implement props validation for all components
3. Use emits for component communication
4. Follow BEM methodology for CSS class naming
5. Maintain consistent file structure:
```
Directory structure:
└── /vue-project/
    ├── .editorconfig
    ├── package.json
    ├── README.md
    ├── vite.config.js
    ├── src/
    │   ├── components/
    │   │   └── icons/
    │   │       ├── IconCommunity.vue
    │   │       ├── IconTooling.vue
    │   │       ├── IconEcosystem.vue
    │   │       ├── IconDocumentation.vue
    │   │       └── IconSupport.vue
    │   ├── App.vue
    │   ├── router/
    │   │   └── index.js
    │   ├── main.js
    │   ├── views/
    │   │   ├── ChatInterface.vue
    │   │   ├── HomeView.vue
    │   │   ├── SignUp.vue
    │   │   ├── SignIn.vue
    │   │   └── StudentDashboard.vue
    │   └── assets/
    │       ├── main.css
    │       └── base.css
    ├── eslint.config.js
    ├── public/
    ├── .prettierrc.json
    ├── jsconfig.json
    └── index.html

   ```

## 🔍 Quality Checklist

- [ ] Components support both dark and light modes
- [ ] Responsive on all screen sizes
- [ ] Accessible (WCAG 2.1 AA compliant)
- [ ] Consistent spacing and alignment
- [ ] Smooth animations and transitions
- [ ] Clear visual hierarchy
- [ ] Error states and loading states implemented
- [ ] Interactive elements have hover/focus states
