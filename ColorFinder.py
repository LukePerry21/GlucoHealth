import cv2
import numpy as np
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
from colormath.color_objects import LabColor, sRGBColor
from sklearn.cluster import KMeans


class ColorFinder:
    def __init__(self, visualize=False):
        self.visualize = visualize
        self.colors = [[48.9483, 41.6267, 48.5562], [71.0316, 52.5161, 73.1012], [69.7912, 52.2791, 71.2367],
                       [78.4401, 46.8239, 75.1105], [79.2467, 56.6135, 64.6417],
                       [77.795, 54.2564, 71.6756], [103.253, 76.9758, 83.7061]]
        self.colorLabels = ["0 mg/ml", "2.2 mg/ml", "2.35 mg/ml",
                            "2.5 mg/ml", "2.65 mg/ml",
                            "2.8 mg/ml", "3.1 mg/ml"]
        self.colorBin = ''
        self.colorBin_dist = ''

    def findBin(self, filename):
        color = self.find_Color(filename)
        self.colorBin = ''
        self.colorBin_dist = ''
        for index, color_bin in enumerate(self.colors):
            cb = self.convert_to_Lab(color_bin)
            dist = self.find_distance(color, cb)
            if self.colorBin == '':
                self.colorBin = self.colorLabels[index]
                self.colorBin_dist = dist
            else:
                if self.colorBin_dist > dist:
                    self.colorBin = self.colorLabels[index]
                    self.colorBin_dist = dist
        print('Bin found')
        print(f'Bin is {self.colorBin} and distance is {self.colorBin_dist}')

    @staticmethod
    def find_distance(color, color_bin):
        return delta_e_cie1976(color, color_bin)

    def find_Color(self, filename):
        """This function finds the most dominant color of an image
        returns the color in a Lab value"""
        # Load image and convert to a list of pixels
        reshape = self.convert_image(filename)
        # Find and display most dominant colors
        dominant = self.find_dominant_color(reshape)
        # Converts dominant color to Lab Values
        lab_value = self.convert_to_Lab(dominant)
        return lab_value

    @staticmethod
    def convert_to_Lab(domi):
        """Converts final color to a lab values"""
        rgb = sRGBColor((domi[0]) / 255, (domi[1]) / 255, (domi[2]) / 255)
        lab = convert_color(rgb, LabColor, through_rgb_type=sRGBColor, target_illuminant='d65')
        return lab

    def find_dominant_color(self, reshape):
        """This function finds and displays most dominant colors.
        Visual will only run if self.visualization == True"""
        cluster = KMeans(n_clusters=5).fit(reshape)
        visualize, domi = self.visualize_colors(cluster, cluster.cluster_centers_)
        if self.visualize:
            visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
            cv2.imshow('visualize', visualize)
            cv2.waitKey()
        return domi

    def visualize_colors(self, cluster, centroids):
        # Get the number of different clusters, create histogram, and normalize
        labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
        (hist, _) = np.histogram(cluster.labels_, bins=labels)
        hist = hist.astype("float")
        hist /= hist.sum()

        # Create frequency rect and iterate through each cluster's color and percentage
        rect = np.zeros((50, 300, 3), dtype=np.uint8)
        colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
        start = 0
        for (percent, color) in colors:
            if self.visualize:
                print(color, "{:0.2f}%".format(percent * 100))
            end = start + (percent * 300)
            cv2.rectangle(rect, (int(start), 0), (int(end), 50),
                          color.astype("uint8").tolist(), -1)
            start = end
        return rect, color

    @staticmethod
    def convert_image(filename):
        """This function loads an image and converts it to a list of pixels
        """
        image = cv2.imread(filename)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        reshape = image.reshape((image.shape[0] * image.shape[1], 3))

        return reshape

#
# print('### 2.35 Test ###')
# cf = ColorFinder(visualize=False)
# cf.findBin('Amyl_2.35(2).jpg')
#
# print('### 2.5 Test 1 ###')
# cf2 = ColorFinder(visualize=False)
# cf2.findBin('Amyl_2.5(1).jpg')
#
# print('### 2.5 Test 2 ###')
# cf4 = ColorFinder(visualize=False)
# cf4.findBin('Amyl_2.5(2).jpg')
#
# dist = cf4.find_distance(cf4.find_Color('Amyl_2.5(2).jpg'), cf4.convert_to_Lab(cf4.colors[0]))
# print(f'2.5 bin distance is {dist}')
#
# print('### 2.5 Test 3 ###')
# cf5 = ColorFinder(visualize=False)
# cf5.findBin('Amyl_2.5(3).jpg')
#
# dist = cf5.find_distance(cf5.find_Color('Amyl_2.5(3).jpg'), cf5.convert_to_Lab(cf5.colors[0]))
# print(f'2.5 bin distance is {dist}')
#
# print('### 0 Test ###')
# cf3 = ColorFinder(visualize=False)
# cf3.findBin('Amyl_0(1).jpg')






