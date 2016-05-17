#!/usr/bin/env python3

import sys, re, os.path

POINTLINE = re.compile(
  r"^(#+) (?P<text>.*): (?P<points>\+?(\d+(\.\d+)?)?)(/(?P<total>\d+))?$",
  re.MULTILINE)

def tofloat(string, default):
  if string == None or len(string) == 0:
    return default
  else:
    return float(string)

def parse(filepath):
  with open(filepath) as f:
    contents = f.read()

  cumsum = {}
  curdepth = 0
  summary = [os.path.basename(filepath[:-4])]

  def sumtodepth(depth):
    nonlocal cumsum
    nonlocal curdepth
    nonlocal summary
#    print(" " * curdepth, "Cumsum:", cumsum[curdepth])
    while depth < curdepth:
      if curdepth == 3:
        summary.append(cumsum[curdepth])
      cumsum[curdepth - 1] += cumsum[curdepth]
      del(cumsum[curdepth])
      curdepth -= 1
#      print(" " * curdepth, "Cumsum:", cumsum[curdepth])

  def account(depth, points, text = None):
    nonlocal cumsum
    nonlocal curdepth
    nonlocal summary
    if depth > curdepth:
      curdepth = depth
      if depth >= 3:
        cumsum[curdepth] = points
      else:
        cumsum[curdepth] = 0.0
    elif depth < curdepth:
      sumtodepth(depth)
    else:
      if depth in cumsum.keys():
        cumsum[depth] += points
      else:
        cumsum[depth] = points
    print(cumsum)

  for match in POINTLINE.finditer(contents):
    depth = len(match.group(1))
    text = match.group("text")
    points = tofloat(match.group("points"), float('nan'))
    total = tofloat(match.group("total"), float('inf'))

    account(depth, points, text)
    print(depth, text, points, total)

  sumtodepth(1)
  return summary

def main(filepath):
  values = parse(filepath)
  print(values)

if __name__ == "__main__":
  main(sys.argv[1])
