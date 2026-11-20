# CSE 219 TF kit — progress

## Done
- Spec + gold reference read. All question papers transcribed -> question_log.md.
- Slide text of all decks -> slide_text/. Visual pass done -> reading_logs.md.
- questions.json (367 rows: Anik 231, Ashraf 100, Outside 36) built by make_questions.py.
- Lesson plan (continuous numbering):
  Anik  F1 Signals L1-5 | F2 LTI&Conv L6-10 | F3 Fourier Series L11-15 | F4 Fourier Transform L16-19
  Ashraf F1 DTFT/DFT L1-4 | F2 FFT L5-8 | F3 Sampling L9-12 | F4 Laplace L13-16 | F5 Z L17-19

## In progress
- Trackers: build_tracker.py (both), coverage check, Word PDF checks of all 9 notes, final report

## Done notes
- Ashraf F5 Z: build_notes_ashraf_ztransform.py
- Ashraf F4 Laplace: build_notes_ashraf_laplace.py
- Ashraf F3 Sampling: build_notes_ashraf_sampling.py
- Ashraf F1 DTFT/DFT + F2 FFT: build_notes_ashraf_dft.py, build_notes_ashraf_fft.py (verify_ashraf12 OK)
- Anik F4 Fourier Transform: build_notes_anik_fourier_transform.py (verify_anik4 OK)
- Anik F3 Fourier Series: build_notes_anik_fourier_series.py (verify_anik3 OK; slide 40 ramp error noted)
- Anik F2 LTI/Conv: build_notes_anik_lti_conv.py (verify_anik2 OK)
- Anik F1 Signals: build_notes_anik_signals.py (verify_anik1.py, 39 checks OK), Word-PDF checked (20 pp)

## Next
- Anik F2-F4, Ashraf F1-F5 (each: verify_*.py then build_notes_*.py)
- build_tracker.py (both trackers), coverage counts
- Word->PDF visual check, final report

## STATUS: all 8 notes + 2 trackers built (Anik 4 notes: Signals, LTI_Convolution, Fourier_Series, Fourier_Transform; Ashraf 5: DTFT_DFT, FFT, Sampling, Laplace, ZTransform). Word PDFs checked (Anik Signals 20pp, others 9-15pp).
