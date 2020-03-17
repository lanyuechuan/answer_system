from django.db import models

# class Answer(models.Model):
#     """答案表"""
#     answer = models.CharField(max_length=7,verbose_name="正确答案")
#
#     class Meta:
#         db_table = "answer"
#         verbose_name = "答案表"
#         verbose_name_plural = verbose_name


class SubType(models.Model):
    """题目类型表"""
    type = models.CharField(max_length=10,verbose_name='题目类型')

    class Meta:
        db_table = "sub_type"
        verbose_name = "题目类型表"
        verbose_name_plural = verbose_name


class Subject(models.Model):
    """题目表"""
    type = models.ForeignKey(to=SubType,verbose_name="题目类型",on_delete=models.CASCADE)
    # answer_sub = models.ForeignKey(to=Answer,on_delete=models.CASCADE)
    sub = models.CharField(max_length=254,unique=True,verbose_name="问题")
    answer = models.CharField(max_length=32,unique=True,verbose_name="正确答案")
    sub_score = models.BigIntegerField(verbose_name="本题分数")
    sub_chioces = (
        (0, '单选'),
        (1, '多选')
    )
    sub_type = models.SmallIntegerField(default=1,choices=sub_chioces,verbose_name='题目选项类型')

    class Meta:
        db_table = "subject"
        verbose_name = "题目表"
        verbose_name_plural = verbose_name

class SubOption(models.Model):
    """题目选项内容表"""
    sub_option = models.ForeignKey(to=Subject, on_delete=models.CASCADE) # Subject表和该表一对多，外键sub_option
    option = models.CharField(max_length=128,verbose_name="选项具体内容")

    class Meta:
        db_table = "sub_options"
        verbose_name = "选项表"
        verbose_name_plural = verbose_name





