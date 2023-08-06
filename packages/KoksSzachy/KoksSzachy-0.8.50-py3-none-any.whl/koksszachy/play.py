#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import os
DEBUG = os.getenv("DEBUG", None) is not None
SP = os.getenv("SP", None) is not None

if __name__=="koksszachy.play":
  from koksszachy.engine import KoksSzachy
  from koksszachy.selfplay import Selfplay
else:
  sys.path.append(os.getcwd())
  from engine import KoksSzachy
  from selfplay import Selfplay

import chess
import chess.svg
import webbrowser
import time
from flask import Flask, Response, request, render_template, url_for, jsonify
app = Flask(__name__) 

if not DEBUG: # jesli nie debug nie pokazuj logów flaska
  import logging
  log = logging.getLogger('werkzeug')
  log.setLevel(logging.ERROR)

arguments = [
    '-h',
    '--help',
    '-p',
    '--play',
    '-d',
    '--docs'
]

def my_help():
  mes = '''
  użycie: koksszachy [OPTION]
  Lubisz grać w szachy? Podobał ci się chess.com lub lichess? W takim razie pokochasz KoksSzachy! <3
  Po więcej informacji odwiedź: https://github.com/a1eaiactaest/KoksSzachy
  argumenty:
  -h, --help    pokaż tą wiadomość
  -p, --play    zagraj w swoje ulubione szachy! 
  -d, --docs    przeczytaj dokumentację
  '''
  print(mes)

@app.route("/")
def hello():
  r = render_template('index.html') # musialem uzyc render_template, inaczej ciezko by dzialalo z packagowaniem
  return r

@app.route("/selfplay")
def hello_selfplay():
  r = render_template('selfplay.html')
  return r

start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
s = Selfplay(start_fen)
@app.route("/spinfo/<path:fen>/") #pobiera fen zwraca ruch
def sp_move(fen):
  print(fen)
  s = Selfplay(fen)
  m = s.run_gui()
  return m 

@app.route("/info/<int:depth>/<path:fen>/") # routuj fen i depth do url tak zeby mozna bylo requestowac
def calc_move(depth, fen):
  v = KoksSzachy(fen)
  if SP:
    while 1:
      move = v.ids(depth)
      print(move)
      return move

  if DEBUG:
    start = time.time()
    print('\ndepth: %s'%depth)
    move = v.ids(depth, True)
    nodes_explored = v.leaves()
    val = v.evaluate()
    end = time.time()
    if move is None:
      print('Game over')
      return 0
    else: 
      print(move)
      print('nodes explored: %s '% nodes_explored)
      print('eval: %s'% str(val))
      print('fen: %s'% fen)
      print('time elapsed: %s'% (end-start))
      print(v.game,'\n')
      return move
  else:
    move = v.ids(depth)
    if move is None:
      return 0
    else:
      return move

# nie dziala na heroku, prawdopodobnie dlatego, ze to serwer nie client
@app.route("/analysis", methods=['POST'])
def get_data():
  if request.method == 'POST':
    import json
    import urllib
    content = request.get_json() # {"content": ["1. f3 e5 2. g4 Qh4#"]}
    pgn = content['content'][0] # ['1. f3 e5 2. g4 Qh4#']
    pgn = {"pgn": pgn, "pgnFile": "", "analyse":"true"} # dwa ostatnie tak profilaktycznie
    url = 'https://lichess.org/paste?%s'%urllib.parse.urlencode(pgn) # encode url zeby wstawic dane automatycznie
    if DEBUG:
      print(url)
    webbrowser.open_new_tab(url)
    return '', 200 # zwroc odpowiedni kod
 
def main(argument="", DEBUG=False, show=True, ngrok=False):
  try:
    if ngrok == True:
      from flask_ngrok import run_with_ngrok
      run_with_ngrok(app)
    if argument == "":
      argument = sys.argv[1]
    if argument not in arguments:
      print('\n  Wystąpił problem z rozpoznaniem argumentu %s' % argument)
      my_help()
      return 0
    else:
      if argument == '--play' or argument == '-p':
        if DEBUG:
          #os.environ['WERKZEUG_RUN_MAIN'] = 'true'
          app.run(debug=True)
        else:
          #os.environ['WERKZEUG_RUN_MAIN'] = 'false'
          if show==True:
            webbrowser.open_new_tab('http://localhost:5000')
          app.run(debug=False)
      if argument == '--docs' or argument == '-d':
        webbrowser.open_new_tab('https://github.com/a1eaiactaest/KoksSzachy/blob/main/README.md')
        return 0
      if argument == '--help' or argument == '-h':
        my_help()
        return 0
  except IndexError:
    my_help()
    return 0

if __name__ == "__main__":
  try:
    argument = sys.argv[1]
    if argument not in arguments:
      print('\n  Wystąpił problem z rozpoznaniem argumentu %s' % argument)
      my_help()
    else:
      if argument == '--play' or argument == '-p':
        if DEBUG:
          app.run(debug=True)
        else:
          webbrowser.open_new_tab('http://localhost:5000')
          app.run(debug=False)
      if argument == '--docs' or argument == '-d':
        webbrowser.open_new_tab('https://github.com/a1eaiactaest/KoksSzachy/blob/main/README.md')
      if argument == '--help' or argument == '-h':
        my_help()
  except IndexError:
    if DEBUG:
      app.run(debug=True)
    else:
      webbrowser.open_new_tab('http://localhost:5000')
      app.run(debug=False)

