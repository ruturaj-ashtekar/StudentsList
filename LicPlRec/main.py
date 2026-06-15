import cv2
import pytesseract
import imutils

# Linux path (usually not needed if tesseract is installed)
# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Load image
image = cv2.imread("car.jpg")

# Resize for easier processing
image = imutils.resize(image, width=600)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Reduce noise while preserving edges
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Edge detection
edged = cv2.Canny(gray, 30, 200)

# Find contours
contours, _ = cv2.findContours(
    edged.copy(),
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE
)

# Sort contours by area
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

plate_contour = None

# Locate number plate
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.018 * perimeter, True)

    # License plate is usually rectangular
    if len(approx) == 4:
        plate_contour = approx
        break

if plate_contour is not None:

    # Create mask
    mask = cv2.drawContours(
        cv2.zeros_like(gray),
        [plate_contour],
        0,
        255,
        -1
    )

    # Extract plate region
    x, y, w, h = cv2.boundingRect(plate_contour)
    plate = gray[y:y+h, x:x+w]

    # OCR
    text = pytesseract.image_to_string(
        plate,
        config='--psm 8'
    )

    print("Detected Plate Number:", text.strip())

    # Draw contour
    cv2.drawContours(image, [plate_contour], -1, (0, 255, 0), 3)

    cv2.imshow("Detected Plate", plate)

else:
    print("License plate not found")

cv2.imshow("Original Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()