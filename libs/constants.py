SETTING_FILENAME = 'filename'
SETTING_RECENT_FILES = 'recentFiles'
SETTING_WIN_SIZE = 'window/size'
SETTING_WIN_POSE = 'window/position'
SETTING_WIN_GEOMETRY = 'window/geometry'
SETTING_LINE_COLOR = 'line/color'
SETTING_FILL_COLOR = 'fill/color'
SETTING_ADVANCE_MODE = 'advanced'
SETTING_WIN_STATE = 'window/state'
SETTING_SAVE_DIR = 'savedir'
SETTING_LAST_OPEN_DIR = 'lastOpenDir'
SETTING_TASK_MODE = 'task_mode'
SETTING_BINARY = 'binary'
SETTING_FRAMESTOSKIP = 'framestoskip'
SETTING_COPYPREVPRED = 'copyprevdev'
SETTING_LABEL_FONT_SIZE = 'det/label_font_size'
COLORMAP = {0: [0, 0, 0], 1: [120, 120, 120], 2: [180, 120, 120], 3: [6, 230, 230], 4: [80, 50, 50], 5: [4, 200, 3],
               6: [120, 120, 80], 7: [140, 140, 140], 8: [204, 5, 255], 9: [230, 230, 230], 10: [4, 250, 7],
               11: [224, 5, 255], 12: [235, 255, 7], 13: [150, 5, 61], 14: [120, 120, 70], 15: [8, 255, 51],
               16: [255, 6, 82], 17: [143, 255, 140], 18: [204, 255, 4], 19: [255, 51, 7], 20: [204, 70, 3],
               21: [0, 102, 200], 22: [61, 230, 250], 23: [255, 6, 51], 24: [11, 102, 255], 25: [255, 7, 71],
               26: [255, 9, 224], 27: [9, 7, 230], 28: [220, 220, 220], 29: [255, 9, 92], 30: [112, 9, 255],
               31: [8, 255, 214], 32: [7, 255, 224], 33: [255, 184, 6], 34: [10, 255, 71], 35: [255, 41, 10],
               36: [7, 255, 255], 37: [224, 255, 8], 38: [102, 8, 255], 39: [255, 61, 6], 40: [255, 194, 7],
               41: [255, 122, 8], 42: [0, 255, 20], 43: [255, 8, 41], 44: [255, 5, 153], 45: [6, 51, 255],
               46: [235, 12, 255], 47: [160, 150, 20], 48: [0, 163, 255], 49: [140, 140, 140], 50: [250, 10, 15],
               51: [20, 255, 0], 52: [31, 255, 0], 53: [255, 31, 0], 54: [255, 224, 0], 55: [153, 255, 0],
               56: [0, 0, 255], 57: [255, 71, 0], 58: [0, 235, 255], 59: [0, 173, 255], 60: [31, 0, 255],
               61: [11, 200, 200], 62: [255, 82, 0], 63: [0, 255, 245], 64: [0, 61, 255], 65: [0, 255, 112],
               66: [0, 255, 133], 67: [255, 0, 0], 68: [255, 163, 0], 69: [255, 102, 0], 70: [194, 255, 0],
               71: [0, 143, 255], 72: [51, 255, 0], 73: [0, 82, 255], 74: [0, 255, 41], 75: [0, 255, 173],
               76: [10, 0, 255], 77: [173, 255, 0], 78: [0, 255, 153], 79: [255, 92, 0], 80: [255, 0, 255],
               81: [255, 0, 245], 82: [255, 0, 102], 83: [255, 173, 0], 84: [255, 0, 20], 85: [255, 184, 184],
               86: [0, 31, 255], 87: [0, 255, 61], 88: [0, 71, 255], 89: [255, 0, 204], 90: [0, 255, 194],
               91: [0, 255, 82], 92: [0, 10, 255], 93: [0, 112, 255], 94: [51, 0, 255], 95: [0, 194, 255],
               96: [0, 122, 255], 97: [0, 255, 163], 98: [255, 153, 0], 99: [0, 255, 10], 100: [255, 112, 0],
               101: [143, 255, 0], 102: [82, 0, 255], 103: [163, 255, 0], 104: [255, 235, 0], 105: [8, 184, 170],
               106: [133, 0, 255], 107: [0, 255, 92], 108: [184, 0, 255], 109: [255, 0, 31], 110: [0, 184, 255],
               111: [0, 214, 255], 112: [255, 0, 112], 113: [92, 255, 0], 114: [0, 224, 255], 115: [112, 224, 255],
               116: [70, 184, 160], 117: [163, 0, 255], 118: [153, 0, 255], 119: [71, 255, 0], 120: [255, 0, 163],
               121: [255, 204, 0], 122: [255, 0, 143], 123: [0, 255, 235], 124: [133, 255, 0], 125: [255, 0, 235],
               126: [245, 0, 255], 127: [255, 0, 122], 128: [255, 245, 0], 129: [10, 190, 212], 130: [214, 255, 0],
               131: [0, 204, 255], 132: [20, 0, 255], 133: [255, 255, 0], 134: [0, 153, 255], 135: [0, 41, 255],
               136: [0, 255, 204], 137: [41, 0, 255], 138: [41, 255, 0], 139: [173, 0, 255], 140: [0, 245, 255],
               141: [71, 0, 255], 142: [122, 0, 255], 143: [0, 255, 184], 144: [0, 92, 255], 145: [184, 255, 0],
               146: [0, 133, 255], 147: [255, 214, 0], 148: [25, 194, 194], 149: [102, 255, 0], 150: [92, 0, 255],
               255: [255, 255, 255]}
