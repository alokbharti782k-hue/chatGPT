from backend.agent.executor import AgentExecutor
from backend.agent.planner import create_plan


def test_plan_has_verification_step():
    assert create_plan("build a report").steps[-1] == "verify"


def test_executor_refuses_missing_handler():
    result = AgentExecutor().execute(create_plan("goal"), {})
    assert result.completed is False
