"""
practice_template.py -- practice scaffold for CSE 220 DFT/FFT Practice Question Bank.

Companion code to CSE220_DFT_FFT_Practice_QuestionBank.pdf.

This file mirrors the structure of hybrid_image_template.py: it imports your
already-completed transforms.py and image_conv.py (and the provided
image_utils.py / io_utils.py / bench_utils.py), and leaves ONLY the
TODO-marked functions for you to fill in, one section per practice problem.

Do NOT modify transforms.py, image_conv.py, image_utils.py, io_utils.py, or
bench_utils.py -- exactly as in the real lab. Everything you need from them
is already imported below.

Usage: pick one problem at a time, matching the "Run:" command shown for it
in the question bank PDF, e.g.

    python3 practice_template.py p1 --image images/skyline512.png \\
        --kernel-size 15 --boost 2.5 --engine fft --out-dir outputs/p1

Each pN() function at the bottom wires up argparse for that problem only, so
you can practice one problem within its own 40-45 minute window without the
others' CLI options getting in the way.
"""

import argparse
import os
import sys

import numpy as np  # type: ignore

from bench_utils import plot_runtime_curve, time_best, timing_table_lines
from image_conv import convolve_image, inverse_2d, transform_2d
from image_utils import (load_image, make_kernel, save_comparison, save_image,
                          save_kernel_preview)
from io_utils import write_report
from transforms import (ArbitraryLengthFFT, DFTAnalyzer, FFTTransformer,
                         next_power_of_two)


def _make_engine(name):
    if name == "dft":
        return DFTAnalyzer()
    if name == "fft":
        return FFTTransformer()
    if name == "arbitrary":
        return ArbitraryLengthFFT()
    raise ValueError("unknown engine: %r" % name)


def _pad_top_left(array, shape):
    result = np.zeros(shape, dtype=np.complex128)
    result[:array.shape[0], :array.shape[1]] = array
    return result


def centred_delta_spectrum(transform_shape, kernel_shape):
    """Provided helper (same as the lab): DFT of an impulse at the kernel's centre."""
    height, width = transform_shape
    centre_row = kernel_shape[0] // 2
    centre_column = kernel_shape[1] // 2
    vertical = np.arange(height, dtype=np.float64)[:, np.newaxis]
    horizontal = np.arange(width, dtype=np.float64)[np.newaxis, :]
    phase = vertical * centre_row / height + horizontal * centre_column / width
    return np.exp(-2j * np.pi * phase)


def choose_transform_shape(image_shape, kernel_shape, engine):
    """Provided helper (same as the lab). Reuse this in any problem below."""
    full_height = image_shape[0] + kernel_shape[0] - 1
    full_width = image_shape[1] + kernel_shape[1] - 1
    if engine.name == "fft":
        return next_power_of_two(full_height), next_power_of_two(full_width)
    return full_height, full_width


def _dispatch_planes(fn, image, *args, **kwargs):
    """Small helper: run a single-plane function on grayscale or RGB input."""
    image = np.asarray(image, dtype=np.float64)
    if image.ndim == 2:
        return fn(image, *args, **kwargs)
    if image.ndim == 3 and image.shape[2] == 3:
        planes = [fn(image[:, :, c], *args, **kwargs) for c in range(3)]
        return np.stack(planes, axis=-1)
    raise ValueError("images must be grayscale or RGB")


# ===========================================================================
# Problem 1 -- High-boost sharpening
# ===========================================================================
def sharpen_plane(plane, kernel, boost, engine):
    """
    TODO (P1): build Y = X*(boost*Delta - (boost-1)*G) in the frequency
    domain, inverse-transform once, take the real part, and crop back to
    plane.shape using the same kernel-centre offset as the lab's hybrid_plane.
    """
    plane = np.asarray(plane, dtype=np.float64)
    kernel = np.asarray(kernel, dtype=np.float64)
    shape = choose_transform_shape(plane.shape, kernel.shape, engine)
    image_spectrum = transform_2d(_pad_top_left(plane, shape), engine)
    kernel_spectrum = transform_2d(_pad_top_left(kernel, shape), engine)
    delta_spectrum = centred_delta_spectrum(shape, kernel.shape)
    combined = image_spectrum * (
        boost * delta_spectrum - (boost - 1.0) * kernel_spectrum
    )
    full = inverse_2d(combined, engine).real
    row, column = kernel.shape[0] // 2, kernel.shape[1] // 2
    return full[row:row + plane.shape[0], column:column + plane.shape[1]]


def sharpen_image(image, kernel, boost, engine):
    """Apply high-boost sharpening independently to each image plane."""
    return _dispatch_planes(sharpen_plane, image, kernel, boost, engine)


def run_p1(args):
    engine = _make_engine(args.engine)
    image = load_image(args.image, as_gray=True)
    kernel = make_kernel("gaussian", size=args.kernel_size)
    result = sharpen_image(image, kernel, args.boost, engine)

    blurred = convolve_image(image, kernel, engine)
    reference = blurred + args.boost * (image - blurred)   # low-pass + boost*(residual)
    err = float(np.max(np.abs(result - reference)))
    verdict = "MATCH" if err <= 1e-9 else "MISMATCH"

    os.makedirs(args.out_dir, exist_ok=True)
    save_image(result, os.path.join(args.out_dir, "sharpened.png"))
    save_comparison([image, result], ["original", "sharpened"],
                     os.path.join(args.out_dir, "comparison.png"))
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P1 -- high-boost sharpening",
        "image     : %s" % args.image,
        "kernel    : gaussian %d x %d" % (args.kernel_size, args.kernel_size),
        "boost     : %.3f" % args.boost,
        "engine    : %s" % args.engine,
        "max error : %.3e" % err,
        "verification: %s" % verdict,
    ])
    print("verification:", verdict, "(max error %.3e)" % err)


# ===========================================================================
# Problem 2 -- Ring band-pass mask
# ===========================================================================
def _signed_frequency_indices(n):
    """u for a single axis, wrap-around convention: k for k<=n//2, k-n after."""
    idx = np.arange(n, dtype=np.float64)
    return np.where(idx > n // 2, idx - n, idx)


def frequency_grid(shape):
    """
    TODO (P2): return a 2D array of shape `shape` giving the radial
    frequency magnitude sqrt(u^2 + v^2) at every bin, where u, v follow the
    DFT's own wrap-around index convention (index k represents frequency k
    for k <= N/2 and k-N for k > N/2). _signed_frequency_indices(n) above
    already gives you the signed index for a single axis -- combine it for
    both axes into a 2D grid via broadcasting.
    """
    height, width = shape
    vertical = _signed_frequency_indices(height)[:, np.newaxis]
    horizontal = _signed_frequency_indices(width)[np.newaxis, :]
    return np.sqrt(vertical ** 2 + horizontal ** 2)


def bandpass_mask(shape, r_low, r_high):
    """TODO (P2): boolean array, True where r_low <= radius <= r_high."""
    radius = frequency_grid(shape)
    return (r_low <= radius) & (radius <= r_high)


def bandpass_plane(plane, r_low, r_high, engine):
    """Transform a plane and retain a radial frequency ring."""
    plane = np.asarray(plane, dtype=np.float64)
    height, width = plane.shape
    shape = ((next_power_of_two(height), next_power_of_two(width))
             if engine.name == "fft" else (height, width))
    spectrum = transform_2d(_pad_top_left(plane, shape), engine)
    filtered = spectrum * bandpass_mask(shape, r_low, r_high)
    return inverse_2d(filtered, engine).real[:height, :width]


def run_p2(args):
    engine = _make_engine(args.engine)
    image = load_image(args.image, as_gray=True)
    result = bandpass_plane(image, args.r_low, args.r_high, engine)
    os.makedirs(args.out_dir, exist_ok=True)
    save_image(np.clip(result, 0.0, 1.0), os.path.join(args.out_dir, "bandpassed.png"))
    save_comparison([image, np.clip(result, 0.0, 1.0)], ["original", "band-passed"],
                     os.path.join(args.out_dir, "comparison.png"))
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P2 -- ring band-pass filter",
        "image  : %s" % args.image, "r_low  : %s" % args.r_low,
        "r_high : %s" % args.r_high, "engine : %s" % args.engine,
    ])
    print("wrote", args.out_dir)


# ===========================================================================
# Problem 3 -- Wiener deconvolution
# ===========================================================================
def wiener_deconvolve_plane(blurred, kernel, lam, engine):
    """
    TODO (P3): S_hat(f) = B(f) * conj(K(f)) / (|K(f)|^2 + lam). Pad both to
    choose_transform_shape(blurred.shape, kernel.shape, engine), transform,
    apply the formula pointwise, inverse-transform once, take the real part,
    and undo the kernel-centre crop offset (same convention as the lab).
    """
    blurred = np.asarray(blurred, dtype=np.float64)
    kernel = np.asarray(kernel, dtype=np.float64)
    shape = choose_transform_shape(blurred.shape, kernel.shape, engine)
    blurred_spectrum = transform_2d(_pad_top_left(blurred, shape), engine)
    kernel_spectrum = transform_2d(_pad_top_left(kernel, shape), engine)
    estimate = blurred_spectrum * np.conj(kernel_spectrum) / (
        np.abs(kernel_spectrum) ** 2 + lam
    )
    full = inverse_2d(estimate, engine).real
    row, column = kernel.shape[0] // 2, kernel.shape[1] // 2
    return full[row:row + blurred.shape[0], column:column + blurred.shape[1]]


def wiener_deconvolve_image(blurred, kernel, lam, engine):
    """TODO (P3): grayscale/RGB dispatch."""
    return _dispatch_planes(wiener_deconvolve_plane, blurred, kernel, lam, engine)


def run_p3(args):
    engine = _make_engine(args.engine)
    blurred = load_image(args.blurred, as_gray=True)
    kernel = make_kernel("gaussian", size=args.kernel_size)
    result = wiener_deconvolve_image(blurred, kernel, args.lam, engine)
    os.makedirs(args.out_dir, exist_ok=True)
    save_image(np.clip(result, 0.0, 1.0), os.path.join(args.out_dir, "deblurred.png"))
    save_comparison([blurred, np.clip(result, 0.0, 1.0)], ["blurred input", "deblurred"],
                     os.path.join(args.out_dir, "comparison.png"))
    print("wrote", args.out_dir, "(compare visually / RMSE against your own held-out source)")


# ===========================================================================
# Problem 4 -- FFT template matching
# ===========================================================================
def choose_correlation_shape(image_shape, template_shape, engine):
    """TODO (P4): same linear + power-of-two rule as choose_transform_shape."""
    full_height = image_shape[0] + template_shape[0] - 1
    full_width = image_shape[1] + template_shape[1] - 1
    if engine.name == "fft":
        return next_power_of_two(full_height), next_power_of_two(full_width)
    return full_height, full_width


def cross_correlate_plane(image_plane, template_plane, engine):
    """
    Correlate at a padded shape and return only valid template positions.
    """
    image_plane = np.asarray(image_plane, dtype=np.float64)
    template_plane = np.asarray(template_plane, dtype=np.float64)
    height, width = image_plane.shape
    template_height, template_width = template_plane.shape
    if template_height > height or template_width > width:
        raise ValueError("template must fit inside the image")
    shape = choose_correlation_shape(
        image_plane.shape, template_plane.shape, engine
    )
    image_spectrum = transform_2d(_pad_top_left(image_plane, shape), engine)
    template_spectrum = transform_2d(_pad_top_left(template_plane, shape), engine)
    full = inverse_2d(
        image_spectrum * np.conj(template_spectrum), engine
    ).real
    return full[:height - template_height + 1,
                :width - template_width + 1]


def best_match_location(corr_surface):
    """TODO (P4): return (row, col) of the maximum value as plain ints."""
    row, column = np.unravel_index(np.argmax(corr_surface), corr_surface.shape)
    return int(row), int(column)


def run_p4(args):
    engine = _make_engine(args.engine)
    image = load_image(args.image, as_gray=True)
    template = load_image(args.template, as_gray=True)
    corr = cross_correlate_plane(image, template, engine)
    loc = best_match_location(corr)
    os.makedirs(args.out_dir, exist_ok=True)
    save_kernel_preview(corr / (np.max(np.abs(corr)) + 1e-12),
                         os.path.join(args.out_dir, "correlation.png"), title="correlation surface")
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P4 -- FFT template matching",
        "image    : %s" % args.image, "template : %s" % args.template,
        "engine   : %s" % args.engine, "best match (row, col): %s" % (loc,),
    ])
    print("best match at", loc)


# ===========================================================================
# Problem 5 -- Three-way multi-focus fusion
# ===========================================================================
def _pad_at_offset(array, shape, dr, dc):
    """Zero-pad `array` into a complex array of `shape`, anchored at (dr, dc)
    instead of the top-left corner. Provided -- useful when your two kernels
    have different sizes and can't both be anchored at (0, 0)."""
    result = np.zeros(shape, dtype=np.complex128)
    result[dr:dr + array.shape[0], dc:dc + array.shape[1]] = array
    return result


def trifocal_plane(a_plane, b_plane, c_plane, kernel1, kernel2, engine):
    """
    TODO (P5): Y = A*G1 + B*(G2-G1) + C*(Delta-G2). Pad every operand to the
    shape sized for the LARGER of kernel1 / kernel2. Watch out: G1 and G2
    must each be placed so that THEIR OWN centre lands on the *same*
    absolute anchor point inside the padded array (the larger kernel's
    centre) -- top-left placement (as in the lab, where kernel and Delta
    share one size) is only valid when every term shares one kernel size.
    _pad_at_offset is provided for exactly this.
    """
    a_plane=np.asarray(a_plane,dtype=np.float64)
    b_plane=np.asarray(b_plane,dtype=np.float64)
    c_plane=np.asarray(c_plane,dtype=np.float64)
    
    larger_kernel=(max(kernel1.shape[0],kernel2.shape[0]),
                            max(kernel1.shape[1],kernel2.shape[1]))
    shape=choose_transform_shape(a_plane.shape,larger_kernel,engine)
    
    anchor_r,anchor_c=larger_kernel[0]//2,larger_kernel[1]//2
    k1_r,k1_c=kernel1.shape[0]//2,kernel1.shape[1]//2
    k2_r,k2_c=kernel2.shape[0]//2,kernel2.shape[1]//2
    
    A=transform_2d(_pad_top_left(a_plane,shape),engine)
    B=transform_2d(_pad_top_left(b_plane,shape),engine)
    C=transform_2d(_pad_top_left(c_plane,shape),engine)
    
    G1 = transform_2d(_pad_at_offset(kernel1, shape, anchor_r - k1_r, anchor_c - k1_c), engine)
    G2 = transform_2d(_pad_at_offset(kernel2, shape, anchor_r - k2_r, anchor_c - k2_c), engine)
    Delta = centred_delta_spectrum(shape, larger_kernel)
    
    Y=A*G1+B*(G2-G1)+C*(Delta-G2)
    full=inverse_2d(Y,engine).real
    
    return full[anchor_r:anchor_r + a_plane.shape[0], anchor_c:anchor_c + a_plane.shape[1]]
    


def trifocal_image(a_image, b_image, c_image, kernel1, kernel2, engine):
    """TODO (P5): grayscale/RGB dispatch, same pattern as hybrid_image."""
    a_image=np.asarray(a_image,dtype=np.float64)
    if a_image.ndim==2:
        return trifocal_plane(a_image,b_image,c_image,kernel1,kernel2,engine)
    if a_image.ndim==3 and a_image.shape[2]==3:
        planes=[
            trifocal_plane(a_image[:,:,ch],b_image[:,:,ch],c_image[:,:,ch],kernel1,kernel2,engine)
            for ch in range(3)
        ]
        return np.stack(planes,axis=-1)
    raise ValueError("images must be grayscale or RGB")


def run_p5(args):
    engine = _make_engine(args.engine)
    a = load_image(args.near, as_gray=True)
    b = load_image(args.mid, as_gray=True)
    c = load_image(args.far, as_gray=True)
    k1 = make_kernel("gaussian", size=args.kernel1_size)
    k2 = make_kernel("gaussian", size=args.kernel2_size)
    result = trifocal_image(a, b, c, k1, k2, engine)

    low = convolve_image(a, k1, engine)
    mid = convolve_image(b, k2, engine) - convolve_image(b, k1, engine)
    high = c - convolve_image(c, k2, engine)
    reference = low + mid + high
    err = float(np.max(np.abs(result - reference)))
    verdict = "MATCH" if err <= 1e-9 else "MISMATCH"

    os.makedirs(args.out_dir, exist_ok=True)
    save_image(np.clip(result, 0.0, 1.0), os.path.join(args.out_dir, "trifocal.png"))
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P5 -- three-way multi-focus fusion",
        "max error : %.3e" % err, "verification: %s" % verdict,
    ])
    print("verification:", verdict, "(max error %.3e)" % err)


# ===========================================================================
# Problem 6 -- Fourier shift theorem
# ===========================================================================
def _axis_shift_ramp(n, d):
    """
    1D phase ramp exp(-2j*pi*u*d/n) for signed frequency index u, with one
    correction: when n is even, bin n/2 (the Nyquist bin) has no distinct
    negative-frequency partner -- it is its own mirror under negation mod n.
    A real input's spectrum still must satisfy Y[-u] = conj(Y[u]) there,
    which forces that single bin's multiplier to be purely real
    (cos(pi*d) instead of the complex exp(-j*pi*d)). Skipping this special
    case leaves a residual imaginary component after the inverse transform
    that grows with the fractional part of d and corrupts round-trips.
    """
    u = _signed_frequency_indices(n)
    ramp = np.exp(-2j * np.pi * u * d / n)
    if n % 2 == 0:
        ramp[n // 2] = 1.0
    return ramp

def shift_phase_ramp(shape, dr, dc):
    """
    TODO (P6): return exp(-2j*pi*(u*dr/R + v*dc/C)) over the (R, C) grid,
    where u, v are SIGNED frequency indices using the same wrap-around
    convention as frequency_grid in P2 (index k represents frequency k for
    k <= N/2 and k-N for k > N/2).

    Trap: for an EVEN axis length n, bin n/2 (the Nyquist bin) is its own
    mirror under negation mod n -- it has no distinct negative-frequency
    partner. A real input's spectrum must still satisfy Y[-u] = conj(Y[u])
    there, which forces that one bin's multiplier to be purely real rather
    than the general complex exponential. If you skip this special case,
    single fractional shifts will pick up a small but nonzero imaginary
    residual that silently gets discarded by .real, and round-trip tests
    (shift then shift back) will show a surprisingly large error.
    """
    height, width = shape
    ramp_r = _axis_shift_ramp(height, dr).reshape(-1, 1)
    ramp_c = _axis_shift_ramp(width, dc).reshape(1, -1)
    return ramp_r * ramp_c


def shift_plane(plane, dr, dc, engine):
    """
    Transform the UN-padded plane at native shape, multiply by
    shift_phase_ramp, inverse-transform, return the real part (same shape
    as the input -- no linear-convolution padding here).
    """
    plane = np.asarray(plane, dtype=np.float64)
    X = transform_2d(plane, engine)
    ramp = shift_phase_ramp(plane.shape, dr, dc)
    return inverse_2d(X * ramp, engine).real


def shift_image(image, dr, dc, engine):
    """Grayscale/RGB dispatch."""
    return _dispatch_planes(shift_plane, image, dr, dc, engine)


def run_p6(args):
    engine = _make_engine(args.engine)
    image = load_image(args.image, as_gray=True)
    result = shift_image(image, args.dr, args.dc, engine)
    back = shift_image(result, -args.dr, -args.dc, engine)
    err = float(np.max(np.abs(back - image)))
    os.makedirs(args.out_dir, exist_ok=True)
    save_image(np.clip(result, 0.0, 1.0), os.path.join(args.out_dir, "shifted.png"))
    print("round-trip max error: %.3e (should be small, e.g. <= 1e-6)" % err)


# ===========================================================================
# Problem 7 -- Circular vs linear convolution aliasing
# ===========================================================================
def circular_convolve_plane(plane, kernel, engine):
    """
    Convolve at transform length = max(plane.shape, kernel.shape) per axis
    (no linear-convolution padding), producing a circularly-wrapped result
    cropped back to plane.shape. The kernel is centred by rolling it so its
    peak sits at the array origin (same trick as image_conv's circular
    branch), otherwise the whole picture shifts diagonally.
    """
    plane = np.asarray(plane, dtype=np.float64)
    H, W = plane.shape
    kh, kw = kernel.shape
    Nh, Nw = max(H, kh), max(W, kw)
    if engine.name == "fft":
        Nh, Nw = next_power_of_two(Nh), next_power_of_two(Nw)
 
    padded_plane = np.zeros((Nh, Nw))
    padded_plane[:H, :W] = plane
    kernel_placed = np.zeros((Nh, Nw))
    kernel_placed[:kh, :kw] = kernel
    kernel_placed = np.roll(kernel_placed, shift=(-(kh // 2), -(kw // 2)), axis=(0, 1))
 
    X = transform_2d(padded_plane, engine)
    K = transform_2d(kernel_placed, engine)
    full = inverse_2d(X * K, engine).real
    return full[:H, :W]
 
 
def linear_convolve_plane(plane, kernel, engine):
    """The lab's correct version -- reuse choose_transform_shape."""
    plane = np.asarray(plane, dtype=np.float64)
    shape = choose_transform_shape(plane.shape, kernel.shape, engine)
    X = transform_2d(_pad_top_left(plane, shape), engine)
    K = transform_2d(_pad_top_left(kernel, shape), engine)
    full = inverse_2d(X * K, engine).real
    r0, c0 = kernel.shape[0] // 2, kernel.shape[1] // 2
    return full[r0:r0 + plane.shape[0], c0:c0 + plane.shape[1]]
 
 
def aliasing_error_map(plane, kernel, engine):
    """Return |circular_convolve_plane - linear_convolve_plane| and print
    the fraction of pixels whose error exceeds 1e-3."""
    circ = circular_convolve_plane(plane, kernel, engine)
    lin = linear_convolve_plane(plane, kernel, engine)
    err = np.abs(circ - lin)
    fraction = float(np.mean(err > 1e-3))
    print("fraction of pixels with |circular-linear| > 1e-3: %.4f" % fraction)
    return err


def run_p7(args):
    engine = _make_engine(args.engine)
    image = load_image(args.image, as_gray=True)
    kernel = make_kernel("gaussian", size=args.kernel_size)
    err_map = aliasing_error_map(image, kernel, engine)
    os.makedirs(args.out_dir, exist_ok=True)
    save_kernel_preview(err_map / (np.max(err_map) + 1e-12),
                         os.path.join(args.out_dir, "aliasing_error.png"), title="|circular-linear|")
    print("wrote", args.out_dir)


# ===========================================================================
# Problem 8 -- Bluestein-only hybrid image (non-power-of-two)
# ===========================================================================
def choose_transform_shape_arbitrary(image_shape, kernel_shape):
    """Return (R+Kr-1, C+Kc-1) with NO power-of-two rounding."""
    return image_shape[0] + kernel_shape[0] - 1, image_shape[1] + kernel_shape[1] - 1
 
 
def hybrid_plane_arbitrary(low_plane, high_plane, kernel, engine):
    """
    Identical spectral combination to the lab's hybrid_plane, but on the
    minimum linear-convolution size only (never rounded to a power of two),
    and defensively requires the Bluestein engine.
    """
    if engine.name != "arbitrary":
        raise ValueError("hybrid_plane_arbitrary requires engine.name == 'arbitrary'")
 
    low_plane = np.asarray(low_plane, dtype=np.float64)
    high_plane = np.asarray(high_plane, dtype=np.float64)
    shape = choose_transform_shape_arbitrary(low_plane.shape, kernel.shape)
 
    low_spec = transform_2d(_pad_top_left(low_plane, shape), engine)
    high_spec = transform_2d(_pad_top_left(high_plane, shape), engine)
    kernel_spec = transform_2d(_pad_top_left(kernel, shape), engine)
    delta_spec = centred_delta_spectrum(shape, kernel.shape)
 
    combined = low_spec * kernel_spec + high_spec * (delta_spec - kernel_spec)
    full = inverse_2d(combined, engine).real
 
    row, col = kernel.shape[0] // 2, kernel.shape[1] // 2
    return full[row:row + low_plane.shape[0], col:col + low_plane.shape[1]]
 
 
def hybrid_image_arbitrary(low_image, high_image, kernel, engine):
    """Grayscale/RGB dispatch."""
    low_image = np.asarray(low_image, dtype=np.float64)
    if low_image.ndim == 2:
        return hybrid_plane_arbitrary(low_image, high_image, kernel, engine)
    if low_image.ndim == 3 and low_image.shape[2] == 3:
        planes = [
            hybrid_plane_arbitrary(low_image[:, :, ch], high_image[:, :, ch], kernel, engine)
            for ch in range(3)
        ]
        return np.stack(planes, axis=-1)
    raise ValueError("images must be grayscale or RGB")


def run_p8(args):
    engine = _make_engine(args.engine)
    low = load_image(args.low_image, as_gray=True)
    high = load_image(args.high_image, as_gray=True)
    kernel = make_kernel("gaussian", size=args.kernel_size)
    result = hybrid_image_arbitrary(low, high, kernel, engine)

    low_component = convolve_image(low, kernel, engine)
    high_component = high - convolve_image(high, kernel, engine)
    reference = low_component + high_component
    err = float(np.max(np.abs(result - reference)))
    verdict = "MATCH" if err <= 1e-6 else "MISMATCH"

    os.makedirs(args.out_dir, exist_ok=True)
    save_image(np.clip(result, 0.0, 1.0), os.path.join(args.out_dir, "hybrid.png"))
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P8 -- Bluestein-only hybrid image",
        "max error : %.3e" % err, "verification: %s" % verdict,
    ])
    print("verification:", verdict, "(max error %.3e)" % err)


# ===========================================================================
# Problem 9 -- Frequency-domain watermark
# ===========================================================================
def embed_watermark_plane(plane, u0, v0, amplitude, engine):
    """
    Transform plane at native size, add `amplitude` to bin (u0, v0) and add
    amplitude (conjugated -- amplitude is real here, so this is the same
    value) to the conjugate-symmetric partner bin ((-u0) % R, (-v0) % C),
    inverse-transform, return the real part. Skipping the partner bin would
    leave a nonzero imaginary residual that silently gets thrown away.
    """
    plane = np.asarray(plane, dtype=np.float64)
    R, C = plane.shape
    X = transform_2d(plane, engine).copy()
    target = X[u0, v0]
    magnitude = abs(target)
    phase = target / magnitude if magnitude else 1.0
    increment = amplitude * magnitude * phase
    X[u0, v0] += increment
    u0c, v0c = (-u0) % R, (-v0) % C
    X[u0c, v0c] += np.conj(increment)
    return inverse_2d(X, engine).real
 
 
def detect_watermark_plane(plane, u0, v0, engine):
    """Transform plane, return |X[u0, v0]| as a float."""
    plane = np.asarray(plane, dtype=np.float64)
    X = transform_2d(plane, engine)
    return float(np.abs(X[u0, v0]))
 
 
def watermark_image(image, u0, v0, amplitude, engine):
    """Grayscale/RGB dispatch for embedding."""
    return _dispatch_planes(embed_watermark_plane, image, u0, v0, amplitude, engine)


def run_p9(args):
    engine = _make_engine(args.engine)
    image = load_image(args.image, as_gray=True)
    watermarked = watermark_image(image, args.u0, args.v0, args.amplitude, engine)
    baseline = detect_watermark_plane(image, args.u0, args.v0, engine)
    detected = detect_watermark_plane(watermarked, args.u0, args.v0, engine)
    os.makedirs(args.out_dir, exist_ok=True)
    save_image(np.clip(watermarked, 0.0, 1.0), os.path.join(args.out_dir, "watermarked.png"))
    print("baseline statistic: %.4f, watermarked statistic: %.4f (want >= 5x)" % (baseline, detected))


# ===========================================================================
# Problem 10 -- 2D convolution runtime study
# ===========================================================================
DFT_SIZES_2D = [32, 48, 64, 96, 128]
FFT_SIZES_2D = [32, 64, 128, 256, 512, 1024]
ARBITRARY_SIZES_2D = [33, 65, 129, 257, 513]
TIME_BUDGET_2D = 20.0


def time_convolution(image_size, kernel_size, engine_name):
    """Time one convolve_image call at a given square image size."""
    engine = _make_engine(engine_name)
    rng = np.random.default_rng(image_size)
    plane = rng.standard_normal((image_size, image_size))
    kernel = make_kernel("gaussian", size=kernel_size)
    return time_best(lambda: convolve_image(plane, kernel, engine), repeats=2)
 
 
def run_2d_benchmark(out_dir, kernel_size=9):
    """
    Sweep image_size for 'dft', 'fft', and 'arbitrary' engines, stopping a
    sweep once a measurement exceeds TIME_BUDGET_2D, then plot and tabulate
    exactly as bigmul.py's run_benchmark does.
    """
    def measure(label, engine_name, sizes):
        xs, ys = [], []
        print("%s:" % label)
        for n in sizes:
            seconds = time_convolution(n, kernel_size, engine_name)
            xs.append(n)
            ys.append(seconds)
            print("  %8d px   %9.4f s" % (n, seconds))
            if seconds > TIME_BUDGET_2D:
                print("  (stopping this curve -- over the time budget)")
                break
        return xs, ys
 
    series = {}
    series["Naive DFT"] = measure("naive DFT", "dft", DFT_SIZES_2D)
    series["Radix-2 FFT"] = measure("radix-2 FFT", "fft", FFT_SIZES_2D)
    series["Bluestein (arbitrary)"] = measure("Bluestein", "arbitrary", ARBITRARY_SIZES_2D)
 
    os.makedirs(out_dir, exist_ok=True)
    plot_path = os.path.join(out_dir, "runtime_2dconv.png")
    plot_runtime_curve(series, plot_path,
                       title="Practice P10: 2D convolution runtime by engine",
                       xlabel="image side length N (pixels)",
                       references=("n2", "nlogn"))
    write_report(os.path.join(out_dir, "report.txt"),
                 ["Practice P10 -- 2D convolution runtime study", ""]
                 + timing_table_lines(series, size_label="N")
                 + ["", "plot: %s" % os.path.basename(plot_path)])
    print("wrote", plot_path)


def run_p10(args):
    run_2d_benchmark(args.out_dir)


# ===========================================================================
# CLI wiring -- one subcommand per problem, matching the PDF's "Run:" lines.
# ===========================================================================
def main():
    ap = argparse.ArgumentParser(description="CSE220 DFT/FFT practice scaffold")
    sub = ap.add_subparsers(dest="problem", required=True)

    p1 = sub.add_parser("p1")
    p1.add_argument("--image", required=True)
    p1.add_argument("--kernel-size", type=int, default=15)
    p1.add_argument("--boost", type=float, default=2.0)
    p1.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="fft")
    p1.add_argument("--out-dir", default="outputs/p1")
    p1.set_defaults(func=run_p1)

    p2 = sub.add_parser("p2")
    p2.add_argument("--image", required=True)
    p2.add_argument("--r-low", type=float, default=8)
    p2.add_argument("--r-high", type=float, default=40)
    p2.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="dft")
    p2.add_argument("--out-dir", default="outputs/p2")
    p2.set_defaults(func=run_p2)

    p3 = sub.add_parser("p3")
    p3.add_argument("--blurred", required=True)
    p3.add_argument("--kernel-size", type=int, default=21)
    p3.add_argument("--lam", type=float, default=1e-4)
    p3.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="fft")
    p3.add_argument("--out-dir", default="outputs/p3")
    p3.set_defaults(func=run_p3)

    p4 = sub.add_parser("p4")
    p4.add_argument("--image", required=True)
    p4.add_argument("--template", required=True)
    p4.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="fft")
    p4.add_argument("--out-dir", default="outputs/p4")
    p4.set_defaults(func=run_p4)

    p5 = sub.add_parser("p5")
    p5.add_argument("--near", required=True)
    p5.add_argument("--mid", required=True)
    p5.add_argument("--far", required=True)
    p5.add_argument("--kernel1-size", type=int, default=9)
    p5.add_argument("--kernel2-size", type=int, default=31)
    p5.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="fft")
    p5.add_argument("--out-dir", default="outputs/p5")
    p5.set_defaults(func=run_p5)

    p6 = sub.add_parser("p6")
    p6.add_argument("--image", required=True)
    p6.add_argument("--dr", type=float, default=13.5)
    p6.add_argument("--dc", type=float, default=-6.25)
    p6.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="dft")
    p6.add_argument("--out-dir", default="outputs/p6")
    p6.set_defaults(func=run_p6)

    p7 = sub.add_parser("p7")
    p7.add_argument("--image", required=True)
    p7.add_argument("--kernel-size", type=int, default=25)
    p7.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="fft")
    p7.add_argument("--out-dir", default="outputs/p7")
    p7.set_defaults(func=run_p7)

    p8 = sub.add_parser("p8")
    p8.add_argument("--low-image", required=True)
    p8.add_argument("--high-image", required=True)
    p8.add_argument("--kernel-size", type=int, default=17)
    p8.add_argument("--engine", choices=["arbitrary"], default="arbitrary")
    p8.add_argument("--out-dir", default="outputs/p8")
    p8.set_defaults(func=run_p8)

    p9 = sub.add_parser("p9")
    p9.add_argument("--image", required=True)
    p9.add_argument("--u0", type=int, default=30)
    p9.add_argument("--v0", type=int, default=47)
    p9.add_argument("--amplitude", type=float, default=4.0)
    p9.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="dft")
    p9.add_argument("--out-dir", default="outputs/p9")
    p9.set_defaults(func=run_p9)

    p10 = sub.add_parser("p10")
    p10.add_argument("--out-dir", default="outputs/p10")
    p10.set_defaults(func=run_p10)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()