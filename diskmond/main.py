import os
from time import sleep

import click
from pySMART import Device, Attribute, DeviceList
from statsd.defaults.env import statsd


@click.command()
@click.option('--interval', default=1)
def cli(interval):
    interval = os.getenv('DISKMON_INTERVAL', interval)

    device_list = DeviceList()
    while True:
        for dev in device_list.devices:
            assert isinstance(dev, Device)
            dev.update()

            for a in filter(None, dev.attributes):
                assert isinstance(a, Attribute)

                key = f'system.disk.smart.{a.num}_{a.name}.{dev.name}'
                value = int(a.raw)
                statsd.gauge(key, value)
        sleep(interval)


if __name__ == '__main__':
    cli()
