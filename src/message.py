import re
import collections
import hashlib
from Crypto.Util.number import bytes_to_long
import html

HTMLHeader = """<html>
  <head>
      <title>[Cumulus] Clone Report</title>
      <style type="text/css">
          body {font-family:sans-serif;}
          table {
            background-color:white;
            border:0px;
            padding:0px; 
            border-spacing:4px;
            table-layout: fixed;
          }
          td {
            background-color:rgba(192,212,238,0.8); 
            border:0px; 
            padding:8px; 
            vertical-align:top; 
            border-radius:8px
          }
          pre {
            background-color:white; 
            padding:4px;
          }
          a {
            color:darkblue;
          }
      </style>
  </head>
  <body>
    <h2>[Cumulus] Clone Report</h2>
    <!-- <table>
    <tr style="font-size:14pt">
    <td><b>System:</b> &nbsp; ca.usask.cs.srlab.simLib</td>
    <td><b>Clone pairs:</b> &nbsp; 13</td>
    <td><b>Clone classes:</b> &nbsp; 13</td>
    </tr>
    <tr style="font-size:12pt">
    <td style="background-color:white">Clone type: &nbsp; 3-2</td>
    <td style="background-color:white">Granularity: &nbsp; blocks-blind</td>
    <td style="background-color:white">Max diff threshold: &nbsp; 30%</td>
    <td style="background-color:white">Clone size: &nbsp; 10 - 2500 lines</td>
    <td style="background-color:white">Total blocks-blind: &nbsp; 1136</td>
    </tr>
    </table> -->
    <br>
"""

HTMLCloneDOMHeader = """		<table style="border:2px solid lightgrey; border-radius:8px; margin-left:30px; margin-right:30px;">
			<tr><td style="background-color:white">
			<table style="width: 100%">
				<tr>"""

HTMLCloneDOMFooter = """				</tr>
			</table>
			</td></tr>
		</table>
		<br>
"""

HTMLFooter = """    <script language="JavaScript">
    function ShowHide(divId) { 
        if(document.getElementById(divId).style.display == 'none') {
            document.getElementById(divId).style.display='block';
        } else { 
            document.getElementById(divId).style.display = 'none';
        } 
    }
    </script>
  </body>
</html>
"""

ExpectedResponse = {'serv_file': 'stock/20.214.226.173:5000/content/sample.c.ifdefed', 'serv_startline': '3', 'serv_endline': '38', 'serv_content': 'static x x (x *x, int x, int *x) {\n    int x;\n    x x;\n    x.x = x;\n    x.x = x;\n    x.x = 0;\n    x.x = 0;\n    for (x = x; x < x (x); ++x) {\n        x[x]++;\n        x.x++;\n        if (x (x, x) == x)\n            break;\n        else if (x (x, x)) {\n            x (x.x, x.x, x + x (x, x));\n            if (x (x, x) != x) {\n                x (x.x, x.x, x + 1);\n            }\n            break;\n        }\n        else if (x (x, x) == x) {\n            struct {\n                int x;\n                x *x;\n            } *x;\n            int x;\n            x = x (x, x);\n            x (x.x, x.x, x + x -> x [0].x);\n            for (x = 1; x < x->x; x += 2)\n                x (x.x, x.x, x +x->x[x + 1].x);\n            break;\n        }\n    }\n    if (x == x (x))\n        x[x]++;\n    return x;\n}', 'clnt_cfid': 595, 'darkweb_url': 'http://20.214.226.173:5000/post_reply/6', 'clnt_cloneclass': {595: ['101', '/home/sindo/EiC-4.4.3/test/EiCtests/testlimits.c.ifdefed', '143', 3045915941841438357], 1199: ['43', '/home/sindo/EiC-4.4.3/src/optomizer.c.ifdefed', '78', 2468364491199913620]}}

def getHTMLHeader():
  return HTMLHeader

def getHTMLFooter():
  return HTMLFooter

def getHTMLCloneDOMHeader():
  return HTMLCloneDOMHeader

def getHTMLCloneDOMFooter():
  return HTMLCloneDOMFooter

def tokenizer(content):
  # lineCount = content.count("\n")
  seperator = "[ \t\n\r\f.]"
  tokenList = re.split(seperator,content)
  tokenList = list(filter(lambda x: x != '', tokenList))
  tokenFrequencyDict = collections.Counter(tokenList)
  return tokenFrequencyDict

def getSimHash(tokenFrequencyDict):
  v = [0 for i in range(64)]
  
  for token, frequency in tokenFrequencyDict.items():
    hash = bytes_to_long(hashlib.sha256(token.encode()).digest()[:8]) # 64 bit hash in int  TO DO: implement efficient hash
    for i in range(64):
      bit = (hash>>i) & 1
      if bit:
        v[i] += frequency
      else:
        v[i] -= frequency

  simhash = 0
  for freqSum in v:
    if freqSum > 0:
      simhash = (simhash << 1) | 1
    else:
      simhash = (simhash << 1) | 0

  return simhash

def getHammingDistance(simhash1, simhash2):
  xor = simhash1^simhash2
  hamming = bin(xor).count('1')
  return hamming

def getContent(filename, s, e):
  #filename = "C:\\Users\\USER\\" + ("\\".join(filename.split("/")[3:]))[:-8]
  output = ""
  with open(filename, "r") as f:
    for i in range(1, s):
      f.readline()
    
    for i in range(e+1-s):
      output += f.readline()
  
  return output

def checkCloneWithCoreGroup(clnt_cloneclass:dict, serv_content_simhash):
  print(clnt_cloneclass)

  ServerGroupList = {}

  for cfid, cfid_metadata in clnt_cloneclass.items():
    # @TODO 리스트 순서 변경
    startline = int(cfid_metadata[0])
    endline = int(cfid_metadata[2])
    filename = cfid_metadata[1]
    simhash = cfid_metadata[3]

    gapHD = getHammingDistance(serv_content_simhash, simhash)

    getCode = getContent(filename, startline, endline)

    if gapHD in ServerGroupList.keys():
      ServerGroupList[gapHD].append([
        cfid,
        filename,
        startline,
        endline,
        getCode
      ])
    else:
      ServerGroupList[gapHD] = [
        [
          cfid,
          filename,
          startline,
          endline,
          getCode
        ]
      ]

  return ServerGroupList

def ServerGroupDictToHTML(ServerGroupDict:dict):
  OutputHTML = ""

  key = sorted(ServerGroupDict.keys())
  for GapHD in key:
    MetaDataList = ServerGroupDict[GapHD]
    print(GapHD, MetaDataList)
    for MetaData in MetaDataList:

      # MetaData[0] == cfid
      # MetaData[1] == filename
      # MetaData[2] == startline
      # MetaData[3] == endline
      # MetaData[4] == full Code

      # gen div - title?
      OutputHTML += "\t"*5 + "<div>\n"
      OutputHTML += "\t"*6 + f"""<a onclick="javascript:ShowHide('frag{MetaData[0]}')" href="javascript:;" style="word-break: break-all;">{MetaData[1]}: {MetaData[2]}-{MetaData[3]}</a><br><br>\n"""
      OutputHTML += "\t"*6 + f"simhash 오차율 : {GapHD}\n"
      OutputHTML += "\t"*5 + "</div>\n"

      # den div - content
      OutputHTML += "\t"*5 + f"""<div id="frag{MetaData[0]}" style="display:none"><pre style="overflow: scroll;"><pre>\n"""
      OutputHTML += html.escape(MetaData[4])
      
      OutputHTML += "\t"*5 + "</pre></div>\n"
  
  return OutputHTML

def MonitoringDictToHTML(MonitoringDict:dict, serv_content_simhash):
  OutputHTML = "\t"*5 + "<div>\n"
  OutputHTML += "\t"*6 + f"""<a onclick="javascript:ShowHide('frag-{MonitoringDict['clnt_cfid']}')" href="javascript:;" style="word-break: break-all;">{MonitoringDict['darkweb_url']}: {MonitoringDict['serv_startline']}-{MonitoringDict['serv_endline']}</a><br><br>\n"""
  OutputHTML += "\t"*6 + f"simhash : {format(serv_content_simhash, '#066b')}\n"
  OutputHTML += "\t"*5 + "</div>\n"

  # den div - content
  OutputHTML += "\t"*5 + f"""<div id="frag-{MonitoringDict['clnt_cfid']}" style="display:none"><pre style="overflow: scroll;"><pre>\n"""
  OutputHTML += html.escape(MonitoringDict['serv_content'])
  
  OutputHTML += "\t"*5 + "</pre></div>\n"
  
  return OutputHTML

def getHTMLCloneDOM(OutputDict:dict=ExpectedResponse):
  print("[*]", OutputDict)
  serv_file = OutputDict['serv_file']
  serv_startline = OutputDict['serv_startline']
  serv_end = OutputDict['serv_endline']
  serv_content = OutputDict['serv_content']
  serv_content_simhash = getSimHash(tokenizer(serv_content))

  darkweb_url = OutputDict['darkweb_url']
  clnt_cfid = OutputDict['clnt_cfid']
  clnt_cloneclass = OutputDict['clnt_cloneclass']

  simhashDict = {}

  ServerGroupDict = checkCloneWithCoreGroup(clnt_cloneclass, serv_content_simhash)

  # print("[*]", ServerGroupDict)
  HTMLCloneDOM = getHTMLHeader() + getHTMLCloneDOMHeader() + \
    "\t\t\t\t<td>\n" + \
    ServerGroupDictToHTML(ServerGroupDict) + \
    "\t\t\t\t</td>\n" + \
    "\t\t\t\t<td>\n" + \
    MonitoringDictToHTML(OutputDict, serv_content_simhash) + \
    "\t\t\t\t</td>\n" + \
    getHTMLCloneDOMFooter() + getHTMLFooter()

  return HTMLCloneDOM

def main():
  k = getHTMLCloneDOM()
  with open("test.html", "w") as f:
    f.write(k)

if __name__ == '__main__':
  main()