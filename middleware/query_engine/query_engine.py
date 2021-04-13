from middleware.query_engine.query import Query


def query(request: dict) -> Query:
    return Query() \
        .set_cik(request["cik"]) \
        .set_years(request["years"]) \
        .set_report_type(request["report_type"])


class QueryEngine:

    @staticmethod
    def retrieve_raw_reports(request: dict) -> dict:
        return query(request).run()

    @staticmethod
    def generate_new_report(request: dict) -> dict:
        return query(request).set_filter(request["report_filter"]).run()
