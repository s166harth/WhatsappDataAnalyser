import re
import pandas as pd
import matplotlib.pyplot as plt
#data = open('test.txt',encoding='utf8')

#contents = data.read()
def startwithname(line):
    patterns = [
            '([\w]+):',
            '([\w]+[\s]+[\w]+):',
            '([\w]+[\s]+[\w]+[\s]+[\w]+):',
            '([+]\d{2} \d{5} \d{5}):',
            '([+]\d{2} \d{4} \d{3} \d{3}):'
            ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, line)
    if result:
        return True
    return False

def startwithtime(line):
    date = re.match("(\d\d\/\d\d\/\d\d\d\d, \d\d:\d\d - )",line)
    if date:
        return True
    return False
#print(contents)
def get(line):
    splitline = line.split(' - ')
    datetime=splitline[0]
    date,time=datetime.split(',')
    message = ' '.join(splitline[1:])
    if startwithname(message):
        splitMessage = message.split(': ')
        author = splitMessage[0]
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message



parseddata=[]
data = open('test.txt',encoding='utf8')
buffer=[]
date,time,name=None,None,None
while True:
        line = data.readline()
        if not line:
            break
        line = line.strip()
        if startwithtime(line):
            if len(buffer) > 0:
                parseddata.append([date, time, author, ' '.join(buffer)])
            buffer.clear()
            date, time, author, message = get(line)
            buffer.append(message)
        else:
            buffer.append(line)

df = pd.DataFrame(parseddata, columns=['Date', 'Time', 'Author', 'Message'])
df.head(10)
mpa=df['Author'].value_counts()
print(mpa)
graphdata=mpa.head(10)
graphdata.plot.barh()
df['Hour'] = df['Time'].apply(lambda x : x.split(':')[0])
df['Hour'].value_counts().head(24).sort_index(ascending=False).plot.barh()
plt.xlabel('Number of messages')
plt.ylabel('Hour of Day')
