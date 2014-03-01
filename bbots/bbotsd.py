#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging.handlers
import logging
from daemon import runner
import sys,os
import lockfile
import cherrypy
import bbots

class daemon_base(object):
    def __init__(self):
        self.stdin_path = None
        self.stdout_path = None
        self.stderr_path = None
        self.pidfile_path = None
        self.pidfile_timeout = None
        self.args = None

    name = ''


    def setup_process(self, name):
        self.name = name
        outdev = '/dev/null'
# if having trouble debugging exceptions happenign very early in initialization
# you may want to uncomment the following, since there are frequently
# exceptions, we are leaving the tty setup for now, 
        if sys.stdin.isatty():
            outdev = '/dev/tty'
        else:
            outdev = '/dev/null'
        self.stdin_path = outdev
        self.stdout_path = outdev
        self.stderr_path = outdev
        self.pidfile_timeout = 5


        # if arguments are specfied, and arguments have pid file
        if self.args is not None and self.args.pid_file is not None:
            # set pid file name to value from command line
            self.pidfile_path = self.args.pid_file
        # otherwise generate a pid file path
        else:
            # get the path to this python file
            # convert all of the '/' to '_'
            f = os.path.dirname(os.path.dirname(__file__)).replace('/','_')
            # append name and '.pid'
            f += "_" + name + '.pid'
            # preppend '/tmp'
            self.pidfile_path = os.path.join('/tmp',f)

        logging.info('pid path is ' + str(self.pidfile_path))

    def main(self, argv):
        logging.debug('"' + '" "'.join(argv) + '"')
        try:
            daemon_runner = runner.DaemonRunner(self)


            # setup loggging for the daemon
            # get the currently configured logger
            logger = logging.getLogger()
            handle = None

            # if daemon has arguments and has log file
            if self.args is not None and self.args.log_file is not None:
                # NOTE special treatment is needed.  We want logging before and
                # after we daemonize, so though this was setup in common_init
                # we do it again because all filehandles get closed for us by
                # running the daemon
                # http://stackoverflow.com/questions/13180720/maintaining-logging-and-or-stdout-stderr-in-python-daemon

                # We have already set a handler in common_init, guaranteed to
                # be called before this, so grab the file handle
                handler = logger.handlers[0]
                handle = handler.stream
            # otherwise
            else:
                # NOTE: logging is setup here trying to copy what is done in 
                # common_init, when changing logging, you may want to look in
                # bothplaces

                # NOTE: Before you go crazy, no DEBUG level is not going to syslog
                # I do not know why, I can only guess it is by that log handler's
                # design.  Makes sense, if you want to debug, point it to a file

                # add a syslog log handler to the logger
                handler = logging.handlers.SysLogHandler()

                format = self.name + '%(process)d:%(levelname)s:%(message)s'

                # preserve the logging file handle
                # http://bugs.python.org/issue17981
                handle = handler.socket.fileno()

                # set logging format
                if format is not None:
                    formatter = logging.Formatter(format)
                    handler.setFormatter(formatter)

                # set the logging level for the handler
                strlevel = 'WARN'
                if self.args is not None and self.args.log_level is not None:
                    strlevel = self.args.log_level
                #logger.setLevel(eval('logging.' + strlevel))
                logger.setLevel(logging.DEBUG) #TODO Fix


                # add the logging file handler to the logger
                logger.addHandler(handler)

            # initialze the context of the daemon runner with the logger's
            #   file handler
            if daemon_runner.daemon_context.files_preserve is None:
                daemon_runner.daemon_context.files_preserve = []
            daemon_runner.daemon_context.files_preserve.append(handle)

            daemon_runner.do_action()


        except lockfile.LockTimeout as e:
            logging.warning(self.name + " Lockfile exists: " + str(e))
        except runner.DaemonRunnerStopFailureError as e:
            logging.warning(self.name + " Failed to stop daemon: " + str(e))
        except:
            raise


class bbotsd(daemon_base):
    def __init__(self, args):
        daemon_base.__init__(self)
        self.args = args
        self.setup_process("bbotsd")

    def run(self):
        app = bbots.Bbots()
        print "running"
        cherrypy.quickstart(app.webui)



def common_init(name, args):
    """
    Common site for logging configuration, always call as first function
    from main and other initialization
    """
    # NOTE: Daemon's have a special case when using the system log, any changes to
    # defualt logging should also be canidates to be made in QuiltDaemon.main
    strlevel = args.log_level
    logfile = args.log_file
    strformat = '%(asctime)s:' + name + '%(process)d:%(levelname)s:%(message)s'
    if strlevel is None:
        strlevel = 'WARN'
    strlevel = 'logging.' + strlevel
    #TODO Fix
    logging.basicConfig(level=logging.DEBUG, filename=logfile,
                        format=strformat)

def main_helper(name, description, argv):
    """
    Quilt helper function for main to do common things

    description                 # prose description of functionality
    argv                        # input arguments
    """
    argparser = argparse.ArgumentParser(description)

    argparser.add_argument('-l', '--log-level', nargs='?',
                           help='logging level (DEBUG,INFO,WARN,'
                                'ERROR) default: WARN')
    argparser.add_argument('-lf', '--log-file', nargs='?',
                           help='path to log file, default will be syslog or '
                                'stderr')

    if '-h' not in argv and '--help' not in argv:
        args, unknownArgs = argparser.parse_known_args(argv)
        unknownArgs = unknownArgs  # its a pylint thing
        common_init(name, args)

    return argparser

def daemon_main_helper(name, description, argv):
    """
    common initialization for daemon processes
    @description the description of the process shown when accessing the
    cmd line help for the process
    @argv the cmd line arguments for the process, starting with the first
    argument
    """
    # get parser by calling the regular main helper
    # setup command line interface
    parser = main_helper(name, description, argv)

    # add specification of the start, stop, and restart actions
    parser.add_argument('action', choices=['start', 'stop', 'restart'])

    # add specification of the pid file
    parser.add_argument('-p', '--pid-file', nargs='?',
                        help='Path to file used to make sure only one '
                             'instance of the daemon is created')

    # return the  argument oarser
    return parser

def main(argv):
    # setup command line interface
    parser = daemon_main_helper("bbots", "bbot aggregator", argv)

    args = parser.parse_args()

    # start the daemon
    bbotsd(args).main(argv)


if __name__ == "__main__":
    main(sys.argv[1:])