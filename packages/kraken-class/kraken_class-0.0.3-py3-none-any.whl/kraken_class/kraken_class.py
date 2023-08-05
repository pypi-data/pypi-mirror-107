

from kraken_record.kraken_record import Kraken_record as KR

from kraken_db.kraken_db import Kraken_db as DB

from kraken_cache.kraken_cache import Kraken_cache as CACHE

#from kraken_datatype.kraken_datatype import Kraken_datatype as DATATYPE

import json

# Initialize cache
cache = CACHE()

# Initialize db
db = DB()


class Kraken:

    def __init__(self):

        a = 1

        self.records = []


    def __str__(self):

        records = self.__repr__()
        return str(records)


    def __repr__(self):

        records = []
        for i in self.records:
            records.append(str(i))

        return records

    def get(self, record_type, record_id):
        
        return self._get(record_type, record_id)


    def get_simple(self, record_type, record_id):
        
        
        return self._get(record_type, record_id).get_simple()



    def set(self, record_type = None, record_id = None, record = None):
        
        kr = KR()
        if record_type:
            kr.record_type = record_type
        if record_id: 
            kr.record_id = record_id

        kr.set(record)

        self.records.append(kr)


        return 



    def search(self, record_type, search_terms):
        record = {}

        return record


    def post(self, record): 

        

        return self._post(record)

    
    def ingest(self, datasource_id, records):
        # Convert record based on predefined mapping and store in krkn


        # Retrieve mapping



        # Convert record


        # Post record
        self._post(None, None, records)



        return 


    def _get(self, record_type, record_id):

        if not record_type or not record_id:
            return None

        # Retrieve record from cache
        cache_id = record_type + '/' + record_id
        record = cache.get(cache_id)

        # If not in cache, Retrieve record from db
        if not record:
            record = db.get(record_type, record_id)
            record = self._load_db_value_to_kr(record)

        return record


    def _post(self, records):

        # Convert to list if not one
        if not isinstance(records, list):
            records = [records]

        # Convert to KR if not done
        records = self._convert_record_to_kr(records)


        # Process record and store result in cache
        for record in records:
            self._post_process_record(record.record_type, record.record_id, record)


        # Retrieve cache content 
        records = cache.export()
        
        # Save cache content to db
        for record in records:
            db.post(record.record_type, record.record_id, record.dump())

        #Reset all cache data (after save to db)
        cache.clear_all()


        # Save cache content as json files in krkn files


        return


    def _convert_record_to_kr(self, records):
        # Convert values to KR format if required
        
        if not isinstance(records, list):
            records = [records]

        # COnvert to KR if not done
        new_records = []
        for record in records:
            if not isinstance(record, KR):
                kr = KR()
                kr.set(record)
                new_records.append(kr)
        
        return new_records

    def _load_db_value_to_kr(self, records):
        
        is_list = True
        if not isinstance(records, list):
            is_list = False
            records = [records]
        
        # COnvert to KR if not done
        new_records = []
        for record in records:
            # Skip if not dict
            if not isinstance(record, dict):
                continue

            # Remove db data
            record.pop('createdDate', None) 
            record.pop('@id', None)

            # Convert to kr
            if not isinstance(record, KR):
                kr = KR()
                kr.load(record)
                new_records.append(kr)
        
        # Bring back to non-list if it came this way
        if is_list == False:
            new_records = new_records[0]

        return new_records




    def _post_process_record(self, record_type, record_id, record):

        # Check if record is valid


        # Retrieve type schema
        schema = {}


        # Validate and standardize record keys


        # validate and standardize record values
        #dt = DATATYPE()
        #record = dt.clean(record, schema)


        # Transform record into krkn format and flatten
        if not isinstance(record, KR):
            kr_new_record = KR()
            kr_new_record.set(record)
        else:
            kr_new_record = record

        # Override record type and id if one was provided
        if record_type:
            kr_new_record.record_type = record_type
        if record_id:
            kr_new_record.record_id = record_id

        # Reassign recordtype and id
        record_type = kr_new_record.record_type
        record_id = kr_new_record.record_id


        # Retrieve sub_records (from flattening)
        sub_records = kr_new_record.sub_records


        # Process sub records
        for sub_record in sub_records:
            print('a', sub_record.get())
            self._post_process_record(None, None, sub_record)


        # Retrieve record from cache/db
        try:
            kr_db_record = self._get(record_type, record_id)
        except:
            kr_db_record = None
        

        # Merge records (new and old) 
        if kr_db_record:
            merged_record = kr_new_record + kr_db_record
        else:
            merged_record = kr_new_record

        # If record changed, save to cache
        if kr_db_record == None or merged_record > kr_db_record:
            cache_id = record_type + '/' + record_id
            cache.set(cache_id, merged_record)


        return record_id

