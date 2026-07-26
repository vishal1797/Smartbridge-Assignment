# Smartbridge Salesforce AI Assistant — Take-Home Assignment

A conversational agent that answers questions about Smartbridge's Salesforce AI
capabilities, grounded in the transcript of Smartbridge's introductory video
("AI in Salesforce: A 2024 Perspective").

## Architecture

```
[Smartbridge Video]
        |
        v
[Azure Speech Services]  --(transcription)-->  [Transcript document]
        |
        v
[Azure AI Search]  --(keyword search index)-->  [smartbridge-transcript-index]
        |
        v
[Azure AI Foundry Agent Service]  --(grounded chat + tool calling)-->  [Conversational Agent]
        |
        v
[Power Automate Flow] --(send email action)--> [Email summary delivery]
```

## A note on Copilot Studio

The assignment calls for building the agent in **Microsoft Copilot Studio**.
During development, Copilot Studio's environment page failed to load
(persistent infinite-loading state after sign-in, reproduced across Chrome
and Safari, in both normal and incognito modes). To keep the project moving,
I built the functional equivalent using **Azure AI Foundry Agent Service**
instead — same core capability (a conversational agent grounded in a
retrieval knowledge source, with an external tool/action wired in), fully
within Azure. All Copilot-Studio-specific steps below are annotated with
the Foundry equivalent actually used.

## What was built

### Part 1: Conversational Agent
- Agent created in **Azure AI Foundry Agent Service** (Copilot Studio
  substitute — see note above), model: `gpt-5.1-mini`
- Knowledge grounded via **Azure AI Search** index (see Part 2.2)
- *(Stretch goal)* Action wired via **Power Automate**: agent can trigger an
  HTTP-triggered flow that sends a conversation summary by email

### Part 2: Azure AI Pipeline
1. **Transcription** — Smartbridge video was
   transcribed using **Azure Speech Studio** (Speech-to-Text, free F0 tier).
   See `docs/transcript.txt` for the output.
   - *(Stretch goal)* `scripts/transcribe_audio.py` — Python equivalent using
     the Azure Speech SDK, for reproducibility.
2. **Search index** — the transcript was chunked and loaded into an
   **Azure AI Search** index (`smartbridge-transcript-index`, Free tier,
   Keyword search) via the Import Data wizard.
   - *(Stretch goal)* `scripts/build_search_index.py` — Python equivalent
     using the `azure-search-documents` SDK.

## Repo structure

```
.
├── README.md
├── requirements.txt
├── docs/
│   ├── transcript.txt          # transcribed content used as knowledge source
│   ├── sample_qa.md            # tested Q&A pairs against the agent
│   └── screenshots/            # (optional) UI screenshots of each Azure resource
└── scripts/
    ├── transcribe_audio.py     # stretch goal: Speech-to-Text via SDK
    └── build_search_index.py   # stretch goal: Search index creation via SDK
```

## Setup (to reproduce)

1. Create an Azure resource group.
2. Deploy: Speech Services (F0 free tier), Azure AI Search (Free tier),
   a Storage account (for the source audio/transcript).
3. Run transcription (Speech Studio UI, or `scripts/transcribe_audio.py`).
4. Build the search index (Import Data UI wizard → Keyword search, or
   `scripts/build_search_index.py`).
5. Create an Azure AI Foundry project + deploy a tool-calling-capable model
   (e.g. `gpt-4o-mini`).
6. Create an Agent, connect the Azure AI Search index as a knowledge source.
7. *(Stretch)* Create a Power Automate flow with an HTTP trigger + "Send an
   email" action; wire it into the agent as an OpenAPI tool/action.

```bash
pip install -r requirements.txt

export SPEECH_KEY="..."
export SPEECH_REGION="eastus"
python scripts/transcribe_audio.py path/to/clip.wav docs/transcript.txt

export SEARCH_ENDPOINT="https://<your-search-service>.search.windows.net"
export SEARCH_ADMIN_KEY="..."
export SEARCH_INDEX_NAME="smartbridge-transcript-index"
python scripts/build_search_index.py docs/transcript.txt
```

## Testing

See `docs/sample_qa.md` for the assignment's sample questions tested against
the live agent, with the responses received.

## Cost notes

Built entirely on free/low-cost tiers: Speech (F0 free), AI Search (Free),
Storage (a few cents), Azure AI Foundry model usage (gpt-4o-mini, a few
cents for testing). Total cost stayed well under the available credit.
