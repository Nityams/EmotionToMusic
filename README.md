# EmotionToMusic
Experimental python project that converts emotions on picture to autogenerated music

## Read Me:
This is an experimental program that converts emotions on pictures to auto generated music.

### Requirements to run this program:
 - Internet Connection
 - Microsoft Azure account with Emotion API subscribed.
 - python Improviser, 
          I would recommend you to use my version of Improviser since the original version(0.8.6.3) has un-updated files which does not function appropriately with Mingus(0.5.2)
 - python Mingus
 - FluidSynth
 - pyGame (optional, since this is only used for Visualization)
 - SoundFont SF2

### Fore more info on Improviser :
  https://github.com/bspaans/improviser/blob/master/README

### Running emot.py :
 - Before running emot.py I would highly recommend you to run Improviser.py first.
        - Running Improviser.py via Terminal:
        Open terminal and go to Improviser folder.
        Then go to, you can try either:
        
        1) cd build/lib/improviser
            ./Improviser.py -s swing
        ... this is more stable.
        OR

       2) cd improviser
              ./Improviser.py -s swing

       More on Improviser => ./Improviser.py --help

  - Save/Copy emot.py on the same folder as Improviser.py

  - Run:  python emot.py www.example.com/myPicture.com -f none
                      OR
    if you have pyGame installed:
  - Run: python emot.py www.example.com/myPicture.com -f lines

### Visualization available are:
    -f lines
    -f mixed
    -f cli
    -f blocks
    -f none

Any Questions: nityamshrestha@gmail.com

Good Luck
-Nityam
