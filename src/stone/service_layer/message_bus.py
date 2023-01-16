import logging
from collections import deque
from typing import Union

from stone.domain import commands, events, model

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


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
            if isinstance(message, commands.Command):
                self._handle_command(message)
            elif isinstance(message, events.Event):
                self._handle_event(message)
            else:
                raise MessageError(f"{message} is not an Event of Command")

    def _handle_command(self, command: commands.Command):
        logger.debug(f"Handling command {command}")
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.field.collect_new_messages())
        except Exception:
            logger.exception(f"Exception handling command {command}")

    def _handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug(f"Handling event {event} with {handler}")
                handler(event)
                self.queue.extend(self.field.collect_new_messages())
            except Exception:
                logger.exception(f"Exception handling event {event}")
                continue
