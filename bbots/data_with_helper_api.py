import gdata.spreadsheet.service
from google_spreadsheet.api import SpreadsheetAPI
import logging

GOOGLE_SPREADSHEET_USER = "derrick.karimi@gmail.com"
GOOGLE_SPREADSHEET_PASSWORD = "BootyPop!2"
GOOGLE_SPREADSHEET_SOURCE = "bbots"

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Data(object):

    def get_feed(self,query):
        return self.ss.GetCellsFeed(self.ss_key, query=query,
                                    visibility='public', projection='values')

    def query_columns(self):
        """
        The text in the first row is considered to be the name of the column
        """
        query = gdata.spreadsheet.service.CellQuery()
        query.max_row = '1'
        feed = self.get_feed(query)


        cols=[]
        for entry in feed.entry:
            if entry.cell:
                cols.append(entry.cell.text)

        logging.debug("Found columns:" + str(cols))

        return cols


    def query_ids(self):
        """
        Get all the values in the game ID column
        """
        query = gdata.spreadsheet.service.CellQuery()
        col = self.ss_columns.index("id") + 1
        query.min_col = str(col)
        query.max_col = str(col)
        query.min_row = '2'

        feed = self.get_feed(query)
        ids = []
        for entry in feed.entry:
            ids.append(entry.cell.text)
        logging.debug("found ids:" + str(ids))
        return ids

    def load_ss(self):
        logging.debug("Loading spreadsheet")
        self.api = SpreadsheetAPI(GOOGLE_SPREADSHEET_USER,
                                  GOOGLE_SPREADSHEET_PASSWORD,
                                  GOOGLE_SPREADSHEET_SOURCE)
        spreadsheets = self.api.list_spreadsheets()


        self.ss_key = None

        for s in spreadsheets:
            if s[0] == "bbots":
                self.ss_key = s[1]
                break

        self.worksheets = self.api.list_worksheets(self.ss_key)

        self.games_sheet = None

        for w in self.worksheets:
            if w[0] == 'games':
                self.games_sheet = self.api.get_worksheet(
                    self.ss_key, w[1])
                break

        self.games_sheet_rows = self.games_sheet.get_rows()
        logging.debug("table data: " + str(self.games_sheet_rows))
        self.ss_columns = self.games_sheet_rows[0]

        self.ids = []
        for r in self.games_sheet_rows:
            self.ids.append(r['id'])



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

        record = self.games_sheet.get_rows(
            filter_func=lambda row: row['id'] == id)[0]
        logging.debug("ID: " + str(id) + ": " + str(record))

        return record


        feed = self.get_feed(query)

        record = {}
        for i, entry in enumerate(feed.entry):
            if i >= len(self.ss_columns):
                raise Exception("Unknown reason for reading column: " + str(i)
                                + " : " + str(entry.cell.text) + ", for id: " +
                                str(id))

            #logging.debug("Reading column: " + self.ss_columns[i] + " : "
            #              + entry.cell.text)
            header = self.ss_columns[i]
            if is_int(entry.cell.text):
                record[header] = int(entry.cell.text)
            elif is_float(entry.cell.text):
                record[header] = float(entry.cell.text)

            else:
                record[header] = entry.cell.text




        return record

    def record_game_failure(self, id):
        logging.debug("Recording game failure")


    def update_rec(self,rec):

        logging.debug("Updating row: " + str(rec))

        self.games_sheet.update_row(rec)

        return


        query = self.get_record_query(rec['id'])
        cells = self.ss.GetCellsFeed(self.ss_key, query=query,
        #                             visibility='public', projection='values'
        )
        batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()

        for col in range(len(self.ss_columns)):
            cells.entry[col].cell.inputValue = str(rec[self.ss_columns[col]])
            #logging.debug("new value of " + rec['id'] + "[" + self.ss_columns[
            #    col] + "] is: " + str(rec[self.ss_columns[col]]))
            batchRequest.AddUpdate(cells.entry[col])


        updated = self.ss.ExecuteBatch(batchRequest, cells.GetBatchLink().href)
        if updated:
            logging.debug("Updated: " + str(rec['id']))
