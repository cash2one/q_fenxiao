#encoding:utf-8
__author__ = 'binpo'

import math


class Paginator():
    """
        系统查询分页工具
    """
    def __init__(self, url_func, page=1, total=0, page_size=50):

        self.url_func = url_func
        self.page = 1 if int(page) < 1 else int(page)   #当前页
        self.total = int(total)   #总条数
        self.page_size = int(page_size)
        #总页数
        self.page_num = (self.total%self.page_size==0) and self.total/self.page_size or int(math.ceil(self.total / self.page_size))+1
        self.page_bars = {}
        #开始数
        self.page_start=(self.page-1)*page_size+1
        #尾数
        self.page_end=self.page*page_size
        self.data = ()
        for _page in range(1, self.page_num + 1):
            _index = int(_page /self.page_size)
            if not self.page_bars.has_key(_index):
                self.page_bars[_index] = {_page}
            else:
                self.page_bars[_index].add(_page)
        print self.page_num

    def render(self,form_id=None,paras=None):
        '''
        动态输出html内容
        '''
        page_bar = self.page_bars.get(int(self.page / 10))
        if page_bar is None:
            return ''

        _htmls = []
        if form_id:
            _htmls.append('''<script>
                function goto_page(form_id,page){
                    var form=document.getElementById(form_id);
                    var page_input = document.createElement("input");
                    page_input.type="hidden";
                    page_input.name="page";
                    page_input.value=page;
                    form.appendChild(page_input);
                    form.submit();
                }</script>''')
        _htmls.append('<ul class="pagination pull-right">')
        _htmls.append('\t<li class="disabled"><a >查询记录数 %s</a></li>' % self.total)

        current_start = self.page
        if current_start == 1:
            _htmls.append('\t<li class="disabled"><a >首页</a></li>')
            _htmls.append('\t<li class="disabled"><a >&larr; 上一页</a></li>')
        else:
            _htmls.append('\t<li><a href="%s">首页</a></li>' % self.url_func(1,form_id))
            _htmls.append('\t<li><a href="%s">&larr; 上一页</a></li>' % self.url_func(current_start - 1,form_id))

        for page in page_bar:
            print page
            _page_url = self.url_func(page,form_id)
            if page == self.page:
                _htmls.append('\t<li class="active"><span>%s <span class="sr-only">{current}</span></span></li>' % page)
            else:
                _htmls.append('\t<li><a href="%s">%s</a></li>' % (_page_url, page))

        current_end = self.page
        if current_end == self.page_num:
            _htmls.append('\t<li class="disabled"><a >下一页 &rarr;</a></li>')
            _htmls.append('\t<li class="disabled"><a >尾页</a></li>')
        else:
            _htmls.append('\t<li><a href="%s">下一页 &rarr;</a></li>' % self.url_func(current_end + 1,form_id))
            _htmls.append('\t<li><a href="%s">尾页</a></li>' % self.url_func(self.page_num,form_id))

        _htmls.append('</ul>')

        return '\r\n'.join(_htmls)

    def admin_pagination_html(self,form_id=None,params={}):
        page_bar = self.page_bars.get(int(self.page / 10))
        if page_bar is None:
            return ''

        _htmls = []
        if form_id:
            _htmls.append('''<script>
                function goto_page(form_id,page){
                    var form=document.getElementById(form_id);
                    var page_input = document.createElement("input");
                    page_input.type="hidden";
                    page_input.name="page";
                    page_input.value=page;
                    form.appendChild(page_input);
                    form.submit();
                }</script>''')


        _htmls.append('<div class="dataTables_info" role="status" aria-live="polite">显示 {0} 到 {1},共 {2} 条</div>'.format(self.page_start,self.page_end,self.total))

        _htmls.append('<div class="dataTables_paginate paging_simple_numbers">')
        current_page = '<a class="paginate_button previous {1}" aria-controls="DataTables_Table_0" data-dt-idx="0" tabindex="0" href="{2}">{0}</a>'
        _page_bar = '<span><a class="paginate_button {1}" aria-controls="DataTables_Table_0" href="{2}" data-dt-idx="1" tabindex="0">{0}</a></span>'
        next_page = '<a class="paginate_button next {1}" aria-controls="DataTables_Table_0" data-dt-idx="2" tabindex="0" href="{2}">{0}</a>'
        current_start = self.page
        if current_start == 1:
            _htmls.append(current_page.format('首页','disabled','#'))
            _htmls.append(current_page.format('上一页','disabled','#'))
        else:
            _htmls.append(current_page.format('首页','',self.url_func(1,form_id)))
            _htmls.append(current_page.format('上一页','',self.url_func(self.page - 1,form_id)))

        for page in page_bar:
            _page_url = self.url_func(page,form_id)
            if page == self.page:
                _htmls.append(_page_bar.format(page,'current selected',_page_url))
            else:
                _htmls.append(_page_bar.format(page,'',_page_url))

        if self.page == self.page_num:
            _htmls.append(next_page.format('下一页','disabled','#'))
            _htmls.append(next_page.format('尾页','disabled','#'))
        else:
            _htmls.append(next_page.format('下一页','disabled',self.url_func(self.page + 1,form_id)))
            _htmls.append(next_page.format('尾页','disabled',self.url_func(self.page_num,form_id)))

        _htmls.append('</div>')
        return '\r\n'.join(_htmls)

    def pagination_html(self,form_id=None,params={}):
        pass
               # '<div class="splitPages" style="display: block;">
               #          <a href="javascript:void(0);">首页</a>
               #          <a class="prevPage">上一页</a>
               #          <span>1</span>
               #          <a data-page="2" href="javascript:void(0);" class="nextPage">下一页</a>&nbsp;
               #          <a href="javascript:void(0);">末页</a>'

    def to_dict(self):
        return {key:getattr(self,key) for key in ['page','total','page_size','page_num','page_start','page_end']}
