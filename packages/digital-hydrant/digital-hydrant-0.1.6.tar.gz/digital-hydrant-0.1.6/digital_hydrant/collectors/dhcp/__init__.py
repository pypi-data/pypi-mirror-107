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

from datetime import datetime

from digital_hydrant.collectors.collector import Collector


class Dhcp(Collector):
    def __init__(self, name):
        super(Dhcp, self).__init__(name)

    def run(self):
        timestamp = datetime.timestamp(datetime.now()) * 1000

        output = self.execute("dhcpcd -T 2> /dev/null")
        output = output.replace("'", "")

        payload = {"dhcp_log": output}

        for data in output.split("\n"):
            divider = "=" if "=" in data else ":"
            splits = data.split(divider)
            if len(splits) == 2:
                key = splits[0].strip()
                value = splits[1].strip()
                previous = payload[key] if key in payload else ""
                if previous == value:
                    continue

                payload[key] = (previous + " " + value).strip()

        self.queue.put(
            **{"type": self.name, "payload": payload, "timestamp": timestamp}
        )
