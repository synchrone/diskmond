import os
import re
from time import sleep
from datetime import timedelta
import logging

import click
from pySMART import Device, Attribute, DeviceList
from statsd.defaults.env import statsd

logger = logging.getLogger(__name__)
time_re = re.compile(r'^((?P<hours>[\.\d]+?)h\+)?((?P<minutes>[\.\d]+?)m\+)?((?P<seconds>[\.\d]+?)s)?$')


@click.command()
@click.option('--interval', default='300')
def cli(interval):
    interval = int(os.getenv('DISKMON_INTERVAL', interval))

    device_list = DeviceList()
    while True:
        for dev in device_list.devices:
            assert isinstance(dev, Device)
            dev.update()

            for a in filter(None, dev.attributes):
                assert isinstance(a, Attribute)

                key = f'system.disk.smart.{a.num}_{a.name}.{dev.name}'

                if 's' in a.raw:
                    parts = time_re.match(a.raw)
                    time_components = {name: float(param) for name, param in parts.groupdict().items() if param}
                    value = timedelta(**time_components).total_seconds()
                else:
                    try:
                        value = int(a.raw)
                    except ValueError:
                        logger.warning('cannot parse SMART raw value: %s', a.raw)
                        continue

                statsd.gauge(key, value)
        sleep(interval)


if __name__ == '__main__':
    cli()
