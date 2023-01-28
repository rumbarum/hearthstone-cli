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
        source=command.source, target=command.target, spell=command.spell
    )


def handle_play_card(command: commands.PlayCard, field: BattleField):
    field.play_card(
        player=command.player,
        card=command.card,
        minion_field_index=command.minion_field_index,
    )


def handle_attakced(event: events.Attacked, field: BattleField):
    field.attacked(
        source=event.source, target=event.target, attack=event.attack
    )


def handle_spell_used(event: events.SpellUsed, field: BattleField):
    field.spell_used(
        source=event.source,
        target=event.target,
        spell=event.spell,
    )


def handle_card_played(event: events.CardPlayed, field: BattleField):
    field.card_played(player=event.player, card=event.card)


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
