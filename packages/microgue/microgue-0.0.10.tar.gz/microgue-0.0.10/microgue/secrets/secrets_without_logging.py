import logging
from .secrets import Secrets

logger = logging.getLogger('microgue')
logger.setLevel(logging.CRITICAL)


class SecretsWithoutLogging(Secrets):
    pass
