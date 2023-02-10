#!/usr/bin/env python3
import serial
import time
import asyncio

from zone4 import Zone4Manager

zone = Zone4Manager('/dev/ttyS10')

async def write(loop):
  print("Setting volume")

if __name__ == '__main__':
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)

  loop.run_until_complete(zone.setup())
  loop.run_until_complete(test_write())

  loop.run_forever()
  loop.close()