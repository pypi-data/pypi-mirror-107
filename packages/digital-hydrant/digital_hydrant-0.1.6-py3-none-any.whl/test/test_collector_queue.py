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

import os
import sqlite3
import unittest

from digital_hydrant.collector_queue import CollectorQueue
from digital_hydrant.config import db_path


class TestCollectorQueue(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(db_path, timeout=10)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS collectors (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, payload TEXT, timestamp TIMESTAMP, uploaded INTEGER DEFAULT 0)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS unique_ips (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT UNIQUE, mac_address TEXT, ssh_last_tested TIMESTAMP, snmp_last_tested TIMESTAMP, last_nmap_scan TIMESTAMP, open_ports TEXT)"
        )

        self.queue = CollectorQueue()

    def tearDown(self):
        self.cursor.execute("DELETE FROM collectors")
        self.cursor.execute("DELETE FROM unique_ips")
        self.conn.commit()

    def test_put(self):
        timestamp = 123456
        self.queue.put("my type", {"a": "payload"}, timestamp)

        self.cursor.execute(
            "SELECT id, type, payload, timestamp, uploaded FROM collectors"
        )

        (id, type, payload, timestamp, uploaded) = self.cursor.fetchone()

        self.assertEqual(type, "my type")
        self.assertEqual(payload, '{"a": "payload"}')
        self.assertEqual(timestamp, 123456)
        self.assertEqual(uploaded, 0)

    def test_put_ip(self):
        timestamp = 123456
        self.queue.put_ip("1.2.3.4", "mac")

        self.cursor.execute("SELECT id, ip, mac_address FROM unique_ips")

        (id, ip, mac_address) = self.cursor.fetchone()

        self.assertEqual(ip, "1.2.3.4")
        self.assertEqual(mac_address, "mac")

    def test_put_ip_already_exists(self):
        timestamp = 123456
        self.queue.put_ip("1.2.3.4", "mac")

        self.cursor.execute("SELECT count(id) FROM unique_ips")

        (count,) = self.cursor.fetchone()

        self.queue.put_ip("1.2.3.4", "mac")

        self.cursor.execute("SELECT count(id) FROM unique_ips")

        (new_count,) = self.cursor.fetchone()

        self.assertEqual(count, new_count)

    def test_peak(self):
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        )
        self.conn.commit()

        (id, type, payload, timestamp) = self.queue.peak()

        self.assertEqual(type, "another type")
        self.assertEqual(payload, "{another: payload}")
        self.assertEqual(timestamp, 654321)

    def test_find_ip(self):
        self.cursor.execute(
            'INSERT INTO unique_ips(ip, mac_address) VALUES \
                       ("1.2.3.4", "mac")'
        )
        self.cursor.execute(
            'INSERT INTO unique_ips(ip, mac_address) VALUES \
                       ("4.3.2.1", "macdonald")'
        )
        self.conn.commit()

        (id, ip, mac_address) = self.queue.find_ip("1.2.3.4")

        self.assertEqual(ip, "1.2.3.4")
        self.assertEqual(mac_address, "mac")

    def test_find_ip_not_found(self):
        self.cursor.execute(
            'INSERT INTO unique_ips(ip, mac_address) VALUES \
                       ("1.2.3.4", "mac")'
        )
        self.cursor.execute(
            'INSERT INTO unique_ips(ip, mac_address) VALUES \
                       ("4.3.2.1", "macdonald")'
        )
        self.conn.commit()

        result = self.queue.find_ip("9.9.9.9")

        self.assertIsNone(result)

    def test_update_ip(self):
        self.cursor.execute(
            'INSERT INTO unique_ips(ip, mac_address) VALUES \
                       ("1.2.3.4", "mac")'
        )
        self.conn.commit()

        self.queue.update_ip(
            "1.2.3.4",
            {"ssh_last_tested": 123456789, "open_ports": "22,161", "mac_address": None},
        )

        self.cursor.execute(
            "SELECT id, ip, mac_address, ssh_last_tested FROM unique_ips WHERE ip = '1.2.3.4'"
        )

        (id, ip, mac_address, ssh_last_tested) = self.cursor.fetchone()

        self.assertEqual(ip, "1.2.3.4")
        self.assertIsNone(mac_address)
        self.assertEqual(ssh_last_tested, 123456789)

    def test_update_no_changes(self):
        self.cursor.execute(
            'INSERT INTO unique_ips(ip, mac_address) VALUES \
                       ("1.2.3.4", "mac")'
        )
        self.conn.commit()

        self.queue.update_ip("1.2.3.4")

        self.cursor.execute(
            "SELECT id, ip, mac_address, ssh_last_tested FROM unique_ips WHERE ip = '1.2.3.4'"
        )

        (id, ip, mac_address, ssh_last_tested) = self.cursor.fetchone()

        self.assertEqual(ip, "1.2.3.4")
        self.assertEqual(mac_address, "mac")
        self.assertIsNone(ssh_last_tested)

    def test_remove(self):
        first_id = self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("first type", "{first: payload}", 654321)'
        ).lastrowid
        last_id = self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        ).lastrowid
        self.conn.commit()

        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 2)

        self.queue.remove(first_id)

        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 1)

        (id, uploaded) = self.cursor.execute(
            "SELECT id, uploaded FROM collectors"
        ).fetchone()

        self.assertEqual(uploaded, 0)
        self.queue.remove(last_id, delete=False)
        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 1)

        (id, uploaded) = self.cursor.execute(
            "SELECT id, uploaded FROM collectors"
        ).fetchone()
        self.assertEqual(last_id, id)
        self.assertEqual(uploaded, 1)

    def test_remove_all(self):
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("first type", "{first: payload}", 654321)'
        )
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        )
        self.conn.commit()

        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 2)
        self.queue.remove_all()
        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 0)

    def test_remove_all_no_delete(self):
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("first type", "{first: payload}", 654321)'
        )
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        )
        self.conn.commit()

        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 2)
        self.queue.remove_all(delete=False)
        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 2)

        data = self.cursor.execute("SELECT id, uploaded FROM collectors").fetchall()
        self.assertEqual(data[0][1], 1)
        self.assertEqual(data[1][1], 1)

    def test_fail(self):
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        )
        self.conn.commit()

        id = self.cursor.lastrowid

        self.queue.fail(id)

        (id, uploaded) = self.cursor.execute(
            f"SELECT id, uploaded FROM collectors WHERE id={id}"
        ).fetchone()

        self.assertEqual(uploaded, 2)
