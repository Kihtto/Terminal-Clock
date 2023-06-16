from blessed import Terminal
import time 
from datetime import timedelta

numbers = [
  [" 000 ", "0   0", "0   0", "0   0", " 000 "],
  ["  1  ", " 11  ", "1 1  ", "  1  ", "1111 "],
  ["  22 ", " 2  2", "   2 ", "  2  ", " 2222"],
  [" 333 ", "3   3", "  33 ", "3   3", " 333 "],
  ["   4 ", "  44 ", " 4 4 ", "44444", "   4 "],
  ["55555", "5    ", "5555 ", "    5", "5555 "],
  [" 666 ", "6    ", "6666 ", "6   6", " 666 "],
  ["77777", "    7", "   7 ", "  7  ", " 7   "],
  [" 888 ", "8   8", " 888 ", "8   8", " 888 "],
  [" 999 ", "9   9", " 9999", "    9", " 999 "]
]

colon = [
  " ",
  "O",
  " ",
  "O",
  " ",
]

def print_center(line, clock):
  x = term.width // 2 - 44 // 2
  y = term.height // 2 - 3 + line
  with term.location(x,y):
    print(term.orangered_on_black + clock[line])

def print_clock(text):
  line_work = ''
  clock = []
  for line in range(5):
    for character in text:
      if character == ":":
        line_work = line_work + "  " + colon[line] + " "
      else:
        line_work = line_work + " " + numbers[int(character)][line]
    clock.append(line_work)
    line_work = ''
  for line in range(5):
    print_center(line, clock)

def print_temp(key, init_time, actual_time, pause):
  if pause == False:
    delta_time = actual_time - init_time
    print_clock('0' +str(timedelta(seconds=delta_time)).split(sep='.')[0])
  else:
    print_clock('00:00:00')
  if key == "\n":
    if pause:
      init_time = time.time()
    pause = not pause
  return init_time, pause

def print_cron(key):
  print_clock('00:00:00')

def print_menu(resaltado):
  text = "Cron.  Temp.  Reloj"
  x = term.width // 2 - len(text) // 2
  y = 0
  with term.location(x,y):
    if resaltado == 1:
      print(term.black_on_orangered + text[0:5] + term.orangered_on_black + text[5:])
    elif resaltado == 2:
      print(text[:7] + term.black_on_orangered + text[7:12] + term.orangered_on_black + text[12:])
    elif resaltado == 3:
      print(text[:-5] + term.black_on_orangered + text[-5:])


term = Terminal()
with term.cbreak(), term.hidden_cursor():
  key = ''
  resaltado = 3
  init_time = ''
  pause = True
  while key.lower() != 'q':
    key = term.inkey(timeout=0.2)
    if key == "\x1b[C" and resaltado < 3:
      resaltado +=1
    elif key == "\x1b[D" and resaltado > 1:
      resaltado -=1
    print(term.home + term.orangered_on_black +term.clear)
    if resaltado == 3:
      print_clock(time.strftime("%H:%M:%S"))
    elif resaltado == 2:
      init_time, pause = print_temp(key, init_time, time.time(), pause)
    elif resaltado == 1:
      print_cron(key)
    print_menu(resaltado)
