import numpy as np 
import IPython.display as ipd
import matplotlib.pyplot as plt
import wave

'''
HW1.15 DANIEL CHRENKO

RUNNING THE FILE PRODUCES: 2 PNG FIGURES + 2 WAV FILES FOR TWINKLE TWINKLE LITTLE STAR
ONE FOR NO ADSR AND ONE FOR WITH ADSR

IF YOU WANT TO VIEW IN NOTEBOOK AND PLAY SOUND IN NOTEBOOK, YOU CAN CHOOSE WHICH SOUND
BY COMMENTING AND UNCOMMENTING THE LAST 2 LINES IN THE FILE :)
'''

'''
FUNCTIONS
'''

def midi2freq(midi):
    freq = (2**((midi-69)/12)) * 440
    return freq


# MIDI note number and duration
def generate_triangle(midi, duration, N):
    # convert the midi -> freq
    freq = midi2freq(midi)
    
    t = np.arange(0, duration, 1.0 / sampling_rate)

    # Create the (simulated) triangle wave using sinusoids
    triangle_wave = np.zeros_like(t)
    for i in range(1, N, 2):  # Add odd harmonics up to the N-1th harmonic
        triangle_wave += (1 / (i ** 2)) * np.sin(2 * np.pi * i * freq * t)


    return triangle_wave
    

def adsr_envelope(duration, attack, decay, sustain_level, release, sampling_rate):
    t = int(duration * sampling_rate)
    envelope = np.zeros(t)

    # attack
    attack_samples = int(attack * duration * sampling_rate)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    # for the samples from start till end of attack %

    # decay
    decay_samples = int(decay * duration * sampling_rate)
    envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples)
    # from end of the attack -> sustain start

    # sustain
    sustain_samples = int((1 - release) * duration * sampling_rate) - attack_samples - decay_samples
    envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain_level
    # sustain level after decay and attack till end of sustain

    # release
    release_samples = int(release * duration * sampling_rate)
    envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)
    return envelope


def create_seq(notes, duration, sr, envelope=1):

    N = 25
    seq = []
    
    for note in notes:
        if (note == 0):
            num_samples = int(duration * sr)
            rest_signal = np.zeros(num_samples)
            seq.append(rest_signal)
        else:
            seq.append(generate_triangle(note, duration, N) * envelope)

    final_signal = np.hstack(seq)
    return final_signal
    
'''
CALLS
'''

# Parameters
sampling_rate = 44100

# note duration
duration = 0.5  # Duration of the envelope in seconds

# adsr params
attack = 0.1
decay = 0.2
sustain = 0.5
release = 0.3
# Create the ADSR envelope
envelope = adsr_envelope(duration, attack, decay, sustain, release, sampling_rate)


midi_notes = [60, 60, 67, 67, 69, 69, 67, 0, 65, 65, 64, 64, 62, 62, 60]
# used 0 as a rest

data = create_seq(midi_notes, 0.5, sampling_rate)
data_envelope = create_seq(midi_notes, 0.5, sampling_rate, envelope)

# save and show different plots
plt.figure() 
plt.plot(data)
plt.savefig('twinkle_no_adsr.png')

plt.figure() 
plt.plot(data_envelope)
plt.savefig('twinkle_with_adsr.png')

# write different sounds to wav files using 16 bit audio
output_file = 'twinkle_no_adsr.wav'
with wave.open(output_file, 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sampling_rate)
    wav_file.writeframes(np.array(data * 32767, dtype=np.int16))

output_file = 'twinkle_with_adsr.wav'
with wave.open(output_file, 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sampling_rate)
    wav_file.writeframes(np.array(data_envelope * 32767, dtype=np.int16))

# comment out whichever one you would like to output -- for notebook view
ipd.Audio(data_envelope, rate=sampling_rate)
# ipd.Audio(data, rate=sampling_rate)