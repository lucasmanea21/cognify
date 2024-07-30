import numpy as np

fs = 256

bands = {
    'delta': (1, 4),
    'theta': (4, 8),
    'alpha': (8, 12),
    'low_beta': (12, 20),
    'high_beta': (20, 30),
    'beta': (12, 30)
}

# save last metrics, so if data is 0 we don't get errors
last_valid_metrics = {
    'attention': 0.0,
    'stress': 0.0,
    'relaxation': 0.0
}

# band power calculation, based on https://raphaelvallat.com/bandpower.html
def get_band_power(signal, band, fs):
    n = len(signal)
    psd = np.abs(np.fft.fft(signal))**2
    
    freqs = np.fft.fftfreq(n, 1/fs)
    
    idx = np.where((freqs >= band[0]) & (freqs <= band[1]))[0]
    power = np.sum(psd[idx]) / len(psd)
    
    return power


def calculate_metrics(data):
    global last_valid_metrics
    data = np.array(data)

    if np.all(data == 0):
        return last_valid_metrics  # return last valid metrics if data is all 0's

    band_powers = {band: [] for band in bands}

    for channel in data:
        for band in bands:
            power = get_band_power(channel, bands[band], fs)
            band_powers[band].append(power)

    for band in band_powers:
        band_powers[band] = np.array(band_powers[band])

    total_power = np.sum([band_powers[band] for band in bands], axis=0)

    # avoid division by zero by adding a small epsilon value
    epsilon = 1e-10

    # normalize the power ratios
    attention_ratio = band_powers['beta'] / (band_powers['alpha'] + band_powers['theta'] + epsilon)
    stress_ratio = band_powers['high_beta'] / (band_powers['alpha'] + epsilon)
    relaxation_ratio = band_powers['alpha'] / (total_power + epsilon)

    # scale ratios to be within 0-100 range
    attention = attention_ratio / (attention_ratio + 1) * 100
    stress = stress_ratio / (stress_ratio + 1) * 100
    relaxation = relaxation_ratio / (relaxation_ratio + 1) * 100

    if np.isnan(np.mean(attention)) or np.isnan(np.mean(stress)) or np.isnan(np.mean(relaxation)):
        return last_valid_metrics  

    mean_attention = np.mean(attention)
    mean_stress = np.mean(stress)
    mean_relaxation = np.mean(relaxation)

    current_metrics = {
        'attention': mean_attention,
        'stress': mean_stress,
        'relaxation': mean_relaxation
    }

    last_valid_metrics = current_metrics  
    return current_metrics
