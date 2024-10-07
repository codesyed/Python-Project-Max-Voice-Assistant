import speech_recognition as sr #for speech to text conversion.
import pyttsx3 #for text to speech conversion (python text to speech).
import webbrowser #for opening Browser when URL opening request form user.
import MusicFile #musics.py file created to map songName with its URL.
import requests #Used for News API to get  OR newsHeadings.
import os #to get api key from os set in Environment variable.
from openai import OpenAI
'''------------------'''
#creating 'engine' named Object of pyttsx3 module for text to speech conversion 
engine = pyttsx3.init()
engine.setProperty('rate', 165)  # Default rate is 200; reducing it slows down the speech
engine.setProperty('volume', 0.9)  # Adjust volume (0.0 to 1.0)

#Function(2) to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

#Function(4) to access News Headings VIA Api
def fetch_news_headlines():
    myNews_api_key = os.getenv('NEWS_API_KEY')
    
    if not myNews_api_key:
        print("API key not found. Please set it in your environment variables.")
        return
    
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={myNews_api_key}"
    response = requests.get(url)
    news_data = response.json()

    # Extract and print headlines
    for article in news_data['articles']:
        speak(article['title'])

# Function to process query via OpenAI
def aiHelp(query):
    print("Query is:", query)  # Print the received query for debugging

    # Retrieve the OpenAI API key from environment variables
    myOpenAI_API_KEY = os.getenv('OPEN_AI_API_KEY')
    
    if not myOpenAI_API_KEY:
        print("API key for OpenAI not found. Please set it in your environment variables.")
        return "API key not found."
    print("OPEN AI API KEY IS : ", myOpenAI_API_KEY)
    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=myOpenAI_API_KEY)

    try:
        # Create a chat completion
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant like Alexa; keep output short."},
                {"role": "user", "content": query}
            ]
        )

        # Return the response content
        return completion.choices[0].message.content

    except Exception as e:
        print("An error occurred while communicating with OpenAI:", e)
        return "Error in processing your request."

#Function(5) to process Choice of Query by User
def ProcessQuery(query):

    if("close yourself" in query): 
        speak("Ok, I am Closing Thank You")
        exit(0)
    elif ("goole" in query):
        speak("Here's the Google for You")
        webbrowser.open("www.google.com")
    elif("linkedin" in query):
        speak("Here's the LinkedIn for You")
        webbrowser.open("www.linkedin.com")
    elif("youtube" in query):
        speak("Here's the YouTube for You")
        webbrowser.open("www.youtube.com")
    elif("mail" in query):
        speak("Here's the Gmail for You")
        webbrowser.open("www.gmail.com")
        
    elif("news" in query):
        speak("Following are the news")
        fetch_news_headlines()
   
    elif(query.startswith("play")):
        list  = query.split(" ")
        song = list[1]
        if(MusicFile.dict.get(song) != None):
            webbrowser.open(MusicFile.dict[song])
        else:
            speak("Sorry this song Not in Library")
    else:
        output = aiHelp(query)
        print("AI HELP: - \n", output)
        speak(output.lower)
    ProcessQuery

#Function(6) to input User's Voice
def takeUserQuery():

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("\nWhat to help........")
    
        # Listen and capture audio from the microphone
        rec_object.adjust_for_ambient_noise(source, duration=0.5)
        audio = rec_object.listen(source, timeout=3, phrase_time_limit=5)
        
        try:
            # Recognize and convert speech to text
            text = rec_object.recognize_google(audio)
            ProcessQuery(text.lower())
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            speak("Error with the recognition service.")
    takeUserQuery


#Main work - Start of Program
if __name__ == "__main__":
    speak("Initializing Max")
    print("Started..............")
    speak("How can i assist you...")

#Continue user's voice Listning
while(1):
        
        #creating object of speech_recognition's Recognizer class
        rec_object = sr.Recognizer()
        print("\nListning......")
        try:
            # Use the microphone as the audio source
            with sr.Microphone() as source:
                rec_object.adjust_for_ambient_noise(source, duration=0.5)
                audio = rec_object.listen(source, timeout=3, phrase_time_limit=5)
                text = rec_object.recognize_google(audio)

                if("max" in text.lower()):
                    speak("Yes how can i help you")
                    takeUserQuery() #fun to process usercls query
        
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            continue