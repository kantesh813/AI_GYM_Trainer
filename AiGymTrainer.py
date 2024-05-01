import cv2
import numpy as np
import PoseModule as pm

class AIGymTrainer:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = pm.poseDetector()
        self.dir = 0
        self.count = 0
        self.run()

    def Reverse_Fly(self, img, lmList):
        if len(lmList) != 0:
            angle = self.detector.findAngle(img, 11, 13, 15)
            per = np.interp(angle, (180, 210), (0, 100))
            angle = self.detector.findAngle(img, 12, 14, 16)


            if per == 100:
                if self.dir == 0:
                    self.count += 0.5
                    self.dir = 1
            if per == 0:
                if self.dir == 1:
                    self.count += 0.5
                    self.dir = 0

            cv2.putText(img, str(int(self.count)), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5, cv2.LINE_AA)

    def single_handed_curl(self, img, lmList):
        if len(lmList) != 0:
            angle = self.detector.findAngle(img, 11, 13, 15)
            per = np.interp(angle, (191, 310), (0, 100))

            if per == 100:
                if self.dir == 0:
                    self.count += 0.5
                    self.dir = 1
            if per == 0:
                if self.dir == 1:
                    self.count += 0.5
                    self.dir = 0

            cv2.putText(img, str(int(self.count)), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5, cv2.LINE_AA)

    def run(self):
        exercise_choice = input("Enter 1 for single dumbbell curl, 2 for reverse fly:")
        while True:
            success, img = self.cap.read()
            img = cv2.resize(img, (780, 720))
            img = self.detector.findPose(img, False)
            lmList = self.detector.findPosition(img, False)
            if exercise_choice == '1':
                self.single_handed_curl(img, lmList)
            elif exercise_choice == '2':
                self.Reverse_Fly(img, lmList)


            cv2.imshow("Image", img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    trainer = AIGymTrainer()

