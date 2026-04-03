# Timer IS A METHOD WHICH RETURN REACHED TIME OF THR PASSENGER
# PARAMETERS : Btime -> BOOKING TIME OF THE PASSENGER
# Otime -> OVERAL TIME(Travel + Waited) TAKEN FOR THE PASSENGER TO REACH THE DESTINATION
def Timer(Btime, Otime):
    hr, mi = map(int, Btime.split(":"))
    TT = []
    if Otime >= 60 :
        hr += Otime//60
        mi += Otime%60
    else : mi += Otime%60
    if mi >= 60 :
        hr += mi//60
        mi = mi%60
    if hr >= 25 :
        hr -= 24
    TT.append(hr);TT.append(mi)
    return TT

# Tellwhat IS A METHOD WHICH RETURN SUM OF THE VALUES IN THE LIMIT(fr, to) IN THE LIST (L)
def Tellwhat(L, fr, to): 
    return sum(L[i] for i in range(min(fr,to)-1, max(fr,to)-1))

# TellWhich IS A METHOD WHICH SORT THE TAXI BASED ON NEAREST , REVENUE & BY LOWEST NUMBER THEN RETURN TAXI NUMBER
# PARAMETERS : AllT2Pd -> LIST OF DIS OF ALL THE TAXIS TO PASSENGER & ETMinDis -> MIN DIS OF ELIGIBLE TAXIS TO PASSENGER
# AllTRev -> LIST OF REVENUE DETAIL OF ALL THE TAXIS & ElgTRev -> LIST OF REVENUE DETAIL OF ELIGIBLE TAXIS
def TellWhich(AllT2Pd, ETMinDis, AllTRev, ElgTRev):
    NTL = []    # NEAREST TAXI LIST
    for i in range(len(AllT2Pd)):                            #> NEAREST
        if AllT2Pd[i] != "!Elg" and AllT2Pd[i] == ETMinDis:  #>         DISTANCE
            NTL.append(i+1)                                  #>                  BASED TAXI FILLTER

    if len(NTL) >= 2:                                        #> REVENUE BASED TAXI FILLTER
        for j in NTL:                                       
            ElgTRev.append(Taxi[j]["Rev"])                  
        NT = AllTRev.index(min(ElgTRev)) + 1
    else:
        NT = NTL[0] 
        
    return NT # NEAREST COMFORT TAXI NUMBER

                                              # MAIN METHOD #
         # INPUT RECEIVING UNIT #
print("Enter Num of Taxi and PickUp Points: ",end="")
NoT,TPp = map(int,input().split())                                   # Not -> NUMBER OF TAXI & TPp -> TOTAL PICKUP POINT
print("Enter P2P Distace: ",end="") 
P2Pd = list(map(int,input().split()))                                # P2Pd -> POINT TO POINT DISTANCE
print("Enter P2P Travel Time: ",end="")
P2Pt = list(map(int,input().split()))                                # P2Pt -> POINT TO POINT TRAVEL TMIE
print("Enter Min.Dis, Min.Cost, Extra Charge and Max.Radius: ",end="")
Mid, MiC, Ex, Mxr = map(int,input().split()) # Mid -> MIN DIS WITH NO EXTRACHARGE, MiC - > MIN COST         
print("Enter Num of Passenger: ",end="")     # Ex -> EXTRA CHARGE AFTER MIN DIS, Mxr -> MAX DIS TO PICKUP THE PASSENGER BY TAXIS
Tp = int(input())                            # Tp -> TOTAL NUMBER OF PASSENGER

print("\n\t*ENTER PASSENGER DETAIL*\n")
Pdetail = dict()
for i in range(1,Tp+1):   # INITIALCING PASSENGER DETAIL DICTIONARY #
    Pdetail[i] = {}
    Info = list(map(str,input().split()))
    # Name -> PASSENGER NAME, From -> BOARDING POINT, TO -> DESTINATION POINT, At -> BOOKING TIME
    Pdetail[i]["Name"], Pdetail[i]["From"], Pdetail[i]["To"], Pdetail[i]["At"] = Info[0], Info[1], Info[2], Info[3]
    
Taxi = dict()
for i in range(1,NoT+1):  # INITIALCING TAXI REGISTER DICTIONARY #
    Taxi[i] = {}
    # Sp -> TAXI STANDING POINT INITIALLY(1), Rev -> TAXI REVENUE INITIALLY(0), Elg -> TAXI ELIGIBITY VARIABLE INITIALLY(0)
    Taxi[i]["Sp"], Taxi[i]["Elg"], Taxi[i]["Rev"] = 1, 0, 0

         # OUTPUT PRODUCING UNIT #
print("\n *REVIEW FOR THE GIVEN COUSTEMER DETAILS*\n")

for i in range(1,Tp+1):   # BILL PROCESSING UNIT #
    PTDis = Tellwhat(P2Pd, int(Pdetail[i]["From"]), int(Pdetail[i]["To"]))         
    if PTDis > Mid: Pdetail[i]["TCost"] = (PTDis-Mid)*Ex + MiC # FORMULA TO CALCULATE TRAVEL COST  
    else: Pdetail[i]["TCost"] = MiC
    
for i in range(1,Tp+1):   # PASSENGER REQUIRMENT PROCESSING UNIT #       
    PBookHr, PBookMi = map(int, Pdetail[i]["At"].split(":"))
    AllT2Pd, AllTRev, TT, ElgT2Pd, ElgTRev, Wt, Tt = [], [], [], [], [], 0, 0
    # TT -> TOTAL TIME , Wt -> WAITED TIME , Tt -> TRAVEL TIME
    # ElgT2Pd -> LIST OF DIS OF ELIGIBLE TAXIS TO PASSENGER
    
    for j in range(1,NoT+1): # SORTING TAXI UNIT
        if Taxi[j]["Elg"] < PBookHr*100 + PBookMi:
          # PBookHr*100 + PBookMi IS BUFFER BASED ON THE PASSENGER BOOKING TIME
          # THIS BUFFER USED TO SEPARATING IN-DUTY & NON-DUTY TAXI FOR THAT PASSENGER BOOKING TIME 
          ForNow = Tellwhat(P2Pd, int(Taxi[j]["Sp"]), int(Pdetail[i]["From"])) # COLLECTING ELIGIBLE TAXI TO PASSENGER DIS
          ElgT2Pd.append(ForNow)         # THIS LIST ONLY STORE ONLY ELIGIBLE TAXI DIS TO PASSENGER
          AllT2Pd.append(ForNow)         # LIST STORE BOTH IN-NON-DUTY TAXI DIS TO PASSENGER
          AllTRev.append(Taxi[j]["Rev"]) # LIST STORE BOTH IN-NON-DUTY TAXI REVENUE
        else:
          AllT2Pd.append("!Elg")  #>  IN-DUTY TAXI ARE NOT ELIGIBLE FOR THIS INSTANT PASSENGER
          AllTRev.append("!Elg")  #>   BUT WE NEED IN-DUTY TAXI DIS & REVENUE FOR THE SORTING
          
        ElgT2Pd.append(sum(P2Pd)) # IF NO TAXI ELIGIBLE FOR THE PASSENGER DEFAULT DIS IN ADDED
    
    if min(ElgT2Pd) > Mxr:        # IF PASSENGER BOARDING POINT DIS IS GREATER THRN RADIUS THEN PASSENGER REJECTED
        print(Pdetail[i]["Name"],"REJECTED")
        continue
    else:                         
        NT = TellWhich(AllT2Pd, min(ElgT2Pd), AllTRev, ElgTRev)             # NEAREST TAXI SELECTION
        Wt = Tellwhat(P2Pt, int(Taxi[NT]["Sp"]), int(Pdetail[i]["From"]))   # WAITED TIME CALCULATOR
        Tt = Tellwhat(P2Pt, int(Pdetail[i]["From"]), int(Pdetail[i]["To"])) # TRAVEL TIME CALCULATOR
        TT = Timer(Pdetail[i]["At"], Tt + Wt)                               # DESTINATION REACH TIME 
        Taxi[NT]["Sp"]  = Pdetail[i]["To"]     # CHANGING TAXI'S 'SP'  >> REACHED PASSENGER 'TO' POINT 
        Taxi[NT]["Elg"] = TT[0]*100 + TT[1]    # CHANGING TAXI'S 'Elg' >> REACHED PASSENGER 'REACED TIME(TT)'
        Taxi[NT]["Rev"] += Pdetail[i]["TCost"] # REGISTER TAXI'S 'Rev' AS TRAVEL COST OF THE PASSENGER (INCEREMENT EVERY TIME)
        if TT[0] >= 24: TT[0]-=24              # FORMATING TIME AS 24-FORMAT
        print(Pdetail[i]["Name"],f"Taxi-{NT}",Pdetail[i]["TCost"],"%02d:%02d"%(TT[0],TT[1])) # FINALLY PRINTING THE NEEDED DETAILS
# END OF THE CODE

# THIS CODE WAS WRITTEN BY KANISHKUMAR S 2nd-YEAR EEE AT SAIRAM COLLEGE(CHENNAI)
# IT'S A MINI PROJECT GIVEN IN SKILLRACK AT LEVEL 6 DIVISION

        
