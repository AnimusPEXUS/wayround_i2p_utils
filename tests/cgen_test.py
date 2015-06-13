import wayround_org.utils.cgen


c_file = wayround_org.utils.cgen.Cfile()

c_file.add_element(wayround_org.utils.cgen.Import('asm.h'))
c_file.add_element(
    wayround_org.utils.cgen.Struct(
        'MyStr',
        [
            wayround_org.utils.cgen.Var('int', 'a'),
            wayround_org.utils.cgen.Var('int', 'b'),
            wayround_org.utils.cgen.Var('int', 'c'),
            wayround_org.utils.cgen.Var('int', 'd')
            ]
        )
    )
c_file.add_element(
    wayround_org.utils.cgen.Function(
        'void',
        'main',
        [
            wayround_org.utils.cgen.Var('void', '')
            ],
        ''
        )
    )

print(c_file.translate())
