try:
    import Box2D
    # from Box2D.lunar_lander import LunarLander
    # from Box2D.box2d.lunar_lander import LunarLanderContinuous
    # from Box2D.bipedal_walker import BipedalWalker, BipedalWalkerHardcore
    from Box2D.car_racing import CarRacing
except ImportError:
    Box2D = None