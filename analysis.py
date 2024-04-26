import pandas as pd
import matplotlib.pyplot as plt

def perform_analysis():
    df = pd.read_csv("game_data.csv")
    print(df.describe())  # Print basic statistics

    # Plotting the frequency of death causes
    death_causes = df['death_cause'].value_counts()
    death_causes.plot(kind='bar', color='blue', alpha=0.7)
    plt.title('Frequency of Death Causes')
    plt.xlabel('Death Cause')
    plt.ylabel('Frequency')
    plt.show()

    # Scatter plot of score vs game length
    plt.scatter(df['score'], df['game_length'], color='red', alpha=0.5)
    plt.title('Score vs Game Length')
    plt.xlabel('Score')
    plt.ylabel('Game Length (seconds)')
    plt.show()

if __name__ == "__main__":
    perform_analysis()
