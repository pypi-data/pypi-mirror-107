import datetime as dt
import json
import uuid
from decimal import Decimal

INTEGER_TYPES = ()
FLOAT_TYPES = (Decimal,)
TIME_TYPES = (dt.date, dt.datetime)


class JsonSerializer:
    mimetype = "application/json"

    def default(self, data):
        if isinstance(data, TIME_TYPES):
            return data.isoformat()
        elif isinstance(data, uuid.UUID):
            return str(data)
        elif isinstance(data, FLOAT_TYPES):
            return float(data)

        raise TypeError("Unable to serialize %r (type: %s)" % (data, type(data)))

    def dumps(self, data: dict):
        return json.dumps(
            data,
            default=self.default,
            ensure_ascii=False,
        )
