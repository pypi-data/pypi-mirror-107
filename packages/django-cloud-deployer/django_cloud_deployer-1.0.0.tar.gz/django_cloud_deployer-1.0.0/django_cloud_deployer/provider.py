from abc import ABC, abstractmethod

class Provider(ABC):
    def __init__(self, projectName, djangoWSGIApp=None):
        self.projectName = projectName
        self.djangoWSGIApp = djangoWSGIApp

    @abstractmethod
    def isLoggedIn(self) -> bool:
        pass

    @abstractmethod
    def deploy(self):
        pass

    @abstractmethod
    def setupConfigFiles(self):
        pass

    @abstractmethod
    def destroy(self, resourceName) -> bool:
        pass
