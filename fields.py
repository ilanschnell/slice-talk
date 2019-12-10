from numpy import s_
data = """\
0010George Jetson    12345 Spaceship St   Houston       TX
0020Wile E Coyote    312 Acme BLVD        Tucson        AZ
0030Fred Flintstone  246 Granite Lane     Bedrock       CA
0040Jonny Quest      31416 Science AVE    Palo Alto     CA
0050Anne Costello    326 Michigan Rd      Round Rock    TX
0060Robert Morrison  125 Hyndford St      Grand Island  NE
""".splitlines()

fields = [
    ('id',      s_[:4]),
    ('name',    s_[4:21]),
    ('address', s_[21:42]),
    ('city',    s_[42:56]),
    ('state',   s_[56:58]),
]

for record in data:
    for field, sl in fields:
        print("%s: %s" % (field, record[sl]))
    print()
