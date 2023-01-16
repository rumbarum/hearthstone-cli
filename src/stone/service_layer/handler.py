import rich
import typer

from stone.domain import commands, events, model
from stone.domain.model import BattleField


def handle_melee_attack(command: commands.MeleeAttack, field: BattleField):
    target = field.get_target_by_uuid(command.target)
    attacker = field.get_target_by_uuid(command.source)
    target.life -= command.attack
    attacker.life -= target.attack
    field.message_slot.append(
        events.Attacked(
            source=command.source, target=command.target, attack=command.attack
        )
    )
    if target.attack > 0:
        field.message_slot.append(
            events.Attacked(
                source=command.target,
                target=command.source,
                attack=target.attack,
            )
        )


def handle_ranged_attack(command: commands.RangedAttack, field: BattleField):
    target = field.get_target_by_uuid(command.target)
    target.life -= command.attack
    field.message_slot.append(
        events.Attacked(
            source=command.source, target=command.target, attack=command.attack
        )
    )


def handle_attakced(event: events.Attacked, field: BattleField):
    rich.print(
        f"""[green]{event.source[:5]}[/green] damaged [green]{event.target[:5]}[/green] by [red]{event.attack:3}[/red]"""
    )


COMMAND_HANDLERS = {
    commands.MeleeAttack: handle_melee_attack,
    commands.RangedAttack: handle_ranged_attack,
}
EVENT_HANDLERS = {events.Attacked: [handle_attakced]}
