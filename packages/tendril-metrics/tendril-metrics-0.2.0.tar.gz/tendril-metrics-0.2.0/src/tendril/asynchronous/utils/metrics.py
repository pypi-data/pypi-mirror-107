

import datetime
from twisted import logger

from tendril.asynchronous.utils.logger import TwistedLoggerMixin
from tendril.asynchronous.contextmanagers.influxdb import InfluxDBAsyncBurstWriter
from tendril.config import METRICS_INFLUXDB_BUCKET
from tendril.config import METRICS_INFLUXDB_TOKEN


class MetricsLoggerMixin(TwistedLoggerMixin):
    def __init__(self, *args, **kwargs):
        self._metrics_loggers = {}
        super(MetricsLoggerMixin, self).__init__(*args, **kwargs)

    def observers(self):
        rv = TwistedLoggerMixin.observers(self)
        rv.append(self._metrics_log_observer)
        return rv

    @property
    def metrics_loggers(self):
        return self._metrics_loggers

    def metrics_logger(self, namespace):
        if namespace not in self._metrics_loggers.keys():
            self._metrics_loggers[namespace] = logger.Logger(
                namespace="metrics.{0}".format(namespace), source=self
            )
        return self._metrics_loggers[namespace]

    def _metrics_log_observer(self, event):
        if event['log_namespace'].split('.')[0] == "metrics":
            metrics = [x for x in event.keys() if not x.startswith('log_')]
            publishable = {"{0}.{1}".format(event['log_namespace'], x):
                               event[x] for x in metrics}
            ts = datetime.datetime.utcfromtimestamp(event['log_time'])
            with InfluxDBAsyncBurstWriter(bucket=METRICS_INFLUXDB_BUCKET,
                                          token=METRICS_INFLUXDB_TOKEN) as writer:
                for metric, value in publishable.items():
                    _parts = metric.split('.')
                    measurement = _parts[2]
                    namespace = _parts[1]
                    writer.write(measurement=measurement,
                                 tags={"namespace": namespace},
                                 fields={"value": value},
                                 ts=ts)
