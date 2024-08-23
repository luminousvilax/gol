#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import unittest
import pandas as pd
from .board import CellBoard

class TestCellBoard(unittest.TestCase):
    
    def setUp(self) -> None:
        self.cb = CellBoard(3, 3)
        
    def test_init(self):
        expect_df = pd.DataFrame([
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ])
        pd.testing.assert_frame_equal(self.cb.df, expect_df)
        self.assertEqual(self.cb.live_count(), 0)
        
    def test_from_file(self):
        self.cb = CellBoard.from_file('temp/empty.txt')
        expect_df = pd.DataFrame([
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ])
        pd.testing.assert_frame_equal(self.cb.df, expect_df)
        self.assertEqual(self.cb.live_count(), 0)
        
    def test_basic_state(self):
        expect_df = pd.DataFrame([
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ])
        self.cb.next_state()
        pd.testing.assert_frame_equal(self.cb.df, expect_df)
        self.assertEqual(self.cb.live_count(), 0)
        
    def test_revive_state(self):
        self.cb.df = pd.DataFrame([
            [0,0,1],
            [0,1,1],
            [0,0,0]
        ])
        self.assertEqual(self.cb.live_count(), 3)
        self.cb.next_state()
        expect_df = pd.DataFrame([
            [0,1,1],
            [0,1,1],
            [0,0,0]
        ])
        pd.testing.assert_frame_equal(self.cb.df, expect_df)
        self.assertEqual(self.cb.live_count(), 4)
        
    def test_dead_state(self):
        self.cb.df = pd.DataFrame([
            [0,1,1],
            [0,1,1],
            [0,0,1]
        ])
        self.assertEqual(self.cb.live_count(), 5)
        self.cb.next_state()
        expect_df = pd.DataFrame([
            [0,1,1],
            [0,0,0],
            [0,1,1]
        ])
        pd.testing.assert_frame_equal(self.cb.df, expect_df)
        self.assertEqual(self.cb.live_count(), 4)
        
    def test_live_state(self):
        self.cb.df = pd.DataFrame([
            [0,1,0],
            [1,0,1],
            [0,1,0]
        ])
        self.assertEqual(self.cb.live_count(), 4)
        self.cb.next_state()
        expect_df = pd.DataFrame([
            [0,1,0],
            [1,0,1],
            [0,1,0]
        ])
        pd.testing.assert_frame_equal(self.cb.df, expect_df)
        self.assertEqual(self.cb.live_count(), 4)
        
    def test_kill(self):
        self.cb.df = pd.DataFrame([
            [0,1,0],
            [0,0,1],
            [0,1,0]
        ])
        self.assertEqual(self.cb.live_count(), 3)
        self.cb.kill(0, 1)
        self.assertEqual(self.cb.live_count(), 2)
        
        self.cb.next_state()
        expect_df = pd.DataFrame([
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ])
        pd.testing.assert_frame_equal(self.cb.df, expect_df)
        self.assertEqual(self.cb.live_count(), 0)
