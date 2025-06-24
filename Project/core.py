import csv
import random
import time

class GameCore:
    def __init__(self):
        self.csv_file = 'data.csv'
        self.typing_data = []
        self.scramble_data = []
        self.load_data()
    
    def load_data(self):
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['game_type'] == 'typing':
                        self.typing_data.append(row['content'])
                    elif row['game_type'] == 'scramble':
                        self.scramble_data.append({
                            'word': row['content'],
                            'hint': row['hint']
                        })
        except FileNotFoundError:
            print(f"Error: {self.csv_file} not found!")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def get_random_typing_sentence(self):
        if self.typing_data:
            return random.choice(self.typing_data)
        return "No typing data available"
    
    def get_random_scramble_word(self):
        if self.scramble_data:
            return random.choice(self.scramble_data)
        return {'word': 'test', 'hint': 'Default word'}
    
    def scramble_word(self, word):
        word_list = list(word.lower())
        original = word_list.copy()
        while word_list == original and len(word) > 1:
            random.shuffle(word_list)
        return ''.join(word_list)
    
    def calculate_wpm(self, text, time_taken):
        if time_taken == 0:
            return 0
        word_count = len(text.split())
        minutes = time_taken / 60
        return round(word_count / minutes, 2)
    
    def calculate_accuracy(self, original, typed):
        if not original:
            return 0
        correct_chars = 0
        total_chars = len(original)
        for i, char in enumerate(original):
            if i < len(typed) and char == typed[i]:
                correct_chars += 1
        accuracy = (correct_chars / total_chars) * 100
        return round(accuracy, 2)

class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.is_running = False
    
    def start(self):
        self.start_time = time.time()
        self.is_running = True
    
    def stop(self):
        if self.is_running:
            self.end_time = time.time()
            self.is_running = False
            return self.get_elapsed_time()
        return 0
    
    def get_elapsed_time(self):
        if self.is_running:
            return time.time() - self.start_time
        return self.end_time - self.start_time if self.end_time > self.start_time else 0
    
    def reset(self):
        self.start_time = 0
        self.end_time = 0
        self.is_running = False