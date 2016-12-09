import os

import song
import waveimport


# GLOBAL VARIABLES
FRAMERATE = waveimport.FRAMERATE


while True:

    os.system('cls' if os.name == 'nt' else 'clear')

    print("OPTIONS:\n"
          "----------------------------------\n"
          "_play_  ->  PLAY AVAILABLE SAMPLES\n"
          "_song_  ->  PARSE A SONG FILE\n"
          "_exit_  ->  QUIT\n")

    userinput = input()

    if userinput == '_exit_':
        break

    elif userinput == '_play_':

        # MAKE DICT OF AVAILABLE SAMPLES AND DISPLAY THEM
        SourceSamples = waveimport.import_folder()
        SamplesNames = list(SourceSamples.keys())
        SamplesNames.sort()

        for i in range(6 - len(SamplesNames) % 6):

            SamplesNames.append(' ')

        while True:

            # PRINT THE SAMPLES LIBRARY IN 6 COLUMNS
            os.system('cls' if os.name == 'nt' else 'clear')

            print("SAMPLES:\n{}".format('-' * 132))

            for i in range(0, len(SamplesNames) - 5, 6):

                print("{:<22}{:<22}{:<22}{:<22}{:<22}{:<22}".format(
                        SamplesNames[i],
                        SamplesNames[i + 1],
                        SamplesNames[i + 2],
                        SamplesNames[i + 3],
                        SamplesNames[i + 4],
                        SamplesNames[i + 5]))

            # CHOOSE A SAMPLE AND PLAY
            print("\n\nOPTIONS:\n"
                  "--------------------------------\n"
                  "'samplename'  ->  PLAY A SAMPLE\n"
                  "_back_      ->  GO BACK TO MENUE\n")

            userinput = input()

            if userinput == '_back_':
                break

            elif userinput in SourceSamples.keys():

                SAMPLE = SourceSamples[userinput]
                song.play(1, SAMPLE, FRAMERATE)

    elif userinput == '_song_':

        # MAKE LIST OF AVAILABLE SONG TEMPLATES AND DISPLAY THEM
        SourceSongs = song.Songs()
        SongNames = SourceSongs.songs
        SongNames.sort()

        while True:

            # PRINT THE SONGS LIBRARYs
            os.system('cls' if os.name == 'nt' else 'clear')

            print("SONGS:\n"
                  "------------------------------")

            for songname in SongNames:
                print(songname)

            # CHOOSE A SONG AND PLAY IT
            print("\n\nOPTIONS:\n"
                  "------------------------------\n"
                  "'songname'  ->  MAKE A SONG\n"
                  "_back_    ->  GO BACK TO MENUE\n")

            userinput = input()

            if userinput == '_back_':
                break

            elif userinput in SongNames:

                SONG = song.Song(userinput)

                print(SONG)

                song.play(SONG.nchannels, SONG.data, FRAMERATE, SONG.repeat)

                # RECORD THE SONG TO DISC
                print("\nRECORD SONG TO DISC [Y/n]:\n")

                rec = input().lower()

                if rec == 'y':

                    song.record(userinput, SONG.nchannels, SONG.data, FRAMERATE, SONG.repeat)
