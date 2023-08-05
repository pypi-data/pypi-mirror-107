import logging
from mldock.platform_helpers.mldock.configuration.environment.base import BaseEnvironment
from mldock.platform_helpers.mldock.configuration.container import \
    BaseTrainingContainer, BaseServingContainer

logger = logging.getLogger('mldock')

# Instantiate Environment here
# import to other scripts
environment = BaseEnvironment(base_dir='/opt/ml/')

# (TODO)
# Assess situations and likelihood of whether users should by
# default create their own or can it be hidden until needed.
# For example, using just the BaseServingContainer by default
# USE-CASES:
#   - special Metric loggers (cleaning up, uploading to separate s3 locatations, etc)
#   - Environment and importing from here to other scripts
class TrainingContainer(BaseTrainingContainer):
    """Implements the base training container, allow a user to override/add/extend any training container setup logic"""
    pass

# (TODO)
# Assess situations and likelihood of whether users should by
# default create their own or can it be hidden until needed.
# For example, using just the BaseServingContainer by default
# USE-CASES:
#   - special Metric loggers (cleaning up, uploading to separate s3 locatations, etc)
#   - Instantiating Environment and importing from here to other scripts
class ServingContainer(BaseServingContainer):
    """Implements the base serving container, allow a user to override/add/extend any serving container setup logic"""
    pass
