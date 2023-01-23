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


def handle_play_card(command: commands.PlayCard, field: BattleField):
    pl = field.get_player_by_uuid(command.player)
    card = field.get_card_from_player(command.player, command.card)

    if pl.mana < card.mana:
        rich.print("NOT ENOUGH MANA")
        return
    if (
        command.minion_field_index is not None
        and pl.minion_field[command.minion_field_index] is not None
    ):
        rich.print("ALREADY TAKEN POSITION")
        return
    if issubclass(card.object, model.Minion):
        minion = card.object()
        if command.minion_field_index is not None:
            pl.minion_field[command.minion_field_index] = minion
            rich.print(
                f"{pl.uuid} play a card {card.name} on {command.minion_field_index}"
            )
            field.message_slot.append(
                events.CardPlayed(
                    player=pl.uuid,
                    card=card.uuid,
                    minion_field_index=command.minion_field_index,
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
