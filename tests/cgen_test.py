import org.wayround.utils.cgen


c_file = org.wayround.utils.cgen.Cfile()

c_file.add_element(org.wayround.utils.cgen.Import('asm.h'))
c_file.add_element(
    org.wayround.utils.cgen.Struct(
        'MyStr',
        [
            org.wayround.utils.cgen.Var('int', 'a'),
            org.wayround.utils.cgen.Var('int', 'b'),
            org.wayround.utils.cgen.Var('int', 'c'),
            org.wayround.utils.cgen.Var('int', 'd')
            ]
        )
    )
c_file.add_element(
    org.wayround.utils.cgen.Function(
        'void',
        'main',
        [
            org.wayround.utils.cgen.Var('void', '')
            ],
        ''
        )
    )

print(c_file.translate())
