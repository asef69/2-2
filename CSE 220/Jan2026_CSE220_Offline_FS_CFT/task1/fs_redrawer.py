import numpy as np #type:ignore
import matplotlib.pyplot as plt
from svg_utils import load_svg_path
from epicycle_animation import save_outputs


class FourierEpicycles:
    def __init__(self, t, signal, n_harmonics):
        """
        Step 1: Store the sampled signal and set up everything the other
        methods will need.

        Parameters
        ----------
        t : 1D numpy array, shape (M,)
            Uniformly spaced sample times covering ONE FULL PERIOD of the
            signal, as a *closed* interval: t[0] == 0 and t[-1] == T (the
            period). This is exactly what svg_utils.load_svg_path(...)
            returns.
        signal : 1D complex numpy array, shape (M,)
            signal[i] = f(t[i]) = x(t[i]) + 1j * y(t[i]). Periodic, so
            signal[-1] == signal[0].
        n_harmonics : int (call it N)
            The series will use every integer harmonic n with
            -N <= n <= N (i.e. 2N+1 terms in total -- do not forget the
            negative harmonics).

        You must set at least the following attributes, since the rest of
        this class (and the provided plotting/animation code) expects
        them to exist:
            self.t, self.signal, self.N
            self.T      -- the period (a float)
            self.omega  -- the fundamental angular frequency, 2*pi/T
            self.coeffs -- an (initially empty) dict that will map
                           n -> c_n once calculate_all_coefficients() has
                           been called
        """
        self.t=t
        self.signal=signal
        self.N=n_harmonics
        self.T=t[-1]-t[0]
        self.omega=2*np.pi/self.T
        self.coeffs={}

    def calculate_cn(self, n):
        """
        Step 2: Compute a single complex Fourier coefficient c_n using
        numerical integration (np.trapezoid) over the stored samples
        self.t, self.signal.

            c_n = (1/T) * integral_0^T  f(t) * exp(-j*n*omega*t)  dt

        n may be zero, positive, or negative.
        """
        kernel=np.exp(-1j*n*self.omega*self.t)
        return np.trapezoid(self.signal*kernel,self.t)/self.T

    def calculate_all_coefficients(self):
        """
        Step 3: Populate self.coeffs with c_n for every harmonic
        n = -N, ..., -1, 0, 1, ..., N by repeatedly calling calculate_cn(n).
        """
        for n in range(-self.N,self.N+1):
            self.coeffs[n]=self.calculate_cn(n)

    def approximate(self, t, coeffs=None):
        """
        Step 4: Reconstruct (an approximation of) the signal at time(s) t
        from the coefficients already stored in self.coeffs:

            f_hat(t) = sum_{n=-N}^{N} c_n * exp(j*n*omega*t)

        t may be a single number or a numpy array of times -- your
        implementation must support both, since the provided
        plotting/animation code calls this both ways.

        An optional coeffs dict may be supplied to reconstruct using a
        temporary coefficient set without mutating self.coeffs.
        """
        t=np.asarray(t)
        if coeffs is None:
            coeffs = self.coeffs
        result=np.zeros_like(t,dtype=complex)
        for n,cn in coeffs.items():
            result+=cn*np.exp(1j*n*self.omega*t)
        return result
    
    def prune_harmonics_by_energy(self,r):
        energy={n: abs(c)**2 for n,c in self.coeffs.items()}
        total_energy=sum(energy.values())
        ranked_energy=sorted(energy.items(),key=lambda kv:kv[1],reverse=True)

        cumulative=0.0
        keep=set()
        for n,e in ranked_energy:
            keep.add(n)
            cumulative += e
            if cumulative >= (r * total_energy):
                break

        for n in list(self.coeffs.keys()):
            if n not in keep:
                self.coeffs[n] = 0j

        actual_ratio = cumulative / total_energy if total_energy > 0 else 1.0
        num_retained = sum(1 for c in self.coeffs.values() if c != 0)
        return num_retained, actual_ratio
    
    def evaluate_reconstruction_error(self):
        approx=self.approximate(self.t)
        
        return np.mean(np.abs(self.signal-approx)**2)            
    
    def plot_amplitude_spectrum(self,ax=None):
        ns=sorted(self.coeffs.keys())
        amps=[abs(self.coeffs[n]) for n in ns]
        if ax is None:
            fig,ax=plt.subplots(figsize=(6,4))
            
        ax.stem(ns,amps)
        ax.set_yscale('log')
        ax.set_xlabel('harmonic n')
        ax.set_ylabel('|c_n| log scaled')
        return ax
    
    def zero_phase_reconstruction(self):
        zp_coeffs={n:complex(abs(c)) for n,c in self.coeffs.items()}
        approx = self.approximate(self.t, coeffs=zp_coeffs)
        return approx, zp_coeffs
    
    def keep_symmetric_pairs_only(self,k):
        pair_energy={}
        for n in self.coeffs:
            if n<=0:
                continue
            pair_energy[n]=abs(self.coeffs[n])**2+abs(self.coeffs.get(-n,0))**2
            
        top_pairs=sorted(pair_energy.items(),key=lambda kv:kv[1],reverse=True)
        keep_n={0}
        for n,_ in top_pairs:
            keep_n.add(n)
            keep_n.add(-n)
            
        filtered={n:(c if n in keep_n else 0j) for n,c in self.coeffs.items()}
        return filtered        
    def perturb_phase(self,phase_std,seed=0):
        rng=np.random.default_rng(seed)
        perturbed={}
        for n,c in self.coeffs.items():
            noise=rng.normal(0,phase_std)
            perturbed[n]=abs(c)*np.exp(1j*(np.angle(c)+noise))
            
        return perturbed   
    def even_odd_split(self):
        signal_flipped=self.signal[::-1]
        signal_even=(self.signal+signal_flipped)/2
        signal_odd=(self.signal-signal_flipped)/2
        return signal_even,signal_odd
    
    def prune_harmonics_by_threshold(self,epsilon):
        kept=0
        for n in list(self.coeffs.keys()):
            if n==0 or abs(self.coeffs[n])>=epsilon:
                kept+=1
            else:
                self.coeffs[n]=0j
        return kept            

# =====================================================
# Practice Set C: Energy-Preserving Harmonic Pruning + Amplitude Spectrum
# Usage: python3 fs_redrawer.py setC <path_to_svg> [n_harmonics]
# =====================================================
def run_set_c(svg_path, n_harmonics=150):
    import matplotlib.pyplot as plt
 
    t, z = load_svg_path(svg_path, num_points=1000)
 
    fs_full = FourierEpicycles(t, z, n_harmonics=n_harmonics)
    fs_full.calculate_all_coefficients()
    fs_full.plot_amplitude_spectrum()
    plt.tight_layout()
    plt.savefig("heart_amplitude_spectrum.png")
    plt.close()
 
    target_ratios = [0.96, 0.98, 0.99, 1.00]
    print(f"{'Target Ratio':13s} | {'Harmonics Retained':18s} | {'Actual Energy Ratio':20s} | MSE")
    print("-" * 68)
    for r in target_ratios:
        fs = FourierEpicycles(t, z, n_harmonics=n_harmonics)
        fs.calculate_all_coefficients()
        n_kept, actual_ratio = fs.prune_harmonics_by_energy(r)
        mse = fs.evaluate_reconstruction_error()
        print(f"{r:13.2f} | {n_kept:18d} | {actual_ratio:20.4f} | {mse:.6e}")
 
        approx = fs.approximate(t)
        plt.figure(figsize=(4, 4))
        plt.plot(z.real, z.imag, label="original")
        plt.plot(approx.real, approx.imag, "--", label=f"r={r}")
        plt.axis("equal")
        plt.legend()
        plt.savefig(f"heart_pruned_{r}.png")
        plt.close()
 
    sweep_ratios = np.linspace(0.80, 1.00, 8)
    counts, mses = [], []
    for r in sweep_ratios:
        fs = FourierEpicycles(t, z, n_harmonics=n_harmonics)
        fs.calculate_all_coefficients()
        n_kept, _ = fs.prune_harmonics_by_energy(r)
        counts.append(n_kept)
        mses.append(fs.evaluate_reconstruction_error())
 
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(sweep_ratios, counts, marker='o')
    axes[0].set_xlabel('target ratio r')
    axes[0].set_ylabel('harmonics retained')
    axes[1].plot(sweep_ratios, mses, marker='o')
    axes[1].set_yscale('log')
    axes[1].set_xlabel('target ratio r')
    axes[1].set_ylabel('MSE (log)')
    fig.tight_layout()
    fig.savefig("heart_compression_tradeoff.png")
    print("Saved heart_amplitude_spectrum.png, heart_pruned_{r}.png x4, heart_compression_tradeoff.png")
 
 
# =====================================================
# Practice Set D: Phase-Zeroed Reconstruction &
# Symmetric-Harmonic Filtering
# Usage: python3 fs_redrawer.py setD <path_to_svg> [n_harmonics]
# =====================================================
def run_set_d(svg_path, n_harmonics=150):
    import matplotlib.pyplot as plt
 
    t, z = load_svg_path(svg_path, num_points=1000)
    fs = FourierEpicycles(t, z, n_harmonics=n_harmonics)
    fs.calculate_all_coefficients()
 
    full_approx = fs.approximate(t)
 
    zp_approx, _ = fs.zero_phase_reconstruction()
    mse_zp = np.mean(np.abs(z - zp_approx) ** 2)
 
    sym_coeffs = fs.keep_symmetric_pairs_only(k=20)
    sym_approx = fs.approximate(t, coeffs=sym_coeffs)
    mse_sym = np.mean(np.abs(z - sym_approx) ** 2)
 
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    for ax, curve, ttl in zip(
        axes,
        [full_approx, zp_approx, sym_approx],
        ["Full N reconstruction (ground truth)",
         f"Zero-phase, MSE={mse_zp:.4e}",
         f"Symmetric k=20, MSE={mse_sym:.4e}"],
    ):
        ax.plot(z.real, z.imag, alpha=0.4, label='true')
        ax.plot(curve.real, curve.imag, '--', label='reconstructed')
        ax.set_title(ttl, fontsize=9)
        ax.axis('equal')
        ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig("heart_phase_symmetry_comparison.png")
    plt.close()
 
    print(f"Zero-phase MSE: {mse_zp:.6e}")
    print(f"Symmetric-pairs (k=20) MSE: {mse_sym:.6e}")
    # self.coeffs was never overwritten above (only local dict copies were
    # used), so fs.coeffs still holds the full n_harmonics solution here.
    print("Saved heart_phase_symmetry_comparison.png")
 
 
# =====================================================
# Practice Set J: Gibbs Phenomenon on a Synthesized Square Wave
# Usage: python3 fs_redrawer.py setJ
# =====================================================
def run_set_j():
    import matplotlib.pyplot as plt
 
    M = 1000
    t = np.linspace(0, 2 * np.pi, M)
    signal = np.where(t < np.pi, 1.0, -1.0).astype(complex)
 
    Ns = [5, 15, 45, 135]
    overshoots = []
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.plot(t, signal.real, 'k', linewidth=2, label="true square wave")
 
    for N in Ns:
        fs = FourierEpicycles(t, signal, n_harmonics=N)
        fs.calculate_all_coefficients()
        fine_t = np.linspace(0, 2 * np.pi, 4000)
        approx = fs.approximate(fine_t)
        overshoot = approx.real.max() - 1.0
        overshoots.append(overshoot)
        ax2.plot(fine_t, approx.real, '--', label=f"N={N}")
 
    ax2.legend()
    ax2.set_xlabel("t")
    ax2.set_ylabel("f_hat(t)")
    fig2.tight_layout()
    fig2.savefig("gibbs_reconstructions_overlay.png")
    plt.close(fig2)
 
    plt.figure(figsize=(6, 4))
    plt.plot(Ns, overshoots, marker='o')
    plt.xlabel("N")
    plt.ylabel("overshoot (f_hat_max - 1.0)")
    plt.tight_layout()
    plt.savefig("gibbs_overshoot_vs_N.png")
    plt.close()
 
    for N, o in zip(Ns, overshoots):
        print(f"N={N:4d}  overshoot={o:.4f}")
    print("Saved gibbs_reconstructions_overlay.png and gibbs_overshoot_vs_N.png")
 
 
# =====================================================
# Practice Set K: Magnitude-Threshold Pruning vs. Energy-Ratio Pruning
# Usage: python3 fs_redrawer.py setK <path_to_svg> [n_harmonics]
# =====================================================
def run_set_k(svg_path, n_harmonics=150):
    import matplotlib.pyplot as plt
 
    t, z = load_svg_path(svg_path, num_points=1000)
    target_count = 41
 
    # (a) find r for energy-based pruning that lands near target_count
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        fs_try = FourierEpicycles(t, z, n_harmonics=n_harmonics)
        fs_try.calculate_all_coefficients()
        n_kept, _ = fs_try.prune_harmonics_by_energy(mid)
        if n_kept < target_count:
            lo = mid
        else:
            hi = mid
    r_matched = hi
    fs_e = FourierEpicycles(t, z, n_harmonics=n_harmonics)
    fs_e.calculate_all_coefficients()
    n_kept_e, _ = fs_e.prune_harmonics_by_energy(r_matched)
    mse_e = fs_e.evaluate_reconstruction_error()
 
    # (b) find epsilon for threshold pruning that lands near target_count
    fs_full = FourierEpicycles(t, z, n_harmonics=n_harmonics)
    fs_full.calculate_all_coefficients()
    mags = sorted((abs(c) for n, c in fs_full.coeffs.items() if n != 0), reverse=True)
    epsilon = mags[min(target_count - 2, len(mags) - 1)]
    fs_t = FourierEpicycles(t, z, n_harmonics=n_harmonics)
    fs_t.calculate_all_coefficients()
    n_kept_t = fs_t.prune_harmonics_by_threshold(epsilon)
    mse_t = fs_t.evaluate_reconstruction_error()
 
    print(f"Energy pruning:    r={r_matched:.4f}, kept={n_kept_e}, MSE={mse_e:.6e}")
    print(f"Threshold pruning: eps={epsilon:.6f}, kept={n_kept_t}, MSE={mse_t:.6e}")
 
    approx_e = fs_e.approximate(t)
    approx_t = fs_t.approximate(t)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    for ax, approx, ttl in zip(axes, [approx_e, approx_t], ["energy-based", "threshold-based"]):
        ax.plot(z.real, z.imag, alpha=0.4, label="true")
        ax.plot(approx.real, approx.imag, '--', label="reconstructed")
        ax.set_title(ttl)
        ax.axis('equal')
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("energy_vs_threshold_pruning.png")
    print("Saved energy_vs_threshold_pruning.png")
 
 
# =====================================================
# Practice Set L: Convergence Rate (MSE vs. Harmonic Count N)
# Usage: python3 fs_redrawer.py setL <path_to_svg>
# =====================================================
def run_set_l(svg_path):
    import matplotlib.pyplot as plt
 
    t, z = load_svg_path(svg_path, num_points=1000)
 
    Ns = [5, 10, 20, 40, 80, 150, 250]
    mses = []
    print(f"{'N':6s} | MSE")
    print("-" * 24)
    for N in Ns:
        fs = FourierEpicycles(t, z, n_harmonics=N)
        fs.calculate_all_coefficients()
        mse = fs.evaluate_reconstruction_error()
        mses.append(mse)
        print(f"{N:6d} | {mse:.6e}")
 
    log_N = np.log(Ns)
    log_mse = np.log(mses)
    p, intercept = np.polyfit(log_N, log_mse, 1)
    print(f"Fitted convergence exponent p = {p:.3f}  (MSE ~ N^p)")
 
    plt.figure(figsize=(6, 4))
    plt.loglog(Ns, mses, marker='o', label="measured MSE")
    fit_line = np.exp(intercept) * np.array(Ns, dtype=float) ** p
    plt.loglog(Ns, fit_line, '--', label=f"fit: MSE ~ N^{p:.2f}")
    plt.xlabel("N")
    plt.ylabel("MSE")
    plt.legend()
    plt.tight_layout()
    plt.savefig("mse_vs_N_convergence.png")
    print("Saved mse_vs_N_convergence.png")
 
 
# =====================================================
# Practice Set M: Robustness to Coefficient Phase Noise
# Usage: python3 fs_redrawer.py setM <path_to_svg> [n_harmonics]
# =====================================================
def run_set_m(svg_path, n_harmonics=150):
    import matplotlib.pyplot as plt
 
    t, z = load_svg_path(svg_path, num_points=1000)
    fs = FourierEpicycles(t, z, n_harmonics=n_harmonics)
    fs.calculate_all_coefficients()
 
    stds = [0, 0.05, 0.1, 0.2, 0.4, 0.8]
    mses = []
    approx_by_std = {}
    for s in stds:
        perturbed = fs.perturb_phase(s)
        approx = fs.approximate(t, coeffs=perturbed)
        mse = np.mean(np.abs(z - approx) ** 2)
        mses.append(mse)
        approx_by_std[s] = approx
 
    plt.figure(figsize=(6, 4))
    plt.plot(stds, mses, marker='o')
    plt.xlabel("phase_std (radians)")
    plt.ylabel("MSE")
    plt.tight_layout()
    plt.savefig("phase_noise_degradation.png")
    plt.close()
 
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, s in zip(axes, [0, 0.2, 0.8]):
        ax.plot(z.real, z.imag, alpha=0.4, label="true")
        ax.plot(approx_by_std[s].real, approx_by_std[s].imag, '--', label="reconstructed")
        ax.set_title(f"phase_std={s}")
        ax.axis('equal')
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("phase_noise_visual_comparison.png")
    print("MSE by phase_std:", dict(zip(stds, mses)))
    print("Saved phase_noise_degradation.png and phase_noise_visual_comparison.png")
 
 
# =====================================================
# Practice Set N: Even/Odd Decomposition of the Traced Signal
# Usage: python3 fs_redrawer.py setN <path_to_svg> [n_harmonics]
# =====================================================
def run_set_n(svg_path, n_harmonics=150):
    import matplotlib.pyplot as plt
 
    t, z = load_svg_path(svg_path, num_points=1000)
    fs = FourierEpicycles(t, z, n_harmonics=n_harmonics)
    fs.calculate_all_coefficients()
 
    even_td, odd_td = fs.even_odd_split()
 
    even_coeffs = {n: (fs.coeffs[n] + fs.coeffs.get(-n, 0)) / 2 for n in fs.coeffs}
    odd_coeffs = {n: (fs.coeffs[n] - fs.coeffs.get(-n, 0)) / 2 for n in fs.coeffs}
 
    even_fd = fs.approximate(t, coeffs=even_coeffs)
    odd_fd = fs.approximate(t, coeffs=odd_coeffs)
 
    mse_even = np.mean(np.abs(even_td - even_fd) ** 2)
    mse_odd = np.mean(np.abs(odd_td - odd_fd) ** 2)
    print(f"Even-part agreement MSE: {mse_even:.6e}")
    print(f"Odd-part agreement MSE:  {mse_odd:.6e}")
 
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, curve, ttl in zip(axes, [z, even_fd, odd_fd], ["original", "even part", "odd part"]):
        ax.plot(curve.real, curve.imag)
        ax.set_title(ttl)
        ax.axis('equal')
    fig.tight_layout()
    fig.savefig("even_odd_decomposition.png")
    print("Saved even_odd_decomposition.png")
 
 
if __name__ == "__main__":
    import sys
    from pathlib import Path
 
    # Extra practice-set modes (added, not part of the original given usage):
    #   python3 fs_redrawer.py setC <path_to_svg> [n_harmonics]
    #   python3 fs_redrawer.py setD <path_to_svg> [n_harmonics]
    #   python3 fs_redrawer.py setJ
    #   python3 fs_redrawer.py setK <path_to_svg> [n_harmonics]
    #   python3 fs_redrawer.py setL <path_to_svg>
    #   python3 fs_redrawer.py setM <path_to_svg> [n_harmonics]
    #   python3 fs_redrawer.py setN <path_to_svg> [n_harmonics]
    if len(sys.argv) >= 2 and sys.argv[1] == "setJ":
        run_set_j()
        sys.exit(0)
 
    if len(sys.argv) >= 3 and sys.argv[1] in ("setC", "setD", "setK", "setM", "setN"):
        mode = sys.argv[1]
        svg_arg = sys.argv[2]
        n_harm = int(sys.argv[3]) if len(sys.argv) > 3 else 150
        if mode == "setC":
            run_set_c(svg_arg, n_harm)
        elif mode == "setD":
            run_set_d(svg_arg, n_harm)
        elif mode == "setK":
            run_set_k(svg_arg, n_harm)
        elif mode == "setM":
            run_set_m(svg_arg, n_harm)
        elif mode == "setN":
            run_set_n(svg_arg, n_harm)
        sys.exit(0)
 
    if len(sys.argv) >= 3 and sys.argv[1] == "setL":
        run_set_l(sys.argv[2])
        sys.exit(0)
 
    # Usage: python3 assignment.py <path_to_svg> [n_harmonics] [comparison_png_path] [gif_path]
    if len(sys.argv) < 2:
        print("Usage: python3 assignment.py <path_to_svg> [n_harmonics] [comparison_png_path] [gif_path]")
        print("Example: python3 assignment.py svgs/heart.svg 150 heart_comparison.png heart_epicycles.gif")
        print("Practice sets: python3 fs_redrawer.py <setC|setD|setK|setM|setN> <path_to_svg> [n_harmonics]")
        print("               python3 fs_redrawer.py setL <path_to_svg>")
        print("               python3 fs_redrawer.py setJ")
        sys.exit(1)
 
    svg_path = sys.argv[1]
    N_HARMONICS = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    stem = Path(svg_path).stem
    comparison_path = sys.argv[3] if len(sys.argv) > 3 else f"{stem}_comparison.png"
    gif_path = sys.argv[4] if len(sys.argv) > 4 else f"{stem}_epicycles.gif"
 
    t, z = load_svg_path(svg_path, num_points=1000)
    fs = FourierEpicycles(t, z, n_harmonics=N_HARMONICS)
    fs.calculate_all_coefficients()
 
    save_outputs(fs, z, comparison_path, gif_path, num_frames=240)
 
    # ---- Online exam Task 1 & 2: energy-preserving pruning sweep ----
    import matplotlib.pyplot as plt
 
    target_ratios = [0.96, 0.98, 0.99, 1.00]
    print(f"{'Target Ratio':13s} | {'Harmonics Retained':18s} | {'Actual Energy Ratio':20s} | MSE")
    print("-" * 68)
    for r in target_ratios:
        fs_r = FourierEpicycles(t, z, n_harmonics=N_HARMONICS)
        fs_r.calculate_all_coefficients()
        n_kept, actual_ratio = fs_r.prune_harmonics_by_energy(r)
        mse = fs_r.evaluate_reconstruction_error()
        print(f"{r:13.2f} | {n_kept:18d} | {actual_ratio:20.4f} | {mse:.6e}")
 
        approx = fs_r.approximate(t)
        plt.figure(figsize=(4, 4))
        plt.plot(z.real, z.imag, label="original")
        plt.plot(approx.real, approx.imag, "--", label=f"pruned r={r}")
        plt.axis("equal")
        plt.legend()
        plt.title(f"r={r}, harmonics={n_kept}, MSE={mse:.3e}")
        plt.savefig(f"heart_pruned_{r}.png")
        plt.close()
 