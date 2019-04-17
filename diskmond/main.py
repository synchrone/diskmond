import os
import re
from time import sleep
from datetime import timedelta
import logging

import click
from pySMART import Device, Attribute, DeviceList

logger = logging.getLogger(__name__)
time_re = re.compile(r'^((?P<hours>[\.\d]+?)h\+)?((?P<minutes>[\.\d]+?)m\+)?((?P<seconds>[\.\d]+?)s)?$')


def get_statsd(use_datadog):
    has_datadog = True
    if use_datadog:
        try:
            from datadog import statsd
        except ImportError:
            has_datadog = False

    if not use_datadog or not has_datadog:
        from statsd.defaults.env import statsd

    try:
        # noinspection PyUnboundLocalVariable
        return statsd
    except NameError:
        raise ModuleNotFoundError('no supported backend found')


@click.command()
@click.option('--interval', default='300')
@click.option('--use-datadog/--no-use-datadog', default=True)
def cli(interval, use_datadog):
    interval = int(os.getenv('DISKMON_INTERVAL', interval))
    statsd = get_statsd(use_datadog)

    device_list = DeviceList()
    while True:
        for dev in device_list.devices:
            assert isinstance(dev, Device)
            dev.update()

            for a in filter(None, dev.attributes):
                assert isinstance(a, Attribute)

                datapoint = {'metric': f'system.disk.smart.{a.num}_{a.name}'}

                if 's' in a.raw:
                    parts = time_re.match(a.raw)
                    time_components = {name: float(param) for name, param in parts.groupdict().items() if param}
                    datapoint['value'] = timedelta(**time_components).total_seconds()
                else:
                    try:
                        datapoint['value'] = int(a.raw)
                    except ValueError:
                        logger.warning('cannot parse SMART raw value: %s', a.raw)
                        continue

                if use_datadog:
                    datapoint['tags'] = ['device:'+dev.name]
                else:
                    datapoint['key'] += '.' + dev.name
                statsd.gauge(**datapoint)
        sleep(interval)


if __name__ == '__main__':
    cli()
