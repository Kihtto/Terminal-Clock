from blessed import Terminal
import time 

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

def print_centered(text):
    #x = term.width // 2 - 44 // 2
    #y = term.height // 2
    #with term.location(x, y):
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
      x = term.width // 2 - 44 // 2
      y = term.height // 2 - 5 + line
      with term.location(x,y):
        print(term.orangered_on_black + clock[line])

def print_menu():
  text = "Cron.  Temp.  Reloj"
  x = term.width // 2 - len(text) // 2
  y = 0
  with term.location(x,y):
    print(text[:-5] + term.black_on_orangered + text[-5:])


term = Terminal()
with term.cbreak(), term.hidden_cursor():
  close_terminal = ''
  while close_terminal.lower() != 'q':
    close_terminal = term.inkey(timeout=0.2)
    print(term.home + term.orangered_on_black +term.clear)
    print_centered(time.strftime("%H:%M:%S"))
    print_menu()
