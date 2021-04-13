
"""
Class Query is and query from a user to generate gather reports.
When they set a new property, it returns a new object so they can
chain queries.

ToDo: Math, Aggregates, Ect...
"""
from report_generator.src.active_report import ActiveReport


class Query(object):
    def __init__(self):
        self.cik = ""
        self.years = []
        self.report_type = ""
        self.report_filter = None

    def set_cik(self, cik: str) -> object:
        self.cik = cik
        return self

    def set_years(self, years: list) -> object:
        self.years = years
        return self

    def set_report_type(self, report_type: str) -> object:
        self.report_type = report_type
        return self

    def set_filter(self, report_filter: dict) -> object:

        self.report_filter = report_filter
        return self

    def run(self) -> dict:
        report = ActiveReport.from_year_list(
            self.cik, self.years, self.report_type)

        if self.report_filter:
            report = report.filter_report(self.report_filter)
            return {"report": report}

        return {"report": report.json}
