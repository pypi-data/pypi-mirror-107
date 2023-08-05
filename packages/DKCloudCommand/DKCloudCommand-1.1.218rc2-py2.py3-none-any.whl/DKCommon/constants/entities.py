from typing import List, Union

import re


def pascal_to_snake_case(items: str) -> str:
    """Converts things like OrderRun to order_run"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", items).lower()


"""These constants are intended to be usable string representations of the Entity classes """
# These are entity types that we build custom endpoints for
VALID_ENDPOINT_ENTITY_TYPES = (
    "Company",
    "Organization",
    "Project",
    # Enable these when we want to support
    # "Kitchen", "Recipe", "Order", "OrderRun"
)
# These are the endpoints used primarily for role-based access control (RBAC)
VALID_RBAC_ENTITY_TYPES = (*VALID_ENDPOINT_ENTITY_TYPES, "User")
# These are the various entity types used to represent roles
VALID_ROLE_TYPES = ("EntityRole", "RoleAssignment")
# This is a superset of all valid entity types  (SQLEntity children)
VALID_ENTITY_TYPES = (*VALID_RBAC_ENTITY_TYPES, *VALID_ROLE_TYPES)

# Misc variants of the above
VALID_ENDPOINT_ENTITY_TYPES_LOWERCASE = (pascal_to_snake_case(e) for e in VALID_ENDPOINT_ENTITY_TYPES)
VALID_RBAC_ENTITY_TYPES_LOWERCASE = (pascal_to_snake_case(e) for e in VALID_RBAC_ENTITY_TYPES)
VALID_ENTITY_TYPES_LOWERCASE = (pascal_to_snake_case(e) for e in VALID_ENTITY_TYPES)
