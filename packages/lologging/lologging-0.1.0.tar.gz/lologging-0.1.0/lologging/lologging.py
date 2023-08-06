


def print_log_and_return(service_name, severity, message,status_code, traceback="",logger_name="cloudrun-custom-logs"):
    """Writes log entries to the given logger."""
    import sys
    import json

    from google.cloud import logging as glogging
    logging_client = glogging.Client()


    logger = logging_client.logger(logger_name)

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
                "service_name":service_name
            }

        return_value={"status":severity,"error":error, "error_v2":error_v2, "traceback":traceback}
    else:
        my_log={
            "message":message,
            "service_name":service_name
        }
        return_value={"status":severity, "message":message}


    logger.log_struct(
      my_log,
      severity=severity
    )

    print("Wrote this log to gcp {}.".format(my_log))
    return return_value, status_code