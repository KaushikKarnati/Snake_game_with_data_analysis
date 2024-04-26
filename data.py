import csv
import os

def save_game_data(game_data, file_name="game_data.csv"):
    file_exists = os.path.isfile(file_name)
    with open(file_name, "a", newline='') as csvfile:
        fieldnames = ['game_length', 'score', 'moves', 'death_cause']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write header if file doesn't exist

        writer.writerow(game_data)
