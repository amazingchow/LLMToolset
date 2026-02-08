# Contributing to LLM Toolset

First off, thank you for considering contributing to LLM Toolset! It's people like you that make this tool better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Contributing Code](#contributing-code)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
  - [JavaScript/TypeScript Style Guide](#javascripttypescript-style-guide)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please be respectful, inclusive, and considerate in all interactions.

### Our Standards

- **Be respectful**: Value each other's ideas, styles, and viewpoints
- **Be inclusive**: Welcome newcomers and encourage diverse perspectives
- **Be collaborative**: Work together and help each other grow
- **Be professional**: Keep discussions constructive and on-topic

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. Input '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., macOS 13.0, Ubuntu 22.04]
- Python Version: [e.g., 3.10.5]
- Node.js Version: [e.g., 18.16.0]
- Browser: [e.g., Chrome 120, Safari 17]

**Additional Context**
Any other context about the problem.
```

### Suggesting Features

We love to receive feature requests! Before submitting, please:

1. Check if the feature has already been requested
2. Ensure it aligns with the project's goals
3. Provide a clear use case

**Feature Request Template:**

```markdown
**Problem Statement**
Describe the problem you're trying to solve.

**Proposed Solution**
How do you envision this feature working?

**Alternatives Considered**
What other solutions have you considered?

**Additional Context**
Mockups, examples, or references.
```

### Contributing Code

We welcome code contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** from `master`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## Development Setup

### Prerequisites

- Git
- Python 3.10 or higher
- Node.js 18 or higher (LTS recommended)
- `uv` for Python package management

### Initial Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/LLMToolset.git
cd LLMToolset

# Add upstream remote
git remote add upstream https://github.com/amazingchow/LLMToolset.git

# Backend setup
cd backend
uv venv
uv sync
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Frontend setup
cd ../frontend
npm install
```

### Running Tests

**Backend Tests:**
```bash
cd backend
make test
# Or manually:
# pytest tests/
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

### Running in Development Mode

**Backend (Terminal 1):**
```bash
cd backend
make dev
# Runs on http://127.0.0.1:15050
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
# Runs on http://localhost:13031
```

## Development Workflow

### 1. Create a Feature Branch

```bash
# Update your master branch
git checkout master
git pull upstream master

# Create a new feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clean, maintainable code
- Follow the style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add feature: description of what you added"
```

### 4. Keep Your Branch Updated

```bash
# Fetch upstream changes
git fetch upstream

# Rebase your branch on top of master
git rebase upstream/master
```

### 5. Push Your Changes

```bash
git push origin feature/your-feature-name
```

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

**Good Examples:**
```
Add memory calculation for INT4 quantization
Fix overflow error in activation estimation
Update documentation for model configuration
Refactor memory calculator to improve readability
```

**Commit Message Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Python Style Guide

We follow [PEP 8](https://peps.python.org/pep-0008/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Type hints**: Use type hints for function signatures

**Code Formatting:**
```bash
# Format with black
black backend/

# Sort imports with isort
isort backend/

# Lint with flake8
flake8 backend/
```

**Example:**
```python
from typing import Dict, Optional

def calculate_memory(
    model_params: int,
    precision: str,
    batch_size: int = 1,
    sequence_length: int = 512
) -> Dict[str, float]:
    """
    Calculate memory requirements for LLM inference.

    Args:
        model_params: Number of model parameters
        precision: Data precision (fp32, fp16, int8)
        batch_size: Batch size for inference
        sequence_length: Maximum sequence length

    Returns:
        Dictionary containing memory estimates in GB
    """
    # Implementation here
    pass
```

### JavaScript/TypeScript Style Guide

We follow modern JavaScript/TypeScript best practices:

- **Indentation**: 2 spaces
- **Quotes**: Single quotes for strings
- **Semicolons**: Use semicolons
- **Arrow functions**: Prefer arrow functions
- **Async/await**: Prefer async/await over promises

**Code Formatting:**
```bash
# Format with Prettier
npm run format

# Lint with ESLint
npm run lint
```

**Example:**
```typescript
interface MemoryResult {
  totalMemory: number;
  modelMemory: number;
  activationMemory: number;
}

export const calculateMemory = async (
  modelParams: number,
  precision: string
): Promise<MemoryResult> => {
  // Implementation here
  return {
    totalMemory: 0,
    modelMemory: 0,
    activationMemory: 0,
  };
};
```

## Pull Request Process

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] Self-review of your code
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated and passing
- [ ] No merge conflicts with master
- [ ] Commit history is clean

### Submitting a Pull Request

1. **Push your branch** to your fork
2. **Open a Pull Request** against the `master` branch
3. **Fill out the PR template** completely
4. **Link related issues** using keywords (fixes #123)
5. **Request reviews** from maintainers

**PR Title Format:**
```
[Type] Brief description of changes
```

Examples:
- `[Feature] Add support for INT4 quantization`
- `[Fix] Resolve memory overflow in large models`
- `[Docs] Update installation instructions`

**PR Description Template:**

```markdown
## Description
Brief description of what this PR does.

## Related Issues
Fixes #123
Relates to #456

## Changes Made
- Added feature X
- Fixed bug Y
- Updated documentation Z

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] All tests passing

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Documentation updated
- [ ] Tests passing
- [ ] No breaking changes (or documented)
```

### Code Review Process

1. **Maintainers review** your code
2. **Address feedback** by pushing new commits
3. **Keep discussion constructive** and professional
4. **Once approved**, a maintainer will merge your PR

**Review Timeline:**
- Initial review: Within 3-5 business days
- Follow-up reviews: Within 1-2 business days

## Testing Guidelines

### Backend Testing

```python
# backend/tests/test_memory.py
import pytest
from utils.memory import calculate_memory

def test_memory_calculation_fp16():
    """Test memory calculation for FP16 precision."""
    result = calculate_memory(
        model_params=7_000_000_000,  # 7B
        precision="fp16",
        batch_size=1,
        sequence_length=512
    )

    # FP16 = 2 bytes per parameter
    expected_model_memory = 7_000_000_000 * 2 / (1024**3)  # Convert to GB
    assert abs(result["model_memory"] - expected_model_memory) < 0.1
```

### Frontend Testing

```typescript
// frontend/__tests__/MemoryCalculator.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import MemoryCalculator from '@/components/MemoryCalculator';

describe('MemoryCalculator', () => {
  it('calculates memory correctly', async () => {
    render(<MemoryCalculator />);

    // Fill in form
    fireEvent.change(screen.getByLabelText('Model Parameters'), {
      target: { value: '7000000000' },
    });

    // Submit
    fireEvent.click(screen.getByText('Calculate'));

    // Assert result
    expect(await screen.findByText(/14 GB/)).toBeInTheDocument();
  });
});
```

## Documentation Guidelines

### Code Documentation

- **Python**: Use docstrings (Google or NumPy style)
- **TypeScript**: Use JSDoc comments
- **Complex logic**: Add inline comments explaining "why", not "what"

### Documentation Files

When updating documentation:
- Keep language clear and concise
- Use examples where helpful
- Update both English and Chinese versions (if applicable)
- Test all code examples

## Adding New Models

To add support for a new model:

1. Create a JSON configuration file in `backend/models/`
2. Follow this structure:

```json
{
  "name": "ModelName-Size",
  "parameters": 7000000000,
  "layers": 32,
  "hidden_size": 4096,
  "attention_heads": 32,
  "vocab_size": 32000,
  "architecture": "transformer"
}
```

3. Add tests for the new model
4. Update documentation

## Questions?

- **Documentation**: Check the [README](README.md)
- **Issues**: Search [existing issues](https://github.com/amazingchow/LLMToolset/issues)
- **Discussions**: Start a [discussion](https://github.com/amazingchow/LLMToolset/discussions)
- **Contact**: Open an issue with the `question` label

## Recognition

Contributors will be recognized in:
- The project README (if significant contribution)
- Release notes
- The GitHub contributors page

## License

By contributing to LLM Toolset, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to LLM Toolset! Your efforts help make AI development more accessible for everyone. 🚀
