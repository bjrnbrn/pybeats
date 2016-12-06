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
_\_play\__:  
all importable .wav-files from ./db/samples
are imported and can be played one bye one

_\_song\__:  
each in \_song\_ generated .wav-file will be
placed in folder ./db/projects/

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

    _accepted values:_
                  
    **'.' :**    _no sample will be placed at triggerpoint. previous sample will play_  
            
    **'X' :**     _sample will be placed at position with full amplitude_  
    
    **'5' :**     _sample will be placed at position with half amplitude. possible: 0-9_
      
    - ALL PATTERNS OF A SONG HAVE TO BE OF THE EXACT SAME LENGTH  
    - BUT: '|' will be ignored  
    - possible are one line or multiple line patterns  
    - one line patterns are strings, multiple line patterns are a list of strings  
          
          
3. Align:  
    
    _**"L"**, **"R"** or **"C"**, for left, right, center  
    channel that shall contain the specific track_
  
### examples  
  
_[1] this is an example json file song with a two line track pattern_  

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
              "Align": "R"
            }
          }
        }
      }
  
_[2] this is an example json file song with a one line track pattern_  
  
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
            "Align": "C"
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
