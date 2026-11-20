from mergedeep import merge

from folker import profiles
from folker.model import Profile
from folker.model.error import InvalidProfileSelectionException
from folker.parameters import Configuration

DEFAULT_PROFILE = Profile(name='DEFAULT',
                          context={},
                          secrets={})



def select_profile(config: Configuration) -> Profile:
    """
    The profile to run with: DEFAULT when none is named, the profile itself when one is, and
    otherwise a new profile merging all of them in command-line order (FEAT-05).

    Merging is recursive: nested mappings are combined key by key, and on any other conflict
    the value of the profile named last wins (lists are replaced, not concatenated).
    Naming a profile that was not loaded is an error: falling back to DEFAULT for a typo would
    run the suite with the wrong context and secrets (BUG-11).
    """
    if not config.profiles:
        return DEFAULT_PROFILE

    unknown = [name for name in config.profiles if name not in profiles]
    if unknown:
        raise InvalidProfileSelectionException(selected=unknown, available=sorted(profiles))

    selected = [profiles[name] for name in config.profiles]
    if len(selected) == 1:
        return selected[0]

    return Profile(name=','.join(config.profiles),
                   context=merge({}, *[profile.context for profile in selected]),
                   secrets=merge({}, *[profile.secrets for profile in selected]))


from .parallel_executor import ParallelExecutor
from .sequential_executor import SequentialExecutor
