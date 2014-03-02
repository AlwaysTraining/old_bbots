#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

import logging
import time
import cherrypy
import bbots




def main():


    logging.basicConfig(
        # filename='bbots.log',
        level=logging.DEBUG)

    app = bbots.BBots()
    wd = cherrypy.process.plugins.BackgroundTask(app.scheduler_period,
                                                 app.scheduler_task)
    wd.start()
    cherrypy.quickstart(app.webui)


if __name__ == '__main__':
    main()





