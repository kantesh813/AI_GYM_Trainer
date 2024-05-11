import cv2
import math
import numpy as np
import PoseModule as pm
from gtts import gTTS
import mediapipe as mp
from playsound import playsound



class AIGymTrainer:
    def __init__(self):
        self.cap = cv2.VideoCapture('./deadlift.mp4')
        self.detector = pm.poseDetector()
        self.dir = 0
        self.count = 0
        self.push_ups = 0
        self.run()
        self.stage = "down"


    def countPushUps(self, img, lmList):

        if lmList:
            a1 = self.detector.findAngle(img,11,13,
                                         15,
                                         )
            a2 = self.detector.findAngle(img,16,
                                         14,
                                         12,
                                         )
            per_val1 = int(np.interp(a1, (190, 280), (0, 100)))
            per_val2 = int(np.interp(a2, (70, 170), (100, 0)))
            bar_val1 = int(np.interp(per_val1, (0, 100), (40 + 350, 40)))
            bar_val2 = int(np.interp(per_val2, (0, 100), (40 + 350, 40)))
            cv2.rectangle(img, (570, bar_val1), (570 + 35, 40 + 350), (0,255,255), cv2.FILLED)
            cv2.rectangle(img, (570, 40), (570 + 35, 40 + 350), (), 3)
            cv2.rectangle(img, (35, bar_val2), (35 + 35, 40 + 350), (0,255,255), cv2.FILLED)
            cv2.rectangle(img, (35, 40), (35 + 35, 40 + 350), (), 3)
            if per_val1 == 100 and per_val2 == 100:
                if self.dir == 0:
                    self.push_ups += 0.5
                    print(self.push_ups)
                    self.dir = 1
                    color = (0, 255, 0)
            elif per_val1 == 0 and per_val2 == 0:
                if self.dir == 1:
                    self.push_ups += 0.5
                    print(self.push_ups)
                    self.dir = 0
                    color = (0, 255, 0)
            else:
                color = (0, 0, 255)

            text = f'push_ups : {int(self.push_ups)}'
            text_color = (0, 0, 255)
            rectangle_color = (255, 0, 0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2
            thickness = 3
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            text_origin = (209, 35)
            cv2.putText(img, text, text_origin, font, font_scale, text_color, thickness)

            # Draw rectangle around the text
            (startX, startY) = text_origin
            endX = startX + text_size[0] + 10
            endY = startY - text_size[1] - 10
            cv2.rectangle(img, (startX, startY), (endX, endY), rectangle_color, thickness,cv2.FILLED)


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


    def deadlift(self,cap):
        # Deadlift counter variables
        counter = 0
        stage = None

        # Setup mediapipe instance
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils

        # Initialize Pose instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            # Recolor image to RGB
            image = cv2.cvtColor(cap, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                leftHand = [landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].y]
                rightHand = [landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].y]
                print("Happening")

                # Adjust these coordinates according to your setup
                if (self.checkHandInBox(leftHand[0] * 640, leftHand[1] * 480, 590, 20, 670, 80) or self.checkHandInBox(
                        rightHand[0] * 640, rightHand[1] * 480, 600, 0, 680, 60)):
                    print("Wrong View")

                    return

                left_hand = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value]
                right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value]
                left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
                right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]


                if self.checkDeadlift(left_hand, right_hand, left_knee, right_knee,False):
                    print("135 line give true")
                if(self.stage == "down" and self.checkDeadlift(left_hand, right_hand, left_knee, right_knee, True)):
                    print("139 line give true")
                    self.stage = "up"
                    self.count =self.count+1
                    mytext = str(self.count)
                    language = 'en'
                    myobj = gTTS(text=mytext, lang=language, slow=True)
                    print("should play")
                    myobj.save("welcome" + str(self.count) + ".mp3")
                    playsound("welcome" + str(self.count) + ".mp3")
                    print(self.count)
            except:
                pass

            # Setup status box
            cv2.rectangle(image, (0, 0), (240, 73), (245, 117, 16), -1)

            # Rep data
            print("I am here")
            cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(self.count),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (85, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, stage,
                        (80, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

    def checkDeadlift(self,a, b, c, d, checkUp):
        if c.visibility > 0.5 and d.visibility > 0.5:
            print("Visible")
            print(checkUp)
            if checkUp:
                print("Distance",math.sqrt(math.pow(a.y-c.y,2) + math.pow(b.y-d.y,2)))
                if math.sqrt(math.pow(a.y-c.y,2) + math.pow(b.y-d.y,2))<0.009:
                    return True
                else:
                    return False
            else:
                print("for up a.y:", a.y, " c.y:", c.y, " b.y:", b.y, " d.y:", d.y)
                if (a.y+0.11) < (c.y) and (b.y+0.11) < (d.y):
                    print("Give to Down")
                    self.stage="down"
                    return True
                else:
                    return False
        else:
            print("Not Visible")
            return False

    def checkHandInBox(self,x, y, x1, y1, x2, y2):
        if x1 < x < x2 and y1 < y < y2:
            return True
        else:
            return False

    def single_handed_curl(self, img, lmList):
        if len(lmList) != 0:
            angle = self.detector.findAngle(img, 12, 14, 16)
            per = np.interp(angle, (140, 50), (0, 100))

            if per == 100:
                if self.dir == 0:
                    self.count += 0.5
                    self.dir = 1
            if per == 0:
                if self.dir == 1:
                    self.count += 0.5
                    self.dir = 0
            if angle<140:
                self.Wrong_Posture(img)

            cv2.putText(img, str(int(self.count)), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5, cv2.LINE_AA)
    def barbell_curl(self, img, lmList):
        if len(lmList) != 0:
            angle = self.detector.findAngle(img, 12, 14, 16)
            per = np.interp(angle, (170, 50), (0, 100))

            if len(lmList) > 24:
                x, y = lmList[24][1:]
                x = x + 200
                FPangle = self.detector.findAngle(img, 12, 24, (x, y), True, True)
                print(FPangle)
                cv2.circle(img, (x, y), 5, (255, 0, 0), cv2.FILLED)

            if per == 100:
                if self.dir == 0:
                    self.count += 0.5
                    self.dir = 1
            if per == 0:
                if self.dir == 1:
                    self.count += 0.5
                    self.dir = 0

            PFangle = self.detector.findAngle(img, 12, 24, (x, y), True, True)
            if (PFangle < 90 or PFangle > 100):
                self.Wrong_Posture(img,"Wrong Angle")

            cv2.putText(img, str(int(self.count)), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5, cv2.LINE_AA)



    def run(self):
        exercise_choice = input("Enter 1 for single dumbbell curl, 2 for reverse fly, 3 for barbell curl, 4 for push-ups:")
        while True:
            success, img = self.cap.read()
            img = cv2.resize(img, (780, 720))
            img = self.detector.findPose(img, False)
            lmList = self.detector.findPosition(img, False)

            if exercise_choice == '1':
                self.single_handed_curl(img, lmList)
            elif exercise_choice == '2':
                self.Reverse_Fly(img, lmList)
            elif exercise_choice == '3':
                self.barbell_curl(img, lmList)
            elif exercise_choice == '4':
                self.countPushUps(img, lmList)
            elif exercise_choice == '5':
                self.deadlift(img)

            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    def Wrong_Posture(self,img,text="Wrong"):
        rectangle_color = (0, 0, 255)
        start_point = (550, 600)
        end_point = (780, 720)

        # Draw filled rectangle
        cv2.rectangle(img, start_point, end_point, rectangle_color, cv2.FILLED)

        # Add text
        text = text
        text_color = (255, 255, 255)  # White color (BGR format)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        thickness = 3
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_origin = (570,670)

        cv2.putText(img, text, text_origin, font, font_scale, text_color, thickness)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    trainer = AIGymTrainer()

