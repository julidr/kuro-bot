import datetime
from unittest.mock import Mock

from requests import HTTPError

from karthuria.client import KarthuriaClient
from karthuria.model.event import Event
from karthuria.repository.event_repository import EventRepository


class TestLoadEvents:

    def test_when_events_load_successful(self, event):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_events.return_value = [event]
        repository = EventRepository(mock_client)

        # Act
        response = repository.events

        # Assert
        assert len(response) == 1
        assert response[0].event_id == 1

    def test_when_events_load_unsuccessful(self):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_events.side_effect = HTTPError('Ups')
        repository = EventRepository(mock_client)

        # Act
        response = repository.events

        # Assert
        assert len(response) == 0


class TestGetCurrentEvents:

    def test_when_all_events_are_present(self, complete_current_events):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_current_events.return_value = complete_current_events
        repository = EventRepository(mock_client)

        # Act
        response = repository.get_current_events()

        # Assert
        assert response is not None
        assert len(response) != 0
        assert 'events' in response
        assert response['events'][0].event_id == 1
        assert 'challenges' in response
        assert response['challenges'][0].event_id == 2
        assert 'bosses' in response
        assert response['bosses'][0].event_id == 3

    def test_when_current_events_are_unsuccessful(self):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_current_events.side_effect = HTTPError('Ups')
        repository = EventRepository(mock_client)

        # Act
        response = repository.get_current_events()

        # Assert
        assert len(response) == 0


class TestGetEventNameById:

    def test_when_event_is_found(self, event):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_events.return_value = [event]
        repository = EventRepository(mock_client)
        expected_name = 'Event Test'

        # Act
        response = repository.get_event_name_by_id(1)

        # Assert
        assert response == expected_name

    def test_when_event_is_not_found(self, event):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_events.return_value = [event]
        repository = EventRepository(mock_client)

        # Act
        response = repository.get_event_name_by_id(2)

        # Assert
        assert response is None


class TestReloadEvents:

    def test_when_new_data_is_added(self, event):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        new_event = Event(2, name='Event Test 2', end_date=datetime.datetime.now().timestamp(),
                          start_date=datetime.datetime.now().timestamp())
        mock_client.get_events.return_value = [event]
        repository = EventRepository(mock_client)
        mock_client.get_events.return_value = [event, new_event]

        # Act
        repository.reload_events()
        response = repository.events

        # Assert
        assert len(response) == 2
        assert response[1].event_id == 2

    def test_when_data_is_the_same(self, event):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_events.return_value = [event]
        repository = EventRepository(mock_client)

        # Act
        repository.reload_events()
        response = repository.events

        # Assert
        assert len(response) == 1
        assert response[0].event_id == 1
