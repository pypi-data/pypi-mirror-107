#!/usr/bin/env python3

import os
import sys

if __name__=="selfplay":
  sys.path.append(os.getcwd())
  from engine import KoksSzachy
else:
  from koksszachy.engine import KoksSzachy

import chess

DEPTH = 5 

class Selfplay:
  def __init__(self, fen):
    self.fen = fen
    self.valuator = KoksSzachy(self.fen)
    self.game = chess.Board()
    self.game.set_fen(self.fen)

  def run(self):
    m = self.valuator.ids(DEPTH)
    self.game.push_san(m)

  def run_gui(self):
    m = self.valuator.ids(DEPTH)
    return m

  def update(self,fen):
    self.fen = fen 
    self.valuator.game.set_fen(fen)

if __name__ == "__main__":
  sys.path.append(os.getcwd())
  from engine import KoksSzachy
  start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
  s = Selfplay(start_fen)
  i = 0
  while not s.game.is_game_over():
    s.run() 
    print(f'\n[{i}] {s.game.fen()}')
    print(s.game)
    s.update(s.game.fen())
    i+=1 
  '''
  while not s.game.is_game_over():
    m = s.run_gui()
    print(m)
    s.game.push_san(m)
  '''
