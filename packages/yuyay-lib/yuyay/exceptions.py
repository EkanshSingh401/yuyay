"""Custom exception hierarchy for the YUYAY library."""


class YUYAYError(Exception):
    """Base exception for all YUYAY library errors.

    Catch this to handle any error raised by the YUYAY library.
    """


class InvalidResponseError(YUYAYError):
    """Raised when a questionnaire response is invalid or unrecognized.

    For example: a response that is not YES, NO, or PO.
    """


class ProviderError(YUYAYError):
    """Raised when an LLM provider call fails.

    For example: API timeout, authentication failure, or invalid response from OpenAI.
    """
