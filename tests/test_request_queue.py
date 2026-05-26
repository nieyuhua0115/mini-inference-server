import asyncio

import pytest

from app.model_runner import ModelRunner
from app.request_queue import PredictionQueue


class PrefixModelRunner(ModelRunner):
    def predict(self, input: str) -> str:
        return f"queued: {input}"


def test_prediction_queue_returns_model_runner_output() -> None:
    async def run_test() -> None:
        queue = PredictionQueue(PrefixModelRunner())
        await queue.start()
        try:
            assert await queue.predict("hello") == "queued: hello"
        finally:
            await queue.stop()

    asyncio.run(run_test())


def test_prediction_queue_requires_start_before_predict() -> None:
    async def run_test() -> None:
        queue = PredictionQueue(PrefixModelRunner())

        with pytest.raises(RuntimeError, match="PredictionQueue is not started"):
            await queue.predict("hello")

    asyncio.run(run_test())


def test_prediction_queue_can_restart_on_a_new_event_loop() -> None:
    queue = PredictionQueue(PrefixModelRunner())

    async def run_once() -> None:
        await queue.start()
        try:
            assert await queue.predict("hello") == "queued: hello"
        finally:
            await queue.stop()

    asyncio.run(run_once())
    asyncio.run(run_once())
