#__*__coding:utf-8__*__
from django.utils.safestring import mark_safe

class Page:

	def __init__(self,current_page_number,total_count,page_number_show,per_page_count,recv_data=None):
		"""
		实现django下的分页功能
		:param current_page_number：当前页码
		:param total_count:总数据条数
		:param per_page_count:每页显示多少条
		:param page_number_show:显示的页码数量
		start_page_number:起始页码
		end_page_number:结束页码
		question：个人认为分页最大的问题所在就是数据的验证问题，
				因为我们接收前端页面的数据的方式是get的方式，
				所以验证用户发来的数据问题就是我们最大的问题
		"""
		self.recv_data = recv_data
		try:
			current_page_number = int(current_page_number)
		except Exception:
			#判断数据收否是整数
			current_page_number = 1

		half_number = page_number_show // 2
		a,b = divmod(total_count,per_page_count)
		#分多少页
		if b:
			total_page_count = a + 1
		else:
			total_page_count = a

		#当前大于总结码，赋值总页数
		if current_page_number >= total_page_count:
			current_page_number = total_page_count

		#当前页面小于1，赋值第一页
		if current_page_number <= 0:
			current_page_number = 1

		start_page_number = current_page_number - half_number
		end_page_number = current_page_number + half_number + 1

		if start_page_number <= 0:
			start_page_number = 1
			end_page_number = page_number_show +1

		if end_page_number > total_page_count:
			start_page_number = total_page_count - page_number_show +1
			end_page_number = total_page_count + 1

		if total_page_count < page_number_show:
			start_page_number = 1
			end_page_number = total_page_count

		self.current_page_number = current_page_number
		self.per_page_count = per_page_count
		self.total_page_count = total_page_count
		self.start_page_number = start_page_number
		self.end_page_number = end_page_number

	@property
	def start_data_number(self):
		"""
		每页多少条数据API
		:return:
		"""
		return (self.current_page_number - 1) * self.per_page_count

	@property
	def end_data_number(self):
		"""

		:return:
		"""
		return self.current_page_number * self.per_page_count

	def page_html_func(self):
		"""
		直接把前端的内容也写好
		:return:
		"""
		page_html = """
					<nav aria-label="Page navigation">
					<ul class="pagination">
					"""
		self.recv_data['page'] = 1
		first_page = f"""
					<li>
						<a href="?{ self.recv_data.urlencode() }" aria-label="Previous">
							<span aria-hidden="true">首页</span>
						</a>
					</li>"""
		page_html += first_page

		self.recv_data['page'] = self.current_page_number - 1
		previous_page = f"""
						<li>
							<a href="?{self.recv_data.urlencode()}" aria-label="Previous">
								<span aria-hidden="true">&laquo;</span>
							</a>
						</li>"""
		page_html += previous_page

		for i in range(self.start_page_number, self.end_page_number):
			self.recv_data['page'] = i
			if i == self.current_page_number:
				page_html += f'<li class="active"><a href="?page={i}">{i}</a></li>'
			else:
				page_html += f'<li><a href="?{self.recv_data.urlencode()}">{i}</a></li>'

		self.recv_data['page'] = self.current_page_number + 1
		next_page = f"""
					<li>
						<a href="?{self.recv_data.urlencode()}" aria-label="Next">
							<span aria-hidden="true">&raquo;</span>
						</a>
					</li>
					"""
		page_html += next_page

		self.recv_data['page'] = self.total_page_count
		last_page = f"""
					<li>
						<a href="?{self.recv_data.urlencode()}" aria-label="Previous">
							<span aria-hidden="true">尾页</span>
						</a>
					</li>"""
		page_html += last_page

		page_html += """
						</ul>
					</nav>
					"""
		return mark_safe(page_html)