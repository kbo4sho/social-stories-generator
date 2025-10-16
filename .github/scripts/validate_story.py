import os
import json
import glob
import re

def validate_story(story_dir):
    """
    Validate a generated social story for completeness and quality
    
    Args:
        story_dir: Path to the story directory
    
    Returns:
        dict: Validation results with score, issues, warnings
    """
    issues = []
    warnings = []
    score = 0
    max_score = 10
    
    story_name = os.path.basename(story_dir)
    print(f"\n🔍 Validating story: {story_name}...")
    
    # 1. Story Structure Completeness (2 points)
    required_files = ['index.html', 'story.json', 'story.md']
    required_dirs = ['pages', 'audio', 'interactive']
    
    structure_complete = True
    for file in required_files:
        if not os.path.exists(os.path.join(story_dir, file)):
            issues.append(f"Missing required file: {file}")
            structure_complete = False
            print(f"❌ Missing required file: {file}")
    
    for dir in required_dirs:
        if not os.path.exists(os.path.join(story_dir, dir)):
            issues.append(f"Missing required directory: {dir}")
            structure_complete = False
            print(f"❌ Missing required directory: {dir}")
    
    if structure_complete:
        score += 2
        print(f"✅ Story structure complete")
    
    # 2. Page Generation (2 points)
    pages_dir = os.path.join(story_dir, 'pages')
    page_files = glob.glob(os.path.join(pages_dir, 'page-*.html'))
    
    if len(page_files) >= 5:
        score += 2
        print(f"✅ Sufficient pages generated: {len(page_files)}")
    elif len(page_files) >= 3:
        score += 1
        warnings.append(f"Only {len(page_files)} pages generated (recommended: 5-8)")
        print(f"⚠️  Only {len(page_files)} pages generated")
    else:
        issues.append(f"Insufficient pages: {len(page_files)} (minimum: 3)")
        print(f"❌ Insufficient pages: {len(page_files)}")
    
    # 3. Accessibility Features (2 points)
    accessibility_score = 0
    sample_pages = page_files[:min(3, len(page_files))]
    
    for page_file in sample_pages:
        try:
            with open(page_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for ARIA labels
            if 'aria-label' in content or 'role=' in content:
                accessibility_score += 0.3
            
            # Check for semantic HTML
            if '<nav' in content and '<main' in content:
                accessibility_score += 0.3
            
            # Check for alt text or descriptions
            if 'alt=' in content or 'aria-describedby' in content:
                accessibility_score += 0.4
        except:
            pass
    
    if accessibility_score >= 1.5:
        score += 2
        print(f"✅ Good accessibility features")
    elif accessibility_score >= 0.8:
        score += 1
        warnings.append("Limited accessibility features found")
        print(f"⚠️  Limited accessibility features")
    else:
        issues.append("Insufficient accessibility features")
        print(f"❌ Insufficient accessibility features")
    
    # 4. Interactive Elements (2 points)
    interactive_dir = os.path.join(story_dir, 'interactive')
    interactive_files = ['quiz.js', 'choices.js', 'games.js']
    interactive_found = 0
    
    for file in interactive_files:
        file_path = os.path.join(interactive_dir, file)
        if os.path.exists(file_path):
            # Check if file has actual content (not just empty)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if len(content.strip()) > 100:  # At least 100 chars
                    interactive_found += 1
            except:
                pass
    
    if interactive_found >= 3:
        score += 2
        print(f"✅ All interactive elements present")
    elif interactive_found >= 2:
        score += 1
        warnings.append(f"Only {interactive_found}/3 interactive elements found")
        print(f"⚠️  Only {interactive_found}/3 interactive elements")
    else:
        issues.append(f"Insufficient interactive elements: {interactive_found}/3")
        print(f"❌ Insufficient interactive elements: {interactive_found}/3")
    
    # 5. Audio Files (2 points)
    audio_dir = os.path.join(story_dir, 'audio')
    audio_files = glob.glob(os.path.join(audio_dir, 'page-*.mp3'))
    
    # Audio should match number of pages
    expected_audio = len(page_files)
    audio_coverage = len(audio_files) / expected_audio if expected_audio > 0 else 0
    
    if audio_coverage >= 0.9:  # At least 90% of pages have audio
        score += 2
        print(f"✅ Audio files complete: {len(audio_files)}/{expected_audio}")
    elif audio_coverage >= 0.5:
        score += 1
        warnings.append(f"Incomplete audio: {len(audio_files)}/{expected_audio} pages")
        print(f"⚠️  Incomplete audio: {len(audio_files)}/{expected_audio}")
    else:
        issues.append(f"Insufficient audio files: {len(audio_files)}/{expected_audio} pages")
        print(f"❌ Insufficient audio files: {len(audio_files)}/{expected_audio}")
    
    # 6. Navigation Elements (1 point)
    index_path = os.path.join(story_dir, 'index.html')
    has_navigation = False
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        # Check for navigation elements
        nav_patterns = ['<nav', 'page-nav', 'btn-next', 'btn-prev', 'navigation']
        if any(pattern in index_content for pattern in nav_patterns):
            has_navigation = True
            score += 1
            print(f"✅ Navigation elements present")
    except:
        pass
    
    if not has_navigation:
        warnings.append("No navigation elements found in index.html")
        print(f"⚠️  No navigation elements found")
    
    # 7. Print-Friendly CSS (1 point)
    has_print_css = False
    
    for page_file in sample_pages[:1]:  # Check first page
        try:
            with open(page_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '@media print' in content or 'print.css' in content:
                has_print_css = True
                score += 1
                print(f"✅ Print-friendly CSS detected")
                break
        except:
            pass
    
    if not has_print_css:
        warnings.append("No print-friendly CSS detected")
        print(f"⚠️  No print-friendly CSS detected")
    
    # Calculate percentage
    percentage = (score / max_score) * 100
    passing = percentage >= 70
    
    print(f"\n🔍 Validation Score: {score}/{max_score} ({percentage:.1f}%)")
    print(f"Status: {'✅ PASSING' if passing else '❌ FAILING'}")
    
    return {
        'score': score,
        'max_score': max_score,
        'percentage': percentage,
        'passing': passing,
        'issues': issues,
        'warnings': warnings,
        'details': {
            'pages_found': len(page_files),
            'audio_files': len(audio_files),
            'interactive_elements': interactive_found,
            'has_navigation': has_navigation,
            'has_print_css': has_print_css
        }
    }

def validate_all_stories():
    """Validate all stories in the stories directory"""
    print("🔍 Validating all stories...")
    
    story_dirs = sorted(glob.glob("stories/2*"))
    
    if not story_dirs:
        print("No story directories found!")
        return
    
    results = {}
    total_score = 0
    passing_stories = 0
    
    for story_dir in story_dirs:
        result = validate_story(story_dir)
        story_name = os.path.basename(story_dir)
        results[story_name] = result
        total_score += result['percentage']
        
        if result['passing']:
            passing_stories += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"VALIDATION SUMMARY")
    print(f"{'='*50}")
    print(f"Total stories validated: {len(story_dirs)}")
    print(f"Stories passing (≥70%): {passing_stories}")
    print(f"Stories failing: {len(story_dirs) - passing_stories}")
    print(f"Average score: {total_score/len(story_dirs):.1f}%")
    
    return {
        'total_stories': len(story_dirs),
        'passing_stories': passing_stories,
        'failing_stories': len(story_dirs) - passing_stories,
        'average_score': total_score/len(story_dirs) if story_dirs else 0,
        'all_passing': passing_stories == len(story_dirs)
    }

if __name__ == "__main__":
    results = validate_all_stories()
    
    if not results['all_passing']:
        print(f"\n❌ {results['failing_stories']} stories are failing validation!")
        exit(1)
    else:
        print(f"\n✅ All stories pass validation!")
        exit(0)

