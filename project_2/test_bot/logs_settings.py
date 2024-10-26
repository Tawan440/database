import logging

def create_logger(py_module_name: str , start_message: str) -> None:
    logger = logging.getLogger(py_module_name)
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info(start_message )