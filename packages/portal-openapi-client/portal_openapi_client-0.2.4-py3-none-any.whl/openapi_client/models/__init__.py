# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from openapi_client.model.company import Company
from openapi_client.model.machine import Machine
from openapi_client.model.machine_counter_reading import MachineCounterReading
from openapi_client.model.machine_state import MachineState
from openapi_client.model.telemetry_value import TelemetryValue
