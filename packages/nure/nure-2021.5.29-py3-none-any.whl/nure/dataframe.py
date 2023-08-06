import numpy as np
import pandas as pd
import concurrent.futures
import os

_DEFAULT_N_WORKERS = os.cpu_count() or 4


def parallelize_dataframe(dataframe, func, n_workers=_DEFAULT_N_WORKERS, use_process=False):
    splits = np.array_split(dataframe, n_workers)
    if use_process:
        with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
            processed_splits = executor.map(func, splits)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as executor:
            processed_splits = executor.map(func, splits)

    return pd.concat(processed_splits)
