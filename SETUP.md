# Setup Guide - AI Social Stories Generator

This guide will help you set up and deploy your own Social Stories Generator.

## Prerequisites

- GitHub account
- OpenAI API key (sign up at https://platform.openai.com)
- Basic understanding of GitHub Actions

## Step-by-Step Setup

### 1. Create a New GitHub Repository

1. Go to GitHub and create a new repository
2. Name it `social-stories-generator` (or your preferred name)
3. Make it public (required for GitHub Pages)
4. Don't initialize with README (we already have one)

### 2. Push This Code to Your Repository

```bash
cd /path/to/social-stories-generator
git remote add origin https://github.com/YOUR-USERNAME/social-stories-generator.git
git branch -M main
git push -u origin main
```

### 3. Configure GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

### 4. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select **Deploy from a branch**
3. Select branch: **main**
4. Select folder: **/ (root)**
5. Click **Save**

Your site will be available at: `https://YOUR-USERNAME.github.io/social-stories-generator/`

### 5. Configure GitHub Actions Permissions

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select **Read and write permissions**
3. Check **Allow GitHub Actions to create and approve pull requests**
4. Click **Save**

## Generating Your First Story

### Using GitHub Actions (Recommended)

1. Go to the **Actions** tab in your repository
2. Select **Generate Social Story** workflow
3. Click **Run workflow**
4. Enter a story topic, for example:
   - "Emma goes to the dentist with her dad"
   - "Alex learns to ride the school bus"
   - "Maya visits the library for the first time"
5. Click **Run workflow** button
6. Wait 2-5 minutes for the workflow to complete
7. View your story at the GitHub Pages URL

### Using Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/social-stories-generator.git
   cd social-stories-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. Generate a story:
   ```bash
   python .github/scripts/generate_story.py "Your story topic here"
   ```

5. View the generated story:
   ```bash
   open stories/2025-XX-XX-your-story-slug/index.html
   ```

## Customization

### Changing AI Model

Edit `.github/scripts/generate_story.py`:

```python
MODEL_NAME = "gpt-4"  # Change to "gpt-4-turbo" or "gpt-3.5-turbo"
```

### Adjusting Story Length

Edit `.github/scripts/generate_story.py`:

```python
MIN_PAGES = 5  # Minimum pages
MAX_PAGES = 8  # Maximum pages
```

### Changing Voice for Audio

Edit `.github/scripts/generate_story.py`:

```python
TTS_VOICE = "alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer
```

### Modifying Validation Threshold

Edit `.github/scripts/generate_story.py`:

```python
VALIDATION_THRESHOLD = 70  # Percentage required to pass (0-100)
```

## Troubleshooting

### Workflow Fails with "Permission denied"

- Ensure you've enabled **Read and write permissions** in Actions settings
- Check that your `OPENAI_API_KEY` secret is set correctly

### Stories Don't Appear on Website

- Wait a few minutes for GitHub Pages to rebuild
- Check that GitHub Pages is enabled and pointing to the correct branch
- Clear your browser cache

### Audio Files Not Generated

- Verify your OpenAI API key has access to the TTS API
- Check the workflow logs for specific error messages
- TTS API may have rate limits - wait a few minutes and try again

### Validation Fails

- Review the validation errors in the workflow logs
- Lower the `VALIDATION_THRESHOLD` if needed
- Check that all required files are being generated

## Cost Considerations

Each story generation typically costs:
- **Structure**: ~$0.05
- **Pages (5-8)**: ~$0.10-$0.20
- **Interactive elements**: ~$0.05
- **Audio (5-8 files)**: ~$0.10-$0.20
- **Enhancement**: ~$0.05

**Total per story: $0.35-$0.55**

For 100 stories: approximately $35-$55

### Reducing Costs

1. Use `gpt-3.5-turbo` instead of `gpt-4` (10x cheaper)
2. Skip the enhancement pass
3. Generate fewer pages (MIN_PAGES = 3)
4. Use `tts-1` model (cheaper than `tts-1-hd`)

## Next Steps

- Generate your first story
- Share the GitHub Pages link with educators, parents, or therapists
- Customize the prompts in `generate_story.py` for your specific needs
- Add custom styling to `shared/styles.css`
- Create additional interactive game types

## Support

For issues and questions:
- Check the GitHub Issues page
- Review the main README.md
- Consult the OpenAI API documentation

## License

MIT License - See LICENSE file for details

