import openai
import os
from pathlib import Path

def generate_audio_file(text, output_path, model="tts-1", voice="alloy"):
    """
    Generate audio file from text using OpenAI TTS API
    
    Args:
        text: The text to convert to speech
        output_path: Path where the MP3 file should be saved
        model: TTS model to use (default: "tts-1")
        voice: Voice to use (default: "alloy")
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        print(f"🔊 Generating audio: {os.path.basename(output_path)}")
        
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the audio file
        response.stream_to_file(output_path)
        
        print(f"✅ Audio generated: {os.path.basename(output_path)}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating audio for {os.path.basename(output_path)}: {e}")
        return False

def generate_story_audio(pages, audio_dir, model="tts-1", voice="alloy"):
    """
    Generate audio files for all pages in a story
    
    Args:
        pages: List of page dictionaries with 'narration' text
        audio_dir: Directory where audio files should be saved
        model: TTS model to use
        voice: Voice to use
    
    Returns:
        dict: Results with success/failure counts and file paths
    """
    results = {
        'total': len(pages),
        'success': 0,
        'failed': 0,
        'files': []
    }
    
    print(f"\n🔊 Generating audio for {len(pages)} pages...")
    
    for i, page in enumerate(pages, 1):
        page_num = f"{i:02d}"
        output_path = os.path.join(audio_dir, f"page-{page_num}.mp3")
        
        # Get narration text from page
        narration = page.get('narration', '')
        
        if not narration:
            print(f"⚠️  No narration text for page {page_num}, skipping audio generation")
            results['failed'] += 1
            continue
        
        # Generate audio file
        success = generate_audio_file(narration, output_path, model, voice)
        
        if success:
            results['success'] += 1
            results['files'].append(output_path)
        else:
            results['failed'] += 1
    
    print(f"\n🔊 Audio Generation Complete:")
    print(f"   ✅ Success: {results['success']}/{results['total']}")
    print(f"   ❌ Failed: {results['failed']}/{results['total']}")
    
    return results

def extract_narration_from_html(html_content):
    """
    Extract narration text from HTML page content
    
    Args:
        html_content: HTML string
    
    Returns:
        str: Extracted narration text
    """
    import re
    
    # Look for text in narration-text class
    narration_pattern = r'<div class="narration-text"[^>]*>(.*?)</div>'
    matches = re.findall(narration_pattern, html_content, re.DOTALL)
    
    if matches:
        # Strip HTML tags and clean up
        text = matches[0]
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text.strip()
    
    # Fallback: extract all paragraph text
    p_pattern = r'<p[^>]*>(.*?)</p>'
    p_matches = re.findall(p_pattern, html_content, re.DOTALL)
    
    if p_matches:
        text = ' '.join(p_matches)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    return ""

