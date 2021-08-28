from folker.logger import logger_factory
from folker.parameters import parameterised, Configuration


@parameterised
def run(config: Configuration):
    system_logger = logger_factory.build_system_logger(config)

    system_logger.system_setup_start()
    system_logger.system_setup_completed()
