"""Contains GUI layouts."""

from typing import Any

from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QIcon, QPixmap

from .resources import Traversable, get_svg, root

STYLE_SHEET: Traversable = root / "style_sheet.qss"
"""The style sheet resource.

:meta hide-value:
"""


def get_icon(name: str) -> QIcon:
    """Create a :py:class:`QIcon` from an svg resource.

    Args:
        name: The name of svg resource (without file extension).

    Returns:
        The created :py:class:`QIcon`.
    """
    pixmap = QPixmap()
    pixmap.loadFromData(get_svg(name))
    icon = QIcon()
    icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
    return icon


class Task(QtWidgets.QFrame):
    """Horizontal container that stores information about task."""

    def __init__(
        self,
        description: str,
        time_text: str,
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize task.

        Args:
            description: Task description that will appear on the screen.
            time_text: Task time/due-date that will appear on the screen.
        """
        super().__init__(*args, **kwargs)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)

        self.button = QtWidgets.QToolButton(self)
        self.button.setIcon(get_icon("task"))
        self.button.setProperty("class", "Task")

        self.description = QtWidgets.QLabel(self)
        self.description.setProperty("class", "TaskText")
        self.description.setText(description)

        self.time = QtWidgets.QLabel(self)
        self.time.setProperty("class", "TaskTime")
        self.time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.time.setText(time_text)

        self.horizontal_layout.addWidget(self.button)
        self.horizontal_layout.addWidget(self.description)
        self.horizontal_layout.addWidget(self.time)


class QueueHeader(QtWidgets.QFrame):
    """Horizontal container that stores queue name and control buttons."""

    def __init__(self, queue_name: str, *args: Any, **kwargs: Any):
        """Initialize queue header.

        Args:
            queue_name: Name of queue that will appear on the screen.
        """
        super().__init__(*args, **kwargs)
        self.collapse_queue = QtWidgets.QToolButton(self)
        self.collapse_queue.setIcon(get_icon("queue"))
        self.collapse_queue.setProperty("class", ["QueueHeader", "CollapseQueue"])
        self.name = QtWidgets.QLabel(self)
        self.name.setProperty("class", "QueueName")
        self.name.setText(queue_name)

        self.add_task = QtWidgets.QToolButton(self)
        self.add_task.setIcon(get_icon("add"))
        self.add_task.setProperty("class", "QueueHeader")

        self.more = QtWidgets.QToolButton(self)
        self.more.setIcon(get_icon("more"))
        self.more.setProperty("class", "QueueHeader")

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.addWidget(self.collapse_queue)
        self.horizontal_layout.addWidget(self.name)
        self.horizontal_layout.addWidget(self.add_task)
        self.horizontal_layout.addWidget(self.more)


class Queue(QtWidgets.QFrame):
    """Vertical container that stores tasks organized in a queue."""

    def __init__(self, queue_name: str, *args: Any, **kwargs: Any):
        """Initialize queue.

        Args:
            queue_name: Queue name, will be used to initialize header attribute.
        """
        super().__init__(*args, **kwargs)
        self.vertical_layout = QtWidgets.QVBoxLayout(self)

        self.header = QueueHeader(queue_name, self)
        self.tasks_frame = QtWidgets.QFrame(self)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.tasks_frame.setSizePolicy(size_policy)

        self.vertical_layout.addWidget(self.header)
        self.vertical_layout.addWidget(self.tasks_frame)

        self.vertical_task_layout = QtWidgets.QVBoxLayout(self.tasks_frame)
        task = Task("Task 1", "Time", self.tasks_frame)
        self.vertical_task_layout.addWidget(task, 0, Qt.AlignTop)
        self.vertical_task_layout.addStretch(0)


class AsideWindow(QtWidgets.QMainWindow):
    """Main window of the app."""

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize main window."""
        super().__init__(*args, **kwargs)
        self.resize(653, 612)
        self.setWindowTitle("aside")
        self.setStyleSheet(STYLE_SHEET.read_text())

        self.central_widget = QtWidgets.QWidget(self)
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)

        self.logo = QtWidgets.QLabel(self.central_widget)
        self.logo.setObjectName("Logo")
        pixmap = QPixmap()
        pixmap.loadFromData(get_svg("logo"))
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)

        self.settings = QtWidgets.QToolButton(self.central_widget)
        self.settings.setObjectName("Settings")
        self.settings.setFocusPolicy(Qt.ClickFocus)
        self.settings.setIcon(get_icon("settings"))

        self.search = QtWidgets.QLineEdit(self.central_widget)
        self.search.setPlaceholderText("Search...")
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.search.setSizePolicy(size_policy)

        self.grid_layout.addWidget(self.logo, 0, 0, 1, 2, Qt.AlignCenter)
        self.grid_layout.addWidget(self.settings, 0, 2)
        self.grid_layout.addWidget(self.search, 1, 0, Qt.AlignVCenter)

        queue = Queue("Queue of tasks", self.central_widget)
        self.grid_layout.addWidget(queue, 2, 0, 1, 3)
        self.setCentralWidget(self.central_widget)

        QMetaObject.connectSlotsByName(self)


def main(*argv: str) -> int:  # pragma: no cover
    """Execute the main GUI entrypoint."""
    app = QtWidgets.QApplication(list(argv))
    main_window = AsideWindow()
    main_window.show()
    return app.exec_()
