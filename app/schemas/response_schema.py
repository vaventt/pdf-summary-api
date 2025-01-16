from pydantic import BaseModel, Field

class SummaryResponse(BaseModel):
    summary: str = Field(
        ...,
        description="Generated summary of the PDF content"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "This document discusses the implementation of a new project management system. Key points include the adoption of agile methodologies, integration with existing tools, and a phased rollout plan over the next quarter."
            },
            "description": "Response model for the PDF summarization endpoint containing the generated summary."
        }