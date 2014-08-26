

END_CHAR = 'e'
class TorrentParser(object):
  def __init__(self, obj):
    """ Parser class used for obtaining data from a torrent. All the parsing is 
    done recursively , with _parse_int and _parse_string being the particular cases
    This constructor supports a stream object (read will fill a buffer)"""
    self.stream = obj.read()
    self.choices = {'i':self._parse_int, 'l':self._parse_list, 'd':self._parse_dict}

  def parse(self):
    """ Main entry point to the parser, will return a dictionary containing
    the relevant torrent data. It WILL fail with a probably not too very 
    message upon encountering any malformed/unexpected value along the way """
    return self._parse_dict()
  
  def _choice_func(self, char):
    return self.choices.get(char, self._parse_string)

  def _parse_string(self):
    in_size = 0
    while self.stream[in_size].isdigit():
      in_size+=1
      size = int(self.stream[:in_size])
    ret_val = self.stream[in_size+1:in_size+size+1]
    self.stream = self.stream[size+in_size+1:]
    return ret_val

  def _parse_int(self):
    if self.stream[0]!='i':
      raise Exception('Invalid function called : Stream should start with an "i"')
    i = 1
    while self.stream[1:1+i].isdigit():
      i+=1;
    ret_val = int(self.stream[1:i])
    if self.stream[i]!=END_CHAR:
      raise Exception('Invalid integer format')
    self.stream = self.stream[i+1:]
    return ret_val

  def _parse_list(self):
    ret_val = []
    if self.stream[0]!='l':
      raise Exception('Invalid list format')
    # shift
    self.stream = self.stream[1:]
    while self.stream[0]!=END_CHAR:
      next_parse = self._choice_func(self.stream[0])
      value = next_parse()
      ret_val.append(value)
    self.stream = self.stream[1:]
    return ret_val

  def _parse_dict(self):
    ret_val = {}
    self.stream = self.stream[1:]
    while self.stream[0]!=END_CHAR:
      next_parse = self._choice_func(self.stream[0])
      key = next_parse()
      next_parse = self._choice_func(self.stream[0])
      value = next_parse()
      ret_val[key] = value
    self.stream = self.stream[1:]
    return ret_val
