import gdata.spreadsheet.service


class Data(object):

    def query_columns(self):
        """
        The text in the first row is considered to be the name of the column
        """
        query = gdata.spreadsheet.service.CellQuery()
        query.max_row = '2'
        feed = self.ss.GetCellsFeed(self.ss_key, query=query)

        cols=[]
        for entry in feed.entry:
            cols.append(entry.cell.inputValue)
        return cols


    def query_ids(self):
        """
        Get all the values in the game ID column
        """
        query = gdata.spreadsheet.service.CellQuery()
        col = self.ss_columns.index("id") + 1
        query.min_col = str(col)
        query.max_col = str(col)
        query.min_ro1 = '2'

        feed = self.ss.GetCellsFeed(self.ss_key, query=query)
        ids = []
        for entry in feed.entry:
            ids.append(entry.cell.inputValue)
        return ids

    def load_ss(self):
        self.ss_key = '0AlItClzrqP_edHoxMmlOcTV3NHJTbU4wZDJGQXVTTXc'
        self.ss = gdata.spreadsheet.service.SpreadsheetsService()
        self.ss.ProgrammaticLogin()
        self.ss_columns = self.query_columns()
        self.ids = self.query_ids()
        self.games = {}
        for id in self.ids:
            self.games[id] = { 'failures'  :   0}



    def __init__(self, con):
        self.con = con
        self.ss_columns = None
        self.ss_key = None
        self.ss = None
        self.ids = None
        self.load_ss()


    def get_record(self, id):
        """
        Get a dictionary, keys are spreadsheet headers, values are entries
        in the cell for the row specified by id
        """
        row = self.ids.index(id) + 2

        query = gdata.spreadsheet.service.CellQuery()
        query.min_row = str(row)
        query.max_row = str(row)

        feed = self.ss.GetCellsFeed(self.ss_key, query=query)

        record = {}
        for i, entry in enumerate(feed.entry):
            header = self.ss_columns[i]
            record[header] = entry.cell.inputValue

        return record


    def gen_rows(self, i):
        'rows generator'
        for x in range(1, i):
            yield [x, x * x, x * x * x]

    def record_game_failure(self, id):
        self.games[id]['failures'] += 1


