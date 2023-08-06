import cv2
import numpy as np

class add4cto3c():

    def __init__(self,alpha=1.0,scale=1.0):
        self.alpha = alpha
        self.scale = scale

    def F2T(self,img,logo,x=0,y=0):
        (h, w) = img.shape[:2]
        image = np.dstack([img, np.ones((h, w), dtype="uint8") * 255])#sitongdao
        overlay = cv2.resize(logo, None,fx=self.scale,fy=self.scale)
        (ho, wo) = overlay.shape[:2]
        output = image.copy()
        if x < 0:
            x = w+x
        if y < 0:
            y = h+y
        if x+wo > w:
            x = w-wo
        if y+ho > h:
            y = h-ho
        overlay = cv2.addWeighted(output[y:y+ho, x:x+wo],self.alpha,overlay[:ho,:wo],0.5,0)
        output[y:y+ho, x:x+wo] = overlay
        output= output[:,:,:3]
        return output


if __name__ == "__main__":
    main()