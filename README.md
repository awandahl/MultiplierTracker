# MultiplierTracker

```
sqlite3 cqww_se0i.db ".dump table_name" > table_output.sql
sqlite3 cqww_se0i.db ".schema" > structure.sql
```

### Database Query
Create a SQL query to extract the required information:

```
SELECT CountryPrefix, Band, COUNT(*) as QSO_Count 
FROM DXLOG 
GROUP BY CountryPrefix, Band 
ORDER BY CountryPrefix, Band;
```

This query will give us a list of CountryPrefixes, Bands, and the number of QSOs for each combination.

### QT6 Implementation
To integrate this into the not1mm project, we'll create a new window class:

```
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import sqlite3

class MultiplierTracker(QWidget):
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle('Multiplier Tracker')
        self.updateData()

    def updateData(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT CountryPrefix, Band, COUNT(*) as QSO_Count 
            FROM DXLOG 
            GROUP BY CountryPrefix, Band 
            ORDER BY CountryPrefix, Band
        """)
        data = cursor.fetchall()
        conn.close()

        unique_bands = sorted(set(row[1] for row in data))
        unique_countries = sorted(set(row[0] for row in data))

        self.table.setRowCount(len(unique_countries))
        self.table.setColumnCount(len(unique_bands) + 1)
        self.table.setHorizontalHeaderLabels(['Country'] + [str(band) for band in unique_bands])

        for row, country in enumerate(unique_countries):
            self.table.setItem(row, 0, QTableWidgetItem(country))
            for col, band in enumerate(unique_bands, start=1):
                count = next((d[2] for d in data if d[0] == country and d[1] == band), 0)
                item = QTableWidgetItem(str(count))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if count > 0:
                    item.setBackground(Qt.GlobalColor.green)
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
```

### Integration with not1mm
To integrate this into the main not1mm application:

- Add a new menu item or button in the main window to open the Multiplier Tracker.
- When the user clicks this item, create and show the MultiplierTracker window.

Example of how to add this to the main window:

```
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction
from multiplier_tracker import MultiplierTracker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ... existing code ...

        menubar = self.menuBar()
        viewMenu = menubar.addMenu('View')
        multiplierAction = QAction('Multiplier Tracker', self)
        multiplierAction.triggered.connect(self.showMultiplierTracker)
        viewMenu.addAction(multiplierAction)

    def showMultiplierTracker(self):
        self.multiplierTracker = MultiplierTracker('cqww_se0i.db')
        self.multiplierTracker.show()
```

This implementation will create a table where:

- Each row represents a country (CountryPrefix)
- Each column represents a band
- Cells contain the number of QSOs for that country-band combination
- Cells with QSOs are highlighted in green

Further enhancements:

- Adding a refresh button to update the data
- Implementing sorting functionality
- Adding filters for specific bands or countries
- Displaying additional information like the last QSO date for each combination

