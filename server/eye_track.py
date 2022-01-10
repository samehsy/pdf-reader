import cv2
import numpy as np
import cv2


class EyeTrack:

    face_detector = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml")
    eye_detector = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")

    capturing = False

    def detect_face(self, img):
        """
        Capture the biggest face on the frame, return it
        """
        faces = self.face_detector.detectMultiScale(img, 1.3, 5)

        if len(faces) > 1:
            biggest = (0, 0, 0, 0)
            for i in faces:
                if i[3] > biggest[3]:
                    biggest = i
            # noinspection PyUnboundLocalVariable
            biggest = np.array([i], np.int32)
        elif len(faces) == 1:
            biggest = faces
        else:
            return -200, -200, None

        for (x, y, w, h) in biggest:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('face', img)
            frame = img[y: y + h, x: x + w]
            return x, y, frame

    def detect_eyes(self, img):
        """return left eye and right eye """
        eyes = self.eye_detector.detectMultiScale(img, 1.3, 5)  # detect eyes
        width = np.size(img, 1)  # get face frame width
        height = np.size(img, 0)  # get face frame height
        left_eye = None
        right_eye = None
        for (x, y, w, h) in eyes:
            if y > height / 2:
                pass
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 250), 2)
            cv2.imshow('eye', img)
            eyecenter = x + w / 2  # get the eye center
            if eyecenter < (width/2):
                left_eye = img[y:y + h, x:x + w]
            else:
                right_eye = img[y:y + h, x:x + w]
        return left_eye, right_eye

    def cut_eyebrows(self, img):
        """ remove eyebrows from eye image"""

        height, width = img.shape

        eyebrow_h = int(height / 4)
        img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

        return img

    def get_contour(self, img, threshold):
        """ return center of eye"""
        cx = 0
        cy = 0
        img = self.cut_eyebrows(img)
        kernel = np.ones((5, 5), np.uint8)
        ret, thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
        thresh = cv2.dilate(thresh, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if (len(contours)) > 0:
            contour = sorted(
                contours, key=lambda x: cv2.contourArea(x), reverse=True)
            cv2.drawContours(img, contour, -1, (0, 0, 255), 1)

            M = cv2.moments(contour[0])
    #         print(M)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        return cx, cy

    def nothing(self, x):
        pass

    def get_operter(self, count_frame, list_frame ,  socketio):
        """return opreation """
        f1 = list_frame[0]
        f5 = list_frame[9]
        if (abs(f5[4] - f1[4]) <= 4) and (abs(f5[5] - f1[5]) <= 4):
            #             print('face')
            if f5[1] == -200 and f5[3] == -200 and f1[1] == -200 and f1[3] == -200:
                print('screenshot')
                socketio.emit('scroll',{'screenshot': True} )
                return 'screenshot'
            elif f5[1] > f1[1] or f5[3] > f1[3]:
                print('scroll up')
                socketio.emit('scroll',{'up': True} )
                return 'scroll up'
            elif f5[1] < f1[1] or f5[3] < f1[3]:
                print('scroll down')
                socketio.emit('scroll',{'down': True} )

                return 'scroll down'

    def process_frame(self  ,  socketio):

        count_frame = 0
        list_frame = []
        cx_l = -200
        cy_l = -200
        cx_r = -200
        cy_r = -200
        cap = cv2.VideoCapture(0)
        cv2.namedWindow('image')
        cv2.createTrackbar('threshold', 'image', 0, 255, self.nothing)

        while True:

            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            xf, yf, faces = self.detect_face(gray)
            if faces is not None:
                count_frame += 1

                left_eye, right_eye = self.detect_eyes(faces)
                threshold = cv2.getTrackbarPos('threshold', 'image')

                if left_eye is not None:
                    cx_l, cy_l = self.get_contour(left_eye, threshold)

                if right_eye is not None:
                    cx_r, cy_r = self.get_contour(right_eye, threshold)

                if count_frame < 10:
                    list_frame.append((cx_l, cy_l,  cx_r, cy_r, xf, yf))
                else:
                    #                     print(list_frame)
                    #                     print("------------------------------------------------------------------------")
                    list_frame.append((cx_l, cy_l,  cx_r, cy_r, xf, yf))
                    opreter = self.get_operter(count_frame, list_frame , socketio)
                    list_frame.pop(0)

            cv2.imshow('img', img)

            k = cv2.waitKey(30) & 0xff
            if not self.capturing:
                break
        cv2.waitKey(0)
        cap.release()
        cv2.destroyAllWindows()

        # cv2.destroyAllWindows()


    def stop(self):
        cv2.waitKey(0)
        self.capturing = False
        cv2.destroyAllWindows()

