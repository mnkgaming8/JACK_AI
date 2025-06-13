import os
import json
import requests
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import wikipedia
import random


# Configuration
CONFIG = {
    "name": "Jack",
    "user": "Client",
    "languages": {
        "english": "en",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "italian": "it",
        "japanese": "ja"
    },
    "default_language": "en",
    "travel_api_key": "your-travel-api-key",  # Replace with actual API key
    "weather_api_key": "your-weather-api-key"  # Replace with actual API key
}

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Set a friendly voice
for voice in voices:
    if "english" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 160)  # Slightly slower for clarity

class JackTravelAssistant:
    def __init__(self):
        self.current_language = CONFIG["default_language"]
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.geolocator = Nominatim(user_agent="JackTravelAssistant")
        self.tf = TimezoneFinder()
        
    def speak(self, text):
        """Convert text to speech"""
        try:
            print(f"{CONFIG['name']}: {text}")
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in speak function: {e}")

    def listen(self):
        """Listen for user input"""
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, phrase_time_limit=8)
            
        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language=self.current_language)
            print(f"{CONFIG['user']}: {query}")
            return query.lower()
        except Exception as e:
            print(f"Error in listen function: {e}")
            return None

    def process_command(self, command):
        """Process travel-related commands"""
        if not command:
            return
            
        # Travel booking commands
        if any(word in command for word in ["book flight", "find flights", "flight to"]):
            self.handle_flight_search(command)
            
        elif any(word in command for word in ["book hotel", "find hotels", "stay in"]):
            self.handle_hotel_search(command)
            
        elif any(word in command for word in ["weather", "forecast"]):
            self.handle_weather_request(command)
            
        elif any(word in command for word in ["time in", "current time"]):
            self.handle_time_request(command)
            
        elif any(word in command for word in ["recommend", "suggest", "what to do"]):
            self.handle_recommendations(command)
            
        elif any(word in command for word in ["budget", "cost", "price"]):
            self.handle_budget_questions(command)
            
        elif any(word in command for word in ["visa", "passport", "requirements"]):
            self.handle_travel_requirements(command)
            
        elif any(word in command for word in ["hello", "hi", "hey"]):
            greetings = [
                f"Hello {CONFIG['user']}! Ready to plan your next adventure?",
                f"Hi there! I'm Jack, your travel assistant. Where shall we go today?",
                f"Greetings! Let's make some travel magic happen!"
            ]
            self.speak(random.choice(greetings))
            
        elif any(word in command for word in ["thank you", "thanks"]):
            self.speak("You're welcome! Happy travels!")
            
        elif any(word in command for word in ["goodbye", "bye"]):
            self.speak("Safe travels! Come back if you need more assistance.")
            return "exit"
            
        else:
            self.speak("I'm not sure I understand. Could you rephrase your travel request?")

    def handle_flight_search(self, query):
        """Handle flight search requests"""
        try:
            # Extract destination from query
            if "to" in query:
                destination = query.split("to")[-1].strip()
            else:
                destination = query.replace("book flight", "").replace("find flights", "").strip()
                
            self.speak(f"Searching for flights to {destination}")
            
            # In a real implementation, you would call a flight API here
            # For demo purposes, we'll simulate this
            flights = [
                {"airline": "Global Airways", "price": "$450", "departure": "08:00 AM", "duration": "2h 30m"},
                {"airline": "Oceanic Airlines", "price": "$390", "departure": "11:30 AM", "duration": "3h 15m"},
                {"airline": "SkyHigh", "price": "$520", "departure": "03:45 PM", "duration": "2h 00m"}
            ]
            
            response = f"I found {len(flights)} flight options to {destination}:\n"
            for i, flight in enumerate(flights, 1):
                response += (f"{i}. {flight['airline']} for {flight['price']} "
                           f"departing at {flight['departure']} ({flight['duration']})\n")
            
            response += "Would you like me to book any of these?"
            self.speak(response)
            
        except Exception as e:
            print(f"Error in flight search: {e}")
            self.speak("Sorry, I couldn't complete the flight search. Please try again.")

    def handle_hotel_search(self, query):
        """Handle hotel search requests"""
        try:
            if "in" in query:
                location = query.split("in")[-1].strip()
            else:
                location = query.replace("book hotel", "").replace("find hotels", "").strip()
                
            self.speak(f"Searching for hotels in {location}")
            
            # Simulated hotel data
            hotels = [
                {"name": "Grand Plaza", "price": "$120/night", "rating": "4.5 stars", "amenities": "pool, spa, free wifi"},
                {"name": "Harbor View Inn", "price": "$85/night", "rating": "4.1 stars", "amenities": "breakfast included"},
                {"name": "Downtown Suites", "price": "$150/night", "rating": "4.7 stars", "amenities": "fitness center, restaurant"}
            ]
            
            response = f"I found {len(hotels)} hotel options in {location}:\n"
            for i, hotel in enumerate(hotels, 1):
                response += (f"{i}. {hotel['name']} for {hotel['price']} "
                           f"({hotel['rating']}, {hotel['amenities']})\n")
            
            response += "Shall I book any of these for you?"
            self.speak(response)
            
        except Exception as e:
            print(f"Error in hotel search: {e}")
            self.speak("Sorry, I couldn't complete the hotel search. Please try again.")

    def handle_weather_request(self, query):
        """Provide weather information"""
        try:
            location = query.replace("weather", "").replace("forecast", "").strip()
            if not location:
                location = "current location"
                
            # In a real implementation, use a weather API
            weather_data = {
                "current": "72°F (22°C), sunny",
                "forecast": [
                    "Tomorrow: 75°F (24°C), partly cloudy",
                    "Day after: 68°F (20°C), chance of rain"
                ]
            }
            
            response = (f"The weather in {location} is currently {weather_data['current']}.\n"
                       f"Forecast for the next days:\n"
                       f"- {weather_data['forecast'][0]}\n"
                       f"- {weather_data['forecast'][1]}")
            self.speak(response)
            
        except Exception as e:
            print(f"Error in weather request: {e}")
            self.speak("Sorry, I couldn't get the weather information. Please try again.")

    def handle_time_request(self, query):
        """Provide timezone information"""
        try:
            location = query.replace("time in", "").replace("current time", "").strip()
            if not location:
                location = "current location"
                
            # Get coordinates for the location
            geo_location = self.geolocator.geocode(location)
            if geo_location:
                timezone_str = self.tf.timezone_at(lng=geo_location.longitude, lat=geo_location.latitude)
                timezone = pytz.timezone(timezone_str)
                current_time = datetime.datetime.now(timezone).strftime("%I:%M %p")
                
                self.speak(f"The current time in {location} is {current_time}")
            else:
                self.speak(f"Sorry, I couldn't find the timezone for {location}")
                
        except Exception as e:
            print(f"Error in time request: {e}")
            self.speak("Sorry, I couldn't determine the time. Please try again.")

    def handle_recommendations(self, query):
        """Provide travel recommendations"""
        try:
            if "in" in query:
                location = query.split("in")[-1].strip()
            else:
                location = query.replace("recommend", "").replace("suggest", "").replace("what to do", "").strip()
                
            # Get Wikipedia summary for the location
            try:
                summary = wikipedia.summary(location, sentences=3)
                self.speak(f"Here's what I found about {location}: {summary}")
            except:
                # Fallback recommendations
                recommendations = [
                    f"In {location}, I recommend visiting the historic city center and trying local cuisine.",
                    f"Top activities in {location} include museum tours and outdoor adventures.",
                    f"When in {location}, don't miss the famous landmarks and shopping districts."
                ]
                self.speak(random.choice(recommendations))
                
            self.speak("Would you like more specific recommendations?")
            
        except Exception as e:
            print(f"Error in recommendations: {e}")
            self.speak("Sorry, I couldn't get recommendations. Please try again.")

    def handle_budget_questions(self, query):
        """Provide budget estimates"""
        try:
            if "for" in query:
                location = query.split("for")[-1].strip()
            else:
                location = "a trip"
                
            # Sample budget data
            budgets = {
                "luxury": "$200-$500 per day",
                "mid-range": "$100-$200 per day",
                "budget": "$50-$100 per day",
                "backpacker": "under $50 per day"
            }
            
            response = (f"For {location}, here are typical daily budgets:\n"
                       f"- Luxury travel: {budgets['luxury']}\n"
                       f"- Mid-range: {budgets['mid-range']}\n"
                       f"- Budget: {budgets['budget']}\n"
                       f"- Backpacker: {budgets['backpacker']}\n"
                       f"Would you like help planning within a specific budget?")
            self.speak(response)
            
        except Exception as e:
            print(f"Error in budget questions: {e}")
            self.speak("Sorry, I couldn't provide budget estimates. Please try again.")

    def handle_travel_requirements(self, query):
        """Provide visa/passport information"""
        try:
            if "for" in query:
                destination = query.split("for")[-1].strip()
            else:
                destination = "your destination"
                
            # Sample requirements
            requirements = [
                f"For {destination}, most travelers need a valid passport with 6 months remaining.",
                f"Visa requirements for {destination} vary by nationality. I can check specifics for you.",
                f"Travel to {destination} typically requires proof of onward travel and sufficient funds."
            ]
            
            self.speak(random.choice(requirements))
            self.speak("Would you like me to check the exact requirements for your nationality?")
            
        except Exception as e:
            print(f"Error in travel requirements: {e}")
            self.speak("Sorry, I couldn't get the travel requirements. Please try again.")

    def run(self):
        """Main execution loop"""
        welcome_messages = [
            f"Hello! I'm Jack, your personal travel assistant. Where shall we go today?",
            f"Welcome aboard! I'm Jack, ready to help plan your perfect trip.",
            f"Greetings, traveler! I'm Jack, your guide to the world's wonders."
        ]
        self.speak(random.choice(welcome_messages))
        
        while True:
            try:
                command = self.listen()
                if command:
                    result = self.process_command(command)
                    if result == "exit":
                        break
            except KeyboardInterrupt:
                self.speak("Happy travels! Until next time.")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                self.speak("Sorry, I didn't catch that. Could you please repeat?")

def streamlit_app():
    import streamlit as st
    st.title("Jack - AI Travel Assistant")
    st.write("Your virtual travel consultant")
    
    assistant = JackTravelAssistant()
    
    if st.button("Start Voice Interaction"):
        assistant.run()
    
    user_input = st.text_input("Or type your travel question here:")
    if user_input:
        assistant.process_command(user_input)

if __name__ == "__main__":
    # To run the console version
    assistant = JackTravelAssistant()
    assistant.run()
    
    # To run the Streamlit app, use this command in terminal:
    # streamlit run jack_app.py