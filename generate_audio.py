#!/usr/bin/env python3
"""
Audio Generator for Kingdom of Aldoria
Creates sound effects using pure Python audio synthesis
"""

import os
import math
import wave
import struct
import random

def create_directories():
    """Create audio directories"""
    directories = [
        "assets/audio/sfx",
        "assets/audio/music",
        "assets/audio/ui",
        "assets/audio/combat",
        "assets/audio/ambient"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created audio directory: {directory}")

def generate_tone(frequency, duration, sample_rate=22050, amplitude=0.5):
    """Generate a pure tone"""
    frames = int(duration * sample_rate)
    wave_data = []
    
    for i in range(frames):
        t = float(i) / sample_rate
        value = amplitude * math.sin(2 * math.pi * frequency * t)
        wave_data.append(int(value * 32767))
    
    return wave_data

def generate_noise(duration, sample_rate=22050, amplitude=0.3):
    """Generate white noise"""
    frames = int(duration * sample_rate)
    wave_data = []
    
    for i in range(frames):
        value = amplitude * (random.random() * 2 - 1)
        wave_data.append(int(value * 32767))
    
    return wave_data

def apply_envelope(wave_data, attack=0.1, decay=0.1, sustain=0.7, release=0.2):
    """Apply ADSR envelope to audio data"""
    length = len(wave_data)
    attack_frames = int(length * attack)
    decay_frames = int(length * decay)
    release_frames = int(length * release)
    sustain_frames = length - attack_frames - decay_frames - release_frames
    
    for i in range(length):
        if i < attack_frames:
            # Attack phase
            envelope = i / attack_frames
        elif i < attack_frames + decay_frames:
            # Decay phase
            envelope = 1.0 - (1.0 - sustain) * (i - attack_frames) / decay_frames
        elif i < attack_frames + decay_frames + sustain_frames:
            # Sustain phase
            envelope = sustain
        else:
            # Release phase
            envelope = sustain * (1.0 - (i - attack_frames - decay_frames - sustain_frames) / release_frames)
        
        wave_data[i] = int(wave_data[i] * envelope)
    
    return wave_data

def save_wav(wave_data, filename, sample_rate=22050):
    """Save wave data to WAV file"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Convert to bytes
        wav_data = struct.pack('<%dh' % len(wave_data), *wave_data)
        wav_file.writeframes(wav_data)

def create_sword_slash():
    """Create sword slash sound effect"""
    # Whoosh sound with metallic ring
    duration = 0.8
    sample_rate = 22050
    
    # Generate noise sweep
    frames = int(duration * sample_rate)
    wave_data = []
    
    for i in range(frames):
        t = float(i) / sample_rate
        
        # Whoosh (filtered noise with frequency sweep)
        freq = 800 - (t * 600)  # Sweep from 800Hz to 200Hz
        noise_val = (random.random() * 2 - 1) * 0.3
        filtered_noise = noise_val * math.exp(-t * 3)  # Decay
        
        # Metallic ring (sine wave)
        ring_freq = 1200 + 200 * math.sin(t * 10)
        ring_val = 0.2 * math.sin(2 * math.pi * ring_freq * t) * math.exp(-t * 5)
        
        combined = filtered_noise + ring_val
        wave_data.append(int(combined * 32767))
    
    # Apply envelope
    wave_data = apply_envelope(wave_data, 0.05, 0.1, 0.6, 0.25)
    
    save_wav(wave_data, "assets/audio/combat/sword_slash.wav")
    print("Created sword slash sound")

def create_magic_spell():
    """Create magic spell sound effect"""
    duration = 1.2
    sample_rate = 22050
    frames = int(duration * sample_rate)
    wave_data = []
    
    for i in range(frames):
        t = float(i) / sample_rate
        
        # Magical shimmer (multiple sine waves with vibrato)
        freq1 = 400 + 100 * math.sin(t * 8)
        freq2 = 600 + 80 * math.sin(t * 12)
        freq3 = 800 + 60 * math.sin(t * 16)
        
        val1 = 0.3 * math.sin(2 * math.pi * freq1 * t)
        val2 = 0.2 * math.sin(2 * math.pi * freq2 * t)
        val3 = 0.15 * math.sin(2 * math.pi * freq3 * t)
        
        # Sparkle effect (high frequency modulation)
        sparkle = 0.1 * math.sin(2 * math.pi * 2000 * t) * (1 + math.sin(t * 20)) * 0.5
        
        combined = (val1 + val2 + val3 + sparkle) * math.exp(-t * 0.8)
        wave_data.append(int(combined * 32767))
    
    wave_data = apply_envelope(wave_data, 0.1, 0.2, 0.7, 0.0)
    
    save_wav(wave_data, "assets/audio/combat/magic_spell.wav")
    print("Created magic spell sound")

def create_enemy_hit():
    """Create enemy hit sound effect"""
    duration = 0.4
    sample_rate = 22050
    frames = int(duration * sample_rate)
    wave_data = []
    
    for i in range(frames):
        t = float(i) / sample_rate
        
        # Impact sound (low frequency thump)
        thump_freq = 80 + 40 * math.exp(-t * 8)
        thump = 0.6 * math.sin(2 * math.pi * thump_freq * t)
        
        # Crack sound (noise burst)
        if t < 0.1:
            crack = (random.random() * 2 - 1) * 0.4 * math.exp(-t * 20)
        else:
            crack = 0
        
        combined = (thump + crack) * math.exp(-t * 5)
        wave_data.append(int(combined * 32767))
    
    wave_data = apply_envelope(wave_data, 0.01, 0.05, 0.3, 0.64)
    
    save_wav(wave_data, "assets/audio/combat/enemy_hit.wav")
    print("Created enemy hit sound")

def create_level_up():
    """Create level up sound effect"""
    duration = 2.0
    sample_rate = 22050
    frames = int(duration * sample_rate)
    wave_data = []
    
    for i in range(frames):
        t = float(i) / sample_rate
        
        # Rising arpeggio
        base_freq = 262  # C4
        notes = [1.0, 1.25, 1.5, 2.0]  # C, E, G, C octave
        
        note_duration = 0.4
        note_index = min(int(t / note_duration), len(notes) - 1)
        freq = base_freq * notes[note_index]
        
        # Bell-like tone
        fundamental = 0.5 * math.sin(2 * math.pi * freq * t)
        harmonic1 = 0.3 * math.sin(2 * math.pi * freq * 2 * t)
        harmonic2 = 0.2 * math.sin(2 * math.pi * freq * 3 * t)
        
        # Sparkling effect
        sparkle_freq = 1000 + 500 * math.sin(t * 15)
        sparkle = 0.1 * math.sin(2 * math.pi * sparkle_freq * t) * (1 + math.sin(t * 8)) * 0.5
        
        combined = (fundamental + harmonic1 + harmonic2 + sparkle) * math.exp(-t * 0.5)
        wave_data.append(int(combined * 32767))
    
    wave_data = apply_envelope(wave_data, 0.05, 0.1, 0.8, 0.05)
    
    save_wav(wave_data, "assets/audio/ui/level_up.wav")
    print("Created level up sound")

def create_button_click():
    """Create UI button click sound"""
    duration = 0.2
    sample_rate = 22050
    frames = int(duration * sample_rate)
    wave_data = []
    
    for i in range(frames):
        t = float(i) / sample_rate
        
        # Short click with harmonic
        click_freq = 800
        click = 0.5 * math.sin(2 * math.pi * click_freq * t)
        harmonic = 0.2 * math.sin(2 * math.pi * click_freq * 2 * t)
        
        combined = (click + harmonic) * math.exp(-t * 15)
        wave_data.append(int(combined * 32767))
    
    wave_data = apply_envelope(wave_data, 0.01, 0.05, 0.2, 0.74)
    
    save_wav(wave_data, "assets/audio/ui/button_click.wav")
    print("Created button click sound")

def create_coin_pickup():
    """Create coin pickup sound effect"""
    duration = 0.6
    sample_rate = 22050
    frames = int(duration * sample_rate)
    wave_data = []
    
    for i in range(frames):
        t = float(i) / sample_rate
        
        # Bright metallic ping
        ping_freq = 1200 + 300 * math.exp(-t * 8)
        ping = 0.4 * math.sin(2 * math.pi * ping_freq * t)
        
        # Jingle harmonics
        harm1 = 0.2 * math.sin(2 * math.pi * ping_freq * 1.5 * t)
        harm2 = 0.1 * math.sin(2 * math.pi * ping_freq * 2.2 * t)
        
        combined = (ping + harm1 + harm2) * math.exp(-t * 3)
        wave_data.append(int(combined * 32767))
    
    wave_data = apply_envelope(wave_data, 0.01, 0.1, 0.5, 0.39)
    
    save_wav(wave_data, "assets/audio/ui/coin_pickup.wav")
    print("Created coin pickup sound")

def create_victory_fanfare():
    """Create victory fanfare"""
    duration = 3.0
    sample_rate = 22050
    frames = int(duration * sample_rate)
    wave_data = []
    
    # Victory melody notes (frequencies)
    melody = [
        (523, 0.5),  # C5
        (659, 0.5),  # E5
        (784, 0.5),  # G5
        (1047, 1.5)  # C6
    ]
    
    for i in range(frames):
        t = float(i) / sample_rate
        
        # Determine current note
        note_time = 0
        current_freq = 523
        
        for freq, duration_note in melody:
            if t >= note_time and t < note_time + duration_note:
                current_freq = freq
                break
            note_time += duration_note
        
        # Trumpet-like sound
        fundamental = 0.6 * math.sin(2 * math.pi * current_freq * t)
        harmonic1 = 0.3 * math.sin(2 * math.pi * current_freq * 2 * t)
        harmonic2 = 0.2 * math.sin(2 * math.pi * current_freq * 3 * t)
        
        # Add some brass brightness
        brightness = 0.1 * math.sin(2 * math.pi * current_freq * 4 * t)
        
        combined = (fundamental + harmonic1 + harmonic2 + brightness)
        if t > 2.5:  # Fade out
            combined *= math.exp(-(t - 2.5) * 4)
        
        wave_data.append(int(combined * 32767))
    
    save_wav(wave_data, "assets/audio/ui/victory.wav")
    print("Created victory fanfare")

def create_background_music():
    """Create simple background music loop"""
    duration = 8.0  # 8-second loop
    sample_rate = 22050
    frames = int(duration * sample_rate)
    wave_data = []
    
    # Simple chord progression: C - Am - F - G
    chord_progression = [
        ([262, 330, 392], 2.0),  # C Major
        ([220, 262, 330], 2.0),  # A Minor
        ([175, 220, 262], 2.0),  # F Major
        ([196, 247, 294], 2.0)   # G Major
    ]
    
    for i in range(frames):
        t = float(i) / sample_rate
        
        # Determine current chord
        chord_time = 0
        current_chord = [262, 330, 392]
        
        for chord, chord_duration in chord_progression:
            if t >= chord_time and t < chord_time + chord_duration:
                current_chord = chord
                break
            chord_time += chord_duration
        
        # Generate chord tones
        value = 0
        for freq in current_chord:
            # Soft sine waves for ambient background
            tone = 0.15 * math.sin(2 * math.pi * freq * t)
            value += tone
        
        # Add gentle melody on top
        melody_freq = current_chord[0] * 2  # Octave above root
        melody = 0.1 * math.sin(2 * math.pi * melody_freq * t + math.sin(t * 0.5))
        
        combined = value + melody
        wave_data.append(int(combined * 32767))
    
    save_wav(wave_data, "assets/audio/music/background_loop.wav")
    print("Created background music loop")

def create_boss_music():
    """Create dramatic boss battle music"""
    duration = 10.0
    sample_rate = 22050
    frames = int(duration * sample_rate)
    wave_data = []
    
    for i in range(frames):
        t = float(i) / sample_rate
        
        # Dramatic low frequency drone
        drone_freq = 65.4  # C2
        drone = 0.3 * math.sin(2 * math.pi * drone_freq * t)
        
        # Pulsing rhythm
        pulse_rate = 2.0  # 2 Hz
        pulse = (1 + math.sin(2 * math.pi * pulse_rate * t)) * 0.5
        
        # Dark melody
        melody_freq = 130.8 + 50 * math.sin(t * 0.3)  # C3 with vibrato
        melody = 0.4 * math.sin(2 * math.pi * melody_freq * t) * pulse
        
        # High tension element
        tension_freq = 800 + 200 * math.sin(t * 8)
        tension = 0.1 * math.sin(2 * math.pi * tension_freq * t) * pulse
        
        combined = drone + melody + tension
        wave_data.append(int(combined * 32767))
    
    save_wav(wave_data, "assets/audio/music/boss_battle.wav")
    print("Created boss battle music")

def main():
    """Generate all sound effects and music"""
    print("🎵 Generating Kingdom of Aldoria Audio 🎵")
    print("=" * 50)
    
    try:
        create_directories()
        
        print("\n⚔️ Creating combat sounds...")
        create_sword_slash()
        create_magic_spell()
        create_enemy_hit()
        
        print("\n🎮 Creating UI sounds...")
        create_button_click()
        create_coin_pickup()
        create_level_up()
        create_victory_fanfare()
        
        print("\n🎼 Creating background music...")
        create_background_music()
        create_boss_music()
        
        print("\n✅ Audio generation complete!")
        print("Generated high-quality fantasy RPG sound effects")
        print("All audio optimized for mobile gameplay")
        
        # Create audio manifest
        audio_manifest = {
            "combat": [
                "sword_slash.wav",
                "magic_spell.wav", 
                "enemy_hit.wav"
            ],
            "ui": [
                "button_click.wav",
                "coin_pickup.wav",
                "level_up.wav",
                "victory.wav"
            ],
            "music": [
                "background_loop.wav",
                "boss_battle.wav"
            ]
        }
        
        import json
        with open("assets/audio/audio_manifest.json", 'w') as f:
            json.dump(audio_manifest, f, indent=2)
        
        print("Created audio manifest file")
        
    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎵 Audio ready! Sound effects generated successfully.")
    else:
        print("\n❌ Audio generation failed.")