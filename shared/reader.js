/**
 * AI Social Stories Generator - Reader Module
 * Handles text-to-speech and audio playback functionality
 */

class StoryReader {
  constructor() {
    this.synth = window.speechSynthesis;
    this.utterance = null;
    this.isPlaying = false;
    this.voices = [];
    this.currentVoice = null;
    this.rate = 1.0;
    this.pitch = 1.0;
    
    // Load voices
    this.loadVoices();
    
    // iOS needs this
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = () => this.loadVoices();
    }
  }
  
  loadVoices() {
    this.voices = this.synth.getVoices();
    
    // Prefer English voices
    const englishVoices = this.voices.filter(v => v.lang.startsWith('en'));
    
    if (englishVoices.length > 0) {
      // Prefer high-quality or "natural" voices
      const preferredVoice = englishVoices.find(v => 
        v.name.includes('Natural') || 
        v.name.includes('Enhanced') ||
        v.name.includes('Premium')
      ) || englishVoices[0];
      
      this.currentVoice = preferredVoice;
    } else if (this.voices.length > 0) {
      this.currentVoice = this.voices[0];
    }
    
    return this.voices;
  }
  
  speak(text, options = {}) {
    // Stop any current speech
    this.stop();
    
    if (!text || text.trim() === '') {
      console.warn('No text provided to speak');
      return Promise.reject(new Error('No text provided'));
    }
    
    return new Promise((resolve, reject) => {
      this.utterance = new SpeechSynthesisUtterance(text);
      
      // Apply settings
      this.utterance.voice = options.voice || this.currentVoice;
      this.utterance.rate = options.rate || this.rate;
      this.utterance.pitch = options.pitch || this.pitch;
      this.utterance.volume = options.volume || 1.0;
      
      // Event handlers
      this.utterance.onstart = () => {
        this.isPlaying = true;
        if (options.onStart) options.onStart();
      };
      
      this.utterance.onend = () => {
        this.isPlaying = false;
        if (options.onEnd) options.onEnd();
        resolve();
      };
      
      this.utterance.onerror = (event) => {
        this.isPlaying = false;
        console.error('Speech synthesis error:', event);
        if (options.onError) options.onError(event);
        reject(event);
      };
      
      this.utterance.onpause = () => {
        if (options.onPause) options.onPause();
      };
      
      this.utterance.onresume = () => {
        if (options.onResume) options.onResume();
      };
      
      // Speak
      try {
        this.synth.speak(this.utterance);
      } catch (error) {
        console.error('Error starting speech:', error);
        reject(error);
      }
    });
  }
  
  pause() {
    if (this.isPlaying) {
      this.synth.pause();
    }
  }
  
  resume() {
    if (this.synth.paused) {
      this.synth.resume();
    }
  }
  
  stop() {
    if (this.isPlaying || this.synth.speaking) {
      this.synth.cancel();
      this.isPlaying = false;
    }
  }
  
  setVoice(voiceName) {
    const voice = this.voices.find(v => v.name === voiceName);
    if (voice) {
      this.currentVoice = voice;
      return true;
    }
    return false;
  }
  
  setRate(rate) {
    this.rate = Math.max(0.1, Math.min(10, rate));
  }
  
  setPitch(pitch) {
    this.pitch = Math.max(0, Math.min(2, pitch));
  }
  
  getVoices() {
    return this.voices;
  }
  
  getCurrentVoice() {
    return this.currentVoice;
  }
}

/**
 * Audio Player for pre-generated audio files
 */
class AudioPlayer {
  constructor() {
    this.audio = null;
    this.isPlaying = false;
    this.currentSource = null;
  }
  
  load(audioSrc) {
    return new Promise((resolve, reject) => {
      // Stop current audio if playing
      this.stop();
      
      this.audio = new Audio(audioSrc);
      this.currentSource = audioSrc;
      
      this.audio.addEventListener('loadeddata', () => {
        resolve(this.audio);
      });
      
      this.audio.addEventListener('error', (e) => {
        console.error('Audio loading error:', e);
        reject(e);
      });
      
      // Preload
      this.audio.load();
    });
  }
  
  play(options = {}) {
    if (!this.audio) {
      return Promise.reject(new Error('No audio loaded'));
    }
    
    return new Promise((resolve, reject) => {
      // Event handlers
      this.audio.onplay = () => {
        this.isPlaying = true;
        if (options.onStart) options.onStart();
      };
      
      this.audio.onended = () => {
        this.isPlaying = false;
        if (options.onEnd) options.onEnd();
        resolve();
      };
      
      this.audio.onerror = (e) => {
        this.isPlaying = false;
        console.error('Audio playback error:', e);
        if (options.onError) options.onError(e);
        reject(e);
      };
      
      this.audio.onpause = () => {
        if (options.onPause) options.onPause();
      };
      
      // Apply settings
      if (options.rate) {
        this.audio.playbackRate = options.rate;
      }
      if (options.volume !== undefined) {
        this.audio.volume = options.volume;
      }
      
      // Play
      this.audio.play().catch(reject);
    });
  }
  
  pause() {
    if (this.audio && this.isPlaying) {
      this.audio.pause();
      this.isPlaying = false;
    }
  }
  
  resume() {
    if (this.audio && !this.isPlaying) {
      this.audio.play();
    }
  }
  
  stop() {
    if (this.audio) {
      this.audio.pause();
      this.audio.currentTime = 0;
      this.isPlaying = false;
    }
  }
  
  setRate(rate) {
    if (this.audio) {
      this.audio.playbackRate = Math.max(0.25, Math.min(4, rate));
    }
  }
  
  setVolume(volume) {
    if (this.audio) {
      this.audio.volume = Math.max(0, Math.min(1, volume));
    }
  }
  
  getCurrentTime() {
    return this.audio ? this.audio.currentTime : 0;
  }
  
  getDuration() {
    return this.audio ? this.audio.duration : 0;
  }
  
  seek(time) {
    if (this.audio) {
      this.audio.currentTime = time;
    }
  }
}

/**
 * Unified Reader Interface
 * Handles both TTS and pre-generated audio
 */
class UnifiedReader {
  constructor() {
    this.ttsReader = new StoryReader();
    this.audioPlayer = new AudioPlayer();
    this.mode = 'audio'; // 'audio' or 'tts'
    this.autoFallback = true;
  }
  
  async read(text, audioSrc, options = {}) {
    // Try audio first if available
    if (audioSrc && this.mode === 'audio') {
      try {
        await this.audioPlayer.load(audioSrc);
        return await this.audioPlayer.play(options);
      } catch (error) {
        console.warn('Audio playback failed, falling back to TTS:', error);
        if (this.autoFallback && text) {
          this.mode = 'tts';
          return await this.ttsReader.speak(text, options);
        }
        throw error;
      }
    }
    
    // Use TTS
    if (text) {
      return await this.ttsReader.speak(text, options);
    }
    
    throw new Error('No text or audio source provided');
  }
  
  pause() {
    if (this.mode === 'audio') {
      this.audioPlayer.pause();
    } else {
      this.ttsReader.pause();
    }
  }
  
  resume() {
    if (this.mode === 'audio') {
      this.audioPlayer.resume();
    } else {
      this.ttsReader.resume();
    }
  }
  
  stop() {
    this.audioPlayer.stop();
    this.ttsReader.stop();
  }
  
  setMode(mode) {
    if (mode === 'audio' || mode === 'tts') {
      this.mode = mode;
      return true;
    }
    return false;
  }
  
  getMode() {
    return this.mode;
  }
  
  setAutoFallback(enabled) {
    this.autoFallback = enabled;
  }
}

/**
 * UI Helper Functions
 */
function createReaderControls(containerId, text, audioSrc) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error('Container not found:', containerId);
    return null;
  }
  
  const reader = new UnifiedReader();
  
  const controlsHtml = `
    <div class="audio-controls">
      <button class="btn btn-primary" id="play-btn">
        <span>▶️ Listen</span>
      </button>
      <button class="btn btn-secondary" id="pause-btn" style="display:none;">
        <span>⏸️ Pause</span>
      </button>
      <button class="btn btn-secondary" id="stop-btn" style="display:none;">
        <span>⏹️ Stop</span>
      </button>
      <select class="mode-select" id="mode-select">
        <option value="audio">Pre-recorded Audio</option>
        <option value="tts">Text-to-Speech</option>
      </select>
      <label>
        Speed:
        <input type="range" id="rate-slider" min="0.5" max="2" step="0.1" value="1">
        <span id="rate-value">1.0x</span>
      </label>
    </div>
  `;
  
  container.innerHTML = controlsHtml;
  
  const playBtn = document.getElementById('play-btn');
  const pauseBtn = document.getElementById('pause-btn');
  const stopBtn = document.getElementById('stop-btn');
  const modeSelect = document.getElementById('mode-select');
  const rateSlider = document.getElementById('rate-slider');
  const rateValue = document.getElementById('rate-value');
  
  let isPlaying = false;
  
  playBtn.addEventListener('click', async () => {
    try {
      playBtn.style.display = 'none';
      pauseBtn.style.display = 'inline-block';
      stopBtn.style.display = 'inline-block';
      isPlaying = true;
      
      await reader.read(text, audioSrc, {
        rate: parseFloat(rateSlider.value),
        onEnd: () => {
          playBtn.style.display = 'inline-block';
          pauseBtn.style.display = 'none';
          stopBtn.style.display = 'none';
          isPlaying = false;
        },
        onError: (error) => {
          console.error('Playback error:', error);
          playBtn.style.display = 'inline-block';
          pauseBtn.style.display = 'none';
          stopBtn.style.display = 'none';
          isPlaying = false;
          alert('Error playing audio. Please try again or switch to text-to-speech mode.');
        }
      });
    } catch (error) {
      console.error('Failed to start playback:', error);
      playBtn.style.display = 'inline-block';
      pauseBtn.style.display = 'none';
      stopBtn.style.display = 'none';
      isPlaying = false;
    }
  });
  
  pauseBtn.addEventListener('click', () => {
    reader.pause();
    playBtn.style.display = 'inline-block';
    pauseBtn.style.display = 'none';
  });
  
  stopBtn.addEventListener('click', () => {
    reader.stop();
    playBtn.style.display = 'inline-block';
    pauseBtn.style.display = 'none';
    stopBtn.style.display = 'none';
    isPlaying = false;
  });
  
  modeSelect.addEventListener('change', (e) => {
    reader.setMode(e.target.value);
    if (isPlaying) {
      reader.stop();
      playBtn.style.display = 'inline-block';
      pauseBtn.style.display = 'none';
      stopBtn.style.display = 'none';
      isPlaying = false;
    }
  });
  
  rateSlider.addEventListener('input', (e) => {
    const rate = parseFloat(e.target.value);
    rateValue.textContent = rate.toFixed(1) + 'x';
    reader.ttsReader.setRate(rate);
    reader.audioPlayer.setRate(rate);
  });
  
  return reader;
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    StoryReader,
    AudioPlayer,
    UnifiedReader,
    createReaderControls
  };
}

