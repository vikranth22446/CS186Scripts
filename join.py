from math import ceil


class SortHash:
    def __init__(self, numPages, numBuffers):
        self.numPages = numPages
        self.numBuffers = numBuffers

    def sort(self):
        B = self.numBuffers
        P = self.numPages
        runs = [P // B, B, P % B]
        i = 0
        while runs[0] + (runs[2] > 0) > 1:
            print("Pass {}: {} runs of {} pages, 1 run of {} pages".format(i, runs[0], runs[1], runs[2]))
            runs = [runs[0] // (B - 1), runs[1] * (B - 1), runs[2] + (runs[0] % (B - 1)) * runs[1]]
            i += 1
        print("Pass {}: {} runs of {} pages, 1 run of {} pages".format(i, runs[0], runs[1], runs[2]))
        ios = 2 * P * (i + 1)
        print("Total IO:", ios)
        return ios

    def hash(self):
        B = self.numBuffers
        ios = P = self.numPages
        parts = 1
        i = 0
        while P > B:
            parts *= B - 1
            P = ceil(P / (B - 1))
            print("Pass {}: {} partitions of {} pages".format(i, parts, P))
            ios += P * parts * 2
            i += 1
        ios += P * parts
        print("Total IO:", ios)
        return ios


class Join:
    def __init__(self, numPages1, numRecords1, numPages2, numRecords2, numBuffers=3):
        self.p1 = numPages1
        self.r1 = numRecords1
        self.p2 = numPages2
        self.r2 = numRecords2
        self.b = numBuffers

    def SNLJ(self):
        print("Relation 1 as outer: {}".format(self.p1 + self.r1 * self.p2))
        print("Relation 2 as outer: {}".format(self.p2 + self.r2 * self.p1))

    def PNLJ(self):
        print("Relation 1 as outer: {}".format(self.p1 + self.p1 * self.p2))
        print("Relation 2 as outer: {}".format(self.p2 + self.p2 * self.p1))

    def BNLJ(self):
        print("Relation 1 as outer: {}".format(
            self.p1 + ceil(self.p1 / (self.b - 2)) * self.p2))
        print("Relation 2 as outer: {}".format(
            self.p2 + ceil(self.p2 / (self.b - 2)) * self.p1))

    # Above work for all joins
    # below only work for equijoins

    def hash(self):
        b, p1, p2 = self.b, self.p1, self.p2
        parts = 1
        ios = p1 + p2
        i = 0
        while p1 > b - 2 and p2 > b - 2:
            parts *= b - 1
            p1, p2 = ceil(p1 / (b - 1.0)), ceil(p2 / (b - 1.0))

            print("Pass {}: {} partitions".format(i, parts))
            print("  Relation 1: {} pages\n  Relation 2: {} pages".format(p1, p2))
            ios += (p1 + p2) * parts * 2
            i += 1
        print("Partitioning: ", ios - (p1 * parts + p2 * parts))
        print("Build and Probe Phase: ", p1 * parts + p2 * parts)

        print("Total IO:", ios, "Total Passes", i)
        return ios

    def sort(self, merging_phase_only=False):
        if merging_phase_only:
            print("Merging Cost:", self.p1 + self.p2)
            return
        ios = SortHash(self.p1, self.b).sort() + SortHash(self.p2, self.b).sort()
        print("Total IO:", ios + self.p1 + self.p2)

    def INLJ(self, num_pages_reach_data, clustered=True):
        def inlj_helper(p1, r1, r2, relation="1"):
            io = p1 + r1 * num_pages_reach_data
            extra_unclusterd = 0
            if not clustered:
                extra_unclusterd = r2
            io += extra_unclusterd
            print(
                "Cost to Join Relation {} as Outer: {} + {}*{} + {} = {}".format(relation, p1, num_pages_reach_data, r2,
                                                                                 extra_unclusterd, io))

        inlj_helper(self.p1, self.r1, self.r2)
        inlj_helper(self.p2, self.r2, self.r1, relation="2")

    def index_scan(self, height, num_leaf, num_record_pages, tuples_per_record, selectivity):
        print("height: {}, leaf Cost: {}, records cost: {}".format(height, ceil(num_leaf * selectivity),
                                                                   ceil(
                                                                       num_record_pages * tuples_per_record * selectivity)))
        print("Total Index Scan Cost",
              height + ceil(num_leaf * selectivity) + ceil(num_record_pages * tuples_per_record * selectivity))


if __name__ == "__main__":
    # SortHash(12, 4).sort()
    # Join(500, 500 * 50, 600, 600*50, numBuffers=12).BNLJ() # 30500
    # Join(500, 500 * 50, 600, 600*50, numBuffers=12).hash() # 5742
    Join(500, 500 * 50, 600, 600*50, numBuffers=50).hash() # 7700 IO

    # Join(200, 0, 20, 0, numBuffers=8).sort()
    # Join(60, 35 * 1200, 20, 100 * 50, numBuffers=6).hash()

    # Join(80, 20000, 5, 1000, numBuffers=102).hash()
    # Join(80, 20000, 25, 1000, numBuffers=102).sort()









"""
CREATE TABLE students (
name VARCHAR, 
sid INTEGER UNIQUE, 
edx_id INTEGER UNIQUE PRIMARY KEY, 
email VARCHAR UNIQUE);

CREATE TABLE assignments (
assignment_name VARCHAR UNIQUE, 
profile VARCHAR, 
assignment_group VARCHAR,
 weight FLOAT, 
 due_date TIMESTAMP, 
 PRIMARY KEY(assignment_name,profile));
 
CREATE TABLE results(
submission_id INTEGER PRIMARY  KEY,
edx_id INT  REFERENCES students(edx_id),
assignment_name VARCHAR REFERENCES assignments(assignment_name) ,
profile VARCHAR,
submission_time TIMESTAMP ,
score FLOAT 
);
"""
