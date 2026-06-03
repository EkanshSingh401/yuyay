# YUYAY Intelligence Framework

YUYAY — from the Quechua word for knowledge — is a multi-dimensional intelligence framework for evaluating alignment across 12 archetype dimensions.

## Install

```bash
pip install yuyay
```

## Quick Example

```python
from yuyay.questionnaire import process_responses

report = process_responses({"1a": "YES", "1b": "NO", "2a": "PO"})
print(report.yes_count, report.no_count, report.po_count)
print(report.flags)
```

## CLI

```bash
yuyay archetypes
yuyay transformers
yuyay evaluate --responses "1a=YES,1b=NO,2a=PO"
yuyay query --prompt "What is wisdom?" --provider anthropic
```

## Links

- [Live Platform](https://www.unofficeofthefuture.org)
- [API Docs](https://yuyay-production-2e45.up.railway.app/docs)
- [PyPI](https://pypi.org/project/yuyay/)
- [GitHub](https://github.com/EkanshSingh401/yuyay)