import pytest
import pandas as pd
from pathlib import Path
from .. import get_SRLevels


@pytest.fixture
def sr():
    df = pd.read_csv(Path(__file__).parent / "sr_test.csv")
    return get_SRLevels(df, 0.25, 15)


def test_SRLevels(sr):
    """Testing if the levels are what expected"""
    assert (sr.levels[0].price, sr.levels[0].n_peaks, sr.levels[0].score) == (
        5.825,
        1,
        -2.0,
    )
    assert (sr.levels[1].price, sr.levels[1].n_peaks, sr.levels[1].score) == (
        1.51,
        1,
        -5.0,
    )


def test_supports_resistances_level(sr):
    """Test if the correct supports are provided"""
    # If no support exists, then return 0
    assert sr.get_next_support(1.0) == 0.0
    # Check if the support is the next underlying value
    assert sr.get_next_support(2.0) == sr.levels[1].price
    assert sr.get_next_support(6.0) == sr.levels[0].price

    # If no resistance exists, then return inf
    assert sr.get_next_resistance(6.0) == float("inf")
    # Check if the resistances are correct
    assert sr.get_next_resistance(1.0) == sr.levels[1].price
    assert sr.get_next_resistance(4.0) == sr.levels[0].price
