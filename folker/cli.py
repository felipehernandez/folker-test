from folker.logger import logger_factory, SystemLogger
from folker.parameters import parameterised, Configuration


@parameterised
def run(config: Configuration):
    system_logger = logger_factory.system_logger(config)

    run_system_setup(system_logger)

    # Execution setup

    # Execution

    # Report


def run_system_setup(system_logger: SystemLogger):
    system_logger.system_setup_start()
    system_logger.system_setup_completed()


if __name__ == '__main__':
    run(Configuration())
