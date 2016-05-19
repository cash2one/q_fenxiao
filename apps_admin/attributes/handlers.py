#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_admin.common_handler import CommonHandler
from services.attributes.attributes_service import AttributesService

attributes_service = AttributesService()

class AttributesHandler(CommonHandler):
    def get(self,operation,*args, **kwargs):
        attributes_service.set_rdb(self.rdb)
        if operation == 'list':
            category_id = self.get_argument('category_id','')
            category_name = self.get_argument('category_name',u'全部')
            query = attributes_service._list_attribute(category_id=category_id)
            attributes = self.get_page_data(query)
            self.echo('admin/attributes/_list.html',{'data':attributes,
                                                     'category_name':category_name,
                                                     'category_id':category_id
                                                    })
        else:
            attribute,attribute_values='',''
            attribute_id = self.get_argument('attribute_id','')
            if attribute_id:
                attribute_values = ' '.join([str(data.attribute_value) for data in attributes_service.get_attribute_value_by_id(attribute_id)])
                attribute = attributes_service.get_attribute_by_id(attribute_id)
            self.echo('admin/attributes/_add.html',{'attribute':attribute,'attribute_values':attribute_values})

    def post(self,operation,*args, **kwargs):
        self.get_paras_dict()
        attributes_service.set_db(self.db)
        attribute_id = self.get_argument('attribute_id','')
        attributes_service._add_attribute(attribute_name=self.qdict.get('attribute_name'),
                                          is_filter=self.qdict.get('is_filter'),
                                          is_sku=self.qdict.get('is_sku'),
                                          is_multi_select=0,
                                          status=self.qdict.get('status'),
                                          sort=self.qdict.get('paixu'),
                                          attribute_desc=self.qdict.get('attribute_desc'),
                                          category_id=self.qdict.get('category_id'),
                                          attribute_values=self.qdict.get('attribute_values').strip(),
                                          attribute_id=attribute_id)
        self.write('属性添加成功')



class AttributeValueHandler(CommonHandler):
    def get(self, operation,*args, **kwargs):
        attributes_service.set_rdb(self.rdb)
        if operation == 'add':
            attribute_id = self.get_argument('attribute_id')
            attribute_name = self.get_argument('attribute_name')
            self.echo('admin/attributes/_add_values.html',{'attribute_id':attribute_id,'attribute_name':attribute_name})
        else:
            attribute_id = self.get_argument('attribute_id')
            attribute_name = self.get_argument('attribute_name')
            category_name = self.get_argument('category_name')
            print category_name
            query = attributes_service._list_attribute_value(attribute_id)
            attribute_values = self.get_page_data(query)
            self.echo('admin/attributes/_list_values.html',{'data':attribute_values,
                                                            'attribute_id':attribute_id,
                                                            'attribute_name':attribute_name,
                                                            'category_name':category_name
                                                           })

    def post(self, operation,*args, **kwargs):
        attributes_service.set_db(self.db)
        if operation == 'add':
                attribute_id = self.get_argument('attribute_id')
                attribute_name = self.get_argument('attribute_name')
                values = self.get_argument('values')
                for value in values.split(' '):
                    attributes_service._add_attribute_value(1,attribute_id=attribute_id,attribute_name=attribute_name,value=value)
                self.write('添加属性成功!')
        elif operation == 'switch':
            attribute_v_id = self.get_argument('attribute_v_id')
            status = self.get_argument('status')
            attributes_service._add_attribute_value(status,attribute_v_id=attribute_v_id)
            self.write_json({'stat':200,'data':'','info':''})




















