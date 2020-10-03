# WPI.CS4341 - Gomoku referee
Code developed for the CS4341 class at WPI by Sam Ogden
Maintained by Jackson Powell.

Please note: unless otherwise stated all code is written for python27 (which is usually mapped to just python on systems) and so should generally be run as "python [script name]"
If your default python mapping is not to python 2.7 then you may need to install python 2.7, change the environment path to map python to python 2.7, and/or create a virtual environment that uses python 2.7.

The referee script takes two arguments, the two names of the teams playing the game. Assuming that python is mapped to python 2.7 and the terminal is open in the directory containing the referee script, then the referee would be run as "python referee.py teamname1 teamname2"

All files created by the referee will be located in the directory where the referee script is being run from which will be the same directory as the location of your team's executable when grading.
After the completion of a game, both groupname.go files will remain unless manually deleted or until the first move is taken for the next game. Thus, you may need to manually remove the files after each game is completed during your testing for the expected behavior of detecting your groupname.go file for the next game's first move. When grading, we will do this as well.