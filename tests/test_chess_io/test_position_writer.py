import os

import pytest

from chess_io.position_writer import PositionWriter
from chess_logic_and_presentation.pieces.king import King


@pytest.fixture
def position_writer():
    filename = "test.test"
    return PositionWriter(filename)


@pytest.fixture
def sample_opening_name():
    opening_name = "Test Opening"
    return opening_name


@pytest.fixture
def sample_pieces():
    pieces_white = [[King("e1", True)]]
    pieces_black = [[King("e8", False)]]
    return pieces_white, pieces_black


def test_save_position(position_writer, sample_opening_name, sample_pieces):
    pieces_white, pieces_black = sample_pieces
    position_writer.save_position(sample_opening_name, pieces_white, pieces_black)
    saved_positions = position_writer.database

    assert len(saved_positions) == 1
    assert saved_positions[0][0] == sample_opening_name
    assert saved_positions[0][1][4][7] == pieces_white[0][0].character_representation
    assert saved_positions[0][1][4][0] == pieces_black[0][0].character_representation


def test_get_position_after_ord(position_writer, sample_pieces):
    pieces_white, pieces_black = sample_pieces
    position = position_writer.get_position_after_ord(pieces_white, pieces_black)

    assert position[4][7] == ord(pieces_white[0][0].character_representation)
    assert position[4][0] == ord(pieces_black[0][0].character_representation)
