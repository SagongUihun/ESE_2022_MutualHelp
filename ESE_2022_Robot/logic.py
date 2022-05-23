import Queue

class Counter:
    def __init__(self):
        self.MAXSIZE = 600 
        self.upperBound = 1.05
        self.lowerBound = 0.90
        self.countBuffer = Queue.Queue(self.MAXSIZE) # 10sec buffer  
        self.checkBuffer = [] # 1sec buffer
        self.count = 0
        pass

    def counterAlgorithm(self, value):
        # if(self.countBuffer.qsize() > self.MAXSIZE):
        #     self.countBuffer.get()
        if(len(self.checkBuffer) > 20):
            self.checkBuffer.pop(0)


        # self.countBuffer.put(value)

        if (value > self.upperBound):
            # before value check ( 1 1 X) (-1 1 O)
            if (len(self.checkBuffer) == 0 or self.checkBuffer[-1] ==  -1):
                self.checkBuffer.append(1) 
        elif(value < self.lowerBound):
            # before value check ( -1 -1 X) (1 -1 O)
            if(len(self.checkBuffer) == 0 or self.checkBuffer[-1] == 1):
                self.checkBuffer.append(-1)



        #check numerical alogrithm ([-1 1 -1] , counter ++ )-> [-1]
        if len(self.checkBuffer) > 2 :
            for i in range(len(self.checkBuffer)-2):
                if(self.checkBuffer[i] == -1 and self.checkBuffer[i+1] == 1 and self.checkBuffer[i+2] == -1 ):
                    self.count += 1
                    self.checkBuffer.pop(i)
                    self.checkBuffer.pop(i)
        print(value,self.checkBuffer[-1])
        print(self.checkBuffer,self.count)