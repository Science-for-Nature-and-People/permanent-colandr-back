#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import logging
import sys

from schematics.exceptions import ModelValidationError

import cipy

LOGGER = logging.getLogger('create_project')
LOGGER.setLevel(logging.INFO)
if len(LOGGER.handlers) == 0:
    _handler = logging.StreamHandler()
    _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _handler.setFormatter(_formatter)
    LOGGER.addHandler(_handler)


def get_objective():
    objective = input('Enter review objective:\n')
    return objective


def get_research_questions():
    rqs = []
    idx = 0
    while True:
        question = input('Enter research question:\n')
        if question:
            rqs.append({'question': question, 'idx': idx})
            idx += 1
        another = input('Add another question (y/n)? ')
        if another == 'n':
            break
        elif another == 'y':
            continue
        else:
            LOGGER.warning('invalid value: "%s"', another)
    return rqs


def main():
    parser = argparse.ArgumentParser(
        description='Create a new systematic map project.')
    parser.add_argument(
        '--user_id', type=int, required=True, metavar='user_id',
        help='unique identifier of current user')
    parser.add_argument(
        '--project_id', type=int, required=True, metavar='project_id',
        help='unique identifier of current systematic map project')
    parser.add_argument(
        '--database_url', type=str, metavar='psql_database_url', default='DATABASE_URL',
        help='environment variable to which Postgres connection credentials have been assigned')
    parser.add_argument(
        '--test', action='store_true', default=False,
        help='flag to run script without modifying any data or models')
    args = parser.parse_args()

    act = not args.test

    conn_creds = cipy.db.get_conn_creds(args.database_url)
    projects_db = cipy.db.PostgresDB(conn_creds, ddl='projects')

    objective = get_objective()
    research_questions = get_research_questions()

    plan = {}
    if objective:
        plan['objective'] = objective
    if research_questions:
        plan['research_questions'] = research_questions


if __name__ == '__main__':
    sys.exit(main())
