import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
from tqdm import tqdm

import torch

from alpha_gradient.objective_function import ObjectiveFunction
from alpha_gradient.statistical_analysis import compute_mean, compute_variance_norm
from ball_with_wall_softplus import BallWithWallSoftPlus
from ball_with_wall import BallWithWallSoftPlusObjective


plt.figure(figsize=(20,10))
matplotlib.rcParams.update({'font.size': 22})
colors = ["magenta", "springgreen", "royalblue", "orangered"]
kappa_space = np.array([8,10,20,100.0])
B = 1000
plot_space = np.arange(0, B, 40)

for i in range(len(kappa_space)):
    dynamics = BallWithWallSoftPlus()
    dynamics.T = 175
    dynamics.kappa = kappa_space[i]
    objective = BallWithWallSoftPlusObjective(dynamics)
    theta_linspace = torch.linspace(0.0, np.pi/2, B)
    objects = objective.evaluate_batch(theta_linspace, torch.zeros(B))
    plt.subplot(1,2,1)
    plt.plot(theta_linspace, objects, color=colors[i],alpha=0.8, label=str(dynamics.kappa))
    plt.ylabel("Cost")
    plt.xlabel(r'$\theta(rad)$')
    plt.legend()        

    plt.subplot(1,2,2)
    dynamics.render(plt.gca())
    trj_batch = dynamics.rollout_batch(theta_linspace)

    b0 = 370
    b1 = 300
    plt.plot(trj_batch[b0,:,0], trj_batch[b0,:,1], color=colors[i], alpha=0.8)
    plt.plot(trj_batch[b1,:,0], trj_batch[b1,:,1], color=colors[i], alpha=0.8)

    T = 90
    scale = 100.0
    dx0 = trj_batch[b0,T+1,0] - trj_batch[b0,T,0]
    dx1 = trj_batch[b1,T+1,0] - trj_batch[b1,T,0]
    dy0 = trj_batch[b0,T+1,1] - trj_batch[b0,T,1]
    dy1 = trj_batch[b1,T+1,1] - trj_batch[b1,T,1]

    plt.plot(trj_batch[b0, T, 0], trj_batch[b0, T, 1], 'ro', color=colors[i], markersize=7)
    plt.plot(trj_batch[b1, T, 0], trj_batch[b1, T, 1], 'ro', color=colors[i], markersize=7)
    plt.xlabel(r'$x(m)$')
    plt.ylabel(r'$y(m)$')

    fobg_storage = np.zeros((B, 1))
    zobg_storage = np.zeros((B, 1))
    fobg_var_storage = np.zeros((B, 1))
    zobg_var_storage = np.zeros((B, 1))    


plt.show()
