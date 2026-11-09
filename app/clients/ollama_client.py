import json
from collections.abc import AsyncIterator

import httpx
from ollama import AsyncClient, ResponseError
from pydantic import ValidationError

from app.core.settings import settings
from app.response_schema import BugReport


class OllamaClient:
    def __init__(self):
        self.client = AsyncClient(settings.OLLAMA_HOST, timeout=httpx.Timeout(60.0, connect=3.0))
        self.model = settings.OLLAMA_MODEL

    async def pull(self):
        await self.client.pull(model=self.model)

    def report_error(self, code: str, message: str) -> str:
        data = json.dumps({"code": code, "message": message}, ensure_ascii=False)
        return f"event: report_error\ndata: {data}\n\n"

    async def generate_bug_report(self, bag_prompt: str) -> AsyncIterator[str]:
        parts: list[str] = []
        try:
            stream_response = await self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": bag_prompt}],
                format=BugReport.model_json_schema(),
                stream=True,
                think=False
            )

            async for chunk in stream_response:
                content = chunk.message.content

                if content:
                    parts.append(content)
                    print(content, end="", flush=True)
                    yield f"event: delta\ndata: {json.dumps(content, ensure_ascii=False)}\n\n"

                if chunk.done and chunk.load_duration is not None and chunk.total_duration is not None:
                    print(f"\nЗагрузка модели: {chunk.load_duration / 1e9:.3f} с")
                    print(f"\nПолное время ответа: {chunk.total_duration / 1e9:3f} с")

            report = BugReport.model_validate_json("".join(parts))

        except httpx.TimeoutException:
            yield self.report_error("ollama_timeout", "Ollama не ответила вовремя")
            return

        except (ResponseError, ConnectionError) as e:
            yield self.report_error("ollama_error", "Не удалось получить ответ от Ollama")
            return

        except ValidationError:
            yield self.report_error("ollama_timeout", "Ответ модели не соответствует схеме BugReport")
            return

        yield f"event: report\ndata: {report.model_dump_json()}\n\n"

    async def ps(self):
        return await self.client.ps()

    async def list(self):
        return await self.client.list()


ollama_client = OllamaClient()