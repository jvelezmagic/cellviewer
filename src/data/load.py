import numpy as np
import janitor
import pandas as pd
import pandas_flavor as pf

from zipfile import ZipFile
from typing import (
    Any,
    Iterable
)

def read_experiment(
    experiment_file: str,
    experiment_id: Any = None,
    **kwargs
) -> pd.DataFrame:
    """Read and combine multiple files contained in one zipped file.

    Args:
        experiment_file: Zip file name with individual files with the
            of the experiments.
        experiment_id: Unique value that indicates the identifier of the
            experiment. If this is not specified, the name of the zip
            file is used instead.
        kwargs: Extra parameters to pass to the function pd.read_csv().

    Returns:
        Data frame with all the files contained in the compressed file
        with an extra column called 'file_name_id' that serves as an
        indicator of which observations were read from which file.
    """

    zf = ZipFile(file=experiment_file)
    experiment_id = experiment_file if experiment_id is None else experiment_id

    dfs_generator = (
        (pd.read_csv(filepath_or_buffer=zf.open(f.filename), **kwargs)
         .add_columns(
            file_name_id=f.filename,
            experiment_id= experiment_id
         )
        )
        for f in zf.infolist()
    )

    return (pd.concat(dfs_generator, ignore_index=True))

def read_experiments(
    experiment_files: Iterable[str],
    experiment_ids: Iterable[Any] = None,
    **kwargs
) -> pd.DataFrame:
    """Wrapper to read multiple experiment zips.
    """

    if experiment_ids is None:
        experiment_ids = [None] * len(experiment_files)

    experiments_generator = (
        read_experiment(
            experiment_file=x,
            experiment_id=y,
            **kwargs
        ) for x, y in zip(experiment_files, experiment_ids)
    )

    return pd.concat(experiments_generator, ignore_index=True)

# Helper functions -------------------------------------------------------------
@pf.register_dataframe_method
def clean_experiment_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.clean_names(remove_special=True, preserve_original_columns=False)
    df.columns = (
        df.columns
        .str.replace("id", "_id")
        .str.replace("__", "_")
    )

    return df