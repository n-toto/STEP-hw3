# Read numbers
def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


# Read symbols of operation
def readMul(line, index):
  token = {'type': 'MUL'}
  return token, index + 1


def readDiv(line, index):
  token = {'type': 'DIV'}
  return token, index + 1


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def readPow(line, index):
  token = {'type': 'POW'}
  return token, index + 2
 

# Read brackets
def readBrackets(line, index, depth):
  if line[index] == '(':
      token = {'type': 'BEGIN', 'depth' : depth+1}
      depth += 1
  else:
      token = {'type': 'END', 'depth' : depth}
      depth -= 1
  return token, index + 1, depth


# Tokenize the calculating formula
def tokenize(line):
  tokens = []
  index = 0
  depth = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '*' and line[index+1] == '*':  
      (token, index) = readPow(line, index)
    elif line[index] == '*':
      (token, index) = readMul(line, index)
    elif line[index] == '/':
      (token, index) = readDiv(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '(' or ')':
      (token, index, depth) = readBrackets(line, index, depth)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  if(depth != 0):
    print('Invalid syntax: ')
    exit(1)
  return tokens


# Calculate powers
def evaluate_pow(tokens):
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'POW':
        tokens[index - 2]['number'] **= tokens[index]['number']
        del tokens[index-1:index+1]
        index -= 2
    index += 1
  return tokens


# Calculate multiplications and divisions
def evaluate_mul_div(tokens):
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'MUL':
        tokens[index - 2]['number'] *= tokens[index]['number']
        del tokens[index - 1: index + 1]
        index -= 2
      elif tokens[index - 1]['type'] == 'DIV':
        tokens[index - 2]['number'] /= tokens[index]['number']
        del tokens[index - 1: index + 1] 
        index -= 2
    index += 1
  return tokens

# Calculate additions and substractions
def evaluate_plus_minus(tokens):
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        tokens[index - 2]['number'] += tokens[index]['number']
        del tokens[index - 1: index + 1]
        index -= 2
      elif tokens[index - 1]['type'] == 'MINUS':
        tokens[index - 2]['number'] -= tokens[index]['number']
        del tokens[index - 1: index + 1]
        index -= 2
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return tokens


# Calculate all
def evaluate(tokens):
  #tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  answer = 0
  index = 0
  while index < len(tokens):
    # Find brackets
    if tokens[index]['type'] == 'BEGIN':
      index_begin = index
      depth = tokens[index]['depth']
      while(index < len(tokens)):
        if(tokens[index]['type'] == 'END' and tokens[index]['depth'] == depth):
          answer =  evaluate(tokens[index_begin + 1: index])
          del tokens[index_begin : index + 1]
          tokens.insert(index_begin, {'type': 'NUMBER', 'number' : answer})
          index = index_begin - 1
          break
        index += 1

    else:
      index += 1
  # Evaluate calculation formula
  tokens = evaluate_pow(tokens[:index])
  tokens = evaluate_mul_div(tokens[:index])
  tokens = evaluate_plus_minus(tokens[:index])
  #print(answer)
  return tokens[0]['number']


def test(line):
  tokens = tokenize(line)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("1*3/2")
  test("3-2")
  test("1.2-1")
  test("5-2.8+3.1")
  test("3*4")
  test("3*2.5")
  test("5/2")
  test("4.5/3")
  test("5/3*2")
  test("1*3/2")
  test("3*2+3")
  test("3/3+2.5")
  test("1*3/2")
  test("4.2/3+3.0*2")
  test("2**3")
  test("2**3*4")
  test("4*2**3")
  test("(1)")
  test("(1+3)")
  test("(1+3)*2")
  test("2*(3+2)")
  test("(2*4)*(3-1)")
  test("(4+2**3)/(3-8)")
  test("(5*(3+2))-4")
  test("1+(2+(3*(4+2)*3/2)+1)*6")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)