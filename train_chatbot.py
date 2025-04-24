import json
import random
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split



class ChatbotTrainer:
    def __init__(self, intents_file_path):
        self.intents_file_path = intents_file_path
        self.pipeline = None
        self.intents = self.load_intents()

    def load_intents(self):
        with open(self.intents_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data["intents"]

    def augment_patterns(self, patterns, num_augments=3):
        augmented = []
        synonyms = {
            "donate": ["contribute", "give", "help out"],
            "how": ["in what way", "what's the way to", "can I"],
            "much": ["many", "amount", "how big"],
            "you": ["you guys", "your team", "u"],
            "secure": ["safe", "protected", "secured"],
            "start": ["begin", "initiate", "kick off"],
            "goodbye": ["bye", "see ya", "farewell"],
            "help": ["assist", "guide", "support"],
            "hi": ["hello", "hiii", "hey","hii there","hii"],
            "thank": ["thanks", "thank you"],
            "material": ["supplies", "materials", "items"]

        }

        for pattern in patterns:
            for _ in range(num_augments):
                words = pattern.split()
                new_words = [
                    random.choice(synonyms.get(word.lower(), [word])) for word in words
                ]
                augmented_pattern = " ".join(new_words)
                if random.random() < 0.5:
                    augmented_pattern += random.choice([" 😊", " 🙏", " please", " now?"])
                augmented.append(augmented_pattern)
        return augmented

    def preprocess_data(self):
        X, y = [], []
        for intent in self.intents:
            patterns = intent['patterns']
            if len(patterns) < 5:
                patterns += self.augment_patterns(patterns)
            for pattern in patterns:
                X.append(pattern)
                y.append(intent['tag'])
        return X, y

    def train_model(self):
        X, y = self.preprocess_data()

        # Split data for evaluation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB())
        ])

        param_grid = {
            'tfidf__ngram_range': [(1, 1), (1, 2)],
            'clf__alpha': [0.1, 0.5, 1.0]
        }

        grid_search = GridSearchCV(pipeline, param_grid, cv=3)
        grid_search.fit(X_train, y_train)

        self.pipeline = grid_search.best_estimator_

        # Evaluate
        y_pred = self.pipeline.predict(X_test)
        print("\n📊 Classification Report:\n")
        print(classification_report(y_test, y_pred))


    def save_model(self, filename='chatbot_model.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(self.pipeline, file)
trainer = ChatbotTrainer('intents.json')
trainer.train_model()
trainer.save_model()
