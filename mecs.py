import numpy as np

class MECS:
    """Multi-Event-Class Synchronization (MECS) algorithm class."""

    def __init__(self, tau, distance_metric=None, coincidence_function=None):
        self.tau = np.array(tau)
        self.distance_metric = distance_metric or self._default_distance_metric
        self.coincidence_function = coincidence_function or self._default_coincidence_function

    @staticmethod
    def _default_distance_metric(x, y):
        return np.abs(x - y)

    @staticmethod
    def _default_coincidence_function(d, tau_k):
        return (1 - d / tau_k) * (0 <= d) * (d <= tau_k)

    # def _calculate_coincidences(self, TSi, TSj, tau_k):
    #     distances = self.distance_metric(TSi[:, None], TSj)
    #     coincidences = self.coincidence_function(distances, tau_k)
    #     return coincidences

    def _calculate_coincidences(self, TSi, TSj, tau_k):
        TSi = np.array(TSi)
        TSj = np.array(TSj)
        distances = self.distance_metric(TSi[:, None], TSj)
        coincidences = self.coincidence_function(distances, tau_k)
        return coincidences


    def compute_intra_class_synchronization(self, time_series, classes):
        condition = lambda i, j: i != j and classes[i] == classes[j]
        return self._compute_synchronization(time_series, classes, condition)

    def compute_inter_class_synchronization(self, time_series, classes):
        condition = lambda i, j: i != j and classes[i] != classes[j]
        return self._compute_synchronization(time_series, classes, condition)

    def _compute_synchronization(self, time_series, classes, condition):
        results = {}
        for k, tau_k in enumerate(self.tau):
            for i, TSi in enumerate(time_series):
                for j, TSj in enumerate(time_series):
                    if condition(i, j):
                        key = (i, j, classes[i], classes[j]) # Include classes in the key
                        coincidences = self._calculate_coincidences(TSi, TSj, tau_k)
                        results[key] = np.sum(coincidences) / coincidences.size
        return results

    def compute_aggregated_inter_class_synchronization(self, inter_class_results, aggregation_classes):
        results = {}
        if aggregation_classes:
            for agg_class in aggregation_classes:
                aggregated_result = 0
                count = 0
                for key, value in inter_class_results.items():
                    if key[2] in agg_class and key[3] in agg_class:
                        aggregated_result += value
                        count += 1
                if count > 0:
                    results[agg_class] = aggregated_result / count
        return results

    def finalize_results(self, results):
        # Normalizing Results
        for category in results:
            for key in results[category]:
                results[category][key] = results[category][key] / len(self.tau)
        return results

    def identify_macro_events(self, time_series, macro_event_criteria):
        """Identify macro-events based on given criteria."""
        macro_events = []
        for ts in time_series:
            macro_event = [event for event in ts if macro_event_criteria(event)]
            macro_events.append(macro_event)
        return macro_events

    def compute_macro_event_synchronization(self, macro_events):
        """Compute synchronization for macro-events."""
        results = {}
        for k, tau_k in enumerate(self.tau):
            for i, MEi in enumerate(macro_events):
                for j, MEj in enumerate(macro_events):
                    if i != j:
                        key = (i, j)
                        coincidences = self._calculate_coincidences(MEi, MEj, tau_k)
                        results[key] = np.sum(coincidences) / coincidences.size
        return results

    def compute_aggregated_macro_event_synchronization(self, macro_event_results, aggregation_classes):
        """Aggregate synchronization results for macro-events."""
        results = {}
        if aggregation_classes:
            for agg_class in aggregation_classes:
                aggregated_result = 0
                count = 0
                for key, value in macro_event_results.items():
                    if key[0] in agg_class and key[1] in agg_class:
                        aggregated_result += value
                        count += 1
                if count > 0:
                    results[agg_class] = aggregated_result / count
        return results
