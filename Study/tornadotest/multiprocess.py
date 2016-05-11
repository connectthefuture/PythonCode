import functools
from multiprocessing import Pool, Process


def setruntime(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        env = args[0]
        return func(*args, **kwargs)

    return wrapper

@setruntime
def f(env, request, runtime):
    pass


if __name__ == '__main__':
    pool = Pool(5, )
    pool.apply_async(f, [{}, {}, {}])
