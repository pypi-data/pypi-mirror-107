from interface import RoseDriverImpl


class RoseDriver(RoseDriverImpl):

    def __init__(self, url, port, auth):
        super(RoseDriver, self).__init__(url, port, auth)

    def get(self, database, collection, identifier) -> dict:
        """
        Sends a "get" request to the websocket and retrieves the requested data

        :param database: database holding the data.
        :type database: str
        :param collection: collection holding the data
        :type collection: str
        :param identifier: name or identifier of the data
        :type identifier: str
        :return: dict converted from JSON
        :rtype: dict
        """
        data = self.loop.run_until_complete(self._get_impl(database, collection, identifier))
        return data

    def add(self, database, collection, identifier, JSON) -> dict:
        """
        Adds an item to the database in the form of an JSON object
        :param database: the database to place the data.
        :type database: str
        :param collection: collection to place the data
        :type collection: str
        :param identifier: name or identifier of the file
        :type identifier: str
        :param JSON: JSON/Dict object to be stored
        :type JSON: dict, JSON
        :return: response [dict]
        :rtype: dict
        """
        data = self.loop.run_until_complete(self._add_impl(database, collection, identifier, JSON))
        return data

    def remove(self, database, collection, identifier, *key) -> dict:
        """
        Removes *keys(value) from the given Item
        :param database: the database of the file containing the key/value to remove.
        :type database: str
        :param collection: collection of the file containing the key/value to remove.
        :type collection: str
        :param identifier: name or identifier of the file containing the key/value to remove.
        :type identifier: str
        :param key: key to remove from the identifier/file
        :type key: any
        :return: dict
        :rtype: dict
        """
        data = self.loop.run_until_complete(self._remove_impl(database, collection, identifier, key))
        return data

    def remove_item(self, database, collection, identifier) -> dict:
        """
        Removes an Identifier/file from a given collection.
        :param database: the database of the file
        :type database: str
        :param collection: collection of the file
        :type collection: str
        :param identifier: name or identifier of the file
        :type identifier: str
        :return: dict
        :rtype: dict
        """
        data = self.loop.run_until_complete(self._remove_item_impl(database, collection, identifier))
        return data

    def remove_Collection(self, database, collection) -> dict:
        data = self.loop.run_until_complete(self._remove_Collection_impl(database, collection))
        return data

    def remove_Database(self, database) -> dict:
        data = self.loop.run_until_complete(self._remove_Database_impl(database))
        return data
