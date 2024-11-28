"""
Snake Game Reinforcement Learning Package
-----------------------------------------
This package contains the core modules for the Snake AI project:
- environment: Board and game logic
- snake: Snake entity and movement logic
- vision: Snake's perception of the board
- agent: AI decision-making with Q-learning
- interpreter: State and reward processing
- display: Optional rendering functionality
- utils: Helper functions
"""

# Version of the package
__version__ = "1.0.0"

# Expose key modules for easier imports
from .environment import Environment
from .vision import Vision
from .agent import Agent
from .interpreter import Interpreter
# from .display import Display
# from .utils import *
from .cl_args import *
