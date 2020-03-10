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


def camelize(string, uppercase_first_letter=True):
    """
    Convert strings to CamelCase.
    """
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    else:
        return string[0].lower() + camelize(string)[1:]


def paginated_args(request):
    """Get pagianted arguments from reuqest"""
    return {
        "page": request.args.get("page", 1, type=int),
        "page_size": request.args.get("page_size", 10, type=int),
        "sort_by": request.args.get("sortBy", type=str),
        "sort_order": request.args.get("sortOrder", "asc", type=str),
    }


def parse_bool(value):
    """Parse bool field"""
    return True if value > 0 else False
