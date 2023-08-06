import base64
import datetime
import pickle
import zlib
from typing import Any


def pickle_and_base64_decode(data: Any):
    return base64.b64encode(zlib.compress(pickle.dumps(data))).decode("utf-8")


def unpack_base64_encoded_pickle(encoded_pickle: str):
    return pickle.loads(zlib.decompress(base64.b64decode(encoded_pickle)))


def datetime_to_timestamp_ms(dt: datetime.datetime):
    return int(dt.timestamp() * 1000)


def timestamp_ms_to_datetime_str(ts: int, formatter):
    return datetime.datetime.fromtimestamp(ts).strftime(formatter)
