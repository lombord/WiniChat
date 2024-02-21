from django.db.models import Lookup, Field


@Field.register_lookup
class AnyOP(Lookup):
    lookup_name = "any"

    def as_sql(self, compiler, connection):
        lhs, params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params.extend(rhs_params)
        return "%s = ANY(array(%s))" % (lhs, rhs), params
