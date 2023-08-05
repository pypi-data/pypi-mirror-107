import datetime
import json
import os
import socket
import sys
import typing

import pandas as pd

from aemeasure.utils.capture import OutputCopy
from aemeasure.utils.git import get_git_revision

git_revision = get_git_revision()


class Measurement(dict):
    _measurement_stack = []

    @staticmethod
    def last() -> dict:
        return Measurement._measurement_stack[-1]

    def time(self, timer=None) -> datetime.timedelta:
        if timer is None:
            return datetime.datetime.now() - self._time
        else:
            return datetime.datetime.now() - self._timer[timer]

    def save_timestamp(self, key="timestamp"):
        self[key] = datetime.datetime.now().isoformat()

    def save_seconds(self, key="runtime", timer=None):
        v = self.time(timer).total_seconds()
        self[key] = v
        return v

    def save_hostname(self, key="hostname"):
        v = socket.gethostname()
        self[key] = v
        return v

    def save_argv(self, key="argv"):
        if sys.argv:
            v = " ".join(sys.argv)
            self[key] = v
            return v
        else:
            self[key] = None
            return None

    def save_git_revision(self, key="git_revision") -> str:
        self[key] = git_revision
        return git_revision

    def save_metadata(self):
        self.save_seconds()
        self.save_timestamp()
        self.save_hostname()
        self.save_argv()
        self.save_git_revision()

    def start_timer(self, name: str):
        self._timer[name] = datetime.datetime.now()

    def __init__(self, path: typing.Optional[str],
                 capture_stdout: typing.Optional[str] = None,
                 capture_stderr: typing.Optional[str] = None):
        super().__init__()
        self._time = datetime.datetime.now()
        self._path = path
        self._timer = dict()
        self._capture_stdout = capture_stdout
        self._capture_stderr = capture_stderr

    def __enter__(self):
        self._measurement_stack.append(self)
        self.start_capture()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_capture()
        self.write()
        e = self._measurement_stack.pop()
        assert e is self

    def start_capture(self):
        if self._capture_stdout:
            sys.stdout = OutputCopy(sys.stdout)
        if self._capture_stderr:
            sys.stderr = OutputCopy(sys.stderr)

    def stop_capture(self):
        if self._capture_stdout:
            self[self._capture_stdout] = sys.stdout.getvalue()
            sys.stdout = sys.stdout.wrapped_stream
        if self._capture_stderr:
            self[self._capture_stderr] = sys.stderr.getvalue()
            sys.stderr = sys.stderr.wrapped_stream

    def write(self):
        if not self._path:
            return
        if os.path.exists(self._path):
            with open(self._path, "r") as f:
                data = json.load(f)
                if not data:
                    data = []
                data.append(self)
            with open(self._path, "w") as f:
                json.dump(data, f)
        else:
            if os.path.dirname(self._path):
                os.makedirs(os.path.dirname(self._path), exist_ok=True)
            with open(self._path, "w") as f:
                json.dump([self], f)


def read_as_pd(path, columns: typing.Optional[typing.List[str]] = None) -> pd.DataFrame:
    with open(path, "r") as f:
        data = json.load(f)
        if type(data) is not list:
            raise ValueError("Expected list of dicts but json file contains", type(data))
        converted_data = dict()
        for i, entry in enumerate(data):
            for key, value in entry.items():
                if columns is None or key in columns:
                    converted_data.setdefault(key, dict())[i] = value
        return pd.DataFrame.from_dict(converted_data, orient='columns')


def query(path: str, query: dict):
    if not os.path.exists(path):
        print("Query on not existing path", path)
        return

    with open(path, "r") as f:
        data = json.load(f)
        if type(data) is not list:
            raise ValueError("Expected list of dicts but json file contains", type(data))

    def compare(e: dict, q: dict):
        for k, v in q.items():
            if e.setdefault(k, None) != v:
                return False
        return True

    for entry in data:
        if compare(entry, query):
            yield entry


def exists(path: str, q: dict) -> bool:
    for q in query(path, q):
        return True
    return False
