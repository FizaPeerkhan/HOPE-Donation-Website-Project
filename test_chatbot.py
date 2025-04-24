import json
import joblib
import random
from sklearn.feature_extraction.text import CountVectorizer

# Load the trained chatbot model
model = joblib.load("chatbot_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
labels = joblib.load("labels.pkl")

# Load intents.json
with open("intents.json", "r") as file:
    intents = json.load(file)

# Function to get chatbot response
def chatbot_response(user_input):
    X_test = vectorizer.transform([user_input])
    predicted_label = model.predict(X_test)[0]
    response_tag = labels[predicted_label]
    
    # Find the matching response in intents.json
    for intent in intents["intents"]:
        if intent["tag"] == response_tag:
            return random.choice(intent["responses"])

    return "I'm sorry, I didn't understand that."

# Test the chatbot
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Chatbot: Goodbye! 👋")
        break

    response = chatbot_response(user_input)
    print(f"Chatbot: {response}")
