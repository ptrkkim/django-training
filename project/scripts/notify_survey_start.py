from src.mailing.email_sending import notify_survey_releasing
from src.survey.models import Survey


def run():
    released_surveys = Survey.objects.released().had_started()

    for survey in released_surveys:
        notify_survey_releasing(survey)

    released_surveys.update_to_invitations_sent()
