from folker.logger import TestLogger
from folker.model import Validatable
from folker.model.context import Context
from folker.model.error.error import SourceException
from folker.model.stage.stage import Stage


class Test(Validatable):
    id: str
    name: str
    description: str
    parallel: bool

    foreach: dict
    tags: [str]

    stages: [Stage]

    def __init__(self,
                 id: str = None,
                 name: str = None,
                 description: str = None,
                 parallel: bool = False,
                 foreach: dict = {},
                 tags: [str] = None,
                 stages: [Stage] = None
                 ) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.description = description
        self.parallel = parallel
        self.foreach = foreach
        self.tags = tags if tags else []
        self.stages = stages if stages else []

    def __bool__(self):
        if self.name is None:
            self.validation_report.missing_fields.add('test.name')

        for stage in self.stages:
            if not stage:
                self.validation_report.merge_with_prefix('test[{name}].'.format(name=self.name),
                                                         stage.validation_report)

        return bool(self.validation_report)

    def execute(self, logger: TestLogger, context: Context = None):
        if context is None:
            context = Context.EMPTY_CONTEXT()
        execution_contexts = context.replicate_on_test(self.foreach)
        executions_result = True

        for execution_context in execution_contexts:
            executions_result = executions_result and self._execute(logger, execution_context)

        return executions_result

    def _execute(self, logger: TestLogger, context: Context):
        name = context.replace_variables(self.name)
        logger.test_start(name, self.description)
        try:
            for stage in self.stages:
                context = stage.execute(logger, context)
        except SourceException as e:
            logger.test_finish_error(e)
            return False
        except Exception as e:
            logger.test_finish_error(e)
            return False

        logger.test_finish()

        return True
