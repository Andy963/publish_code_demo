#!usr/bin/env python
# *- coding:utf-8 -*-
# Andy Create @ 10/21/2019 6:57 PM


from django.utils.safestring import mark_safe


class CustomPage:

    def __init__(self, cur_page_num, total_count, obj_per_page=8, page_tab_num=7, request_data=None):
        """
        :param cur_page_num:   当前页码
        :param total_count:    总数据量
        :param obj_per_page:    每页显示多少条
        :param page_tab_num:   总共显示多少个页码按钮

        start_page_number:起始页码
        end_page_number:结束页码
        """
        # 用来从url中获取 页码信息
        self.request_data = request_data

        try:
            cur_page_num = int(cur_page_num)
        except Exception:
            cur_page_num = 1

        # 显示的页码按钮中间值
        half_number = page_tab_num // 2

        # 诸总页码
        temp_count, rest = divmod(total_count, obj_per_page)
        # 如果余数不为0，页码总数为商+1
        if rest:
            total_page_count = temp_count + 1
        else:
            total_page_count = temp_count

        # total_page_count 最大页数
        #  如果当前页大于总页码，当前页为总页数
        if cur_page_num >= total_page_count:
            cur_page_num = total_page_count
        # 当当前页码小于等于0的时候，默认显示第一页
        if cur_page_num <= 0:
            cur_page_num = 1

        # current_page_number 2
        # print(total_page_count)  # 2
        start_page_number = cur_page_num - half_number  #
        end_page_number = cur_page_num + half_number + 1  # 6

        if start_page_number <= 0:
            start_page_number = 1
            end_page_number = page_tab_num + 1  # 7

        if end_page_number >= total_page_count:  # 6 > 2
            start_page_number = total_page_count - page_tab_num + 1  # -4
            end_page_number = total_page_count + 1  # 3

        if total_page_count < page_tab_num:
            start_page_number = 1
            end_page_number = total_page_count + 1

        self.cur_page_num = cur_page_num
        self.obj_per_page = obj_per_page
        self.total_page_count = total_page_count
        self.start_page_number = start_page_number
        self.end_page_number = end_page_number

    @property
    def start_data_number(self):

        return (self.cur_page_num - 1) * self.obj_per_page

    @property
    def end_data_number(self):

        return self.cur_page_num * self.obj_per_page

    def page_html_func(self):

        page_html = """
                           <nav aria-label="Page navigation">
                             <ul class="pagination">

                           """
        self.request_data['page'] = 1
        first_page = f"""
                               <li>
                                 <a href="?{self.request_data.urlencode()}" aria-label="Previous">
                                   <span aria-hidden="true">首页</span>
                                 </a>
                               </li>"""
        page_html += first_page

        self.request_data['page'] = self.cur_page_num - 1
        previous_page = f"""
                           <li>
                                 <a href="?{self.request_data.urlencode()}" aria-label="Previous">
                                   <span aria-hidden="true">&laquo;</span>
                                 </a>
                               </li>"""
        page_html += previous_page

        for i in range(self.start_page_number, self.end_page_number):
            self.request_data['page'] = i  #
            # <QueryDict: {'search_field': ['qq__contains'], 'keyword': ['123'],'page':'1'}>
            # page=2&search_field=qq__contains&keyword=12
            if i == self.cur_page_num:

                page_html += f'<li class="active"><a href="?{self.request_data.urlencode()}">{i}</a></li>'
            else:
                # page=2&search_field=qq__contains&keyword=123
                # page_html += f"""<li><a href="?page={i}&{ self.recv_data.urlencode().replace('page='+str(self.current_page_number)+'&','') if 'page=' in self.recv_data.urlencode() else self.recv_data.urlencode() }">{i}</a></li>"""
                page_html += f"""<li><a href="?{self.request_data.urlencode()}">{i}</a></li>"""

        self.request_data['page'] = self.cur_page_num + 1
        next_page = f"""
                               <li>
                                     <a href="?{self.request_data.urlencode()}" aria-label="Next">
                                       <span aria-hidden="true">&raquo;</span>
                                     </a>
                                   </li>
                   """
        page_html += next_page

        self.request_data['page'] = self.total_page_count
        last_page = f"""
                                   <li>
                                     <a href="?{self.request_data.urlencode()}" aria-label="Previous">
                                       <span aria-hidden="true">尾页</span>
                                     </a>
                                   </li>"""
        page_html += last_page

        page_html += """

                                 </ul>
                               </nav>
                           """
        return mark_safe(page_html)
