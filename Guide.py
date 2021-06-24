from functools import lru_cache

from levenshtein import lev

class Guide:
    BASE_COMP_TABLE = str.maketrans('ATCG', 'TAGC')

    def __init__(self, chrom: str, start: int , end: int, strand: str, bases: str):
        self.chrom = chrom
        self.start = start
        self.end = end
        self.strand = strand
        self.bases = bases
        self.rc_bases = bases[::-1].translate(Guide.BASE_COMP_TABLE)
        self.location = round((self.end + self.start) / 2)

    def dist(self, guide):
        if self.location > guide.location:
            return self.location - guide.location

        return guide.location - self.location

    def edit_dist(self, guide):
        return lev(self.bases, guide.bases)

    def rev_compliment_edit_dist(self, guide):
        return lev(self.bases, guide.rc_bases)

    def min_edit_dist(self, guide):
        return min(self.edit_dist(guide), self.rev_compliment_edit_dist(guide))

    def __str__(self):
        return f"{self.chrom}.{self.start}.{self.end}.{self.strand}.{self.bases}"

def parse_guides(guidefile):
    guides = {}
    with open(guidefile) as guide_lines:
        for guide_line in guide_lines:
            line, guide = guide_line.strip().split(' ', maxsplit=1)
            line = int(line)
            if not guide.startswith('chr'):
                continue
            guide_data = guide.split('-')
            if len(guide_data) == 6:
                guide_data[3] = '-'
                del guide_data[4]
            chrom, start, end, strand, bases = guide_data
            start = int(start)
            end = int(end)
            guides[line] = Guide(chrom, start, end, strand, bases)
    return guides