#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base_handler import AdminBaseHandler

class BuildCenterHandler(AdminBaseHandler):
    def prepare(self):
        self.set_header('Content-Type', 'application/force-download')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % 'sales.xls')