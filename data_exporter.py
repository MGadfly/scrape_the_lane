import csv


class DataExporter(object):

    def write_to_csv(self, header, row_objects):
        filename = 'output.csv'
        values = self._get_rows_from_objects(row_objects)
        rows = [header]
        rows.extend(values)
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    @staticmethod
    def _get_rows_from_objects(row_objects):
        rows = []
        for obj in row_objects:
            rows.append(obj.emit_row())
        return rows
