
import re
import nltk
import pdfplumber
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file while preserving structure."""
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def semantic_chunking(text, max_chunk_size=512, min_chunk_size=50):
    """Splits text into chunks while preserving headings and structure."""
    # Step 1: Split by headings (Assumes headings are all caps or numbered)
    sections = re.split(r'\*+', text)  # Splits at one or more asterisks (*)
    # sections = re.split(r'\n(?=[A-Z][A-Z ]{3,}|[0-9]+\.)', text)
    chunks = []
    for section in sections:
        section = section.strip()
        # if len(section) > max_chunk_size:
        #     # Step 2: If section is too large, split into sentences
        #     sentences = sent_tokenize(section)
        #     current_chunk = ""
            
        #     for sentence in sentences:
        #         if len(current_chunk) + len(sentence) <= max_chunk_size:
        #             current_chunk += " " + sentence
        #         else:
        #             chunks.append(current_chunk.strip())
        #             current_chunk = sentence

        #     if current_chunk:
        #         chunks.append(current_chunk.strip())

        # elif len(section) < min_chunk_size:
        #     # Step 3: Merge small chunks with the previous one
        #     if chunks:
        #         chunks[-1] += " " + section
        #     else:
        #         chunks.append(section)
        # else:
        chunks.append(section)

    return chunks

# Load the PDF and apply chunking
pdf_text = extract_text_from_pdf("english_document_updated_3.pdf")
# pdf_text = extract_text_from_pdf("gujarati_doc_updated.pdf")
print("pdf_text")
chunks = semantic_chunking(pdf_text)

# Save chunks to a file
with open("structured_chunks.txt", "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(chunk + "\n\n")

print(f"Total Chunks: {len(chunks)}")
print(f"First 3 Chunks:\n", "\n---\n".join(chunks[:3]))
