from . import models

import odoo.modules


def pre_init(cr):
    f = odoo.modules.get_module_resource('jiksaa_complex_state_pattern', 'data', 'init_data.sql')
    if not f:
        m = "File not found: 'init_data.sql' (provided by module 'jiksaa_complex_state_pattern')."
        raise IOError(m)

    with odoo.tools.misc.file_open(f) as init_sql_file:
        cr.execute(init_sql_file.read())
