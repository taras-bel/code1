# NoaMetrics Frontend

[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green.svg)](https://vuejs.org)
[![Nuxt](https://img.shields.io/badge/Nuxt-3.x-black.svg)](https://nuxt.com)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg)](https://tailwindcss.com)

> **Modern, responsive frontend application** for NoaMetrics AI-powered CV analysis platform. Built with Vue.js 3, Nuxt 3, and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Access at http://localhost:3000
```

### Build for Production
```bash
# Build the application
npm run build

# Start production server
npm run start

# Generate static site
npm run generate
```

## 📁 Project Structure

```
frontend/
├── components/              # Vue.js components
│   ├── AppHeader.vue       # Main navigation header
│   ├── AppFooter.vue       # Site footer
│   ├── HeroSection.vue     # Landing page hero
│   ├── VideoAISection.vue  # File upload & demo section
│   ├── JoinBetaDrawer.vue  # Registration modal
│   ├── Toast.vue           # Notification component
│   └── ...                 # Other components
├── pages/                  # Application pages
│   ├── index.vue          # Landing page
│   ├── dashboard.vue      # User dashboard
│   ├── analysis/          # Analysis pages
│   └── features.vue       # Features page
├── composables/           # Vue composables
│   ├── useApi.js         # API client
│   ├── useFormValidation.js # Form validation
│   ├── useJoinBetaDrawer.js # Beta drawer state
│   └── useToast.js       # Toast notifications
├── assets/               # Static assets
│   ├── css/             # Global styles
│   └── images/          # Images and icons
├── layouts/             # Page layouts
├── utils/               # Utility functions
└── public/              # Public static files
```

## 🏗️ Architecture

### Technology Stack
- **Framework**: Vue.js 3 with Composition API
- **Meta Framework**: Nuxt 3
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Vue composables with reactive state
- **Build Tool**: Vite
- **Package Manager**: npm

### Key Features
- **Responsive Design**: Mobile-first approach
- **Component-Based**: Modular, reusable components
- **Type Safety**: TypeScript support (optional)
- **Performance**: Optimized bundle size and loading
- **Accessibility**: WCAG 2.1 AA compliant
- **SEO**: Server-side rendering with meta tags

## 🎨 Design System

### Color Palette
```css
/* Primary Colors */
--primary-50: #f5f7ff;
--primary-600: #6366f1;
--primary-700: #4f46e5;

/* Neutral Colors */
--gray-50: #f9fafb;
--gray-900: #111827;
--gray-600: #4b5563;
```

### Typography
- **Primary Font**: Inter (sans-serif)
- **Secondary Font**: Space Grotesk (for headings)
- **Font Sizes**: Responsive scale from 12px to 48px

### Components
- **Buttons**: Primary, secondary, and ghost variants
- **Forms**: Input fields with validation states
- **Cards**: Content containers with shadows
- **Modals**: Overlay dialogs and drawers
- **Toast**: Notification system

## 🔧 Configuration

### Environment Variables
```env
# API Configuration
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Supabase Configuration
NUXT_PUBLIC_SUPABASE_URL=your_supabase_url
NUXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key

# Application Settings
NUXT_PUBLIC_APP_NAME=NoaMetrics
NUXT_PUBLIC_APP_VERSION=1.0.0
```

### Nuxt Configuration
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  // Development settings
  devtools: { enabled: true },
  
  // CSS and styling
  css: ['~/assets/css/main.css'],
  
  // Modules
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
  ],
  
  // Runtime config
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL,
    }
  }
})
```

## 📱 Components

### Core Components

#### AppHeader.vue
Main navigation component with:
- Responsive mobile menu
- Authentication state management
- Dynamic navigation items
- Logo and branding

#### JoinBetaDrawer.vue
Registration modal with:
- Multi-step form validation
- File upload integration
- Real-time progress tracking
- Success state handling

#### VideoAISection.vue
File upload interface with:
- Drag & drop functionality
- File type validation
- Progress tracking
- Error handling

#### Toast.vue
Notification system with:
- Multiple positions (top, bottom, left, right)
- Auto-dismiss functionality
- Custom styling options
- Accessibility features

### Composables

#### useApi.js
API client with:
- Automatic authentication
- Error handling
- Request/response interceptors
- Retry logic

#### useFormValidation.js
Form validation with:
- Real-time validation
- Custom validation rules
- Error message management
- Field state tracking

#### useJoinBetaDrawer.js
Global state management for:
- Drawer visibility
- Form state persistence
- Cross-component communication

## 🎯 Key Features

### File Upload System
```javascript
// Drag & drop implementation
const onDrop = (e) => {
  const files = Array.from(e.dataTransfer.files)
  handleFiles(files)
}

// File validation
const validateFile = (file) => {
  const maxSize = 10 * 1024 * 1024 // 10MB
  const allowedTypes = ['.pdf', '.doc', '.docx']
  
  if (file.size > maxSize) {
    throw new Error('File too large')
  }
  
  const ext = file.name.split('.').pop().toLowerCase()
  if (!allowedTypes.includes(`.${ext}`)) {
    throw new Error('Invalid file type')
  }
}
```

### Authentication Flow
```javascript
// Login state management
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access_token')
})

// Token management
const setToken = (token) => {
  localStorage.setItem('access_token', token)
  window.dispatchEvent(new CustomEvent('auth-changed'))
}
```

### Form Validation
```javascript
// Real-time validation
const validateField = (fieldName, value) => {
  const rules = validationRules[fieldName]
  const errors = []
  
  rules.forEach(rule => {
    if (!rule.validator(value)) {
      errors.push(rule.message)
    }
  })
  
  return errors
}
```

## 🧪 Testing

### Unit Tests
```bash
# Run unit tests
npm run test:unit

# Run with coverage
npm run test:coverage
```

### Component Tests
```bash
# Test specific component
npm run test:unit -- components/JoinBetaDrawer.vue
```

### E2E Tests
```bash
# Run end-to-end tests
npm run test:e2e
```

## 🚀 Deployment

### Static Site Generation
```bash
# Generate static site
npm run generate

# Deploy to Netlify/Vercel
npm run deploy
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

### Environment-Specific Builds
```bash
# Development
npm run dev

# Staging
npm run build:staging

# Production
npm run build:production
```

## 📊 Performance

### Optimization Strategies
- **Code Splitting**: Automatic route-based splitting
- **Lazy Loading**: Components loaded on demand
- **Image Optimization**: Automatic image compression
- **Caching**: Browser and CDN caching strategies
- **Bundle Analysis**: Webpack bundle analyzer

### Performance Metrics
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## 🔒 Security

### Security Features
- **XSS Protection**: Input sanitization
- **CSRF Protection**: Token-based protection
- **Content Security Policy**: CSP headers
- **HTTPS Enforcement**: Secure connections only
- **Input Validation**: Client and server-side validation

### Best Practices
- Sanitize all user inputs
- Use HTTPS in production
- Implement proper CORS policies
- Regular dependency updates
- Security headers configuration

## 🌐 Internationalization

### Multi-language Support
```javascript
// i18n configuration
export default {
  locales: [
    { code: 'en', iso: 'en-US', name: 'English' },
    { code: 'ru', iso: 'ru-RU', name: 'Русский' },
    { code: 'es', iso: 'es-ES', name: 'Español' }
  ],
  defaultLocale: 'en',
  strategy: 'prefix_except_default'
}
```

### Translation Files
```json
// locales/en.json
{
  "hero": {
    "title": "Stop Guessing. Hire the Real Talent.",
    "subtitle": "AI-powered CV analysis for better hiring decisions"
  }
}
```

## 🔧 Development

### Development Commands
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check
```

### Code Standards
- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **Husky**: Git hooks
- **Conventional Commits**: Commit message format

### Git Workflow
```bash
# Feature branch
git checkout -b feature/new-feature

# Development
git add .
git commit -m "feat: add new feature"

# Push and PR
git push origin feature/new-feature
```

## 📈 Analytics

### User Analytics
- **Page Views**: Track user navigation
- **User Engagement**: Time on page, interactions
- **Conversion Tracking**: Form submissions, file uploads
- **Error Tracking**: JavaScript errors and API failures

### Performance Analytics
- **Core Web Vitals**: Real user metrics
- **API Performance**: Response times and errors
- **Bundle Size**: JavaScript bundle analysis
- **Loading Times**: Page load performance

## 🆘 Troubleshooting

### Common Issues

#### Build Errors
```bash
# Clear cache
rm -rf node_modules/.cache
npm run build

# Update dependencies
npm update
```

#### Development Server Issues
```bash
# Clear Nuxt cache
rm -rf .nuxt
npm run dev

# Check port conflicts
lsof -ti:3000 | xargs kill -9
```

#### API Connection Issues
```bash
# Check environment variables
echo $NUXT_PUBLIC_API_BASE_URL

# Test API endpoint
curl http://localhost:8000/health
```

## 📚 Resources

### Documentation
- [Vue.js 3 Documentation](https://vuejs.org/)
- [Nuxt 3 Documentation](https://nuxt.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

### Tools
- [Vue DevTools](https://devtools.vuejs.org/)
- [Nuxt DevTools](https://devtools.nuxt.com/)
- [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)

### Community
- [Vue.js Community](https://vuejs.org/community/)
- [Nuxt Community](https://nuxt.com/community)
- [Discord Server](https://discord.gg/nuxt)

---

**Frontend Team** | **Last Updated**: January 2025
