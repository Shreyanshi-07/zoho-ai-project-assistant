"""Chatbot API endpoints for handling chat interactions.

This module provides endpoints for chat interactions, including regular chat,
streaming chat, message history management, and chat history clearing.
"""

import json

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)
from fastapi.responses import StreamingResponse


from app.core.config import settings
from app.core.langgraph.graph import LangGraphAgent
from app.core.limiter import limiter
from app.core.logging import logger
from app.core.metrics import llm_stream_duration_seconds

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    StreamResponse,
)
from app.services.session_naming import maybe_name_session

router = APIRouter()
agent = LangGraphAgent()


@router.post("/chat", response_model=ChatResponse)
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["chat"][0])
async def chat(
    request: Request,
    chat_request: ChatRequest,
):
    """Process a chat request using LangGraph.

    Args:
        request: The FastAPI request object for rate limiting.
        chat_request: The chat request containing messages.
        session: The current session from the auth token.

    Returns:
        ChatResponse: The processed chat response.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        print("========== SESSION ==========")
        print(dict(request.session))
        print("=============================")
        access_token = request.session.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=403,
                detail="Not authenticated"
            )
        session_id = request.session.get("user", "default-user")
        logger.info(
            "chat_request_received",
            session_id="zoho-session",
            message_count=len(chat_request.messages),
        )

        if settings.SESSION_NAMING_ENABLED:
            maybe_name_session(
                session_id,
                "Zoho Session",
                chat_request.messages
            )

        result = await agent.get_response(
            chat_request.messages, session_id, user_id=request.session.get("user"), username=request.session.get("user"),)

        logger.info("chat_request_processed", session_id=session_id)

        return ChatResponse(messages=result)
    except HTTPException:
        raise    
    except Exception as e:
        logger.exception("chat_request_failed", session_id=session_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["chat_stream"][0])
async def chat_stream(
    request: Request,
    chat_request: ChatRequest,
):
    """Process a chat request using LangGraph with streaming response.

    Args:
        request: The FastAPI request object for rate limiting.
        chat_request: The chat request containing messages.
        session: The current session from the auth token.

    Returns:
        StreamingResponse: A streaming response of the chat completion.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        session_id = request.session.get("user", "default-user")
        logger.info(
            "stream_chat_request_received",
            
            message_count=len(chat_request.messages),
        )
        access_token = request.session.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=403,
                detail="Not authenticated"
            )

        session_id = request.session.get("user", "default-user")
        if settings.SESSION_NAMING_ENABLED:
            maybe_name_session(
                session_id,
                "Zoho Session",
                chat_request.messages
            )

        async def event_generator():
            """Generate streaming events.

            Yields:
                str: Server-sent events in JSON format.

            Raises:
                Exception: If there's an error during streaming.
            """
            try:
                with llm_stream_duration_seconds.labels(model=agent.llm_service.get_llm().get_name()).time():
                    async for chunk in agent.get_stream_response(
                        chat_request.messages, session_id, user_id=request.session.get("user"), username=request.session.get("user")
                    ):
                        response = StreamResponse(content=chunk, done=False)
                        yield f"data: {json.dumps(response.model_dump(mode='json'))}\n\n"

                # Send final message indicating completion
                final_response = StreamResponse(content="", done=True)
                yield f"data: {json.dumps(final_response.model_dump(mode='json'))}\n\n"

            except Exception as e:
                logger.exception(
                    "stream_chat_request_failed",
                    session_id = request.session.get("user", "default-user"),
                    error=str(e),
                )
                error_response = StreamResponse(content=str(e), done=True)
                yield f"data: {json.dumps(error_response.model_dump(mode='json'))}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(
            "stream_chat_request_failed",
           session_id = request.session.get("user", "default-user"),
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/messages", response_model=ChatResponse)
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["messages"][0])
async def get_session_messages(
    request: Request,
):
    session_id = request.session.get("user", "default-user")
    try:
        access_token = request.session.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=403,
                detail="Not authenticated"
            )

        messages = await agent.get_chat_history(session_id)

        return ChatResponse(messages=messages)

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            "get_messages_failed",
            session_id = request.session.get("user", "default-user"),
            error=str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete("/messages")
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["messages"][0])
async def clear_chat_history(
    request: Request
):
    session_id = request.session.get("user", "default-user")
    try:
        access_token = request.session.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=403,
                detail="Not authenticated"
            )

        await agent.clear_chat_history(session_id)

        return {
            "message": "Chat history cleared successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            "clear_chat_history_failed",
            session_id = request.session.get("user", "default-user"),
            error=str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )