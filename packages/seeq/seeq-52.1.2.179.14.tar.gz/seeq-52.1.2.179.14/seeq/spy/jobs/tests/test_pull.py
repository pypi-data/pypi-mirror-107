import base64
import json
import mock
import pickle
import pytest

import pandas as pd

from ...tests import test_common
from ... import _login
from .. import _pull
from .. import _common as _jobs_common
from . import test_schedule


test_notebook_url = f'{test_schedule.seeq_url}/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C862/' + \
                    f'notebooks/Path/To/Some/Notebook.ipynb'


def get_pickle_mock():
    test_df = pd.DataFrame(data={'Schedule': ['Daily'], 'Additional Info': ['What you need to know']})
    mock_get_resp = mock.Mock()
    mock_get_resp.content = json.dumps({'content': base64.b64encode(pickle.dumps(test_df)).decode('utf-8')})
    mock_get_resp.status_code = 200
    return mock.Mock(return_value=mock_get_resp)


@pytest.mark.system
def test_pull_success_in_datalab():
    test_schedule.setup_run_in_datalab()
    _pull.get_pickle = get_pickle_mock()
    retrieved_job = _pull.pull(test_notebook_url)
    assert 'Schedule' in retrieved_job
    assert 'What you need to know' in retrieved_job.values


@pytest.mark.system
def test_pull_success_in_executor():
    test_schedule.setup_run_in_executor()
    mock_get_pickle = get_pickle_mock()
    _pull.get_pickle = mock_get_pickle
    contents_url = f'{test_schedule.seeq_url}/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C862/api/contents/Path/To/Some' \
                   f'/_Job DataFrames/Notebook.with.label.run-in-executor-label.pkl'
    retrieved_job = _pull.pull(test_notebook_url)
    assert 'Schedule' in retrieved_job
    assert 'What you need to know' in retrieved_job.values
    cookies = {'sq-auth': _login.client.auth_token}
    mock_get_pickle.assert_called_once_with(contents_url, cookies=cookies)


@pytest.mark.system
def test_pull_success_outside_datalab():
    test_common.login()
    test_schedule.setup_run_outside_datalab()
    _pull.get_pickle = get_pickle_mock()
    retrieved_job = _pull.pull(test_notebook_url)
    assert 'Schedule' in retrieved_job
    assert 'What you need to know' in retrieved_job.values


@pytest.mark.system
def test_pull_failure_outside_datalab():
    test_common.login()
    test_schedule.setup_run_outside_datalab()
    mock_get_resp_403 = mock.Mock()
    mock_get_resp_403.status_code = 403
    _pull.get_pickle = mock.Mock(return_value=mock_get_resp_403)
    retrieved_job = _pull.pull(test_notebook_url)
    assert retrieved_job is None
