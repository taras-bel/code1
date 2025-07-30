# 🤝 Contributing to NoaMetrics

Thank you for your interest in contributing to NoaMetrics! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Documentation](#documentation)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/noa-metrics.git
   cd noa-metrics
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original/noa-metrics.git
   ```

## 🔧 Development Setup

### 1. Environment Setup

```bash
# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env
```

### 2. Install Dependencies

```bash
# Backend dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Frontend dependencies
cd ../frontend
npm install
```

### 3. Start Development Environment

```bash
# Start with Docker (recommended)
docker-compose up -d

# Or start services individually
cd backend && python main.py
cd frontend && npm run dev
```

## 🔄 Making Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clear, readable code
- Add comments for complex logic
- Follow the existing code style
- Update documentation if needed

### 3. Test Your Changes

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm run test

# Integration tests
python test_api_endpoints.py
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_api.py

# Run with verbose output
python -m pytest -v
```

### Frontend Testing

```bash
cd frontend

# Run unit tests
npm run test

# Run with coverage
npm run test:coverage

# Run e2e tests
npm run test:e2e
```

### Integration Testing

```bash
# Test API endpoints
python test_api_endpoints.py

# Test CV analysis
python test_cv_analysis.py

# Test complete flow
python test_complete_flow.py
```

## 📤 Submitting Changes

### 1. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 2. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template
5. Submit the PR

### 3. PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🎨 Code Style

### Python (Backend)

- Use **Black** for code formatting
- Use **flake8** for linting
- Follow **PEP 8** guidelines
- Use type hints where appropriate

```bash
# Format code
black backend/

# Check linting
flake8 backend/
```

### JavaScript/Vue (Frontend)

- Use **ESLint** for linting
- Use **Prettier** for formatting
- Follow **Vue Style Guide**
- Use **TypeScript** for type safety

```bash
# Format code
npm run format

# Check linting
npm run lint

# Fix linting issues
npm run lint:fix
```

### General Guidelines

- Use meaningful variable and function names
- Keep functions small and focused
- Add docstrings to functions and classes
- Use consistent indentation
- Remove unused imports and variables

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Use clear, concise language
- Include examples for complex functions
- Document parameters and return values

### API Documentation

- Update API documentation for new endpoints
- Include request/response examples
- Document error codes and messages
- Keep OpenAPI/Swagger docs up to date

### User Documentation

- Update README.md for new features
- Add usage examples
- Include screenshots for UI changes
- Update deployment guides

## 🐛 Reporting Issues

### Before Reporting

1. Check existing issues
2. Search documentation
3. Try to reproduce the issue
4. Check if it's a known limitation

### Issue Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 11]
- Browser: [e.g., Chrome 120]
- Version: [e.g., v1.2.3]

## Additional Information
Screenshots, logs, etc.
```

## 💡 Feature Requests

### Before Requesting

1. Check if the feature already exists
2. Search existing feature requests
3. Consider if it aligns with project goals
4. Think about implementation complexity

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why this feature is needed

## Proposed Solution
How you think it should work

## Alternatives Considered
Other approaches you considered

## Additional Information
Mockups, examples, etc.
```

## 🏷️ Labels

We use the following labels for issues and PRs:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `priority: high` - High priority
- `priority: low` - Low priority
- `status: in progress` - Work in progress
- `status: blocked` - Blocked by something else

## 🎯 Getting Help

- **Documentation:** Check the [docs/](docs/) folder
- **Issues:** Search existing [GitHub Issues](https://github.com/yourusername/noa-metrics/issues)
- **Discussions:** Use [GitHub Discussions](https://github.com/yourusername/noa-metrics/discussions)
- **Email:** support@noametrics.com

## 🙏 Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor hall of fame
- GitHub contributors page

Thank you for contributing to NoaMetrics! 🚀 