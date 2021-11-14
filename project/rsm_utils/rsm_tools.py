"""Function and Tools for working with a Recursive State Machine"""
from project.rsm_utils.rsm import RSM


def minimize_rsm(rsm: RSM) -> RSM:
    return rsm.minimize()
