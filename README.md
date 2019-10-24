crm客户管理系统

### 项目需求分析

### 项目的数据库设计

|       表名       |                        功能                        |
| :--------------: | :------------------------------------------------: |
|     UserInfo     | 用户表：销售、讲师、班主任（针对后台数据的使用者） |
|     Customer     |     客户表：就是后台最原始的数据，被操作的对象     |
|     Campuses     |                       校区表                       |
|    Department    |                       部门表                       |
|    ClassList     |                       班级表                       |
| ContractTemplate |                     合同模板表                     |
|  ConsultRecord   |        跟进记录表（针对客户信息的详细描述）        |
|    Enrollment    |                       报名表                       |
|  PaymentRecord   |                     缴费记录表                     |
|   CourseRecord   |                     课程记录表                     |
|   StudyRecord    |                      学习记录                      |

数据库表的设计可以说是一个项目成败的关键。所以说，在开一个项目之前，一定需要考虑多方的因素；做方案的时候把各方面的情况都考虑在内。

### 基于Django框架的项目搭建

### 模块一：管理员的登录与注册

重点部分：

注册登录这一部分，我们使用4个路由分别去做页面的分发和前端数据的处理。其实这一部分完全可以使用两个路由使用**method判断**的方法去处理。

前端页面数据的验证是非常重要的一点：在这里我们使用**Form表单**的形式去做的。

首先，在我们的forms.py文件下面创建我们的2个表单类，每个类里面为我么的字段做加限定的条件和错误信息（普通的字段，直接使用限制条件就可以，对于密码的验证我们使用全局钩子去做数据校验）

然后，我们创建好这些验证消息和字段之后，就可以在我们的视图里面实例化传给前端的界面使用（直接模板渲染）

对于Form最重要的几点就是：

- 实例化的时候不加参数是给前端页面时候的空页面

- 实例化的时候带有参数是前端 页面给后台的，我们对其中的数据进行处理或者持久化储存

- form最重要的一个方法**is_valid()**是用于表单数据验证的，我们判断的原理就是根据我们在form里面定义的各个字段的限制来实现的，前端页面返回数据合法，我们就进行后台的处理，数据不合法就还返回给原来的页面，这个时候错误的信息就会在前端页面展示出来
- 表单的**clean_data**包含了表单的一切数据

**中间件**：既然，我们写了登录的界面，那么我们级需要然站内的内容都一以我们的lgoin为入口，只要没有登录成功，就必须走我们的login，这个时候中间件就很重要了，我们在中间件里面设置白名单的形式过滤掉login的路由，其他的一切都重定向到我们的login

**session**:还有就是，我们需要在站内进行跳转，这就需要操持我们登录的状态，这个时候就使用到了session，所以在我们登录成功之后，我们可以个session['is_login']=true用来保持我们的状态



### 模块二：管理员进行数据的操作（查、增、改）

重点部分：

登录成功之后，我们就可以进入我们的后台管理主界面，这个时候就是一个菜单式的页面，我们通过点击不同的需求，显示不同的页面。

我们的客户信息展示页面信息添加和编辑的时候我们使用的是**ModelForm**，同样，在我们的form文件下创建一个类CustomerModelsForm类用来产生数据

```python
class CustomersModelsForm(forms.ModelForm):

	class Meta:
		model = models.Customer
        #应用所有的字段
		fields = "__all__"

		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)

			for field_name,field in self.fields.items():
                #表中有一个字段是多选的，它不支持这个attrs的样式，所以把它挑出来，其他的字段都使用一样的样式
				from multiselectfield.forms.fields import MultiSelectFormField
				if not isinstance(field,MultiSelectFormField):
					field.widget.attrs.update({'class':'form-control'})
```

ModelForm用法：https://chpl.top/2019/10/05/%E4%B9%A6/Django/%E7%AC%AC%E5%85%AD%E8%AE%B2%E2%80%94%E2%80%94Django%E8%A1%A8%E5%8D%95/

之后，就和form表单的流程是一样的，**实例化，给前端渲染，带参数返回，判断，处理储存（还是返回展示错误）**。

**ModelForm和form表单的一个非常大的不同**就是，form表单储存数据的方式是和orm模型是一样的谁用**data打散**的方式，把数据写入数据库。ModelForm保存数据的方式非常的简单，只要，我们的is_valid()验证通过之后，直接可以使用**form_obj.save()**保存到数据库。

**对于编辑数据（ModelForm的instance参数非常重要）**：

```python
old_obj = models.Customer.objects.filter(pk=id).first()
	if request.method == "GET":
        #这里的instance把重数据库中取到的数据放到了即将生成的表单中
		old_form = forms.CustomersModelsForm(instance=old_obj)  
		return render(request,'customers/edit_cumtomers.html',{"form":old_form})
	else:
		next_path = request.GET.get('next')
        #我们在把修改之后的数据持久化储存的时候，也必须带这个参数，不然怎么知道我恩修改的是哪一条数据？是不是
		new_form = forms.CustomersModelsForm(request.POST,instance=old_obj)
		if new_form.is_valid():
			new_form.save()
			print (next_path)
			return redirect(next_path)
		else:
			return render(request,'customers/edit_cumtomers.html',{"form":new_form})
```

### 模块三：分页与客户信息简单搜索功能

**分页**

这个比较复杂,先把思路先说明一下:分页，既然分页在前端的页面那么就有很多的按钮，代表页码，前端通过按钮告诉我们后端，我们后端取得对应的数据返回给前端的页面。

那么，前端给后端的通信方式是什么？是使用post还是get？post可能是我们首选的是不是，但是，在这里我们**使用的却是get**，因为请求页面没不要那么麻烦。使用post我们还需要过csrf验证，有点麻烦。

话说，我们把这一切的操作，**包括前端的页面和后端的逻辑都封装在了一个Page文件里面**，现在我们知道前端的分页按钮改变的就是在路由后面携带的一个数据page=xx的请求。

现在，我们就进入这个Page文件看看，它里面都进行了怎样的操作：
在分页组件里面我们定义了：
**总数据的条数（一切的根源，页面展示的东西）
每页显示多少条数据（在前端展示）
展示多少页码（在前端展示）
当前的页码
起始页码
结束页码**

最开始，我们在**__init__**里面取得当前页的页码：

**组件显示和页面数据展示控制**

我们确定分页显示页码的数量

- 显示的时候最左边怎么控制
- 最右边的页码怎么控制

确定可以分多少页

- 每页的起始数据是哪一条
- 结束数据是哪一条

因为页面的数据是不可控的，所以，去验证数据是非常重要。

然后，初始化之后，把产生的当前页、总页数、起始数据、结束数据等都给self，这样，我们在实例对象的时候就可以使用这些数据了。

**定义API用来返回给调用者数据**

返回控制页面显示数据的条数

定义两个方法，使用@property装饰两个函数，伪装成属性，用来返回前端页面的数据从数据库的哪里取，哪里结束

最后就是定义一个函数，写前端页面的便签和嵌入我们的数据。

现在，在我们的视图里面，我们在这里可以取得url请求里面的当前页码，我们自定义每页展示多少条数据，显示多少的分页按钮，以及取得数据库数据的总条数。现在我们有了这四个数据，传递给

Page实例化出来一个page_obj对象，我们就可以通过该对象调用写html标签的函数，传递给前端的页面，直接就可以展示出来我们的分页组件和对应分页显示的数据。

```python
#实例化对象
page_obj = Page(current_page_number, total_count, page_number_show,per_page_count,recv_data)
#调用伪装的方法，确定给前端展示哪些数据
all_customers = all_customers[page_obj.start_data_number:page_obj.end_data_number]
#调用生成便签的函数给前端展示
page_html = page_obj.page_html_func()
return render(request, 'customers/show_customers.html', {'all_customers': all_customers, "page_html": page_html,"keyword":keyword,'message':message,'search_field':search_field})

```

**客户信息简单搜索功能**

搜索有几个巧妙的地方：

我们在定义前端标签的时候这样定义

```html
                <select class="btn-box-tool bg-gray" id="search_field">
                    <option selected="selected" value="qq__contains">qq</option>
                    <option value="name__contains">姓名</option>
                    <option value="phone__contains">手机号</option>
                    <option value="status__contains">状态</option>
```

看着他们的值是不是特定的熟悉，不就是我们orm里面的双下划线的查询方式吗?没错就是他们。后面就知道为什么这样了

在后台我们还有这个操作：

```python
recv_data = copy.copy(request.GET)
#大家看到这个可能会问，query.GET就是一个queryDict对象吗，copy不就是拷贝这个对象吗？这有什么用途呢？别急往下看
```

然后我们自然而然的在后台取到前台的搜索GET发来的数据search_field和keyword。

有了上述的两个字段，我们不就可以去数据库取得对应的数据吗？这时候，我们filter的需要跨表查询就使用到了我们的双下方法，这个时候，我们标签里面的value就可以大显身手了，直接把他们当作查询的条件（如果前端的value使用其他的字符在filter里面是不能使用变量的方式__的，所以这个就很巧）

```python
		if keyword:
			q = Q()
			q.children.append([search_field,keyword])
			all_customers = models.Customer.objects.filter(q)
方式一：
#这里，我们不实用我们上述说的那种方法，这里使用Q的特殊方法，children.append([search_field,keyword])和(qq__contains='qq')是一样的效果
方式二：
我们也可以使用**{search_field:keyword},这种方式的结结果也是(qq__contains='qq')
```

然后，我们把查到的数据返回给前端的页面是不是完工了？

答案：非也，我们在页面查询的时候没有问题，但是，我们发现查询之后，我们的搜索框里面的数据就没有了，因为刷新了页面呀？怎么解决？这就要说到上买呢的copy的queryDict的作用了。

因为queryDict对象是不能改变里面的数据的，但是copy之后的对象我们就可以对他进行操作了（因为它有一个参数mutil=False）表示不可修改，说白了就是修改这个参数，把它改成True







