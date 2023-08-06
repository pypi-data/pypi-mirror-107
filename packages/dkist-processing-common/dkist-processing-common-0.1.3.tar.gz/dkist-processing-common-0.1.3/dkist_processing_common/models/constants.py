"""
Components of the Constant model
"""
from enum import Enum


class BudName(str, Enum):
    """
    Controlled list of names for constant stems (buds)
    """

    instrument = "INSTRUMENT"
    num_cs_steps = "NUM_CS_STEPS"
    num_modstates = "NUM_MODSTATES"
    proposal_id = "PROPOSAL_ID"
