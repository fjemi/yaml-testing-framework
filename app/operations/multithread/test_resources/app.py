import asyncio
import dataclasses as dc
import threading
from time import ctime, time

import yaml

# Global variable to store results from
# executing target functions in threads
THREAD_EXECUTION_RESULTS = []

TYPE_HANDLER = {
  "str": lambda name: f"Hello {name}",
  "NoneType": lambda name: "Hello World",
}


def main_sync(name: str = None) -> str:
  """Returns the greeting hello world. Use as an example for setting up
    functions as targets to be threaded"""
  name_type = type(name).__name__
  if name_type not in TYPE_HANDLER:
    message = f"{name_type} is not a valid input type"
    raise RuntimeError(message)
  handler = TYPE_HANDLER[name_type]
  result = handler(name=name)
  return result


async def main_async(name: str = None) -> str:
  """Returns the greeting hello world. Use as an example for setting up
    functions as targets to be threaded"""
  name_type = type(name).__name__
  if name_type not in TYPE_HANDLER:
    message = f"{name_type} is not a valid input type"
    raise RuntimeError(message)
  handler = TYPE_HANDLER[name_type]
  result = handler(name=name)
  return result


if __name__ == '__main__':
  main_sync()
  asyncio.run(main_async())
