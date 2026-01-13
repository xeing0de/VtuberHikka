import os

from PySide6.QtWidgets import QFileDialog, QMessageBox

from objects import Project, ImageObject, TextObject

class UI:
    def __init__(self, window):
        self.window = window

    def create_text(self):
        project = self.window.project

        obj = TextObject()

        project.add_item(obj)
        self.window.left_panel.scene.addItem(obj)
        self.window.left_panel.on_items_changed()

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Load Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp);;All Files (*.*)",
        )
        if not file_path:
            return

        try:
            image = ImageObject(file_path)
        except Exception as e:
            QMessageBox.critical(self.window, "Load error", str(e))
            return
        
        self.window.project.add_item(image)
        self.window.left_panel.scene.addItem(image)
        self.window.left_panel.on_items_changed()

    def load_project(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Load Project",
            "",
            "Project JSON (*.json);;All Files (*.*)",
        )
        if not file_path:
            return

        try:
            project = Project.load_json(file_path)
        except Exception as e:
            QMessageBox.critical(self.window, "Load error", str(e))
            return

        self.window.project = project
        self.window.left_panel.set_project(project)
        self.window.right_panel.project = project

    def save_project(self):
        project = self.window.project

        suggested_name = (project.name).strip()
        suggested_path = f"{suggested_name}.json"

        file_path, _ = QFileDialog.getSaveFileName(
            self.window,
            "Save Project",
            suggested_path,
            "Project JSON (*.json);;All Files (*.*)",
        )
        if not file_path:
            return

        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if base_name:
            project.name = base_name

        if not file_path.lower().endswith(".json"):
            file_path += ".json"

        try:
            project.save_json(file_path)
        except Exception as e:
            QMessageBox.critical(self.window, "Save error", str(e))


    def work_space(self):
        w = self.window.right_panel.sp_w.value()
        h = self.window.right_panel.sp_h.value()
        self.window.left_panel.update_output_rect(w, h)
