"""MLDock Friendly Environments for Sagemaker"""
from mldock.platform_helpers.mldock.configuration.environment import base
from mldock.platform_helpers.aws.sagemaker.environment import Environment as BaseSagemakerEnvironment

class SagemakerEnvironment(BaseSagemakerEnvironment, base.AbstractEnvironment):
    """
        Structures Sagemaker Environment similarily to
        other environments maintaining it's function
    """
    def __init__(self, **kwargs):
        super(SagemakerEnvironment, self).__init__()