from report_generator.src.active_report import ActiveReport


def get_active_report(request) -> ActiveReport:
    return ActiveReport.from_year_list(request["cik"], request["years"], request["report_type"])


class QueryEngine:

    @staticmethod
    def retrieve_raw_reports(request: dict) -> dict:
        report = get_active_report(request)

        return {"report": report.json}

    @staticmethod
    def generate_new_report(request: dict) -> dict:
        report = get_active_report(request)

        if request["report_filter"]:
            report = report.filter_report(request["report_filter"])
            return {"report": report}

        return {"report": report.json}
