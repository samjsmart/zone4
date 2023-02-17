import math
import time
import asyncio
import serial

from serial_asyncio import open_serial_connection
from zone4 import Zone4Output

class Zone4Manager:
  def __init__(self, socket_name):
    self._zones = {
      'a' : Zone4Output('a', self),
      'b' : Zone4Output('b', self),
      'c' : Zone4Output('c', self),
      'd' : Zone4Output('d', self),
    }
    self._socket_name = socket_name
    self._buffer = bytearray()

  async def setup(self):
    self._reader, self._writer = await open_serial_connection(
      url=self._socket_name,
      baudrate=9600,
      bytesize=8,
      timeout=2,
      stopbits=serial.STOPBITS_ONE
    )

  def _decorate_message(self, message):
    return '$' + message

  async def _send_message(self, message):
    msg = self._decorate_message(message)
    self._writer.write(msg.encode('utf-8'))
    await self._writer.drain()

  async def _send_messages(self, messages):
    for message in messages:
      msg = self._decorate_message(message)
      self._writer.write(msg.encode('utf-8'))
      await asyncio.sleep(0.05)
    
    await self._writer.drain()

  async def request_states(self):
    messages = ["aR 1"]

    for zone in self._zones.values():
      messages += zone._request_state_messages()

    await self._send_messages(messages)

  async def update(self):
    tmp = await self._reader.read(100)
    self._buffer.extend(tmp)

    if(len(self._buffer) >= 5):
      try:
        messages = [x for x in self._buffer.decode("Ascii").split("$") if x]

        for idx, message in enumerate(messages, start=1):
          if len(message) == 4:
            if message[0] in ['a', 'b', 'c', 'd']:
              zone = message[0]

              if message[1] == 'V':
                self._zones[zone]._set_volume(int(message[2:]))

              if message[1] == 'S':
                self._zones[zone]._set_channel(message[2:])

              if message[1] == 'M':
                if message[2:] in ['01', '02']:
                  self._zones[zone]._set_mute(message[2:])
                else:
                  self._zones[zone]._set_mic_mute(message[2:])

              if message[1] == 'T':
                self._zones[zone]._set_treble(int(message[2:]))

              if message[1] == 'U':
                self._zones[zone]._set_bass(int(message[2:]))

          elif idx == len(messages) and len(message) < 4:
            continue # Probably an interrupted message, leave for next iteration

          del self._buffer[:len(message) + 1]
      except UnicodeDecodeError as e:
        self._buffer = bytearray()

  def zone(self, zone_id):
    return self._zones[zone_id]
