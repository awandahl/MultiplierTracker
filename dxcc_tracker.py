from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QTableView, QVBoxLayout
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt6.QtCore import Qt

class CustomSqlModel(QSqlQueryModel):
    def data(self, index, role):
        if role == Qt.BackgroundRole:
            column = index.column()
            if column < 7:  # Columns 0-6 (CountryPrefix and band columns)
                value = super().data(index, Qt.DisplayRole)
                if value and isinstance(value, (int, float)) and value > 0:
                    return QBrush(QColor(144, 238, 144))  # Light green color
                elif value == 0:
                    return QBrush(QColor(255, 200, 200))  # Light red color
        return super().data(index, role)

class DXCCTrackerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DXCC Multiplier Tracker")
        self.setGeometry(100, 100, 600, 400)

        # Create table view
        self.table_view = QTableView(self)
        self.table_view.verticalHeader().setVisible(False)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)

        # Set up database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.update_database_connection()

        # Create and set the model
        self.model = CustomSqlModel(self)
        self.update_model()
        self.table_view.setModel(self.model)

    def update_database_connection(self):
        # This method should be called to update the database connection when the active contest changes in not1mm
        current_db = self.get_current_database()
        self.db.setDatabaseName(current_db)
        if not self.db.open():
            print("Unable to connect to the database")

    def get_current_database(self):
        # Implement this method to get the current database path from not1mm
        # This is just a placeholder
        return "path/to/current/database.db"

    def update_model(self):
        query = QSqlQuery(self.db)
        query.prepare("""
        SELECT CountryPrefix,
            SUM(CASE WHEN Band = 1.8 THEN 1 ELSE 0 END) AS '160m',
            SUM(CASE WHEN Band = 3.5 THEN 1 ELSE 0 END) AS '80m',
            SUM(CASE WHEN Band = 7.0 THEN 1 ELSE 0 END) AS '40m',
            SUM(CASE WHEN Band = 14.0 THEN 1 ELSE 0 END) AS '20m',
            SUM(CASE WHEN Band = 21.0 THEN 1 ELSE 0 END) AS '15m',
            SUM(CASE WHEN Band = 28.0 THEN 1 ELSE 0 END) AS '10m',
            COUNT(*) AS Total
        FROM DXLOG
        GROUP BY CountryPrefix
        ORDER BY Total DESC
        """)
        if not query.exec():
            print("Query failed:", query.lastError().text())
        else:
            self.model.setQuery(query)
            self.model.setHeaderData(0, Qt.Horizontal, "DXCC")
