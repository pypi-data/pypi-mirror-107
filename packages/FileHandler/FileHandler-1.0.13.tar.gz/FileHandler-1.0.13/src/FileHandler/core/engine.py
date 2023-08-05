from FileHandler.core import file_handler, item_handler


class DataHandleEngine:

    def __init__(self):
        self.file_handler = None
        self.item_handler = None
        self.engine_meta = None

    def file_handle(self):
        file_handler_generator = self.file_handler.parse(meta=self.engine_meta)
        return file_handler_generator

    def item_handle(self, generator):
        for item in generator:
            yield self.item_handler.item_pipe(item, meta=self.engine_meta)

    def execute_pipeline(self):
        if not self.engine_meta:
            self.engine_meta = dict()

        generator = self.file_handle()
        if not generator:
            return None
        generator = self.item_handle(generator)
        piped_result = [item for item in list(generator) if item]
        self.item_handler.context_pipe(piped_result, meta=self.engine_meta)
        return self.engine_meta


class EngineConfigBuilder:
    def __init__(self):
        self._engine = DataHandleEngine()

    def build(self):
        return self._engine


class EngineFileHandlerBuilder(EngineConfigBuilder):
    def file_handler(self, file_handler: file_handler.FileHandler):
        self._engine.file_handler = file_handler
        return self


class EngineItemHandlerBuilder(EngineFileHandlerBuilder):
    def item_handler(self, item_handler: item_handler.ItemHandler):
        self._engine.item_handler = item_handler
        return self


class EngineMetaBuilder(EngineItemHandlerBuilder):
    def engine_meta(self, engine_meta: dict = None):
        self._engine.engine_meta = engine_meta
        return self


class EngineBuilder(EngineMetaBuilder):
    @classmethod
    def config(cls):
        return EngineBuilder()
