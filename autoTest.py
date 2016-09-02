import random
import shlex
import subprocess
import sys
import re
import json

def genSlaves(numGroup, numSlaveRange = [2, 16, 1], numTaskRange = [4, 16, 1], tymRange = [4, 1000, 4]):
    slaves = []
    slvPref = "slv"
    for slaveId in xrange(numGroup):
        tsks = []
        slvNm = slvPref + str(slaveId+1)
        cnt = random.randrange(*numSlaveRange)
        for tskId in xrange(random.randrange(*numTaskRange)):
            tym = random.randrange(*tymRange)
            tmp = [slvNm+"tsk"+str(tskId+1), tym]
            tsks += [tmp]
        k = [slvNm, cnt, tsks]
        slaves += [k]
    return slaves

def saveSlaves(slaveInfo, slaveFile):

    lines = []
    for slv in slaveInfo:
        line = " ".join(str(x) for x in slv[:2])
        # print slv[2]
        line += " " + " ".join(" ".join([str(x) for x in y]) for y in slv[2])
        lines += [line]
    fp = open(slaveFile, "w")
    fp.write("\n".join(lines))
    fp.close()

def genJobs(numJobs, slaves, numTaskRange = [4, 16, 1]):
    jobs = []
    for jobid in xrange(numJobs):
        jobName = "job"+str(jobid+1)
        tsks = []
        for x in xrange(random.randrange(*numTaskRange)):
            tskGrpId = random.randrange(0, len(slaves), 1)
            tskId = random.randrange(0, len(slaves[tskGrpId][2]), 1)
            tskName = slaves[tskGrpId][0] + ":" + slaves[tskGrpId][2][tskId][0]
            tsks += [tskName]
        jobs += [[jobName]+tsks]
    return jobs

def saveJobs(jobInfo, jobFile):
    lines = []
    for x in jobInfo:
        line = str(x[0]) + " "
        line += " ".join(x[1:])
        lines += [line]

    fp = open(jobFile, "w")
    fp.write("\n".join(lines))
    fp.close()

def executeTheProc(masterExe, slaveInfoFile, jobInfoFIle, N, op):
    arguments = masterExe \
            + " " + slaveInfoFile \
            + " " + jobInfoFIle \
            + " " + str(N) \
            + " 2>/dev/null > " + op
    print arguments
    # return
    cmd = shlex.split(arguments)
    subprocess.call(arguments, shell=True)
    # proc = subprocess.Popen(cmd, stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # out, err = proc.communicate()
    fp = open(op)
    out = fp.read()
    fp.close()

    return out

def parseOutput(slvInf, jobInf, output):
    slvNames = set([x[0] for x in slvInf])
    jobNames = set([x[0] for x in jobInf])
    slvPIDs  = set()

    output = output.strip()

    opts = [re.split(" +", x) for x in re.split("\n+", output)]

    initilization = []
    finalization  = []
    status        = []

    lineNum = 1
    for line in opts:
        if len(line) == 2 and line[0] in slvNames and line[1].isdigit():
            initilization += [[lineNum, line]]
            slvPIDs |= set([line[1]])
        elif len(line) >= 3 and line[0] in slvPIDs and line[2] in slvNames:
            finalization += [[lineNum, line]]
        elif len(line) == 5 and line[0] in jobNames and line[2] in slvPIDs:
            status += [[lineNum, line]]
        else:
            print "Something wrong"
        lineNum += 1
    return [initilization, finalization, status]

def testSequencialExecution(slaveInfo, jobInf, N, output):
    if len(jobInf) < N: #otherwise it will be difficult to test
        return True
    jobs = {}
    for i in xrange(N):
        jbName = jobInf[i][0]
        jbCount = len(jobInf[i])
        jobs[jbName] = [i, 1, jbCount]

    # for i in xrange
    # lineNum = 1
    testResult = True
    for stat in output[2]: #output[2] is status output
        job = jobs[stat[1][0]]
        nextTsk = jobInf[job[0]][job[1]]
        if stat[1][1] != nextTsk:
            print "task not matching: expected '%s', got '%s' @line: %d"%(nextTsk, stat[1][1], stat[0])

        job[1] += 1

        if job[1] == job[2] and stat[1][4] != "finished": #expectin status finishes
            print "expecting 'finished' but got '%s' @line: %d" %(stat[1][4], stat[0])
            testResult = False
        if job[1] != job[2] and stat[1][4] != "waiting":
            print "expecting 'waiting' but got '%s' @line: %d"%(stat[1][4], stat[0])
            testResult = False
    return testResult
        # lineNum += 1 

def testProperSlaveExecution(slaveInfo, jobInf, N, output):
    if len(jobInf) < N: #otherwise it will be difficult to test
        return True
    testResult = True
    pidBucket = {}
    for stat in output[0]:
        bucket = pidBucket.setdefault(stat[1][0], set())
        bucket |= set([stat[1][1]])

    for stat in output[2]: #output[2] is status output
        task = stat[1][1]
        tasks = task.split(":")
        pot = pidBucket.get(tasks[0], [])
        pid = stat[1][2]
        if pid not in pot:
            print "error in slave matching, '%s' is not in group '%s'" %(pid, str(pot))
            testResult = False
    return testResult

def testTotalCount(slaveInfo, jobInf, N, output):
    totTskCnt = 0 #number task need to be performed.
    for i in xrange(N):
        l = i % len(jobInf)
        totTskCnt += len(jobInf[l]) - 1
    totSlv = 0
    for slv in slaveInfo:
        totSlv += slv[1]
    testResult = True
    if len(output[2]) != totTskCnt:
    #     print "Task count is matching: %d/%d"%(totTskCnt, len(output[2]))
    # else:
        print "Task count is not matching %d/%d"%(totTskCnt, len(output[2]))
        testResult = False

    if len(output[0]) != totSlv or len(output[1]) != totSlv:
    #     print "Slave count is matching: total slave: %d, started: %d, finishes: %d"%(totSlv, len(output[1]), len(output[0]))
    # else:
        print "Slave count is not matching: total slave: %d, started: %d, finishes: %d"%(totSlv, len(output[1]), len(output[0])) 
        testResult = False
    return testResult

def test(testId, exe = "/tmp/master", numSlave = 12, numJobs = 10, N = 10, numSlaveRange = [2, 16, 1], numTaskRange = [4, 16, 1], tymRange = [4, 50, 4]):

    slaveInfoFile = "test-" + str(testId) + "-slave.info"
    jobInfoFIle = "test-" + str(testId) + "-job.info"
    outputFIle = "test-" + str(testId) + "-output"
    # N = random.randrange(10, 20, 1)

    slvInf = genSlaves(numSlave, numSlaveRange = [2, 16, 1], numTaskRange = [4, 16, 1], tymRange = [4, 1000, 4])
    saveSlaves(slvInf, slaveInfoFile)
    jobInf = genJobs(numJobs, slvInf, numTaskRange)
    saveJobs(jobInf, jobInfoFIle)
    
    outputraw = executeTheProc(exe, slaveInfoFile, jobInfoFIle, N, outputFIle)
    
    output = parseOutput(slvInf, jobInf, outputraw)
    print "="*23
    print "Test id:", testId
    print "="*23
    print "="*23
    print "testing slave count\t\t\t", 
    res = testTotalCount(slvInf, jobInf, N, output)
    ress = '\033[92m\033[1mPASSED\033[0m' if res else "\033[91m\033[1mFAILED\033[0m"
    print ress
    print "="*23
    print "testing sequencial execution\t\t", 
    res = testSequencialExecution(slvInf, jobInf, N, output)
    ress = '\033[92m\033[1mPASSED\033[0m' if res else "\033[91m\033[1mFAILED\033[0m"
    print ress
    print "="*23
    print "Testing if task done by appropriat salve group\t",
    res = testProperSlaveExecution(slvInf, jobInf, N, output)
    ress = '\033[92m\033[1mPASSED\033[0m' if res else "\033[91m\033[1mFAILED\033[0m"
    print ress
    print "="*23

    print ""
    # pass

testCases = [
#numSlave, numJobs, N, numSlaveRange, numTaskRange, tymRange
[2, 3, 2, [2, 3, 2], [2, 3, 2], [4, 50, 4] ],
[2, 3, 2, [2, 3, 2], [2, 3, 2], [500, 1000, 4] ],
[12, 10, 30, [2, 16, 1], [4, 16, 2], [4, 50, 4] ],
[24, 20, 19, [2, 16, 1], [4, 16, 1], [4, 50, 4] ],
[12, 10, 10, [2, 16, 1], [4, 16, 1], [4, 500, 4] ]
]
tid = 1
for tc in testCases:
    test(tid, sys.argv[1], *tc)
    tid += 1