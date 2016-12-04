import os

import song
import waveimport


# GLOBAL VARIABLES
FRAMERATE = waveimport.FRAMERATE


while True:

    os.system('cls' if os.name == 'nt' else 'clear')
    print("OPTIONS:\n"
          "'_play_'  ->  PLAY AVAILABLE SAMPLES\n"
          "'_song_'  ->  PARSE A SONG FILE\n"
          "'_exit_'  ->  QUIT\n")
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

            # PRINT THE SAMPLES LIBRARY
            os.system('cls' if os.name == 'nt' else 'clear')
            print("SAMPLES:")

            for i in range(0, len(SamplesNames) - 5, 6):

                print("{:<22}{:<22}{:<22}{:<22}{:<22}{:<22}".format(
                        SamplesNames[i],
                        SamplesNames[i + 1],
                        SamplesNames[i + 2],
                        SamplesNames[i + 3],
                        SamplesNames[i + 4],
                        SamplesNames[i + 5]))

            # CHOOSE A SAMPLE AND PLAY
            print("\nOPTIONS:\n"
                  "'samplename'  ->  PLAY A SAMPLE\n"
                  "'_back_'      ->  GO BACK TO MENUE\n")
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
            print("SONGS:")

            for i in range(0, len(SongNames)):
                print(SongNames[i])

            # CHOOSE A SONG AND MAKE IT
            print("\nOPTIONS:\n"
                  "'songname'  ->  MAKE A SONG\n"
                  "'_back_'    ->  GO BACK TO MENUE\n")
            userinput = input()

            if userinput == '_back_':
                break

            elif userinput in SongNames:

                SONG = song.Song(userinput)

                print(SONG)

                song.play(SONG.nchannels, SONG.data, FRAMERATE, SONG.repeat)

                song.record(userinput, SONG.nchannels, SONG.data, FRAMERATE, SONG.repeat)
