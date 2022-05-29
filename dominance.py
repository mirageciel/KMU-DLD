import copy

def toBinary(nums): #이진수 변환
    binary = []
    global length
    length = nums[0]
    
    for i in nums[2:]:
        if i not in binary:
            num = bin(i)[2:]
            binary.append(num)
    
    for i in range(len(binary)):
        binary[i] = binary[i].zfill(length)
    
    return binary

def numOf1s(nums): #1의 개수 세기
    num_of_1s = {}
    
    for i in nums:
        if i.count("1") in num_of_1s.keys():
            num_of_1s[i.count("1")].append(i)
        else:
            num_of_1s[i.count("1")] = [i]
            
    index = sorted(num_of_1s.keys())
    sorted_num_of_1s = {}
    for i in index:
        sorted_num_of_1s[i] = num_of_1s[i]
    
    return sorted_num_of_1s

def find_implicant(minterm): #각 자리의 숫자 비교
    implicant = minterm
    table = numOf1s(minterm)
    start = next(iter(table)) #table의 가장 첫 번째 키, 비교의 기준점
    combined = 0 #combine에 하나 이상 check되었을 때
    
    for i in range(len(table.keys())-1):
        for j in table[start]:
            if start+1 not in table.keys():
                start += 1
                break
            for k in table[start+1]:
                change = ""
                                
                for l in range(length):
                    if j[l] != k[l] and (j[l]=="-" or k[l]=="-"):
                        change = ""
                        break
                    elif j[l] != k[l]:
                        change += "-"
                    else:
                        change += j[l]
                    
                if change.count("-") == table[start][0].count("-") + 1:
                    if change not in implicant:
                        implicant.append(change)
                    if j in implicant: implicant.remove(j)
                    if k in implicant: implicant.remove(k)
                    combined = 1
                
        start += 1
        
    return implicant, combined

def checked_times_num(answer): #EPI 찾기 (각 minterm들의 cover 횟수 세기)
    num_check = {}
    maxNum = 2 ** length
    EPI = []
    for i in range(maxNum):
        num_check[bin(i)[2:].zfill(length)] = 0

    for i in answer: #각 숫자들의 cover 횟수
        for j in num_check.keys():
            for k in range(length):
                if not (i[k] == j[k] or i[k] == "-"):
                    break
                if k == length-1:
                    num_check[j] += 1
        
    for i in answer:
        for key, value in num_check.items():
            if value == 1:
                for k in range(length):
                    if key[k] == i[k] or i[k] == "-":
                        if k==length-1 and i not in EPI: 
                            EPI.append(i)
                    else:
                        break

    return EPI

def NEPI_covering(PI, EPI, minterm):  
    NEPI_bin = PI;
    for epi in EPI:
        NEPI_bin.remove(epi)
    
    NEPI_cover_row = {} #key: nepi
    for nepi in NEPI_bin:
        NEPI_cover_row[nepi] = []
        
    EPI_cover = []
        
    NEPI_cover_col = {} #key: minterm
    for mt in minterm:
        NEPI_cover_col[mt] = []
    
    for i in EPI:
        for j in minterm:
            for k in range(length):
                if not (i[k] == j[k] or i[k] == "-"):
                    break
                if k == length-1:
                    EPI_cover.append(j)

    for i in NEPI_bin:
        for j in minterm:
            if j in EPI_cover:
                continue
            else:
                for k in range(length):
                    if not (i[k] == j[k] or i[k] == "-"):
                        break
                    if k == length-1:
                        NEPI_cover_row[i].append(j)
                        NEPI_cover_col[j].append(i)
    
    key = list(NEPI_cover_col.keys())              
    for i in key:
        if NEPI_cover_col[i] == []:
            del(NEPI_cover_col[i])
    
    return NEPI_cover_row, NEPI_cover_col

def row_dominance(covered):
    NEPI = list(covered.keys())
    minterm = list(covered.values())
    
    NEPI_choosed = copy.deepcopy(NEPI)
    minterm_choosed = copy.deepcopy(minterm)
        
    for i in range(len(minterm)):
        for j in range(i, len(minterm)):
            if i != j:
                if check_dominance(minterm[i], minterm[j])[1] == 3:
                    print("PI", NEPI[i], "and PI", NEPI[j], "row-dominantes each other")
                    if NEPI[j] in NEPI_choosed: NEPI_choosed.remove(NEPI[j])
                    if minterm[j] in minterm_choosed: minterm_choosed.remove(minterm[j])
                    
                elif check_dominance(minterm[i], minterm[j])[0] == True:
                    if check_dominance(minterm[i], minterm[j])[1] == 2:
                        print("PI", NEPI[i], "row-dominates PI", NEPI[j])
                        if NEPI[j] in NEPI_choosed: NEPI_choosed.remove(NEPI[j])
                        if minterm[j] in minterm_choosed: minterm_choosed.remove(minterm[j])
                    elif check_dominance(minterm[i], minterm[j])[1] == 1:
                        print("PI", NEPI[j], "row-dominates PI", NEPI[i])
                        if NEPI[i] in NEPI_choosed: NEPI_choosed.remove(NEPI[i])
                        if minterm[i] in minterm_choosed: minterm_choosed.remove(minterm[i])
                        
                elif check_dominance(minterm[i], minterm[j])[0] == False:
                    if check_dominance(minterm[i], minterm[j])[1] == 2:
                        print("PI", NEPI[j], "row-dominates PI", NEPI[i])
                        if NEPI[i] in NEPI_choosed: NEPI_choosed.remove(NEPI[i])
                        if minterm[i] in minterm_choosed: minterm_choosed.remove(minterm[i])
                    elif check_dominance(minterm[i], minterm[j])[1] == 1:
                        print("PI", NEPI[i], "row-dominates PI", NEPI[j])
                        if NEPI[j] in NEPI_choosed: NEPI_choosed.remove(NEPI[j])
                        if minterm[j] in minterm_choosed: minterm_choosed.remove(minterm[j])
                    
    return NEPI_choosed, minterm_choosed
            
def col_dominance(covered):
    NEPI = list(covered.values())
    minterm = list(covered.keys())
    
    NEPI_choosed = copy.deepcopy(NEPI)
    minterm_choosed = copy.deepcopy(minterm)
    
    for i in range(len(minterm)):
        for j in range(i, len(minterm)):
            if i != j:
                if check_dominance(NEPI[i], NEPI[j])[1] == 3:
                    print("minterm", minterm[i], "and minterm", minterm[j], "col-dominantes each other")
                    if NEPI[j] in NEPI_choosed: NEPI_choosed.remove(NEPI[j])
                    if minterm[j] in minterm_choosed: minterm_choosed.remove(minterm[j])
                    
                elif check_dominance(NEPI[i], NEPI[j])[0] == True:
                    if check_dominance(NEPI[i], NEPI[j])[1] == 2:
                        print("minterm", minterm[j], "col-dominates minterm", minterm[i])
                        if NEPI[i] in NEPI_choosed: NEPI_choosed.remove(NEPI[i])
                        if minterm[i] in minterm_choosed: minterm_choosed.remove(minterm[i])
                    elif check_dominance(NEPI[i], NEPI[j])[1] == 1:
                        print("minterm", minterm[i], "col-dominates minterm", minterm[j])
                        if NEPI[j] in NEPI_choosed: NEPI_choosed.remove(NEPI[j])
                        if minterm[j] in minterm_choosed: minterm_choosed.remove(minterm[j])
                        
                elif check_dominance(NEPI[i], NEPI[j])[0] == False:
                    if check_dominance(NEPI[i], NEPI[j])[1] == 2:
                        print("minterm", minterm[i], "col-dominates minterm", minterm[j])
                        if NEPI[j] in NEPI_choosed: NEPI_choosed.remove(NEPI[j])
                        if minterm[j] in minterm_choosed: minterm_choosed.remove(minterm[j])
                    elif check_dominance(NEPI[i], NEPI[j])[1] == 1:
                        print("minterm", minterm[j], "col-dominates minterm", minterm[i])
                        if NEPI[i] in NEPI_choosed: NEPI_choosed.remove(NEPI[i])
                        if minterm[i] in minterm_choosed: minterm_choosed.remove(minterm[i])
                    
    return minterm_choosed, NEPI_choosed
                    
def check_dominance(a, b): #check dominance
    idx_a = 0; idx_b = 0; check = 0
    rt = -1
    change = False

    if len(a) >= len(b): #shorter to name a
        rem = a
        a = b
        b = rem
        change = True
                        
    if len(a) == 0:
        check += 1
    else:
        while idx_a < len(a):
            if "-" in a[idx_a]:
                a_toInt = a[idx_a].replace("-", "2")
                b_toInt = b[idx_b].replace("-", "2")
            else:
                a_toInt = a[idx_a]
                b_toInt = b[idx_b]
                
            if int(a_toInt) > int(b_toInt):
                idx_b += 1
                if idx_b >= len(b):
                    idx_a += 1;
                    idx_b = 0
            elif a_toInt != b_toInt:
                break
            else:
                idx_b += 1; check += 1
                if idx_b >= len(b):
                    idx_a += 1;
                    idx_b = 0
    
    if check > 0:                
        if len(a) == len(b):
            rt = 3
        elif len(a) < len(b):
            rt = 2
        elif len(a) > len(b):
            rt = 1
    else:
        rt = -1
        
    return change, rt
    
#main
def solution(minterm):
    
    PI, combined = find_implicant(toBinary(minterm))
    
    while combined:
        PI, combined = find_implicant(PI)
    
    sorted_PI = []
    
    for i in PI:
        sorted_PI.append(i.replace('-', '2'))
    PI = []
    for i in sorted(sorted_PI):
        PI.append(i.replace('2', '-'))
    
    EPI = checked_times_num(PI)
    by_row, by_col = NEPI_covering(PI, EPI, toBinary(minterm))
    
    row_domi = row_dominance(by_row)
    col_domi = col_dominance(by_col)
    
    print(row_domi)
    print(col_domi)
    
    return "Finish"

#print(row_dominance({'101-': ['1010', '1011'], '10-0': ['1010'], '110-': [], '11-1': [], '1-11': ['1011']}))
#print(col_dominance({'1010': ['101-', '10-0', '1-11'], '1011': ['101-', '1-11']}))