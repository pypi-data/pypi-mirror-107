import abc


class FileHandler(abc.ABC):

    @abc.abstractmethod
    def parse(self, *args, **kwargs):
        return NotImplementedError
