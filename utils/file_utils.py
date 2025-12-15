import pandas as pd
import docx
from pdfminer.high_level import extract_text
from io import BytesIO


def read_uploaded_file(uploaded_file):
    """
    Reads CSV, Excel, PDF, or DOCX files and returns a DataFrame
    """
    if uploaded_file is None:
        return None

    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    elif name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    elif name.endswith(".pdf"):
        text = extract_text(uploaded_file)
        return text_to_df(text)

    elif name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text_to_df(text)

    else:
        raise ValueError("Unsupported file format")


def text_to_df(text):
    rows = []

    for line in text.split("\n"):
        parts = line.split(",")
        if len(parts) >= 3:
            rows.append(parts[:3])

    return pd.DataFrame(rows, columns=["date", "location", "cases"])
