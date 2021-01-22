import pandas as pd
import pandas_flavor as pf

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

@pf.register_dataframe_method
def center_frames(df, by, frame_col):
    return (
        df
        .groupby(by=by)
        .apply(lambda group:
            group.assign(frame=lambda x: x[frame_col] - x[frame_col].min())
        )
        .assign(**{frame_col: lambda x: x.frame.astype(int)})
        .reset_index(drop=True)
    )
