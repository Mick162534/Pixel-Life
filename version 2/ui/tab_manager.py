class TabManager:
    def __init__(self):
        self.active_tab = "SIM"

    def toggle(self):
        self.active_tab = "GRAPH" if self.active_tab == "SIM" else "SIM"
