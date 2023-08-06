from typing import Type
from arc import ExecutionError

from .dmenu_like import Dmenu, Rofi, RofiQL, Wofi, WofiQL
from .ui_provider import UIProvider, OpenContext


ProviderType = dict[str, dict[OpenContext, Type[UIProvider]]]
providers: ProviderType = {
    "rofi": {
        OpenContext.DEFAULT: Rofi,
        OpenContext.QUICK_LAUNCH: RofiQL,
    },
    "wofi": {
        OpenContext.DEFAULT: Wofi,
        OpenContext.QUICK_LAUNCH: WofiQL,
    },
    "dmenu": {
        OpenContext.DEFAULT: Dmenu,
        OpenContext.QUICK_LAUNCH: Dmenu,
    },
}


def get_ui_provider(provider_str: str, open_context: OpenContext) -> Type[UIProvider]:
    if provider_str not in providers:
        raise ExecutionError(
            f"{provider_str} is not a valid UI Provider. "
            f" Valid providers: {providers.keys()}"
        )
    if open_context not in providers[provider_str]:
        raise ExecutionError(f"{provider_str} does not support {open_context.value}")

    return providers[provider_str][open_context]
