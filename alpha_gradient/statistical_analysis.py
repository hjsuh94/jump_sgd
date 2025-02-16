import numpy as np

def compute_mean(x):
    """
    Given a batch of vector quantities, determine the mean.
    args: x of shape (B,n), batch of samples. 
    """
    B = x.shape[0]
    return np.sum(x, axis=0) / B

def compute_covariance_norm(x, p=2):
    """
    Given a batch of vector quantities, compute the covariance
    and computes a norm on the covariance matrix.
    args: x of shape (B,n), batch of samples.
    """
    B = x.shape[0]
    mu = compute_mean(x)
    deviations = np.subtract(x, mu) # B x n
    covariance = np.zeros((x.shape[1], x.shape[1]))
    for i in range(B):
        covariance += np.outer(deviations[i], deviations[i])
    covariance /= (B - 1)
    return np.linalg.norm(covariance, p)# / x.shape[1])

def compute_variance_norm(x, p=2):
    """
    Given a batch of vector quantities, determine the variance.
    Unlike the covariance norms, this computes the inner product
    and takes a vector norm. (i.e. only computes vector norm on 
    the diagonal elemetns of the covariance matrix).
    args: x of shape (B,n), batch of samples.
    """
    B = x.shape[0]
    mu = compute_mean(x)
    deviations = np.subtract(x, mu) # B x n
    covariance = 0.0
    for i in range(B):
        covariance += np.linalg.norm(deviations[i]) ** 2.0
    return covariance / (B - 1)

def compute_confidence_interval_roots(mu, sigma, N, L, delta):
    """
    Compute Bernstein bounds given the empirical mean mu, sigma
    number of samples N, max bound L, and confidence value delta.
    """
    d = len(mu) # dimension of the problem.

    # Compute coefficients of the quadratic inequality.
    # a * eps^2 + b * eps + c >= 0.
    a = N / 2
    b = L / 3 * np.log((1-delta) / (d + 1))
    c = sigma * np.log((1-delta) / (d + 1))

    # Compute the determinant.
    return np.roots(np.array([a,b,c]))

def compute_confidence_interval(mu, sigma, N, L, delta):
    """
    Compute Bernstein bounds given the empirical mean mu, sigma
    number of samples N, max bound L, and confidence value delta.
    """
    d = len(mu) # dimension of the problem.

    # Compute coefficients of the quadratic inequality.
    ft = np.sqrt((2 * sigma * np.log((d + 1) / delta)) / N)
    st = 2 * L / (3 * N) * np.log((d + 1) / delta)
    # Compute the determinant.
    return ft + st

def compute_confidence_probability(d, sigma, N, L, eps):
    """
    Compute Bernstein bounds given the empirical mean mu, sigma
    number of samples N, max bound L, and confidence value delta.
    """
    # Compute coefficients of the quadratic inequality.
    # a * eps^2 + b * eps + c >= 0.
    numer = -eps ** 2.0 * N / 2
    denom = sigma ** 2.0 + L * eps / 3
    p = (d + 1) * np.exp(numer / denom)

    # Compute the determinant.
    return p
