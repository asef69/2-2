#!/usr/bin/env python3
"""
Comprehensive test suite for cft_edge_detector.py
Tests all classes and functions to ensure they run properly.
"""

import sys
import numpy as np
from cft_edge_detector import (
    ContinuousImage, CFT2D, FrequencyFilter, FrequencyFilter2,
    InverseCFT2D, compute_psnr, ringing_score, compare_rotated_spectra,
    top_k_mask
)

def test_continuous_image():
    """Test ContinuousImage class"""
    print("Testing ContinuousImage...")
    try:
        img = ContinuousImage('pikachu.png')
        assert img.image.shape[0] > 0 and img.image.shape[1] > 0
        assert img.x.shape[0] == img.image.shape[1]
        assert img.y.shape[0] == img.image.shape[0]
        assert np.min(img.image) >= 0 and np.max(img.image) <= 1
        print("  ✓ ContinuousImage works correctly")
        return img
    except Exception as e:
        print(f"  ✗ ContinuousImage failed: {e}")
        sys.exit(1)

def test_cft2d(img):
    """Test CFT2D class"""
    print("Testing CFT2D...")
    try:
        cft2d = CFT2D(img)
        real, imag = cft2d.compute_cft()
        assert real.shape == img.image.shape
        assert imag.shape == img.image.shape
        assert np.isfinite(real).all() and np.isfinite(imag).all()
        print("  ✓ CFT2D.compute_cft() works correctly")
        return cft2d, real, imag
    except Exception as e:
        print(f"  ✗ CFT2D failed: {e}")
        sys.exit(1)

def test_frequency_filter(real, imag, cft2d):
    """Test FrequencyFilter class"""
    print("Testing FrequencyFilter...")
    try:
        filt = FrequencyFilter()
        
        # Test high_pass
        real_hp, imag_hp = filt.high_pass(real, imag, 15)
        assert real_hp.shape == real.shape
        assert imag_hp.shape == imag.shape
        print("  ✓ high_pass() works")
        
        # Test low_pass
        real_lp, imag_lp = filt.low_pass(real, imag, 20)
        assert real_lp.shape == real.shape
        assert imag_lp.shape == imag.shape
        print("  ✓ low_pass() works")
        
        # Test band_pass
        real_bp, imag_bp = filt.band_pass(real, imag, 10, 30)
        assert real_bp.shape == real.shape
        assert imag_bp.shape == imag.shape
        print("  ✓ band_pass() works")
        
        # Test spectral_energy_ratio
        ratio = filt.spectral_energy_ratio(real, imag, real_bp, imag_bp)
        assert 0 <= ratio <= 1
        print("  ✓ spectral_energy_ratio() works")
        
        return filt
    except Exception as e:
        print(f"  ✗ FrequencyFilter failed: {e}")
        sys.exit(1)

def test_frequency_filter2(real, imag, cft2d):
    """Test FrequencyFilter2 class"""
    print("Testing FrequencyFilter2...")
    try:
        filt2 = FrequencyFilter2()
        
        # Test notch
        centers = [(10, 10), (20, 20)]
        real_n, imag_n = filt2.notch(real, imag, centers, radius=3)
        assert real_n.shape == real.shape
        assert imag_n.shape == imag.shape
        print("  ✓ notch() works")
        
        # Test gaussian_low_pass
        real_gl, imag_gl = filt2.gaussian_low_pass(real, imag, sigma=15)
        assert real_gl.shape == real.shape
        assert imag_gl.shape == imag.shape
        print("  ✓ gaussian_low_pass() works")
        
        # Test directional_pass
        real_dp, imag_dp = filt2.directional_pass(real, imag, angle_center_deg=0, 
                                                   angle_width_deg=20, min_radius=3)
        assert real_dp.shape == real.shape
        assert imag_dp.shape == imag.shape
        print("  ✓ directional_pass() works")
        
        return filt2
    except Exception as e:
        print(f"  ✗ FrequencyFilter2 failed: {e}")
        sys.exit(1)

def test_inverse_cft2d(real, imag, cft2d, img):
    """Test InverseCFT2D class"""
    print("Testing InverseCFT2D...")
    try:
        icft2d = InverseCFT2D(real, imag, cft2d.u, cft2d.v, img.x, img.y)
        reconstructed = icft2d.reconstruct()
        assert reconstructed.shape == img.image.shape
        assert np.isfinite(reconstructed).all()
        print("  ✓ InverseCFT2D.reconstruct() works")
        return reconstructed
    except Exception as e:
        print(f"  ✗ InverseCFT2D failed: {e}")
        sys.exit(1)

def test_utility_functions(img, reconstructed):
    """Test utility functions"""
    print("Testing utility functions...")
    try:
        # Test compute_psnr
        psnr = compute_psnr(img.image, np.clip(reconstructed, 0, 1))
        assert np.isfinite(psnr)
        print("  ✓ compute_psnr() works")
        
        # Test ringing_score
        profile = reconstructed[reconstructed.shape[0]//2, :]
        score = ringing_score(profile)
        assert np.isfinite(score)
        print("  ✓ ringing_score() works")
        
        # Test compare_rotated_spectra
        from scipy.ndimage import rotate as ndi_rotate
        cft2d = CFT2D(img)
        real, imag = cft2d.compute_cft()
        mag = np.sqrt(real**2 + imag**2)
        
        rotated_img_pixels = ndi_rotate(img.image, 30, reshape=False, order=1)
        class TempImg:
            pass
        temp_img = TempImg()
        temp_img.image = rotated_img_pixels
        temp_img.x = img.x
        temp_img.y = img.y
        
        cft2d_rot = CFT2D(temp_img)
        real_rot, imag_rot = cft2d_rot.compute_cft()
        mag_rot = np.sqrt(real_rot**2 + imag_rot**2)
        
        sim = compare_rotated_spectra(mag, mag_rot, 30)
        assert 0 <= sim <= 1
        print("  ✓ compare_rotated_spectra() works")
        
        # Test top_k_mask
        real_topk, imag_topk = top_k_mask(real, imag, 100)
        assert real_topk.shape == real.shape
        assert imag_topk.shape == imag.shape
        print("  ✓ top_k_mask() works")
        
    except Exception as e:
        print(f"  ✗ Utility functions failed: {e}")
        sys.exit(1)

def test_all_practice_sets():
    """Test all practice set runners"""
    print("Testing all practice set runners...")
    try:
        from cft_edge_detector import (
            run_set_a, run_set_b, run_set_e, run_set_f, 
            run_set_g, run_set_h, run_set_i
        )
        
        sets = [
            ('setA', run_set_a),
            ('setB', run_set_b),
            ('setE', run_set_e),
            ('setF', run_set_f),
            ('setG', run_set_g),
            ('setH', run_set_h),
            ('setI', run_set_i),
        ]
        
        for name, runner in sets:
            print(f"  Testing {name}...", end=" ")
            try:
                runner('pikachu.png')
                print("✓")
            except Exception as e:
                print(f"✗ ({e})")
                raise
                
    except Exception as e:
        print(f"  ✗ Practice set runners failed: {e}")
        sys.exit(1)

def test_edge_detection():
    """Test main edge detection pipeline"""
    print("Testing main edge detection pipeline...")
    try:
        from cft_edge_detector import ContinuousImage, CFT2D, FrequencyFilter, InverseCFT2D
        import matplotlib.pyplot as plt
        
        img = ContinuousImage('pikachu.png')
        cft2d = CFT2D(img)
        real, imag = cft2d.compute_cft()
        
        filt = FrequencyFilter()
        real_f, imag_f = filt.high_pass(real, imag, 15)
        
        icft2d = InverseCFT2D(real_f, imag_f, cft2d.u, cft2d.v, img.x, img.y)
        edges = icft2d.reconstruct()
        
        edge_map = np.abs(edges)
        if edge_map.max() > 0:
            edge_map = edge_map / edge_map.max()
        edge_map = 1 - edge_map
        
        plt.imsave("test_edges.png", edge_map, cmap='gray')
        print("  ✓ Main pipeline works")
        
    except Exception as e:
        print(f"  ✗ Main pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("CFT Edge Detector - Comprehensive Test Suite")
    print("=" * 60)
    
    # Run basic tests
    img = test_continuous_image()
    cft2d, real, imag = test_cft2d(img)
    filt = test_frequency_filter(real, imag, cft2d)
    filt2 = test_frequency_filter2(real, imag, cft2d)
    reconstructed = test_inverse_cft2d(real, imag, cft2d, img)
    test_utility_functions(img, reconstructed)
    test_edge_detection()
    
    # Run practice sets
    print("\n" + "=" * 60)
    test_all_practice_sets()
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
