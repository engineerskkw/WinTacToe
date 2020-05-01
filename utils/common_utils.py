from copy import deepcopy


def return_deepcopy(func):
    def deepcopy_wrapper(*args, **kwargs):
        return deepcopy(func(*args, **kwargs))

    return deepcopy_wrapper
