import time
import urllib2
from urllib2 import urlopen

def yahooKeyStats(stock):
    try:
        sourceCode = urllib2.urlopen('http://finance.yahoo.com/q/ks?s='+stock).read()
        pbr - sourceCode.split('Price/Book</span><!-- react-text: 60 --> <!-- /react-text --><!-- react-text: 61 -->(mrq)<!-- /react-text --><sup data-reactid="62"></sup></td><td class="Fz(s) Fw(500) Ta(end)" data-reactid="63">')[1].split('</td>')[0]
        print ("price to book ratio:",pbr)
    except Exception:
        print ("failed in the main loop",str(e))
