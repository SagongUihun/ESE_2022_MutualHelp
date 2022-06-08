if self.stackedWidget.currentWidget() == self.page_2:
    # L_x = np.array([np.cos(hp),0 ,-np.sin(hp)])
    # L_y = np.array([np.sin(hp)*np.sin(hr),np.cos(hr),np.cos(hp)*np.sin(hr)])
    # L_z = np.array([np.sin(hp)*np.cos(hr),-np.sin(hr),np.cos(hp)*np.cos(hr)])

    # R_x = np.array([np.cos(rhp),0 ,-np.sin(rhp)])
    # R_y = np.array([np.sin(rhp)*np.sin(rhr),np.cos(rhr),np.cos(rhp)*np.sin(rhr)])
    # R_z = np.array([np.sin(rhp)*np.cos(rhr),-np.sin(rhr),np.cos(rhp)*np.cos(rhr)])
    x1_L = np.cos(60*np.pi/180)
    y1_L = np.sin(60*np.pi/180)
    x2_L = np.cos(20*np.pi/180)
    y2_L = np.sin(20*np.pi/180)
    x3_L = np.cos(0*np.pi/180)
    y3_L = np.sin(0*np.pi/180)
    x4_L = np.cos(-20*np.pi/180)
    y4_L = np.sin(-20*np.pi/180)
    x5_L = np.cos(-40*np.pi/180)
    y5_L = np.sin(-40*np.pi/180)
    L_1 = np.array([x1_L*np.cos(rhp) + y1_L*np.sin(rhp)*np.sin(rhr) , y1_L*np.cos(rhr) , -x1_L*sin(rhp) + y1_L*cos(rhp)*sin(rhr)])
    L_2 = np.array([x2_L*np.cos(rhp) + y2_L*np.sin(rhp)*np.sin(rhr) , y2_L*np.cos(rhr) , -x2_L*sin(rhp) + y2_L*cos(rhp)*sin(rhr)])
    L_3 = np.array([x3_L*np.cos(rhp) + y3_L*np.sin(rhp)*np.sin(rhr) , y3_L*np.cos(rhr) , -x3_L*sin(rhp) + y3_L*cos(rhp)*sin(rhr)])
    L_4 = np.array([x4_L*np.cos(rhp) + y4_L*np.sin(rhp)*np.sin(rhr) , y4_L*np.cos(rhr) , -x4_L*sin(rhp) + y4_L*cos(rhp)*sin(rhr)])
    L_5 = np.array([x5_L*np.cos(rhp) + y5_L*np.sin(rhp)*np.sin(rhr) , y5_L*np.cos(rhr) , -x5_L*sin(rhp) + y5_L*cos(rhp)*sin(rhr)])

    x1_R = np.cos(-40*np.pi/180)
    y1_R = np.sin(-40*np.pi/180)
    x2_R = np.cos(-20*np.pi/180)
    y2_R = np.sin(-20*np.pi/180)
    x3_R = np.cos(0*np.pi/180)
    y3_R = np.sin(0*np.pi/180)
    x4_R = np.cos(20*np.pi/180)
    y4_R = np.sin(20*np.pi/180)
    x5_R = np.cos(60*np.pi/180)
    y5_R = np.sin(60*np.pi/180)
    R_1 = np.array([x1_R*np.cos(rhp) + y1_R*np.sin(rhp)*np.sin(rhr) , y1_R*np.cos(rhr) , -x1_R*sin(rhp) + y1_R*cos(rhp)*sin(rhr)])
    R_2 = np.array([x2_R*np.cos(rhp) + y2_R*np.sin(rhp)*np.sin(rhr) , y2_R*np.cos(rhr) , -x2_R*sin(rhp) + y2_R*cos(rhp)*sin(rhr)])
    R_3 = np.array([x3_R*np.cos(rhp) + y3_R*np.sin(rhp)*np.sin(rhr) , y3_R*np.cos(rhr) , -x3_R*sin(rhp) + y3_R*cos(rhp)*sin(rhr)])
    R_4 = np.array([x4_R*np.cos(rhp) + y4_R*np.sin(rhp)*np.sin(rhr) , y4_R*np.cos(rhr) , -x4_R*sin(rhp) + y4_R*cos(rhp)*sin(rhr)])
    R_5 = np.array([x5_R*np.cos(rhp) + y5_R*np.sin(rhp)*np.sin(rhr) , y5_R*np.cos(rhr) , -x5_R*sin(rhp) + y5_R*cos(rhp)*sin(rhr)])
    v = np.array([5, 6, 2])
    
    
    if(self.triger):
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.triger = False
    if(self.triger_r):
        self.axr = self.fig_r.add_subplot(111, projection='3d')
        self.triger_r = False        
    #print( hand_p, hand_r, hand_y, hr, hp)
    start = [0,0,0]

    #self.axr.quiver(start[0],start[1],start[2],R_x[0],R_x[1],R_x[2],color='red')
    #self.axr.quiver(start[0],start[1],start[2],R_y[0],R_y[1],R_y[2],color='orange')
    #self.axr.quiver(start[0],start[1],start[2],R_z[0],R_z[1],R_z[2],color='magenta')
    #self.axr.quiver(start[0],start[1],-1,0,0,1,color = 'black')
    
    self.axr.quiver(start[0],start[1],start[2],R_1[0],R_1[1],R_1[2],color='red')
    self.axr.quiver(start[0],start[1],start[2],R_2[0],R_2[1],R_2[2],color='orange')
    self.axr.quiver(start[0],start[1],start[2],R_3[0],R_3[1],R_3[2],color='yellow')
    self.axr.quiver(start[0],start[1],start[2],R_4[0],R_4[1],R_4[2],color='green')
    self.axr.quiver(start[0],start[1],start[2],R_5[0],R_5[1],R_5[2],color='blue')
    self.axr.quiver(start[0],start[1],-1,0,0,1,color = 'black')
    
    self.axr.set_xlim([-1,1])
    self.axr.set_ylim([-1,1])
    self.axr.set_zlim([-1,1])
    self.canvas_r.draw()
    self.axr.axes.clear()
    
    #self.ax.quiver(start[0],start[1],start[2],L_x[0],L_x[1],L_x[2],color='red')
    #self.ax.quiver(start[0],start[1],start[2],L_y[0],L_y[1],L_y[2],color='orange')
    #self.ax.quiver(start[0],start[1],start[2],L_z[0],L_z[1],L_z[2],color='magenta')
    #self.ax.quiver(start[0],start[1],-1,0,0,1,color = 'black')

    self.axr.quiver(start[0],start[1],start[2],L_1[0],L_1[1],L_1[2],color='red')
    self.axr.quiver(start[0],start[1],start[2],L_2[0],L_2[1],L_2[2],color='orange')
    self.axr.quiver(start[0],start[1],start[2],L_3[0],L_3[1],L_3[2],color='yellow')
    self.axr.quiver(start[0],start[1],start[2],L_4[0],L_4[1],L_4[2],color='green')
    self.axr.quiver(start[0],start[1],start[2],L_5[0],L_5[1],L_5[2],color='blue')
    self.axr.quiver(start[0],start[1],-1,0,0,1,color = 'black')
    
    self.ax.set_xlim([-1,1])
    self.ax.set_ylim([-1,1])
    self.ax.set_zlim([-1,1])
    self.canvas.draw()
    self.ax.axes.clear()

    
    # print("update")