# This file is part of Tryton.  The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta


class AssetLine(metaclass=PoolMeta):
    __name__ = 'account.asset.line'
    company = fields.Function(
        fields.Many2One('company.company', "Company"),
        'on_change_with_company', searcher='searcher_company')

    @fields.depends('asset', '_parent_asset.company')
    def on_change_with_company(self, name=None):
        if self.asset and self.asset.company:
            return self.asset.company.id

    @classmethod
    def searcher_company(cls, name, clause):
        Asset = Pool().get('account.asset')

        asset = Asset.__table__()
        line = cls.__table__()

        Operator = fields.SQL_OPERATORS[clause[1]]
        sql_where = Operator(asset.company, clause[2])
        query = asset.join(line, type_='LEFT',
            condition=asset.id == line.asset).select(line.id, where=sql_where)
        return [('id', 'in', query)]
