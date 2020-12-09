#Created by Devon Smyth for ECE 1150 Term Report
#traffic simulation


import random
import matplotlib.pyplot as plt

standardQueue = [1,1,1,1,1,1,1,1,1,1]  #10 cars in standard line
longestQueue = [0, 0, 0]

class flow:
    # tracks interaction data
    def __init__(self):
        self.queue = [1,1,1,1,1,1,1,1,1,1]
        self.queue1 = [1,1,1,1,1,1,1,1,1,1]
        self.queue2 = [1,1,1,1,1,1,1,1,1,1]
        self.queue3 = [1,1,1,1,1,1,1,1,1,1]
        self.carsJoined = [0,0,0,0]
        self.totalWaitTime = [0,0,0,0]
        self.avgWaitTime = [0,0,0,0]

    #simulating 1 step(second) of simulation
    def step(self, chance, switch):

        #queue 0
            num = random.randint(1, chance[0])
            if num == chance[0]:
                self.queue.append(1)  #randomly joining queue
                self.carsJoined[0] += 1  #tally how many cars have been in queue
            longestQueue[qIndex] += len(self.queue)  #find average queue length
            longestQueue[2] += 1
            if(switch == 0):
                self.dequeue(0)
            self.totalWaitTime[0] += len(self.queue)  # add to total wait time

        #queue 1
            num = random.randint(1, chance[1])
            if num == chance[1]:
                self.queue1.append(1)  #randomly joining queue
                self.carsJoined[1] += 1  #tally how many cars have been in queue
            longestQueue[qIndex] += len(self.queue1)  #find max queue length
            longestQueue[2] += 1
            if(switch == 0):
                self.dequeue(1)
            self.totalWaitTime[1] += len(self.queue1)  # add to total wait time
        #queue 2
            num = random.randint(1, chance[2])
            if num == chance[2]:
                self.queue2.append(1)  #randomly joining queue
                self.carsJoined[2] += 1  #tally how many cars have been in queue
            longestQueue[qIndex] += len(self.queue2)  #find max queue length
            longestQueue[2] += 1
            if(switch == 1):
                self.dequeue(2)
            self.totalWaitTime[2] += len(self.queue2)  # add to total wait time

        #queue 3
            num = random.randint(1, chance[3])
            if num == chance[3]:
                self.queue3.append(1)  #randomly joining queue
                self.carsJoined[3] += 1  #tally how many cars have been in queue
            longestQueue[qIndex] += len(self.queue3)  #find max queue length
            longestQueue[2] += 1
            if(switch == 1):
                self.dequeue(3)
            self.totalWaitTime[3] += len(self.queue3)  # add to total wait time

    def dequeue(self,num):
        if num == 0:
            if len(self.queue) != 0:
                self.queue.pop(0)
                return
        if num == 1:
            if len(self.queue1) != 0:
                self.queue1.pop(0)
                return
        if num == 2:
            if len(self.queue2) != 0:
                self.queue2.pop(0)
                return
        if num == 3:
            if len(self.queue3) != 0:
                self.queue3.pop(0)
                return

    def getLength(self, num): #method to get length of queues
        if num == 0:
            return len(self.queue)
        if num == 1:
            return len(self.queue1)
        if num == 2:
            return len(self.queue2)
        if num == 3:
            return len(self.queue3)

    def getMaxQueue(self, num): #method to get length of queues
        return max(self.longestQueue)

    def getAvgWaitTime(self, num, initialQueue):   #method to get avgWaitTime
        self.avgWaitTime[num] = self.totalWaitTime[num]/(self.carsJoined[num]+initialQueue[num])
        return self.avgWaitTime[num]



class intersection:

    def __init__(self):
        self.flow = flow()
        self.switch = 0

    def simulate(self, chance):
        self.flow.step(chance, self.switch)


    def switchGreen(self):
        if self.switch == 0:
            self.switch = 1
        else:
            self.switch = 0

    def controlNorm(self, time, chance):
        count = 0
        for i in range(time):
            self.simulate(chance)
            if count == 25:  #set controls every 25 seconds, fixed intervals
                self.switchGreen()
                count = 0  #reset control switch timer
            count += 1

        print("Normal Average Wait Times:")
        print('Flow0: ' + str(self.flow.getAvgWaitTime(0,[10,10,10,10])))
        print('Flow1: ' + str(self.flow.getAvgWaitTime(1,[10,10,10,10])))
        print('Flow2: ' + str(self.flow.getAvgWaitTime(2,[10,10,10,10])))
        print('Flow3: ' + str(self.flow.getAvgWaitTime(3,[10,10,10,10])))
        return (self.flow.getAvgWaitTime(0, [10, 10, 10, 10]) + self.flow.getAvgWaitTime(1, [10, 10, 10,10]) + self.flow.getAvgWaitTime(2, [10, 10, 10, 10]) + self.flow.getAvgWaitTime(3, [10, 10, 10, 10])) / 4


    def controlOptimized(self, time, chance):
        count = 0
        priority = 0
        max = 0
        for i in range(time):

            if count == 0:  #only recalculate once dealing with previous priority
                max = 0
                for j in range(3): #find priority
                     if max < (self.flow.getLength(j)):
                        max = self.flow.getLength(j)
                        priority = j

            if (priority == 0) or (priority == 1): #decide which flow to let through
                self.switch = 0;
            else:
                self.switch = 1;

            if count < max:
                count += 1
            else:
                if count < 15:
                    count += 1
                else:
                    count = 0

            self.simulate(chance)

        print("\nOptimized Average Wait Times:")
        print('Flow0: ' + str(self.flow.getAvgWaitTime(0,[10,10,10,10])))
        print('Flow1: ' + str(self.flow.getAvgWaitTime(1,[10,10,10,10])))
        print('Flow2: ' + str(self.flow.getAvgWaitTime(2,[10,10,10,10])))
        print('Flow3: ' + str(self.flow.getAvgWaitTime(3,[10,10,10,10])))

        return (self.flow.getAvgWaitTime(0,[10,10,10,10])+self.flow.getAvgWaitTime(1,[10,10,10,10])+self.flow.getAvgWaitTime(2,[10,10,10,10])+self.flow.getAvgWaitTime(3,[10,10,10,10]))/4



def main():
    normAvg = [0,0,0,0,0,0,0,0,0,0]
    nmean = 0
    optAvg = [0,0,0,0,0,0,0,0,0,0]
    optmean = 0
    for i in range(10):     #run 10 1-hour simulations
        global qIndex

        intersectionSim = intersection()
        qIndex = 0
        normAvg[i] = intersectionSim.controlNorm(3600,[2,3,4,3])      #***Switch from Light vs Rush hour:  [2,3,4,3] vs [2,2,2,3]******
        longestQueue[0] = longestQueue[0]/longestQueue[2]


        intersectionSim1 = intersection()
        longestQueue[2] = 0
        qIndex = 1
        optAvg[i] = intersectionSim1.controlOptimized(3600, [2,3,4,23])
        longestQueue[1] = longestQueue[1] / (longestQueue[2])

    for i in normAvg:   #find average wait times across normal, and across optimized sims
        nmean += i
    for j in optAvg:
        optmean += j
    nmean = round(nmean / 10,2)
    optmean = round(optmean / 10,2)

    print('\n\n\nNormal Avg = ' + str(nmean))
    print('Optimized Avg = ' + str(optmean))


    x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    x2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.scatter(x1,normAvg,label=('Normal Control, Avg: '+str(nmean)+'s'), color="gray", marker="o", s=30)
    plt.scatter(x2,optAvg,label=('Optimized Control, Avg: '+str(optmean)+'s'), color="springgreen", marker="o", s=30)
    plt.xlabel('Sim #')
    plt.ylabel('Average Wait Time (s)')
    plt.title('Comparison of Control Styles (Light Traffic)')
    plt.legend()
    plt.show()
    

if __name__ == '__main__':
    main()
