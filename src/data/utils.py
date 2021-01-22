import pandas as pd
import pandas_flavor as pf

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
