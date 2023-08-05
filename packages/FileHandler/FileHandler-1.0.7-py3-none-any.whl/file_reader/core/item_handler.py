import abc


class ItemHandler(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def item_pipe(cls, item, *args, **kwargs):
        return NotImplemented

    @classmethod
    @abc.abstractmethod
    def context_pipe(cls, item_list, *args, **kwargs):
        return NotImplemented



