import sys
import json


class Client():
    def __init__(self, logging_client, service_name,logger_name):
        """
        Retrieves google cloud logging client. Defines service name (cloud run name) and logger name (bq logging table name)
        """
        self.logging_client=logging_client
        self.service_name=service_name
        self.logger_name=logger_name
    

    def print_log_and_return(self, severity, message,status_code, traceback="",**kwargs):
        """Writes log entries to the given logger."""
        logger = self.logging_client.logger(self.logger_name)

        return_value=None
        my_log=None

        if severity=="ERROR":
            e=message
            error=f"Found error: {e}"
            error_v2=f"Found error in function: {e.__traceback__.tb_frame.f_code.co_name} line {e.__traceback__.tb_lineno} of file {e.__traceback__.tb_frame.f_code.co_filename} caused by a: {e.__doc__} This might be an explanation: {sys.exc_info()[1]}"
            
            my_log={
                    "traceback":traceback,
                    "error":error,
                    "error_v2": error_v2,
                    "service_name":self.service_name
                }

            return_value={"status":severity,"error":error, "error_v2":error_v2, "traceback":traceback, **kwargs}
        else:
            my_log={
                "message":message,
                "service_name":self.service_name
            }
            return_value={"status":severity, "message":message, **kwargs}


        logger.log_struct(
        my_log,
        severity=severity
        )

        print("Wrote this log to gcp {}.".format(my_log))
        return return_value, status_code

