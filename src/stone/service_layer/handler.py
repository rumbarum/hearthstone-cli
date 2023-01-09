import typer

from stone.domain import command, event, model
from stone.domain.model import BattleField


def handle_melee_attack(command: command.MeleeAttack, field: BattleField):
    target = field.get_target_by_uuid(command.target)
    attacker = field.get_target_by_uuid(command.source)
    target.life -= command.attack
    attacker.life -= target.attack


def after_attacked(event: event.Attacked, field: BattleField):
    pass


COMMAND_HANDLERS = {command.MeleeAttack: handle_melee_attack}
EVENT_HANDLERS = {event.Attacked: [after_attacked]}
