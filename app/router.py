from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.clients.ollama_client import ollama_client
from app.request_schema import BagRequestSchema


router = APIRouter()


@router.get(
    "/bug-reports/draft",
    response_class=StreamingResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Поток SSE с событием delta, report и report_error.",
            "content-type": {"text/event-stream": {"schema": {"type": "string"}}},
        },
    }
)
async def bug_reports_draft(
    bug_request: BagRequestSchema = Depends()
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