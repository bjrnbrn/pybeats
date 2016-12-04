pybeats

-systemanforderungen-
  python > 3.
  scipy
  sounddevice
  linux oder mac 
   oder windows und google und nerven wg scipy
    funktioniert: http://www.lfd.uci.edu/~gohlke/pythonlibs/


-start-	
  terminal im ordner ./pybeats öffnen
  fenster maximieren und 'python[3] beats.py' ausführen


_play_:
  alle importierbaren .wav-dateien aus ./db/samples werden importiert
  die samples können dann einzeln abgespielt werden


_song_:
  in _song_ erzeugte .wav-dateien werden im ordner ./db/projects/songs abgelegt


/db/projects/songs.json kann zb mit notepad++ oder atom bearbeitet werden und neue
songs können angehängt werden:
  jeder key der ersten Ebene bezeichnet einen song
  
   jeder song hat die daten {Tempo, Channels, Beat, Repeat, Tracks}:

	Tempo:		int		    zB 50, 120, keine "
	Channels:	1 oder 2	keine "
	Beat:		"...."		auflösung von einem beat in (hier) 4 sub-beats
	Repeat:		int		    loops, keine "
	Tracks:		dict		jeder key von tracks bezeichnet einen track


    jeder track in tracks eines songs hat die daten {SampleName, Pattern, Align}:

	SampleName:	name des zu importierenden samples für die spur
			    == .wav-datei ohne Endung
		
	Pattern:	aufbau des tracks
			    ALLE PATTERNS EINES SONGS MÜSSEN GLEICH LANG SEIN

			    aber: '|' wird dabei ignoriert

			    statt einzeiligen patterns können mehrzeilige patterns
			    in Form von strings in einer liste aufgenommen werden.
				
			    akzeptierte Werte:

                    '.':	kein sample wird an der stelle eingefügt
                            vorheriges sample der spur kann ausspielen
                    'X':	sample wird in voller lautstärke an position eingefügt
                    '5':	sample wird in halber lautstärke an position eingefügt
                     mgl.   0-9

	Align:		"L", "R" oder "C", für left, right, center
			    channel auf den der jew track gelegt werden soll
