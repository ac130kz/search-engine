import pickle
import pyzstd
import time
import os


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(f"{method.__name__}:  {(te - ts) * 1000} ms")
        return result
    return timed


@timeit
def load_index(filename="index.zstd", low_mem=False):
    options = {pyzstd.DParameter.windowLogMax: 26 if low_mem else 30}
    with pyzstd.ZstdFile(filename, level_or_option=options) as f:
        index = pickle.load(f)
    return index


@timeit
def save_index(index, filename="index", low_mem=False):
    options = {pyzstd.CParameter.nbWorkers: os.cpu_count(),
               pyzstd.CParameter.jobSize: 10_000 if low_mem else 50_000,
               pyzstd.CParameter.compressionLevel: 5}
    with pyzstd.ZstdFile(f"{filename}.zstd", "w", level_or_option=options) as f:
        pickle.dump(index, f, protocol=-1)
