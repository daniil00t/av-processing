import math
from os import system

def print_progress(index, total, step = 5):
  percentage = index / total * 100
  if(index % step == 0):
    system('clear')
    print(f"{percentage}%")