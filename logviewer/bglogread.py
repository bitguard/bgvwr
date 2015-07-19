#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
#  bglogread.py
#
#  Copyright 2014 bitGuard Tech
#
#  


import sys,struct,time, datetime

translate = {
  0x0021:'!', 0x0022:'"', 0x0023:'#', 0x0024:'$', 0x0025:'%', 0x0026:'&',
  0x0027:'\'', 0x0028:'(', 0x0029:')', 0x002a:'*', 0x002b:'+', 0x002c:',',
  0x002d:'-', 0x002e:'.', 0x002f:'/', 0x0030:'0', 0x0031:'1', 0x0032:'2',
  0x0033:'3', 0x0034:'4', 0x0035:'5', 0x0036:'6', 0x0037:'7', 0x0038:'8',
  0x0039:'9', 0x003a:':', 0x003b:';', 0x003c:'<', 0x003d:'=', 0x003e:'>',
  0x003f:'?', 0x0040:'@', 0x0041:'A', 0x0042:'B', 0x0043:'C', 0x0044:'D',
  0x0045:'E', 0x0046:'F', 0x0047:'G', 0x0048:'H', 0x0049:'I', 0x004a:'J',
  0x004b:'K', 0x004c:'L', 0x004d:'M', 0x004e:'N', 0x004f:'O', 0x0050:'P',
  0x0051:'Q', 0x0052:'R', 0x0053:'S', 0x0054:'T', 0x0055:'U', 0x0056:'V',
  0x0057:'W', 0x0058:'X', 0x0059:'Y', 0x005a:'Z', 0x005b:'[', 0x005c:'\\',
  0x005d:']', 0x005e:'^', 0x005f:'_', 0x0060:'`', 0x0061:'a', 0x0062:'b',
  0x0063:'c', 0x0064:'d', 0x0065:'e', 0x0066:'f', 0x0067:'g', 0x0068:'h',
  0x0069:'i', 0x006a:'j', 0x006b:'k', 0x006c:'l', 0x006d:'m', 0x006e:'n',
  0x006f:'o', 0x0070:'p', 0x0071:'q', 0x0072:'r', 0x0073:'s', 0x0074:'t',
  0x0075:'u', 0x0076:'v', 0x0077:'w', 0x0078:'x', 0x0079:'y', 0x007a:'z',
  0x007b:'{', 0x007c:'|', 0x007d:'}', 0x007e:'~', 0xff08:'<backspace>',
  0xff09:'<tab>', 0xff0a:'<linefeed>', 0xff0b:'<clear>', 0xff0d:'<return>',
  0xff13:'<pause>', 0xff14:'<scroll>', 0xff15:'<sysreq>', 0xff1b:'<escape>',
  0xffff:'<delete>', 0xff50:'<home>', 0xff51:'<left>', 0xff52:'<up>',
  0xff53:'<right>', 0xff54:'<down>', 0xff55:'<pageup>',0xff56:'<pagedown>', 
  0xff63:'<insert>',0xff57:'<end>', 0xff58:'<begin>',
  0xffbe:'<F1>',0xffbf:'<F2>',0xffc0:'<F3>',0xffc1:'<F4>',
  0xffc2:'<F5>',0xffc3:'<F6>',0xffc4:'<F7>',0xffc5:'<F8>',
  0xffc6:'<F9>',0xffc7:'<F10>',0xffc8:'<F11>',0xffc9:'<F12>',
  0xffe1:'<lshift>', 0xffe2:'<rshift>', 0xffe3:'<lctrl>', 0xffe4:'<rctrl>',
  0xffe5:'<capslock>', 0xffe6:'<shiftlock>', 0xffe9:'<lalt>',
  0xffea:'<ralt>', 0x0020:'<space>'
}


BG_TIME_EVENT=0x80
BG_CONNECTED_EVENT=0x81
BG_AUTH_SUCCESS_EVENT=0x82
BG_CLOSED_EVENT=0x83
BG_KEY_EVENT=0x84
BG_POINT_EVENT=0x85
BG_FRAME_UPDATE_EVENT=0x86
BG_STAT_MESSAGE_EVENT=0x87
BG_FRAME_BUFFER_UPDATE=0x88
BG_SERVER_CUT_TEXT_EVENT = 0x89
BG_FULL_FRAME_MARK = 0x8a
BG_CLIENT_CUT_TEXT_EVENT = 0x8b

BG_STAT_MSG_KEYPRESSED = 0x1
BG_STAT_MSG_POINTPRESSED = 0x2
BG_STAT_MSG_FRAME_UPDATED = 0x3
BG_STAT_MSG_FRAME_RAW_BYTES_EQUAL=0x4
BG_STAT_MSG_FRAME_BYTES_SENT=0x5
BG_STAT_MSG_ENCODE_RAW = 0x80
BG_STAT_MSG_ENCODE_COPY = 0x81
BG_STAT_MSG_ENCODE_TIGHT = 0x87

bgstatmsg = {
    BG_STAT_MSG_KEYPRESSED:     'Key Pressed',
    BG_STAT_MSG_POINTPRESSED:   'Point Pressed',
    BG_STAT_MSG_FRAME_UPDATED:  'Frame update',
    BG_STAT_MSG_FRAME_RAW_BYTES_EQUAL: 'Frame Raw Bytes Sent Equal',
    BG_STAT_MSG_FRAME_BYTES_SENT:'Frame Bytes Sent Actual',
    BG_STAT_MSG_ENCODE_RAW:     'Frame Encode Type Raw',
    BG_STAT_MSG_ENCODE_COPY:    'Frame Encode Type Copy',
    BG_STAT_MSG_ENCODE_TIGHT:   'Frame Encode Type Tight',
}

firstFrameUpdateTime = 0
lastFrameUpdateTime = 0
currentTime_in_ms = 0

def timeEvent(buffer,f):
    (eventtype,b2,minisecond,second) = struct.unpack('BBHI',buffer)
    timeval = datetime.datetime.strptime(time.ctime(second),
            "%a %b %d %H:%M:%S %Y" )
    print "%s.%d"%(timeval,minisecond)
    global currentTime_in_ms
    currentTime_in_ms = (second * 1000) +minisecond

def connectedEvent(buffer,f):
    print "Connected"

def keyEvent(buffer,f):
    (eventtype,action,key) = struct.unpack('BBH',buffer)
    if key in translate:
        keystr = translate[key]
    else:
        keystr = "Unknown"
    print "Key Event","Downflag",action,"key","%4x"%key,keystr

def pointEvent(buffer,f):
    (eventtype,action,b3,b4,x,y) = struct.unpack('BBBBHH',buffer)
    print "Point Event","buttonMask",action,"x",x,"y",y

def authSuccessEvent(buffer,f):
    print "Authentication Successful"

def frameUpdateEvent(buffer,f):
    (eventtype,action,RectNum) = struct.unpack('BBH',buffer)
    print "Frame Update RectNo",RectNum
    global firstFrameUpdateTime
    global currentTime_in_ms
    global lastFrameUpdateTime
    lastFrameUpdateTime = currentTime_in_ms
    if 0 == firstFrameUpdateTime:
        firstFrameUpdateTime = currentTime_in_ms
    
        

def closeEvent(buffer,f):
    print "File Closed Normally"

def frameBufferUpdate(buffer,f):
    (eventtype,action,RectNum,length) = struct.unpack('BBHI',buffer)
    print "Frame Buffer Update RectNo:",RectNum,"length:",length
    f.read(length)
    #check alignment
    align=4
    mod=length%align
    #print "mod",mod
    if mod>0:
        f.read(align-mod)
        
def serverCutTextEvent(buffer,f):
    (eventtype,action,length) = struct.unpack('BBH',buffer)
    print "Server Clipboard Text Event, len:",length
    text = f.read(length)
    print text
    #check alignment
    align=4
    mod=length%align
    #print "mod",mod
    if mod>0:
        f.read(align-mod)


def clientCutTextEvent(buffer,f):
    (eventtype,action,length) = struct.unpack('BBH',buffer)
    print "Client Clipboard Text Event, len:",length
    text = f.read(length)
    print text
    #check alignment
    align=4
    mod=length%align
    #print "mod",mod
    if mod>0:
        f.read(align-mod)
        
def statMessage(buffer,f):
    (eventtype,action,b3,b4,i1,value)=struct.unpack('BBBBIQ',buffer)
    if action in bgstatmsg:
        print "Stat Msg",bgstatmsg[action],value

def insertfullframeMark(buffer,f):
    (eventtype,action,b3,b4,width,height)=struct.unpack('BBBBHH',buffer)
    print "Full Frame Mark","Width",width,"Height",height

bglogitem = {
    BG_TIME_EVENT:(8,timeEvent),
    BG_CONNECTED_EVENT:(4,connectedEvent),
    BG_AUTH_SUCCESS_EVENT:(4,authSuccessEvent),
    BG_CLOSED_EVENT:(4,closeEvent),
    BG_KEY_EVENT:(4,keyEvent),
    BG_POINT_EVENT:(8,pointEvent),
    BG_FRAME_UPDATE_EVENT:(4,frameUpdateEvent),
    BG_STAT_MESSAGE_EVENT:(16,statMessage),
    BG_FRAME_BUFFER_UPDATE: (8,frameBufferUpdate),
    BG_SERVER_CUT_TEXT_EVENT: (4,serverCutTextEvent),
    BG_FULL_FRAME_MARK: (8,insertfullframeMark),
    BG_CLIENT_CUT_TEXT_EVENT: (4,clientCutTextEvent),
}
    
def main():
    if len(sys.argv)==2:
        try:
            f=open(sys.argv[1],"rb")
        except:
            print("can not open %s"%sys.argv[1])
            return 0
    else:
        print sys.argv[0], "inputfile"
        return 0

    while True:
        byte=f.read(1)
        if byte =="":
            print("End of Bglog Parsing")
            timeval = datetime.datetime.strptime(time.ctime(firstFrameUpdateTime/1000),
                      "%a %b %d %H:%M:%S %Y" )
            print "Frame recording started at %s.%d"%(timeval,firstFrameUpdateTime%1000)
            print "Duration in Second: ",(lastFrameUpdateTime-firstFrameUpdateTime)/1000
            
            break
        (item,)=struct.unpack('B',byte)
        #print "0x%x"%item
        if item in bglogitem:
            (length,func) = bglogitem[item]
        else:
            break
        #print length
        #Get the whole record
        buffer = byte+f.read(length-1)
        func(buffer,f)

    return 0

if __name__ == '__main__':
    main()
