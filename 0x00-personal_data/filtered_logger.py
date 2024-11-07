#!/usr/bin/env python3
'''filtered_logger.py'''
import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    '''tobecommented later'''
    for f in fields:
        regex = f"{f}=[^{separator}]*"
        message = re.sub(regex, f"{f}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    '''tobecommented later'''

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''tobecommented later'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''tobecommented later'''
        org = super().format(record)
        return filter_datum(self.fields, self.REDACTION, org, self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    '''tobecommented later'''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''tobecommented later'''
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username, password=password, host=host, database=db
    )


def main() -> None:
    '''tobecommented later'''
    db = get_db()
    cr = db.cursor()
    cr.execute("SELECT * FROM users;")
    logger = get_logger()
    for i in cr:
        data = []
        for desc, val in zip(cr.description, i):
            pair = f"{desc[0]}={str(val)}"
            data.append(pair)
        row_str = "; ".join(data)
        logger.info(row_str)
    cr.close()
    db.close()


if __name__ == "__main__":
    '''main func'''
    main()
