from folker.model import Profile

DEFAULT_PROFILE = Profile(name='DEFAULT',
                          context={},
                          secrets={})

from .parallel_executor import ParallelExecutor
from .sequential_executor import SequentialExecutor
