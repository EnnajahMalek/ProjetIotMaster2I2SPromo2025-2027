import random

def anomalous(normal, rate, anomaly):
    """
    Returns normal value or anomaly value based on rate percentage.
    """
    
    if not 0 <= rate <= 100:
        raise ValueError(f"rate must be between 0 and 100, got {rate}")
    
    if not anomaly:
        return normal
    
    if random.random() * 100 < rate:
        return normal
    else:
        return anomaly
    