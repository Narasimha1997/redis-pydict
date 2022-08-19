"""
This class is taken from the following answer from StackOverflow
https://stackoverflow.com/a/66558182/12580609

Written by phani pavan k <kphanipavan@gmail.com>.
use this code as per gplv3 guidelines.
"""


from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep
from types import DynamicClassAttribute


class Loader:
  def __init__(self, desc: str = "Loading...", end: str = "Done!", timeout: int = 0.1):
    """
    A loader-like context manager

    Args:
        desc (str, optional): The loader's description. Defaults to "Loading...".
        end (str, optional): Final print. Defaults to "Done!".
        timeout (float, optional): Sleep time between prints. Defaults to 0.1.
    """
    self.desc = desc
    self.end = end
    self.timeout = timeout

    self._thread = Thread(target=self._animate, daemon=True)
    # self.steps = ["⢿", "⡿", "⣟", "⣻", "⣽", "⣯", "⣷", "⣾", "⣽", "⣻"]
    self.steps = ["⢿⣿", "⡿⣿", "⣿⢿", "⣿⡿", "⣿⣟", "⣿⣻", "⣟⣿", "⣻⣿",
                  "⣽⣿", "⣯⣿", "⣿⣽", "⣿⣯", "⣿⣷", "⣿⣾", "⣷⣿", "⣾⣿", "⣽⣿", "⣻⣿"]
    self.done = False

  def start(self):
    self._thread.start()
    return self

  def _animate(self):
    for c in cycle(self.steps):
      if self.done:
        break
      print(f"\r{self.desc} {c}", flush=True, end="")
      sleep(self.timeout)

  def __enter__(self):
    self.start()

  def stop(self):
    self.done = True
    cols = get_terminal_size((80, 20)).columns
    print("\r" + "" * cols, end="", flush=True)
    # print(f"\r{self.end}", flush=True)

  def __exit__(self, **kwargs: DynamicClassAttribute):
    # handle exceptions with those variables ^
    self.stop()
