#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webui import webui
import time
from data import Data
from session import Session
from webui import WebUi

SCHEDULER_PERIOD = 1


class BBots(object):
    def __init__(self):
        self.scheduler_period = SCHEDULER_PERIOD
        self.data = Data(self)
        self.webui = WebUi()

    def play_game(self, rec):
        """
        Play the game specified in the record
        """
        Session(rec)

    def maybe_play_game(self, id):
        """
        Check if conditions are correct to play game and play it
        """
        rec = self.data.get_record(id)
        # get the date time last played

        # if we have not played since yesterday
        # then play the game


    def scheduler_task(self):
        """
        Randomly try to play until we get into at least one bre game
        """
        self.data.load_ss()
        ids = list(self.data.ids)
        for id in ids:
            if self.maybe_play_game(id):
                return



