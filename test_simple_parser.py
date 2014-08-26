from simple_torrent_parser import TorrentParser
import unittest

class TorrentParserTest(unittest.TestCase):
  def test_parse_int(self):
    parser = TorrentParser(MockStream('i90e'))
    self.assertEqual(90, parser._parse_int())
  def test_parse_string(self):
    parser = TorrentParser(MockStream('4:baaz'))
    self.assertEqual('baaz', parser._parse_string())
  def test_parse_list(self):
    parser = TorrentParser(MockStream('l3:fooi90el4:baazei9000ee'))
    value = parser._parse_list()
    self.assertEqual(4, len(value))
    self.assertEqual('foo', value[0])
    self.assertEqual(90, value[1])
    self.assertEqual(1, len(value[2]))
    self.assertEqual(['baaz'], value[2])
    self.assertEqual(9000, value[3])
  def test_parse_dict(self):
    parser = TorrentParser(MockStream('d3:fooli900e4:baaze3:bari9000e4:quux5:alphae'))
    val = parser.parse()
    self.assertEqual(3, len(val.keys()))
    self.assertIsNotNone(val['foo'])
    self.assertEqual(2, len(val['foo']))
    self.assertEqual(900, val['foo'][0])
    self.assertEqual('baaz', val['foo'][1])
    self.assertIsNotNone(val['foo'])
    self.assertIsNotNone(val['bar'])
    self.assertEqual(9000, val['bar'])
    self.assertIsNotNone(val['quux'])
    self.assertEqual('alpha', val['quux'])

  def test_parse_torrent_file(self):
    parser = TorrentParser(open('sample.torrent'))
    val = parser.parse()
    self.assertIsNotNone(val['info'])
    self.assertIsNotNone(val['info']['pieces'])

class MockStream(object):
  def __init__(self, string):
    self.string = string
  def read(self):
    return self.string

if __name__ == '__main__':
  unittest.main()
