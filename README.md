# Zone4

Zone4 is a Python library for interacting with the Apart Zone4 pre-amplifier over serial.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install zone4.

```bash
pip install zone4
```

## Usage
```python
import asyncio
from zone4 import Zone4Manager

async def set_volume(manager, zone, volume):
	await manager.zone(zone).set_volume(volume)

async def update(manager, loop):
	await manager.update()
	loop.create_task(update(manager, loop))

if __name__ == '__main__':
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)

  manager = Zone4Manager('/dev/ttyS3')

  loop.run_until_complete(manager.setup())

  loop.create_task(set_volume(manager, 'a', 55))
  loop.create_task(update(manager, loop))

  loop.run_forever()
  loop.close()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)