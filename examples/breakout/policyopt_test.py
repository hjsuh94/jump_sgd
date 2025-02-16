import numpy as np
import torch 
import matplotlib.pyplot as plt 

from alpha_gradient.objective_function_policy import ObjectiveFunctionPolicy
from alpha_gradient.dynamical_system import DynamicalSystem
from alpha_gradient.optimizer_policy import (
    FobgdPolicyOptimizer, FobgdPolicyOptimizerParams,
    ZobgdPolicyOptimizer, ZobgdPolicyOptimizerParams,
    BCPolicyOptimizer, BCPolicyOptimizerParams)
from alpha_gradient.stepsize_scheduler import ManualScheduler   
from alpha_gradient.policy import LinearPolicy 

from breakout_dynamics_toi import BreakoutDynamics
from breakout_policyopt import BreakoutPolicyOpt

# Set up dynamics.
dynamics = BreakoutDynamics()
sample_size = 100
stdev = 0.001

# Initial condition.
xg = torch.tensor([0.0, 2.5, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=torch.float32)
T = 200
Q = torch.diag(torch.tensor([0, 0, 0, 0, 0, 0, 0], dtype=torch.float32))
Qd = 100.0 * torch.diag(torch.tensor([1, 1, 0.1, 0.1, 0, 0, 0], dtype=torch.float32))
R = 0.001 * torch.diag(torch.tensor([1, 1, 1], dtype=torch.float32))

# Set up sampling function for x0.
def sample_x0_batch(sample_size):
    #ball_x0 = 1.8 * (2.0 * torch.rand(sample_size) - 1.0)
    #ball_y0 = 2.0 + torch.rand(sample_size)

    ball_x0 = 1.0 * torch.ones(sample_size) + torch.normal(
        0, 1.0, (sample_size,1)).squeeze(1)
    ball_y0 = 2.0 * torch.ones(sample_size) + torch.normal(
        0, 0.2, (sample_size,1)).squeeze(1)
    ball_vx0 = -0.2 * ball_x0 + torch.normal(0.0, 0.01, (sample_size,1)).squeeze(1)
    ball_vy0 = -0.2 * ball_y0 + torch.normal(0.0, 0.01, (sample_size,1)).squeeze(1)

    pad_x0 = torch.normal(0.0, 0.5, (sample_size,1)).squeeze(1)
    pad_y0 = torch.normal(0.0, 0.01, (sample_size,1)).squeeze(1)
    pad_theta0 = torch.normal(0.0, 0.01, (sample_size,1)).squeeze(1)

    return torch.vstack(
        (ball_x0, ball_y0, ball_vx0, ball_vy0, pad_x0, pad_y0, pad_theta0)
        ).transpose(0,1)


print(sample_x0_batch(1000).shape)

# Set up policy.
policy = LinearPolicy(dynamics.dim_x, dynamics.dim_u)
theta0 = torch.zeros(policy.d)

# Set up Objective.
objective = BreakoutPolicyOpt(T, dynamics, policy, Q, Qd, R, xg, sample_x0_batch)

#print(objective.zero_order_batch_gradient(theta0, sample_size, 0.01))
#print(objective.first_order_batch_gradient(theta0, sample_size, 0.01))

#============================================================================
params = FobgdPolicyOptimizerParams()
params.stdev = stdev
params.sample_size = sample_size
def constant_step(iter, initial_step): return 1e-5 * 1/(iter ** 0.1)
params.step_size_scheduler = ManualScheduler(constant_step, 1e-5)
params.theta0 = theta0
num_iters = 10

optimizer = FobgdPolicyOptimizer(objective, params)
optimizer.iterate(num_iters)

x_trj_batch, _ = objective.rollout_policy_batch(
    sample_x0_batch(100), torch.zeros(100, T, objective.m),
    optimizer.theta)

plt.figure()
for b in range(x_trj_batch.shape[0]):
    plt.plot(x_trj_batch[b,:,0], x_trj_batch[b,:,1])
plt.show()

plt.figure()
plt.plot(optimizer.cost_lst)
plt.show()


