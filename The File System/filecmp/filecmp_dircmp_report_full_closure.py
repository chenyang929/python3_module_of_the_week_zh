# filecmp_dircmp_report_full_closure.py

import filecmp

dc = filecmp.dircmp('example/dir1', 'example/dir2')
dc.report_full_closure()
