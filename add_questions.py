#!/usr/bin/env python
import os
import sys
import django
import json

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
django.setup()

from questions.models import Question

def add_sample_questions():
    """批量添加示例题目"""
    
    # 简单难度题目 (10道)
    easy_questions = [
        # 选择题 - 简单
        {
            'content': '下列哪个是Python的基本数据类型？',
            'question_type': 'choice',
            'difficulty_level': 'easy',
            'choice_type': 'single',
            'options': {
                'A': 'int',
                'B': 'array',
                'C': 'pointer',
                'D': 'struct'
            }
        },
        {
            'content': '在Python中，哪个关键字用于定义函数？',
            'question_type': 'choice',
            'difficulty_level': 'easy',
            'choice_type': 'single',
            'options': {
                'A': 'function',
                'B': 'def',
                'C': 'define',
                'D': 'func'
            }
        },
        {
            'content': '下列哪些是Python的内置函数？',
            'question_type': 'choice',
            'difficulty_level': 'easy',
            'choice_type': 'multiple',
            'options': {
                'A': 'print()',
                'B': 'len()',
                'C': 'input()',
                'D': 'display()'
            }
        },
        # 判断题 - 简单
        {
            'content': 'Python是一种解释型编程语言。',
            'question_type': 'true_false',
            'difficulty_level': 'easy',
            'true_false_answer': True
        },
        {
            'content': 'Python中的变量需要先声明类型再使用。',
            'question_type': 'true_false',
            'difficulty_level': 'easy',
            'true_false_answer': False
        },
        {
            'content': 'Python中的列表是可变的数据类型。',
            'question_type': 'true_false',
            'difficulty_level': 'easy',
            'true_false_answer': True
        },
        # 填空题 - 简单
        {
            'content': '在Python中，使用 _____ 关键字可以导入模块。',
            'question_type': 'fill_in_blank',
            'difficulty_level': 'easy',
            'fill_answer': 'import'
        },
        {
            'content': 'Python中表示空值的关键字是 _____。',
            'question_type': 'fill_in_blank',
            'difficulty_level': 'easy',
            'fill_answer': 'None'
        },
        # 简答题 - 简单
        {
            'content': '请简述Python语言的主要特点。',
            'question_type': 'essay',
            'difficulty_level': 'easy',
            'essay_answer': 'Python是一种高级编程语言，具有语法简洁、易于学习、跨平台、开源免费、拥有丰富的第三方库等特点。'
        },
        {
            'content': '什么是Python中的缩进？为什么重要？',
            'question_type': 'essay',
            'difficulty_level': 'easy',
            'essay_answer': 'Python中的缩进是用来表示代码块的层次结构，它替代了其他语言中的大括号。缩进对于Python语法是必需的，错误的缩进会导致语法错误。'
        }
    ]
    
    # 中等难度题目 (10道)
    medium_questions = [
        # 选择题 - 中等
        {
            'content': '下列关于Python列表推导式的说法，哪个是正确的？',
            'question_type': 'choice',
            'difficulty_level': 'medium',
            'choice_type': 'single',
            'options': {
                'A': '列表推导式比普通循环慢',
                'B': '列表推导式只能用于数字列表',
                'C': '列表推导式可以包含条件判断',
                'D': '列表推导式不能嵌套使用'
            }
        },
        {
            'content': '在Python中，下列哪个方法可以用来合并两个字典？',
            'question_type': 'choice',
            'difficulty_level': 'medium',
            'choice_type': 'single',
            'options': {
                'A': 'dict.merge()',
                'B': 'dict.update()',
                'C': 'dict.combine()',
                'D': 'dict.join()'
            }
        },
        {
            'content': '下列哪些是Python中的装饰器的特点？',
            'question_type': 'choice',
            'difficulty_level': 'medium',
            'choice_type': 'multiple',
            'options': {
                'A': '可以修改函数行为',
                'B': '使用@符号语法',
                'C': '必须返回函数对象',
                'D': '只能用于类方法'
            }
        },
        # 判断题 - 中等
        {
            'content': 'Python中的生成器表达式比列表推导式更节省内存。',
            'question_type': 'true_false',
            'difficulty_level': 'medium',
            'true_false_answer': True
        },
        {
            'content': 'Python中的lambda函数可以包含多个语句。',
            'question_type': 'true_false',
            'difficulty_level': 'medium',
            'true_false_answer': False
        },
        {
            'content': 'Python中的with语句主要用于异常处理。',
            'question_type': 'true_false',
            'difficulty_level': 'medium',
            'true_false_answer': False
        },
        # 填空题 - 中等
        {
            'content': '在Python中，使用 _____ 方法可以将字符串按指定分隔符分割成列表。',
            'question_type': 'fill_in_blank',
            'difficulty_level': 'medium',
            'fill_answer': 'split'
        },
        {
            'content': 'Python中的 _____ 函数可以同时遍历索引和值。',
            'question_type': 'fill_in_blank',
            'difficulty_level': 'medium',
            'fill_answer': 'enumerate'
        },
        # 简答题 - 中等
        {
            'content': '解释Python中的闭包概念，并给出一个简单的例子。',
            'question_type': 'essay',
            'difficulty_level': 'medium',
            'essay_answer': '闭包是指内部函数引用了外部函数的变量，即使外部函数已经返回，这些变量仍然被保存在内存中。例如：def outer(x): def inner(): return x; return inner'
        },
        {
            'content': '什么是Python中的GIL？它对多线程编程有什么影响？',
            'question_type': 'essay',
            'difficulty_level': 'medium',
            'essay_answer': 'GIL（全局解释器锁）是Python解释器中的一个机制，它确保同一时间只有一个线程执行Python字节码。这限制了多线程程序的并行性，使得CPU密集型任务无法真正并行执行。'
        }
    ]
    
    # 困难难度题目 (10道)
    hard_questions = [
        # 选择题 - 困难
        {
            'content': '下列关于Python元类（metaclass）的描述，哪个是正确的？',
            'question_type': 'choice',
            'difficulty_level': 'hard',
            'choice_type': 'single',
            'options': {
                'A': '元类是类的实例',
                'B': '元类是创建类的类',
                'C': '元类只能继承自type',
                'D': '元类不能有自己的方法'
            }
        },
        {
            'content': '在Python中，下列哪个描述符方法的优先级最高？',
            'question_type': 'choice',
            'difficulty_level': 'hard',
            'choice_type': 'single',
            'options': {
                'A': '__get__',
                'B': '__set__',
                'C': '__delete__',
                'D': '__set_name__'
            }
        },
        {
            'content': '下列哪些是Python中协程的特点？',
            'question_type': 'choice',
            'difficulty_level': 'hard',
            'choice_type': 'multiple',
            'options': {
                'A': '使用async/await语法',
                'B': '可以暂停和恢复执行',
                'C': '比线程更轻量级',
                'D': '自动处理并发安全'
            }
        },
        # 判断题 - 困难
        {
            'content': 'Python中的__slots__可以完全阻止动态添加属性。',
            'question_type': 'true_false',
            'difficulty_level': 'hard',
            'true_false_answer': False
        },
        {
            'content': 'Python中的弱引用可以防止循环引用导致的内存泄漏。',
            'question_type': 'true_false',
            'difficulty_level': 'hard',
            'true_false_answer': True
        },
        {
            'content': 'Python中的asyncio事件循环是线程安全的。',
            'question_type': 'true_false',
            'difficulty_level': 'hard',
            'true_false_answer': False
        },
        # 填空题 - 困难
        {
            'content': '在Python中，_____ 方法可以自定义对象的字符串表示，主要用于调试。',
            'question_type': 'fill_in_blank',
            'difficulty_level': 'hard',
            'fill_answer': '__repr__'
        },
        {
            'content': 'Python中的 _____ 装饰器可以将方法转换为类方法。',
            'question_type': 'fill_in_blank',
            'difficulty_level': 'hard',
            'fill_answer': '@classmethod'
        },
        # 简答题 - 困难
        {
            'content': '详细解释Python中的描述符协议，并说明其在属性访问中的作用机制。',
            'question_type': 'essay',
            'difficulty_level': 'hard',
            'essay_answer': '描述符协议定义了__get__、__set__、__delete__方法。当访问对象属性时，如果该属性是描述符对象，Python会调用相应的描述符方法。这是property、staticmethod、classmethod等功能的底层实现机制。'
        },
        {
            'content': '解释Python中的内存管理机制，包括引用计数、垃圾回收和内存池。',
            'question_type': 'essay',
            'difficulty_level': 'hard',
            'essay_answer': 'Python使用引用计数作为主要的内存管理机制，当对象引用计数为0时立即释放。同时使用标记-清除和分代回收处理循环引用。内存池机制用于小对象的快速分配和释放，提高性能。'
        }
    ]
    
    # 合并所有题目
    all_questions = easy_questions + medium_questions + hard_questions
    
    # 添加题目到数据库
    added_count = 0
    for question_data in all_questions:
        try:
            question = Question.objects.create(**question_data)
            added_count += 1
            print(f"成功添加题目 {added_count}: {question.content[:50]}...")
        except Exception as e:
            print(f"添加题目失败: {e}")
            print(f"题目数据: {question_data}")
    
    print(f"\n总共成功添加 {added_count} 道题目")
    print(f"简单难度: {len(easy_questions)} 道")
    print(f"中等难度: {len(medium_questions)} 道") 
    print(f"困难难度: {len(hard_questions)} 道")

if __name__ == '__main__':
    print("开始添加示例题目...")
    add_sample_questions()
    print("题目添加完成！")