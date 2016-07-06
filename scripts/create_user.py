#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import getpass
import logging
import sys

from schematics.exceptions import ModelValidationError

import cipy

LOGGER = logging.getLogger('create_user')
LOGGER.setLevel(logging.INFO)
if len(LOGGER.handlers) == 0:
    _handler = logging.StreamHandler()
    _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _handler.setFormatter(_formatter)
    LOGGER.addHandler(_handler)


def email_exists(users_db, email):
    check = list(users_db.run_query(
        users_db.ddl['templates']['check_email_exists'],
        bindings={'email': email}))
    if check:
        msg = 'user with email "{}" already exists'.format(email)
        raise ValueError(msg)


def main():
    parser = argparse.ArgumentParser(
        description='Create a new app user.')
    parser.add_argument(
        '--database_url', type=str, metavar='psql_database_url', default='DATABASE_URL',
        help='environment variable to which Postgres connection credentials have been assigned')
    parser.add_argument(
        '--test', action='store_true', default=False,
        help='flag to run script without modifying any data or models')
    args = parser.parse_args()

    act = not args.test

    conn_creds = cipy.db.get_conn_creds(args.database_url)
    users_db = cipy.db.PostgresDB(conn_creds, ddl='users')
    users_db.create_table(act=act)

    name = input('Enter user name: ')
    email = input('Enter user email: ')
    email_confirm = input('Confirm user email: ')
    while email != email_confirm:
        LOGGER.warning('email mismatch, please try again...')
        email = input('Enter user email: ')
        email_confirm = input('Confirm user email: ')
    password = getpass.getpass(prompt='Enter password: ')
    password_confirm = getpass.getpass(prompt='Confirm password: ')
    while password != password_confirm:
        LOGGER.warning('password mismatch, please try again...')
        password = getpass.getpass(prompt='Enter password: ')
        password_confirm = getpass.getpass(prompt='Confirm password: ')

    record = {'name': name,
              'email': email,
              'password': password}
    sanitized_record = cipy.validation.user.sanitize(record)
    user = cipy.validation.user.User(sanitized_record)
    try:
        user.validate()
    except ModelValidationError:
        msg = 'invalid record: {}'.format(sanitized_record)
        LOGGER.exception(msg)

    validated_record = user.to_primitive()

    if act is True:

        email_exists(users_db, validated_record['email'])

        users_db.execute(
            users_db.ddl['templates']['insert_values'],
            bindings=validated_record, act=act)
    else:
        msg = 'valid record: {}'.format(validated_record)
        LOGGER.info(msg)


if __name__ == '__main__':
    sys.exit(main())
