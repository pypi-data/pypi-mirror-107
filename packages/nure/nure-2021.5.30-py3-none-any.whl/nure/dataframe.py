import numpy as np
import pandas as pd
import concurrent.futures
import os

_DEFAULT_N_WORKERS = os.cpu_count() or 4


def parallelize_dataframe(dataframe, func,
                          executor: concurrent.futures.Executor = None,
                          n_workers=_DEFAULT_N_WORKERS, use_process=False):
    # check if exe is provided
    if executor is None:
        if use_process:
            my_executor = concurrent.futures.ProcessPoolExecutor(max_workers=n_workers)
        else:
            my_executor = concurrent.futures.ThreadPoolExecutor(max_workers=n_workers)
    else:
        my_executor = executor

    splits = np.array_split(dataframe, n_workers)
    processed_splits = my_executor.map(func, splits)

    # if is my exe, then shutdown
    if executor is None:
        my_executor.shutdown()

    return pd.concat(processed_splits)
