from unittest import mock

from pykubeslurm.scheduler import init_scheduler, reconcile
from pykubeslurm.settings import SETTINGS


@mock.patch("pykubeslurm.scheduler.BackgroundScheduler")
def test_init_scheduler(mocked_background_scheduler: mock.MagicMock):
    mocked_background_scheduler.return_value.add_job = mock.Mock()
    mocked_background_scheduler.return_value.start = mock.Mock()

    init_scheduler()

    mocked_background_scheduler.return_value.add_job.assert_called_once_with(
        func=reconcile,
        trigger="interval",
        seconds=SETTINGS.RECONCILIATION_TIME,
        id="reconcile_jobs",
    )
    mocked_background_scheduler.return_value.start.assert_called_once_with()
