#!/usr/bin/python
# A python library that provides update when something changes in social profiles.
# Copyright (C) 2021 Shubhendra Kushwaha
# @TheShubhendra shubhendrakushwaha94@gmail.com
# This file is a part of profile-watcher <https://github.com/TheShubhendra/profile-watcher>.
#
# profile-watcher is a free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# profile-watcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with profile-watcher.  If not, see <http://www.gnu.org/licenses/>.
import asyncio
from quora import User
from .updaters import Quora
from .dispatcher import Dispatcher
from threading import Thread


class Watcher:
    def __init__(self):
        self.eventQueue = asyncio.Queue()
        self.updaters = []
        self.dispatcher = Dispatcher(self.eventQueue)

    def add_quora(self, username):
        updater = Quora(username, self)
        self.updaters.append(updater)

    async def start(self):
        tasks = []
        tasks.append(asyncio.create_task(self.dispatcher.listen()))
        for updater in self.updaters:
            tasks.append(asyncio.create_task(updater.start()))
        [await asyncio.gather(task) for task in tasks]
