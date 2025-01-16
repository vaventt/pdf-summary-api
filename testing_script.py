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
