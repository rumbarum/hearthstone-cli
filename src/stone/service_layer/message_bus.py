import logging
from collections import deque
from typing import Union

from stone.domain import command, event, model

logger = logging.getLogger(__name__)

Message = Union[command.Command, event.Event]


class MessageError(Exception):
    pass


class MessageBus:
    def __init__(
        self,
        field: model.BattleField,
        event_handlers: dict,
        command_handlers: dict,
    ):
        self.field = field
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.queue: deque = deque()

    def handle(self, message: Message):
        self.queue.append(message)
        while q := self.queue:
            message = q.popleft()
            if isinstance(message, command.Command):
                self.handle_command(message)
            elif isinstance(message, event.Event):
                self.handle_event(message)
            else:
                raise MessageError(f"{message} is not an Event of Command")

    def handle_command(self, command: command.Command):
        for handler in self.command_handlers:
            try:
                logger.debug(f"Handling command {command} with {handler}")
                handler(command)
                self.queue.extend(self.field.collect_new_messages())
            except Exception:
                logger.exception(f"Exception handling command {command}")

    def handle_event(self, event: event.Event):
        for handler in self.event_handlers:
            try:
                logger.debug(f"Handling event {event} with {handler}")
                handler(event)
                self.queue.extend(self.field.collect_new_messages())
            except Exception:
                logger.exception(f"Exception handling event {event}")
