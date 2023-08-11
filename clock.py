from blessed import Terminal
import time 
from datetime import timedelta, datetime

numbers = {
  '0' : [" 000 ", "0   0", "0   0", "0   0", " 000 "],
  '1' : ["  1  ", " 11  ", "1 1  ", "  1  ", "1111 "],
  '2' : ["  22 ", " 2  2", "   2 ", "  2  ", " 2222"],
  '3' : [" 333 ", "3   3", "  33 ", "3   3", " 333 "],
  '4' : ["   4 ", "  44 ", " 4 4 ", "44444", "   4 "],
  '5' : ["55555", "5    ", "5555 ", "    5", "5555 "],
  '6' : [" 666 ", "6    ", "6666 ", "6   6", " 666 "],
  '7' : ["77777", "    7", "   7 ", "  7  ", " 7   "],
  '8' : [" 888 ", "8   8", " 888 ", "8   8", " 888 "],
  '9' : [" 999 ", "9   9", " 9999", "    9", " 999 "],
  ':' : [" ", "O", " ", "O", " "]
}

def print_center(line_work, line):
  x = term.width // 2 - 44 // 2
  y = term.height // 2 - 3 + line
  with term.location(x,y):
    print(term.orangered_on_black + line_work)

def print_clock(text):
  for line in range(5):
    line_work = ''
    for character in text:
      line_work = f'{line_work} {numbers[character][line]}'
    print_center(line_work, line)

def seconds_to_clock(delta_time):
  if delta_time > 35999:
    print_clock(str(timedelta(seconds=delta_time)).split(sep='.')[0])
  else:
    print_clock('0' +str(timedelta(seconds=delta_time)).split(sep='.')[0])

def pause_or_stop(key, delta_time, pause):
  if key == "\n":
    pause = delta_time > 0
    delta_time = 0
  elif key.lower() == "p" and delta_time > 0:
    pause = not pause
    seconds_to_clock(delta_time)
    time.sleep(1)
  return delta_time, pause

def temp(key, delta_time, pause):
  delta_time, pause = pause_or_stop(key, delta_time, pause)
  delta_time += 1 if not pause else 0
  seconds_to_clock(delta_time)
  return delta_time, pause

def make_chain(key, chain):
  if len(chain) < 6 and key in [str(x) for x in range(10)]:
    chain = chain + str(key)
  if key == '\x7f' and len(chain) > 0:
    chain = chain[:-1]
  return chain

def render_chain(chain):
  if len(chain) > 4:
    time_cron = f'{chain[:2]}:{chain[2:4]}:{chain[4:]}'
  elif len(chain) > 2:
    time_cron = f'{chain[:2]}:{chain[2:]}'
  else:
    time_cron = chain
  print("time: " + time_cron)
  return time_cron

def cron(key, chain, delta_time, pause):
  chain = make_chain(key, chain)
  if delta_time > 0 and not pause:
    delta_time -= 1
  else:
    pause = True
  seconds_to_clock(delta_time)
  time_cron = render_chain(chain)
  if len(chain) == 6:
    delta_time, pause = pause_or_stop(key, delta_time, pause)
    if key == "\n" and not pause:
      delta_time_obj = datetime.strptime(time_cron, "%H:%M:%S").time()
      delta_time = (delta_time_obj.hour * 60 + delta_time_obj.minute) * 60 + delta_time_obj.second
  return chain, delta_time, pause


def print_menu(resaltado):
  text = "Cron.  Temp.  Reloj"
  x = term.width // 2 - len(text) // 2
  with term.location(x,y=0):
    if resaltado == 1:
      print(term.black_on_orangered + text[:5] + term.orangered_on_black + text[5:])
    elif resaltado == 2:
      print(text[:7] + term.black_on_orangered + text[7:12] + term.orangered_on_black + text[12:])
    elif resaltado == 3:
      print(text[:-5] + term.black_on_orangered + text[-5:])


term = Terminal()
with term.cbreak(), term.hidden_cursor():
  #general
  key = ''
  #menu
  resaltado = 3
  #temp
  pause = True
  delta_time = 0
  #cron
  chain = ''
  delta_time_cron = 0
  pause_cron = True

  print(term.home + term.orangered_on_black + term.clear)

  while key.lower() != 'q':
    #exit and time rendering
    key = term.inkey(timeout=1)
    #menu move
    if key == "\x1b[C" and resaltado < 3:
      resaltado += 1
    elif key == "\x1b[D" and resaltado > 1:
      resaltado -= 1
    #clear and rendering background
    print(term.clear)
    #rendering menu
    print_menu(resaltado)
    #choosing clock mode
    if resaltado == 3:
      print_clock(time.strftime("%H:%M:%S"))
    elif resaltado == 2:
      delta_time, pause = temp(key, delta_time, pause)
    else:
      chain, delta_time_cron, pause_cron = cron(key, chain, delta_time_cron, pause_cron)
  #clear all
  print(term.normal + term.clear)