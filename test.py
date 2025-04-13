import unittest
from unittest.mock import Mock, patch
from PySide6.QtWidgets import QApplication
from sqlalchemy.orm import Session
from datetime import date
from admin_p import AdminPanel, Application, ApplicationStatus

class TestApproveApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Инициализация QApplication для тестирования GUI
        cls.app = QApplication([])

    def setUp(self):
        # Создаем экземпляр AdminPanel
        self.panel = AdminPanel()
        # Заменяем session на мок, имитирующий SQLAlchemy Session
        self.panel.session = Mock(spec=Session)
        self.mock_session = self.panel.session
        # Настраиваем мок для query
        self.mock_session.query = Mock()
        # Отключаем вызов closeEvent для предотвращения ошибок
        self.panel.closeEvent = Mock()
        # Устанавливаем текущую страницу
        self.panel.current_page = 1

    def tearDown(self):
        # Очистка без вызова close(), так как closeEvent замокан
        pass

    def test_approve_application_success(self):
        # Подготовка тестовых данных
        mock_app = Application(
            application_id=1,
            user_id=12345,
            start_date=date(2025, 5, 1),
            end_date=date(2025, 5, 10),
            type="отпуск",
            status=ApplicationStatus.PENDING
        )
        mock_user = Mock()
        mock_user.user_id = 12345

        # Настройка мока для query в approve_application
        mock_query = Mock()
        mock_query.filter_by.return_value.first.return_value = mock_app

        # Настройка мока для show_applications
        mock_show_query = Mock()
        mock_show_query.join.return_value.filter.return_value.limit.return_value.offset.return_value.all.return_value = [(mock_app, mock_user)]
        self.mock_session.query.side_effect = [mock_query, mock_show_query]

        # Мок для notify_user и show_applications
        with patch("admin_p.notify_user") as mock_notify:
            with patch.object(self.panel, "show_applications") as mock_show_applications:
                # Вызов метода
                self.panel.approve_application(1)

                # Проверки
                self.assertEqual(mock_app.status, ApplicationStatus.APPROVED)
                self.mock_session.commit.assert_called_once()
                mock_notify.assert_called_once_with(1, ApplicationStatus.APPROVED)
                mock_show_applications.assert_called_once_with(1)

    def test_approve_application_already_processed(self):
        # Подготовка тестовых данных
        mock_app = Application(
            application_id=1,
            user_id=12345,
            start_date=date(2025, 5, 1),
            end_date=date(2025, 5, 10),
            type="отпуск",
            status=ApplicationStatus.APPROVED  # Заявка уже одобрена
        )
        mock_query = Mock()
        mock_query.filter_by.return_value.first.return_value = mock_app
        self.mock_session.query.return_value = mock_query

        # Мок для QMessageBox
        with patch("PySide6.QtWidgets.QMessageBox.warning") as mock_warning:
            # Вызов метода
            self.panel.approve_application(1)

            # Проверки
            self.assertEqual(mock_app.status, ApplicationStatus.APPROVED)  # Статус не изменился
            self.mock_session.commit.assert_not_called()
            mock_warning.assert_called_once()

    def test_approve_application_not_found(self):
        # Подготовка тестовых данных
        mock_query = Mock()
        mock_query.filter_by.return_value.first.return_value = None  # Заявка не найдена
        self.mock_session.query.return_value = mock_query

        # Мок для QMessageBox
        with patch("PySide6.QtWidgets.QMessageBox.warning") as mock_warning:
            # Вызов метода
            self.panel.approve_application(1)

            # Проверки
            self.mock_session.commit.assert_not_called()
            mock_warning.assert_called_once()

    @classmethod
    def tearDownClass(cls):
        # Очистка QApplication
        cls.app.quit()

if __name__ == "__main__":
    unittest.main()