#! /usr/bin/env python3

"""
    Make file for running log analysis scripts.

    Before executing scripts in this project, run
        $ ./make.py setup
"""

import sys
import argparse
from pathlib import Path
import psycopg2


#
# Commands
#

def setup():
    """Sets up views required for tools."""

    print("Creating articles_ok_logs view...")
    create_articles_ok_logs()

    print("Creating author_article_views view...")
    create_author_article_views()

    print("Creating daily_http_request_counts view...")
    create_daily_http_request_counts()


def clean():
    """Removes all tool artifacts."""

    print("Ensuring removal of articles_ok_logs view...")
    delete_articles_ok_logs()

    print("Ensuring removal of author_article_views view...")
    delete_author_article_views()

    print("Ensuring removal of daily_http_request_counts view...")
    delete_daily_http_request_counts()


#
# Views CRUD
#

def create_articles_ok_logs():
    """Loads articles_ok_logs view."""

    exec_create_view_sql(
        Path('src/sql/create_view_articles_ok_logs.sql').read_text())


def create_author_article_views():
    """Loads author_article_views view."""

    exec_create_view_sql(
        Path('src/sql/create_view_author_article_views.sql').read_text())


def create_daily_http_request_counts():
    """Loads daily_http_request_counts view."""

    exec_create_view_sql(
        Path('src/sql/create_view_daily_http_request_counts.sql').read_text())


def delete_articles_ok_logs():
    """Deletes articles_ok_logs view."""

    exec_delete_view_sql("DROP VIEW articles_ok_logs CASCADE;")


def delete_author_article_views():
    """Deletes author_article_views view."""

    exec_delete_view_sql("DROP VIEW author_article_views CASCADE;")


def delete_daily_http_request_counts():
    """Deletes author_article_views view."""

    exec_delete_view_sql("DROP VIEW daily_http_request_counts CASCADE;")


def exec_create_view_sql(sql):
    """Executes sql for creating views."""

    conn = psycopg2.connect("dbname=news user=vagrant")
    cur = conn.cursor()

    try:
        cur.execute(sql)
        conn.commit()
    except psycopg2.Error as db_error:
        print("Warning:", db_error)
    except Exception:
        raise
    finally:
        cur.close()
        conn.close()


def exec_delete_view_sql(sql):
    """Deletes (idempotent) view in the news database."""

    conn = psycopg2.connect("dbname=news user=vagrant")
    cur = conn.cursor()

    try:
        cur.execute(sql)
        conn.commit()
    except psycopg2.Error:
        pass
    except Exception:
        raise
    finally:
        cur.close()
        conn.close()


def main():
    parser = argparse.ArgumentParser(prog='make')
    parser.add_argument('commands', nargs='+', help="setup, clean")

    commands_buffer = []

    for command in parser.parse_args().commands:
        if command == "setup":
            commands_buffer.append(setup)
        elif command == "clean":
            commands_buffer.append(clean)
        else:
            print("Error: Unrecognized command:", command)
            sys.exit(1)

    for command in commands_buffer:
        try:
            command()
        except Exception:
            print("Error: Python Exception:", sys.exc_info()[0])
            sys.exit(1)


if __name__ == '__main__':
    main()
