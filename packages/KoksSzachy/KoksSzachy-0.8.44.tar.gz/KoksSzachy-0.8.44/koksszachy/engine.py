#!/usr/bin/env python3
import chess
import math
import numpy as np

MAXVAL = 10000

class KoksSzachy:
  centipawns = { # centipawns
    chess.PAWN: 100, # pion
    chess.BISHOP: 300, # skoczek
    chess.KNIGHT: 300, # goniec
    chess.ROOK: 500, # wieza
    chess.QUEEN: 900, # hetman
    chess.KING: 0 # krol, zero bo nie da sie przejac
  }
  positions = {
    # gdzie najlepiej stac przedstawione w arrayach 8x8 
    # moze kiedys: https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function
    chess.PAWN: [ 
      0, 0, 0, 0, 0, 0, 0, 0,         # 8
      50, 50, 50, 50, 50, 50, 50, 50, # 7
      10, 10, 20, 30, 30, 20, 10, 10, # 6
      5, 5, 10, 25, 25, 10, 5, 5,     # 5
      0, 0, 0, 20, 20, 0, 0, 0,       # 4
      5, -5, -10, 0, 0, -10, -5, 5,   # 3
      5, 10, 10, -20, -20, 10, 10, 5, # 2
      0, 0, 0, 0, 0, 0, 0, 0          # 1
#     a  b  c  d  e  f  g  h 
    ],
    chess.KNIGHT: [
      -50,-40,-30,-30,-30,-30,-40,-50,
      -40,-20,  0,  0,  0,  0,-20,-40,
      -30,  0, 10, 15, 15, 10,  0,-30,
      -30,  5, 15, 20, 20, 15,  5,-30,
      -30,  0, 15, 20, 20, 15,  0,-30,
      -30,  5, 10, 15, 15, 10,  5,-30,
      -40,-20,  0,  5,  5,  0,-20,-40,
      -50,-40,-30,-30,-30,-30,-40,-50 
    ],
    chess.BISHOP: [
      -20,-10,-10,-10,-10,-10,-10,-20,
      -10,  0,  0,  0,  0,  0,  0,-10,
      -10,  0,  5, 10, 10,  5,  0,-10,
      -10,  5,  5, 10, 10,  5,  5,-10,
      -10,  0, 10, 10, 10, 10,  0,-10,
      -10, 10, 10, 10, 10, 10, 10,-10,
      -10,  5,  0,  0,  0,  0,  5,-10,
      -20,-10,-10,-10,-10,-10,-10,-20
    ],
    chess.ROOK: [
        0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10, 10, 10, 10, 10,  5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0
      ],
    chess.QUEEN: [
      -20,-10,-10, -5, -5,-10,-10,-20,
      -10,  0,  0,  0,  0,  0,  0,-10,
      -10,  0,  5,  5,  5,  5,  0,-10,
       -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
      -10,  5,  5,  5,  5,  5,  0,-10,
      -10,  0,  5,  0,  0,  0,  0,-10,
      -20,-10,-10, -5, -5,-10,-10,-20
    ],
    chess.KING: [
      -30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30,
      -20,-30,-30,-40,-40,-30,-30,-20,
      -10,-20,-20,-20,-20,-20,-20,-10,
       20, 20,  0,  0,  0,  0, 20, 20,
       20, 30, 10,  0,  0, 10, 30, 20
    ]}

  """
  chess.KING w middle gamie
  -50,-40,-30,-20,-20,-30,-40,-50,
  -30,-20,-10,  0,  0,-10,-20,-30,
  -30,-10, 20, 30, 30, 20,-10,-30,
  -30,-10, 30, 40, 40, 30,-10,-30,
  -30,-10, 30, 40, 40, 30,-10,-30,
  -30,-10, 20, 30, 30, 20,-10,-30,
  -30,-30,  0,  0,  0,  0,-30,-30,
  -50,-30,-30,-30,-30,-30,-30,-50
  """

  def __init__(self, fen):
    self.game = chess.Board()
    self.game.set_fen(fen)
    self.leaves_explored = 0 # mozliwosci rozwiniecia gry
    self.c = 0

  def leaves(self): # finalne mozliwosci
    my_nodes = self.leaves_explored
    self.leaves_explored = 0 # reset
    return my_nodes

  def evaluate(self): 
    # ocena pozycji
    val = 0
    for piece in self.centipawns: # iteracja przez figury i ich wartosci
      white_squares = self.game.pieces(piece, chess.WHITE) # wypisz {piece} figury na planszy 
      val += len(white_squares) * self.centipawns[piece] # ilosc wszsytkich {piece} na planszy * ich wartosc
      for ws in white_squares:
        val += np.flip(self.positions[piece][ws])

      black_squares = self.game.pieces(piece, chess.BLACK)
      val -= len(black_squares) * self.centipawns[piece]
      for bs in black_squares:
        val -= self.positions[piece][bs]
    
    return val


  # https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm 
  # zwraca liste ruchów oraz wartosc jej
  def minmax(self, from_bot, depth, move, a, b, ismax): #alpha-beta minimax
    m_tree = [] # sekwencja ruchow
    if from_bot == 0: # czy to ostatni poziom depth
      m_tree.append(move)
      return m_tree, self.evaluate()
    
    moves = list(self.game.legal_moves) # mozliwe, legalne ruchy
    #print('moves before:',moves, 'moves length:',len(moves))

    # wartosci "game over", jesli nie ma legalnych ruchow
    if not moves: # jesli nie ma ruchow sprawdz czy sa zakonczenia gry
      if self.game.is_game_over():
        if self.game.result() == '1-0': # sprawdza czy wynik jest korzystny
          m_tree.append(move)
          return m_tree, MAXVAL 
        elif self.game.result() == '0-1':
          m_tree.append(move)
          return m_tree, -MAXVAL
        else:
          return 0

    bmove = None
    bscore = -MAXVAL if ismax else MAXVAL

    if ismax: # dla gracza zwiekszajacego wartosc minimaxu
      for move in moves:
        self.leaves_explored += 1 # nowy node
        self.game.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.minmax(from_bot-1, depth+1, move, a, b, False) # jesli teraz max=True nastepnie musi byc False
        self.game.pop() # cofnij ruch

        # sprawdz czy odkryty ruch jest lepszy niz poprzedni, jesli tak zamien 
        if nscore > bscore:
          m_tree = nseq
          bscore, bmove = nscore, move

        # sprawdz czy nowy ruch jest lepszy od bety jesli jest, przerwij - to jest wlasnie alfa-beta pruning
        if nscore >= b:
          m_tree.append(bmove)
          return m_tree, bscore # b mowimy papa

        # update alfy
        if nscore > a:
          a = nscore

      # zwroc najlepszy wynik
      m_tree.append(bmove)
      #print(m_tree, bscore)
      return m_tree, bscore
          
    if not ismax: # dla gracza zmniejszajacego to samo co powyżej tyle ze dla alfy
      for move in moves:
        self.leaves_explored += 1 # dodaj odkryty node

        self.game.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.minmax(from_bot-1, depth+1, move, a, b, True) # to samo co wyzej ok. 141
        self.game.pop() # cofnij ruch

        # sprawdz czy odkryty ruch jest lepszy niz poprzedni, jesli tak zamien 
        if nscore < bscore:
          m_tree = nseq
          bscore, bmove = nscore, move

        # lepszy niz alfa?
        if nscore <= a:
          m_tree.append(bmove)
          return m_tree, bscore # a mowimy papa

        # update bety
        if nscore < b:
          b = nscore

      # zwroc najlepszy wynik
      m_tree.append(bmove)
      #print(m_tree, bscore)
      return m_tree, bscore

  # https://www.youtube.com/watch?v=JnXKZYFmGOg bardzo polecam koks filmik
  def iter_deep(self, depth, debug=False): 
    move_tree, ret = self.minmax(1, 0, None, -MAXVAL, MAXVAL, self.game.turn) # oblicz raz
    for i in range(2, depth):
      move_tree, ret = self.minmax(i, 0, None,-MAXVAL, MAXVAL, self.game.turn) 
      print(move_tree, ret)
    if debug == True:
      if len(move_tree) == 1:
        print('top:')
        for i,m in enumerate(list(self.game.legal_moves)[0:3]):
          print("   ", m)
      else:
        print('in future?:')
        for i,m in enumerate(list(reversed(move_tree))[0:3]):
          print("   ", m)
      #print(tree, move) 
    if len(move_tree) == 1:
      if not self.game.is_checkmate():
        return list(self.game.legal_moves)[0]
    return str(move_tree[-1])

if __name__ == "__main__":
  import sys
  #fen = "r1b2k1r/pp1pQppp/3P4/5P2/8/5N2/4KP1P/qN3B1R b - - 3 19"
  fen = "r1b1k3/ppp1nQ2/4P1pN/2q5/8/6P1/5PBP/R3R1K1 b - - 2 28"
  if len(sys.argv) > 1:
    v = KoksSzachy(sys.argv[1]) # bierz fen z argumentu
  else:
    v = KoksSzachy(fen)
  m = v.iter_deep(5, True) # zwroc ruch
  print(m)
