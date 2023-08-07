import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class MECSVisualizer:
    def __init__(self, mecs_results):
        self.results = mecs_results

    def plot_time_series(self, time_series, classes):
        for i, ts in enumerate(time_series):
            plt.plot(ts, label=f"Class: {classes[i]}")
        plt.legend()
        plt.title("Time Series Plot")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.savefig("time_series_plot.png")
        plt.close()

    def heatmap(self, data, title):
        # Convert dictionary to 2D DataFrame
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.unstack().unstack()
        sns.heatmap(df, cmap="YlGnBu", annot=True)
        plt.title(title)
        plt.savefig(f"{title}.png")
        plt.close()

    def plot_aggregated_results(self, data, title):
        # Convert tuple keys to string representations
        keys = [str(key) for key in data.keys()]
        values = list(data.values())
        plt.bar(keys, values)
        plt.title(title)
        plt.ylabel("Synchronization Score")
        plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
        plt.tight_layout()  # Ensure that labels fit into the figure
        plt.savefig(f"{title}.png")
        plt.close()


    def plot_macro_events(self, time_series, macro_events):
        for i, ts in enumerate(time_series):
            plt.plot(ts, alpha=0.5)
            plt.scatter(range(len(ts)), ts, c=['red' if t in macro_events[i] else 'blue' for t in ts], s=5)
        plt.title("Macro Events in Time Series")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.savefig("macro_events_plot.png")
        plt.close()
