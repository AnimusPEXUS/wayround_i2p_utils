def name_parse_test(args, opts):
    """
    Test Name Parsing Facilities
    """
    parse_test()
    return 0

def name_parse_name(opts, args):
    """
    Parse name

    [-w] NAME

    if -w is set - change <name>.json info file nametype value to
    result
    """

    ret = 0

    if len(args) != 1:
        logging.error("File name required")
        ret = 1
    else:

        filename = args[0]

        packagename = (
            org.wayround.aipsetup.pkginfo.get_package_name_by_tarball_filename(
                filename,
                mute=False
                )
            )

        print("Package name is: {}".format(packagename))

    return ret

