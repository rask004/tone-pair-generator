# tone-pair-generator
Script that generates pairs of tones that converge over time in frequency. Intended for Tinnitus treatment studies.

##Dependencies
###External Python Packages
- Numpy
- Simpleaudio
###External libraries
- ALSA sound libraries (for simpleaudio package)

##Usage
Run from CLI, for example:

    python audiotones.py 10 1000 4000

will run 10 cycles of tone pairs, starting with the frequencies 1000 Hz and 4000 Hz, 
converging toward 2500 Hz, shifting by 50% of the remaining difference each time 
(1000 Hz, to 1750 Hz, to 2075 Hz and so on). The tomes will have "50%" Loudness depending
on the current speaker / audio software volume settings (what "50%" exactly translates to will
likely vary between different machines). Tones will last for 1 second, have a half second pause 
between, and a 2 second pause between pairs of tones. 

    python audiotones.py 10 1000 4000 -t 3000 -v 75.5 -c 70.0
    
will run 10 cycles of tone pairs, starting with the frequencies 1000 Hz and 4000 Hz, 
but will converge toward 3000 Hz, shifting by 70% of the remaining difference each time. 
Loudness will ve at 75.5%. Tone and pause durations are the same as above.

    python audiotones.py 10 1000 4000 -t 3000 -v 75.5 -c 70.0 -d 0.333 -p 0.8 -l 1.5
    
This is like the last example, but with tone durations of a 1/3rd of a second, a 0.8 second 
pause between tones, and a 1.5 second pause between tone pairs.

---

The intended usage is for the study of Auditory Therapies, especially with Tinnitus. Otherwise
as per the licence the software may be used as one see fits.

Though intended for CLI use, the software script can be imported as a module. Check
the script file for function documentation.

##Defects
- Tones might not play properly if the sound hardware is in use by other programs or software,
or is blocked / locked by other resources. This can be dependent on your hardware
or particular firmware. 
- Pauses are managed using `time.sleep`, as the script is single threaded this might cause 
slowdowns. 
 
