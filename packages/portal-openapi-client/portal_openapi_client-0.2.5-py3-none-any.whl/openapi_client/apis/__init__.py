
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.companies_api import CompaniesApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from openapi_client.api.companies_api import CompaniesApi
from openapi_client.api.machinecounterreadings_api import MachinecounterreadingsApi
from openapi_client.api.machines_api import MachinesApi
from openapi_client.api.schema_api import SchemaApi
from openapi_client.api.states_api import StatesApi
from openapi_client.api.telemetry_api import TelemetryApi
