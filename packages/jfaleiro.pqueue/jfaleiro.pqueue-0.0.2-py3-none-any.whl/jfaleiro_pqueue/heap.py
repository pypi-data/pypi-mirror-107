#
#     pqueue - A simple priority queue for use cases in computational finance.
#
#     Copyright (C) 2016 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import itertools
from heapq import heappop, heappush

REMOVED = '<removed-entry>'


class Heap(object):
    def __init__(self, reverse=False):
        self.reverse = reverse
        self.priority_queue = list()
        self.finder = dict()
        self.counter = itertools.count()

    def push(self, priority, id, item):
        priority = -priority if self.reverse else priority
        if id in self.finder:
            raise IndexError(f'{id} already added')
        entry = [priority, next(self.counter), id, item]
        self.finder[id] = entry
        heappush(self.priority_queue, entry)
        return entry[1]

    def remove(self, id):
        if id not in self.finder:
            raise IndexError(f'{id} not added')
        entry = self.finder.pop(id)
        priority, count, id, item = entry
        entry[-1] = REMOVED
        return -priority if self.reverse else priority, count, id, item

    def pop(self):
        while self.priority_queue:
            priority, count, id, task = heappop(self.priority_queue)
            if task is not REMOVED:
                del self.finder[id]
                return -priority if self.reverse else priority, count, id, task
        raise IndexError('heap is empty')

    def peek(self):
        for entry in self.priority_queue:
            _, _, _, item = entry
            if item is not REMOVED:
                return tuple(entry)
        return None
