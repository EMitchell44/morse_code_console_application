from math import pi, sin
import wave
import struct


def silence(duration_ms, sample_rate):
    output = []
    samples = duration_ms * (sample_rate / 1000)
    for x in range(int(samples)):
        output.append(0.0)
    return output


def sine_wave(duration_ms, frequency, volume, sample_rate):
    output = []
    freq = frequency
    vol = volume
    samples = duration_ms * (sample_rate / 1000)
    for x in range(int(samples)):
        output.append(vol * sin(2 * pi * freq * (x / sample_rate)))
    return output


def dit(dit_length_ms, frequency, volume, sample_rate, waveform='sine'):
    if waveform == 'sine':
        return sine_wave(dit_length_ms, frequency, volume, sample_rate)


def dah(dit_length_ms, frequency, volume, sample_rate, waveform='sine'):
    if waveform == 'sine':
        return sine_wave(dit_length_ms * 3, frequency, volume, sample_rate)


def intra_character_space(dit_length_ms, sample_rate):
    return silence(dit_length_ms, sample_rate)


def letter_space(dit_length_ms, sample_rate):
    # Two spaces are added instead of three because the intra character space is already
    # added automatically after each dit and dah.
    return silence(dit_length_ms * 2, sample_rate)


def word_space(dit_length_ms, sample_rate):
    # Six spaces are added instead of seven for the same reason.
    return silence(dit_length_ms * 6, sample_rate)


def generate_audio_data(morse_in, dit_length, frequency, volume, sample_rate=44100.0, waveform='sine'):
    # Accepts "morse_in" as a string of spaces, dots, and dashes. This merely generates the audio;
    # it does not check to see whether the input is valid morse code. The generated file begins and
    # ends with a word space.
    audio_data = []
    audio_data += word_space(dit_length, sample_rate)
    space = 0
    for char in morse_in:
        if space == 3:
            audio_data += word_space(dit_length, sample_rate)
            space = 0
        if char == '.':
            if space > 0:
                audio_data += intra_character_space(dit_length, sample_rate)
            space = 0
            audio_data += dit(dit_length, frequency, volume, sample_rate, waveform)
            audio_data += intra_character_space(dit_length, sample_rate)
        if char == '-':
            if space > 0:
                audio_data += letter_space(dit_length, sample_rate)
            space = 0
            audio_data += dah(dit_length, frequency, volume, sample_rate, waveform)
            audio_data += intra_character_space(dit_length, sample_rate)
        if char == ' ':
            space += 1
    audio_data += word_space(dit_length, sample_rate)
    return audio_data


def generate_wav_file(filename, sample_rate, audio_data):
    nchannels = 1
    sampwidth = 2
    nframes = len(audio_data)
    comptype = 'NONE'
    compname = 'not compressed'

    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((nchannels,
                            sampwidth,
                            sample_rate,
                            nframes,
                            comptype,
                            compname))
        for sample in audio_data:
            wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))
    return
