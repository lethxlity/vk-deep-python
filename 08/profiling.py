import weakref
import cProfile
import pstats
import time


def profiler(func):
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, "stats"):
            wrapper.__setattr__("stats", pstats.Stats())
        if not hasattr(wrapper, "print_stats"):
            wrapper.__setattr__("print_stats",  wrapper.stats.print_stats)
        profile = cProfile.Profile()
        profile.enable()
        profiler(func)
        func(*args, **kwargs)
        profile.disable()
        wrapper.stats.add(pstats.Stats(profile))
        wrapper.stats.sort_stats(pstats.SortKey.CUMULATIVE)
        return func
    return wrapper


class WeakFloat(float):
    pass


class StarNormal:
    def __init__(self, mass, radius, age):
        self.mass = mass
        self.radius = radius
        self.age = age


class StarSlots:
    __slots__ = ("mass", "radius", "age")

    def __init__(self, mass, radius, age):
        self.mass = mass
        self.radius = radius
        self.age = age


class StarWeakref:

    def __init__(self, mass, radius, age):
        self.mass = weakref.proxy(mass)
        self.radius = weakref.proxy(radius)
        self.age = weakref.proxy(age)


@profiler
def run_star(num):
    time_start = time.time()
    star_normal = [StarNormal(1.9885 * 10**30,
                              695_700,
                              4.6*10**9) for i in range(num)]
    for star in star_normal:
        star.mass -= 100_000
        star.age += 1
        star.radius = 700_000
    print(f"For normal class: {time.time()-time_start}")


@profiler
def run_star_slots(num):
    time_start = time.time()
    star_slots = [StarSlots(1.9885 * 10 ** 30,
                            695_700,
                            4.6 * 10 ** 9) for i in range(num)]
    for star in star_slots:
        star.mass -= 100_000
        star.age += 1
        star.radius = 700_000
    print(f"For class with slots: {time.time()-time_start}")


@profiler
def run_star_weakref(num):
    time_start = time.time()
    star_weakref = [StarWeakref(WeakFloat(1.9885 * 10 ** 30),
                                WeakFloat(695_700),
                                WeakFloat(4.6 * 10 ** 9)) for i in range(num)]
    for star in star_weakref:
        try:
            star.mass += 100_000
            star.age += 1
            star.radius = 700_000
        except ReferenceError:
            pass
    print(f"For weakref class: {time.time()-time_start}")


if __name__ == "__main__":
    N = 500_000
    run_star(N)
    run_star(N)
    run_star_slots(N)
    run_star_weakref(N)
    run_star.print_stats()
    run_star_slots.print_stats()
    run_star_weakref.print_stats()
