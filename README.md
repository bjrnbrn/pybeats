# pybeats
_a python command line drum machine_

### requirements
**linux or mac:**  
  python > 3.4  
  scipy  
  sounddevice  
  
**windows:**  
  additionally follow scipy installation [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy)

### usage
#### start
open terminal in folder ./pybeats  
maximize window and run 'python[3] beats.py'

#### options
_\_play\__:

- all importable .wav-files from ./db/samples are imported and can be played one bye one  
- one can put ones own wavefiles into this folder or any subfolder of ./db/samples  
- accepted formats are int8, int16, int32 and float32 WAV

_\_song\__:  
each in \_song\_ recorded .wav-file will be placed in folder ./db/projects/

#### write songs

- /db/projects/songs.json can be edited with
  atom or notepad++
- new songs can be attached to songs.json  
- every first layer key defines a song  
  
**every song has the attributes** _{Tempo, Channels, Beat, Repeat, Tracks}_  

1. Tempo:   integer
2. Channels:	1 or 2
3. Beat: "...."; rationing of beats into (here: 4) sub-beats
4. Repeat:   integer;    number of loops
5. Tracks:   dictionary; every key of Tracks defines one track

**every track in tracks of a song has the attributes** _{SampleName, Pattern, Align}_  

1. SampleName:  
    
    _name of the sample to be imported for specific track.  == .wav-file without extension_  
    

2. Pattern:  

  - ALL PATTERNS OF A SONG HAVE TO BE OF THE EXACT SAME LENGTH  
  - BUT: '|' will be ignored  
  - possible are one line or multiple line patterns  
  - one line patterns are strings, multiple line patterns are a list of strings  

  _accepted values:_

  **'.' :**    _no sample will be placed at triggerpoint. previous sample will play_  

  **'X' :**     _sample will be placed at position with full amplitude_  

  **'5' :**     _sample will be placed at position with half amplitude. possible: 0-9_  

      
3. Align:  
    
    _**"L"**, **"R"** or **"C"**, for left, right, center  
    channel that shall contain the specific track_
  
### examples  
  
[1] this is a json formatted song with a two line track pattern  

      {
        "Songname1":
        {
          "Tempo": 90,
          "Channels": 2,
          "Beat": "....",
          "Repeat": 4,
          "Tracks":
          {
            "0":
            {
              "SampleName": "kick_808",
              "Pattern": ["|X..X|X..X|.X.X|X..X|",
                          "|X...|...X|..XX|X...|"              
                         ],
              "Align": "C"
            },
            "1":
            {
              "SampleName": "snare_808",
              "Pattern": ["|..7.|..9.|..7.|..9.|",
                          "|..7.|..9.|..7.|..9.|"
                         ],
              "Align": "R"
            },
            "2":
            {
              "SampleName": "openhat_808",
              "Pattern": ["|0404|0404|0404|0440|",
                          "|0404|0404|0404|0440|"
                         ],
              "Align": "L"
            }
          }
        }
      }
  
[2] this is a json formatted song with a one line track pattern  
  
    { 
      "Songname2":
      {
        "Tempo": 60,
        "Channels": 1,
        "Beat": "....",
        "Repeat": 2,
        "Tracks":
        {
          "0":
          {
            "SampleName": "kick_808",
            "Pattern": "|X...|....|....|....|",
            "Align": "L"
          },
          "1":
          {
            "SampleName": "snare_808",
            "Pattern": "|....|....|X...|....|",
            "Align": "R"
          },
          "2":
          {
            "SampleName": "openhat_808",
            "Pattern": "|...7|...4|...8|.8.4|",
            "Align": "R"
          }
        }
      }
    }
