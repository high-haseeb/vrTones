import json
from math import sqrt

import cv2 as cv
import numpy as np
from pygame import mixer

from hand_detector import handDetector


class playInstrument:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.myHand = handDetector()

    def instrument_init(self, instrument):
        file = open("data.json")
        self.data = json.load(file)
        self.instrument = instrument
        self.total_channels = self.data[self.instrument].get("total_channels")
        self.mode = self.data[self.instrument].get("mode")
        self.__key_angle = 139
        self._tap_distance = 70
        self._draw_flag = False
        self.hands = ["Left", "Right"]
        if self.mode == "key":
            self.key_init()
        elif self.mode == "tap":
            self.tap_init()
        else:
            raise TypeError("Unknown mode")
        self.mixer_init()

    def play(self):
        _, self.img = self.cap.read()
        self.imgRGB = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)
        self.img, self.landmarks = self.myHand.get_landmarks(
            self.imgRGB, draw=self._draw_flag
        )
        if self.mode == "tap":
            self.tap_play()
        elif self.mode == "key":
            self.key_play()
        self.img = cv.flip(self.img, 1)
        return self.img

    def key_init(self):
        self.prev_angle = {}
        for hand in self.hands:
            self.prev_angle[hand] = [self.__key_angle + 10 for _ in range(5)]
        self.joints = [[8, 6, 5], [12, 10, 9], [16, 14, 13], [20, 19, 17], [4, 3, 2]]

    def tap_init(self):
        X = [300, 245, 200, 170, 145, 130, 112, 103, 92, 87, 80, 75, 70, 67, 62, 59, 57]
        Y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        self.A, self.B, self.C = np.polyfit(X, Y, deg=2)
        self.prev_dist = {}
        for hand in self.hands:
            self.prev_dist[hand] = self._tap_distance + 100

    def mixer_init(self):
        mixer.init()
        mixer.set_num_channels(self.total_channels)
        self.channels = []
        for i in range(self.total_channels):
            self.channels.append(mixer.Channel(i))
        self.sounds = {}
        file_type = self.data[self.instrument]["file_type"]
        for hand in self.hands:
            key_map = self.data[self.instrument][f"key_map_{hand}"]
            for i in key_map:
                if self.sounds.get(hand) is None:
                    self.sounds[hand] = []
                try:
                    self.sounds[hand].append(
                        mixer.Sound(
                            f"./assets/sound effects/{self.instrument}/{self.instrument}_{i}.{file_type}"
                        )
                    )
                except:  # noqa: E722
                    raise FileNotFoundError("No sound effect")

    @property
    def _key_angle(self):
        return self.__key_angle

    @_key_angle.setter
    def _key_angle(self, sensitivity):
        self.__key_angle = sensitivity

    @property
    def tap_sensitivity(self):
        return self._tap_distance

    @tap_sensitivity.setter
    def tap_sensitivity(self, sensitivity):
        self._tap_distance = sensitivity

    @property
    def draw_flag(self):
        return self._draw_flag

    @draw_flag.setter
    def draw_flag(self, flag):
        self._draw_flag = flag

    def key_play(self):
        for hand in self.hands:
            channel_offset = 4 if hand == "Left" else 0
            if hand in self.landmarks:
                angle = self.get_angle(self.landmarks[hand])
                for i in range(len(self.joints)):
                    if (
                        angle[i] < self._key_angle
                        and not self.prev_angle[hand][i] < self._key_angle
                    ):
                        self.channels[i + channel_offset].play(self.sounds[hand][i])
                    self.prev_angle[hand][i] = angle[i]

    def tap_play(self):
        for hand in self.hands:
            channel_offset = 1 if hand == "Left" else 0
            channel_idx = 0
            if hand in self.landmarks:
                hand_length = self.landmarks[hand]
                distance = sqrt(
                    (hand_length[5][0] - hand_length[17][0]) ** 2
                    + (hand_length[5][1] - hand_length[17][1]) ** 2
                )
                distanceCM = self.A * (distance**2) + self.B * (distance) + self.C
                if (
                    distanceCM < self._tap_distance
                    and self.prev_dist[hand] > self._tap_distance
                ):
                    self.channels[channel_idx + channel_offset].play(
                        self.sounds[hand][0]
                    )
                self.prev_dist[hand] = distanceCM

    def get_angle(self, pos_data):
        out = []
        for joint in self.joints:
            a = np.array([pos_data[joint[0]][0], pos_data[joint[0]][1]])
            b = np.array([pos_data[joint[1]][0], pos_data[joint[1]][1]])
            c = np.array([pos_data[joint[2]][0], pos_data[joint[2]][1]])
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
                a[1] - b[1], a[0] - b[0]
            )
            angle = np.abs(radians * 180.0 / np.pi)
            if angle > 180:
                angle = 360 - angle
            out.append(angle)
        return out
