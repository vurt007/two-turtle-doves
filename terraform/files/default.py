#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, _context):
    logger.info("Event: %s", event)


    logger.info('Slack message: %s', event)

    return {"test": "data"}

