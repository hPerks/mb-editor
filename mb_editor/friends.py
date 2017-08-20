from mb_editor.utils.lists import flatlist


class Friends:
    def __init__(self, object, adjacent=None):
        self.object = object
        self.adjacent = [] if adjacent is None else adjacent

    def add(self, *friends):
        for friend in flatlist(*friends):
            self.adjacent.append(friend)
            friend.friends.adjacent.append(self.object)

    def remove(self, *friends):
        for friend in flatlist(*friends):
            self.adjacent.remove(friend)
            friend.friends.adjacent_friends.remove(friend)

    def remove_all(self):
        for friend in self.adjacent:
            self.remove(friend)

    @property
    def list(self):
        return list(filter(lambda x: x != self.object, self.__list([])))

    def __list(self, already_found):
        already_found.append(self.object)
        for friend in filter(lambda x: x not in already_found, self.adjacent):
            friend.friends.__list(already_found)
        return already_found

    def __getitem__(self, item):
        if item == "":
            return None

        return next(filter(lambda f: item == f.name, self.list), None)
