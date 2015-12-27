from zope.interface import Interface

class IGameOfLifeEngine(Interface):
    def step():
        pass

    def randomize():
        pass
