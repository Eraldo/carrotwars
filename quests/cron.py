#!/usr/bin/env python
"""
Contains the quest related cron job settings.
This module manages automatic failing of overdue quests
by using time based triggering.
"""

from django_cron import CronJobBase, Schedule
from quests.models import Quest

__author__ = "Eraldo Helal"


class UpdateQuestStatusCronJob(CronJobBase):
    """
    Triffers updating of all quest status once a day.
    For optimal performance call 'python manage.py runcrons' every day at '00:00'.
    If this command is called multiple times a day, only the first call will evoce
    quest status updates and all following calls will be ignored.
    This means calling it every hour will also just work fine.
    """
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'quests.update_quest_status'    # a unique code

    def do(self):
        """Updates the status of all quests."""
        # print("updating quest status")
        Quest.objects.update_status()    

