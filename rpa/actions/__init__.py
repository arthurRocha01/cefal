"""Módulo de ações do CeFal."""

from rpa.actions.action_factory import ActionFactory
from rpa.actions.base_action import BaseAction
from rpa.actions.click_action import ClickAction
from rpa.actions.type_action import TypeAction
from rpa.actions.wait_action import WaitAction
from rpa.actions.select_action import SelectAction
from rpa.actions.scroll_action import ScrollAction
from rpa.actions.screenshot_action import ScreenshotAction

# Registrar ações na factory
ActionFactory.register_action('click', ClickAction)
ActionFactory.register_action('type', TypeAction)
ActionFactory.register_action('wait', WaitAction)
ActionFactory.register_action('select', SelectAction)
ActionFactory.register_action('scroll', ScrollAction)
ActionFactory.register_action('screenshot', ScreenshotAction)

__all__ = [
    'ActionFactory',
    'ClickAction',
    'TypeAction',
    'WaitAction',
    'SelectAction',
    'ScrollAction',
    'ScreenshotAction',
    'BaseAction',
]