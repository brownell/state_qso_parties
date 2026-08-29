
import os, math
from datetime import datetime
#-----------------------------------------------------------------------------------------------------
#  now do the scoring by reading each "prepared" log file from the PreparedLogs directory
#  dupes are removed by constructing a dupeline from each QSO line and
#  collecting the unique dupelines in a dupeList list
#  dupeLine = rcvdCall[0] + "_" + band + "_" + mode + "_" + sentCall + "_" + sentQth + "_" + rcvdQth
#  any two lines that have the same dupeLine will be dupes and only one of the two will be kept in dupeList
#------------------------------------------------------------------------------------------------------
def score_qsos(s):

    for result in s.results:
        cab = result['cab']
        if not getattr(cab, 'valid',  False):
            continue   

        dupeList = []
        removedDupesList = []
        multList = []

        CWQs = 0
        PHQs = 0
        DGQs = 0
        QsoPts = 0
        Mults = 0
        ScoreWOBonus = 0
        MobileTrackingBonus = 0
        CountyActivationBonus = 0
        TotalBonus = 0
        TotalScore = 0        
        CWQs = 0
        PHQs = 0
        DGQs = 0
        ctysSent = []
        uniqueCtysSent = []
        ctysRcvd = []
        uniqueCallsRcvd = []

        for qso in result.qso:
            if not qso.valid:
                continue
            dupeLine = qso.dx_call.upper().split("/") + "_" + qso.category_band + "_" + qso.category_mode.upper() + "_" + qso.de_call.upper() + "_" + qso.de_exch[1] + "_" + qso.dx_exch[1]
            if dupeLine in dupeList:
                qso.valid = False
                s.stats['duplicate_qsos'] += 1
            else: 
                dupeList.append(dupeLine)

            if cab.category_mode == "CW":
               CWQs += 1
            elif cab.category_mode == "PH":
               PHQs += 1
            if cab.category_mode in ["DG", "RY"]:
                DGQs += 1
            if qso.dx_exch not in multList:
               multList.append(qso.dx_exch)
            if(qso.de_exch in s.counties):
                ctysSent.append(qso.de_exch)
                if(qso.de_exch not in uniqueCtysSent):
                    uniqueCtysSent.append(qso.de_exch)
            if(qso.dx_exch in s.mobile_callsigns):
                ctysRcvd.append(qso.de_call + "_" + qso.dx_exch) #the current station logged a QSO with mobile(qso.dx_exch) in cty qso.dx_exch
                if(qso.dx_exch not in uniqueCallsRcvd):
                    uniqueCallsRcvd.append(qso.dx_exch)  #uniqueCallsRcvd is a list of callsigns of mobiles worked 
            
        CountyActivationBonus = 0
        for ctys in uniqueCtysSent:
            numQ = ctysSent.count(ctys)
            if numQ >= 5:
                CountyActivationBonus = CountyActivationBonus + 1000
                print("CountyActivation for, " + qso.de_call + "," + ctys)
                
        if(len(uniqueCtysSent) <= 2):
            CountyActivationBonus = 0

        MobileTrackingBonus = 0
        for item in uniqueCallsRcvd:
                numCtysWorkedThisMobile = 0
                for aCallQth in ctysRcvd:
                    aMobCallSplit = aCallQth.split("_")
                    aMobCall = aMobCallSplit[0]
                    if item == aMobCall:
                        numCtysWorkedThisMobile += 1
                numCtysWorkedMobile = numCtysWorkedMobile + math.floor(numCtysWorkedThisMobile/5)
        MobileTrackingBonus = 500*numCtysWorkedMobile
        

        QsoPts = 3*CWQs + 2*PHQs + 3*DGQs
        Mults = len(multList)
        ScoreWOBonus = QsoPts*Mults

        TotalBonus = MobileTrackingBonus + CountyActivationBonus

        TotalScore = ScoreWOBonus + TotalBonus

        ScoreReduction = int(cab.claimed_score) - TotalScore
        if(ScoreReduction < 0):
            ScoreReduction = 0

        print(f"{cab.callsign}, {cab.email}, {cab.category}")
        print(result['callsign'] + "," + result[caemail.lower() + "," + TQPCat + "," + Club + "," + Operators + "," + ClaimedScore + "," + str(CWQs) + "," + str(PHQs) + "," + str(DGQs) + "," + str(QsoPts) + "," + str(Mults) + "," + str(ScoreWOBonus) + "," + str(MobileTrackingBonus) + "," + str(CountyActivationBonus) + "," + str(TotalBonus) + "," + str(TotalScore) + "," + str(ScoreReduction))
        


