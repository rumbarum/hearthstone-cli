import inspect
from typing import Callable

from stone.domain import model
from stone.service_layer import handler, message_bus


def bootstrap(
    field: model.BattleField,
) -> message_bus.MessageBus:

    dependencies = {"field": field}

    injected_event_handler = {}
    for event_type, event_handlers in handler.EVENT_HANDLERS.items():
        injected_event_handler[event_type] = [
            inject_dependencies(evnet_handler, dependencies)
            for evnet_handler in event_handlers
        ]

    injected_command_handler = {}
    for command_type, command_handler in handler.COMMAND_HANDLERS.items():
        injected_command_handler[command_type] = inject_dependencies(
            command_handler, dependencies
        )

    return message_bus.MessageBus(
        field=field,
        event_handlers=injected_event_handler,
        command_handlers=injected_command_handler,
    )


def inject_dependencies(
    handler: Callable,
    dependencies: dict[str, model.BattleField],
):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
