# AlphaCalc
AlphaCalc is a calculator (with a GUI component) that takes verbal input in the form of text or audio, such as "multiply 4 by 3 subtracted by 2" and converts it into a mathematical expression which it evaluates. Users can add or specifically remove presets such as "multiplied by" evaluates to "*" in each use.

It also has a memory feature which can be accessed or cleared at any time.

Prerequisites
-------------
The machine must have MySQL installed. The password asked for by AlphaCalc is the MySQL password.

The following modules are to be installed:
- Tkinter
- mysql.connector
- Pyaudio
- playsound
- SpeechRecognition
- gTTS

If these modules are not already installed, just install them from the Command Prompt using:
>pip install <module_name>

The assets folder must be copied correctly.
