from typing import Callable, Type

import rich
import typer

from stone.domain import commands, events, model
from stone.domain.model import BattleField


def handle_melee_attack(command: commands.MeleeAttack, field: BattleField):
    field.melee_attack(
        source=command.source, target=command.target, attack=command.attack
    )


def handle_ranged_attack(command: commands.RangedAttack, field: BattleField):
    field.ranged_attack(
        source=command.source, target=command.target, attack=command.attack
    )


def handle_use_spell(command: commands.UseSpell, field: BattleField):
    field.use_spell(
        source=command.source,
        target=command.target,
        spell=command.spell,
        attack=command.attack,
    )


def handle_play_card(command: commands.PlayCard, field: BattleField):
    field.play_card(
        player=command.player,
        card=command.card,
        minion_field_index=command.minion_field_index,
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


def handle_card_played(event: events.CardPlayed, field: BattleField):
    player = field.get_player_by_uuid(event.player)
    card = player.get_card_from_player(event.card)
    rich.print(f"{player.name} play a {card.name}{card.uuid[:3]}")


COMMAND_HANDLERS = {
    commands.MeleeAttack: handle_melee_attack,
    commands.RangedAttack: handle_ranged_attack,
    commands.UseSpell: handle_use_spell,
    commands.PlayCard: handle_play_card,
}  # type: dict[Type[commands.Command], Callable]

EVENT_HANDLERS = {
    events.Attacked: [handle_attakced],
    events.SpellUsed: [handle_spell_used],
    events.CardPlayed: [handle_card_played],
}  # type: dict[Type[events.Event], list[Callable]]
