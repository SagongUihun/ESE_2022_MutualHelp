import Queue
import time
class Counter():
    def __init__(self):
        self.MAXSIZE = 600 
        self.countBuffer = Queue.Queue(self.MAXSIZE) # 10sec buffer  
        self.checkBuffer = [] # 1sec buffer
        self.kcBuffer = []
        self.pushupBuffer = []
        self.pole = []
        self.pole2 = [] 
        self.pole3 =[]
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.asd = 0
        self.up = 0
        self.down = 0
        self.timer = time.time()
        self.stopTimer = time.time()
        pass

    def shoulderPress(self, value):
        if(len(self.kcBuffer) > 70):
           self.kcBuffer.pop(0)
        self.kcBuffer.append(value)

        if(len(self.kcBuffer) > 69):
            self.pole.append(max(self.kcBuffer[10:60]))

            if(len(self.pole)>69):
        # Ideally, if the filter is applied well, there will be no problem
                if self.pole[50]+0.28 < self.pole[51] and self.pole[51] == self.pole[52]==self.pole[53]:# == self.pole[54]:#==self.pole[55]:
                    if(time.time() - self.timer > 1.5):
                        self.count3 = self.count3 + 1
                        self.timer = time.time()

                self.pole.pop(0)
                if(len(self.pole)>100):
                    self.pole.pop(0)
                time.sleep(0.01)

        return self.count3


    def KcCurl(self, value):
    # This is developed by ChangHyun Kim 
    # @Copyright is only his own :D 

        if(len(self.kcBuffer) > 70):
           self.kcBuffer.pop(0)
        self.kcBuffer.append(value)

    
        if(len(self.kcBuffer) > 69):
            self.pole2.append(max(self.kcBuffer[10:60]))
            
            
            if(len(self.pole2)>69):
        # Ideally, if the filter is applied well, there will be no problem
                if self.pole2[50]+70 < self.pole2[51] and self.pole2[51] == self.pole2[52]==self.pole2[53]:# == self.pole2[54]:#==self.pole2[55]:
                    # self.up = self.up + 1
                    # if self.up%3 == 1:
                    if(time.time() - self.timer > 1.5):
                        self.count1 = self.count1 + 1
                        self.timer = time.time()



                #print(self.count1, self.pole2[50], self.up, self.down)
                self.pole2.pop(0)
                time.sleep(0.01)

                #if nowmax == dmax and pole[i-13] == pole[i-12] == pole[i-11] == pole[i-10] == pole[i-9] == pole[i-8] == pole[i-7] == pole[i-6] == pole[i-5] == pole[i-4] == pole[i-3]:# == pole[i-2] == pole[i-1] == pole[i]:
                #    count = count+1
                    #print(i)
            
        #print(self.count1, self.pole[90])
        #self.asd = self.asd+1

        return self.count1


    def pushUp(self, value):
        

        if(len(self.pushupBuffer) > 70):
           self.pushupBuffer.pop(0)
        self.pushupBuffer.append(value)

    
        if(len(self.pushupBuffer) > 69):
            self.pole3.append(max(self.pushupBuffer[10:60]))
            
            
            if(len(self.pole3)>69):
            # Ideally, if the filter is applied well, there will be no problem
                if self.pole3[50]+12 < self.pole3[51] and self.pole3[51] == self.pole3[52]==self.pole3[53]: #== self.pole3[54]==self.pole3[55]:
                    # if self.up%3 == 1:
                    if(time.time() - self.timer > 1.5):
                        self.count3 = self.count3 + 1
                        self.timer = time.time()
            #     #print(high)
                
                #print(self.count1, self.pole2[50], self.up, self.down)
                self.pole3.pop(0)
                if(len(self.pole3)>100):
                    self.pole3.pop(0)
                time.sleep(0.01)

                #if nowmax == dmax and pole[i-13] == pole[i-12] == pole[i-11] == pole[i-10] == pole[i-9] == pole[i-8] == pole[i-7] == pole[i-6] == pole[i-5] == pole[i-4] == pole[i-3]:# == pole[i-2] == pole[i-1] == pole[i]:
                #    count = count+1
                    #print(i)
            
                # print(value,self.count3, self.pole2[50])
        #self.asd = self.asd+1

        return self.count3