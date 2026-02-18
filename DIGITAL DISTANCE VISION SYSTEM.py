# Main launcher for DIGITAL DISTANCE VISION SYSTEM 
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLabel, QFrame)
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QBrush, QPen, QFont
from PyQt6.QtCore import Qt, QRectF, QPointF

# ==========================================
# CORE ENGINE: Landolt C Generator (ISO 8596)
# ==========================================
class LandoltC(QWidget):
    def __init__(self, size_px, orientation_deg=0, color=Qt.GlobalColor.white):
        """
        ISO 8596 Compliant Landolt C Generator.
        
        Args:
            size_px (int): Total diameter in pixels (The 5-unit dimension).
            orientation_deg (int): Rotation (0=Right, 90=Up, 180=Left, 270=Down).
            color (QColor): The color of the optotype.
        """
        super().__init__()
        self.size_px = size_px
        self.orientation = orientation_deg
        self.optotype_color = color
        
        # Set fixed size with padding to prevent clipping during rotation
        self.setFixedSize(int(size_px * 1.2), int(size_px * 1.2))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Define the Unit Grid (ISO Standard: 5x5 Grid)
        # Total Size = 5 units. Stroke = 1 unit. Gap = 1 unit.
        unit = self.size_px / 5.0
        
        # 2. Calculate Center
        cx = self.width() / 2
        cy = self.height() / 2
        
        # 3. Create Vector Paths (Constructive Geometry)
        
        # A. Outer Circle (Diameter = 5 units, Radius = 2.5 units)
        outer_path = QPainterPath()
        outer_path.addEllipse(QPointF(cx, cy), 2.5 * unit, 2.5 * unit)
        
        # B. Inner Circle (Diameter = 3 units, Radius = 1.5 units)
        inner_path = QPainterPath()
        inner_path.addEllipse(QPointF(cx, cy), 1.5 * unit, 1.5 * unit)
        
        # C. The Gap Rectangle (Width > stroke, Height = 1.0 unit)
        # Positioned on the Right (0 degrees) to cut through the ring.
        # Starts at x=1.0 (inside the hole) and extends to x=3.0 (outside the ring).
        gap_path = QPainterPath()
        gap_rect = QRectF(cx + (1.0 * unit), cy - (0.5 * unit), 2.5 * unit, 1.0 * unit)
        gap_path.addRect(gap_rect)
        
        # 4. Boolean Subtraction to create the shape
        # Ring = Outer - Inner
        ring_path = outer_path.subtracted(inner_path)
        
        # Final C = Ring - Gap
        final_shape = ring_path.subtracted(gap_path)
        
        # 5. Apply Rotation to the Canvas
        painter.translate(cx, cy)
        # Rotate negative because screen Y coordinates go down
        painter.rotate(-self.orientation) 
        painter.translate(-cx, -cy)
        
        # 6. Draw the result
        painter.setBrush(QBrush(self.optotype_color))
        painter.setPen(Qt.PenStyle.NoPen) # No outline
        painter.drawPath(final_shape)

# ==========================================
# UI: Test Dashboard
# ==========================================
class VisionTester(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisionEye - ISO 8596 Calibration Test")
        self.resize(1000, 600)
        
        # Main Container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Dark Mode Background (to prove transparency works)
        central_widget.setStyleSheet("background-color: #2b2b2b;") 
        
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("ISO 8596 Landolt C Vector Engine")
        header.setStyleSheet("color: #00ADB5; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Instructions
        sub_header = QLabel("Verifying: 5x5 Grid Geometry | Transparency | Rotation | Vector Scaling")
        sub_header.setStyleSheet("color: #EEEEEE; font-size: 14px; margin-bottom: 20px;")
        sub_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub_header)
        
        # --- TEST ROW 1: Large Optotypes (Standard Orientations) ---
        row1_label = QLabel("Standard Orientations (Size: 150px)")
        row1_label.setStyleSheet("color: #AAAAAA; font-weight: bold;")
        layout.addWidget(row1_label)

        box1 = QFrame()
        box1.setStyleSheet("background-color: #393E46; border-radius: 10px;")
        layout1 = QHBoxLayout(box1)
        
        # Create 4 Cs
        layout1.addWidget(LandoltC(150, 0, Qt.GlobalColor.white))   # Right
        layout1.addWidget(LandoltC(150, 90, Qt.GlobalColor.white))  # Up
        layout1.addWidget(LandoltC(150, 180, Qt.GlobalColor.white)) # Left
        layout1.addWidget(LandoltC(150, 270, Qt.GlobalColor.white)) # Down
        
        layout.addWidget(box1)
        
        # --- TEST ROW 2: Scaling Test (Different Sizes) ---
        row2_label = QLabel("Infinite Scaling Check (10px to 100px)")
        row2_label.setStyleSheet("color: #AAAAAA; font-weight: bold; margin-top: 10px;")
        layout.addWidget(row2_label)

        box2 = QFrame()
        box2.setStyleSheet("background-color: #393E46; border-radius: 10px;")
        layout2 = QHBoxLayout(box2)
        
        # Add progressively smaller Cs to check for pixelation/clarity
        sizes = [100, 80, 60, 40, 20, 10]
        for size in sizes:
            layout2.addWidget(LandoltC(size, 0, Qt.GlobalColor.cyan))
            
        layout.addWidget(box2)
        
        layout.addStretch()

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    # Handle High DPI Scaling (Retina/4K Screens)
    if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = VisionTester()
    window.show()
    sys.exit(app.exec())