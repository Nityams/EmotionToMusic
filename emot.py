#
# @Author: Nityam Shrestha
# emot.py-> python program that takes in Picture via url,
#           gets emotions analyzed via Microsoft Emotion api
#           generates relative music with Improviser, pyton's automatic music generation program
#


import httplib, urllib, base64, json, os, random, sys

args = sys.argv[1:]
link = args[0]
argKey = args[1] # has to be -f or -frontEnd
frontEnd = args[2]

if (argKey == '-f' or argKey == '-frontEnd') and (frontEnd =='mixed' or frontEnd =='cli' or frontEnd =='lines' or frontEnd =='blocks' or frontEnd == 'none'):

    body = {"URL": link }

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'insertApiKeyHere!!!',
    }

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/emotion/v1.0/recognize", json.dumps(body) , headers)
        response = conn.getresponse()#
        data = response.read()
        conn.close()

    except Exception as e:
        print 'Error found yo!!!'
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    mydata1 = json.loads(data)

    if type(mydata1) == dict:
        print mydata1
    else:       #i.e. no error found
        mydata = mydata1[0]
        print "-------------------"
        # dictionary
        sadness = mydata['scores']['sadness']
        neutral = mydata['scores']['neutral']
        happiness = mydata['scores']['happiness']

        data = {'sadness': sadness,'netural': neutral, 'happiness': happiness}
        maximum= max(data, key=data.get)
        maxValue = int (data.get(maximum) * 100)
        happinessValue = int(happiness * 100000)
        # happinessValue = happinessValue  if happinessValue >=1 else 1

        print maximum

        #datas:
        setI = ['SimpleSoloInstrument','SimpleSoloInstrument','PowerChords','SimpleSoloInstrument','FastStridePianist','SimpleSoloInstrument','RandomSoloist']
        setP = ['serbitat','black_metal','onvoorwaardelijk_fietsen','jazzy_blues','fietsen_intro','reincarnatie' ]
        setE = ['jazz','rocknroll','soothing','swing'] #only for happy
        setIValue = maxValue % len(setI)
        i = setI[setIValue]
        print 'I value: ', i

        if maximum == 'sadness':
            print 'sadness'
            b = random.randint(100,110)
            setPValue = happinessValue % 3             #happiness value
            p = setP[setPValue]
            print 'P Value: ',p
            fileName = 'python Improviser.py -i '+ i + ' -b '+ str(b) +' -p ' +p + ' -r 3'

        elif maximum == 'happiness':
            print 'happiness Value:' , happinessValue
            b = random.randint(195,220)

            if happinessValue >= 99500:
                hV = happinessValue % len(setE)
                e = setE[hV]
                print e
                fileName = 'python Improviser.py -e' + e + ' -b' + str(b)

            else:
                setPValue = (happinessValue % 3) +3
                p = setP[setPValue]
                print 'P Value: ',p
                fileName = 'python Improviser.py -i'+ i + ' -s -b'+ str(b) +' -p' +p
        else :
            print 'neutral'
            b = random.randint(130,140)
            setPValue = (len(setP)-1)-(happinessValue % 4)
            p = setP[setPValue]
            fileName = 'python Improviser.py -i'+ i + ' -b'+ str(b) +' -p' +p

        if frontEnd != 'None':
            os.system(fileName + ' -f '+frontEnd )
        else:
            os.system(fileName)

else:
    print 'Front End Syntax Error, has to be "-f" or "-frontEnd" followed by "none", "mixed", "cli", "lines" or "blocks" '
