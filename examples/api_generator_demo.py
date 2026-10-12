"""Try the API generator:

    python examples/api_generator_demo.py
"""
import sys
from pathlib import Path

# Make the project root importable when this file is run as a script
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.schema import State
from core.generator.api_generator import APIGenerator
from services.llm import LLM

# Edit these to try your own scenario
MODEL = None            # None: LLM_DEFAULT in .env; or e.g. "anthropic/claude-opus-5.5"
NUM_ACTIONS = None      # None: 3 to 5 actions
STATE = State(data={
    "available_cash_cny": 200000,
    "current_holdings": "沪深300ETF 约 5 万元",
    "investment_horizon_years": 3,
    "risk_tolerance": "中等",
    "has_a_share_account": True,
    "has_star_market_access": False,
})
OBJECTIVE = "用 20 万元在 A 股买入 2 到 3 只股票，争取 3 年年化收益 8% 以上"
CONSTRAINTS = [
    "单只股票仓位不超过可投资金的 30%",
    "不买 ST 股和上市不满一年的次新股",
    "最大回撤尽量控制在 20% 以内",
    "不加杠杆，不融资融券",
]


if __name__ == "__main__":
    llm = LLM(MODEL)
    generator = APIGenerator(llm, num_actions=NUM_ACTIONS)
    print(f"Model: {llm.model} (via {llm.provider.name})\n")

    space = generator.generate(STATE, OBJECTIVE, CONSTRAINTS)
    for i, action in enumerate(space.actions, 1):
        print(f"{i}. {action.id}\n   {action.description}\n")
