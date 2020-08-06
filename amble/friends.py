from amble.utils.lists import flatlist


class Friends:
    def __init__(self, object, adjacent=None):
        self.object = object
        self.adjacent = [] if adjacent is None else adjacent

    def add(self, *friends):
        for friend in flatlist(*friends):
            self.adjacent.append(friend)
            friend.friends.adjacent.append(self.object)

    def remove_all(self):
        for friend in self.adjacent:
            if self in friend.friends.adjacent:
                friend.friends.adjacent.remove(self)
        self.adjacent = []

    @property
    def list(self):
        return list(filter(lambda x: x != self.object, self.__list([])))

    def __list(self, already_found):
        already_found.append(self.object)
        for friend in filter(lambda x: x not in already_found, self.adjacent):
            friend.friends.__list(already_found)
        return already_found

    def __getitem__(self, item):
        if item == '':
            return None

        return next(filter(lambda f: item == f.id, self.list), None)
