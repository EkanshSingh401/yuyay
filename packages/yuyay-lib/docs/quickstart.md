# Quickstart

## Installation

```bash
pip install yuyay
```

## Running an Evaluation

```python
from yuyay.questionnaire import process_responses

responses = {
    "1a": "YES", "1b": "NO",
    "2a": "PO", "2b": "YES",
    "3": "NO", "4": "YES",
    "5": "NO", "6": "PO",
    "7": "YES", "8": "NO",
    "9": "YES", "10": "NO",
}

report = process_responses(responses)
print(f"YES: {report.yes_count}")
print(f"NO: {report.no_count}")
print(f"PO: {report.po_count}")
print(f"Flagged: {report.flags}")
print(report.summary())
```

## Querying FIOS

```python
import asyncio
from yuyay.fios import FIOS, FIOSConfig

async def main():
    config = FIOSConfig(provider="anthropic", model="claude-sonnet-4-6")
    fios = FIOS(config)
    result = await fios.query("What does it mean to act with wisdom?")
    print(result.response)
    print(f"Coherence score: {result.coherence_score}/100")
    print(f"Cost: ${result.estimated_cost_usd:.6f}")

asyncio.run(main())
```

## Using the CLI

```bash
# List archetypes
yuyay archetypes

# List transformer questions  
yuyay transformers

# Run evaluation
yuyay evaluate --responses "1a=YES,1b=NO,2a=PO,2b=YES,3=NO,4=YES,5=NO,6=PO,7=YES,8=NO,9=YES,10=NO"

# Query FIOS
yuyay query --prompt "What is wisdom?" --provider anthropic
```