import pyttsx3
import speech_recognition as sr
from datetime import datetime
import wikipedia
import webbrowser
from BardAI import Bard
import pickle
import random
import logging

logging.basicConfig(filename='./logs/error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

intents = {
    "greetings": {
        "patterns": ["hello", "hi", "hey", "howdy", "greetings", "good morning", "good afternoon", "good evening", "hi there", "hey there", "what's up", "hello there"],
        "responses": ["Hello! How can I assist you?", "Hi there!", "Hey! What can I do for you?", "Howdy! What brings you here?", "Greetings! How may I help you?", "Good morning! How can I be of service?", "Good afternoon! What do you need assistance with?", "Good evening! How may I assist you?", "Hey there! How can I help?", "Hi! What's on your mind?", "Hello there! How can I assist you today?"]
    },
    "goodbye": {
        "patterns": ["bye", "see you later", "goodbye", "farewell", "take care", "until next time", "bye bye", "catch you later", "have a good one", "so long"],
        "responses": ["Goodbye!", "See you later!", "Have a great day!", "Farewell! Take care.", "Goodbye! Until next time.", "Take care! Have a wonderful day.", "Bye bye!", "Catch you later!", "Have a good one!", "So long!"]
    },
    "gratitude": {
        "patterns": ["thank you", "thanks", "appreciate it", "thank you so much", "thanks a lot", "much appreciated"],
        "responses": ["You're welcome!", "Happy to help!", "Glad I could assist.", "Anytime!", "You're welcome! Have a great day.", "No problem!"]
    },
    "apologies": {
        "patterns": ["sorry", "my apologies", "apologize", "I'm sorry"],
        "responses": ["No problem at all.", "It's alright.", "No need to apologize.", "That's okay.", "Don't worry about it.", "Apology accepted."]
    },
    "positive_feedback": {
        "patterns": ["great job", "well done", "awesome", "fantastic", "amazing work", "excellent"],
        "responses": ["Thank you! I appreciate your feedback.", "Glad to hear that!", "Thank you for the compliment!", "I'm glad I could meet your expectations.", "Your words motivate me!", "Thank you for your kind words."]
    },
    "negative_feedback": {
        "patterns": ["not good", "disappointed", "unsatisfied", "poor service", "needs improvement", "could be better"],
        "responses": ["I'm sorry to hear that. Can you please provide more details so I can assist you better?", "I apologize for the inconvenience. Let me help resolve the issue.", "I'm sorry you're not satisfied. Please let me know how I can improve.", "Your feedback is valuable. I'll work on improving."]
    },
    "weather": {
        "patterns": ["what's the weather like?", "weather forecast", "is it going to rain today?", "temperature today", "weather report"],
        "responses": ["The weather today is [weather_description].", "Currently, it's [temperature] degrees with [weather_description].", "The forecast predicts [weather_forecast].", "It might rain today. Don't forget your umbrella!", "The temperature today is [temperature] degrees."]
    },
    "help": {
        "patterns": ["help", "can you help me?", "I need assistance", "support"],
        "responses": ["Sure, I'll do my best to assist you.", "Of course, I'm here to help!", "How can I assist you?", "I'll help you with your query."]
    },
    "time": {
        "patterns": ["what's the time?", "current time", "time please", "what time is it?"],
        "responses": ["It's [current_time].", "The current time is [current_time].", "Right now, it's [current_time]."]
    },
    "jokes": {
        "patterns": ["tell me a joke", "joke please", "got any jokes?", "make me laugh"],
        "responses": ["Why don't we ever tell secrets on a farm? Because the potatoes have eyes and the corn has ears!", "What do you get when you cross a snowman and a vampire? Frostbite!", "Why was the math book sad? Because it had too many problems!"]
    },
    "music": {
        "patterns": ["play music", "music please", "song recommendation", "music suggestion"],
        "responses": ["Sure, playing some music for you!", "Here's a song you might like: [song_name]", "How about some music?"]
    },
    "food": {
        "patterns": ["recommend a restaurant", "food places nearby", "what's good to eat?", "restaurant suggestion"],
        "responses": ["Sure, here are some recommended restaurants: [restaurant_names]", "Hungry? Let me find some good food places for you!", "I can suggest some great places to eat nearby."]
    },
    "news": {
        "patterns": ["latest news", "news updates", "what's happening?", "current events"],
        "responses": ["Let me fetch the latest news for you.", "Here are the top headlines: [news_headlines]", "Stay updated with the latest news!"]
    },
    "movies": {
        "patterns": ["movie suggestions", "recommend a movie", "what should I watch?", "best movies"],
        "responses": ["How about watching [movie_name]?", "Here's a movie suggestion for you.", "Let me recommend some great movies!"]
    },
    "sports": {
        "patterns": ["sports news", "score updates", "latest sports events", "upcoming games"],
        "responses": ["I'll get you the latest sports updates.", "Stay updated with the current sports events!", "Let me check the sports scores for you."]
    },
    "gaming": {
        "patterns": ["video game recommendations", "best games to play", "recommend a game", "gaming suggestions"],
        "responses": ["How about trying out [game_name]?", "Here are some gaming suggestions for you!", "Let me recommend some fun games to play!"]
    },
        "tech_support": {
        "patterns": ["technical help", "computer issues", "troubleshooting", "IT support"],
        "responses": ["I can assist with technical issues. What problem are you facing?", "Let's troubleshoot your technical problem together.", "Tell me about the technical issue you're experiencing."]
    },
    "book_recommendation": {
        "patterns": ["recommend a book", "good books to read", "book suggestions", "what should I read?"],
        "responses": ["How about reading [book_title]?", "I've got some great book recommendations for you!", "Let me suggest some interesting books for you to read."]
    },
    "fitness_tips": {
        "patterns": ["fitness advice", "workout tips", "exercise suggestions", "healthy habits"],
        "responses": ["Staying fit is important! Here are some fitness tips: [fitness_tips]", "I can help you with workout suggestions and fitness advice.", "Let me provide some exercise recommendations for you."]
    },
    "travel_recommendation": {
        "patterns": ["travel suggestions", "places to visit", "recommend a destination", "travel ideas"],
        "responses": ["Looking for travel recommendations? Here are some great destinations: [travel_destinations]", "I can suggest some amazing places for your next travel adventure!", "Let me help you with travel destination ideas."]
    },
    "education": {
        "patterns": ["learning resources", "study tips", "education advice", "academic help"],
        "responses": ["I can assist with educational queries. What subject are you studying?", "Let's explore learning resources together.", "Tell me about your educational goals or questions."]
    },
    "pet_advice": {
        "patterns": ["pet care tips", "animal advice", "pet health", "taking care of pets"],
        "responses": ["Pets are wonderful! Here are some pet care tips: [pet_care_tips]", "I can provide advice on pet health and care.", "Let's talk about your pet and their well-being."]
    },
    "shopping": {
        "patterns": ["online shopping", "buying something", "shopping advice", "product recommendations"],
        "responses": ["I can help you with online shopping. What are you looking to buy?", "Let's find the perfect item for you!", "Tell me what you're interested in purchasing."]
    },
    "career_advice": {
        "patterns": ["job search help", "career guidance", "career change advice", "professional development"],
        "responses": ["I can provide career advice. What specific guidance do you need?", "Let's explore career opportunities together.", "Tell me about your career goals or concerns."]
    },
    "relationship_advice": {
        "patterns": ["relationship help", "love advice", "dating tips", "relationship problems"],
        "responses": ["Relationships can be complex. How can I assist you?", "I can offer advice on relationships and dating.", "Tell me about your relationship situation."]
    },
    "mental_health": {
        "patterns": ["mental health support", "coping strategies", "stress relief tips", "emotional well-being"],
        "responses": ["Mental health is important. How can I support you?", "I can provide guidance for managing stress and emotions.", "Let's talk about strategies for maintaining mental well-being."]
    },
    "language_learning": {
        "patterns": ["language learning tips", "language practice", "learning new languages", "language study advice"],
        "responses": ["Learning a new language can be exciting! How can I assist you?", "I can help with language learning tips and practice.", "Tell me which language you're interested in learning."]
    },
    "finance_advice": {
        "patterns": ["financial planning help", "money management tips", "investment advice", "budgeting assistance"],
        "responses": ["I can provide guidance on financial matters. What specific advice do you need?", "Let's discuss your financial goals and plans.", "Tell me about your financial situation or goals."]
    },
}

info = ['who are you', 'hello', 'tell me about yourself', 'hey', 'hi', 'what is your name']
stopping = ['goodbye', 'bye', 'stop', 'thank you', 'quit']
compliment = ['i like you']




def Wiki(command):
    speak('searching wikipedia')
    command = command.replace('wikipedia', '')
    wikiRes = wikipedia.summary(command, sentences= 3)
    speak("According to Wikipedia")
    print(f"PyBot: {wikiRes}")
    speak(wikiRes)


def greet():
    time  = datetime.now().hour
    if time >= 0 and time < 12:
        speak("Good morning Sir.")
        curTime = 'morning'
    elif time >= 12 and time < 18:
        speak("Good afternoon Sir")
        curTime = 'afternoon'
    else:
        speak('Good evening Sir')
        curTime = 'evening'
    speak("pybot at your service")
    return curTime


def pybot(command):
    if command in info:
        speak("Hello sir, I am Pybot")
        speak("My creator is Shodhan Shetty, and i'm here to assist you.")
    elif command =="how are you":
        speak("I am good. Thank you for asking. Hope you are in a great health too.")
        speak('Dont forget to wear the mask and sanitize yourself reguraly.')


def predict_intent(user_input):
    user_input = user_input.lower()
    loaded_model = pickle.load(open('./model/finalized_model.model', 'rb'))
    loaded_vectorizer = pickle.load(open('./model/vectorizer.pickle', 'rb'))
    
    intent = loaded_model.predict(loaded_vectorizer.transform(["thank you"]))

    return intent


def OpenBrowser(command):

    if 'instagram' in command:
        speak("Opening Instagram")
        print(f"Pybot: Opening instagram...")
        webbrowser.open('https://www.instagram.com/')
        return speak("Opend Instagram Sucessfully")
    elif 'github' in command:
        speak("Opening Github")
        print(f"Pybot: Opening github...")
        webbrowser.open('https://github.com/shodhanshetty14/')
        return speak("Opend Github Sucessfully")
    elif 'youtube' in command:
        speak("Opening Youtube")
        print(f"Pybot: Opening youtube...")
        webbrowser.open('https://www.youtube.com/')
        return speak("Opend Youtube Sucessfully")
    elif 'spotify' in  command:
        speak("Opening Spotify")
        print(f"Pybot: Opening Spotify...")
        webbrowser.open('https://www.spotify.com/')
        return speak("Opend Spotify Sucessfully")
    return speak("Can you please repeat again?")


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    hour = datetime.now().hour
    post_fix = 'AM'
    if hour > 12:
        hour = 24 - hour
        post_fix = 'PM'
    minute = datetime.now().minute
    speak(f"The time is {hour} hours and {minute} minutes {post_fix}")
    # make it to 12 hour format and add AM and PM


def voiceCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"PyBot: listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)
        try:
            print(f'PyBot: Recognizing...')
            q = r.recognize_google(audio, language='english')
            # q = r.recognize_sphinx(audio, language='en-in')
            print(f'Shodhan: {q}')
            # speak(f"Recognised command as {q}")
        except Exception as e:
            logging.error(e)
            # print(f"PyBot: Sorry, can you repeat it again?")
            return 'None'
        return q


def PlayMusic():
    pass


def playMovie():
    pass


if __name__ == '__main__':
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    curTime = greet()
    while True:
        command = voiceCommand().lower()

        if command in  info:
            pybot(command)
        elif command == 'how are you':
            pybot(command)
        elif command in stopping:
            speak("It was good speaking with you. GoodBye Sir ")
            exit()


        if 'wikipedia' in command:
            Wiki(command)

        elif 'open' in command:
            OpenBrowser(command)

        elif "time" in command:
            time()
        elif "search" in command:
            speak(Bard(command))
        elif "code" in command:
            speak("What should i save the file as?")
            name = voiceCommand().lower()
            speak(Bard(command,name))
        elif "play music" in command:
            PlayMusic()

# Need to complete the PlayMusic, PlayMovie & time Function and make some change in the structuring