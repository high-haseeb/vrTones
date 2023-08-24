import mediapipe as mp


class handDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def get_landmarks(self, img, draw=True, connect=False):
        landmark_list = {}
        height, width = 480, 640
        self.results = self.hands.process(img)
        if self.results.multi_hand_landmarks:
            for idx, handlms in enumerate(self.results.multi_hand_landmarks):
                side = self.results.multi_handedness[idx].classification[0].label
                landmark_list[side] = []
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handlms, self.mpHands.HAND_CONNECTIONS if connect else {}
                    )
                for landmark in handlms.landmark:
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    landmark_list[side].append([cx, cy])
        return img, landmark_list
