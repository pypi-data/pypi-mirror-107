import base64
import json
import pathlib
import pickle
import requests
from typing import Optional

import pandas as pd

from .. import _common
from .. import _login
from . import _common as _jobs_common
from . import _push
from . import _schedule


def pull(datalab_notebook_url=None, label=None, interactive_index: int = 0) -> Optional[pd.Series]:
    """
    Retrieves a jobs DataFrame previously created by a call to spy.jobs.push or
    spy.jobs.schedule.  The DataFrame will have been stored as a pickle (.pkl)
    file in the _Job DataFrames folder within the parent folder of the Notebook
    specified by the datalab_notebook_url, or of the current Notebook if no
    datalab_notebook_url is specified.

    Parameters
    ----------
    datalab_notebook_url : str, default None
        The URL of the Data Lab Notebook for which the scheduled jobs DataFrame
        is desired.  If the value is not specified, the URL of the
        currently-running notebook is used.

    label : str, default None
        The label that was used in scheduling, if any.  In most circumstances,
        this parameter should not be specified, since the scheduled Notebook
        will use the label that was provided during scheduling.

    interactive_index : int, default 0
        Used during notebook development to control which row of jobs_df is
        returned when NOT executing as a job. Change this value if you want
        to test your notebook in the Jupyter environment with various rows
        of parameters.

        When the notebook is executed as a job, this parameter is ignored.

    Returns
    -------
    pandas.Series
        The requested row of the DataFrame that was pushed for the specified
        Notebook and label using the spy.jobs.push or spy.jobs.schedule method

"""
    data_lab_url, project_id, file_path = _schedule.retrieve_notebook_path(datalab_notebook_url)
    file_path_path = pathlib.PurePosixPath(file_path)
    path_to_parent = _schedule.path_or_empty_string(file_path_path.parent)
    jobs_dfs_folder_path = pathlib.PurePosixPath(path_to_parent, _common.JOB_DATAFRAMES_FOLDER_NAME)
    cookies = {'sq-auth': _login.client.auth_token}
    label_text = label or _jobs_common.get_label_from_executor()
    with_label_text = f'.with.label.{label_text}' if label_text else ''
    jobs_df_pickle = f'{file_path_path.stem}{with_label_text}.pkl'
    get_pickle_path = pathlib.PurePosixPath(jobs_dfs_folder_path, jobs_df_pickle)
    resp = get_pickle(f'{data_lab_url}/{project_id}/api/contents/{get_pickle_path}', cookies=cookies)
    if resp.status_code in [200, 201]:
        jobs_df = pickle.loads(base64.b64decode(json.loads(resp.content)['content']))
        return _push.get_parameters(jobs_df, interactive_index, _common.Status(quiet=True))


def get_pickle(url, cookies):
    return requests.get(url, cookies=cookies)
