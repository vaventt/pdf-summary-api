from pydantic import BaseModel, Field
from fastapi import UploadFile

class PDFRequest(BaseModel):
    file: UploadFile = Field(
        ...,
        description="PDF file to be summarized (single page only)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "file": "example.pdf"
            },
            "description": "Input model for PDF summarization request. Accepts single-page PDF files only."
        }