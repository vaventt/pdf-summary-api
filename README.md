# PDF Summary API

A streamlined REST API service that converts PDF documents into concise summaries using OpenAI's GPT-4o-mini. Built with FastAPI and LangChain, this service demonstrates modern API development practices, PDF processing, and AI integration.

## Features
- Single-page PDF text extraction
- AI-powered content summarization using GPT-4
- Docker containerization
- FastAPI REST endpoints
- Swagger documentation
- Proper error handling
- Performance logging

## Prerequisites
- Docker installed on your system
- OpenAI API key

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/vaventt/pdf-summary-api.git
cd pdf-summary-api
```

2. Create a .env file in the root directory (important: use this exact command to avoid environment issues):
```bash
echo -n "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

3. Build and run with Docker:
```bash
make up
```

The API will be available at `http://localhost:8000/swagger`

## API Usage

You can test the API using this Python script:

```python
import requests

def test_pdf_summary():
    url = "http://localhost:8000/summarize"
    
    # Replace with your PDF file path
    with open("test_file.pdf", "rb") as f:
        files = {"file": ("test_file.pdf", f, "application/pdf")}
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            print("Summary:", response.json()["summary"])
        else:
            print("Error:", response.json())

if __name__ == "__main__":
    test_pdf_summary()
```

Requirements for testing:
- Python 3.x
- requests library (`pip install requests`)

## Available Endpoints

- `POST /summarize`: Submit a PDF file for summarization
- `GET /health`: Health check endpoint

## Development

### Local Setup with Conda

1. Create and activate environment:
```bash
conda create -n pdf-summary python=3.10
conda activate pdf-summary
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run locally:
```bash
python app/main.py
```

### Docker Commands

Using Make commands for convenience:

- `make build`: Build Docker image
- `make run`: Run container
- `make dev`: Run with development mode (auto-reload)
- `make stop`: Stop container
- `make clean`: Clean everything
- `make up`: Build and run
- `make down`: Stop and clean

## Error Handling

The API handles several types of errors:
- Invalid file format (non-PDF files)
- Multi-page PDFs (only single-page supported)
- Empty or unreadable PDFs
- OpenAI API errors
- Server errors

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.