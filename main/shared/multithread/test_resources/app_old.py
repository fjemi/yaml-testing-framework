import asyncio
import dataclasses as dc
import threading
from time import ctime, time

import yaml

# Global variable to store results from
# executing target functions in threads
STORE = []


@dc.dataclass
class Time:
  start: str | float | None = None
  end: str | float | None = None
  run: str | float | None = None


@dc.dataclass
class Data:
  time: Time = dc.field(default_factory=lambda: Time())
  thread_name: str | None = None


TYPE_HANDLER = {
  "str": lambda name: f"Hello {name}",
  "NoneType": lambda name: "Hello World",
}


def format_time(data: Data) -> str:
  """Calculates process run time, formats time objects, and returns the
    dataclass as a YAML string"""
  data.time.run = f"{(data.time.end - data.time.start) * 1000} ms"
  data.time.start = ctime(data.time.start)
  data.time.end = ctime(data.time.end)
  data = dc.asdict(data)
  data = yaml.dump(data, indent=2)
  return data


def main_sync(name: str = None) -> str:
  """Returns the greeting hello world. Use as an example for setting up
    functions as targets to be threaded"""
  data = Data(time=Time(start=time()))
  data.thread_name = threading.current_thread().name

  name_type = type(name).__name__
  if name_type not in TYPE_HANDLER:
    message = f"{name_type} is not a valid input type",
    raise RuntimeError(message)
  handler = TYPE_HANDLER[name_type]
  result = handler(name=name)
  global STORE
  STORE.append(result)

  data.time.end = time()
  data = format_time(data=data)
  return


async def main_async(name: str = None) -> str:
  """Returns the greeting hello world. Use as an example for setting up
    functions as targets to be threaded"""
  data = Data(time=Time(start=time()))
  data.thread_name = threading.current_thread().name

  name_type = type(name).__name__
  if name_type not in TYPE_HANDLER:
    message = f"{name_type} is not a valid input type"
    raise RuntimeError(message)
  
  handler = TYPE_HANDLER[name_type]
  result = handler(name=name)
  global STORE
  STORE.append(result)

  data.time.end = time()
  data = format_time(data=data)
  # print(data)
  # print(result)
  return


if __name__ == '__main__':
  main_sync()
  asyncio.run(main_async())
