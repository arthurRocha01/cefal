"""Configuração global do CeFal, definida via CLI."""

_matching_threshold: float = 0.85


def set_matching_threshold(value: float) -> None:
    global _matching_threshold
    _matching_threshold = value


def get_matching_threshold() -> float:
    return _matching_threshold
