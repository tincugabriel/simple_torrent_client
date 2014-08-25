

END_CHAR = 'e'
class TorrentParser(object):
  def __init__(self, path):
    self.stream = open(path).read()
    self.choices = {'i':self.parse_int, 'l':self.parse_list, 'd':self.parse_dict}

  def parse(self):
    ret_val, _ = self.parse_dict(self.stream)
    return ret_val
  
  def choice_func(self, char):
    return self.choices.get(char, self.parse_string)

  def parse_string(self, stream):
    """ Parses a string from the torrent stream
        In :
        -> The torrent stream
        Out :
        -> The parsed string
        -> The rest of the torrent stream """
    in_size = 0
    while stream[in_size].isdigit():
      in_size+=1
      size = int(stream[:in_size])
    return stream[in_size+1:in_size+size+1], stream[size+in_size+1:]

  def parse_int(self, stream):
    """ Parses an integer from the torrent file stream 
        In :
        -> stream : The remainer of the torrent file stream
                    We only care for the part parsed in this function
                    to be valid
        Out :
        -> The parsed integer
        -> The rest of the torrent stream"""
    if stream[0]!='i':
      raise Exception('Invalid function called : Stream should start with an "i"')
    i = 1
    while stream[1:1+i].isdigit():
      i+=1;
    ret_val = int(stream[1:i])
    if stream[i]!=END_CHAR:
      raise Exception('Invalid integer format')
    return ret_val, stream[i+1:]

  def parse_list(self, stream):
    ret_val = []
    if stream[0]!='l':
      raise Exception('Invalid list format')
    # shift
    stream = stream[1:]
    while stream[0]!=END_CHAR:
      choice_func = self.choice_func(stream[0])
      self.choice_func(stream[0])
      value, stream = choice_func(stream)
      ret_val.append(value)
    return ret_val, stream[1:]

  def parse_dict(self, stream):
    ret_val = {}
    stream = stream[1:]
    while stream[0]!=END_CHAR:
      choice_func = self.choice_func(stream[0])
      key, stream = choice_func(stream)
      choice_func = self.choice_func(stream[0])
      self.choice_func(stream[0])
      value, stream = choice_func(stream)
      ret_val[key] = value
    return ret_val, stream[1:]
