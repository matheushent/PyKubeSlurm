"""Core module for mapping common Slurmrestd errors."""

ERROR_DICT = {
    2084: "Job has already finished",
    2017: "Invalid job ID specified",
    2127: "Environment must be set",
    9001: "Failure during parsing",
    5005: "Zero Bytes were transmitted or received",
    9003: "Nothing found with query",
}
