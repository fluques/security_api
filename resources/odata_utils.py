from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select

def apply_odata_query_with_pagination(model, filter, order_by, pagination_parameters):
    """
    Applies OData query with pagination to the SQLAlchemy ORM query.

    Args:
        orm_query: SQLAlchemy ORM query to apply the OData query to.
        filter: OData filter string.
        order_by: OData order by string.
        pagination_parameters: Pagination parameters for the query.

    Returns:
        The modified ORM query with applied OData filter, order_by and pagination.
    """
    orm_query = model.query
    if filter:
        orm_query = apply_odata_query(orm_query, filter)

    if order_by:
        sort_criteria = []
        for item in order_by.split(','):
            item = item.strip()
            if 'desc' in item.lower():
                field, direction = item.split(' ', 1)
                sort_criteria.append(getattr(model, field).desc())
            elif 'asc' in item.lower():
                field, direction = item.split(' ', 1)
                sort_criteria.append(getattr(model, field).asc())
            else:
                sort_criteria.append(getattr(model, item))
        orm_query = orm_query.order_by(*sort_criteria)

    return orm_query.limit(pagination_parameters.page_size).offset(
        (pagination_parameters.page - 1) * pagination_parameters.page_size
    )
