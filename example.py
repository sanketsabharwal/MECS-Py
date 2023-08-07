import numpy as np
from mecs import MECS
from mecs_visualizer import MECSVisualizer

# Create synthetic data to simulate heart rates of athletes during a training session
np.random.seed(42)
time_series = [np.random.randint(60, 190, 1000) for _ in range(10)]  # Heart rates typically range from 60 to 190 bpm

# Assign each time series to a sport (event class): 'Basketball', 'Soccer', 'Tennis'
classes = np.random.choice(['Basketball', 'Soccer', 'Tennis'], size=10)

# Define tau values for coincidence windows
tau = [5, 10, 15, 20]

# Define aggregation classes: 'Team Sports' (Basketball and Soccer) vs 'Solo Sport' (Tennis)
aggregation_classes = [('Basketball', 'Soccer'), ('Tennis',)]

# Initialize MECS object
mecs = MECS(tau)

# Define macro-event criteria: Heart rate going above 180 bpm
def macro_event_criteria(heart_rate):
    return heart_rate > 180

# Compute results using MECS
macro_events = mecs.identify_macro_events(time_series, macro_event_criteria)
macro_event_results = mecs.compute_macro_event_synchronization(macro_events)
aggregated_macro_event_results = mecs.compute_aggregated_macro_event_synchronization(macro_event_results, aggregation_classes)
intra_class_results = mecs.compute_intra_class_synchronization(time_series, classes)
inter_class_results = mecs.compute_inter_class_synchronization(time_series, classes)
aggregated_inter_class_results = mecs.compute_aggregated_inter_class_synchronization(inter_class_results, aggregation_classes)

# Combine results
results = {
    'intra': intra_class_results,
    'inter': inter_class_results,
    'aggregated': aggregated_inter_class_results,
    'macro': macro_event_results,
    'aggregated_macro': aggregated_macro_event_results
}

final_results = mecs.finalize_results(results)

# Print results
categories = [
    ("Intra-Class Synchronization (e.g., Basketball vs. Basketball)", 'intra'),
    ("Inter-Class Synchronization (e.g., Basketball vs. Tennis)", 'inter'),
    ("Aggregated Inter-Class Synchronization (e.g., Team Sports vs. Solo Sport)", 'aggregated'),
    ("Macro-Event Synchronization (Heart rate > 180 bpm)", 'macro'),
    ("Aggregated Macro-Event Synchronization (e.g., Team Sports' intense moments vs. Solo Sport's intense moments)", 'aggregated_macro')
]

for title, key in categories:
    print(f"\n{title}:")
    for sub_key, value in final_results[key].items():
        print(sub_key, value)

# Visualize results using MECSVisualizer
visualizer = MECSVisualizer(final_results)
visualizer.plot_time_series(time_series, classes)
visualizer.plot_macro_events(time_series, macro_events)
visualizer.heatmap(final_results['intra'], "Intra-Class Synchronization")
visualizer.heatmap(final_results['inter'], "Inter-Class Synchronization")
visualizer.plot_aggregated_results(final_results['aggregated'], "Aggregated Inter-Class Synchronization")
visualizer.plot_aggregated_results(final_results['aggregated_macro'], "Aggregated Macro-Event Synchronization")
