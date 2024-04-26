import json

def load_high_scores(filename="highscores.json"):
    """Load high scores from a specified JSON file. If the file doesn't exist, return an empty list."""
    try:
        with open(filename, 'r') as file:
            high_scores = json.load(file)
            return high_scores
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_high_scores(scores, filename="highscores.json"):
    """Save high scores to a specified JSON file. Overwrite any existing file."""
    try:
        with open(filename, 'w') as file:
            json.dump(scores, file, indent=4)
    except IOError as e:
        print(f"Error saving high scores: {e}")

def update_high_scores(new_score, high_scores):
    """Update the list of high scores with a new score, if it's high enough to be included."""
    high_scores.append(new_score)
    # Sort the list of high scores in descending order by score and limit the list to the top N scores
    high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)[:10]
    return high_scores

def add_new_high_score(name, score, high_scores):
    """Add a new score to the high scores list and save it to the file."""
    new_score = {'name': name, 'score': score}
    updated_scores = update_high_scores(new_score, high_scores)
    save_high_scores(updated_scores)
