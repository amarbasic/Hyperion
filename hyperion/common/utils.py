"""Utils functions"""
import re


def underscore(word):
    """
    Make an underscored, lowercase form from the expression in the string.
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", word)
    word = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", word)
    word = word.replace("-", "_")
    return word.lower()


def paginated_args(query_params):
    """Get pagianted arguments from reuqest"""
    return {
        "page": query_params.get("page", 1, type=int),
        "page_size": query_params.get("pageSize", 10, type=int),
        "sort_by": query_params.get("sortBy", type=str),
        "sort_order": query_params.get("sortOrder", "asc", type=str),
        "retreive_all": query_params.get("retreiveAll", 0, type=int),
    }


def parse_bool(value):
    """Parse bool field"""
    if value is None:
        return None

    return True if value > 0 else False
