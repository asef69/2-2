"""
CSE220 - LTI Systems & Convolution
MASTER PRACTICE TEMPLATE (covers every topic style seen in A1/A2 online +
the 8-problem practice set: deconvolution, cascade/parallel networks,
binomial smoothing, multi-echo superposition, polynomial division,
echo/reverb, edge detection, step-response recovery).

Rules (same as real exam):
- Use ONLY DiscreteSignal / LTISystem (extend LTISystem with new methods
  if a problem needs something it doesn't have yet, e.g. deconvolve()).
- Do NOT use numpy.convolve / scipy.signal / any built-in convolution.
- numpy is allowed for arrays/plots only. matplotlib is allowed for plots.
- Everything below is a SKELETON. Fill in every TODO yourself.
"""

import math
import numpy as np  # type: ignore
import matplotlib.pyplot as plt

from signal_lti import DiscreteSignal, LTISystem, readable_time_ticks


# =====================================================================
# SECTION 0 — Core helpers you will reuse in almost every problem
# =====================================================================

def make_signal(start_time, end_time, values):
    """Build a DiscreteSignal from a list of values placed at start..end.
    Example: make_signal(2, 4, [7, 8, 9]) -> x[2]=7, x[3]=8, x[4]=9.
    """
    # TODO: create a DiscreteSignal(start_time, end_time) and fill it in
    #       using set_value_at_time. Raise an error if lengths mismatch.
    if len(values)!=(end_time-start_time+1):
        raise ValueError("Wrong length")
    signal=DiscreteSignal(start_time,end_time)
    for t,v in zip(range(start_time,end_time+1),values):
        signal.set_value_at_time(t,v)
    return signal    


def signal_from_samples(start_time, end_time, samples):
    """Build a DiscreteSignal over [start_time, end_time]; samples is a
    dict {time_index: value}. Unspecified indices stay 0.
    """
    # TODO
    signal=DiscreteSignal(start_time,end_time)
    for t,v in samples.items():
        signal.set_value_at_time(t,v)
    return signal    


def max_absolute_difference(first_signal, second_signal):
    """Return the largest |first[n] - second[n]| over their combined
    time range. Used for every 'verify these two match' check.
    """
    # TODO
    start=min(first_signal.start_time,second_signal.start_time)
    end=max(first_signal.end_time,second_signal.end_time)
    
    max_diff=0.0
    for t in range(start,end+1):
        diff=abs(first_signal.get_value_at_time(t)-second_signal.get_value_at_time(t))
        
        if diff>max_diff:
            max_diff=diff
    
    return round(max_diff,9)        


def print_signal(signal, name):
    """Pretty-print a DiscreteSignal for a report/console output."""
    # TODO: loop signal.times(), print n and value nicely formatted
    lines=[f"{name}:"]
    for n in signal.times():
        lines.append(f"  n={n:4d} ,value={signal.get_value_at_time(n):10.4f}")
        
    return "\n".join(lines)    


# =====================================================================
# SECTION 1 — Generic LTI property testers (A1/A2 style)
#   Must work for ANY apply_system callable: DiscreteSignal -> DiscreteSignal
#   Do NOT assume apply_system is bound to an LTISystem.
# =====================================================================

def test_linearity(apply_system, x1, x2, a, b):
    """Return max| apply_system(a*x1 + b*x2) - (a*apply_system(x1) + b*apply_system(x2)) |"""
    # TODO
    lhs=apply_system(x1.multiply(a).add(x2.multiply(b)))
    rhs=apply_system(x1).multiply(a).add(apply_system(x2).multiply(b))
    
    return max_absolute_difference(lhs,rhs)


def test_time_invariance(apply_system, x, k):
    """Return max| apply_system(x shifted by k) - (apply_system(x) shifted by k) |"""
    # TODO
    lhs=apply_system(x.shift(k))
    rhs=apply_system(x).shift(k)
    return max_absolute_difference(lhs,rhs)


def system_time_varying_amplifier(input_signal):
    """Example of a NON-LTI system: y[n] = n * x[n].
    Exam variants might ask for y[n] = x[n]^2, y[n] = x[2n], y[n] = x[n] + 1, etc.
    Use only DiscreteSignal operations (no numpy arithmetic on the object itself).
    """
    # TODO
    result=DiscreteSignal(input_signal.start_time,input_signal.end_time)
    for n in result.times():
        result.set_value_at_time(n,n*input_signal.get_value_at_time(n))
        #result.set_value_at_time(n,input_signal.get_value_at_time(2n))
        #result.set_value_at_time(n,input_signal.get_value_at_time(n)*input_signal.get_value_at_time(n))
        #result.set_value_at_time(n,input_signal.get_value_at_time(n).+1)
    return result    


# =====================================================================
# SECTION 2 — Deconvolution / System Identification (Problem A / E style)
#   Extend LTISystem with a deconvolve method (monkey-patch here, or copy
#   into signal_lti.py and add as a real class method if the exam allows
#   editing that file).
# =====================================================================

def deconvolve(self, output_signal):
    """Given self.h acting as the KNOWN input x[n], and output_signal as
    y[n] = (x*h)[n], recover the unknown impulse response h[n].

    Formula (forward substitution), for causal x with x[0] != 0:
        h[n] = ( y[n] - sum_{k=0}^{n-1} x[k]*h[n-k] ) / x[0]

    Length of recovered h = len(y) - len(x) + 1.
    Returns a DiscreteSignal starting at n = 0.
    """
    # TODO: implement using only self.get_value_at_time / output_signal.get_value_at_time
    x=self.h
    x0=x.get_value_at_time(0)
    if x0==0:
        raise ValueError("x[0] must be nonzero for deconvolution")
    
    h_length=len(output_signal)-len(x)+1
    if h_length<=0:
        raise ValueError("Not Possible")
    
    h=DiscreteSignal(0,h_length-1)
    for n in range(h_length):
        total=output_signal.get_value_at_time(n)
        
        for k in range(0,n):
            total-=x.get_value_at_time(n-k)*h.get_value_at_time(k)
        h.set_value_at_time(n,total/x0)
        
    return h        


# Attach to LTISystem so you can call system.deconvolve(y) directly.
LTISystem.deconvolve = deconvolve #type:ignore


def polynomial_to_signal(coeffs_highest_first):
    """Convert polynomial coefficients (highest degree first) into a
    0-indexed causal DiscreteSignal (constant term at n=0)."""
    # TODO: reverse the list and build a DiscreteSignal starting at 0
    reversed_coeff = list(reversed(list(coeffs_highest_first)))

    return make_signal(0, len(reversed_coeff) - 1, reversed_coeff) # type: ignore


def signal_to_polynomial(signal):
    """Inverse of polynomial_to_signal: return coefficients highest-degree-first."""
    # TODO
    values=[signal.get_value_at_time(t) for t in signal.times()]
    return list(reversed(values))


# =====================================================================
# SECTION 3 — Cascade + Parallel Networks (Problem B style)
# =====================================================================

def combined_impulse_response(h1, h2, h3):
    """Network: x -> [h1] -\\
                x -> [h2] -/-> (+) -> [h3] -> y
       h_combined[n] = (h1[n] + h2[n]) * h3[n]
    """
    # TODO: use DiscreteSignal.add and LTISystem convolution
    parallel_sum=h1.add(h2)
    system=LTISystem(parallel_sum)
    return system.output(h3)


def run_network_the_long_way(x, h1, h2, h3):
    """Compute y[n] by actually simulating each stage separately."""
    # TODO: build LTISystem(h1), LTISystem(h2); run x through each,
    #       add outputs, run the sum through LTISystem(h3)
    system1=LTISystem(h1)
    system2=LTISystem(h2)
    parallel_output=system1.output(x).add(system2.output(x))
    system3=LTISystem(h3)
    return system3.output(parallel_output)


# =====================================================================
# SECTION 4 — Binomial-Weighted Smoothing (Problem C style)
# =====================================================================

def binomial_impulse_response(window_size):
    """h[k] = C(window_size-1, k) / 2^(window_size-1), k = 0..window_size-1
    Newest sample (k=0) gets weight C(n-1,0); oldest gets C(n-1,n-1).
    """
    # TODO: use math.comb; sanity check weights sum to 1.0
    n=window_size-1
    weights=[math.comb(n,k)/(2**n) for k in range(window_size)]
    assert math.isclose(sum(weights),1.0,abs_tol=1e-9),"weights must sum up to 1"
    return make_signal(0,window_size-1,weights)


def trim_partial_window_edges(signal, window_size):
    """Return only the 'fully overlapped' output samples, dropping the
    same (window_size - 1) values from each end that a plain moving
    average would also have to drop."""
    # TODO
    new_start=signal.start_time+window_size-1
    new_end=signal.end_time-window_size+1
    new_signal=DiscreteSignal(new_start,new_end)
    for t in new_signal.times():
        new_signal.set_value_at_time(t,signal.get_value_at_time(t))
    return new_signal    


# =====================================================================
# SECTION 5 — Multi-Echo Superposition (Problem D style)
# =====================================================================

class Supersignal:
    """Holds several DiscreteSignal components, each at its own time range."""

    def __init__(self, components):
        # TODO: store the list of DiscreteSignal components
        self.components=list(components)

    def combined_input(self):
        """Sum all components into one DiscreteSignal (fold with .add())."""
        # TODO
        first=self.components[0]
        new_signal=DiscreteSignal(first.start_time,first.end_time)
        new_signal.values=list(first.values)
        for component in self.components[1:]:
            new_signal=new_signal.add(component)
        return new_signal    


def output_super_via_combined_input(system, supersignal):
    """Method 1: sum the components first, then convolve once."""
    # TODO
    combined=supersignal.combined_input()
    return system.output(combined)


def output_super_via_per_component_sum(system, supersignal):
    """Method 2: convolve each component separately, then add the outputs."""
    # TODO
    outputs=[system.output(component) for component in supersignal.components]
    result=outputs[0]
    for output in outputs[1:]:
        result=result.add(output)
    return result    


# =====================================================================
# SECTION 6 — Digital Echo / Reverb (Problem F style, sparse impulse response)
# =====================================================================

def echo_impulse_response(delay_D, alpha):
    """h[n] = delta[n] + alpha*delta[n-D] + alpha^2*delta[n-2D]
    Build as a DiscreteSignal of length 2*D + 1, mostly zeros.
    """
    # TODO
    length=2*delay_D+1
    h=DiscreteSignal(0,length-1)
    h.set_value_at_time(0,1.0)
    h.set_value_at_time(delay_D,alpha)
    h.set_value_at_time(2*delay_D,alpha**2)
    return h

# =====================================================================
# SECTION 7 — 1-D Edge Detector (Problem G style)
# =====================================================================

def first_difference_impulse():
    """h[0] = 1, h[1] = -1  (built-in filter reused from Offline 1)."""
    # TODO
    return make_signal(0,1,[1.0,-1.0])


def detect_edges(output_signal, threshold):
    """Return the list of time indices n where |y[n]| > threshold."""
    # TODO
    return [n for n in output_signal.times() if abs(output_signal.get_value_at_time(n))>threshold]


# =====================================================================
# SECTION 8 — Step Response Recovery (Problem H style)
# =====================================================================

def step_response_cumulative_sum(h,end_n=None):
    """Method 1: s[n] = s[n-1] + h[n], no convolution at all.
    Choose a sensible output range yourself (e.g. h.start_time .. some N)."""
    # TODO
    start_n=h.start_time
    if end_n is None:
        end_n=h.end_time+5    
    s=DiscreteSignal(start_n,end_n)
    running_sum=0.0
    for n in range(start_n,end_n+1):
        running_sum+=h.get_value_at_time(n)
        s.set_value_at_time(n,running_sum)
    return s    


def step_response_via_truncated_convolution(h, U):
    """Method 2: build u[n] = 1 for n in [0, U] (finite truncation of the
    unit step) and compute s2 = (h * u) via LTISystem. Explain in your
    report why this becomes wrong for n close to U."""
    # TODO
    u=DiscreteSignal(0,U)
    u.values=[1.0]*(U+1)
    system=LTISystem(h)
    return system.output(u)


# =====================================================================
# SECTION 8b — Output from Step Response (new assignment style)
#   Given only s[n] (the step response of an LTI system), compute the
#   output y[n] for ANY input x[n] WITHOUT ever explicitly building h[n]
#   the "normal" way -- use the identities:
#     h[n]  = s[n]  - s[n-1]      (s[-1] = 0)
#     dx[n] = x[n]  - x[n-1]      (x[-1] = 0)
#     y[n]  = (dx * s)[n]
# =====================================================================


# =====================================================================
# SECTION 8b — Output of an LTI System Given Only Its Step Response s[n]
#   Identities:
#     h[n]      = s[n] - s[n-1]        (s[-1] = 0)
#     dx[n]     = x[n] - x[n-1]        (x[-1] = 0)
#     y[n]      = (dx * s)[n]
#   i.e. you never need to explicitly build h[n] to get y[n]: convolving
#   the FIRST DIFFERENCE of the input directly with the STEP RESPONSE
#   gives the same output as convolving x[n] with h[n] would.
# =====================================================================

def first_difference_of_signal(x):
    """dx[n] = x[n] - x[n-1], with any sample outside x's stored range
    treated as 0 (this is exactly x[-1] = 0 from the assignment, applied
    consistently at BOTH ends).

    IMPORTANT: the output must span one extra sample on the LEFT (to
    capture the leading edge x[start] - 0) AND one extra sample on the
    RIGHT (to capture the trailing edge 0 - x[end], since x implicitly
    drops back to 0 right after its stored range). Only extending the
    left side is a common bug -- it silently breaks the y[n] = (dx*s)[n]
    identity for any n past x's original range.
    """
    dx = DiscreteSignal(x.start_time - 1, x.end_time + 1)
    for n in dx.times():
        current = x.get_value_at_time(n)
        previous = x.get_value_at_time(n - 1)
        dx.set_value_at_time(n, current - previous)
    return dx


def impulse_response_from_step(s):
    """h[n] = s[n] - s[n-1], with s[-1] treated as 0.
    Recovers the impulse response purely from the step response --
    this is just first_difference_of_signal applied to s."""
    return first_difference_of_signal(s)


def output_from_step_response(step_response, input_signal):
    """Compute y[n] for ANY input x[n], given only the system's step
    response s[n] -- without ever explicitly forming h[n].

    y[n] = (dx * s)[n], where dx[n] = x[n] - x[n-1].

    Implemented with LTISystem: treat s as the impulse response of an
    LTI system and convolve it with dx.
    """
    dx = first_difference_of_signal(input_signal)
    system = LTISystem(step_response)
    return system.output(dx)


def output_from_step_response_via_h(step_response, input_signal):
    """Cross-check path: explicitly recover h[n] = s[n]-s[n-1] first,
    then run the ORIGINAL x[n] (not dx) through LTISystem(h). Should
    match output_from_step_response(...) exactly."""
    h = impulse_response_from_step(step_response)
    system = LTISystem(h)
    return system.output(input_signal)


# =====================================================================
# SECTION 8c — Causality and BIBO Stability of an LTI System
#   Causal:  h[n] = 0 for all n < 0   <=>   h.start_time >= 0
#   BIBO stable:  sum_{n=-inf}^{inf} |h[n]| < infinity
#   Since every DiscreteSignal here is FINITE-length by construction,
#   the absolute sum is automatically finite (a finite sum of finite
#   numbers can't diverge) -- so any DiscreteSignal-based h[n] you build
#   in this course is always BIBO stable. The check is still worth
#   coding explicitly: (a) it generalizes correctly if you ever extend
#   DiscreteSignal to represent a truncated/periodic infinite signal,
#   and (b) it is exactly what the exam will ask you to justify in
#   words even when the numeric answer is "trivially yes".
# =====================================================================

def is_causal(h):
    """A discrete-time LTI system with impulse response h[n] is causal
    iff h[n] = 0 for every n < 0. For our DiscreteSignal representation
    this is simply h.start_time >= 0 (nothing is stored before n=0)."""
    if h.start_time >= 0:
        return True
    # start_time < 0 is still causal if every sample before n=0 happens
    # to be (numerically) zero -- check explicitly rather than assuming.
    for n in range(h.start_time, 0):
        if abs(h.get_value_at_time(n)) > 1e-12:
            return False
    return True


def bibo_stability_sum(h):
    """Return sum_n |h[n]| over the signal's stored range.
    This is the quantity the BIBO-stability test compares to infinity."""
    return sum(abs(value) for value in h.values)


def is_stable(h, tolerance=1e12):
    """BIBO stability check: sum |h[n]| < infinity.
    Every finite-length DiscreteSignal has a finite sum by construction,
    so this will always return True for well-formed input; `tolerance`
    exists only to flag pathological/overflow values (e.g. NaN or huge
    blown-up coefficients), which would otherwise silently look "stable"."""
    total = bibo_stability_sum(h)
    if math.isnan(total) or math.isinf(total):
        return False
    return total < tolerance


def describe_causality_and_stability(h, name="h[n]"):
    """Convenience report combining both checks, exam-report style."""
    causal = is_causal(h)
    stable = is_stable(h)
    total_abs = bibo_stability_sum(h)
    lines = [
        f"{name}: n = {h.start_time}..{h.end_time}",
        f"  Causal:  {causal}  (h[n] = 0 for all n < 0? {'yes' if causal else 'no'})",
        f"  Stable:  {stable}  (sum |h[n]| = {total_abs:.6f} < infinity)",
    ]
    return "\n".join(lines)


# =====================================================================
# SECTION 9 — Visualization helpers (matplotlib: plot / subplot / stem,
#             plus the grayscale color-block visualization)
# =====================================================================

def plot_three_signals_as_stems(input_signal, impulse_response, output_signal,
                                 save_path=None):
    """3 stacked stem subplots: x[n], h[n], y[n].
    Use plt.subplots(3, 1, ...) then signal.plot(title, ax=axes[i])
    (DiscreteSignal.plot already exists in signal_lti.py) OR build your
    own stem plot manually with ax.stem(...).
    """
    # TODO
    fig,axes=plt.subplots(3,1,figsize=(10,8),constrained_layout=True)
    input_signal.plot("Input Signal x[n]",ax=axes[0])
    impulse_response.plot("Impulse Response h[n]",ax=axes[1])
    output_signal.plot("Output Signal y[n]",ax=axes[2])
    
    if save_path is not None:
        fig.savefig(save_path,dpi=150)
    
    plt.close(fig)
    return save_path    
    


def normalized_grayscale_rgb(signal):
    """Map signal values to 0..255 grayscale for the color-block plot."""
    # TODO: use np.array/np.min/np.max/np.stack, same idea as Offline 1
    values=np.array(signal.values,dtype=float)
    minimum=float(np.min(values))
    maximum=float(np.max(values))
    
    if np.isclose(minimum,maximum):
        gray_values=np.full(values.shape,128,dtype=np.uint8)
    else:
        gray_values=np.round(255*(values-minimum)/(maximum-minimum))
        gray_values=gray_values.astype(np.uint8)
    
    return np.stack([gray_values,gray_values,gray_values],axis=-1)        


def plot_signal_as_color_blocks(signal, title, ax):
    """Single-row imshow visualization with white cell boundaries and
    n-value tick labels (readable_time_ticks from signal_lti helps)."""
    # TODO
    rgb_values = normalized_grayscale_rgb(signal)
    image = rgb_values.reshape(1, len(rgb_values), 3)
    time_values = list(signal.times())
    tick_labels = readable_time_ticks(time_values)
    tick_positions = [time_values.index(label) for label in tick_labels]
 
    ax.imshow(image, aspect="auto", interpolation="nearest")
    ax.set_title(title)
    ax.set_yticks([])
    ax.set_xlabel("n")
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    ax.tick_params(axis="x", labelsize=9)
 
    for boundary in range(len(signal.values) + 1):
        ax.axvline(boundary - 0.5, color="white", linewidth=0.8)


def plot_before_after_color_blocks(before_signal, after_signal, save_path=None):
    """2 stacked subplots comparing a signal before/after filtering
    (used for the edge-detector problem)."""
    # TODO
    fig, axes = plt.subplots(2, 1, figsize=(10, 3.6), constrained_layout=True)
 
    plot_signal_as_color_blocks(before_signal, "Before filtering", axes[0])
    plot_signal_as_color_blocks(after_signal, "After filtering", axes[1])
 
    if save_path is not None:
        fig.savefig(save_path, dpi=150)
    plt.close(fig)
    return save_path


# =====================================================================
# SECTION 10 — Driver / main()
#   On the real exam this reads an input file; here just wire up the
#   given sample data for whichever sub-problem you are practicing.
# =====================================================================

def main():
    tolerance = 1e-9

    # ---- Sample data (mirrors A1/A2 online) ----
    x1 = make_signal(-2, 2, [1, 0, 2, -1, 3])
    x2 = make_signal(-1, 3, [2, -3, 0, 1, 1])
    a, b = 2.0, -3.0
    k = 3
    h = make_signal(0, 2, [1.0, 0.5, 0.25])

    # TODO 1: build sys_a = LTISystem(h); test linearity & time-invariance
    #         for sys_a.output and for system_time_varying_amplifier;
    #         print all four max-diff values and state which property
    #         system_time_varying_amplifier fails.
    sys_a=LTISystem(h)
    print("System A: genuine LTI system (LTISystem.output)")
    diff_linear_a=test_linearity(sys_a.output,x1,x2,a,b)
    diff_time_a=test_time_invariance(sys_a.output,x1,k)
    print(f"  Linearity max diff:        {diff_linear_a}")
    print(f"  Time-invariance max diff:  {diff_time_a}")
    
    print("System B: y[n] = n * x[n]")
    diff_linear_b = test_linearity(system_time_varying_amplifier, x1, x2, a, b)
    diff_time_b = test_time_invariance(system_time_varying_amplifier, x1, k)
    print(f"  Linearity max diff:        {diff_linear_b}")
    print(f"  Time-invariance max diff:  {diff_time_b}")
 
    failed = []
    if diff_linear_b > tolerance:
        failed.append("Linearity")
    if diff_time_b > tolerance:
        failed.append("Time-invariance")
    print(f"  System B fails: {', '.join(failed) if failed else 'nothing (both hold)'}")
    print()

    # TODO 2: Deconvolution demo.
    #   x = make_signal(0, 2, [1, 2, -1])
    #   y = make_signal(0, 5, [2, 3, -3.5, 5, 5.5, -3])
    #   sys = LTISystem(x)
    #   recovered_h = sys.deconvolve(y)
    #   verify with output_by_superposition / output, print max diff.
    x=make_signal(0,2,[1,2,-1])
    y=make_signal(0,5,[2, 3, -3.5, 5, 5.5, -3])
    sys=LTISystem(x)
    recovered_h=sys.deconvolve(y) #type:ignore
    
    print("=" * 70)
    print("2) DECONVOLUTION (System Identification)")
    print("=" * 70)
     
    x = make_signal(0, 2, [1, 2, -1])
    y = make_signal(0, 5, [2, 3, -3.5, 5, 5.5, -3])
    dec_system = LTISystem(x)
    recovered_h = dec_system.deconvolve(y) #type:ignore
    print(print_signal(recovered_h, "Recovered h[n]"))
     
    verify_system = LTISystem(recovered_h)
    y_check = verify_system.output(x)
    print(f"  Max |y_check - y| = {max_absolute_difference(y_check, y)} (should be ~0)")
    print()

    # TODO 3: Cascade + parallel network demo (Problem B sample I/O).
    print("=" * 70)
    print("3) CASCADE + PARALLEL NETWORK")
    print("=" * 70)
 
    net_x = make_signal(-1, 4, [1, 2, 3, 4, -1, 2])
    net_h1 = make_signal(0, 2, [1, 1, 1])
    net_h2 = make_signal(0, 2, [1, 0, -1])
    net_h3 = make_signal(0, 1, [0.5, 0.5])
 
    y_long_way = run_network_the_long_way(net_x, net_h1, net_h2, net_h3)
    h_combined = combined_impulse_response(net_h1, net_h2, net_h3)
    y_via_combined = LTISystem(h_combined).output(net_x)
 
    print(print_signal(h_combined, "h_combined"))
    print(print_signal(y_long_way, "y[n] (network)"))
    print(f"  Max diff between two methods: {max_absolute_difference(y_long_way, y_via_combined)}")
    print()

    # TODO 4: Binomial smoothing demo (Problem C sample I/O).
    print("=" * 70)
    print("4) BINOMIAL-WEIGHTED SMOOTHING")
    print("=" * 70)
 
    prices = make_signal(0, 7, [4, 8, 6, 10, 14, 12, 16, 20])
    window = 4
    binom_h = binomial_impulse_response(window)
    smoothed_full = LTISystem(binom_h).output(prices)
    smoothed_trimmed = trim_partial_window_edges(smoothed_full, window)
 
    print(print_signal(binom_h, "Binomial weights h[k]"))
    print(print_signal(smoothed_trimmed, "Smoothed series (fully overlapped)"))
    print()
    

    # TODO 5: Multi-echo superposition demo (Problem D sample I/O).
    print("=" * 70)
    print("5) MULTI-ECHO SUPERPOSITION")
    print("=" * 70)
 
    echo_h = make_signal(0, 2, [1, 0.5, 0.25])
    comp1 = make_signal(-1, 1, [3, -1, 2])
    comp2 = make_signal(2, 3, [1, 1])
    comp3 = make_signal(0, 3, [-2, 4, 1, 0])
    super_signal = Supersignal([comp1, comp2, comp3])
    echo_system = LTISystem(echo_h)
 
    y_method1 = output_super_via_combined_input(echo_system, super_signal)
    y_method2 = output_super_via_per_component_sum(echo_system, super_signal)
 
    print(print_signal(super_signal.combined_input(), "Combined input x[n]"))
    print(print_signal(y_method1, "y[n] via combined input"))
    print(f"  Max diff between the two methods: {max_absolute_difference(y_method1, y_method2)}")
    print()

    # TODO 6: Polynomial long division demo (Problem E sample I/O).
    print("=" * 70)
    print("6) POLYNOMIAL LONG DIVISION VIA DECONVOLUTION")
    print("=" * 70)
 
    dividend_coeffs = [2, 3, 1, 6]
    divisor_coeffs = [1, 2]
 
    dividend_signal = polynomial_to_signal(dividend_coeffs)
    divisor_signal = polynomial_to_signal(divisor_coeffs)
 
    poly_system = LTISystem(divisor_signal)
    quotient_signal = poly_system.deconvolve(dividend_signal) #type:ignore
    quotient_coeffs = signal_to_polynomial(quotient_signal)
 
    print(f"  Quotient degree: {len(quotient_coeffs) - 1}")
    print(f"  Quotient coefficients (highest first): {quotient_coeffs}")
 
    reconstructed = LTISystem(quotient_signal).output(divisor_signal)
    print(f"  Max diff (quotient*divisor vs dividend): "
          f"{max_absolute_difference(reconstructed, dividend_signal)}")
    print()

    # --- Extra polynomial-division test cases (sanity-check that
    #     deconvolve()/polynomial_to_signal()/signal_to_polynomial() are
    #     truly general, not just tuned to the one sample above) ---
    print("=" * 70)
    print("6b) POLYNOMIAL LONG DIVISION - EXTRA TEST CASES")
    print("=" * 70)

    extra_poly_test_cases = [
        # (dividend highest-first, divisor highest-first, description)
        ([1, 2, 1], [1, 1],
         "(x^2 + 2x + 1) / (x + 1) -> expect quotient x + 1"),
        ([2, -2, -8, 8], [2, 4],
         "(2x^3 - 2x^2 - 8x + 8) / (2x + 4) -> expect quotient x^2 - 3x + 2"),
        ([1, -3, 3, -1], [1, -1],
         "(x^3 - 3x^2 + 3x - 1) / (x - 1) -> expect quotient x^2 - 2x + 1"),
        ([6, 11, -4, -4], [3, -2],
         "(6x^3 + 11x^2 - 4x - 4) / (3x - 2) -> expect quotient 2x^2 + 5x + 2"),
    ]

    for case_number, (test_dividend, test_divisor, description) in enumerate(
        extra_poly_test_cases, start=1
    ):
        print(f"  Test case {case_number}: {description}")

        test_dividend_signal = polynomial_to_signal(test_dividend)
        test_divisor_signal = polynomial_to_signal(test_divisor)

        test_system = LTISystem(test_divisor_signal)
        test_quotient_signal = test_system.deconvolve(test_dividend_signal)  # type:ignore
        test_quotient_coeffs = signal_to_polynomial(test_quotient_signal)

        test_reconstructed = LTISystem(test_quotient_signal).output(test_divisor_signal)
        test_max_diff = max_absolute_difference(test_reconstructed, test_dividend_signal)

        print(f"    Dividend coefficients:  {test_dividend}")
        print(f"    Divisor coefficients:   {test_divisor}")
        print(f"    Quotient degree:        {len(test_quotient_coeffs) - 1}")
        print(f"    Quotient coefficients:  {test_quotient_coeffs}")
        print(f"    Max diff (verify):      {test_max_diff}")
        print()

    # TODO 7: Digital echo / reverb demo (Problem F sample I/O) + plots.
    print("=" * 70)
    print("7) DIGITAL ECHO / REVERB")
    print("=" * 70)
 
    dry_signal = make_signal(0, 9, [2, -1, 3, 0, 1, -2, 1, 0, 0, 0])
    delay_D = 3
    alpha = 0.5
    reverb_h = echo_impulse_response(delay_D, alpha)
    wet_signal = LTISystem(reverb_h).output(dry_signal)
 
    print(print_signal(reverb_h, "Echo impulse response h[n]"))
    print(print_signal(wet_signal, "Wet (echoed) signal y[n]"))
    plot_three_signals_as_stems(dry_signal, reverb_h, wet_signal, save_path="echo_stems.png")
    print("  Saved stem plot: echo_stems.png")
    print()

    # TODO 8: Edge detector demo (Problem G sample I/O) + color-block plots.
    print("=" * 70)
    print("8) 1-D EDGE DETECTOR")
    print("=" * 70)
 
    row = make_signal(0, 13, [10, 10, 10, 50, 50, 50, 50, 10, 10, 10, 10, 80, 80, 80])
    edge_h = first_difference_impulse()
    edge_y = LTISystem(edge_h).output(row)
    threshold = 30
    edges = detect_edges(edge_y, threshold)
 
    print(print_signal(edge_y, "Edge-filtered row y[n]"))
    print(f"  Edges detected at n = {edges}")
    plot_before_after_color_blocks(row, edge_y, save_path="edges_before_after.png")
    print("  Saved color-block plot: edges_before_after.png")
    print()
    # TODO 9: Step response recovery demo (Problem H sample I/O).
    print("=" * 70)
    print("9) STEP RESPONSE RECOVERY")
    print("=" * 70)
 
    step_h = make_signal(-1, 2, [3, -1, 2, 0.5])
    U = 20
 
    s_cumsum = step_response_cumulative_sum(step_h, end_n=8)
    s_conv = step_response_via_truncated_convolution(step_h, U)
 
    print(print_signal(s_cumsum, "s[n] via cumulative sum"))
    print(print_signal(s_conv, "s2[n] via truncated convolution (n=-1..8 shown for comparison)"))
 
    safe_end = 8
    diffs = []
    for n in range(step_h.start_time, safe_end + 1):
        diffs.append(abs(s_cumsum.get_value_at_time(n) - s_conv.get_value_at_time(n)))
    print(f"  Max diff over safe region [-1..{safe_end}]: {max(diffs)}")
    print("  (s2[n] would start diverging from s[n] as n approaches U="
          f"{U}, since u[n] used in Method 2 is truncated there.)")

    # TODO 10: Output from step response only (Δx * s) demo.
    print()
    print("=" * 70)
    print("10) OUTPUT FROM STEP RESPONSE ONLY  (y = Δx * s)")
    print("=" * 70)

    given_step_response = make_signal(0, 3, [1.0, 1.5, 1.75, 1.75])  # s[n]
    demo_input = make_signal(0, 3, [2, -1, 3, 1])                     # x[n]

    dx_demo = first_difference_of_signal(demo_input)
    h_from_s = impulse_response_from_step(given_step_response)

    y_via_step = output_from_step_response(given_step_response, demo_input)
    y_via_h = output_from_step_response_via_h(given_step_response, demo_input)

    print(print_signal(given_step_response, "Given step response s[n]"))
    print(print_signal(h_from_s, "Recovered h[n] = s[n] - s[n-1]"))
    print(print_signal(dx_demo, "dx[n] = x[n] - x[n-1]"))
    print(print_signal(y_via_step, "y[n] via (dx * s)"))
    print(f"  Max diff vs. running x through recovered h directly: "
          f"{max_absolute_difference(y_via_step, y_via_h)}")
    print()

    # TODO 11: Causality and stability checks.
    print("=" * 70)
    print("11) CAUSALITY AND BIBO STABILITY CHECKS")
    print("=" * 70)

    causal_stable_h = make_signal(0, 2, [1.0, 0.5, 0.25])       # causal, stable
    noncausal_h = make_signal(-2, 1, [0.3, 0.3, 1.0, -0.2])      # non-causal
    unstable_like_h = make_signal(0, 3, [1e13, 1.0, 1.0, 1.0])   # flagged by tolerance

    print(describe_causality_and_stability(causal_stable_h, "h1 (causal FIR)"))
    print()
    print(describe_causality_and_stability(noncausal_h, "h2 (nonzero for n<0)"))
    print()
    print(describe_causality_and_stability(unstable_like_h, "h3 (huge coefficient)"))


if __name__ == "__main__":
    main()