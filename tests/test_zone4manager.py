from zone4 import Zone4Output, Zone4Manager

import pytest
import mock
import serial
from asyncio import StreamReader, StreamWriter


class TestZone4Manager:
  socket_name = '/dev/ttyS11'

  def encode(self, message):
    return message.encode('utf-8')
  
  @mock.patch('zone4.zone4manager.Zone4Output', autospec=True)
  def test_init(self, output_mock):
    manager = Zone4Manager(self.socket_name)

    myzone = manager.zone('a').get_volume()
    print(manager._zones)

    output_mock.assert_has_calls([
      mock.call('a', manager),
      mock.call('b', manager),
      mock.call('c', manager),
      mock.call('d', manager),
    ])

    assert manager._socket_name == self.socket_name

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_setup(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    mock_open_serial_connection.return_value = (True, True)

    await manager.setup()

    mock_open_serial_connection.assert_called_once_with(
      url=self.socket_name,
      baudrate=9600,
      bytesize=8,
      timeout=2,
      stopbits=serial.STOPBITS_ONE
    )

  def test_internal_decorate_message(self):
    manager = Zone4Manager(self.socket_name)
    test_message = '-1234'
    decorated_message = manager._decorate_message(test_message)

    assert decorated_message == '$' + test_message

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_internal_send_message(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    writer = mock.create_autospec(StreamWriter)
    test_message = '-1234'
    mock_open_serial_connection.return_value = (writer, writer)

    await manager.setup()
    await manager._send_message(test_message)

    writer.write.assert_called_with(self.encode('$' + test_message))
    writer.drain.assert_called_once()

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_internal_send_messages(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    writer = mock.create_autospec(StreamWriter)
    
    test_messages = [
      '-1234',
      '-abcd',
      'xyzva',
      'aV01'
    ]

    mock_open_serial_connection.return_value = (writer, writer)
    await manager.setup()
    await manager._send_messages(test_messages)

    encoded_test_message_calls = []
    for test_message in test_messages:
      encoded_test_message_calls.append(mock.call(self.encode('$' + test_message)))

    writer.write.assert_has_calls(encoded_test_message_calls)
    writer.drain.assert_called_once()

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_request_states(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    writer = mock.create_autospec(StreamWriter)
    mock_open_serial_connection.return_value = (writer, writer)
    
    expected_calls = [
      mock.call(b'$aR 1'), # Power
      mock.call(b'$aR 2'), # Zone 1 Mute
      mock.call(b'$aR 3'), # Zone 1 Treble
      mock.call(b'$aR 4'), # Zone 1 Bass
      mock.call(b'$aR 5'), # Zone 1 Source
      mock.call(b'$aR 6'), # Zone 1 Volume
      mock.call(b'$aR 7'), # Zone 1 Mic Volume
      mock.call(b'$aR 8'), # Zone 1 Mic Mute
      mock.call(b'$bR 2'), # Zone 2 Mute
      mock.call(b'$bR 3'), # Zone 2 Treble
      mock.call(b'$bR 4'), # Zone 2 Bass
      mock.call(b'$bR 5'), # Zone 2 Source
      mock.call(b'$bR 6'), # Zone 2 Volume
      mock.call(b'$bR 7'), # Zone 2 Mic Volume
      mock.call(b'$bR 8'), # Zone 2 Mic Mute
      mock.call(b'$cR 2'), # Zone 3 Mute
      mock.call(b'$cR 3'), # Zone 3 Treble
      mock.call(b'$cR 4'), # Zone 3 Bass
      mock.call(b'$cR 5'), # Zone 3 Source
      mock.call(b'$cR 6'), # Zone 3 Volume
      mock.call(b'$cR 7'), # Zone 3 Mic Volume
      mock.call(b'$cR 8'), # Zone 3 Mic Mute
      mock.call(b'$dR 2'), # Zone 4 Mute
      mock.call(b'$dR 3'), # Zone 4 Treble
      mock.call(b'$dR 4'), # Zone 4 Bass
      mock.call(b'$dR 5'), # Zone 4 Source
      mock.call(b'$dR 6'), # Zone 4 Volume
      mock.call(b'$dR 7'), # Zone 4 Mic Volume
      mock.call(b'$dR 8'), # Zone 4 Mic Mute
    ]

    await manager.setup()
    await manager.request_states()

    writer.write.assert_has_calls(expected_calls)
    writer.drain.assert_called_once()


  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_update_volume(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    reader = mock.create_autospec(StreamReader)
    mock_open_serial_connection.return_value = (reader, reader)

    reader.read.return_value = b'$cV32'

    assert manager.zone('c').get_volume() == 0

    await manager.setup()
    await manager.update()

    assert manager.zone('c').get_volume() == 32

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_update_channel(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    reader = mock.create_autospec(StreamReader)
    mock_open_serial_connection.return_value = (reader, reader)

    reader.read.return_value = b'$bS03'

    assert manager.zone('b').get_channel() == 'A'

    await manager.setup()
    await manager.update()

    assert manager.zone('b').get_channel() == 'B'

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_update_mute(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    reader = mock.create_autospec(StreamReader)
    mock_open_serial_connection.return_value = (reader, reader)

    reader.read.return_value = b'$dM02'

    assert manager.zone('d').get_mute() == True

    await manager.setup()
    await manager.update()

    assert manager.zone('d').get_mute() == False


  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_update_mic_mute(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    reader = mock.create_autospec(StreamReader)
    mock_open_serial_connection.return_value = (reader, reader)

    reader.read.return_value = b'$aM04'

    assert manager.zone('a').get_mic_mute() == True

    await manager.setup()
    await manager.update()

    assert manager.zone('a').get_mic_mute() == False

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_update_treble(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    reader = mock.create_autospec(StreamReader)
    mock_open_serial_connection.return_value = (reader, reader)

    reader.read.return_value = b'$bT-3'

    assert manager.zone('b').get_treble() == 0

    await manager.setup()
    await manager.update()

    assert manager.zone('b').get_treble() == -3

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_update_bass(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    reader = mock.create_autospec(StreamReader)
    mock_open_serial_connection.return_value = (reader, reader)

    reader.read.return_value = b'$cU 6'

    assert manager.zone('c').get_bass() == 0

    await manager.setup()
    await manager.update()

    assert manager.zone('c').get_bass() == 6


  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_malformed_message_start(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    reader = mock.create_autospec(StreamReader)
    mock_open_serial_connection.return_value = (reader, reader)

    reader.read.return_value = b'M02$cV71$aS02'

    await manager.setup()
    await manager.update()

    assert manager.zone('c').get_volume() == 71
    assert manager.zone('a').get_channel() == 'C'

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_malformed_message_middle(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    reader = mock.create_autospec(StreamReader)
    mock_open_serial_connection.return_value = (reader, reader)

    reader.read.return_value = b'$dV45$re$123vq$bS03'

    await manager.setup()
    await manager.update()

    assert manager.zone('d').get_volume() == 45
    assert manager.zone('b').get_channel() == 'B'

  @pytest.mark.asyncio
  @mock.patch('zone4.zone4manager.open_serial_connection', autospec=True)
  async def test_interrupted_message_resume(self, mock_open_serial_connection):
    manager = Zone4Manager(self.socket_name)
    reader = mock.create_autospec(StreamReader)
    mock_open_serial_connection.return_value = (reader, reader)

    reader.read.side_effect = [b'$dV41$bS02$c', b'V21$aM', b'02']

    await manager.setup()
    await manager.update()

    assert manager.zone('d').get_volume() == 41
    assert manager.zone('b').get_channel() == 'C'

    await manager.update()

    assert manager.zone('c').get_volume() == 21

    await manager.update()

    assert manager.zone('a').get_mute() == False
