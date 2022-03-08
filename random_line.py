# Returns random line from essays.txt

from random import randrange
import linecache


class RandomLine():
  def _make_gen(self, reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024*1024)
  
  def rawgencount(self, filename):
    f = open(filename, 'rb')
    f_gen = self._make_gen(f.raw.read)
    return sum(buf.count(b'\n') for buf in f_gen )

  def get_random_line(self, file_name):
    line = linecache.getline(file_name, randrange(1, self.rawgencount(file_name)))
    linecache.clearcache()
    return line