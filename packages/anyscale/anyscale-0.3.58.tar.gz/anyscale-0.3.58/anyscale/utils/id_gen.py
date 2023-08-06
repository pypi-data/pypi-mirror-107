from enum import Enum, unique
import secrets

import base62


@unique
class IDTypes(Enum):
    projects = "prj"
    snapshots = "sna"
    users = "usr"
    organizations = "org"
    organization_invitations = "orginv"
    sessions = "ses"
    applied_snapshots = "asn"
    clouds = "cld"
    permissions_projects = "ppr"
    permissions_sessions = "pse"
    permissions_snapshots = "psn"
    permissions_clouds = "pcl"
    permissions_organizations = "por"
    identities = "ide"
    autosync_sessions = "aus"
    session_state_transitions = "sst"
    server_sessions = "sss"
    session_commands = "scd"
    instances = "ins"
    instances_unique = "asi"
    application_templates = "apt"
    builds = "bld"
    session_operations = "sop"
    compute_templates = "cpt"
    usage_snapshots = "usp"
    namespaces = "nsp"
    runtime_environments = "rte"
    actors = "act"
    jobs = "job"


class IDGenerator:
    def __init__(self, type: IDTypes):
        self.type = type.value

    def generate_id(self) -> str:
        id_part = base62.encodebytes(secrets.token_bytes(16))
        return f"{self.type}_{id_part}"


# Use this to avoid global variables due to cloudpickle not having great support for them.
def generate_id(type: IDTypes) -> str:
    generator = IDGenerator(type)
    return generator.generate_id()
