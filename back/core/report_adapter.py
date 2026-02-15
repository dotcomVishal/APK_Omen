class ReportAdapter:

    @staticmethod
    def extract_list(value):

        if value is None:
            return []

        if isinstance(value, list):
            return value

        if isinstance(value, dict):

            combined = []

            for v in value.values():

                if isinstance(v, list):
                    combined.extend(v)

                elif isinstance(v, dict):
                    # Flatten nested dict properly
                    combined.extend([str(x) for x in v.keys()])

                else:
                    combined.append(str(v))

            return combined

        return [str(value)]

    @staticmethod
    def normalize(raw_data):

        report = {
            "app_name": raw_data.get("app_name"),
            "package": raw_data.get("package"),

            "permissions": ReportAdapter.extract_list(
                raw_data.get("permissions")
            )[:20],

            "exported_components": ReportAdapter.extract_list(
                raw_data.get("exported_components")
            )[:20],

            "network_indicators": ReportAdapter.extract_list(
                raw_data.get("network_indicators")
            )[:20],

            "crypto_indicators": ReportAdapter.extract_list(
                raw_data.get("crypto_indicators")
            )[:20],

            "secrets_indicators": ReportAdapter.extract_list(
                raw_data.get("secrets_indicators")
            )[:20],

            "insecure_configs": ReportAdapter.extract_list(
                raw_data.get("insecure_configs")
            )[:20],
        }

        return report


def normalize_report(raw_data):
    return ReportAdapter.normalize(raw_data)
