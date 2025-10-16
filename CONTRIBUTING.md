# Contributing to AI Social Stories Generator

Thank you for your interest in contributing! This project aims to make personalized, accessible social stories available to everyone.

## Ways to Contribute

### 1. Report Issues

Found a bug or have a suggestion?
- Check if the issue already exists
- Create a new issue with:
  - Clear description
  - Steps to reproduce (for bugs)
  - Expected vs actual behavior
  - Screenshots if applicable

### 2. Improve Documentation

- Fix typos or unclear instructions
- Add examples or use cases
- Translate documentation
- Create video tutorials

### 3. Add Features

Some ideas for contributions:
- New interactive game types
- Additional language support
- PDF export functionality
- Custom character builder
- Progress tracking system
- Offline PWA support
- Alternative TTS providers

### 4. Improve Story Quality

- Refine AI prompts for better stories
- Add validation checks
- Improve accessibility features
- Enhance visual styling

### 5. Share Stories

- Share example stories you've created
- Provide feedback on generated content
- Suggest new story topics

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/social-stories-generator.git
   cd social-stories-generator
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. Make your changes

6. Test your changes:
   ```bash
   # Test generation
   export OPENAI_API_KEY="your-key"
   python .github/scripts/generate_story.py "Test story topic"
   
   # Test validation
   python .github/scripts/validate_story.py
   ```

7. Commit with clear messages:
   ```bash
   git add .
   git commit -m "Add feature: description of what you added"
   ```

8. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

9. Create a Pull Request

## Code Style

### Python
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Include error handling
- Add comments for complex logic

### JavaScript
- Use ES6+ features
- Use meaningful variable names
- Add JSDoc comments for functions
- Handle errors gracefully
- Ensure accessibility

### HTML/CSS
- Use semantic HTML5
- Include ARIA labels
- Ensure responsive design
- Follow BEM naming convention for CSS classes
- Test with screen readers

## Testing Guidelines

Before submitting a PR:

1. **Test story generation**
   - Generate at least 2 test stories
   - Verify all files are created
   - Check validation passes

2. **Test UI**
   - Browse stories in the web interface
   - Test on mobile and desktop
   - Check keyboard navigation
   - Test with screen reader

3. **Test interactive elements**
   - Try quiz questions
   - Test choice interactions
   - Play mini-games

4. **Check accessibility**
   - Run automated accessibility tests
   - Test keyboard-only navigation
   - Verify ARIA labels
   - Check color contrast

## Pull Request Guidelines

### PR Title Format
```
Type: Brief description

Examples:
- Feature: Add memory game to interactive elements
- Fix: Resolve audio playback on iOS
- Docs: Update setup instructions
- Style: Improve mobile responsive design
```

### PR Description Template
```markdown
## What does this PR do?
Brief description of changes

## Why is this needed?
Problem this solves or feature it adds

## How was it tested?
- [ ] Local testing
- [ ] Generated test stories
- [ ] Tested on mobile
- [ ] Checked accessibility

## Screenshots/Examples
If applicable

## Related Issues
Closes #123
```

### Review Process
- Maintainers will review within 3-5 days
- Address feedback promptly
- Keep PRs focused and small when possible
- Be patient and respectful

## AI Prompt Engineering

If modifying AI prompts:

1. **Be specific**: Clear, detailed instructions work best
2. **Structure output**: Request JSON or specific formats
3. **Include examples**: Show what you want
4. **Set constraints**: Specify limits and requirements
5. **Test thoroughly**: Try with multiple topics
6. **Document changes**: Explain why prompts were changed

### Example Prompt Improvement

**Before:**
```python
prompt = "Create a social story about going to the dentist"
```

**After:**
```python
prompt = """Create a social story about going to the dentist.

Requirements:
- 5-6 pages
- Include main character, parent, dentist
- Focus on reducing anxiety
- Include sensory details
- End with positive outcome

Output as JSON with structure: {...}
"""
```

## Validation Rules

When adding validation checks:

1. Make checks meaningful
2. Provide clear error messages
3. Give suggestions for fixes
4. Don't make rules too strict
5. Test with various story types

## Interactive Elements

When creating new interactive features:

1. Keep it simple for children
2. Provide visual feedback
3. Include encouraging messages
4. Make it keyboard accessible
5. Test with various story content
6. Add clear instructions

## Community Guidelines

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn
- Share knowledge generously
- Follow the code of conduct

## Questions?

- Open an issue for discussion
- Tag maintainers for guidance
- Check existing documentation
- Review similar projects

## Recognition

Contributors will be:
- Listed in the README
- Credited in release notes
- Appreciated by the community

Thank you for contributing! 🎉

