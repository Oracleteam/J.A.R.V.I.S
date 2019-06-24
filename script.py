import os
import time
import argparse
import aiml


mode = "text"
voice = "pyttsx"
terminate = ['bye', 'buy', 'shutdown',
             'exit', 'quit', 'gotosleep',
             'goodbye', 'adios', 'cerrar']


def get_arguments():
    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group('params')
    optional.add_argument('-v', '--voice', action='store_true', required=False,
                          help='Enable voice mode')
    optional.add_argument('-g', '--gtts', action='store_true', required=False,
                          help='Enable Google Text To Speech engine')
    arguments = parser.parse_args()
    return arguments


def gtts_speak(jarvis_speech):
    tts = gTTS(text=jarvis_speech, lang='es')
    tts.save('jarvis_speech.mp3')
    mixer.init()
    mixer.music.load('jarvis_speech.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)


def offline_speak(jarvis_speech):
    engine = pyttsx.init()
    engine.say(jarvis_speech)
    engine.runAndWait()


def speak(jarvis_speech):
    if voice == "gTTS":
        gtts_speak(jarvis_speech)
    else:
        offline_speak(jarvis_speech)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Habla a JAIME: ")
        audio = r.listen(source)
    try:
        print r.recognize_google(audio)
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        speak("No le entiendo senor repitalo por favor")
        return(listen())
    except sr.RequestError as e:
        print("Could not request results from " +
              "Google Speech Recognition service; {0}".format(e))


if __name__ == '__main__':
    args = get_arguments()

    if (args.voice):
        try:
            import speech_recognition as sr
            mode = "voice"
        except ImportError:
            print("\nInstall SpeechRecognition to use this feature." +
                  "\nStarting text mode\n")
    if (args.gtts):
        try:
            from gtts import gTTS
            from pygame import mixer
            voice = "gTTS"
        except ImportError:
            import pyttsx
            print("\nInstall gTTS and pygame to use this feature." +
                  "\nUsing pyttsx\n")
    else:
        import pyttsx

    kernel = aiml.Kernel()

    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
        # kernel.saveBrain("bot_brain.brn")

    # kernel now ready for use
    while True:
        if mode == "voice":
            response = listen()
        else:
            response = raw_input("Habla a JAIME : ")
        if response.lower().replace(" ", "") in terminate:
            break
        jarvis_speech = kernel.respond(response)
        print "JAIME: " + jarvis_speech
        speak(jarvis_speech)
