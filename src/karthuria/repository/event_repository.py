import logging

from requests import HTTPError

from karthuria.client import KarthuriaClient

LOG_ID = "EventRepository"


class EventRepository:
    """
    Repository with the information of events
    """

    def __init__(self, client: KarthuriaClient):
        self.client = client
        self.events = self.__load_events()

    def get_event_name_by_id(self, event_id: str) -> str:
        """
        Search for the name of an event based on the given id.

        :param event_id: Id of the event to search
        :return: The name of the event
        """
        for event in self.events:
            if str(event.event_id) == str(event_id):
                return event.name

    def get_current_events(self) -> dict:
        """
        Calls Karthuria API to get current ongoing events

        :return: A dict with the different type of ongoing events, like bosses or challenges
        """
        current_events = {}
        try:
            current_events = self.client.get_current_events()
            logging.debug('[{0}] - Current Events retrieved successfully'.format(LOG_ID))
        except HTTPError as error:
            logging.error("[{0}] - Couldn't retrieve current events {1}".format(LOG_ID, error))
        return current_events

    def reload_events(self) -> None:
        """
        Refresh the current event information of the API into the EventRepository.
        This is a measure to keep data updated.

        :return: None
        """
        self.events = self.__load_events()

    def __load_events(self) -> list:
        """
        Calls Karthuria API to get all events information, mostly its names

        :return: A list with events names and ids
        """
        events = []
        try:
            events = self.client.get_events()
            logging.debug('[{0}] - Events retrieved successfully'.format(LOG_ID))
        except HTTPError as error:
            logging.error("[{0}] - Couldn't retrieve events {1}".format(LOG_ID, error))
        return events
