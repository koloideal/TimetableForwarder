class TooLongQueryForSearchError(ValueError):
    def __init__(self, len_of_query: int) -> None:
        self.__len_of_query: int = len_of_query

    def __str__(self) -> str:
        return f"Too long query for search {self.__len_of_query} > 25"