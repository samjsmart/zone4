from zone4 import Zone4Output, Zone4Manager

import pytest
import mock

class TestZone4Output:
  zone_id = 'a'

  # Messaging
  @pytest.mark.asyncio
  async def test_internal_send_message(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_message = '-1234'

    await output._send_message(test_message)

    mock_manager._send_message.assert_called_with(self.zone_id + test_message)

  def test_internal_decorate_message(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_message = '-1234'
    decorated_message = output._decorate_message(test_message)

    assert decorated_message == self.zone_id + test_message

  def test_internal_request_state_messages(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    
    messages = output._request_state_messages()

    assert messages == [
      self.zone_id + 'R 2',
      self.zone_id + 'R 3',
      self.zone_id + 'R 4',
      self.zone_id + 'R 5',
      self.zone_id + 'R 6',
      self.zone_id + 'R 7',
      self.zone_id + 'R 8',
    ]

  # Volume
  def test_internal_set_volume(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_volume = 32
    output._set_volume(test_volume)

    assert output._volume == test_volume

  def test_internal_set_volume_upper_limit(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_volume = 100
    output._set_volume(test_volume)

    assert output._volume == 79

  def test_internal_set_volume_lower_limit(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_volume = -100
    output._set_volume(test_volume)

    assert output._volume == 0

  def test_get_volume(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_volume = 51
    output._set_volume(test_volume)

    assert output.get_volume() == test_volume

  @pytest.mark.asyncio
  async def test_set_volume(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_volume = 51
    await output.set_volume(test_volume)

    mock_manager._send_message.assert_called_with(self.zone_id + 'V' + str(test_volume))
    assert output.get_volume() == test_volume

  @pytest.mark.asyncio
  async def test_set_volume_padding(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_volume = 1
    await output.set_volume(test_volume)

    mock_manager._send_message.assert_called_with(self.zone_id + 'V0' + str(test_volume))
    assert output.get_volume() == test_volume

  # Mic Volume
  def test_internal_set_mic_volume(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_mic_volume = 32
    output._set_mic_volume(test_mic_volume)

    assert output._mic_volume == test_mic_volume

  def test_internal_set_mic_volume_upper_limit(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_mic_volume = 100
    output._set_mic_volume(test_mic_volume)

    assert output._mic_volume == 79

  def test_internal_set_mic_volume_lower_limit(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_mic_volume = -100
    output._set_mic_volume(test_mic_volume)

    assert output._mic_volume == 0

  def test_get_mic_volume(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_mic_volume = 51
    output._set_mic_volume(test_mic_volume)

    assert output.get_mic_volume() == test_mic_volume

  @pytest.mark.asyncio
  async def test_set_mic_volume(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_mic_volume = 51
    await output.set_mic_volume(test_mic_volume)

    mock_manager._send_message.assert_called_with(self.zone_id + 'C' + str(test_mic_volume))
    assert output.get_mic_volume() == test_mic_volume

  @pytest.mark.asyncio
  async def test_set_mic_volume_padding(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_mic_volume = 1
    await output.set_mic_volume(test_mic_volume)

    mock_manager._send_message.assert_called_with(self.zone_id + 'C0' + str(test_mic_volume))
    assert output.get_mic_volume() == test_mic_volume

  # Channel
  def test_internal_set_channel(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)

    output._set_channel('A')
    assert output._channel == '04'

    output._set_channel('B')
    assert output._channel == '03'

    output._set_channel('C')
    assert output._channel == '02'

    output._set_channel('D')
    assert output._channel == '01'

    output._set_channel('04')
    assert output._channel == '04'

    output._set_channel('03')
    assert output._channel == '03'

    output._set_channel('02')
    assert output._channel == '02'

    output._set_channel('01')
    assert output._channel == '01'

  def test_get_channel(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_channel = 'B'
    output._set_channel(test_channel)

    assert output.get_channel() == test_channel

  @pytest.mark.asyncio
  async def test_set_channel(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)

    await output.set_channel('A')
    mock_manager._send_message.assert_called_with(self.zone_id + 'S04')
    assert output.get_channel() == 'A'

    await output.set_channel('02')
    mock_manager._send_message.assert_called_with(self.zone_id + 'S02')
    assert output.get_channel() == 'C'

  # Mute
  def test_internal_set_mic_mute(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)

    output._set_mic_mute(True)
    assert output._mic_mute == '03'

    output._set_mic_mute(False)
    assert output._mic_mute == '04'

    output._set_mic_mute('03')
    assert output._mic_mute == '03'

    output._set_mic_mute('04')
    assert output._mic_mute == '04'

  def test_get_mic_mute(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    
    output._set_mic_mute(False)
    assert output.get_mic_mute() == False

    output._set_mic_mute('03')
    assert output.get_mic_mute() == True

  @pytest.mark.asyncio
  async def test_set_mic_mute(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)

    await output.set_mic_mute(True)
    mock_manager._send_message.assert_called_with(self.zone_id + 'M03')
    assert output.get_mic_mute() == True

    await output.set_mic_mute(False)
    mock_manager._send_message.assert_called_with(self.zone_id + 'M04')
    assert output.get_mic_mute() == False

  # Bass
  def test_internal_set_bass(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_bass = 5
    output._set_bass(test_bass)

    assert output._bass == test_bass

  def test_internal_set_bass_upper_limit(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)

    output._set_bass(100)

    assert output._bass == 7

  def test_internal_set_bass_lower_limit(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)

    output._set_bass(-100)

    assert output._bass == -7

  def test_get_bass(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_bass = -2
    output._set_bass(test_bass)

    assert output.get_bass() == test_bass

  @pytest.mark.asyncio
  async def test_set_bass(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_bass = -4
    await output.set_bass(test_bass)

    mock_manager._send_message.assert_called_with(self.zone_id + 'U' + str(test_bass))
    assert output.get_bass() == test_bass

  @pytest.mark.asyncio
  async def test_set_bass_padding(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_bass = 2
    await output.set_bass(test_bass)

    mock_manager._send_message.assert_called_with(self.zone_id + 'U ' + str(test_bass))
    assert output.get_bass() == test_bass

  # Treble
  def test_internal_set_treble(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_treble = 5
    output._set_treble(test_treble)

    assert output._treble == test_treble

  def test_internal_set_treble_upper_limit(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)

    output._set_treble(100)

    assert output._treble == 7

  def test_internal_set_treble_lower_limit(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)

    output._set_treble(-100)

    assert output._treble == -7

  def test_get_treble(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_treble = -2
    output._set_treble(test_treble)

    assert output.get_treble() == test_treble

  @pytest.mark.asyncio
  async def test_set_treble(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_treble = -4
    await output.set_treble(test_treble)

    mock_manager._send_message.assert_called_with(self.zone_id + 'U' + str(test_treble))
    assert output.get_treble() == test_treble

  @pytest.mark.asyncio
  async def test_set_treble_padding(self):
    mock_manager = mock.create_autospec(Zone4Manager)
    output = Zone4Output(self.zone_id, mock_manager)
    test_treble = 2
    await output.set_treble(test_treble)

    mock_manager._send_message.assert_called_with(self.zone_id + 'U ' + str(test_treble))
    assert output.get_treble() == test_treble