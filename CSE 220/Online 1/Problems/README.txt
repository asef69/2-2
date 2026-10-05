CSE 219 - Signals and Their Properties : Coding Problem Set
===========================================================

This bundle accompanies
  CSE219_Signals_Coding_Problems_with_Solutions.pdf

Folders
  templates/   P01..P10 - student starter files. Implement the functions
               marked "ANSWER IMPLEMENTATION"; base signals and most plotting
               are already provided.
  solutions/   P01..P10 - reference solutions. Each was executed and its
               built-in assertions verified before being placed in the PDF.

Run any file with:
  python3 solutions/P05_solution.py

Requirements: Python 3, numpy, matplotlib (scipy NOT required).

Topics (mapped to Lecture 1):
  1  Energy, power & signal classification
  2  General affine transform x(a t + b) via the shift-reverse-scale recipe
  3  Discrete-time periodicity & fundamental period
  4  Finite energy of infinite-range signals (convergence)
  5  Echo / multipath signal & its energy
  6  The time-scaling energy law  E{x(at)} = E{x}/|a|
  7  Energy split into even & odd parts (orthogonality)
  8  Average power of periodic signals (one period is enough)
  9  Discrete vs continuous energy (sampling / Riemann limit)
  10 Building a waveform from a single prototype pulse
