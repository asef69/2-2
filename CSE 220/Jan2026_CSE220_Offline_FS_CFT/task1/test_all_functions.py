#!/usr/bin/env python3
"""
Comprehensive test suite for fs_redrawer.py (Task 1)
Tests all classes and functions to ensure they run properly.
"""

import sys
import numpy as np
from svg_utils import load_svg_path
from fs_redrawer import FourierEpicycles

def test_fourier_epicycles_init():
    """Test FourierEpicycles initialization"""
    print("Testing FourierEpicycles.__init__...")
    try:
        t, z = load_svg_path("svgs/heart.svg", num_points=1000)
        fs = FourierEpicycles(t, z, n_harmonics=50)
        
        assert fs.t is not None
        assert fs.signal is not None
        assert fs.N == 50
        assert fs.T == 2 * np.pi
        assert fs.omega == 2 * np.pi / fs.T
        assert len(fs.coeffs) == 0
        print("  ✓ __init__ works correctly")
        return fs, t, z
    except Exception as e:
        print(f"  ✗ __init__ failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def test_calculate_cn(fs):
    """Test calculate_cn method"""
    print("Testing calculate_cn...")
    try:
        c0 = fs.calculate_cn(0)
        assert isinstance(c0, complex)
        assert np.isfinite(c0.real) and np.isfinite(c0.imag)
        
        c1 = fs.calculate_cn(1)
        assert isinstance(c1, complex)
        assert np.isfinite(c1.real) and np.isfinite(c1.imag)
        
        cn = fs.calculate_cn(-1)
        assert isinstance(cn, complex)
        print("  ✓ calculate_cn works correctly")
    except Exception as e:
        print(f"  ✗ calculate_cn failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def test_calculate_all_coefficients(fs):
    """Test calculate_all_coefficients method"""
    print("Testing calculate_all_coefficients...")
    try:
        fs.calculate_all_coefficients()
        assert len(fs.coeffs) == 2 * fs.N + 1
        
        for n in range(-fs.N, fs.N + 1):
            assert n in fs.coeffs
            assert isinstance(fs.coeffs[n], complex)
            assert np.isfinite(fs.coeffs[n].real) and np.isfinite(fs.coeffs[n].imag)
        
        print("  ✓ calculate_all_coefficients works correctly")
    except Exception as e:
        print(f"  ✗ calculate_all_coefficients failed: {e}")
        sys.exit(1)

def test_approximate(fs, t):
    """Test approximate method"""
    print("Testing approximate...")
    try:
        # Test with single time
        z_single = fs.approximate(1.5)
        # Check if it's complex-like (handles both numpy scalar and Python complex)
        assert hasattr(z_single, 'real') and hasattr(z_single, 'imag')
        assert np.isfinite(z_single.real) and np.isfinite(z_single.imag)
        
        # Test with array of times
        z_array = fs.approximate(t)
        assert z_array.shape == t.shape
        assert np.isfinite(z_array).all()
        
        print("  ✓ approximate works correctly")
    except Exception as e:
        print(f"  ✗ approximate failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def test_prune_harmonics_by_energy(fs):
    """Test prune_harmonics_by_energy method"""
    print("Testing prune_harmonics_by_energy...")
    try:
        # Create a fresh copy
        t, z = load_svg_path("svgs/heart.svg", num_points=1000)
        fs_test = FourierEpicycles(t, z, n_harmonics=50)
        fs_test.calculate_all_coefficients()
        
        n_kept, ratio = fs_test.prune_harmonics_by_energy(0.95)
        assert n_kept > 0
        assert 0 <= ratio <= 1.0
        
        print("  ✓ prune_harmonics_by_energy works correctly")
    except Exception as e:
        print(f"  ✗ prune_harmonics_by_energy failed: {e}")
        sys.exit(1)

def test_evaluate_reconstruction_error(fs, z):
    """Test evaluate_reconstruction_error method"""
    print("Testing evaluate_reconstruction_error...")
    try:
        mse = fs.evaluate_reconstruction_error()
        assert np.isfinite(mse)
        assert mse >= 0
        
        print("  ✓ evaluate_reconstruction_error works correctly")
    except Exception as e:
        print(f"  ✗ evaluate_reconstruction_error failed: {e}")
        sys.exit(1)

def test_plot_amplitude_spectrum():
    """Test plot_amplitude_spectrum method"""
    print("Testing plot_amplitude_spectrum...")
    try:
        import matplotlib.pyplot as plt
        t, z = load_svg_path("svgs/heart.svg", num_points=1000)
        fs = FourierEpicycles(t, z, n_harmonics=50)
        fs.calculate_all_coefficients()
        
        ax = fs.plot_amplitude_spectrum()
        assert ax is not None
        plt.close('all')
        
        print("  ✓ plot_amplitude_spectrum works correctly")
    except Exception as e:
        print(f"  ✗ plot_amplitude_spectrum failed: {e}")
        sys.exit(1)

def test_zero_phase_reconstruction():
    """Test zero_phase_reconstruction method"""
    print("Testing zero_phase_reconstruction...")
    try:
        t, z = load_svg_path("svgs/heart.svg", num_points=1000)
        fs = FourierEpicycles(t, z, n_harmonics=50)
        fs.calculate_all_coefficients()
        
        zp_approx, zp_coeffs = fs.zero_phase_reconstruction()
        assert zp_approx.shape == z.shape
        assert len(zp_coeffs) == len(fs.coeffs)
        assert np.isfinite(zp_approx).all()
        
        print("  ✓ zero_phase_reconstruction works correctly")
    except Exception as e:
        print(f"  ✗ zero_phase_reconstruction failed: {e}")
        sys.exit(1)

def test_keep_symmetric_pairs_only():
    """Test keep_symmetric_pairs_only method"""
    print("Testing keep_symmetric_pairs_only...")
    try:
        t, z = load_svg_path("svgs/heart.svg", num_points=1000)
        fs = FourierEpicycles(t, z, n_harmonics=50)
        fs.calculate_all_coefficients()
        
        sym_coeffs = fs.keep_symmetric_pairs_only(k=10)
        assert len(sym_coeffs) == len(fs.coeffs)
        assert 0 in sym_coeffs  # Always keeps DC
        
        print("  ✓ keep_symmetric_pairs_only works correctly")
    except Exception as e:
        print(f"  ✗ keep_symmetric_pairs_only failed: {e}")
        sys.exit(1)

def test_perturb_phase():
    """Test perturb_phase method"""
    print("Testing perturb_phase...")
    try:
        t, z = load_svg_path("svgs/heart.svg", num_points=1000)
        fs = FourierEpicycles(t, z, n_harmonics=50)
        fs.calculate_all_coefficients()
        
        perturbed = fs.perturb_phase(phase_std=0.1, seed=42)
        assert len(perturbed) == len(fs.coeffs)
        
        # Verify magnitudes are preserved
        for n in perturbed:
            if n in fs.coeffs and fs.coeffs[n] != 0:
                orig_mag = abs(fs.coeffs[n])
                pert_mag = abs(perturbed[n])
                assert np.isclose(orig_mag, pert_mag, rtol=1e-10)
        
        print("  ✓ perturb_phase works correctly")
    except Exception as e:
        print(f"  ✗ perturb_phase failed: {e}")
        sys.exit(1)

def test_even_odd_split():
    """Test even_odd_split method"""
    print("Testing even_odd_split...")
    try:
        t, z = load_svg_path("svgs/heart.svg", num_points=1000)
        fs = FourierEpicycles(t, z, n_harmonics=50)
        fs.calculate_all_coefficients()
        
        even_td, odd_td = fs.even_odd_split()
        assert even_td.shape == z.shape
        assert odd_td.shape == z.shape
        
        # Verify decomposition
        reconstructed = even_td + odd_td
        assert np.allclose(reconstructed, z, rtol=1e-10)
        
        print("  ✓ even_odd_split works correctly")
    except Exception as e:
        print(f"  ✗ even_odd_split failed: {e}")
        sys.exit(1)

def test_prune_harmonics_by_threshold():
    """Test prune_harmonics_by_threshold method"""
    print("Testing prune_harmonics_by_threshold...")
    try:
        t, z = load_svg_path("svgs/heart.svg", num_points=1000)
        fs = FourierEpicycles(t, z, n_harmonics=50)
        fs.calculate_all_coefficients()
        
        # Find a reasonable threshold
        mags = [abs(c) for n, c in fs.coeffs.items() if n != 0]
        if mags:
            epsilon = np.median(mags)
            n_kept = fs.prune_harmonics_by_threshold(epsilon)
            assert n_kept > 0
        
        print("  ✓ prune_harmonics_by_threshold works correctly")
    except Exception as e:
        print(f"  ✗ prune_harmonics_by_threshold failed: {e}")
        sys.exit(1)

def test_practice_sets():
    """Test all practice set runners"""
    print("\nTesting Practice Set Runners...")
    try:
        from fs_redrawer import (
            run_set_c, run_set_d, run_set_j, run_set_k, 
            run_set_l, run_set_m, run_set_n
        )
        
        svg_file = "svgs/heart.svg"
        
        # Test setC
        print("  Testing setC...", end=" ")
        try:
            run_set_c(svg_file, n_harmonics=50)
            print("✓")
        except Exception as e:
            print(f"✗ ({e})")
            raise
        
        # Test setD
        print("  Testing setD...", end=" ")
        try:
            run_set_d(svg_file, n_harmonics=50)
            print("✓")
        except Exception as e:
            print(f"✗ ({e})")
            raise
        
        # Test setJ
        print("  Testing setJ...", end=" ")
        try:
            run_set_j()
            print("✓")
        except Exception as e:
            print(f"✗ ({e})")
            raise
        
        # Test setK
        print("  Testing setK...", end=" ")
        try:
            run_set_k(svg_file, n_harmonics=50)
            print("✓")
        except Exception as e:
            print(f"✗ ({e})")
            raise
        
        # Test setL
        print("  Testing setL...", end=" ")
        try:
            run_set_l(svg_file)
            print("✓")
        except Exception as e:
            print(f"✗ ({e})")
            raise
        
        # Test setM
        print("  Testing setM...", end=" ")
        try:
            run_set_m(svg_file, n_harmonics=50)
            print("✓")
        except Exception as e:
            print(f"✗ ({e})")
            raise
        
        # Test setN
        print("  Testing setN...", end=" ")
        try:
            run_set_n(svg_file, n_harmonics=50)
            print("✓")
        except Exception as e:
            print(f"✗ ({e})")
            raise
        
    except Exception as e:
        print(f"\n  ✗ Practice set runners failed: {e}")
        sys.exit(1)

def test_main_pipeline():
    """Test the main pipeline (default usage)"""
    print("\nTesting main pipeline (default usage)...")
    try:
        from epicycle_animation import save_outputs
        
        t, z = load_svg_path("svgs/heart.svg", num_points=1000)
        fs = FourierEpicycles(t, z, n_harmonics=80)
        fs.calculate_all_coefficients()
        
        save_outputs(fs, z, "test_heart_comparison.png", "test_heart_epicycles.gif", num_frames=120, fps=15)
        
        print("  ✓ Main pipeline works correctly")
    except Exception as e:
        print(f"  ✗ Main pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("Task 1 (fs_redrawer.py) - Comprehensive Test Suite")
    print("=" * 60)
    
    # Test basic functionality
    fs, t, z = test_fourier_epicycles_init()
    test_calculate_cn(fs)
    test_calculate_all_coefficients(fs)
    test_approximate(fs, t)
    test_prune_harmonics_by_energy(fs)
    test_evaluate_reconstruction_error(fs, z)
    test_plot_amplitude_spectrum()
    test_zero_phase_reconstruction()
    test_keep_symmetric_pairs_only()
    test_perturb_phase()
    test_even_odd_split()
    test_prune_harmonics_by_threshold()
    
    # Test practice sets
    test_practice_sets()
    
    # Test main pipeline
    test_main_pipeline()
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
