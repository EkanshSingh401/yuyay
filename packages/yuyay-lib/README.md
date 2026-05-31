# YUYAY Intelligence Framework

[![CI](https://github.com/EkanshSingh401/yuyay/actions/workflows/ci.yml/badge.svg)](https://github.com/EkanshSingh401/yuyay/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](https://github.com/EkanshSingh401/yuyay)
[![PyPI version](https://img.shields.io/pypi/v/yuyay)](https://pypi.org/project/yuyay/)
[![Python versions](https://img.shields.io/pypi/pyversions/yuyay)](https://pypi.org/project/yuyay/)

A multi-dimensional intelligence framework for evaluating alignment across 12 archetype dimensions — developed for the UN Office of the Future by Mitchell Gold.

```bash
pip install yuyay
```

## Quickstart

```python
from yuyay.archetypes import get_archetype_by_name
from yuyay.questionnaire import process_responses
from yuyay.fios import FIOS, FIOSConfig

# Look up an archetype
archetype = get_archetype_by_name("The Seer")
print(archetype.summary())
# → The Seer: Vision, source insight, coherence sensing

# Process questionnaire responses
report = process_responses({
    "1a": "YES",
    "1b": "NO", 
    "2a": "PO",
})
print(report.summary())
# → YES: 1 | NO: 1 | PO: 1 | Total: 3 | Flagged: 2

# Query an LLM with YUYAY context injected
import asyncio

async def main():
    fios = FIOS(FIOSConfig(
        provider="anthropic",
        model="claude-opus-4-6",
        api_key="your-key",
    ))
    result = await fios.query("What is the highest purpose of technology?")
    print(result.summary())
    # → [anthropic/claude-opus-4-6] Tokens: 850 | Latency: 1240ms | Coherence: 80/100 | Cost: $0.002400

asyncio.run(main())
```

## Modules

| Module | Purpose |
|--------|---------|
| `archetypes.py` | 12 YUYAY archetypes with gifts and shadow aspects |
| `transformers.py` | 10 transformer questions with lookup functions |
| `wheel.py` | Co-Creation Wheel — 12 societal sectors |
| `questionnaire.py` | YES/NO/PO response processor with scoring |
| `po.py` | Edward de Bono PO lateral thinking logic |
| `fios.py` | LLM orchestration — OpenAI, Anthropic, Google |
| `exceptions.py` | Custom exception hierarchy |
| `config.py` | Environment-based configuration |

## FIOS — LLM Orchestration

FIOS (Foundational Intelligent OS) injects the full YUYAY framework as system context into any LLM query and evaluates the response for coherence.

```python
from yuyay.fios import FIOS, FIOSConfig

# Query all three providers concurrently
fios = FIOS(FIOSConfig(provider="mock", model="mock-model"))
results = await fios.query_all_providers(
    "What is wisdom?",
    configs=[
        FIOSConfig(provider="anthropic", model="claude-opus-4-6", api_key="..."),
        FIOSConfig(provider="openai", model="gpt-4", api_key="..."),
        FIOSConfig(provider="google", model="gemini-pro", api_key="..."),
    ]
)
for r in results:
    print(r.summary())
```

Features:
- Provider adapter pattern — swap providers without changing business logic
- Automatic YUYAY context injection into every prompt
- Response coherence scoring against 12 archetype dimensions
- Token usage tracking and cost estimation per provider
- Retry logic with exponential backoff
- Circuit breaker pattern for resilience
- Concurrent multi-provider queries via asyncio

## The 12 Archetypes

The Seer · The Architect · The Bridgebuilder · The Steward · The Navigator · The Maker · The Catalyst · The Harmonizer · The Sage · The Oracle · The Alchemist · The Weaver

## The Transformer Questions (10 questions, 12 response fields)

Questions 1 and 2 have sub-parts (a and b), giving 12 total response fields.

Each answerable as **YES**, **NO**, or **PO** (Edward de Bono's lateral thinking operator):

1. Does the idea serve my highest purpose?
2. Is it relevant?
3. Do I have enough information to decide?
4. Can we involve other stakeholders?
5. Am I being Wise?
6. Are Judgments or Bias present?
7. Have I used compassion and mercy?
8. Is my heart making the decision on its own?
9. Does this allow peak performance?
10. Will something of lasting endurance be created?

## Links

- **Live platform:** [unofficeofthefuture.org](https://www.unofficeofthefuture.org)
- **API docs:** [yuyay-production-2e45.up.railway.app/docs](https://yuyay-production-2e45.up.railway.app/docs)
- **GitHub:** [github.com/EkanshSingh401/yuyay](https://github.com/EkanshSingh401/yuyay)

---

*Developed by Mitchell Gold — UN Office of the Future*  
*Engineering by Ekansh Singh — Georgia Institute of Technology*