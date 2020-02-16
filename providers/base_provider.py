
class BaseProvider():

    def _get_ranges(self):
        raise NotImplementedError

    def _process_ranges(self):
        raise NotImplementedError

    def get_processed_ranges(self):
    	return self.processed_ranges
    