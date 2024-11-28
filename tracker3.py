import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CQWW Multiplier Tracker")
        self.setGeometry(100, 100, 600, 400)

        # Create table view
        self.table_view = QTableView(self)
        self.table_view.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table_view)

        # Set up database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("cqww_se0i.db")
        if not self.db.open():
            print("Unable to connect to the database")
            sys.exit(1)

        # Create and set the model
        self.model = QSqlQueryModel(self)
        self.update_model()
        self.table_view.setModel(self.model)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
