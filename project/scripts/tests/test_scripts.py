from datetime import timedelta
from model_mommy import mommy
from unittest.mock import patch, Mock, call

from django.utils import timezone
from django.test import TestCase

from src.survey.models import Survey
from scripts import notify_survey_start, send_reminder_emails


class NotifySurveyStartTests(TestCase):

    def setUp(self):
        self.surveys = mommy.make(Survey, _quantity=2, status=Survey.RELEASED)

    @patch('scripts.notify_survey_start.notify_survey_releasing')
    def test_filter_only_released_surveys_that_has_started(self, mocked_service):
        statuses = list(Survey.STATUSES.keys())
        statuses.remove(Survey.RELEASED)
        for status in statuses:
            mommy.make(Survey, status=status)
        mommy.make(Survey, status=Survey.RELEASED, start_time=timezone.now() + timedelta(days=1))

        notify_survey_start.run()

        calls = [call(self.surveys[0]), call(self.surveys[1])]
        assert 2 == mocked_service.call_count
        assert calls == mocked_service.call_args_list

    @patch('scripts.notify_survey_start.notify_survey_releasing', Mock())
    def test_update_surveys_to_notified(self):
        notify_survey_start.run()

        for survey in self.surveys:
            survey.refresh_from_db()
            assert Survey.INVITATIONS_SENT == survey.status


class SendReminderEmailsTests(TestCase):

    @patch('scripts.send_reminder_emails.notify_scheduled_reminders')
    def test_filter_only_released_surveys_that_has_started(self, mocked_service):
        send_reminder_emails.run()
        mocked_service.assert_called_once_with()
