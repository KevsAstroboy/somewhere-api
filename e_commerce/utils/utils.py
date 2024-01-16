class Utils:

    def is_empty_list(my_list: list) -> bool:
        return not my_list or len(my_list) == 0

    def is_not_empty_list(my_list: list) -> bool:
        return not list.is_empty_list(my_list)

    def is_blank(string: str) -> bool:
        return not string or len(string) == 0

    def is_not_blank(string: str) -> bool:
        return not str.is_blank(string)