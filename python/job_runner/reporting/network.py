import json
import os
import pwd
import socket
import sys

# shadow map builtin in py2, making our map usage py2 compatible
# TODO: safely remove after py2 support in ERT ends
from builtins import map
from sys import version as sys_version

import requests
from ecl import EclVersion
from job_runner.reporting.message import Exited, Init
from job_runner.util import pad_nonexisting, read_os_release
from res import ResVersion


class Network(object):

    def __init__(self, error_url=None, log_url=None):
        self.error_url = error_url

        self.simulation_id = None
        self.ert_pid = None

        self.log_url = log_url
        if log_url is None:
            self.log_url = error_url
        self.node = socket.gethostname()

        pw_entry = pwd.getpwuid(os.getuid())
        self.user = pw_entry.pw_name

    def report(self, status):
        if isinstance(status, Init):
            self.start_time = status.timestamp
            self.simulation_id = status.run_id
            self.ert_pid = status.ert_pid

            self._post_initial(status)
        elif isinstance(status, Exited):
            if status.success():
                self._post_success(status)
            else:
                self._post_job_failure(status)

    def _post_initial(self, status):
        os_info = read_os_release()
        _, _, release, _, _ = os.uname()
        python_vs, _ = sys_version.split('\n')
        ecl_v = EclVersion()
        res_v = ResVersion()
        logged_fields = {
            "status": "init",
            "python_sys_path": list(map(pad_nonexisting, sys.path)),
            "pythonpath": list(map(pad_nonexisting,
                                   os.environ.get('PYTHONPATH', '').split(':'))
                               ),
            "res_version": res_v.versionString(),
            "ecl_version": ecl_v.versionString(),
            "LSB_ID": os_info.get('LSB_ID', ''),
            "LSB_VERSION_ID": os_info.get('LSB_VERSION_ID', ''),
            "python_version": python_vs,
            "kernel_version": release,
        }

        job_list = [j.name() for j in status.jobs]
        logged_fields.update({"jobs": job_list})

        self._post_log_message(status.timestamp, extra_fields=logged_fields)

    def _post_log_message(self, timestamp, extra_fields=None):
        self._post_message(self.log_url, timestamp, extra_fields)

    def _post_error_message(self, timestamp, extra_fields):
        self._post_message(self.error_url, timestamp, extra_fields)

    def _post_message(self, url, timestamp, extra_fields=None):
        payload = {"user": self.user,
                   "cwd": os.getcwd(),
                   "application": "ert",
                   "subsystem": "ert_forward_model",
                   "node": self.node,
                   "komodo_release": os.getenv("KOMODO_RELEASE", "--------"),
                   "start_time": self.start_time.isoformat(),
                   "node_timestamp": timestamp.isoformat(),
                   "simulation_id": self.simulation_id,
                   "ert_pid": self.ert_pid}
        payload.update(extra_fields)

        try:
            data = json.dumps(payload)

            # Disabling proxies
            proxies = {
                "http": None,
                "https": None,
            }
            requests.post(url, timeout=3,
                          headers={"Content-Type": "application/json"},
                          data=data, proxies=proxies)
        except:  # noqa
            pass

    def _post_success(self, status):
        self._post_log_message(status.timestamp, {"status": "OK"})

    def _post_job_failure(self, status):

        fields = {"ert_job": status.job.name(),
                  "executable": status.job.job_data["executable"],
                  "arg_list": " ".join(status.job.job_data["argList"])}

        self._post_error_message(status.timestamp, fields)
