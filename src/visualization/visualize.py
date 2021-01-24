import pandas as pd
import pandas_flavor as pf
import seaborn as sns

from typing import (
    Callable,
    Mapping
)

@pf.register_dataframe_method
def experiment_plot(
    df: pd.DataFrame,
    func: Callable,
    x: str="frame",
    y: str="value",
    row: str="variable",
    col: str="experiment_id",
    xlabel: str="Frame",
    ylabel: str="Value",
    func_kwargs: Mapping=None,
    **kwargs
) -> sns.axisgrid.FacetGrid:

    return(
        df
        .facet_grid_plot(
            func=func,
            x=x,
            y=y,
            func_kwargs=func_kwargs,
            row=row,
            col=col,
            **kwargs
        )
        .set_axis_labels(xlabel, ylabel)
    )

@pf.register_dataframe_method
def facet_grid_plot(
    df: pd.DataFrame,
    func: Callable,
    x: str,
    y: str,
    func_kwargs: Mapping=None,
    **kwargs
) -> sns.axisgrid.FacetGrid:

    if func_kwargs is None:
        func_kwargs = {}

    return (
        sns.FacetGrid(
            data=df,
            **kwargs
        )
        .map_dataframe(
            func=func,
            x=x,
            y=y,
            **func_kwargs
        )
    )