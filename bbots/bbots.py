#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from data import Data
from session import Session
from webui import WebUi
import random
import logging

SCHEDULER_PERIOD = 3


class BBots(object):
    def __init__(self):
        self.scheduler_period = SCHEDULER_PERIOD
        self.data = Data(self)
        self.webui = WebUi()

    def play_game(self, rec):
        """
        Play the game specified in the record
        """
        # Session(rec)
        logging.debug("Playing game: " + rec['id'])
        time.sleep(2)
        rec['failures_today'] += 1
        self.data.update_rec(rec)
        return True



    def maybe_play_game(self, id):
        """
        Check if conditions are correct to play game and play it
        """
        rec = self.data.get_record(id)
        logging.debug("considering playing game: " + str(rec['id']))
        # get the date time last played

        # if we have not played since yesterday
        # then play the game
        self.play_game(rec)



    def scheduler_task(self):
        """
        Randomly try to play until we get into at least one bre game
        """
        self.data.load_ss()
        ids = list(self.data.ids)
        random.shuffle(ids)
        for id in ids:
            if self.maybe_play_game(id):
                return



