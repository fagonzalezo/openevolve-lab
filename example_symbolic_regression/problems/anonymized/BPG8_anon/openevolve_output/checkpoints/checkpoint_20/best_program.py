"""
Initial program: A naive linear model for symbolic regression.
This model predicts the output as a linear combination of input variables
or a constant if no input variables are present.
The function is designed for vectorized input (X matrix).

Target output variable: y
Input variables (columns of x): x0, x1
"""
import numpy as np

# Input variable mapping for x (columns of the input matrix):
#   x[:, 0]: x0
#   x[:, 1]: x1

# Parameters will be optimized by BFGS outside this function.
# Number of parameters expected by this model: 10.
# Example initialization: params = np.random.rand(10)

# EVOLVE-BLOCK-START

def func(x, params):
    """
    Calculates the model output using a combination of polynomial and trigonometric features.
    """
    x0 = x[:, 0]
    x1 = x[:, 1]
    return (
        params[0] +
        params[1] * x0 +
        params[2] * x1 +
        params[3] * x0**2 +
        params[4] * x1**2 +
        params[5] * np.sin(x0) +
        params[6] * np.cos(x1) +
        params[7] * (x0 * x1) +
        params[8] * np.exp(-x0**2) +
        params[9] * np.tanh(x1)
    )

# EVOLVE-BLOCK-END

# This part remains fixed (not evolved)
def run_search():
    return func
