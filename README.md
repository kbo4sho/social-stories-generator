# AI Social Stories Generator

An automated system for generating personalized, interactive social stories using AI. Stories are created from simple text prompts and include multiple pages with visual descriptions, interactive elements, audio narration, and print-friendly layouts.

## Features

- **Simple Input**: Generate stories from plain text prompts (e.g., "Geo is going to the dentist with his mom")
- **Multi-Page Stories**: Structured narratives with 5-8 pages including characters, settings, and learning objectives
- **Interactive Elements**: 
  - Quiz questions about story events
  - Choice-based decision points
  - Mini-games (matching, sequencing, memory)
- **Accessibility**:
  - Read mode with visual descriptions
  - Listen mode with pre-generated audio and browser TTS
  - Print-friendly layouts
  - Keyboard navigation
  - ARIA labels and semantic HTML
- **Automated Generation**: GitHub Actions workflow handles entire creation process
- **Browse Interface**: View all generated stories in a card-based gallery

## How It Works

### Generation Process

1. **Story Structure**: AI creates a structured outline with characters, settings, and page-by-page narrative
2. **Page Content**: Each page is generated with HTML, visual descriptions, and narrative text
3. **Interactive Elements**: Quiz questions, choice points, and mini-games are created based on story content
4. **Audio Generation**: Text-to-speech audio files are generated for each page using OpenAI TTS API
5. **Enhancement**: Final pass improves visual descriptions, interactions, and consistency

### Quality Validation

Each story is automatically validated for:
- Story completeness (all pages generated)
- HTML validity and accessibility features
- Interactive elements functionality
- Audio files presence and validity
- Text readability
- Character consistency
- Navigation elements
- Print-friendly CSS

Stories must score 70% or higher to be published.

## Usage

### Generate a New Story

1. Go to the **Actions** tab in GitHub
2. Select **Generate Social Story** workflow
3. Click **Run workflow**
4. Enter a story topic (e.g., "Maya goes to the grocery store with dad")
5. Click **Run workflow** button

The system will:
- Generate the complete story with all pages
- Create interactive elements
- Generate audio files
- Validate quality
- Commit to repository
- Deploy to GitHub Pages

### View Stories

Visit the GitHub Pages site to browse and read all generated stories:
- Browse: `https://[username].github.io/social-stories-generator/`
- Story: `https://[username].github.io/social-stories-generator/stories/[date]-[slug]/`

## Project Structure

```
social-stories-generator/
├── .github/
│   ├── workflows/
│   │   └── generate_story.yml          # GitHub Action workflow
│   └── scripts/
│       ├── generate_story.py            # Main generation script
│       ├── generate_audio.py            # Audio file generation
│       └── validate_story.py            # Quality validation
├── stories/
│   ├── [date]-[slug]/                   # Each story folder
│   │   ├── index.html                   # Main story page
│   │   ├── pages/                       # Individual pages
│   │   ├── audio/                       # Audio files
│   │   ├── interactive/                 # Quiz, choices, games
│   │   ├── story.json                   # Metadata
│   │   └── story.md                     # Documentation
│   └── index.json                       # List of all stories
├── index.html                           # Browse UI
├── viewer.html                          # Story viewer template
├── shared/
│   ├── styles.css                       # Common styles
│   └── reader.js                        # TTS and playback logic
└── README.md
```

## Configuration

### Environment Variables

Set these as GitHub Secrets:
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Configuration Options

In `.github/scripts/generate_story.py`:
- `MODEL_NAME`: OpenAI model to use (default: "GPT-5")
- `MIN_PAGES`: Minimum story pages (default: 5)
- `MAX_PAGES`: Maximum story pages (default: 8)
- `VALIDATION_THRESHOLD`: Minimum quality score % (default: 70)
- `TTS_MODEL`: Text-to-speech model (default: "tts-1")
- `TTS_VOICE`: Voice for audio generation (default: "alloy")

## Development

### Local Testing

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install openai
   ```
3. Set environment variable:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```
4. Run generation script:
   ```bash
   cd .github/scripts
   python generate_story.py "Your story topic here"
   ```

### Story Structure

Each story is self-contained with:
- **index.html**: Main entry point with navigation
- **pages/**: Individual HTML pages (page-01.html, page-02.html, etc.)
- **audio/**: MP3 narration for each page
- **interactive/**: JavaScript modules for interactions
- **story.json**: Metadata and generation details
- **story.md**: Human-readable documentation

## Cost Efficiency

Each story generation costs approximately:
- Structure generation: ~$0.05
- Page content: ~$0.10 - $0.20
- Interactive elements: ~$0.05
- Audio generation: ~$0.10 - $0.20
- Enhancement: ~$0.05

**Total: $0.35 - $0.55 per story**

## Roadmap

- [ ] Add more interactive game types
- [ ] Support for multiple languages
- [ ] Custom character creation
- [ ] Parent/educator customization options
- [ ] Progress tracking for learners
- [ ] Export to PDF functionality
- [ ] Offline PWA support

## License

MIT License - See LICENSE file for details

## Credits

Built using:
- OpenAI GPT-5 for story generation
- OpenAI TTS API for audio narration
- GitHub Actions for automation
- GitHub Pages for hosting

