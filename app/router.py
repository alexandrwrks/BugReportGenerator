from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from app.clients.ollama_client import ollama_client
from app.request_schema import BagRequestSchema
from app.response_schema import BugReport


router = APIRouter()


@router.post(
    "/bug-reports/draft",
    response_class=StreamingResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Поток SSE с событием delta, report и report_error.",
            "content": {"text/event-stream": {"schema": {"type": "string"}}},
        },
    },
    response_model=BugReport,
)
async def bug_reports_draft(
    bug_request: BagRequestSchema
):
    return StreamingResponse(
        ollama_client.generate_bug_report(bug_request.text),
        media_type="text/event-stream"
    )


@router.get("/ollama/ps")
async def ollama_ps():
    return await ollama_client.ps()


@router.get("/ollama/list")
async def ollama_list():
    return await ollama_client.list()


@router.get("/ollama/pull")
async def ollama_pull():
    return await ollama_client.pull()