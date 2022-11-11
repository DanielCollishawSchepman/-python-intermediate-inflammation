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
    return np.loadtxt(fname=filename, delimiter=',')


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
        raise ValueError('Inflammation values should not be negative')

    if type(data) is not np.ndarray:
        raise TypeError('Input data should be a numpy array.')

    if len(np.shape(data)) != 2:
        raise TypeError('Input data should be a 2D array.')

    maxima = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / maxima[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised


# def attach_names(data, names):
#     """
#     Returns a list of dictionaries, each dictionary containing the patient's
#     name and corresponding data.

#     :param data: A list containing lists of patient data.
#     :param names: A list of patients' names.
#     :returns: A list of dictionaries containing patients' names and
#     corresponding data.
#     """
#     attached_names = []

#     for name, datum in zip(names, data):
#         attached_names += [{"name": name, "data": datum}]

#     return attached_names



# # print(attach_names([[1, 2, 3], [2, 3, 4]], ["Alice", "Bob"]))

# class Book:
#     def __init__(self, title, author) -> None:
#         self.title = title
#         self.author = author
    
#     def __str__(self) -> None:
#         return f"{self.title} by {self.author}"

#     def __eq__(self, other):
#         return self.title == other.title and self.author == other.author


# class Library:
#     def __init__(self) -> None:
#         self.books = []

#     def add_book(self, title, author):
#         self.books += [Book(title, author)]

#     def by_author(self, name):
#         matches = []
#         for book in self.books:
#             if book.author == name:
#                 matches += [book]

#         if matches == []:
#             raise KeyError("Author does not exist")
#         return matches

#     def union(self, other):
#         new_library = Library()
#         for book in self.books:
#             if book not in new_library.books:
#                 new_library.books += [book]
#         for book in other.books:
#             if book not in new_library.books:
#                 new_library.books += [book]
#         return new_library

#     @property
#     def titles(self):
#         titles = []
#         for book in self.books:
#             titles += [book.title]

#         return titles
    
#     @property
#     def authors(self):
#         authors = []
#         for book in self.books:
#             if book.author not in authors:
#                 authors += [book.author]
        
#         return authors

#     def __len__(self):
#         return len(self.books)

#     def __getitem__(self, idx):
#         return self.books[idx]

# # book = Book("A Book", "Me")
# # print(book)


# library = Library()
# library2 = Library()

# library.add_book('My First Book', 'Alice')
# library2.add_book('My First Book', 'Alice')
# library2.add_book('My Second Book', 'Alice')
# library2.add_book('A Different Book', 'Bob')

# library3 = library.union(library2)

# print(library3.titles)
# print(library3.authors)


class Observation:
    def __init__(self, day, value):
        self.day = day
        self.value = value

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.day == other.day and self.value == other.value


class Person:
    def __init__(self, name) -> None:
        self.name = name


class Doctor(Person):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.patients = []

    def add_patient(self, patient):
        self.patients += [patient]


class Patient(Person):
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


# from functools import reduce

# import multiprocessing

# def sum_of_squares(sequence):
#     # squares = [int(x) * int(x) for x in sequence if str(x)[0] != "#"]
#     return(reduce((lambda a, b: a + b), sequence))

# def square(value):
#     return value * value

# arr = range(100000000)

# with multiprocessing.Pool(4) as p:
#     squares = p.map(square, arr)

#     print(sum_of_squares(squares))


# with multiprocessing.Pool(5) as p:
#     squares = p.imap(sum_of_squares, arr)

#     print(squares)

# squares = map(square, arr)
# print(sum_of_squares(squares))
# multiprocessing.Pool().map(sum_of_squares, [1, 2, 3])

# print(sum_of_squares([0]))
# print(sum_of_squares([1]))
# print(sum_of_squares([1, 2, 3]))
# print(sum_of_squares([-1]))
# print(sum_of_squares([-1, -2, -3]))
# print(sum_of_squares(['1', '2', '3']))
# print(sum_of_squares(['-1', '-2', '-3']))
# print(sum_of_squares(['1', '2', '#100', '3']))
