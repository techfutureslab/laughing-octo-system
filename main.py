from pickletools import uint8
import socket
import cv2 as c
import numpy as np

IP = "192.168.102.47"
UDP_port = 5000

cam = c.VideoCapture(0);
rBlock = 4
cBlock = 3

ret, frame = cam.read()

h, w = frame.shape[:2]
wBlock = w // cBlock
hBlock = h // rBlock

b = 5;

P1 = [h // 2 - b, w // 2 - b]
P2 = [h // 2 + b, w // 2 + b]
print("h:{0},w:{1}".format(h, w))

print("h:{0},w:{1}".format(P1[0], P1[1]))
print("h:{0},w:{1}".format(P2[0], P2[1]))

grid = False

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
    ret, frame = cam.read()
    # frame[318:322,238:242,:]=255;

    red = frame[:, :, 2]
    green = frame[:, :, 1]
    blue = frame[:, :, 0]
    Orange = np.logical_and((frame[:, :, 0] <190+ frame[:,:,2]),np.logical_and(frame[:,:,1]<170,frame[:, :, 1] > 75))

    # Orange = c.threshold(Orange,40,255,1)
    # &  &
    # org =, frame[:,:,2]>220,(frame[:, :, 1] > 75)
    c.imshow("Orange", Orange.astype(float))
    # selected = int((red>100 + green) & (red > 100 + blue))
    # selected = c.threshold(selected,1,1,0)



    # frame2 = ( frame[:,:,1]<10)
    # frame2 = frame2.
    # if c.waitKey(1)== ord('q'):
    #     break
    # if c.waitKey(1)== ord(' '):
    #     print(frame[P1[1],P1[2]])
    # c.imshow("Red", selected)
    # c.imshow("Processed", frame2)

    Q = np.zeros((rBlock,cBlock))
    T = (Q.reshape((1,rBlock*cBlock)))
    sock.sendto(T, (IP, UDP_port))

    for i in range(0, rBlock -1):
        for j in range(0,cBlock -1):
            if (Orange[i*hBlock:(i+1)*hBlock,j*wBlock:(j+1)*wBlock]).any():
                Q[i,j] = 1;

    recKey = c.waitKey(1)
    if recKey != -1:
        print(recKey)
        if recKey == 32:
            print(frame[240, 320])
        if recKey == 65505:
            grid = ~grid
        if recKey == ord('q'):
            break

    c.rectangle(frame, (318, 238), (322, 242), (0, 0, 255), 1)
    if grid:
        for i in range(1, rBlock):
            c.line(frame, (0, i * hBlock), (w, i * hBlock), (0, 165, 255), 1)
        for i in range(1, cBlock):
            c.line(frame, (i * wBlock, 0), (i * wBlock, h), (0, 165, 255), 1)
    c.imshow("Frames", frame)
c.destroyAllWindows()
cam.release()
print(Q)
print(T)
sock.sendto(T, (IP, UDP_port))
