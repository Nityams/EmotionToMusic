import os,random

maximum = raw_input("Enter Maximum ")
maxValue = int(raw_input("Enter max Value "))
happinessValue = int (raw_input("enter happiness value: "))

setI = ['SimpleSoloInstrument','SoloInstrument','SimpleSoloInstrument','PowerChords','SimpleSoloInstrument','FastStridePianist','SimpleSoloInstrument','RandomSoloist']
setP = ['serbitat','black_metal','onvoorwaardelijk_fietsen','jazzy_blues','fietsen_intro','reincarnatie' ]

setIValue = maxValue % len(setI)
i = setI[setIValue]
print 'I value: ', i

if maximum == 'sadness':
    print 'sadness'
    b = random.randint(100,110)
    setPValue = happinessValue % 3             #happiness value
    p = setP[setPValue]
    print 'P Value: ',p
    fileName = 'python Improviser.py -i'+ i + ' -b'+ str(b) +' -p' +p + ' -r 3'

elif maximum == 'happiness':
    print 'happiness'
    b = random.randint(180,220)
    setPValue = (happinessValue % 3) +3
    p = setP[setPValue]
    print 'P Value: ',p
    fileName = 'python Improviser.py -i'+ i + ' -s -b'+ str(b) +' -p' +p

else :
    print 'neutral'
    # setPValue = ?????????????? should not be too happy
    b = random.randint(130,140)
    setPValue = (len(setP)-1)-(happinessValue % 4)
    p = setP[setPValue]
    print 'P Value: ',p

    fileName = 'python Improviser.py -i'+ i + ' -b'+ str(b) +' -p' +p


os.system(fileName)
