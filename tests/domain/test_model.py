import pytest

from stone.domain.command import Attack
from stone.domain.model import BattleField, Player
from stone.service_layer.handler import handle_message


@pytest.fixture
def players():
    player1 = Player()
    player2 = Player()
    return player1, player2


@pytest.fixture
def battle_field(players):
    field = BattleField(players=list(players))
    return field


def test_attack_player_5_times_with_damage_1_decreases_5_life(battle_field):
    player_a, player_b = battle_field.players
    attack_player = Attack(
        attack=1, target=player_a.uuid, source=player_b.uuid
    )
    battle_field.message_slot.append(attack_player)
    battle_field.message_slot.append(attack_player)
    battle_field.message_slot.append(attack_player)
    battle_field.message_slot.append(attack_player)
    battle_field.message_slot.append(attack_player)

    handle_message(field=battle_field)

    player_a.life == 25
