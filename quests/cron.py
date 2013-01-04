from django_cron import CronJobBase, Schedule
from quests.models import Quest

__author__ = "Eraldo Helal"

class UpdateQuestStatusCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'quests.update_quest_status'    # a unique code

    def do(self):
        print("updating quest status")
        Quest.objects.update_status()    

