import altair as alt
from baguette_bi import bi
from pandas import DataFrame

from .. import datasets, folders


class ViolinPlot(bi.AltairChart):
    name = "Violin Plot"
    folder = folders.other

    def render(self, cars: DataFrame = datasets.cars):
        return (
            alt.Chart(cars)
            .transform_density(
                "Miles_per_Gallon",
                as_=["Miles_per_Gallon", "density"],
                extent=[5, 50],
                groupby=["Origin"],
            )
            .mark_area(orient="horizontal")
            .encode(
                y="Miles_per_Gallon:Q",
                color="Origin:N",
                x=alt.X(
                    "density:Q",
                    stack="center",
                    impute=None,
                    title=None,
                    axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True),
                ),
                column=alt.Column(
                    "Origin:N",
                    header=alt.Header(
                        titleOrient="bottom",
                        labelOrient="bottom",
                        labelPadding=0,
                    ),
                ),
            )
            .properties(width=100)
            .configure_facet(spacing=0)
            .configure_view(stroke=None)
        )
