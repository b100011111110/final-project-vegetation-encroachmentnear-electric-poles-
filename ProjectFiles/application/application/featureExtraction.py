from PIL import Image
import cv2
import numpy as np 
from skimage import color, feature
from scipy.stats import kurtosis
from PIL import Image,ImageDraw

def extract_features(img):
    # Convert the image to different color spaces
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Split the channels
    b, g, r  = cv2.split(img)
    h, s, v = cv2.split(hsv_img)
    l, a, b_human = cv2.split(lab_img)

    # Calculate mean values
    mean_r, mean_g, mean_b = np.mean(r), np.mean(g), np.mean(b)
    mean_h, mean_s, mean_v = np.mean(h), np.mean(s), np.mean(v)
    mean_l, mean_a, mean_bhuman = np.mean(l), np.mean(a), np.mean(b_human)

    # Calculate standard deviations
    std_r, std_g, std_b = np.std(r), np.std(g), np.std(b)
    std_h, std_s, std_v = np.std(h), np.std(s), np.std(v)
    std_l, std_a, std_bhuman = np.std(l), np.std(a), np.std(b_human)

    # Calculate variances
    var_r, var_g, var_b = np.var(r), np.var(g), np.var(b)
    var_h, var_s, var_v = np.var(h), np.var(s), np.var(v)
    var_l, var_a, var_bhuman = np.var(l), np.var(a), np.var(b_human)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kurtosis_r, kurtosis_g, kurtosis_b = kurtosis(r), kurtosis(g), kurtosis(b)
    kurtosis_r_single = np.mean(kurtosis_r)
    kurtosis_g_single = np.mean(kurtosis_g)
    kurtosis_b_single = np.mean(kurtosis_b)
    # Other texture features
    glcm = feature.graycomatrix(gray_img, [1], [0], symmetric=True, normed=True)
    energy = feature.graycoprops(glcm, prop='energy')[0, 0]
    ASM = feature.graycoprops(glcm, prop='ASM')[0, 0]
    contrast = feature.graycoprops(glcm, prop='contrast')[0, 0]
    homogeneity = feature.graycoprops(glcm, prop='homogeneity')[0, 0]

    features_dict = {
        "mean_r": mean_r, "mean_g": mean_g, "mean_b": mean_b,
        "mean_h": mean_h, "mean_s": mean_s, "mean_v": mean_v,
        "mean_l": mean_l, "mean_a": mean_a, "mean_bhuman": mean_bhuman,
        "std_r": std_r, "std_g": std_g, "std_b": std_b,
        "std_h": std_h, "std_s": std_s, "std_v": std_v,
        "std_l": std_l, "std_a": std_a, "std_bhuman": std_bhuman,
        "var_r": var_r, "var_g": var_g, "var_b": var_b,
        "var_h": var_h, "var_s": var_s, "var_v": var_v,
        "var_l": var_l, "var_a": var_a, "var_bhuman": var_bhuman,
        "energy": energy, "ASM": ASM, "contrast": contrast, "homogeneity": homogeneity,
        "kurtosis_r_single": kurtosis_r_single, "kurtosis_g_single": kurtosis_g_single, "kurtosis_b_single": kurtosis_b_single
    }
    
    return features_dict
