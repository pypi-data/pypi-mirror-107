import numpy as np
from tqdm import tqdm

from poseutils.common import normalize_a_to_b

def normalize_torso_2d(torso):

    #0: RH 1: LH 2: LS 3: RS

    assert len(torso.shape) == 3
    assert torso.shape[1] == 4 and torso.shape[-1] == 2

    torso_ = torso.copy()
    
    widths = [[], [], []]
    names = ["RH -> LH", "RH -> LS", "RH -> RS"]

    torso1_4u = torso_[:, 1, :] - torso_[:, 0, :]
    torso1_8u = torso_[:, 2, :] - torso_[:, 0, :]
    torso1_11u = torso_[:, 3, :] - torso_[:, 0, :]

    torso1_4l = np.linalg.norm(torso1_4u, axis=1).reshape(-1, 1)
    torso1_8l = np.linalg.norm(torso1_8u, axis=1).reshape(-1, 1)
    torso1_11l = np.linalg.norm(torso1_11u, axis=1).reshape(-1, 1)

    torso1_4u = torso1_4u / torso1_4l
    torso1_8u = torso1_8u / torso1_8l
    torso1_11u = torso1_11u / torso1_11l
    
    torso_[:, 0, :] = np.zeros((torso_.shape[0], 2))
    torso_[:, 1, :] = (torso1_4l / torso1_8l+1e-8)*torso1_4u
    torso_[:, 2, :] = torso1_8u
    torso_[:, 3, :] = (torso1_11l / torso1_8l+1e-8)*torso1_11u
    
    widths[0].append(torso1_4l)
    widths[1].append(torso1_8l)
    widths[2].append(torso1_11l)

    return torso_, np.array(widths), names