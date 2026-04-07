from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    service: str = Field(default="ai-director-backend")
    status: str = Field(default="ok")
    phase: str = Field(default="grounded-retrieval")


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, description="User question for the course assistant.")
    user_mode: Literal["learner", "maintainer"] = Field(
        default="learner",
        description="High-level audience mode for future retrieval filtering.",
    )


class ChatResponse(BaseModel):
    question: str
    answer: str
    grounded: bool
    status: Literal["contract_only", "grounded", "scoped_ai", "out_of_scope"]
    answer_source: Literal["local_grounded", "gemini_grounded", "gemini_scoped", "out_of_scope"]
    citations: list[str]
