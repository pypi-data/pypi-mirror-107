import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


class OpportunityLoss:
    """
    Main Class for modelling Opportunity Losses
    """

    def __init__(self, rewards, inputs):
        """
        :param rewards: {str: function}
            Deterministic reward function that takes a single dictionary as input, whose keys are a subset of the keys in the random_inputs passed.
        :param inputs: {str: random_generator}
            dictionary of random number generators. These are functions that take a single integer input n and return an array of n randomly
        """

        assert isinstance(rewards,
                          dict), "reward_functions must be a dictionary"
        assert isinstance(
            inputs, dict), "random_value_generators must be a dictionary"
        self.reward_functions = rewards
        # TODO: Allow for dependence of variables in the ramdom inputs.
        self.random_inputs = inputs
        self.options = rewards.keys()
        self.data = pd.DataFrame(
            columns=list(self.random_inputs.keys()) + list(self.options) +
            [option + " opportunity loss" for option in self.options] + ["Optimal Decision"])
        self.colour_map = sns.color_palette("RdBu_r", 7)

    def add_data_points(self, n):
        new_data = pd.DataFrame({key: random_input(n)
                                for key, random_input in self.random_inputs.items()})
        for key, reward_function in self.reward_functions.items():
            new_data[key] = new_data.apply(reward_function, axis=1)
        new_data["Optimal Decision"] = new_data[self.options].apply(
            max, axis=1)
        for key in self.options:
            new_data[key + " opportunity loss"] = new_data["Optimal Decision"] - new_data[key]
        self.data = pd.concat([self.data, new_data],
                              ignore_index=True).astype(float)

    def _generate_single_metric(self, option):
        """
        Generates the expected_loss and std_deviation for a single option
        """

        return {"Expected Loss": np.mean(self.data[option + " opportunity loss"]),
                "Standard Deviation": np.std(self.data[option + " opportunity loss"])}

    def generate_metrics(self):
        """
        Generates the metrics table.
        """
        self.metrics = pd.DataFrame({
            option: self._generate_single_metric(option) for option in self.options})
        return self.metrics.sort_values("Expected Loss", ascending=True, axis=1).round(3).T.style.bar(subset=["Expected Loss"], color='#d65f5f', vmin=0)

    def evaluate_value_of_uncertainty_reduction(self, bins=5):
        """
        Metrics for the evaluation of which random inputs are worth decreasing the uncertainty of
        
        :param bins: integer
        Number of bins to divide the inputs in. Too small a value might cause you to miss certain relations. Too small a value might cause you to overfit to the data.
        """

        savings = {random_input: self.metrics.T["Expected Loss"].min() - self._expected_loss_given_group(
            pd.qcut(self.data[random_input], q=bins, duplicates="drop")) for random_input in self.random_inputs.keys()}
        savings_df = pd.DataFrame({"Savings": savings})
        return savings_df.sort_values(["Savings"], ascending=False).style.bar(color='#5fba7d',
                                                                              vmin=0,
                                                                              vmax=self.metrics.T["Expected Loss"].min())

    def _get_optimal_choices_per_group(self, groups):
        """
        Returns a Dictionary of Optimal Choices per Group
        """
        return self.data[[option + " opportunity loss" for option in self.options]].groupby(groups).progress_apply(np.mean).idxmin(axis=1).to_dict()

    def _expected_loss_given_group(self, groups):
        """
        Returns the expected loss assuming we know exactly in which group we are from the passed Series.
        The series must map the indices in cls.data to the categorical groups
        """
        optimal_choices_per_group = self._get_optimal_choices_per_group(groups)
        return self.data.apply(lambda row: row[optimal_choices_per_group[groups[row.name]]], axis=1).mean()

    def get_optimal_choice_per_group(self, random_input, bins):
        assert random_input in self.random_inputs, "The selected input is invalid. Make sure you typed it correctly, or check in the randow_inputs attribute which ones are available"
        optimal_choices = self._get_optimal_choices_per_group(
            groups=pd.qcut(self.data[random_input], q=bins, duplicates="drop"))
        # Removes the opportunity loss part of the string
        optimal_choices = {key: value[:-17]
                           for key, value in optimal_choices.items()}
        return pd.DataFrame({"Optimal Choice for " + random_input: optimal_choices})

    def plot_loss_distribution(self, options=None):
        """
        Plots the loss function to 
        """
        if options is None:
            options = self.options
        assert set(options) <= set(
            self.options), "You passed choices that were not part of this object's initialization"
        loss_columns = [option + " opportunity loss" for option in options]
        bins = np.linspace(self.data[loss_columns].min().min(),
                           self.data[loss_columns].max().max(),
                           200)
        self.data.hist(column=loss_columns,
                       figsize=(30, 2 * len(options)),
                       density=True,
                       layout=(len(options), 1),
                       sharex=True,
                       bins=bins)
