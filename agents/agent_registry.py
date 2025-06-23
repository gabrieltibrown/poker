from agents.my_first_agent import MyFirstAgent
from agents.random_agent import RandomAgent
from agents.call_agent import CallAgent
from agents.tight_agent import TightAgent
from agents.aggressive_agent import AggressiveAgent
from agents.loose_agent import LooseAgent
from agents.suited_connector_agent import SuitedConnectorAgent
from agents.pair_player import PairPlayer

AGENT_MAP = {
    "MyFirstAgent": MyFirstAgent,
    "RandomAgent": RandomAgent,
    "CallAgent": CallAgent,
    "TightAgent": TightAgent,
    "AggressiveAgent": AggressiveAgent,
    "LooseAgent": LooseAgent,
    "SuitedConnectorAgent": SuitedConnectorAgent,
    "PairPlayer": PairPlayer,
    # Add others here as needed
}