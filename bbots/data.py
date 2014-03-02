import gdata.spreadsheet.service
import logging


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
        self.ss_key = '0AlItClzrqP_edHoxMmlOcTV3NHJTbU4wZDJGQXVTTXc'
        self.ss = gdata.spreadsheet.service.SpreadsheetsService()
        n3="myers"
        n1="dr"
        n2="randy"
        p4="password"
        uname='.'.join([n1,n2,n3])
        self.ss.email = "@".join([uname,'gmail.com'])
        self.ss.password = '.'.join([uname, p4])
        self.ss.source = 'bbots'
        self.ss.ProgrammaticLogin()

        self.ss_columns = self.query_columns()
        self.ids = self.query_ids()


    def __init__(self, con):
        self.con = con
        self.ss_columns = None
        self.ss_key = None
        self.ss = None
        self.ids = None
        self.load_ss()


    def get_record_query(self, rec_id):
        row = self.ids.index(rec_id) + 2
        query = gdata.spreadsheet.service.CellQuery()
        query.min_row = str(row)
        query.max_row = str(row)
        return query

    def get_record(self, id):
        """
        Get a dictionary, keys are spreadsheet headers, values are entries
        in the cell for the row specified by id
        """

        query = self.get_record_query(id)

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




        logging.debug("ID: " + str(id) + ": " + str(record))
        return record

    def record_game_failure(self, id):
        logging.debug("Recording game failure")


    def update_rec(self,rec):


        logging.debug("Updating row: " + str(rec))

        query = self.get_record_query(rec['id'])
        cells = self.ss.GetCellsFeed(self.ss_key, query=query,
        #                             visibility='public', projection='values'
        )
        batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()

        n = 0
        for col in range(len(self.ss_columns)):
            rhs = str(rec[self.ss_columns[col]])

            if (cells.entry[col].cell.inputValue != rhs):

                cells.entry[col].cell.inputValue = rhs
                #logging.debug("new value of " + rec['id'] + "[" + self.ss_columns[
                #    col] + "] is: " + rhs)
                batchRequest.AddUpdate(cells.entry[col])
                n = n + 1


        updated = self.ss.ExecuteBatch(batchRequest, cells.GetBatchLink().href)
        if updated:
            logging.debug("Updated (" + str(n) + ") cells for id: " + str(rec[
                'id']))
