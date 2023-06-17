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

def print_temp(key, init_time, actual_time, clear_temp):
  if clear_temp == False:
    delta_time = actual_time - init_time
    print_clock('0' +str(timedelta(seconds=delta_time)).split(sep='.')[0])
  else:
    print_clock('00:00:00')
  if key == "\n":
    if clear_temp:
      init_time = time.time()
    clear_temp = not clear_temp
  return init_time, clear_temp

def print_cron(key, chain, init_time_cron, actual_time, clear_cron,run):
  chain_seconds = 0
  if not clear_cron:
    delta_time = actual_time - init_time_cron
    if (int(chain[0:2])*60*60 + int(chain[2:4])*60 + int(chain[4:6])) > int(delta_time):
      chain_seconds = timedelta(hours=int(chain[0:2]),minutes=int(chain[2:4]), seconds=int(chain[4:6])-delta_time+1)
      run = True
      if chain[0] != 0:
        print_clock('0' +str(chain_seconds).split(sep='.')[0])
      else:
        print_clock('0' +str(chain_seconds).split(sep='.')[0])
    else:
      print_clock('00:00:00')
      run = False
      clear_cron = not clear_cron
  else:
    print_clock('00:00:00')
  list_numbers = ['0','1','2','3','4','5','6','7','8','9']
  if key in list_numbers and len(chain) < 6:
    chain = chain + str(key)
  if key == '\x7f' and len(chain) != 0 and not run:
    chain = chain[:-1]
  if key == "\n" and len(chain) == 6:
    if clear_cron:
      init_time_cron = time.time()
    clear_cron = not clear_cron
  if len(chain) > 4:
    time_cron = chain[:2] + ":" + chain[2:4] + ":" + chain[4:]
  elif len(chain) > 2:
    time_cron = chain[:2] + ":" + chain[2:]
  else:
    time_cron = chain
  print("time:" + time_cron)
  return chain, init_time_cron,clear_cron

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
  clear_temp = True
  chain = ''
  init_time_cron = time.time()
  clear_cron = True
  run = False
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
      init_time, clear_temp = print_temp(key, init_time, time.time(), clear_temp)
    elif resaltado == 1:
      chain, init_time_cron,clear_cron = print_cron(key,chain, init_time_cron, time.time(), clear_cron, run)
    print_menu(resaltado)
