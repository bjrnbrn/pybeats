# pybeats
_a python command line drum machine_

### requirements
python > 3.4.4  
scipy  
sounddevice  
linux or mac  
windows: follow scipy installation
[here](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

### usage
#### start
open terminal in folder ./pybeats  
  
maximize window and run 'python[3] beats.py'

#### options
\_play\_:  
all importable .wav-files from ./db/samples
are imported and can be played one bye one

\_song\_:  
each in \_song\_ generated .wav-file will be
placed in folder ./db/projects/

#### write songs
- /db/projects/songs.json cab be edited with
atom or notepad++
- new songs can be attached to songs.json  
- every first layer key defines a song  
  
**every song has the attributes**

_{Tempo, Channels, Beat, Repeat, Tracks}_

1. Tempo:   integer
2. Channels:	1 or 2
3. Beat: "...."; rationing of beats into (here: 4) sub-beats
4. Repeat:   integer;    number of loops
5. Tracks:   dictionary; every key of Tracks defines one track

**every track in tracks of a song has the attributes**

_{SampleName, Pattern, Align}_
  
#### SampleName:  
name of the sample to be imported for specific track  
== .wav-file without extension  
  
  
#### Pattern:  
accepted values:
              
**'.' :**    no sample will be placed at triggerpoint previous sample will play  
        
**'X':**     sample will be placed at position with full amplitude  

**'5':**     sample will be placed at position with half amplitude. possible: 0-9
  
- ALL PATTERNS OF A SONG HAVE TO BE OF SAME LENGTH  
- BUT: '|' will be ignored  
- possible are one-line or multiple line patterns  
- one line patterns are strings, multiple line patterns are list of strings  
  
  
#### Align:  
"L", "R" oder "C", for left, right, center  
channel that shall contain the specific track
