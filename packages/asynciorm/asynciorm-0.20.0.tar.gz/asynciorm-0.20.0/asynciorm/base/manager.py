import copy
import re
from asynciorm.exceptions import DoesNotExist, MultipleObjectsReturned
from asynciorm.base.fields import Field


class BaseManager(object):

    def __init__(self, connector):
        self._connector = connector

    def __call__(self, model):
        self.model = object.__new__(model)
        self._names_fields = self.model._names_fields
        self._query = """ SELECT {distinct}  {columns} FROM {table_name} {filter_values} {order_by} {limit}"""
        self._query_params = {
            'filter_values': '',
            'distinct': '',
            'limit': ' ',
            'order_by': '',
            'columns': ', '.join(self._names_fields),
            'table_name': self.model.table_name

        }
        return self

    @property
    def query(self):
        return re.sub(' +', ' ', self._query.format(**self._query_params))

    async def fetchone(self):
        raise NotImplementedError

    async def fetchall(self):
        raise NotImplementedError

    async def execute(self):
        raise NotImplementedError

    async def fetch_row(self):
        raise NotImplementedError

    async def create(self, **model_data):
        self._query = f""" INSERT INTO {self.model.table_name} ( {await self._get_insert_column_name(**model_data)} ) VALUES ( {await self._get_insert_data(**model_data)} )"""
        await self.execute()

    async def delete(self):
        self._query = """ DELETE FROM {table_name} {filter_values}"""
        await self.execute()

    async def update(self, **model_data):
        self._query = """ UPDATE {table_name} SET {columns} {filter_values}"""
        data = "{key}='{value}'"
        self._query_params['columns'] = ', '.join([data.format(key=key + '_id',
                                                               value=model_data.get(key)) if self.model._fields.get(
            key, Field()).is_fk else data.format(key=key, value=model_data.get(key)) for key in model_data.keys()])
        await self.execute()

    async def aggregate(self, *funcs):
        self._query_params['columns'] = ', '.join([func.sql() for func in funcs])
        result = await self.fetchone()
        return {f"{func.column_name}_{func.__class__.__name__.lower()}": result[key] for key, func in enumerate(funcs)}

    async def all(self):
        return [await self._get_query_model(self.model, self._names_fields, row) for row in
                await self.fetchall()]

    async def get(self, **params):
        self._filter_options(**params)
        result = await self.fetchall()
        if not result:
            raise DoesNotExist
        elif len(result) > 1:
            raise MultipleObjectsReturned
        return await self._get_query_model(self.model, self._names_fields, result[0])

    async def get_or_none(self, **params):
        try:
            return await self.get(**params)
        except (DoesNotExist, MultipleObjectsReturned):
            return None

    async def fetch(self):
        return [await self._get_query_model(self.model, self._names_fields, row) for row in
        await self.fetchall()]

    async def first(self):
        self.limit(1)
        data = await self.fetchone()
        if not data:
            raise DoesNotExist
        return await self._get_query_model(self.model, self._names_fields, data)

    async def last(self):
        self.limit(1)
        self.order_by(f"-{[field_name for field_name, field in self.model._fields.items() if field.is_primary_key][0]}")
        data = await self.fetchone()
        if not data:
            raise DoesNotExist
        return await self._get_query_model(self.model, self._names_fields, data)

    async def row(self, query):
        return await self.fetch_row(query)

    def filter(self, **params):
        self._filter_options(**params)
        return self

    def distinct(self, column):
        self._query_params['distinct'] = f' DISTINCT {column} '
        return self

    def order_by(self, field):
        self._query_params[
            'order_by'] = f' ORDER BY {field + " ASC " if not field.startswith("-") else field[1:] + " DESC "} '
        return self

    def limit(self, limit):
        self._query_params['limit'] = f' LIMIT {limit} '
        return self

    def _in_list(self, column_name, values, or_=False):
        values = ', '.join([f"'{value}'" for value in values])
        self._query_params[
            'filter_values'] += f" {' OR ' if or_ else ' AND '} {column_name} IN ({values}) "

    def _not_in_list(self, column_name, values, or_=False):
        values = ', '.join([f"'{value}'" for value in values])
        self._query_params[
            'filter_values'] += f" {' OR ' if or_ else ' AND '} {column_name} NOT IN ({values}) "

    def _between(self, column_name, values, or_=False):
        values = (f"'{values[0]}'", f"'{values[1]}'")
        self._query_params[
            'filter_values'] += f" {' OR ' if or_ else ' AND '} {column_name} BETWEEN {values[0]} AND {values[1]} "

    def _not_between(self, column_name, values, or_=False):
        values = (f"'{values[0]}'", f"'{values[1]}'")
        self._query_params[
            'filter_values'] += f" {' OR ' if or_ else ' AND '} {column_name} NOT BETWEEN {values[0]} AND {values[1]} "

    def _like(self, column_name, exp, or_=False):
        self._query_params['filter_values'] += f' {" OR " if or_ else " AND "} {column_name} LIKE "%{exp}%"'

    def _not_like(self, column_name, exp, or_=False):
        self._query_params['filter_values'] += f' {" OR " if or_ else " AND "} {column_name} NOT LIKE "%{exp}%"'

    def _isnull(self, column_name, value, or_=False):
        self._query_params[
            'filter_values'] += f" {' OR ' if or_ else ' AND '} {column_name} IS {' NULL ' if value else ' NOT NULL '}"

    def _lte(self, column_name, value, or_=False):
        self._query_params['filter_values'] += f' {" OR " if or_ else " AND "} {column_name} <= "{value}"'

    def _gte(self, column_name, value, or_=False):
        self._query_params['filter_values'] += f'  {" OR " if or_ else " AND "} {column_name} >= "{value}"'

    def _gt(self, column_name, value, or_=False):
        self._query_params['filter_values'] += f'  {" OR " if or_ else " AND "} {column_name} > "{value}"'

    def _lt(self, column_name, value, or_=False):
        self._query_params['filter_values'] += f' {" OR " if or_ else " AND "} {column_name} < "{value}"'

    async def _get(self, model, names, **params):
        query = f""" SELECT {', '.join(names)} FROM {model.table_name} WHERE {' AND '.join(await self._get_query_filter_params(**params))}"""
        cursor = await self._connector.execute(query)
        return await cursor.fetchone()

    async def _get_related_model(self, parent_model, fk_field_name):
        fk_field = parent_model._fields.get(fk_field_name)
        return fk_field._related_model

    async def _is_related_field(self, model, attr):
        return model._fields.get(attr, Field()).is_fk

    async def _get_query_model(self, model, attrs, attr_values):
        model = copy.copy(model)
        for attr, attr_value in zip(attrs, attr_values):
            if attr.endswith('_id') and await self._is_related_field(model, attr.replace('_id', '')):
                related_model = await self._get_related_model(model, attr.replace('_id', ''))
                names = related_model._names_fields
                related_object = await self._get_query_model(related_model, names,
                                                             await self._get(related_model, names, id=attr_value))
                setattr(model, attr.replace('_id', ''), related_object)
            setattr(model, attr,
                    model._fields.get(attr).sql_load(attr_value) if model._fields.get(attr) else attr_value)
        return model

    async def _get_query_filter_params(self, **params):
        return [
            f"{key}={self.model._fields.get(key if not key.endswith('_id') else key.replace('_id', '')).sql_dump(value)}"
            for key, value in params.items()]

    async def _get_insert_data(self, **model_data):
        insert_data = []
        for field_name, field in self.model._fields.items():
            if not field.is_primary_key:
                if model_data.get(field_name) is None:
                    if field.default_value is None:
                        if field.is_nullable:
                            continue
                        raise ValueError(f"Field {field_name} can't be null")
                    insert_data.append(field.sql_dump(field.default_value))
                else:
                    insert_data.append(field.sql_dump(model_data.get(field_name)))

        return ', '.join(insert_data)

    async def _get_insert_column_name(self, **model_data):
        column_names = []
        for field_name, field in self.model._fields.items():
            if not field.is_primary_key and (model_data.get(field_name) is not None or field.default_value is not None):
                if field.is_fk:
                    column_names.append(field_name + '_id')
                else:
                    column_names.append(field_name)
        return ', '.join(column_names)

    def _filter_options(self, **params):
        if not self._query_params['filter_values']:
            self._query_params['filter_values'] = 'WHERE  '
        for param_name, param_value in params.items():
            custom_query_params = param_name.split('__')
            param_name = custom_query_params.pop(0)
            if custom_query_params:
                for custom_query_param in custom_query_params:
                    query_filter = getattr(self,
                                           '_' + custom_query_param.replace('or_', '') if custom_query_param.startswith(
                                               'or_') else '_' + custom_query_param, None)
                    if query_filter:
                        query_filter(param_name, param_value, or_=custom_query_param.startswith('or_'))
            else:
                self._query_params['filter_values'] += f" AND {param_name}='{param_value}' "
            self._query_params['filter_values'] = re.sub(' +', ' ', self._query_params['filter_values']).replace(
                'WHERE OR',
                'WHERE').replace(
                'WHERE AND', 'WHERE')
