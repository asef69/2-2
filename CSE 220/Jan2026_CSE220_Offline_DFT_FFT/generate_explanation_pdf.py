from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

OUTPUT = "outputs/DFT_FFT_output_calculations.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER,
    fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=colors.HexColor("#17324D"),
    spaceAfter=12,
))
styles.add(ParagraphStyle(
    name="Subtitle", parent=styles["Normal"], alignment=TA_CENTER,
    fontName="Helvetica", fontSize=10, leading=14, textColor=colors.HexColor("#536575"),
    spaceAfter=20,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=15, leading=19, textColor=colors.HexColor("#17324D"),
    spaceBefore=12, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Subsection", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=11.5, leading=15, textColor=colors.HexColor("#A34E22"),
    spaceBefore=8, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="BodySmall", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.4, leading=13, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Formula", parent=styles["BodyText"], fontName="Courier",
    fontSize=9.2, leading=13, leftIndent=16, rightIndent=16,
    textColor=colors.HexColor("#263746"), backColor=colors.HexColor("#F1F5F7"),
    borderPadding=6, spaceBefore=3, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="BulletSmall", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.3, leading=13, leftIndent=13, firstLineIndent=-8, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="Note", parent=styles["BodyText"], fontName="Helvetica-Oblique",
    fontSize=8.8, leading=12, textColor=colors.HexColor("#536575"),
    leftIndent=12, rightIndent=12, spaceAfter=7,
))


def P(text, style="BodySmall"):
    return Paragraph(text, styles[style])


def bullet(text):
    return P("- " + text, "BulletSmall")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D5DEE5"))
    canvas.line(1.6 * cm, 1.25 * cm, A4[0] - 1.6 * cm, 1.25 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#687985"))
    canvas.drawString(1.6 * cm, 0.85 * cm, "CSE 220 - Offline DFT and FFT")
    canvas.drawRightString(A4[0] - 1.6 * cm, 0.85 * cm, "Page %d" % doc.page)
    canvas.restoreState()


def make_table(rows, widths):
    table = Table(rows, colWidths=widths, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C6CF")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F6F8")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4, rightMargin=1.6 * cm, leftMargin=1.6 * cm,
    topMargin=1.5 * cm, bottomMargin=1.6 * cm,
    title="How the DFT and FFT Outputs Are Calculated",
    author="CSE 220 student project",
)

story = []
story.append(P("How the DFT and FFT Outputs Are Calculated", "TitleCenter"))
story.append(P("A step-by-step guide to the numerical multiplication and image-blurring pipelines", "Subtitle"))
story.append(P("This document explains how the code in bigmul.py, image_conv.py, transforms.py, and image_utils.py produces the files under outputs/. It covers the mathematics, array operations, padding rules, saved images, reports, and verification.", "BodySmall"))
story.append(Spacer(1, 6))
story.append(make_table([
    ["Pipeline", "Input", "Main result"],
    ["Task A", "Two decimal strings", "A decimal product in product.txt"],
    ["Task B", "A PNG image and blur kernel", "blurred.png, wraparound.png, kernel.png, comparison.png"],
], [3.0 * cm, 5.5 * cm, 8.0 * cm]))

story.append(P("1. Shared Transform Core", "Section"))
story.append(P("The transform engine is selected by the caller. The naive DFT computes the definition directly. The radix-2 FFT computes the same mathematical transform using bit reversal and butterfly stages, reducing the work from O(N^2) to O(N log N).", "BodySmall"))
story.append(P("Forward DFT:", "Subsection"))
story.append(P("X[k] = sum from n=0 to N-1 of x[n] * exp(-2*pi*i*k*n/N)", "Formula"))
story.append(P("Inverse DFT:", "Subsection"))
story.append(P("x[n] = (1/N) * sum from k=0 to N-1 of X[k] * exp(+2*pi*i*k*n/N)", "Formula"))
story.append(bullet("The FFT requires a power-of-two length, so the caller pads to next_power_of_two when necessary."))
story.append(bullet("The inverse FFT uses conjugated-sign twiddle factors and divides by N."))
story.append(bullet("For a 2D array, the transform is separable: transform every row, then every column."))

story.append(P("2. Task A - Big-Integer Multiplication", "Section"))
story.append(P("The numerical product is calculated without multiplying the original huge integers directly. The decimal numbers are converted to polynomial coefficients, multiplied through the frequency domain, then converted back to decimal.", "BodySmall"))
story.append(P("Step 1: Read the operands", "Subsection"))
story.append(P("Each input file contains two decimal strings. The sign is separated from the magnitude because the transform processes only nonnegative coefficients. The final sign is the product of the two operand signs.", "BodySmall"))
story.append(P("Step 2: Convert to base-10^4 limbs", "Subsection"))
story.append(P("Four decimal digits are packed into each coefficient. The coefficients are stored least-significant first.", "BodySmall"))
story.append(P("123456789 -> [6789, 2345, 1]", "Formula"))
story.append(P("The array represents the polynomial 6789 + 2345*x + 1*x^2, evaluated at x = 10^4.", "BodySmall"))
story.append(P("Step 3: Treat the limbs as polynomials", "Subsection"))
story.append(P("If A has limbs a[0], a[1], ... and B has limbs b[0], b[1], ..., their product coefficients are the linear convolution:", "BodySmall"))
story.append(P("c[k] = sum over i of a[i] * b[k-i]", "Formula"))
story.append(P("Step 4: Choose the transform length", "Subsection"))
story.append(P("For limb lengths La and Lb, the linear result needs La + Lb - 1 coefficients. FFT padding chooses the next power of two. This prevents the high-order coefficients from wrapping around as circular convolution.", "BodySmall"))
story.append(P("For the first report: 3 + 3 - 1 = 5, so N = 8.", "Formula"))
story.append(P("Step 5: Transform, multiply, and invert", "Subsection"))
story.append(bullet("Zero-pad both limb arrays to N."))
story.append(bullet("Compute the transform of each array: A[k] and B[k]."))
story.append(bullet("Multiply corresponding frequency values: C[k] = A[k] * B[k]."))
story.append(bullet("Apply the inverse transform to obtain the convolution coefficients."))
story.append(bullet("Take the real part and round, because floating-point arithmetic can leave tiny imaginary or fractional errors."))
story.append(P("Step 6: Carry propagation", "Subsection"))
story.append(P("The convolution coefficients are not yet valid base-10^4 digits. Each coefficient is combined with the incoming carry:", "BodySmall"))
story.append(P("total = coefficient + carry; carry, digit = divmod(total, 10000)", "Formula"))
story.append(P("The resulting digits are then joined from most significant to least significant, with four-digit zero padding between limbs. The original sign is restored, and the final string is saved in product.txt.", "BodySmall"))
story.append(P("Step 7: Verification", "Subsection"))
story.append(P("Only after the custom calculation, the program compares the decimal result with Python's integer multiplication. MATCH means the two decimal strings are identical.", "BodySmall"))

story.append(P("3. Task B - Image Blurring", "Section"))
story.append(P("The image pipeline applies a 2D convolution in the frequency domain. RGB images are processed as three independent planes; grayscale images use one plane.", "BodySmall"))
story.append(P("Step 1: Load and normalize pixels", "Subsection"))
story.append(P("An 8-bit pixel is converted to a floating-point intensity in [0, 1]:", "BodySmall"))
story.append(P("normalized_pixel = pixel_value / 255", "Formula"))
story.append(P("Step 2: Construct and normalize the kernel", "Subsection"))
story.append(P("image_utils.make_kernel creates a box, Gaussian, bokeh, or motion kernel. The kernel is divided by its total sum so that all weights add to 1. This makes the operation an averaging or blur operation rather than a brightness amplifier.", "BodySmall"))
story.append(make_table([
    ["Kernel", "Meaning"],
    ["Box", "Every position in the square has equal weight."],
    ["Gaussian", "Nearby pixels receive larger weights than distant pixels."],
    ["Bokeh", "A filled circular aperture; bright points become discs."],
    ["Motion", "A line-shaped streak representing camera movement."],
], [3.3 * cm, 13.2 * cm]))
story.append(P("Step 3: Determine the linear-convolution area", "Subsection"))
story.append(P("For image size H x W and kernel size kh x kw, the full linear convolution has size:", "BodySmall"))
story.append(P("(H + kh - 1) x (W + kw - 1)", "Formula"))
story.append(P("For skyline_bokeh, H = W = 512 and kh = kw = 19, giving 530 x 530.", "BodySmall"))
story.append(P("Step 4: Zero-pad for FFT convolution", "Subsection"))
story.append(P("The image and kernel are placed in the upper-left corner of zero-filled arrays. With the radix-2 FFT, 530 is padded to 1024, so the actual transform size is 1024 x 1024. The padding is what makes the result linear rather than circular.", "BodySmall"))
story.append(P("Step 5: Transform rows and columns", "Subsection"))
story.append(P("The 2D transform is computed by applying the 1D engine to every row and then every column. This is valid because the 2D DFT is separable.", "BodySmall"))
story.append(P("Step 6: Multiply spectra", "Subsection"))
story.append(P("For image spectrum I(u,v) and kernel spectrum K(u,v), the product spectrum is:", "BodySmall"))
story.append(P("S(u,v) = I(u,v) * K(u,v)", "Formula"))
story.append(P("The inverse 2D transform of S is the spatial convolution.", "BodySmall"))
story.append(P("Step 7: Crop the centered result", "Subsection"))
story.append(P("The full result is larger than the original image. The program takes the H x W window starting at row kh//2 and column kw//2. This aligns the kernel center with each original pixel and preserves the input dimensions.", "BodySmall"))
story.append(P("Step 8: Save the PNG", "Subsection"))
story.append(P("Values are clipped to [0, 1], multiplied by 255, rounded, converted to uint8, and written as PNG. The internal calculation remains floating point; only the saved image is quantized to 8-bit values.", "BodySmall"))

story.append(PageBreak())
story.append(P("4. Linear Versus Circular Convolution", "Section"))
story.append(P("The program intentionally writes both versions so the padding effect can be observed.", "BodySmall"))
story.append(P("blurred.png - linear convolution", "Subsection"))
story.append(bullet("The image and kernel are zero-padded."))
story.append(bullet("Pixels outside the image are treated as zero."))
story.append(bullet("The full result is cropped back to the original image size."))
story.append(bullet("This is the normal, physically meaningful blur result."))
story.append(P("wraparound.png - circular convolution", "Subsection"))
story.append(bullet("The transform is performed at exactly H x W, with no padding."))
story.append(bullet("The kernel is shifted so its center is at the transform origin."))
story.append(bullet("Content leaving the right edge re-enters at the left, and content leaving the bottom re-enters at the top."))
story.append(bullet("This creates visible boundary wraparound artifacts."))

story.append(P("5. Verification of Image Results", "Section"))
story.append(P("The program takes the top-left 64 x 64 crop and calculates it in two independent ways: frequency-domain convolution and a direct four-loop spatial convolution.", "BodySmall"))
story.append(P("direct[r,c] = sum over i,j of plane[r + kh//2 - i, c + kw//2 - j] * kernel[i,j]", "Formula"))
story.append(P("Out-of-range source pixels are treated as zero. The maximum absolute difference between the two methods is reported. A value around 10^-15 is normal floating-point roundoff; anything above 10^-9 is classified as a bug.", "BodySmall"))
story.append(P("The skyline report records:", "Subsection"))
story.append(make_table([
    ["Report field", "Value"],
    ["Image", "512 x 512 RGB"],
    ["Kernel", "bokeh, 19 x 19"],
    ["Linear-convolution size", "530 x 530"],
    ["Transform size", "1024 x 1024"],
    ["Maximum difference", "3.331e-15"],
    ["Verification", "MATCH"],
], [6.0 * cm, 10.5 * cm]))

story.append(P("6. Meaning of the Output Files", "Section"))
story.append(make_table([
    ["File", "What it contains"],
    ["product.txt", "The final decimal product from Task A."],
    ["Task A report.txt", "Digit counts, base, limb counts, transform length, product length, and verification."],
    ["blurred.png", "Linear zero-padded blur, cropped to the original image size."],
    ["wraparound.png", "Circular no-padding blur showing boundary wraparound."],
    ["kernel.png", "Magnified visual preview of the normalized blur kernel."],
    ["comparison.png", "Original, linear blur, and circular blur shown side by side."],
    ["Task B report.txt", "Image dimensions, kernel, engine, padding dimensions, numerical error, and verification."],
    ["runtime plots", "Timing curves for DFT, FFT, and direct spatial methods in the benchmark folders."],
], [4.2 * cm, 12.3 * cm]))
story.append(P("In short: Task A uses the convolution theorem to multiply large numbers as polynomials, while Task B uses the same theorem to blur image planes as 2D arrays. Zero-padding determines whether the convolution is linear or circular, and the direct calculations provide correctness checks for both pipelines.", "Note"))

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
