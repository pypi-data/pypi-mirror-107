import os
from datetime import datetime
import json
import getpass
import random
import string
import socket


def save_log(PATH_LOG: str, robot_name: str, schedule_value: str, start_date: datetime, status: str, error_value: str = None, detail_value: str = None):
    """
    Test

    Args:
        PATH_LOG (str): [description]
        robot_name (str): [description]
        schedule_value (str): [description]
        start_date (datetime): [description]
        status (str): [description]
        error_value (str, optional): [description]. Defaults to None.
        detail_value (str, optional): [description]. Defaults to None.
    """
    if status.upper() in ['WARNING', 'FAIL', 'SUCCESS']:
        data = {
            "NAME": robot_name,
            "LOCAL_PATH": os.getcwd(),
            "USER_NAME": getpass.getuser(),
            "SERVER": socket.getfqdn(),
            "SCHEDULE": schedule_value,
            "START_DATE": start_date.isoformat(),
            "END_DATE": datetime.utcnow().isoformat(),
            "STATUS": status.upper(),
            "ERROR":  error_value,
            "MORE_INFORMATION":  detail_value
        }

        code_name = ''.join(random.choice(
            string.ascii_lowercase + string.digits) for _ in range(15)
        )

        name_file = f"{PATH_LOG}/{data['NAME']}_{code_name}.json"

        with open(name_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        print(f"[INFO] Document created: {name_file}")

    else:
        print("[ERROR] Unexpected status ('WARNING', 'FAIL', 'SUCCESS')")

    return
