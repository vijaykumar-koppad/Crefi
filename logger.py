#!/usr/bin/python

import logging


def setLogger(filename):
    global logger
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)
    return


def setupLogger(filename):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(processName)s: %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
