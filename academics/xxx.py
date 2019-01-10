# -*- coding: utf-8 -*-
import codecs
import unicodedata

x = u"Wikipédia, le projet d’encyclopédie  A à á ą b b’ c ć cz d dz dź dż e è é ę f g h ch i j k l ł m m’ n ń o ò ó p p’ q r rz s ś sz t u w w’ x y z ź ż."

xtd = {ord(u'’'): u"'", ord(u'é'): u'e', ord(u'ł'): u'l',ord(u'Ł'): u'L',  }

def asciify(error):
    return xtd[ord(error.object[error.start])], error.end

codecs.register_error('asciify', asciify)

def ae():
  return x.encode('ascii', 'asciify')

def ud():
  return unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore')

def tr():
  return x.translate(xtd)

if __name__ == '__main__':
  print( 'or:%s'%x)
  #print( 'ae:%s'%ae())
  print( 'ud:%s'%ud())
