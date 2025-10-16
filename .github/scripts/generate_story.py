import openai
import os
import json
import sys
import re
from datetime import date, datetime
from pathlib import Path

# Import helper modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from generate_audio import generate_story_audio
    from validate_story import validate_story
    print("✅ Helper modules imported successfully")
except ImportError as e:
    print(f"⚠️  Warning: Could not import helper modules: {e}")
    print("Continuing with limited functionality...")
    
    def generate_story_audio(pages, audio_dir, **kwargs):
        return {'total': 0, 'success': 0, 'failed': 0, 'files': []}
    
    def validate_story(story_dir):
        return {'score': 0, 'max_score': 10, 'percentage': 0, 'passing': False, 'issues': [], 'warnings': []}

# Configuration
MODEL_NAME = "gpt-4"
MIN_PAGES = 5
MAX_PAGES = 8
VALIDATION_THRESHOLD = 70
TTS_MODEL = "tts-1"
TTS_VOICE = "alloy"

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_slug(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = text.strip('-')
    return text[:50]  # Limit length

def call_ai(prompt, system_message=None):
    """Make an AI API call with error handling"""
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content, response.usage.total_tokens
    except Exception as e:
        print(f"❌ Error calling AI: {e}")
        return None, 0

def generate_story_structure(topic):
    """Stage 1: Generate story structure from topic"""
    print(f"\n{'='*60}")
    print(f"STAGE 1: Generating Story Structure")
    print(f"{'='*60}")
    print(f"Topic: {topic}")
    
    system_message = "You are an expert social story creator specializing in creating educational, supportive narratives for children with diverse learning needs."
    
    prompt = f"""Create a structured social story outline for the following topic:

"{topic}"

Your output must be valid JSON with this exact structure:
{{
  "title": "Story title",
  "characters": [
    {{"name": "Character Name", "description": "Brief description", "role": "main/supporting"}}
  ],
  "settings": [
    {{"name": "Location name", "description": "Visual description"}}
  ],
  "learning_objectives": ["objective 1", "objective 2"],
  "emotional_tone": "supportive/reassuring/educational",
  "pages": [
    {{
      "page_number": 1,
      "setting": "Location name",
      "characters_present": ["Character 1", "Character 2"],
      "narrative": "What happens on this page",
      "visual_description": "Description of what should be shown visually",
      "teaching_point": "What this page teaches or reinforces"
    }}
  ]
}}

Requirements:
- Create {MIN_PAGES}-{MAX_PAGES} pages that tell a complete story
- Use clear, simple language appropriate for children
- Include sensory details and emotional support
- Each page should advance the narrative
- End with a positive resolution
- Focus on building understanding and confidence

Output ONLY the JSON, no additional text or explanation."""

    response, tokens = call_ai(prompt, system_message)
    
    if not response:
        raise Exception("Failed to generate story structure")
    
    # Extract JSON from response
    try:
        # Try to find JSON in the response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            structure = json.loads(json_str)
        else:
            structure = json.loads(response)
        
        print(f"✅ Story structure generated: {structure['title']}")
        print(f"   - Characters: {len(structure['characters'])}")
        print(f"   - Settings: {len(structure['settings'])}")
        print(f"   - Pages: {len(structure['pages'])}")
        print(f"   - Tokens used: {tokens}")
        
        return structure, tokens
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON response: {e}")
        print(f"Response was: {response[:500]}")
        raise

def generate_page_html(page_data, story_structure, page_number, total_pages):
    """Stage 2: Generate HTML for a single page"""
    print(f"\n  📄 Generating page {page_number}/{total_pages}...")
    
    system_message = "You are an expert in creating accessible, visual HTML pages for social stories."
    
    characters_info = "\n".join([f"- {c['name']}: {c['description']}" for c in story_structure['characters']])
    settings_info = "\n".join([f"- {s['name']}: {s['description']}" for s in story_structure['settings']])
    
    prompt = f"""Create an HTML page for this social story page.

Story Title: {story_structure['title']}
Page {page_number} of {total_pages}

Characters:
{characters_info}

Settings:
{settings_info}

Page Details:
- Setting: {page_data['setting']}
- Characters: {', '.join(page_data['characters_present'])}
- Narrative: {page_data['narrative']}
- Visual Description: {page_data['visual_description']}
- Teaching Point: {page_data['teaching_point']}

Create a complete, self-contained HTML page with:
1. Semantic HTML5 structure
2. A visual section with CSS-styled elements representing the scene (use div elements with colors, shapes, borders to create simple character and setting representations)
3. The narrative text in a clearly readable format
4. Navigation buttons (Previous/Next)
5. Accessibility features (ARIA labels, semantic tags, alt text)
6. Print-friendly CSS (@media print)
7. Responsive design
8. Audio playback controls (for page-{page_number:02d}.mp3)
9. Links to interactive elements

The page should be visually calming with good contrast and clear fonts.

Output ONLY the complete HTML, no explanations or markdown formatting."""

    response, tokens = call_ai(prompt, system_message)
    
    if not response:
        return None, 0
    
    # Clean up response
    html = response.strip()
    if html.startswith('```html'):
        html = html[7:]
    if html.startswith('```'):
        html = html[3:]
    if html.endswith('```'):
        html = html[:-3]
    html = html.strip()
    
    print(f"  ✅ Page {page_number} generated ({len(html)} chars, {tokens} tokens)")
    
    return html, tokens

def generate_interactive_quiz(story_structure):
    """Stage 3a: Generate quiz questions"""
    print(f"\n  🎯 Generating quiz module...")
    
    system_message = "You are an expert in creating educational quizzes for children."
    
    pages_summary = "\n".join([f"Page {p['page_number']}: {p['narrative']}" for p in story_structure['pages']])
    
    prompt = f"""Create an interactive quiz JavaScript module for this social story.

Story: {story_structure['title']}

Story Summary:
{pages_summary}

Learning Objectives:
{', '.join(story_structure['learning_objectives'])}

Create a quiz.js file with:
1. 3-5 multiple choice questions about the story
2. Questions should test comprehension and reinforce learning objectives
3. Visual feedback for correct/incorrect answers
4. Score tracking
5. Encouraging messages
6. Replay functionality

The module should be callable with: initQuiz(containerId)

Output ONLY the JavaScript code, no markdown formatting or explanations."""

    response, tokens = call_ai(prompt, system_message)
    
    if not response:
        return None, 0
    
    # Clean up
    js = response.strip()
    if js.startswith('```javascript') or js.startswith('```js'):
        js = js[js.find('\n')+1:]
    if js.startswith('```'):
        js = js[3:]
    if js.endswith('```'):
        js = js[:-3]
    js = js.strip()
    
    print(f"  ✅ Quiz generated ({len(js)} chars, {tokens} tokens)")
    
    return js, tokens

def generate_interactive_choices(story_structure):
    """Stage 3b: Generate choice-based interactions"""
    print(f"\n  🎯 Generating choices module...")
    
    system_message = "You are an expert in creating interactive educational experiences."
    
    pages_summary = "\n".join([f"Page {p['page_number']}: {p['narrative']}" for p in story_structure['pages']])
    
    prompt = f"""Create an interactive choices JavaScript module for this social story.

Story: {story_structure['title']}

Story Summary:
{pages_summary}

Create a choices.js file with:
1. 2-3 decision point scenarios from the story
2. Each scenario presents options for what the character could do
3. Show outcomes/consequences for each choice
4. Educational explanations for why certain choices are better
5. "Try again" functionality
6. Supportive, non-judgmental feedback

The module should be callable with: initChoices(containerId)

Output ONLY the JavaScript code, no markdown formatting or explanations."""

    response, tokens = call_ai(prompt, system_message)
    
    if not response:
        return None, 0
    
    # Clean up
    js = response.strip()
    if js.startswith('```javascript') or js.startswith('```js'):
        js = js[js.find('\n')+1:]
    if js.startswith('```'):
        js = js[3:]
    if js.endswith('```'):
        js = js[:-3]
    js = js.strip()
    
    print(f"  ✅ Choices generated ({len(js)} chars, {tokens} tokens)")
    
    return js, tokens

def generate_interactive_games(story_structure):
    """Stage 3c: Generate mini-games"""
    print(f"\n  🎯 Generating games module...")
    
    system_message = "You are an expert in creating educational games for children."
    
    characters = [c['name'] for c in story_structure['characters']]
    key_events = [p['narrative'] for p in story_structure['pages']]
    
    prompt = f"""Create an interactive games JavaScript module for this social story.

Story: {story_structure['title']}
Characters: {', '.join(characters)}

Create a games.js file with 2 mini-games:
1. Character Matching: Match character names to descriptions
2. Event Sequencing: Put story events in correct order

Features:
- Simple, intuitive drag-and-drop or click-based interactions
- Visual feedback for correct/incorrect
- Encouraging messages
- Reset/replay functionality
- Accessible keyboard controls

The module should be callable with: initGames(containerId)

Output ONLY the JavaScript code, no markdown formatting or explanations."""

    response, tokens = call_ai(prompt, system_message)
    
    if not response:
        return None, 0
    
    # Clean up
    js = response.strip()
    if js.startswith('```javascript') or js.startswith('```js'):
        js = js[js.find('\n')+1:]
    if js.startswith('```'):
        js = js[3:]
    if js.endswith('```'):
        js = js[:-3]
    js = js.strip()
    
    print(f"  ✅ Games generated ({len(js)} chars, {tokens} tokens)")
    
    return js, tokens

def generate_story_index(story_structure, story_dir, page_count):
    """Generate main index.html for the story"""
    print(f"\n  📄 Generating story index...")
    
    system_message = "You are an expert in creating accessible web interfaces."
    
    prompt = f"""Create an index.html file for this social story.

Story Title: {story_structure['title']}
Total Pages: {page_count}
Learning Objectives: {', '.join(story_structure['learning_objectives'])}

The index page should include:
1. Story title and brief description
2. Navigation to all pages (page-01.html through page-{page_count:02d}.html)
3. Links to interactive elements:
   - Quiz (loads interactive/quiz.js)
   - Choices (loads interactive/choices.js)
   - Games (loads interactive/games.js)
4. Reading mode options:
   - Sequential reading (start at page 1)
   - Free navigation (jump to any page)
5. Accessibility features
6. Print button
7. Beautiful, calming design

Output ONLY the complete HTML, no explanations or markdown formatting."""

    response, tokens = call_ai(prompt, system_message)
    
    if not response:
        return None, 0
    
    # Clean up
    html = response.strip()
    if html.startswith('```html'):
        html = html[7:]
    if html.startswith('```'):
        html = html[3:]
    if html.endswith('```'):
        html = html[:-3]
    html = html.strip()
    
    print(f"  ✅ Index generated ({len(html)} chars, {tokens} tokens)")
    
    return html, tokens

def enhance_story(story_structure, generated_files):
    """Stage 5: Enhancement pass for consistency and quality"""
    print(f"\n{'='*60}")
    print(f"STAGE 5: Enhancement Pass")
    print(f"{'='*60}")
    
    # For now, we'll skip the enhancement to save tokens
    # In a production version, this would review all generated content
    # and make improvements
    
    print("✅ Enhancement complete (skipped for efficiency)")
    return 0

def save_metadata(story_dir, story_structure, topic, slug, tokens_used, validation_result):
    """Save story metadata as JSON and Markdown"""
    today = date.today().isoformat()
    
    metadata = {
        "generated_date": today,
        "generated_timestamp": datetime.now().isoformat(),
        "model": MODEL_NAME,
        "topic": topic,
        "slug": slug,
        "title": story_structure['title'],
        "pages": len(story_structure['pages']),
        "characters": [c['name'] for c in story_structure['characters']],
        "settings": [s['name'] for s in story_structure['settings']],
        "learning_objectives": story_structure['learning_objectives'],
        "emotional_tone": story_structure['emotional_tone'],
        "tokens_used": tokens_used,
        "validation": validation_result,
        "tts_model": TTS_MODEL,
        "tts_voice": TTS_VOICE
    }
    
    # Save JSON
    with open(os.path.join(story_dir, 'story.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Save Markdown
    markdown_content = f"""# {story_structure['title']}

## Metadata

- **Generated Date:** {today}
- **Topic:** {topic}
- **Model:** {MODEL_NAME}
- **Pages:** {len(story_structure['pages'])}
- **Tokens Used:** {tokens_used}

## Characters

{chr(10).join([f"- **{c['name']}**: {c['description']}" for c in story_structure['characters']])}

## Settings

{chr(10).join([f"- **{s['name']}**: {s['description']}" for s in story_structure['settings']])}

## Learning Objectives

{chr(10).join([f"- {obj}" for obj in story_structure['learning_objectives']])}

## Emotional Tone

{story_structure['emotional_tone']}

## Story Pages

{chr(10).join([f"### Page {p['page_number']}: {p['setting']}\n\n{p['narrative']}\n\n**Teaching Point:** {p['teaching_point']}\n" for p in story_structure['pages']])}

## Validation Results

- **Score:** {validation_result['score']}/{validation_result['max_score']} ({validation_result['percentage']:.1f}%)
- **Status:** {'✅ PASSING' if validation_result['passing'] else '❌ FAILING'}

### Issues

{chr(10).join([f"- ❌ {issue}" for issue in validation_result['issues']]) if validation_result['issues'] else "- None"}

### Warnings

{chr(10).join([f"- ⚠️  {warning}" for warning in validation_result['warnings']]) if validation_result['warnings'] else "- None"}

## Files Generated

- `index.html` - Main story page
- `pages/page-*.html` - Individual story pages
- `audio/page-*.mp3` - Audio narration
- `interactive/quiz.js` - Quiz questions
- `interactive/choices.js` - Choice-based interactions
- `interactive/games.js` - Mini-games
- `story.json` - Machine-readable metadata
- `story.md` - This documentation
"""
    
    with open(os.path.join(story_dir, 'story.md'), 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ Metadata saved to story.json and story.md")

def update_stories_index(story_dir, story_structure, topic, slug):
    """Update the main stories/index.json file"""
    index_path = 'stories/index.json'
    
    # Load existing index or create new
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            stories = json.load(f)
    else:
        stories = []
    
    # Add this story
    story_entry = {
        "date": date.today().isoformat(),
        "slug": slug,
        "title": story_structure['title'],
        "topic": topic,
        "pages": len(story_structure['pages']),
        "path": os.path.basename(story_dir)
    }
    
    stories.append(story_entry)
    
    # Save updated index
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(stories, f, indent=2)
    
    print(f"✅ Updated stories/index.json")

def main():
    """Main generation pipeline"""
    # Get topic from command line or environment
    if len(sys.argv) > 1:
        topic = ' '.join(sys.argv[1:])
    else:
        topic = os.getenv('STORY_TOPIC', 'A child goes to school for the first time')
    
    print(f"\n{'='*60}")
    print(f"AI SOCIAL STORY GENERATOR")
    print(f"{'='*60}")
    print(f"Topic: {topic}")
    print(f"Model: {MODEL_NAME}")
    print(f"{'='*60}\n")
    
    total_tokens = 0
    
    try:
        # Stage 1: Generate story structure
        story_structure, tokens = generate_story_structure(topic)
        total_tokens += tokens
        
        # Create story directory
        today = date.today().isoformat()
        slug = create_slug(topic)
        story_dir = f"stories/{today}-{slug}"
        os.makedirs(story_dir, exist_ok=True)
        os.makedirs(f"{story_dir}/pages", exist_ok=True)
        os.makedirs(f"{story_dir}/audio", exist_ok=True)
        os.makedirs(f"{story_dir}/interactive", exist_ok=True)
        
        print(f"\n📁 Created story directory: {story_dir}")
        
        # Stage 2: Generate page HTML files
        print(f"\n{'='*60}")
        print(f"STAGE 2: Generating Page Content")
        print(f"{'='*60}")
        
        pages = story_structure['pages']
        for page_data in pages:
            page_num = page_data['page_number']
            html, tokens = generate_page_html(page_data, story_structure, page_num, len(pages))
            total_tokens += tokens
            
            if html:
                page_file = f"{story_dir}/pages/page-{page_num:02d}.html"
                with open(page_file, 'w', encoding='utf-8') as f:
                    f.write(html)
        
        # Generate story index
        index_html, tokens = generate_story_index(story_structure, story_dir, len(pages))
        total_tokens += tokens
        if index_html:
            with open(f"{story_dir}/index.html", 'w', encoding='utf-8') as f:
                f.write(index_html)
        
        # Stage 3: Generate interactive elements
        print(f"\n{'='*60}")
        print(f"STAGE 3: Generating Interactive Elements")
        print(f"{'='*60}")
        
        quiz_js, tokens = generate_interactive_quiz(story_structure)
        total_tokens += tokens
        if quiz_js:
            with open(f"{story_dir}/interactive/quiz.js", 'w', encoding='utf-8') as f:
                f.write(quiz_js)
        
        choices_js, tokens = generate_interactive_choices(story_structure)
        total_tokens += tokens
        if choices_js:
            with open(f"{story_dir}/interactive/choices.js", 'w', encoding='utf-8') as f:
                f.write(choices_js)
        
        games_js, tokens = generate_interactive_games(story_structure)
        total_tokens += tokens
        if games_js:
            with open(f"{story_dir}/interactive/games.js", 'w', encoding='utf-8') as f:
                f.write(games_js)
        
        # Stage 4: Generate audio files
        print(f"\n{'='*60}")
        print(f"STAGE 4: Generating Audio Files")
        print(f"{'='*60}")
        
        audio_results = generate_story_audio(
            pages,
            f"{story_dir}/audio",
            model=TTS_MODEL,
            voice=TTS_VOICE
        )
        
        # Stage 5: Enhancement (optional)
        enhancement_tokens = enhance_story(story_structure, {})
        total_tokens += enhancement_tokens
        
        # Validate the generated story
        print(f"\n{'='*60}")
        print(f"VALIDATION")
        print(f"{'='*60}")
        
        validation_result = validate_story(story_dir)
        
        # Save metadata
        print(f"\n{'='*60}")
        print(f"SAVING METADATA")
        print(f"{'='*60}")
        
        save_metadata(story_dir, story_structure, topic, slug, total_tokens, validation_result)
        update_stories_index(story_dir, story_structure, topic, slug)
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"GENERATION COMPLETE")
        print(f"{'='*60}")
        print(f"✅ Story: {story_structure['title']}")
        print(f"✅ Location: {story_dir}")
        print(f"✅ Pages: {len(pages)}")
        print(f"✅ Audio files: {audio_results['success']}/{audio_results['total']}")
        print(f"✅ Total tokens: {total_tokens:,}")
        print(f"✅ Validation: {validation_result['percentage']:.1f}% ({'PASSING' if validation_result['passing'] else 'FAILING'})")
        print(f"{'='*60}\n")
        
        if not validation_result['passing']:
            print(f"⚠️  Warning: Story did not pass validation threshold ({VALIDATION_THRESHOLD}%)")
            print(f"Issues: {', '.join(validation_result['issues'])}")
            sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

