__all__ = ["InvalidIsoCodeError", "IsoSourceError"]


class CountryProcessorError(Exception):
    pass


class InvalidIsoCodeError(CountryProcessorError):
    pass


class IsoSourceError(CountryProcessorError):
    pass
