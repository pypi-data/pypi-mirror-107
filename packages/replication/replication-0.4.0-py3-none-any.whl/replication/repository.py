# ##### BEGIN GPL LICENSE BLOCK #####
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


import collections
import copy
import datetime
import gzip
import logging
from pathlib import Path
from uuid import uuid4
from datetime import datetime

import zmq
from deepdiff import Delta

from replication.objects import Node, ReplicationObject

from .constants import ADDED, COMMITED, FETCHED, HEAD, RP_COMMON, UP
from .exception import NetworkFrameError, NonAuthorizedOperationError
from .protocol import DataTranslationProtocol

try:
    import _pickle as pickle
except ImportError:
    import pickle

class GraphObjectStore(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        str = "\n"
        for key, item in self.store.items():
            str += repr(item)
        return str


class Remote():
    def __init__(self, name='origin', address='127.0.0.1', port=5555):
        self.name = name
        self.address = address
        self.port = port

        self.uuid = uuid4()
        self._context = zmq.Context()
        self.poller = zmq.Poller()

        self.command = self._context.socket(zmq.DEALER)
        self.command.setsockopt(zmq.IDENTITY, self.uuid.bytes)
        self.command.connect(f"tcp://{address}:{port}")
        self.command.setsockopt(zmq.TCP_KEEPALIVE, 1)
        self.command.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 300)
        self.command.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 300)
        self.command.linger = 0

        self.data = self._context.socket(zmq.DEALER)
        self.data.setsockopt(zmq.IDENTITY, self.uuid.bytes)
        self.data.setsockopt(zmq.TCP_KEEPALIVE, 1)
        self.data.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 300)
        self.data.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 300)
        self.data.connect(f"tcp://{address}:{port+1}")
        self.data.linger = 0
        self.data.setsockopt(zmq.RATE, 1000000)
        self.data.setsockopt(zmq.RCVBUF, 2000000)
        self.poller.register(self.command, zmq.POLLIN)
        self.poller.register(self.data, zmq.POLLIN)


class Repository():
    """
    Structure responsible for replication graph manipulation
    """

    def __init__(self,
                 rdp: DataTranslationProtocol = None,
                 username :str = None,
                 bare = False,
                 *args,
                 **kwargs):
        self.username = username
        self.object_store = GraphObjectStore()
        self.rdp = rdp
        self.remotes = {}
        self._bare = bare

    def dumps(self, filepath: str):
        """ Save all session data to a .db file
        """

        nodes_ids = self.list()
        # TODO: add dump graph to replication

        nodes = []
        for node_id in nodes_ids:
            node = self.get_node(node_id)
            nodes.append(node.as_raw_chunks())

        db = dict()
        db['nodes'] = nodes
        # db['users'] = copy.copy(self._online_users)

        stime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S')

        filepath = Path(filepath)
        filepath = filepath.with_name(
            f"{filepath.stem}_{stime}{filepath.suffix}")

        with gzip.open(filepath, "wb") as f:
            logging.info(f"Writing session snapshot to {filepath}")
            pickle.dump(db, f, protocol=4)

    def loads(self, filepath: str):
        f = gzip.open(filepath, "rb")
        db = pickle.load(f)
        repo = Repository()

        nodes = db.get("nodes")

        logging.info(f"Loading {len(nodes)} node")
        self.object_store.clear()
        for node_data in nodes:
                instance = Node.from_raw_chunks(node_data)
                self.do_commit(instance)
                instance.state = FETCHED

        logging.info(f"Repository loaded from {filepath}")

        return repo


    def list(self, filter_state=None, filter_type=None):
        if filter_state:
            return [key for key, item in self.object_store.items()
                    if item.state == filter_state]
        if filter_type:
            return [key for key, item in self.object_store.items()
                    if isinstance(item, filter_type)]
        return [key for key, item in self.object_store.items()]

    def get_dependencies(self, node, deps=[]):
        node_ref = self.get_node(node)

        if node_ref and node_ref.dependencies:
            for child in node_ref.dependencies:
                if child not in deps:
                    deps.append(child)
                self.get_dependencies(child, deps)

    def get_roots(self):
        childs = []
        for node in self.object_store.values():
            if node.dependencies:
                for dep in node.dependencies:
                    if dep not in childs:
                        childs.append(dep)
        return [n for n in self.object_store.keys() if n not in childs]

    def get_node(self, uuid):
        return self.object_store.get(uuid,None)

    def get_node_by_datablock(self, datablock, default=None):
        for v in self.object_store.values():
            if not v.instance:
                continue
            if datablock == v.instance:
                return v
        return default

    def get_parents(self, child):
        parents = []
        for node in self.object_store.values():
            if node.dependencies and child in node.dependencies:
                parents.append(node)

        return parents

    def bfs_from_node(self, start_node):
        visited = []
        queue = start_node

        while queue:
            current = queue.pop(0)

            if current not in visited:
                visited.append(current)
                current_ref = self.object_store.get(current)
                if current_ref and current_ref.dependencies:
                    queue.extend(current_ref.dependencies)

        return visited

    def list_ordered(self):
        return reversed(self.bfs_from_node(self.get_roots()))

    def get_dependencies_ordered(self, node):
        assert(node)

        deps = []
        self.get_dependencies(node, deps=deps)

        return reversed(deps)

    def get_nodes_in_state(self, state=None):
        added_items = self.list(filter_state=state)
        selected_nodes = []

        for item in added_items:
            item_deps = []
            self.get_dependencies(item, deps=item_deps)

            for deps in item_deps:
                if deps not in selected_nodes and self.object_store[deps].state == state:
                    selected_nodes.append(deps)

            if item not in selected_nodes and self.object_store[item].state == state:
                selected_nodes.append(item)

        return selected_nodes

    def do_commit(self, node: Node, cache_delta = False):
        node_id = getattr(node, 'uuid', None)
        if node_id:
            existing_node = self.object_store.get(node_id)
            if existing_node:
                existing_node.patch(Delta(node.delta))
                existing_node.state = node.state
                existing_node.dependencies = node.dependencies
                if cache_delta:
                    existing_node.delta = node.delta
            else:
                if node.delta:
                    node.patch(Delta(node.delta))
                self.object_store[node_id] = node

    def check_modification_rights(self, node_id):
        if self.get_node(node_id).owner not in [self.username, RP_COMMON]:
            raise NonAuthorizedOperationError(f"Not authorized to modify the node {node_id}")

    def push_data(self, socket, node_id, identity=None, force=False):
        node = self.get_node(node_id)
        if node.state == COMMITED or force:
            owner = node.owner.encode()
            key = node.uuid.encode()
            dependencies = pickle.dumps(node.dependencies, protocol=4)

            # Server to specific Client case
            if identity:
                serialized_data = node.delta
                socket.send(identity, zmq.SNDMORE)
            else:
                serialized_data = node.buffer.dumps()

            if not serialized_data or \
                    not dependencies or \
                    not owner or \
                    not socket.IDENTITY:

                raise NetworkFrameError(
                    f"Trying to push incomplete data: {repr(node)}")

            # First step : send nodes metadata
            socket.send_multipart([key,
                                   owner,
                                   dependencies,
                                   serialized_data])
            node.buffer = None
            node.state = UP

    def push_cmd(self, socket, cmd, identity=None):
        if identity:
                socket.send(identity, zmq.SNDMORE)
        socket.send_multipart(cmd.as_raw_chunks())

    def fetch_cmd(self, socket):
        raw_command = socket.recv_multipart(0)

        if len(raw_command) == 4:
            sender = raw_command.pop(0)
        else:
            sender = 'server'

        command = ReplicationObject.from_raw_chunks(raw_command)
        command.sender = sender

        return command

    def fetch_data(self, socket):
        """
        Here we reeceive data from the wire:
            - read data from the socket
            - reconstruct an instance
        """
        frame = socket.recv_multipart(0)

        # Load node metadata

        if len(frame) == 5:
            identity = frame.pop(0)

        if len(frame) != 4:
            logging.info(frame[1])
            logging.error(f"Incomplete frame received ({len(frame)})")
            raise NetworkFrameError("Error fetching data")

        uuid = frame[0].decode()
        owner = frame[1].decode()
        dependencies = pickle.loads(frame[2])
        serialized_data = frame[3]
        dependencies = dependencies if dependencies else None


        instance = None

        # Server side replication
        if self._bare:
            instance = Node(owner=owner,
                            uuid=uuid,
                            dependencies=dependencies,
                            sender=identity,
                            bytes=serialized_data,
                            state=UP)

        # Client side replication
        else:
            instance = Node(owner=owner,
                            uuid=uuid,
                            dependencies=dependencies,
                            bytes=serialized_data,
                            state=FETCHED)

        return instance
