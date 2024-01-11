from unittest.mock import mock_open, patch

import pytest

from chess_io.pgn_reader import PGNReader


def test_load_pngs_from_file_and_process_data_no_eval_get_openings_names(pgn_reader, example_pgn_data_no_eval):
    with patch("builtins.open", mock_open(read_data=example_pgn_data_no_eval)):
        pgn_reader.load_pngs_from_file_and_process("dummy_file.pgn")

    assert pgn_reader.get_openings_names() == ["Old Benoni Defense"]


def test_load_pngs_from_file_and_process_data_no_eval_get_openings_names_and_moves(
    pgn_reader, example_pgn_data_no_eval
):
    with patch("builtins.open", mock_open(read_data=example_pgn_data_no_eval)):
        pgn_reader.load_pngs_from_file_and_process("dummy_file.pgn")

    assert pgn_reader.get_openings_names_and_moves() == (
        ["Old Benoni Defense"],
        [["d4", "e3", "exd4", "c3", "f4", "Nf3", "Ne5", "Kb3", "0-1"]],
        [["c5", "cxd4", "d5", "Nc6", "e5", "e4", "f6", "e3"]],
    )


@pytest.fixture
def pgn_reader():
    return PGNReader()


@pytest.fixture
def example_pgn_data_no_eval():
    return """[Event "Rated Bullet game"]
[Site "https://lichess.org/yd5d4l9a"]
[White "claudiomat"]
[Black "MisterBiggStuff"]
[Result "0-1"]
[UTCDate "2013.12.31"]
[UTCTime "23:00:14"]
[WhiteElo "1711"]
[BlackElo "2035"]
[WhiteRatingDiff "-4"]
[BlackRatingDiff "+3"]
[ECO "A43"]
[Opening "Old Benoni Defense"]
[TimeControl "60+0"]
[Termination "Time forfeit"]

1. d4 c5 2. e3 cxd4 3. exd4 d5 4. c3 Nc6 5. f4 e5 6. Nf3 e4 7. Ne5 f6 8. Kb3 e3 0-1

"""


@pytest.fixture
def example_pgn_data_eval():
    return """[Event "Rated Bullet tournament https://lichess.org/tournament/yc1WW2Ox"]
[Site "https://lichess.org/PpwPOZMq"]
[Date "2017.04.01"]
[Round "-"]
[White "Abbot"]
[Black "Costello"]
[Result "0-1"]
[UTCDate "2017.04.01"]
[UTCTime "11:32:01"]
[WhiteElo "2100"]
[BlackElo "2000"]
[WhiteRatingDiff "-4"]
[BlackRatingDiff "+1"]
[WhiteTitle "FM"]
[ECO "B30"]
[Opening "Sicilian Defense: Old Sicilian"]
[TimeControl "300+0"]
[Termination "Time forfeit"]

1. e4 { [%eval 0.17] [%clk 0:00:30] } 1... c5 { [%eval 0.19] [%clk 0:00:30] }
2. Nf3 { [%eval 0.25] [%clk 0:00:29] } 2... Nc6 { [%eval 0.33] [%clk 0:00:30] }
3. Bc4 { [%eval -0.13] [%clk 0:00:28] } 3... e6 { [%eval -0.04] [%clk 0:00:30] }
4. c3 { [%eval -0.4] [%clk 0:00:27] } 4... b5? { [%eval 1.18] [%clk 0:00:30] }
5. Bb3?! { [%eval 0.21] [%clk 0:00:26] } 5... c4 { [%eval 0.32] [%clk 0:00:29] }
6. Bc2 { [%eval 0.2] [%clk 0:00:25] } 6... a5 { [%eval 0.6] [%clk 0:00:29] }
7. d4 { [%eval 0.29] [%clk 0:00:23] } 7... cxd3 { [%eval 0.6] [%clk 0:00:27] }
8. Qxd3 { [%eval 0.12] [%clk 0:00:22] } 8... Nf6 { [%eval 0.52] [%clk 0:00:26] }
9. e5 { [%eval 0.39] [%clk 0:00:21] } 9... Nd5 { [%eval 0.45] [%clk 0:00:25] }
10. Bg5?! { [%eval -0.44] [%clk 0:00:18] } 10... Qc7 { [%eval -0.12] [%clk 0:00:23] }
11. Nbd2?? { [%eval -3.15] [%clk 0:00:14] } 11... h6 { [%eval -2.99] [%clk 0:00:23] }
12. Bh4 { [%eval -3.0] [%clk 0:00:11] } 12... Ba6? { [%eval -0.12] [%clk 0:00:23] }
13. b3?? { [%eval -4.14] [%clk 0:00:02] } 13... Nf4? { [%eval -2.73] [%clk 0:00:21] } 0-1

"""
