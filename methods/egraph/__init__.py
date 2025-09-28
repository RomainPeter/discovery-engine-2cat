"""
E-graph implementation for Discovery Engine 2-Cat.
"""

from .egraph import EGraph, canonicalize_state, canonicalize_choreography

__all__ = [
    "EGraph",
    "canonicalize_state", 
    "canonicalize_choreography"
]

