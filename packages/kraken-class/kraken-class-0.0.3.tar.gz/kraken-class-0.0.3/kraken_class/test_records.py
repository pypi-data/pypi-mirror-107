class Test_records:
    """ SHORT DESCRIPTION OF CLASS

    LONG DESCRIPTION OF CLASS

    ATTRIBUTES:
    ATTRIBUTE1(type): Description
    ATTRIBUTE2(type): Description
    """

    def __init__(self):
        """ Initialization of class
        """
        pass

    def record(self, record_type = 'schema:test', record_id = 'id_01'):
        """ FUNCTION DESCRIPTION
        """
        record = {
            "@type": record_type,
            "@id": record_id,
            "schema:name": record_id,
            "schema:url": "https://www.test.com"
            }


        return record

    def records(self, quantity = 10, record_type = 'schema:test', record_id = 'id_01'):

        records = []

        while quantity > 0:
            quantity = quantity -1
            records.append(self.record(record_type, record_id + '_' + str(quantity)))

        return records