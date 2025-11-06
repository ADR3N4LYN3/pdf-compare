# Contributing to pdf-compare

Thank you for your interest in contributing to pdf-compare! This document provides guidelines and instructions for contributing.

## Getting Started

### Development Setup

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/ADR3N4LYN3/pdf-compare.git
   cd pdf-compare
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Verify installation**

   ```bash
   pdf-compare --version
   pytest
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Update tests if needed

3. **Test your changes**

   ```bash
   # Run all tests
   pytest

   # Run tests with coverage
   pytest --cov=pdf_compare

   # Run specific test file
   pytest tests/test_comparator.py -v
   ```

4. **Format your code**

   ```bash
   # Auto-format with black
   black src/

   # Check for linting issues
   flake8 src/

   # Type checking
   mypy src/
   ```

### Commit Guidelines

Use clear, descriptive commit messages:

```
Add feature to compare PDF annotations

- Implement annotation extraction
- Add tests for annotation comparison
- Update documentation
```

Commit message format:
- First line: Brief summary (50 chars max)
- Blank line
- Detailed description if needed

## Code Standards

### Python Style

- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use meaningful variable names

**Good:**
```python
def calculate_similarity_percentage(self, img1: Image.Image, img2: Image.Image) -> float:
    """Calculate the percentage of similarity between two images"""
    total_pixels = img1.width * img1.height * 3
    return ((total_pixels - diff_pixels) / total_pixels) * 100
```

**Bad:**
```python
def calc(i1, i2):
    t = i1.width * i1.height * 3
    return ((t - d) / t) * 100
```

### Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Update README.md for user-facing changes

**Example:**
```python
def compare_images(self, img1: Image.Image, img2: Image.Image) -> Tuple[bool, Image.Image, int]:
    """
    Compare two images and generate a diff image

    Args:
        img1: First image
        img2: Second image

    Returns:
        Tuple of (are_identical, diff_image, diff_pixel_count)

    Raises:
        ValueError: If images have different dimensions
    """
```

### Testing

- Write tests for new features
- Maintain or improve code coverage
- Test edge cases and error conditions

**Test structure:**
```python
class TestNewFeature:
    """Tests for new feature"""

    def test_basic_functionality(self):
        """Test basic use case"""
        # Arrange
        comparator = PDFComparator()

        # Act
        result = comparator.new_feature()

        # Assert
        assert result is not None
```

## Pull Request Process

1. **Update documentation**
   - Update README.md if adding features
   - Add docstrings to new code
   - Update CHANGELOG.md (if exists)

2. **Ensure tests pass**
   ```bash
   pytest
   black src/ --check
   flake8 src/
   ```

3. **Submit pull request**
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes (if applicable)

4. **Respond to feedback**
   - Address review comments
   - Make requested changes
   - Keep discussion professional and constructive

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

## Areas for Contribution

### High Priority

- Text-based comparison mode
- Performance optimizations for large PDFs
- Better error messages and handling
- Additional output formats

### Features

- Annotation comparison
- Side-by-side visual comparison
- Web interface
- Docker container
- CI/CD integration examples

### Documentation

- Video tutorials
- More usage examples
- API reference documentation
- Troubleshooting guide

### Testing

- Integration tests
- Performance benchmarks
- Cross-platform testing
- Edge case coverage

## Bug Reports

### Before Submitting

1. Check if the bug is already reported
2. Test with the latest version
3. Verify it's not a configuration issue

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
1. Run command '...'
2. With these files '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.11.0]
- pdf-compare version: [e.g., 1.0.0]

**Additional Context**
Screenshots, error logs, etc.
```

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature is already requested
2. Describe the use case clearly
3. Explain why it would be useful
4. Consider submitting a PR to implement it

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How could this be implemented?

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Examples, mockups, etc.
```

## Code Review Process

### For Reviewers

- Be constructive and respectful
- Explain *why* changes are needed
- Acknowledge good practices
- Test the changes locally

### For Contributors

- Don't take feedback personally
- Ask questions if unclear
- Make requested changes promptly
- Update the PR description if scope changes

## Release Process

(For maintainers)

1. Update version in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG.md
3. Create release branch: `release/vX.Y.Z`
4. Build and test packages
5. Merge to main and tag release
6. Publish to PyPI
7. Create GitHub release with notes

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on what's best for the project
- Show empathy towards others

### Communication

- GitHub Issues: Bug reports and feature requests
- Pull Requests: Code contributions
- Discussions: General questions and ideas

## Questions?

If you have questions about contributing:

1. Check existing issues and documentation
2. Open a GitHub Discussion
3. Tag your issue with "question"

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to pdf-compare! 🎉
