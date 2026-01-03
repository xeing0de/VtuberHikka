class UI:
    def __init__(self, window):
        self.window = window
    
    def load_project(self):
        self.window.left_panel.image.setText("1123")

    def work_space(self):
        w = self.window.right_panel.sp_w.value()
        h = self.window.right_panel.sp_h.value()
        self.window.left_panel.update_output_rect(w, h)
