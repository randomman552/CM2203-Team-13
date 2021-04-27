from typing import List, Dict, Tuple
import json

import numpy as np

from .models import Stock

"""
Based on:
Author: Jason Brownlee
Published: 2019
Title: Naive Bayes Classifier From Scratch in Python
Available at: https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
Accessed: 26/04/21
"""

SUMMARIES_STORAGE_PATH = "summaries.json"


def get_summary_total(summaries: Dict[str, List[Tuple]], label=None) -> int:
    """
    Method to get the total number of entries in a summaries for a certain category.
    :param summaries: Summaries entries to count
    :param label: The class label to count (if None or not set, will return count of all labels)
    :return: The number of entries with the specified class label
    """
    if label is None:
        total = 0
        for label in summaries:
            total += get_summary_total(summaries, label)
        return total
    else:
        return summaries[label][0][2]


def split_by_class(dataset: List[Stock]) -> Dict[str, List[Stock]]:
    """
    Method to split the given data set by class
    :param dataset: The dataset to split
    :return: A dict of lists, each list corresponding to one class label
    """
    split = dict()

    for stock in dataset:
        class_val = stock.class_val
        if class_val not in split:
            split[class_val] = list()
        split[class_val].append(stock)

    return split


def summarise(dataset: List[Stock]) -> List[Tuple]:
    """
    Summarise the given dataset as a list of tuples.
    :param dataset: The dataset to work on
    :return: A list of tuples in the format (mean, std deviation, length) for each attribute selected from the dataset.
    """
    as_tuples = [stock.as_tuple() for stock in dataset]
    # For each element in the tuples, calculate the mean, std deviation and number of entries.
    summary = [(np.nanmean(column), np.nanstd(column), len(column)) for column in zip(*as_tuples)]
    return summary


def summarise_by_class(dataset: List[Stock]) -> Dict[str, List[Tuple]]:
    """
    Summarise the given dataset segmented by class label.
    :param dataset: The dataset to segment and summarise.
    :return: Dict of summaries for each class label.
    """
    split = split_by_class(dataset)
    summaries = dict()
    for class_val in split:
        subset = split[class_val]
        summaries[class_val] = summarise(subset)
    return summaries


def gaussian_probability(mean, std_dev, x) -> float:
    """
    Gaussian function representing probability density (normally distributed)
    Based on https://en.wikipedia.org/wiki/Gaussian_function
    :param mean: Expected value
    :param std_dev: Standard deviation
    :param x: Value
    :return: Probability that the given value x appears in a normal distribution centered on the mean
    """
    exponent = np.exp(-((x - mean) ** 2 / (2 * std_dev ** 2)))
    return (1 / (np.sqrt(2 * np.pi) * std_dev)) * exponent


def calculate_probabilities(summaries: Dict[str, List[Tuple]], stock: Tuple):
    """
    Calculate the probability that the given stock tuple belongs to each class.
    Probability is not between 0 and 1 as we are using a simplified version of Bayes Theorem without the final division.
    We can do this as only the magnitude of the value produced matters.
    :param summaries: Summarised data set to compare to
    :param stock: The stock to calculate probabilities for
    :return:
    """
    probabilities = dict()
    total_entries = get_summary_total(summaries)

    for class_name in summaries:
        probabilities[class_name] = get_summary_total(summaries, class_name) / total_entries
        summary = summaries[class_name]
        for i in range(len(summary)):
            mean, std_dev, length = summary[i]
            probabilities[class_name] *= gaussian_probability(mean, std_dev, stock[i])

    return probabilities


def classify(summaries: Dict[str, List[Tuple]], stock: Stock):
    """
    Function to classify the given stock into a class of the given summaries dict.
    :param summaries: Summarised data set to compared to
    :param stock: The stock object to classify
    :return: Predicted class label, probability magnitude
    """
    probabilities = calculate_probabilities(summaries, stock.as_tuple())
    cur_max = 0
    final_label = "unknown"

    for label in probabilities:
        if probabilities[label] > cur_max:
            cur_max = probabilities[label]
            final_label = label

    return final_label, cur_max


def get_summaries() -> Dict[str, List[Tuple]]:
    """
    Convenience method to load summaries from file
    :return:
    """
    with open(SUMMARIES_STORAGE_PATH, "r") as f:
        return json.load(f)
