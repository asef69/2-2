import numpy as np
import matplotlib.pyplot as plt
from imageio.v2 import imread
import sys


# =====================================================================
# Given classes — paste your Task 2 implementations where indicated
# =====================================================================

class ContinuousImage:
    """Represents a grayscale image as a continuous 2D spatial signal. (Given)"""

    def __init__(self, image_path):
        self.image = imread(image_path, mode='L').astype(float)
        self.image = self.image / np.max(self.image)
        self.x = np.linspace(-1, 1, self.image.shape[1])
        self.y = np.linspace(-1, 1, self.image.shape[0])


class CFT2D:
    """2D Continuous Fourier Transform. (Given — paste your Task 2 solution)"""

    def __init__(self, image_obj: ContinuousImage):
        self.I = image_obj.image
        self.x = image_obj.x
        self.y = image_obj.y
        dx = self.x[1] - self.x[0]
        dy = self.y[1] - self.y[0]
        self.u = np.linspace(-1 / (2 * dx), 1 / (2 * dx), self.I.shape[1])
        self.v = np.linspace(-1 / (2 * dy), 1 / (2 * dy), self.I.shape[0])

    def compute_cft(self):
        """2D CFT via separable trapezoidal integration (no FFT)."""
        cos_ux = np.cos(2 * np.pi * np.outer(self.x, self.u))
        sin_ux = np.sin(2 * np.pi * np.outer(self.x, self.u))

        Ic = np.trapezoid(self.I[:, :, None] * cos_ux[None, :, :], x=self.x, axis=1)
        Is = np.trapezoid(self.I[:, :, None] * sin_ux[None, :, :], x=self.x, axis=1)

        cos_vy = np.cos(2 * np.pi * np.outer(self.v, self.y))
        sin_vy = np.sin(2 * np.pi * np.outer(self.v, self.y))

        term1 = np.trapezoid(cos_vy[:, :, None] * Ic[None, :, :], x=self.y, axis=1)
        term2 = np.trapezoid(sin_vy[:, :, None] * Is[None, :, :], x=self.y, axis=1)
        term3 = np.trapezoid(sin_vy[:, :, None] * Ic[None, :, :], x=self.y, axis=1)
        term4 = np.trapezoid(cos_vy[:, :, None] * Is[None, :, :], x=self.y, axis=1)

        real = term1 - term2
        imag = -(term3 + term4)
        return real, imag

    def plot_magnitude(self):
        real, imag = self.compute_cft()
        magnitude = np.sqrt(real ** 2 + imag ** 2)
        plt.imshow(np.log(1 + magnitude), cmap='gray')
        plt.title("2D CFT Magnitude Spectrum (log-scaled)")
        plt.axis('off')
        plt.show()


class InverseCFT2D:
    """Inverse 2D-CFT. (Given — paste your Task 2 solution)"""

    def __init__(self, real, imag, u, v, x, y):
        self.real = real
        self.imag = imag
        self.u = u
        self.v = v
        self.x = x
        self.y = y

    def reconstruct(self):
        """Inverse 2D CFT via separable trapezoidal integration (no FFT)."""
        cos_vy = np.cos(2 * np.pi * np.outer(self.v, self.y))
        sin_vy = np.sin(2 * np.pi * np.outer(self.v, self.y))

        Cr = np.trapezoid(cos_vy[:, :, None] * self.real[None, :, :], x=self.v, axis=1)
        Sr = np.trapezoid(sin_vy[:, :, None] * self.real[None, :, :], x=self.v, axis=1)
        Ci = np.trapezoid(cos_vy[:, :, None] * self.imag[None, :, :], x=self.v, axis=1)
        Si = np.trapezoid(sin_vy[:, :, None] * self.imag[None, :, :], x=self.v, axis=1)

        G1 = Cr - Si
        G2 = Ci + Sr

        cos_ux = np.cos(2 * np.pi * np.outer(self.x, self.u))
        sin_ux = np.sin(2 * np.pi * np.outer(self.x, self.u))

        term1 = np.trapezoid(G1[:, None, :] * cos_ux[None, :, :], x=self.u, axis=2)
        term2 = np.trapezoid(G2[:, None, :] * sin_ux[None, :, :], x=self.u, axis=2)

        image = term1 - term2
        return image


# =====================================================================
# Task 1 — band_pass and band_stop filters
# =====================================================================

class FrequencyFilter:

    def high_pass(self, real, imag, cutoff):
        """Given."""
        rows, cols = real.shape
        cx, cy = rows // 2, cols // 2
        real = real.copy()
        imag = imag.copy()
        for i in range(rows):
            for j in range(cols):
                if np.sqrt((i - cx) ** 2 + (j - cy) ** 2) <= cutoff:
                    real[i, j] = 0
                    imag[i, j] = 0
        return real, imag

    def band_pass(self, real, imag, r_low, r_high):
        """Retain entries where r_low < d(i,j) <= r_high, zeroing the rest."""
        rows, cols = real.shape
        cx, cy = rows // 2, cols // 2
        real_f = real.copy()
        imag_f = imag.copy()
        for i in range(rows):
            for j in range(cols):
                d = np.sqrt((i - cx) ** 2 + (j - cy) ** 2)
                if not (r_low < d <= r_high):
                    real_f[i, j] = 0
                    imag_f[i, j] = 0
        return real_f, imag_f

    def band_stop(self, real, imag, r_low, r_high):
        """Zero entries where r_low < d(i,j) <= r_high, retaining the rest."""
        rows, cols = real.shape
        cx, cy = rows // 2, cols // 2
        real_f = real.copy()
        imag_f = imag.copy()
        for i in range(rows):
            for j in range(cols):
                d = np.sqrt((i - cx) ** 2 + (j - cy) ** 2)
                if r_low < d <= r_high:
                    real_f[i, j] = 0
                    imag_f[i, j] = 0
        return real_f, imag_f

    def shift_brightness(self, real, imag, shift_amount):
        """Task 3. Add shift_amount to the real component of the exact center pixel."""
        rows, cols = real.shape
        cx, cy = rows // 2, cols // 2
        real_f = real.copy()
        imag_f = imag.copy()
        real_f[cx, cy] = real_f[cx, cy] + shift_amount
        return real_f, imag_f


# =====================================================================
# Task 2 — complementarity check on raw spatial reconstructions
# =====================================================================

class ReconstructionValidator:

    def verify_complementarity(self, I_recon, I_bp, I_bs):
        """Check I_bp + I_bs ~= I_recon on the raw inverse-CFT arrays.
        Returns (is_valid, delta) where delta = max|I_bp + I_bs - I_recon|."""
        delta = np.max(np.abs((I_bp + I_bs) - I_recon))
        is_valid = delta < 1e-9
        return is_valid, delta


# =====================================================================
# Entry point (given — do not modify)
# =====================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cft_edge_detector.py <input_image>")
        sys.exit(1)

    input_path = sys.argv[1]
    r_low, r_high = 10, 50

    img   = ContinuousImage(input_path)
    cft2d = CFT2D(img)
    real, imag = cft2d.compute_cft()

    filt = FrequencyFilter()
    real_bp, imag_bp = filt.band_pass(real, imag, r_low, r_high)
    real_bs, imag_bs = filt.band_stop(real, imag, r_low, r_high)

    def reconstruct(r, im):
        return InverseCFT2D(r, im, cft2d.u, cft2d.v, img.x, img.y).reconstruct()

    I_recon = reconstruct(real,    imag)
    I_bp    = reconstruct(real_bp, imag_bp)
    I_bs    = reconstruct(real_bs, imag_bs)

    validator = ReconstructionValidator()
    is_valid, delta = validator.verify_complementarity(I_recon, I_bp, I_bs)
    print(f"Complementarity check: {is_valid} | max delta: {delta:.2e}")

    def save_edge_map(I_raw, path):
        edge_map = np.abs(I_raw)
        if edge_map.max() > 0:
            edge_map = edge_map / edge_map.max()
        plt.imsave(path, 1 - edge_map, cmap='gray')
        print(f"Saved {path}")

    save_edge_map(I_bp, "pikachu_bandpass.png")
    save_edge_map(I_bs, "pikachu_bandstop.png")

    # Task 3 execution
    real_shifted, imag_shifted = filt.shift_brightness(real, imag, shift_amount=2.0)
    I_brightened = reconstruct(real_shifted, imag_shifted)
    
    # Save brightened image (clip to [0,1], no edge-map inversion)
    I_brightened_clipped = np.clip(I_brightened, 0, 1)
    plt.imsave("pikachu_brightened.png", I_brightened_clipped, cmap='gray')
    print("Saved pikachu_brightened.png")