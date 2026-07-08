# Tên file: frontend/components/image_dialog.py
# CHỨC NĂNG: Hộp thoại chèn ảnh từ máy tính với live CSS preview và hỗ trợ sáng/tối.
# CHANGELOG:
# - 10:00:00 08/07/2026: [NEW] Khởi tạo dialog chèn ảnh Premium hỗ trợ live preview CSS và theme sáng/tối (Antigravity)

import os
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QCheckBox,
    QFormLayout,
    QWidget,
)
from PyQt6.QtCore import QUrl


class InsertImageDialog(QDialog):
    """Hộp thoại Premium hỗ trợ người dùng chèn ảnh từ máy tính vào tài liệu Markdown."""

    def __init__(self, parent: QWidget | None = None, is_dark: bool = False) -> None:
        """Khởi tạo hộp thoại chèn ảnh.

        Args:
            parent: Widget cha sở hữu.
            is_dark: Cờ biểu thị ứng dụng đang chạy ở theme tối.
        """
        super().__init__(parent)
        self.is_dark = is_dark
        self.selected_path = ""

        self.setWindowTitle("Chèn ảnh từ máy tính")
        self.setMinimumWidth(450)
        self.init_ui()
        self.apply_theme()
        self.update_css_preview()

    def init_ui(self) -> None:
        """Khởi tạo các thành phần giao diện của hộp thoại."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Form Layout cho các trường nhập liệu chính
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # 1. Đường dẫn ảnh
        path_layout = QHBoxLayout()
        self.txt_path = QLineEdit()
        self.txt_path.setPlaceholderText("Đường dẫn file ảnh trên máy tính...")
        self.txt_path.textChanged.connect(self.on_path_changed)
        path_layout.addWidget(self.txt_path)

        self.btn_browse = QPushButton("Duyệt...")
        self.btn_browse.clicked.connect(self.browse_file)
        path_layout.addWidget(self.btn_browse)
        form_layout.addRow(QLabel("Đường dẫn ảnh:"), path_layout)

        # 2. Alt text
        self.txt_alt = QLineEdit()
        self.txt_alt.setPlaceholderText("Chú thích thay thế cho ảnh...")
        form_layout.addRow(QLabel("Chú thích (Alt):"), self.txt_alt)

        # 3. Chiều rộng ảnh
        self.txt_width = QLineEdit()
        self.txt_width.setText("380")
        self.txt_width.setPlaceholderText("Ví dụ: 380 hoặc 100%...")
        form_layout.addRow(QLabel("Chiều rộng (Width):"), self.txt_width)

        main_layout.addLayout(form_layout)

        # 4. Nhóm Tùy chọn CSS Style
        style_group_layout = QVBoxLayout()
        style_group_layout.setSpacing(8)

        lbl_style_title = QLabel("Tùy chọn phong cách hiển thị (CSS):")
        lbl_style_title.setStyleSheet("font-weight: bold;")
        style_group_layout.addWidget(lbl_style_title)

        self.chk_radius = QCheckBox("Bo góc ảnh (border-radius: 8px)")
        self.chk_radius.setChecked(True)
        self.chk_radius.toggled.connect(self.update_css_preview)
        style_group_layout.addWidget(self.chk_radius)

        self.chk_shadow = QCheckBox("Đổ bóng ảnh (box-shadow)")
        self.chk_shadow.setChecked(True)
        self.chk_shadow.toggled.connect(self.update_css_preview)
        style_group_layout.addWidget(self.chk_shadow)

        self.chk_margin = QCheckBox("Căn khoảng cách lề dưới (margin-bottom: 25px)")
        self.chk_margin.setChecked(True)
        self.chk_margin.toggled.connect(self.update_css_preview)
        style_group_layout.addWidget(self.chk_margin)

        # 5. Live CSS Preview
        preview_layout = QHBoxLayout()
        preview_layout.addWidget(QLabel("Live CSS Style:"))
        self.txt_css_preview = QLineEdit()
        self.txt_css_preview.setToolTip(
            "Chuỗi CSS được sinh ra tự động, bạn có thể chỉnh sửa trực tiếp."
        )
        preview_layout.addWidget(self.txt_css_preview)
        style_group_layout.addLayout(preview_layout)

        main_layout.addLayout(style_group_layout)

        # 6. Hàng nút bấm xác nhận/hủy bỏ
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.btn_insert = QPushButton("Chèn ảnh")
        self.btn_insert.setObjectName("btnInsert")
        self.btn_insert.clicked.connect(self.accept)
        buttons_layout.addWidget(self.btn_insert)

        self.btn_cancel = QPushButton("Hủy bỏ")
        self.btn_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self.btn_cancel)

        main_layout.addLayout(buttons_layout)

    def apply_theme(self) -> None:
        """Thiết lập Stylesheet Premium cho hộp thoại dựa trên theme hiện tại."""
        if self.is_dark:
            self.setStyleSheet("""
                QDialog {
                    background-color: #161b22;
                    color: #c9d1d9;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QLabel {
                    color: #c9d1d9;
                    font-size: 13px;
                }
                QLineEdit {
                    background-color: #0d1117;
                    color: #c9d1d9;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    padding: 6px 10px;
                    font-size: 13px;
                }
                QLineEdit:focus {
                    border: 1px solid #58a6ff;
                }
                QPushButton {
                    background-color: #21262d;
                    color: #c9d1d9;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #30363d;
                    border-color: #8b949e;
                }
                QPushButton#btnInsert {
                    background-color: #238636;
                    color: #ffffff;
                    border: 1px solid #2ea043;
                }
                QPushButton#btnInsert:hover {
                    background-color: #2ea043;
                }
                QCheckBox {
                    color: #c9d1d9;
                    font-size: 13px;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #ffffff;
                    color: #2c3e50;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 13px;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #2c3e50;
                    border: 1px solid #d0d7de;
                    border-radius: 6px;
                    padding: 6px 10px;
                    font-size: 13px;
                }
                QLineEdit:focus {
                    border: 1px solid #0969da;
                }
                QPushButton {
                    background-color: #f6f8fa;
                    color: #24292f;
                    border: 1px solid #d0d7de;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #f3f4f6;
                    border-color: #8b949e;
                }
                QPushButton#btnInsert {
                    background-color: #2da44e;
                    color: #ffffff;
                    border: 1px solid #2c974b;
                }
                QPushButton#btnInsert:hover {
                    background-color: #2c974b;
                }
                QCheckBox {
                    color: #2c3e50;
                    font-size: 13px;
                }
            """)

    def browse_file(self) -> None:
        """Mở hộp thoại chọn tệp hình ảnh từ máy tính."""
        filters = "Hình ảnh (*.png *.jpg *.jpeg *.gif *.webp *.bmp);;Tất cả các tệp (*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn file ảnh để chèn", "", filters
        )
        if file_path:
            self.txt_path.setText(file_path)

    def on_path_changed(self, text: str) -> None:
        """Cập nhật gợi ý Alt text khi đường dẫn file thay đổi.

        Args:
            text: Đường dẫn file ảnh mới.
        """
        self.selected_path = text
        if text:
            # Lấy tên file không bao gồm phần mở rộng để gợi ý làm alt text
            base_name = os.path.splitext(os.path.basename(text))[0]
            # Thay thế ký tự đặc biệt, gạch dưới thành dấu cách cho đẹp
            suggested_alt = base_name.replace("_", " ").replace("-", " ")
            # Chỉ điền nếu ô Alt text đang trống
            if not self.txt_alt.text().strip():
                self.txt_alt.setText(suggested_alt)

    def update_css_preview(self) -> None:
        """Cập nhật ô Live CSS Style dựa trên các tùy chọn checkbox đã chọn."""
        styles = []
        if self.chk_radius.isChecked():
            styles.append("border-radius: 8px;")
        if self.chk_shadow.isChecked():
            styles.append("box-shadow: 0 4px 15px rgba(0,0,0,0.15);")
        if self.chk_margin.isChecked():
            styles.append("margin-bottom: 25px;")

        self.txt_css_preview.setText(" ".join(styles))

    def get_image_data(self) -> tuple[str, str, str, str]:
        """Trả về dữ liệu đã cấu hình của hình ảnh.

        Returns:
            tuple[str, str, str, str]: Bộ giá trị bao gồm (URL ảnh dạng file, Alt text, Chiều rộng, Style CSS).
        """
        path = self.txt_path.text().strip()
        # Chuyển đổi đường dẫn tuyệt đối sang URL an toàn với file:///
        url = QUrl.fromLocalFile(path).toString() if path else ""
        alt = self.txt_alt.text().strip()
        width = self.txt_width.text().strip()
        style = self.txt_css_preview.text().strip()
        return url, alt, width, style
