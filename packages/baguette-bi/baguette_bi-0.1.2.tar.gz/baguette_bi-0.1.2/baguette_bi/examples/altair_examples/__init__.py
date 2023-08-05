import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from . import datasets
from .case_studies import *  # NOQA: F401, F403
from .folders import root
from .other import *  # NOQA: F401, F403

alt.data_transformers.disable_max_rows()


class BarChartWithNegativeValues(bi.AltairChart):
    folder = root

    def render(self, us_employment: DataFrame = datasets.us_employment):
        return (
            alt.Chart(us_employment)
            .mark_bar(stroke="white")
            .encode(
                x="month:T",
                y="nonfarm_change:Q",
                color=alt.condition(
                    alt.datum.nonfarm_change > 0,
                    alt.value("steelblue"),  # The positive color
                    alt.value("green"),  # The negative color
                ),
            )
            .properties(width=600, height=500)
        )


class Streamgraph(bi.AltairChart):
    folder = root

    def render(self, source: DataFrame = datasets.unemployment_across_industries):
        return (
            alt.Chart(source)
            .mark_area()
            .encode(
                alt.X(
                    "yearmonth(date):T",
                    axis=alt.Axis(format="%Y", domain=False, tickSize=0),
                ),
                alt.Y("sum(count):Q", stack="center", axis=None),
                alt.Color("series:N", scale=alt.Scale(scheme="category20b")),
            )
            .properties(width=900, height=300)
            .interactive()
        )
