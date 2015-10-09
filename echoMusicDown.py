#!/usr/bin/python
# _*_ coding£º utf-8 _*_

import urllib2
from HTMLParser import HTMLParser
import urlparse
import re
import os

class MyHTMLParser(HTMLParser):
   def __init__(self):
      HTMLParser.__init__(self)
      self.music = {}
      self.name = False
      self.href = ''
   def handle_starttag(self, tag, attrs):
      if tag == 'a':
         if attrs.__contains__(('class', 'btn play-btn')):
            self.name = False
            for name,value in attrs:
               if name == 'href':
                  self.href = value
         elif attrs.__contains__(("href",self.href)):
            self.name = True
         else:
            self.name = False
   def handle_data(self,data):
       if self.name == True:
          self.music[self.href] = data
          self.name = False
          

class DownFile:
   def __init__(self,data):
      self.data = data
      self.key = [97,{92:0,85:1,35:2,78:3,90:4,153:5,4:6,40:7,113:8,102:9,47:10,66:11,183:12,152:13,210:14,80:15,255:16,185:17,49:18,213:19,207:20,96:21,94:22,16:23,69:24,131:25,254:26,173:27,61:28,251:29,20:30,141:31,245:32,247:33,146:34,124:35,117:36,84:37,29:38,233:39,24:40,252:41,178:42,214:43,225:44,170:45,164:46,235:47,232:48,107:49,87:50,72:51,123:52,48:53,46:54,140:55,28:56,57:57,177:58,197:59,111:60,30:61,97:62,37:63,139:64,166:65,7:66,157:67,15:68,230:69,129:70,193:71,130:72,14:73,75:74,71:75,36:76,99:77,135:78,223:79,5:80,0:81,186:82,32:83,219:84,150:85,138:86,51:87,44:88,242:89,77:90,41:91,56:92,171:93,136:94,156:95,42:96,128:97,216:98,220:99,162:100,109:101,106:102,95:103,222:104,100:105,89:106,174:107,93:108,119:109,155:110,148:111,43:112,206:113,191:114,83:115,74:116,25:117,169:118,215:119,3:120,208:121,63:122,82:123,134:124,154:125,60:126,175:127,73:128,184:129,218:130,70:131,190:132,195:133,196:134,125:135,231:136,142:137,68:138,244:139,45:140,238:141,189:142,204:143,58:144,226:145,104:146,101:147,209:148,243:149,55:150,151:151,182:152,163:153,253:154,18:155,192:156,200:157,10:158,34:159,98:160,120:161,108:162,145:163,176:164,114:165,13:166,172:167,144:168,11:169,50:170,158:171,67:172,110:173,27:174,122:175,31:176,91:177,133:178,127:179,62:180,52:181,181:182,9:183,115:184,54:185,22:186,59:187,202:188,248:189,112:190,149:191,1:192,167:193,228:194,217:195,33:196,23:197,201:198,132:199,12:200,118:201,147:202,211:203,239:204,17:205,121:206,26:207,234:208,187:209,103:210,2:211,21:212,137:213,8:214,168:215,38:216,179:217,159:218,180:219,76:220,240:221,53:222,79:223,65:224,86:225,161:226,229:227,246:228,39:229,199:230,224:231,249:232,194:233,227:234,19:235,88:236,221:237,64:238,126:239,188:240,116:241,165:242,205:243,143:244,237:245,236:246,105:247,6:248,198:249,160:250,212:251,203:252,250:253,81:254,241:255}]
      self.dicUrl = {}
   def down(self):
      for k,v in self.data.items():
         pathNname=''
         content = urllib2.urlopen(urlparse.urljoin("http://www.app-echo.com",k)).read()
         m = re.findall(r'play_source\(".*\)\);', content)
         url = re.findall(r'_\(".*\)\);', m[0])[0][3:-4]
         mediaType = re.findall(r'\'.*\'', m[0])[0][1:-1]
         #self.dicUrl[self.decode(url)]=mediaType
         pathNname = v+'.mp4'
         if mediaType == "application/x-mpegURL":
            audioContent = urllib2.urlopen(self.decode(url)).read()
            s = re.findall(r'http://.*', audioContent)
            with file(pathNname.decode('utf-8'),'wb') as f:
               for d in s:
                  audio = urllib2.urlopen(d).read()
                  f.write(audio)
         elif mediaType == "audio/mpeg":
            audioContent = urllib2.urlopen(self.decode(url)).read()
            with file(pathNname,'wb') as f:
               f.write(audioContent)
         
   def decode(self,source):
      code = ''
      val = re.findall(r'[A-Z0-9]{2}',source)
      for value in val:
         index = int(value, 16)
         cc = self.key[1][index^self.key[0]]
         h = hex(cc)[2:]
         code += '%' + (cc < 0x10 and "0" + h or h).upper()
      return urllib2.unquote(code)
      
def open():
   fp=urllib2.urlopen("http://www.app-echo.com")
   html = fp.read()
   return html

if __name__ == '__main__':
   Parser = MyHTMLParser()
   Parser.feed(open())
   print Parser.music
   down = DownFile(Parser.music)
   down.down()
   
    
