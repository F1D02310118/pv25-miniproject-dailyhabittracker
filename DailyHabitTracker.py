import sys, os, json
from PyQt5 import QtWidgets, QtGui, QtCore
from datetime import datetime

class HabitModel:
    """Model class representing a habit to track."""
    
    def __init__(self, name, frequency, target_days, created_at=None, completed_days=0, status="Not Started"):
        """Initialize a habit with tracking information."""
        self.name = name
        self.frequency = frequency
        self.target_days = target_days
        self.created_at = created_at or datetime.now().strftime("%d-%m-%Y %H:%M")
        self.completed_days = completed_days
        self.status = status

    def to_dict(self):
        """Convert habit to dictionary for serialization."""
        return {
            "name": self.name,
            "frequency": self.frequency,
            "target_days": self.target_days,
            "created_at": self.created_at,
            "completed_days": self.completed_days,
            "status": self.status
        }

    def from_dict(data):
        """Create a habit from dictionary data."""
        return HabitModel(
            name=data.get("name", "Unknown"),
            frequency=data.get("frequency", "Daily"),
            target_days=data.get("target_days", 1),
            created_at=data.get("created_at"),
            completed_days=data.get("completed_days", 0),
            status=data.get("status", "Not Started")
        )

    def calculate_progress_percentage(self):
        """Calculate progress percentage of the habit."""
        if self.target_days <= 0:
            return 0
        return int((self.completed_days / self.target_days) * 100)
    
    def update_status_from_progress(self):
        """Update status based on current progress."""
        progress_pct = self.calculate_progress_percentage()
        if progress_pct >= 100:
            self.status = "Completed"
        elif progress_pct > 0:
            self.status = "In Progress"
        else:
            self.status = "Not Started"


class DailyHabitTracker(QtWidgets.QMainWindow):
    """Main application window for habit tracking."""
    
    HABIT_FILE = "habits.json"
    LIGHT_THEME_PATH = "styles/light_theme.qss"
    DARK_THEME_PATH = "styles/dark_theme.qss"

    def __init__(self):
        """Initialize the main window and UI components."""
        super().__init__()
        self.habits = []
        
        self.setWindowTitle("Daily Habit Tracker")
        self.setGeometry(100, 100, 900, 600)
        
        self.ensure_directory_structure()
        self.create_ui_components()
        self.setup_ui_layout()
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_keyboard_shortcuts()
        self.apply_theme("light")
        self.load_habits_from_file()

    def ensure_directory_structure(self):
        """Create necessary directories and files if they don't exist."""
        os.makedirs("styles", exist_ok=True)
        
        self._create_theme_file_if_needed(self.LIGHT_THEME_PATH, self._get_light_theme_content())
        self._create_theme_file_if_needed(self.DARK_THEME_PATH, self._get_dark_theme_content())
    
    def _create_theme_file_if_needed(self, file_path, content):
        """Create a theme file if it doesn't exist."""
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write(content)
    
    def _get_light_theme_content(self):
        """Get content for light theme stylesheet."""
        return """QMainWindow {
    background-color: #ffffff;
    color: #000000;
}
QLineEdit, QComboBox, QSpinBox, QListWidget {
    background-color: #f5f5f5;
    color: #000;
    border-radius: 5px;
    padding: 5px;
}
QPushButton {
    background-color: #dddddd;
    color: #000;
    padding: 6px;
    border-radius: 8px;
}
QPushButton:hover {
    background-color: #bbbbbb;
}
QProgressBar {
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #4CAF50;
    width: 10px;
}
"""
    
    def _get_dark_theme_content(self):
        """Get content for dark theme stylesheet."""
        return """QMainWindow {
    background-color: #2d2d2d;
    color: #f0f0f0;
}
QLineEdit, QComboBox, QSpinBox, QListWidget {
    background-color: #444;
    color: #fff;
    border-radius: 5px;
    padding: 5px;
}
QPushButton {
    background-color: #5e5e5e;
    color: #fff;
    padding: 6px;
    border-radius: 8px;
}
QPushButton:hover {
    background-color: #777;
}
QProgressBar {
    border: 2px solid #444;
    border-radius: 5px;
    text-align: center;
    color: white;
}
QProgressBar::chunk {
    background-color: #4CAF50;
    width: 10px;
}
QLabel#student_info {
    font-weight: bold;
    padding: 10px;
    border: 1px solid #555;
    border-radius: 5px;
    background-color: #333;
}
"""

    def create_ui_components(self):
        """Create all UI components."""
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)        
        self.create_header_components()        
        self.create_stats_section()        
        self.tab_widget = QtWidgets.QTabWidget()
        self.create_habits_tab()
        self.create_add_habit_tab()        
        self.create_reset_button()        
        self.statusBar().showMessage("Ready")
    
    def create_header_components(self):
        """Create header title and student info components."""
        self.title_label = QtWidgets.QLabel("Daily Habit Tracker", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #3498db; margin: 10px;")
        
        self.student_info_frame = QtWidgets.QFrame()
        self.student_info_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.student_info_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.student_info_frame.setObjectName("student_info")
        
        student_info_layout = QtWidgets.QHBoxLayout(self.student_info_frame)
        
        student_id_label = QtWidgets.QLabel("Student ID (NIM):")
        student_id_label.setStyleSheet("font-weight: bold;")
        student_id_value = QtWidgets.QLabel("F1D0231018")
        student_id_value.setStyleSheet("font-style: italic;")
        
        student_name_label = QtWidgets.QLabel("Student Name:")
        student_name_label.setStyleSheet("font-weight: bold;")
        student_name_value = QtWidgets.QLabel("Lalu Maulana Rizki Hidayat")
        student_name_value.setStyleSheet("font-style: italic;")
        
        student_info_layout.addWidget(student_id_label)
        student_info_layout.addWidget(student_id_value)
        student_info_layout.addSpacing(20)
        student_info_layout.addWidget(student_name_label)
        student_info_layout.addWidget(student_name_value)
    
    def create_stats_section(self):
        """Create statistics section showing habit counts."""
        stats_layout = QtWidgets.QHBoxLayout()
        self.stats_label = QtWidgets.QLabel("Total Habits: 0 | Completed: 0 | In Progress: 0")
        self.stats_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.stats_label)
        self.main_layout.addLayout(stats_layout)
    
    def create_habits_tab(self):
        """Create tab for displaying habits."""
        self.habits_tab = QtWidgets.QWidget()
        habits_layout = QtWidgets.QVBoxLayout(self.habits_tab)
        
        habits_group = QtWidgets.QGroupBox("Your Habits")
        habits_group_layout = QtWidgets.QVBoxLayout(habits_group)
        
        self.habits_list_widget = QtWidgets.QListWidget()
        self.habits_list_widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.habits_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.habits_list_widget.itemSelectionChanged.connect(self.update_progress_display)
        habits_group_layout.addWidget(self.habits_list_widget)
        
        progress_layout = QtWidgets.QHBoxLayout()
        
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v/%m days (%p%)")
        self.progress_bar.setRange(0, 100)
        self.increment_button = QtWidgets.QPushButton("+1 Day")
        self.increment_button.clicked.connect(self.increment_selected_habit)
        self.decrement_button = QtWidgets.QPushButton("-1 Day")
        self.decrement_button.clicked.connect(self.decrement_selected_habit)
        
        progress_layout.addWidget(QtWidgets.QLabel("Progress:"))
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.increment_button)
        progress_layout.addWidget(self.decrement_button)
        
        habits_group_layout.addLayout(progress_layout)        
        habits_layout.addWidget(habits_group)
        
        self.tab_widget.addTab(self.habits_tab, "My Habits")
    
    def create_add_habit_tab(self):
        """Create tab for adding new habits."""
        self.add_tab = QtWidgets.QWidget()
        add_layout = QtWidgets.QVBoxLayout(self.add_tab)
        
        form_group = QtWidgets.QGroupBox("Add New Habit")
        form_layout = QtWidgets.QFormLayout(form_group)
        
        self.habit_name_input = QtWidgets.QLineEdit(placeholderText="Enter your habit...")
        form_layout.addRow("Habit Name:", self.habit_name_input)
        
        self.frequency_combo = QtWidgets.QComboBox()
        self.frequency_combo.addItems(["Daily", "Weekly", "Monthly"])
        form_layout.addRow("Frequency:", self.frequency_combo)
        
        self.target_days_spin = QtWidgets.QSpinBox()
        self.target_days_spin.setRange(1, 365)
        self.target_days_spin.setPrefix("Target: ")
        self.target_days_spin.setSuffix(" days")
        form_layout.addRow("Target Days:", self.target_days_spin)
        
        self.importance_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.importance_slider.setRange(1, 5)
        self.importance_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.importance_slider.setTickInterval(1)
        self.importance_slider.setValue(3)
        
        self.importance_label = QtWidgets.QLabel("Importance: 3")
        self.importance_slider.valueChanged.connect(
            lambda val: self.importance_label.setText(f"Importance: {val}")
        )
        form_layout.addRow(self.importance_label, self.importance_slider)
        
        self.reminder_checkbox = QtWidgets.QCheckBox("Enable Reminders")
        form_layout.addRow("Reminders:", self.reminder_checkbox)
        
        radio_layout = QtWidgets.QHBoxLayout()
        self.public_radio = QtWidgets.QRadioButton("Public")
        self.private_radio = QtWidgets.QRadioButton("Private")
        self.private_radio.setChecked(True)
        radio_layout.addWidget(self.public_radio)
        radio_layout.addWidget(self.private_radio)
        form_layout.addRow("Privacy:", radio_layout)
        
        add_layout.addWidget(form_group)
        
        button_layout = QtWidgets.QHBoxLayout()
        
        self.add_habit_button = QtWidgets.QPushButton("Add Habit")
        self.add_habit_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogOkButton))
        self.add_habit_button.clicked.connect(self.add_new_habit)
        button_layout.addWidget(self.add_habit_button)
        
        self.clear_form_button = QtWidgets.QPushButton("Clear Form")
        self.clear_form_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogResetButton))
        self.clear_form_button.clicked.connect(self.clear_form_fields)
        button_layout.addWidget(self.clear_form_button)
        
        add_layout.addLayout(button_layout)
        
        self.tab_widget.addTab(self.add_tab, "Add New Habit")
    
    def create_reset_button(self):
        """Create reset all habits button."""
        self.reset_all_button = QtWidgets.QPushButton("Reset All Habits")
        self.reset_all_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogDiscardButton))
        self.reset_all_button.clicked.connect(self.reset_all_habits)
    
    def setup_ui_layout(self):
        """Arrange UI components in the main layout."""
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.student_info_frame)
        self.main_layout.addWidget(self.tab_widget) 
        self.main_layout.addWidget(self.reset_all_button)
    
    def setup_menu_bar(self):
        """Setup application menu bar."""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("&File")
        
        self.save_action = QtWidgets.QAction("&Save Habits", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setStatusTip("Save habits to file")
        self.save_action.triggered.connect(self.save_habits_to_file)
        file_menu.addAction(self.save_action)
        
        self.export_action = QtWidgets.QAction("&Export as Text", self)
        self.export_action.setStatusTip("Export habits as text file")
        self.export_action.triggered.connect(self.export_habits_to_text)
        file_menu.addAction(self.export_action)
        
        file_menu.addSeparator()
        
        self.exit_action = QtWidgets.QAction("E&xit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setStatusTip("Exit application")
        self.exit_action.triggered.connect(self.close)
        file_menu.addAction(self.exit_action)
        
        edit_menu = menubar.addMenu("&Edit")
        
        self.add_action = QtWidgets.QAction("&Add Habit", self)
        self.add_action.setShortcut("Ctrl+N")
        self.add_action.triggered.connect(self.add_new_habit)
        edit_menu.addAction(self.add_action)
        
        self.delete_action = QtWidgets.QAction("&Delete Selected", self)
        self.delete_action.setShortcut("Del")
        self.delete_action.triggered.connect(self.delete_selected_habit)
        edit_menu.addAction(self.delete_action)
        
        view_menu = menubar.addMenu("&View")
        
        theme_menu = view_menu.addMenu("&Theme")
        
        self.light_theme_action = QtWidgets.QAction("&Light Theme", self)
        self.light_theme_action.triggered.connect(lambda: self.apply_theme("light"))
        theme_menu.addAction(self.light_theme_action)
        
        self.dark_theme_action = QtWidgets.QAction("&Dark Theme", self)
        self.dark_theme_action.triggered.connect(lambda: self.apply_theme("dark"))
        theme_menu.addAction(self.dark_theme_action)
        
        help_menu = menubar.addMenu("&Help")
        
        self.about_action = QtWidgets.QAction("&About", self)
        self.about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(self.about_action)
    
    def setup_toolbar(self):
        """Setup application toolbar."""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.addAction(self.add_action)
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.exit_action)
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common actions."""
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+A"), self, self.select_all_habits)
        QtWidgets.QShortcut(QtGui.QKeySequence("F5"), self, self.refresh_habits_display)

    def add_new_habit(self):
        """Add a new habit from form inputs."""
        name = self.habit_name_input.text().strip()
        frequency = self.frequency_combo.currentText()
        target_days = self.target_days_spin.value()
        importance = self.importance_slider.value()
        has_reminder = self.reminder_checkbox.isChecked()
        is_private = self.private_radio.isChecked()
        
        if not name:
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Habit name cannot be empty!")
            return
        
        habit_details = f"{name} (Importance: {importance}/5"
        if has_reminder:
            habit_details += ", With Reminders"
        habit_details += f", {frequency}, {'Private' if is_private else 'Public'})"
        
        reply = QtWidgets.QMessageBox.question(
            self, "Confirm New Habit", 
            f"Create new habit: {habit_details}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            new_habit = HabitModel(name, frequency, target_days)
            self.habits.append(new_habit)
            self.save_and_refresh()
            self.clear_form_fields()
            QtWidgets.QMessageBox.information(self, "Success", "Habit added successfully!")
    
    def clear_form_fields(self):
        """Clear all form input fields."""
        self.habit_name_input.clear()
        self.frequency_combo.setCurrentIndex(0)
        self.target_days_spin.setValue(1)
        self.importance_slider.setValue(3)
        self.reminder_checkbox.setChecked(False)
        self.private_radio.setChecked(True)
    
    def increment_selected_habit(self):
        """Increment completed days for selected habit."""
        selected_items = self.habits_list_widget.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.information(self, "Selection Required", "Please select a habit first.")
            return
        
        index = self.habits_list_widget.row(selected_items[0])
        habit = self.habits[index]
        
        if habit.completed_days < habit.target_days:
            habit.completed_days += 1
            habit.update_status_from_progress()
            self.save_and_refresh()
    
    def decrement_selected_habit(self):
        """Decrement completed days for selected habit."""
        selected_items = self.habits_list_widget.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.information(self, "Selection Required", "Please select a habit first.")
            return
        
        index = self.habits_list_widget.row(selected_items[0])
        habit = self.habits[index]
        
        if habit.completed_days > 0:
            habit.completed_days -= 1
            habit.update_status_from_progress()
            self.save_and_refresh()
    
    def edit_habit_name(self, index):
        """Edit the name of a habit."""
        habit = self.habits[index]
        text, ok = QtWidgets.QInputDialog.getText(self, "Edit Habit Name", "New Habit Name:", text=habit.name)
        if ok and text.strip():
            habit.name = text.strip()
            self.save_and_refresh()
    
    def change_habit_status(self, index):
        """Change the status of a habit."""
        habit = self.habits[index]
        statuses = ["Not Started", "In Progress", "Completed"]
        status, ok = QtWidgets.QInputDialog.getItem(
            self, "Change Status", "Select new status:", 
            statuses, statuses.index(habit.status), False
        )
        if ok and status:
            habit.status = status
            self.save_and_refresh()
    
    def delete_habit(self, index):
        """Delete a habit by index."""
        habit = self.habits[index]
        reply = QtWidgets.QMessageBox.question(
            self, "Delete Habit",
            f"Delete habit '{habit.name}'?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.habits.pop(index)
            self.save_and_refresh()
    
    def delete_selected_habit(self):
        """Delete the currently selected habit."""
        selected_items = self.habits_list_widget.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.information(self, "Selection Required", "Please select a habit to delete.")
            return
        
        index = self.habits_list_widget.row(selected_items[0])
        self.delete_habit(index)
    
    def reset_all_habits(self):
        """Reset all habits (delete all)."""
        if not self.habits:
            QtWidgets.QMessageBox.information(self, "No Habits", "There are no habits to reset.")
            return
        
        reply = QtWidgets.QMessageBox.question(
            self, "Reset All Habits",
            "Are you sure you want to delete ALL habits? This cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.habits.clear()
            self.save_and_refresh()
            QtWidgets.QMessageBox.information(self, "Reset Complete", "All habits have been deleted.")
    
    def show_context_menu(self, position):
        """Show context menu for habit list items."""
        item = self.habits_list_widget.itemAt(position)
        if not item:
            return
        
        index = self.habits_list_widget.row(item)
        
        menu = QtWidgets.QMenu()
        menu.addAction("Edit Name", lambda: self.edit_habit_name(index))
        menu.addAction("Change Status", lambda: self.change_habit_status(index))
        
        progress_menu = menu.addMenu("Progress")
        progress_menu.addAction("+1 Day", lambda: self.increment_habit_progress(index))
        progress_menu.addAction("-1 Day", lambda: self.decrement_habit_progress(index))
        
        menu.addSeparator()
        menu.addAction("Delete Habit", lambda: self.delete_habit(index))
        
        menu.exec_(self.habits_list_widget.viewport().mapToGlobal(position))
    
    def increment_habit_progress(self, index):
        """Increment completed days for a habit by index."""
        habit = self.habits[index]
        if habit.completed_days < habit.target_days:
            habit.completed_days += 1
            habit.update_status_from_progress()
            self.save_and_refresh()
    
    def decrement_habit_progress(self, index):
        """Decrement completed days for a habit by index."""
        habit = self.habits[index]
        if habit.completed_days > 0:
            habit.completed_days -= 1
            habit.update_status_from_progress()
            self.save_and_refresh()
    
    def select_all_habits(self):
        """Select all habits in the list."""
        self.habits_list_widget.selectAll()
    
    def save_and_refresh(self):
        """Save habits and refresh the display."""
        self.save_habits_to_file()
        self.refresh_habits_display()

    
    def refresh_habits_display(self):
        """Refresh the habit list display."""
        self.habits_list_widget.clear()
        
        total = len(self.habits)
        completed = sum(1 for h in self.habits if h.status == "Completed")
        in_progress = sum(1 for h in self.habits if h.status == "In Progress")
        
        self.stats_label.setText(f"Total Habits: {total} | Completed: {completed} | In Progress: {in_progress}")
        
        for idx, habit in enumerate(self.habits, 1):
            progress_pct = habit.calculate_progress_percentage()
            
            item_text = (f"{idx}. {habit.name} | Status: {habit.status} | "
                        f"Progress: {habit.completed_days}/{habit.target_days} days ({progress_pct}%) | "
                        f"Frequency: {habit.frequency}")
            
            item = QtWidgets.QListWidgetItem(item_text)
            
            if habit.status == "Completed":
                item.setBackground(QtGui.QColor("#c8e6c9"))
            elif habit.status == "In Progress":
                item.setBackground(QtGui.QColor("#ffecb3"))
            else:
                item.setBackground(QtGui.QColor("#ffcdd2"))
                
            self.habits_list_widget.addItem(item)
        
        self.statusBar().showMessage(f"Habits updated: {datetime.now().strftime('%H:%M:%S')}")
        self.update_progress_display()
    
    def update_progress_display(self):
        """Update progress bar based on selected habit."""
        selected_items = self.habits_list_widget.selectedItems()
        if selected_items:
            index = self.habits_list_widget.row(selected_items[0])
            habit = self.habits[index]
            
            self.progress_bar.setMaximum(habit.target_days)
            self.progress_bar.setValue(habit.completed_days)
        else:
            self.progress_bar.setMaximum(100)
            self.progress_bar.setValue(0)
    
    def apply_theme(self, theme="light"):
        """Apply a stylesheet theme."""
        theme_path = os.path.join("styles", f"{theme}_theme.qss")
        if os.path.isfile(theme_path):
            try:
                with open(theme_path, "r", encoding="utf-8") as file:
                    self.setStyleSheet(file.read())
                self.statusBar().showMessage(f"{theme.capitalize()} theme applied")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Style Error", f"Failed to load style: {e}")

    def save_habits_to_file(self):
        """Save habits to JSON file."""
        try:
            with open(self.HABIT_FILE, "w", encoding="utf-8") as file:
                json.dump([habit.to_dict() for habit in self.habits], file, indent=4)
            self.statusBar().showMessage(f"Habits saved: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Save Error", f"Failed to save habits: {e}")
    
    def load_habits_from_file(self):
        """Load habits from JSON file."""
        if os.path.exists(self.HABIT_FILE):
            try:
                with open(self.HABIT_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.habits = [HabitModel.from_dict(h) for h in data]
                self.refresh_habits_display()
                self.statusBar().showMessage(f"Habits loaded: {datetime.now().strftime('%H:%M:%S')}")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Load Error", f"Failed to load habits: {e}")
    
    def export_habits_to_text(self):
        """Export habits as text file."""
        if not self.habits:
            QtWidgets.QMessageBox.information(self, "No Habits", "There are no habits to export.")
            return
        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Habits", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write("DAILY HABIT TRACKER - EXPORTED HABITS\n")
                    file.write(f"Export Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n")
                    
                    for idx, habit in enumerate(self.habits, 1):
                        progress_pct = habit.calculate_progress_percentage()
                        file.write(f"{idx}. {habit.name}\n")
                        file.write(f"   Status: {habit.status}\n")
                        file.write(f"   Progress: {habit.completed_days}/{habit.target_days} days ({progress_pct}%)\n")
                        file.write(f"   Frequency: {habit.frequency}\n")
                        file.write(f"   Created: {habit.created_at}\n\n")
                
                QtWidgets.QMessageBox.information(self, "Export Complete", f"Habits exported to {filename}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Export Error", f"Failed to export habits: {e}")

    def show_about_dialog(self):
        """Show about dialog with application information."""
        about_text = """
        <h2>Daily Habit Tracker</h2>
        <p>A PyQt5 application for tracking daily habits.</p>
        <p><b>Version:</b> 1.0</p>
        <p><b>Created by:</b> Lalu Maulana Rizki Hidayat</p>
        <p><b>Student ID:</b> F1D0231018</p>
        <p>This application was created as a mini project for Visual Programming course.</p>
        """
        
        QtWidgets.QMessageBox.about(self, "About Daily Habit Tracker", about_text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DailyHabitTracker()
    window.show()
    sys.exit(app.exec_())