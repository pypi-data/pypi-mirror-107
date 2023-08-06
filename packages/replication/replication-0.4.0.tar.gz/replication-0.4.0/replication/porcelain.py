import logging
from .exception import (UnsupportedTypeError, NetworkFrameError)
from .constants import (RP_COMMON, FETCHED, UP, COMMITED, ADDED, MODIFIED)
from .repository import Repository, Remote
from .objects import Node
import traceback
from deepdiff import DeepDiff, Delta


def add(repostitory, datablock, owner=None, dependencies=[], stamp=True):
    """Register a python to the given repository stagging area

    :param repository: Target repository
    :type repository: Repository
    :param objet: Any registered object
    :type object: Any registered object type in the given factory
    :param dependencies: Object dependencies uuid
    :type dependencies: Array of string
    :raise: UnsupportedTypeError
    """
    if repostitory.rdp.get_implementation(datablock):
        default_owner = RP_COMMON

        new_owner = owner if owner else default_owner
        new_node = Node(
            owner=new_owner,
            instance=datablock,
            dependencies=dependencies,
            state=ADDED)
        if stamp:
            try:
                setattr(datablock, 'uuid', new_node.uuid)
            except AttributeError:
                logging.warning(f"Can stamp uuid on {type(datablock)}")

        dependencies = repostitory.rdp.resolve_deps(datablock)

        for dependance in dependencies:
            dep_ref = repostitory.get_node_by_datablock(dependance)
            if dep_ref:
                new_node.add_dependency(dep_ref.uuid)
            else:
                if dependance:
                    try:
                        new_child_node = add(repostitory,
                                             dependance,
                                             owner=new_owner)
                        if new_child_node:
                            new_node.add_dependency(new_child_node)
                    except UnsupportedTypeError:
                        logging.warning(f"Skipping {type(datablock)}.")
        logging.debug(
            f"Registering {datablock} as {new_node.uuid} (owner:{new_owner})")
        repostitory.do_commit(new_node)

        return new_node.uuid
    else:
        raise UnsupportedTypeError(
            f"{type(object)} not supported, skipping.")


def apply(repository, node_id, force=False, force_dependencies=False):
        """Apply proxy to version to local datablock

        :param node: node key to apply
        :type node: string
        :param force: force node apply
        :type force: bool
        :param force_dependencies: force node dependencies apply
        :type force_dependencies: bool
        """
        node = repository.get_node(node_id)

        if node and (node.state in [FETCHED, UP] or force):

            # Setup apply queue
            deps = repository.get_dependencies_ordered(node.uuid)
            apply_queue = []
            for dep in deps:
                dep_node = repository.get_node(dep)
                if dep_node and (dep_node.state in [FETCHED] or force_dependencies):
                    apply_queue.append(dep_node)
            apply_queue.append(node)
            
            # Apply node in dependencies order
            for node in apply_queue:
                logging.debug(f"Applying {node.uuid}")
                repository.get_node(node)
                if node.instance is None:
                    instance = repository.rdp.resolve(node.data)
                    if instance is None:
                        logging.debug(f'Instanciating {node.uuid}')
                        node.instance =  repository.rdp.construct(node.data)
                    else:
                        node.instance = instance
                try:
                    repository.rdp.load(node.data, node.instance)
                    node.state = UP
                except ReferenceError:
                    logging.error(f"Apply reference error")
                    node.instance = repository.rdp.resolve(node.data)
                    traceback.print_exc()
        else:
            logging.warning(f"Can't apply node {node_id}, node in wrong state")


def evaluate_node_dependencies(repository: Repository, node_id: str):
    node = repository.get_node(node_id)

    assert(node)
    if not node.instance:
        return

    if node.dependencies:
        logging.debug(f"Clearing {len(node.dependencies)} dependencies.")
        node.dependencies.clear()

    dependencies = repository.rdp.resolve_deps(node.instance)

    logging.debug(f"found dependencies: {dependencies}")
    for dep in dependencies:
        registered_dep = repository.get_node_by_datablock(dep)
        if registered_dep:
            node.add_dependency(registered_dep.uuid)
        else:
            try:
                dep_node_uuid = add(repository,
                                    dep,
                                    owner=node.owner)
            except UnsupportedTypeError:
                logging.warning(f"Skipping {type(dep)}")
            else:
                node.add_dependency(dep_node_uuid)


def commit(repository: Repository, node_id: str):
        """Commit the given node

        :param uuid: node uuid
        :type uuid: string
        :raise ReferenceError:
        :raise StateError:
        :raise ContextError:
        """

        node = repository.get_node(node_id)

        if node.state not in [ADDED, UP]:
            logging.warning(f"Commit skipped: data in a wrong state:{repr(node)}")
            return

        evaluate_node_dependencies(repository, node_id)

        # Check for additionnal nodes to commit
        commit_queue = []

        for dep_uuid in repository.get_dependencies_ordered(node=node_id):
            dep = repository.get_node(dep_uuid)
            if dep.state in [ADDED]:
                commit_queue.append(dep_uuid)
        commit_queue.append(node_id)

        for node_id in commit_queue:
            node = repository.get_node(node_id)
            if node.state == ADDED \
                or (repository.rdp.needs_update(node.instance, node.data) and node.state == UP):
                new_version = repository.rdp.dump(node.instance, stamp_uuid=node.uuid)

                delta = repository.rdp.compute_delta(node.data, new_version)
                if delta and delta.diff:
                    node.patch(delta)
                    node.buffer = delta
                    node.state = COMMITED
                    logging.debug(f"Committed {node.uuid}")
                else:
                    logging.debug(f"Nothing to commit on node {node.uuid}")


def remote_add(repository: Repository, name, address, port):
    """ Add a new distant server remote to the repository

        :param repository: target repository to add the remote
        :type repository: Repository
        :param name: name of the remote use for operations
        :type name: str
        :param address: remote ip or dns name
        :type address: str
        :param port: remote port
        :type port: int
    """
    if name not in repository.remotes.keys():
        logging.info(f'Adding remote {name} ({address}:{port})')
        repository.remotes[name] = Remote(name=name, address=address, port=port)
    else:
        logging.error(f"Remote {name} already existing.")


def push(repository: Repository, remote: str, node_id, force=False):
    """ Publish the node and its dependencies(optionnal) on the server repository

        :param repository: target repository to add the remote
        :type repository: Repository
        :param remote: name of the remote use for operations
        :type remote: str
        :param node_id: uuid of the node
        :type node_id: str

    """
    repository.check_modification_rights(node_id)
    remote = repository.remotes.get(remote)
    node = repository.get_node(node_id)

    if node.state != COMMITED and not force:
        logging.debug("Nothing to push")
        return

    # Evaluate node to push
    push_queue = []
    for dep in repository.get_dependencies_ordered(node=node_id):
        dep_node = repository.get_node(dep)
        if dep_node.state in [COMMITED, ADDED]:
            push_queue.append(dep)
    push_queue.append(node.uuid)

    # push
    for node_id in push_queue:
        repository.push_data(remote.data, node_id)