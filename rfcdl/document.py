import functools


@functools.total_ordering
class RFCDocument():
    def __init__(self, number, format, status, doi, is_obsolete=False):
        self.number = number
        self.format = format
        self.status = status
        self.doi = doi
        self.is_obsolete = is_obsolete

    def __str__(self):
        s = "<RFC document {}, status={}, is_obsolete={}>"
        s = s.format(self.number, self.status, str(self.is_obsolete))
        return s

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        same_number = self.number == other.number

        return same_number

    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        gt_number = self.number > other.number

        return gt_number

    def __hash__(self):
        return hash(self.number)
