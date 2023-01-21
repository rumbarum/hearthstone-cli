from typing import Callable, Type

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


def handle_use_spell(command: commands.UseSpell, field: BattleField):
    target = field.get_target_by_uuid(command.target)
    target.life -= command.attack
    field.message_slot.append(
        events.SpellUsed(
            source=command.source,
            target=command.target,
            attack=command.attack,
            spell=command.spell,
        )
    )


def handle_attakced(event: events.Attacked, field: BattleField):
    source_obj = field.get_target_by_uuid(event.source)
    target_obj = field.get_target_by_uuid(event.target)
    rich.print(
        f"""[green]{source_obj.name}{event.source[:5]}[/green] damaged [green]{target_obj.name}{event.target[:5]}[/green] by [red]{event.attack:3}[/red]"""
    )


def handle_spell_used(event: events.SpellUsed, field: BattleField):
    source_obj = field.get_target_by_uuid(event.source)
    target_obj = field.get_target_by_uuid(event.target)

    rich.print(
        f"""[green]{source_obj.name}{event.source[:5]}[/green]'s spell [yellow]{target_obj.name}{event.spell[:5]}[/yellow] damaged [green]{event.target[:5]}[/green] by [red]{event.attack:3}[/red]"""
    )


COMMAND_HANDLERS = {
    commands.MeleeAttack: handle_melee_attack,
    commands.RangedAttack: handle_ranged_attack,
    commands.UseSpell: handle_use_spell,
}  # type: dict[Type[commands.Command], Callable]

EVENT_HANDLERS = {
    events.Attacked: [handle_attakced],
    events.SpellUsed: [handle_spell_used],
}  # type: dict[Type[events.Event], list[Callable]]
