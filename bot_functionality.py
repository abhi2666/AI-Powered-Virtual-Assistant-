import tkinter as tk
import speech_recognition as sr
import re
import pyttsx3
import main
import random
import pywhatkit
import datetime
import wikipedia
from PIL import ImageTk, Image, ImageSequence
import winsound
import weather

# Setting various responses for Exiting
exit_responses = ["Take care", "Thank you for your time", "It was nice talking to you", "Goodbye!"]
user_prompt = ""
bot_response = ""

## Initializing the Text-to-Speech and Speech-to-Text engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Setting Alarm thread
alarm_thread = None


def speak(bot_response):
    engine.say(bot_response)
    engine.runAndWait()
    return


#################################### CHAT SCREEN UPDATION ##################################################
def send_message(user_prompt, bot_response):
    display_message("You: " + user_prompt)
    bot_resp = str(bot_response)
    response = "Bot: " + bot_resp
    display_message(response)


# Display the messages in the chat: text area
def display_message(message):
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, message + "\n")
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)


#############################################################################################################

########################### EXTRACT THE LOCATION FOR THE WEATHER API ########################################
def extract_location(input_string):
    words = input_string.split()
    index_of = words.index("of") if "of" in words else -1
    extracted_text = " ".join(words[index_of+1:]) if index_of != -1 else None
    return extracted_text

##############################################################################################################

######################################### FUNCTIONALITIES ####################################################

def functionalities(user_prompt):
    global alarm_thread
    # Exit program
    if user_prompt.lower() in ['stop', 'quit', 'exit', 'bye', 'sayonara']:
        bot_response = random.choice(exit_responses)
        send_message(user_prompt, bot_response)
        speak(bot_response)
        print(bot_response)
        exit()

    # will be used to play any videos on youtube
    elif "play" in user_prompt.lower():
        query = user_prompt.lower().replace("play", "").replace("song", "").replace("video", "").strip()
        bot_response = f"playing {query}"
        send_message(user_prompt, bot_response)
        pywhatkit.playonyt(query)
        print(f"Playing {query} on YouTube...")

    # will be used to intereact with wikipedia
    elif "wikipedia who" in user_prompt.lower() or "wikipedia what" in user_prompt.lower():
        query = user_prompt.lower().replace("bot who", "").replace("bot what", "").replace("is", "").strip()
        try:
            info = wikipedia.summary(query, 1)
            pattern = r'\([^()]*\)'  # Regex pattern to match parentheses and their contents
            bot_response = re.sub(pattern, ' ', info)  # Replace matched pattern with whitespace
            send_message(user_prompt, bot_response)
            speak(bot_response)
        except sr.UnknownValueError:
            bot_response = "couldn't find what you need"
            speak(bot_response)
            send_message(user_prompt, bot_response)

    # will be used to access date and time from the device
    elif "what" in user_prompt.lower() and ("time" in user_prompt.lower() or "date" in user_prompt.lower()):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%I:%M %p")
        bot_response = f"The date is {date} and the time is {time}"
        send_message(user_prompt, bot_response)
        speak(bot_response)

    # will be used to perform any basic mathematical calculations
    elif re.match(r"[0-9+\-*/()\s]+", user_prompt):
        try:
            result = eval(user_prompt)
            bot_response = f"The result is: {result}"
            send_message(user_prompt, bot_response)
            speak(bot_response)
        except:
            bot_response = "Sorry, I couldn't evaluate the expression."
            send_message(user_prompt, bot_response)
            speak(bot_response)

    # will be used to set reminders and alarms
    elif "weather report" in user_prompt.lower():
        location = extract_location(user_prompt)
        bot_response = weather.get_weather(location)
        send_message(user_prompt, bot_response)
        speak(bot_response)

    # means user wants to interact with the chatbot
    else:
        bot_response = main.generate_response(user_prompt)
        send_message(user_prompt, bot_response)
        speak(bot_response)
        text_input.delete("1.0", "end")  # Clear the text area


##################################################################################################################

########################### CHECKING FOR USER CHOICE (TEXT OR VOICE) ##############################################
# Process user input from the text area
def process_text_input(event=None):
    user_prompt = text_input.get("1.0", "end-1c")
    if user_prompt.lower() in ['stop', 'quit', 'exit', 'bye', 'sayonara']:
        rand_val = random.choice(exit_responses)
        send_message(user_prompt, rand_val)
        speak(bot_response)
        exit()
    else:
        functionalities(user_prompt)
        print("tracked:", user_prompt)
        text_input.delete("1.0", "end")  # Clear the text area


# Process user input from voice recognition
def process_voice_input():

    with sr.Microphone() as source:
        print("Listening...")
        window.after(1000, winsound.Beep(500, 500))
        audio = recognizer.listen(source)
    try:
        user_prompt = recognizer.recognize_google(audio)
        functionalities(user_prompt)
    except sr.UnknownValueError:
        speak("What did you say?")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.say("Something went wrong")


#########################################################################################################


############################################### GUI #####################################################


window = tk.Tk()
window.title("MINI PROJECT VIRTUAL ASSISTANT")

# Set the size and position of the window
window.geometry("500x500")  # width x height
window.resizable(True, True)  # Disable window resizing

gif_image = Image.open("C:/Users/Robin Bohra/Desktop/B.Tech Projects/My_ChatBot/background.gif")
frames = []
for frame in ImageSequence.Iterator(gif_image):
    frame = frame.resize((500, 500))
    frames.append(ImageTk.PhotoImage(frame))

background_label = tk.Label(window)
background_label.pack()


def update_frame(index):
    frame = frames[index]
    background_label.configure(image=frame)
    window.after(100, update_frame, (index + 1) % len(frames))


update_frame(0)

chat_frame = tk.Frame(window)
chat_frame.place(relx=0.5, rely=0.21, anchor=tk.CENTER)


chat_display = tk.Text(chat_frame, height=10, width=46)
chat_display.pack()
chat_display.configure(state='disabled')  # Disable editing the chat display

text_frame = tk.Frame(window)
text_frame.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

text_input = tk.Text(text_frame, height=1.3, width=42, font=("Arial", 12))
text_input.pack()
text_input.bind("<Return>", process_text_input)  # Bind Enter key press to process_text_input function

generate_button = tk.Button(window, text="CHAT", command=process_text_input, width=15, bg="#4CAF50", fg="white",
                            font=("Arial", 12, "bold"))
generate_button.place(relx=0.35, rely=0.75, anchor=tk.CENTER)

voice_button = tk.Button(window, text="VOICE", command=process_voice_input, width=15, bg="#FE0000", fg="white",
                         font=("Arial", 12, "bold"))
voice_button.place(relx=0.64, rely=0.75, anchor=tk.CENTER)

window.mainloop()

##########################################################################################################
