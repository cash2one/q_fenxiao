#encoding:utf-8
__author__ = 'binpo'
from ..base_services import BaseService
from models.gallery import Gallery

class GalleryServices(BaseService):

    def _add(self,*args,**kargs):
        gallery = self.db.execute(
            Gallery.__table__.insert(),[kargs]
        )
        return gallery.inserted_primary_key[0]


