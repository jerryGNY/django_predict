from django.template import loader
from django.test import TestCase

# Create your tests here.

def generate_test_html():
    '''测试生成静态页面'''

    context = {
        'city': '北京',
        'adict': {
            'name': '西游记',
            'author': '吴承恩'
    },
        'alist': [1, 2, 3, 4, 5]
    }

    template = loader.get_template('test3.html')

    html_str = template.render(context)
    print(html_str)

    #保存生成静态内容到： front_end_pc/test3.html
    file_path = '/home/python/Desktop/meiduo/front_end_pc/test3.html'
    with open(file_path, 'w') as file:
        file.write(html_str)