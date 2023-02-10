def clamp(n, minn, maxn):
  return max(min(maxn, n), minn)

sourceMap = {
  "04": "A",
  "03": "B",
  "02": "C",
  "01": "D",
}

class Zone4Output:
  def __init__(self, zone_id, parent):
    self._parent = parent
    self._zone_id = zone_id
    self._volume = 0
    self._mic_volume = 0
    self._channel = '04'
    self._mute = '01'
    self._mic_mute = '03'
    self._bass = 0
    self._treble = 0

  def _decorate_message(self, message):
    return self._zone_id + message

  async def _send_message(self, message):
    await self._parent._send_message(self._decorate_message(message))

  def _request_state_messages(self):
    return [
      self._decorate_message('R 2'), # Mute
      self._decorate_message('R 3'), # Treble
      self._decorate_message('R 4'), # Bass
      self._decorate_message('R 5'), # Source
      self._decorate_message('R 6'), # Volume
      self._decorate_message('R 7'), # Mic Volume
      self._decorate_message('R 8')  # Mic Mute
    ]

  # Volume
  def _set_volume(self, volume):
    self._volume = clamp(volume, 0, 79)

  async def set_volume(self, volume):
    self._set_volume(volume)

    await self._send_message("V" + str(self._volume).zfill(2))

  def get_volume(self):
    return self._volume

  # Mic Volume
  def _set_mic_volume(self, volume):
    self._mic_volume = clamp(volume, 0, 79)

  async def set_mic_volume(self, volume):
    self._set_mic_volume(volume)

    await self._send_message("C" + str(self._mic_volume).zfill(2))

  def get_mic_volume(self):
    return self._mic_volume

  # Channel
  def _set_channel(self, channel):
    if channel.upper() in sourceMap.values(): 
      self._channel = list(sourceMap.keys())[list(sourceMap.values()).index(channel.upper())]

    if channel in sourceMap:
      self._channel = channel

  async def set_channel(self, channel):
    self._set_channel(channel)

    await self._send_message("S" + self._channel)

  def get_channel(self):
    return sourceMap[self._channel]

  # Mute
  def _set_mute(self, mute):
    if mute in ['01', '02']:
      self._mute = mute
    else:
      self._mute = '01' if mute else '02'

  async def set_mute(self, mute):
    self._set_mute(mute)

    await self._send_message("M" + self._mute)

  def get_mute(self):
    return True if self._mute == '01' else False

  # Mic Mute
  def _set_mic_mute(self, mute):
    if mute in ['03', '04']:
      self._mic_mute = mute
    else:
      self._mic_mute = '03' if mute else '04'

  async def set_mic_mute(self, mute):
    self._set_mic_mute(mute)

    await self._send_message("M" + self._mic_mute)

  def get_mic_mute(self):
    return True if self._mic_mute == '03' else False

  # Bass
  def _set_bass(self, bass):
    self._bass = clamp(bass, -7, 7)

  async def set_bass(self, bass):
    self._set_bass(bass)

    await self._send_message("U" + str(self._bass).rjust(2))

  def get_bass(self):
    return self._bass

  # Treble
  def _set_treble(self, treble):
    self._treble = clamp(treble, -7, 7)

  async def set_treble(self, treble):
    self._set_treble(treble)

    await self._send_message("U" + str(self._treble).rjust(2))

  def get_treble(self):
    return self._treble
