import sys

from network_security.logging import logger


class NetworkSecurityError(Exception):
    def __init__(self, error_message: str, error_details: sys) -> None:
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self) -> str:
        return f"Error occured in python script name [{self.file_name}] line number [{self.lineno}] error message [{self.error_message!s}]"


# if __name__ == "__main__":
#     try:
#         logger.logging.info("Enter the try block")
#         a = 1 / 0
#         print("This will not be printed", a)
#     except Exception as e:
#         raise NetworkSecurityError(e, sys) from e
