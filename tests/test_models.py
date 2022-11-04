"""Tests for statistics functions within the Model layer."""

import numpy as np
import numpy.testing as npt
import pytest

# write at least two new test cases that test the daily_max() and daily_min()
# functions, adding them to test/test_models.py. Here are some hints:

# You could choose to format your functions very similarly to daily_mean(),
# defining test input and expected result arrays followed by the equality
# assertion.

# Try to choose cases that are suitably different, and remember that these
# functions take a 2D array and return a 1D array with each element the result
# of analysing each column of the data.


@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0], [0, 0], [0, 0]], [0, 0]),
        ([[1, 2], [3, 4], [5, 6]], [3, 4]),
    ])
def test_daily_mean(test, expected):
    """Test mean function works for array of zeroes and positive integers."""
    from inflammation.models import daily_mean
    npt.assert_array_equal(daily_mean(np.array(test)), np.array(expected))


@pytest.mark.parametrize(
    "test, expected",
    [
        ([[1, 2], [1, 2], [1, 2]], [1, 2]),
        ([[1, 2], [2, 0], [3, 5]], [1, 0]),
    ])
def test_daily_min(test, expected):
    """Test that min function works for an array of equal integers."""
    from inflammation.models import daily_min
    npt.assert_array_equal(daily_min(test), expected)


@pytest.mark.parametrize(
    "test, expected",
    [
        ([[1, 2], [1, 2], [1, 2]], [1, 2]),
        ([[1, 2], [2, 0], [3, 5]], [3, 5]),
    ])
def test_daily_max(test, expected):
    """Test that max function works for an array of equal integers."""
    from inflammation.models import daily_max
    npt.assert_array_equal(daily_max(test), expected)


def test_daily_min_string():
    """Test for TypeError when passing strings"""
    from inflammation.models import daily_min

    with pytest.raises(TypeError):
        error_expected = daily_min([['Hello', 'there'], ['General', 'Kenobi']])
