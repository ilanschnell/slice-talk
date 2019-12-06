data = """\
0010George Jetson    12345 Spaceship St   Houston       TX
0020Wile E Coyote    312 Acme BLVD        Tucson        AZ
0030Fred Flintstone  246 Granite Lane     Bedrock       CA
0040Jonny Quest      31416 Science AVE    Palo Alto     CA
""".splitlines()

fields = [
    ('id',      slice( 0,  4)),
    ('name',    slice( 4, 21)),
    ('address', slice(21, 42)),
    ('city',    slice(42, 56)),
    ('state',   slice(56, 58)),
]

for record in data:
    for field, sl in fields:
        print("%s: %s" % (field, record[sl]))
    print('')
