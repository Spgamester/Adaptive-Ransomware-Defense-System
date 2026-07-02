from src.ui.modern_gui import ARDSApp
from src.core.monitoring import (
    start_monitoring,
    stop_monitoring,
    monitor_running
)
if __name__ == "__main__":
    app = ARDSApp()
    app.mainloop()