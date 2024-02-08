# SIN NOTE SEQUENCER FOR TWINKLE TWINKLE LITTLE STAR

- generates a simulated triangle wave for a set of midi notes
- this is done by converting the midi notes to frequencies and then leveraging odd harmonics to simluate a triangle wave for each note
- the notes are then put into one data signal
- created an adsr envelope to simulate real world instrument sounds (attack, decay, sustain, release on each note)
- data signal is then written to wav files and plotted into png files appropriately named

to run: /python sine_note_sequencer.py

4 file will be written in the same directory