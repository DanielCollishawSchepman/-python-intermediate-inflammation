"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""

import numpy as np


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load.
    :returns: Numpy array of the CSV data.
    """
    return np.loadtxt(fname=filename, delimiter=",")


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array.

    :param data: A 2D inflammation data array.
    :returns: An array of daily mean values.
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2D inflammation data array.

    :param data: A 2D inflammation data array.
    :returns: An array of daily max values.
    """
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2D inflammation data array.

    :param data: A 2D inflammation data array.
    :returns: An array of daily min values.
    """
    return np.min(data, axis=0)


def patient_normalise(data):
    """
    Normalise patient data from a 2D inflammation data array.

    NaN values are ignored, and normalised to 0.

    Negative values are rounded to 0.
    """
    if np.any(data < 0):
        raise ValueError("Inflammation values should not be negative")

    if type(data) is not np.ndarray:
        raise TypeError("Input data should be a numpy array.")

    if len(np.shape(data)) != 2:
        raise TypeError("Input data should be a 2D array.")

    maxima = np.nanmax(data, axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        normalised = data / maxima[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised


class Observation:
    """A class containing the data for an observation.

    Attributes:
    day: integer
        The day on which the observation was made.
    value: float
        The value of the inflammation recorded during the observation.
    """
    def __init__(self, day, value):
        self.day = day
        self.value = value

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.day == other.day and self.value == other.value


class Person:
    """A class containing information about a person.

    Attributes:
    name: str
        The name of the person
    """
    def __init__(self, name) -> None:
        self.name = name


class Doctor(Person):
    """A class containing information about a Doctor.
       Inherits from Person.

    Attributes:
    patients: List[str]
        A list of patients which this Doctor cares for

    Methods:
    add_patient(self, patient):
        Appends a patient to the list of patients cared for by the Doctor
    """
    def __init__(self, name) -> None:
        super().__init__(name)
        self.patients = []

    def add_patient(self, patient):
        self.patients += [patient]


class Patient(Person):
    """A class storing information about a patient.

    Attributes:
    observations: List[observations]
        A list of observations for this patient, in the form Day : Value
    
    Methods:
    add_observation(self, value, day):
        Adds an observation to the list of the patient's observations.
        If no day is provided, it defaults to zero if it is the first item in the list
        Or otherwise it is the previous day iterated by 1.

    """
    def __init__(self, name, observations=None) -> None:
        super().__init__(name)
        self.observations = []
        if observations is not None:
            self.observations = observations

    def add_observation(self, value, day=None):
        if day is None:
            try:
                day = self.observations[-1].day + 1

            except IndexError:
                day = 0

        new_observation = Observation(day, value)

        self.observations.append(new_observation)
        return new_observation

    def __eq__(self, other):
        if self.name != other.name:
            return False

        for self_obs, other_obs in zip(self.observations, other.observations):
            if self_obs == other_obs:
                continue
            return False

        return True
