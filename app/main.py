# Standard library imports
import os
from typing import Dict
import time
from io import BytesIO
from dataclasses import dataclass

# Third-party imports
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pypdf import PdfReader

# Local application imports
from utils.callbacks import FullContextCallbackHandler
from schemas.response_schema import SummaryResponse


load_dotenv(find_dotenv())


@dataclass(frozen=True)
class APIkeys:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")


app = FastAPI(
    title="PDF Summarizer API",
    description="API for summarizing PDF documents using OpenAI",
    version="1.0.0",
    docs_url="/swagger"
)


handler = FullContextCallbackHandler()
config = {'callbacks': [handler]}

main_llm = ChatOpenAI(
    api_key=APIkeys.OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0.3,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    callbacks=[handler]
)

main_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a professional document analyst and summarizer. Your expertise lies in extracting and condensing key information while maintaining accuracy and context.

        TASK:
        Analyze the provided document and create a concise summary following these guidelines:

        1. Structure:
        - Begin with the main topic/purpose
        - Include key points in order of importance
        - Maintain logical flow between ideas

        2. Content Requirements:
        - Capture essential information and main arguments
        - Preserve factual accuracy
        - Retain critical details and statistics
        - Eliminate redundant or peripheral information

        3. Style:
        - Use clear, professional language
        - Maintain objective tone
        - Keep sentences concise but informative
        - Ensure readability for business context

        4. Length:
        - Aim for approximately 15-20% of original length
        - Maximum 3-4 paragraphs

        CONTENT TO SUMMARIZE:
        {pdf_content}

        OUTPUT FORMAT:
        Provide a cohesive summary in clear paragraphs without section headers or bullet points."""
            ),
            (
                "human", 
                "Please provide a clear and concise summary of this document."
            ),
        ]
    )

main_chain = (main_prompt | main_llm).with_config(callbacks=[handler])


def extract_pdf_text(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file using PyPDF.
    
    Args:
        file_bytes (bytes): The PDF file in bytes
        
    Returns:
        str: Extracted text from the PDF
        
    Raises:
        ValueError: If PDF has more than one page
    """
    
    # Create PDF reader object
    pdf_file = BytesIO(file_bytes)
    pdf_reader = PdfReader(pdf_file)
    
    # Check page count
    if len(pdf_reader.pages) > 1:
        raise ValueError("Only single-page PDFs are supported")
    
    # Extract text from first page
    text = pdf_reader.pages[0].extract_text()
    
    if not text.strip():
        raise ValueError("No text content found in the PDF")
        
    return text

def summarize(pdf_content: str) -> Dict[str, str]:
    """
    Generate a summary of the PDF content using the LLM chain.
    
    Args:
        pdf_content (str): Text content extracted from the PDF
        
    Returns:
        Dict[str, str]: Dictionary containing the summary
    """
    result = main_chain.invoke(
        {"pdf_content": pdf_content},
        config=config
    )
    
    return {"summary": result.content.strip()}


def inference(file: UploadFile) -> Dict[str, str]:
    """
    Process the uploaded PDF file and generate a summary.
    
    Args:
        file (UploadFile): The uploaded PDF file
        
    Returns:
        Dict[str, str]: Dictionary containing the summary
    """
    start = time.time()
    
    # Read and extract text from PDF
    pdf_content = extract_pdf_text(file.file.read())
    
    # Generate summary
    result = summarize(pdf_content)
    
    end = time.time()
    print(f'Execution time: {end-start:.2f}s')
    
    return result


@app.post("/summarize", response_model=SummaryResponse)
async def generate_summary(file: UploadFile = File(...)) -> JSONResponse:
    """
    Endpoint to generate a summary from an uploaded PDF file.
    
    Args:
        file (UploadFile): The PDF file to summarize
        
    Returns:
        JSONResponse: The generated summary
    """
    if not file.filename.endswith('.pdf'):
        return JSONResponse(
            status_code=400,
            content={"error": "Only PDF files are supported"}
        )
    
    try:
        result = inference(file)
        return JSONResponse(content=result)
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
