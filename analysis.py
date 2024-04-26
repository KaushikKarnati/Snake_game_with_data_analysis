import pandas as pd
import matplotlib.pyplot as plt

def perform_analysis():
    # Load the data
    df = pd.read_csv("game_data.csv")

    # Display basic statistics
    print(df.describe())

    # Setting up a visually appealing style
    plt.style.use('ggplot')  # Using 'ggplot' for better visual effects

    # Plotting the frequency of death causes
    fig, ax = plt.subplots()
    death_causes = df['death_cause'].value_counts()
    death_causes.plot(kind='bar', color='royalblue', alpha=0.75, ax=ax)
    ax.set_title('Frequency of Death Causes', fontsize=15, fontweight='bold')
    ax.set_xlabel('Death Cause', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(True, linestyle='--', linewidth=0.5, color='grey', alpha=0.5)  # Add grid lines for better readability
    plt.xticks(rotation=45)  # Rotate labels to prevent overlap
    plt.tight_layout()  # Adjust layout to not cut off labels
    plt.show()

    # Scatter plot of score vs game length
    fig, ax = plt.subplots()
    scatter = ax.scatter(df['score'], df['game_length'], color='crimson', alpha=0.6)
    ax.set_title('Score vs Game Length', fontsize=15, fontweight='bold')
    ax.set_xlabel('Score', fontsize=12)
    ax.set_ylabel('Game Length (seconds)', fontsize=12)
    ax.grid(True, linestyle='--', linewidth=0.5, color='grey', alpha=0.5)  # Add grid lines for better readability
    plt.tight_layout()  # Adjust layout to not cut off labels
    plt.show()

if __name__ == "__main__":
    perform_analysis()
