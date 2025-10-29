#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import unittest
import pandas as pd
from board import CellBoard

class TestCellBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.cb = CellBoard(3, 3)

    def _create_empty_df(self):
        """Helper method to create a 3x3 empty DataFrame."""
        return pd.DataFrame([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

    def _assert_state(self, expected_df, expected_live_count):
        """Helper method to assert DataFrame state and live count."""
        pd.testing.assert_frame_equal(self.cb.df, expected_df)
        self.assertEqual(self.cb.live_count(), expected_live_count)

    def _set_and_test_state(self, initial_data, initial_count, expected_data, expected_count):
        """Helper method to set initial state, run next_state, and assert results."""
        self.cb.df = pd.DataFrame(initial_data)
        self.assertEqual(self.cb.live_count(), initial_count)
        self.cb.next_state()
        self._assert_state(pd.DataFrame(expected_data), expected_count)

    def test_init(self):
        self._assert_state(self._create_empty_df(), 0)

    def test_from_file(self):
        self.cb = CellBoard.from_file('temp/empty.txt')
        self._assert_state(self._create_empty_df(), 0)

    def test_basic_state(self):
        self.cb.next_state()
        self._assert_state(self._create_empty_df(), 0)

    def test_revive_state(self):
        self._set_and_test_state(
            initial_data=[
                [0, 0, 1],
                [0, 1, 1],
                [0, 0, 0]
            ],
            initial_count=3,
            expected_data=[
                [0, 1, 1],
                [0, 1, 1],
                [0, 0, 0]
            ],
            expected_count=4
        )

    def test_dead_state(self):
        self._set_and_test_state(
            initial_data=[
                [0, 1, 1],
                [0, 1, 1],
                [0, 0, 1]
            ],
            initial_count=5,
            expected_data=[
                [0, 1, 1],
                [0, 0, 0],
                [0, 1, 1]
            ],
            expected_count=4
        )

    def test_live_state(self):
        self._set_and_test_state(
            initial_data=[
                [0, 1, 0],
                [1, 0, 1],
                [0, 1, 0]
            ],
            initial_count=4,
            expected_data=[
                [0, 1, 0],
                [1, 0, 1],
                [0, 1, 0]
            ],
            expected_count=4
        )

    def test_kill(self):
        self.cb.df = pd.DataFrame([
            [0, 1, 0],
            [0, 0, 1],
            [0, 1, 0]
        ])
        self.assertEqual(self.cb.live_count(), 3)
        self.cb.kill(0, 1)
        self.assertEqual(self.cb.live_count(), 2)

        self.cb.next_state()
        self._assert_state(self._create_empty_df(), 0)

    def test_heal(self):
        self.cb.df = pd.DataFrame([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0]
        ])
        self.assertEqual(self.cb.live_count(), 2)
        self.cb.heal(0, 1)
        self.assertEqual(self.cb.live_count(), 2)

        self.cb.next_state()
        expected_df = pd.DataFrame([
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ])
        self._assert_state(expected_df, 3)
