# MECS-Py: Multi-Event-Class Synchronization in Python

MECS-Py is a Pythonic implementation of the Multi-Event-Class Synchronization (MECS) algorithm, inspired by the paper [The Multi-Event-Class Synchronization (MECS) Algorithm](https://arxiv.org/abs/1903.09530). This library provides tools to compute synchronization metrics for multi-event-class time series data, making it both intuitive and adaptable for Python projects.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Repository Contents](#repository-contents)
- [Getting Started](#getting-started)
- [License](#license)

<a name="features"></a>
## Features

- **Intra-Class Synchronization**: Compute synchronization within the same event class.
- **Inter-Class Synchronization**: Measure synchronization between different event classes.
- **Macro-Event Identification**: Define and identify significant events within time series data.
- **Aggregated Synchronization**: Aggregate synchronization results for a broader perspective.
- **Visualizations**: Visualize time series data, macro-events, and synchronization results.

<a name="installation"></a>
## Installation

To use MECS-Py, you'll need to have Python installed, along with the following libraries:

- `numpy`
- `matplotlib`
- `seaborn`
- `pandas`

You can install these libraries using `pip`:

```bash
pip install numpy matplotlib seaborn pandas
```

Then, clone this repository or download the provided files (`mecs.py` and `mecs_visualizer.py`) to your project directory.

<a name="core-concepts"></a>
## Core Concepts

### 1. **Tau (`tau`)**:
   - `tau` represents the coincidence windows for each class. It's an array of positive integers that defines the range within which two events are considered to be coinciding.
   - For example, if `tau = [5, 10]`, it means the algorithm will consider events coinciding if they are within a distance of 5 or 10 units from each other.
   - The values of `tau` should be chosen based on the nature of the data and the desired granularity of synchronization detection. Smaller values of `tau` will detect coincidences in tighter windows, while larger values will allow for more flexibility in event alignment.

### 2. **Event Classes**:
   - These are categories or types of events within the time series data. For instance, in a dataset monitoring heart rates of athletes from different sports, each sport can be considered an "event class".
   - Event classes allow the algorithm to distinguish between different types of events and compute synchronization metrics accordingly.

### 3. **Macro-Events**:
   - Significant events or spikes in the time series data that are of particular interest. The criteria for what constitutes a macro-event can be user-defined.
   - Macro-events are useful for focusing on specific patterns or occurrences within the data, filtering out noise or less significant events.

### 4. **Synchronization**:
   - A measure of how two time series (or events within them) align or coincide with each other. High synchronization indicates similar patterns or occurrences.
   - Synchronization values range from 0 to 1, with 1 indicating perfect synchronization and 0 indicating no synchronization.

<a name="repository-contents"></a>
## Repository Contents

### 1. `mecs.py`

The heart of MECS-Py. This script contains the `MECS` class, which encapsulates the logic of the MECS algorithm. With this class, users can:

- Define custom distance metrics and coincidence functions.
- Compute various synchronization metrics.
- Normalize and finalize results.

### 2. `mecs_visualizer.py`

A visualization toolkit tailored for MECS results. The `MECSVisualizer` class offers:

- Time series plotting with event class distinction.
- Macro-event visualization within time series.
- Heatmaps for synchronization results.
- Bar plots for aggregated synchronization scores.

<a name="getting-started"></a>
## Getting Started

### Real-World Example: Monitoring Athletes' Heart Rates (Synthetic Data)

Imagine you're a sports scientist, and you're monitoring the heart rates of multiple athletes during a training session. You want to understand how synchronized their heart rates are, both within and across different sports. Let's walk through how you can achieve this using the MECS algorithm.

### Step 1: Simulating Heart Rate Data

Here, we're simulating the heart rates of 10 athletes over a period of time. Each athlete's heart rate data is represented as a time series.

```python
import numpy as np

# Create synthetic data to simulate heart rates of athletes during a training session
np.random.seed(42)
time_series = [np.random.randint(60, 190, 1000) for _ in range(10)]  # Heart rates typically range from 60 to 190 bpm
```


### Step 2: Assigning Athletes to Sports

Each athlete is assigned to a sport, which we refer to as an "event class".


```python
# Assign each time series to a sport (event class): 'Basketball', 'Soccer', 'Tennis'
classes = np.random.choice(['Basketball', 'Soccer', 'Tennis'], size=10)
```


### Step 3: Setting Up the MECS Algorithm

The `tau` values represent different time windows for which we want to check synchronization. For instance, a `tau` of 5 means we're looking at synchronization within a 5-time unit window.

```python
from mecs import MECS

# Define tau values for coincidence windows
tau = [5, 10, 15, 20]

# Initialize MECS object
mecs = MECS(tau)
```

### Step 4: Identifying Intense Moments (Macro-Events)

A macro-event, in this context, is when an athlete's heart rate goes above 180 bpm, indicating intense physical activity.

```python
# Define macro-event criteria: Heart rate going above 180 bpm
def macro_event_criteria(heart_rate):
    return heart_rate > 180

```

### Step 5: Computing and printing Synchronization Metrics

This section computes various synchronization metrics, such as intra-class synchronization (within the same sport) and inter-class synchronization (between different sports).

```python
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
```

### Step 6: Visualizing the Results

```python
from mecs_visualizer import MECSVisualizer

# Visualize results using MECSVisualizer
visualizer = MECSVisualizer(final_results)
visualizer.plot_time_series(time_series, classes)
visualizer.plot_macro_events(time_series, macro_events)
visualizer.heatmap(final_results['intra'], "Intra-Class Synchronization")
visualizer.heatmap(final_results['inter'], "Inter-Class Synchronization")
visualizer.plot_aggregated_results(final_results['aggregated'], "Aggregated Inter-Class Synchronization")
visualizer.plot_aggregated_results(final_results['aggregated_macro'], "Aggregated Macro-Event Synchronization")
```

Finally, we visualize the results to get a clear understanding of the synchronization patterns among athletes.

<a name="license"></a>
## License

This project is licensed under the MIT License.
