"""
build_search_index.py

Stretch-goal script for Part 2.2 of the Smartbridge Gen AI assignment.

This replicates, in Python, what was done manually in the Azure AI Search UI
("Keyword search" import wizard): creating a simple index and populating it
with chunks of the Smartbridge video transcript.

Setup:
    pip install azure-search-documents azure-identity

Environment variables required:
    SEARCH_ENDPOINT   - e.g. "https://smartbridge-aii-search.search.windows.net"
    SEARCH_ADMIN_KEY  - Primary admin key from the Search resource's Keys blade
    SEARCH_INDEX_NAME - e.g. "smartbridge-transcript-index"

Usage:
    export SEARCH_ENDPOINT="https://smartbridge-aii-search.search.windows.net"
    export SEARCH_ADMIN_KEY="your-admin-key"
    export SEARCH_INDEX_NAME="smartbridge-transcript-index"
    python build_search_index.py transcript.txt
"""

import os
import sys
import uuid

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType,
)
from azure.search.documents import SearchClient


def chunk_text(text: str, max_chars: int = 800) -> list[str]:
    """Split transcript into paragraph-ish chunks for better search granularity."""
    words = text.split()
    chunks = []
    current = []
    current_len = 0

    for word in words:
        current.append(word)
        current_len += len(word) + 1
        if current_len >= max_chars:
            chunks.append(" ".join(current))
            current = []
            current_len = 0

    if current:
        chunks.append(" ".join(current))

    return chunks


def create_index(index_client: SearchIndexClient, index_name: str) -> None:
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchableField(name="section", type=SearchFieldDataType.String, filterable=True),
    ]

    index = SearchIndex(name=index_name, fields=fields)
    index_client.create_or_update_index(index)
    print(f"Index '{index_name}' created (or updated).")


def upload_documents(search_client: SearchClient, transcript_path: str) -> None:
    with open(transcript_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)

    documents = [
        {
            "id": str(uuid.uuid4()),
            "content": chunk,
            "section": f"segment-{i+1}",
        }
        for i, chunk in enumerate(chunks)
    ]

    result = search_client.upload_documents(documents=documents)
    succeeded = sum(1 for r in result if r.succeeded)
    print(f"Uploaded {succeeded}/{len(documents)} chunks to the index.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build_search_index.py <transcript.txt>")
        sys.exit(1)

    endpoint = os.environ.get("SEARCH_ENDPOINT")
    admin_key = os.environ.get("SEARCH_ADMIN_KEY")
    index_name = os.environ.get("SEARCH_INDEX_NAME")

    if not all([endpoint, admin_key, index_name]):
        raise EnvironmentError(
            "Please set SEARCH_ENDPOINT, SEARCH_ADMIN_KEY, and SEARCH_INDEX_NAME."
        )

    credential = AzureKeyCredential(admin_key)

    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
    create_index(index_client, index_name)

    search_client = SearchClient(
        endpoint=endpoint, index_name=index_name, credential=credential
    )
    upload_documents(search_client, sys.argv[1])
