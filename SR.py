import pandas as pd
from dataclasses import dataclass
from .pricelevels import RawPriceClusterLevels, TouchScorer


@dataclass
class SRLevel:
    price: float
    n_peaks: int
    score: str


class SRLevels:
    def __init__(self) -> None:
        self._levels = []

    @property
    def levels(self) -> SRLevel:
        return self._levels

    def get_next_support(self, price: float) -> float:
        support = 0.0
        for level in self._levels:
            if level.price < price:
                support = max(support, level.price)
        return support

    def get_next_resistance(self, price: float) -> float:
        resistance = float("inf")
        for level in self._levels:
            if level.price > price:
                resistance = min(resistance, level.price)
        return resistance

    def add(self, level: SRLevel) -> None:
        self._levels.append(level)


def get_SRLevels(
    df: pd.DataFrame, merge_percent: float = 0.25, bars_for_peak: int = 15
) -> SRLevels:
    """Returns all the SR levels for the given df.
    bars_for peaks are the no. of bars that will cause a price action to a level"""
    assert (
        df.shape[0] > bars_for_peak
    ), "df rows should be greater than min_bars_for peak"
    cl = RawPriceClusterLevels(
        None,
        merge_percent=merge_percent,
        use_maximums=True,
        bars_for_peak=bars_for_peak,
    )
    cl.fit(df)
    levels = cl.levels
    scorer = TouchScorer()
    scorer.fit(levels, df.copy())

    srlevels = SRLevels()
    for level, score in zip(cl.levels, scorer.scores):
        srlevels.add(SRLevel(level["price"], level["peak_count"], score[2].score))
    return srlevels
