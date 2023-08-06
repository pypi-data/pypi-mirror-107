# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

import json
import sqlite3

from py_singleton import singleton

from digital_hydrant import logging
from digital_hydrant.config import db_path


@singleton
class CollectorQueue:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.__table__ = "collectors"
        self.__ip_table__ = "unique_ips"
        self.logger.debug("CollectorQueue initialized")

        try:
            self.conn = sqlite3.connect(db_path, timeout=10)
            self.cursor = self.conn.cursor()
        except Exception as err:
            self.logger.critical(f"Failed to connect to the database: {err}")
            exit(1)

    def put(self, type, payload, timestamp):
        type = type.split(".")[0] if "." in type else type
        try:
            query = f"INSERT INTO {self.__table__}(type, payload, timestamp) VALUES('{type}', '{json.dumps(payload)}', '{timestamp}')"
            self.logger.debug(query)
            self.cursor.execute(query)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to insert {type} into table: {e}")
        finally:
            self.conn.commit()

    def put_ip(self, ip, mac):
        try:
            query = f"INSERT INTO {self.__ip_table__}(ip, mac_address) VALUES('{ip}', '{mac}')"
            self.logger.debug(query)
            self.cursor.execute(query)
        except sqlite3.Error as e:
            if isinstance(e, sqlite3.IntegrityError):
                self.logger.debug(
                    f"IP({ip}) already exists in {self.__ip_table__}: {e}"
                )
            else:
                self.logger.critical(
                    f"Failed to insert IP({ip})/macAddress({mac}) into table: {e}"
                )
        finally:
            self.conn.commit()

    def peak(self):
        query = f"SELECT id, type, payload, timestamp FROM {self.__table__} WHERE uploaded=0 ORDER BY id ASC"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def find_ip(self, ip):
        query = f"SELECT id, ip, mac_address FROM {self.__ip_table__} WHERE ip = '{ip}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def update_ip(self, ip, changes={}):
        try:
            set = ""
            for column, value in changes.items():
                if isinstance(value, str):
                    value = f"'{value}'"
                if value is None:
                    value = "NULL"

                set += f"{column}={value}" if len(set) == 0 else f", {column}={value}"

            if set:
                self.cursor.execute(
                    f"UPDATE {self.__ip_table__} SET {set} WHERE ip='{ip}'"
                )
        except sqlite3.Error as e:
            self.logger.error(f"Failed to update {self.__ip_table__} for {ip}: {e}")
        finally:
            self.conn.commit()

    def pop(self, delete=True):
        (id) = self.peak()
        self.remove(id, delete)

    def remove(self, id, delete=True):
        try:
            if delete:
                self.cursor.execute(f"DELETE FROM {self.__table__} WHERE id={id}")
            else:
                self.cursor.execute(
                    f"UPDATE {self.__table__} SET uploaded=1 WHERE ID={id}"
                )
        except sqlite3.Error as e:
            self.logger.error(
                f"Failed to remove({'delete' if delete else 'update'}) from table: {e}"
            )
        finally:
            self.conn.commit()

    def remove_all(self, delete=True):
        try:
            if delete:
                self.cursor.execute(f"DELETE FROM {self.__table__}")
            else:
                self.cursor.execute(f"UPDATE {self.__table__} SET uploaded=1")
        except sqlite3.Error as e:
            self.logger.error(
                f"Failed to remove({'delete' if delete else 'update'}) from table: {e}"
            )
        finally:
            self.conn.commit()

    def fail(self, id):
        try:
            self.cursor.execute(f"UPDATE {self.__table__} SET uploaded=2 WHERE ID={id}")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to update uploaded=2 from table: {e}")
        finally:
            self.conn.commit()

    def set_log_level(self, level):
        self.logger.setLevel(level)
