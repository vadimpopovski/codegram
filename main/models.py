from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
import jdatetime


class Person(models.Model):
    # Personal detail
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name='کاربر')
    username = models.CharField(max_length=50, verbose_name='نام کاربری' )
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='آواتار' )
    name = models.CharField(max_length=50, verbose_name='نام' )
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='توضیحات')
    year_of_born = models.CharField(max_length=4, null=True, blank=True, verbose_name='سال تولد')
    gender = models.CharField(max_length=10, null=True, blank=True, verbose_name='جنسیت')
    join_time = jmodels.jDateTimeField(default=timezone.now, verbose_name='زمان عضویت')

    # Professional detail
    # work = models.CharField(max_length=50, null=True, blank=True, verbose_name='تخصص')
    skills = models.ManyToManyField('Skill', blank=True, verbose_name='مهارت‌ها')
    rezome = models.TextField(default='', null=True, blank=True, verbose_name='رزومه')

    # Statistic detail
    liked_posts = models.ManyToManyField('Post', blank=True, verbose_name='پسندها')
    viewed_posts = models.ManyToManyField('Post', related_name='viewed_posts', blank=True, verbose_name='مطالب مشاهده شده')
    followings = models.ManyToManyField('Person', blank=True, verbose_name='دنبال شوندگان')
    len_followings = models.CharField(max_length=10, default=0, verbose_name='تعداد دنبال شوندگان')
    followers = models.ManyToManyField('Person', related_name='folllowers', blank=True, verbose_name='دنبال کنندگان')
    len_followers = models.CharField(max_length=10, default=0, verbose_name='تعداد دنبال کنندگان')

    # Social detail
    github = models.CharField(max_length=100, null=True, blank=True, verbose_name='گیت‌هاب')
    gitlab = models.CharField(max_length=100, null=True, blank=True, verbose_name='گیت‌لب')
    stackoverflow = models.CharField(max_length=100, null=True, blank=True, verbose_name='استک‌اورفلو')
    linkedin = models.CharField(max_length=100, null=True, blank=True, verbose_name='لینکدین')
    dev = models.CharField(max_length=100, null=True, blank=True, verbose_name='دِو')
    facebook = models.CharField(max_length=100, null=True, blank=True, verbose_name='فیسبوک')
    instagram = models.CharField(max_length=100, null=True, blank=True, verbose_name='اینستاگرام')
    twitter = models.CharField(max_length=100, null=True, blank=True, verbose_name='توییتر')
    virgool = models.CharField(max_length=100, null=True, blank=True, verbose_name='ویرگول')
    website = models.URLField(null=True, blank=True, verbose_name='تارنما')
    public_email = models.CharField(max_length=100, null=True, blank=True, verbose_name='رایانامه')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره تماس')
    telegram = models.CharField(max_length=100, null=True, blank=True, verbose_name='تلگرام')
    matrix = models.CharField(max_length=100, null=True, blank=True, verbose_name='ماتریکس')

    class Meta:
        verbose_name = 'فرد'
        verbose_name_plural = 'افراد'

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    slug = models.CharField(max_length=50, blank=True, null=True)
    body = models.TextField(verbose_name='متن')
    cover = models.CharField(max_length=1000, null=True, blank=True, verbose_name='کاور')
    short_description = models.TextField(max_length=156, null=True, blank=True, verbose_name='توضیح کوتاه')
    author = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, verbose_name='نویسنده')
    publish_time = jmodels.jDateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    comments = models.ManyToManyField('Comment', blank=True, verbose_name='نظرات')
    likes = models.ManyToManyField('Person', blank=True, related_name='likes', verbose_name='پسندیدگان')

    # Statistic
    len_comments = models.CharField(max_length=10, default='0', verbose_name='تعداد نظر')
    len_likes = models.CharField(max_length=10, default='0', verbose_name='تعداد پسند')
    views = models.CharField(max_length=10, default='0', verbose_name='تعداد بازدید')

    class Meta:
        verbose_name = 'مطلب'
        verbose_name_plural = 'مطالب'

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, verbose_name='نویسنده')
    text = models.CharField(max_length=1000, verbose_name='متن')
    replys = models.ManyToManyField('Comment', blank=True, verbose_name='پاسخ‌ها')
    submit_time = jmodels.jDateTimeField(default=timezone.now, verbose_name='زمان ثبت')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class Ad(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, verbose_name='مطلب')
    type = models.CharField(max_length=50, verbose_name='نوع')
    end_date = jmodels.jDateTimeField(default=jdatetime.datetime.today(), verbose_name='زمان پایان')

    class Meta:
        verbose_name = 'تبلیغ'
        verbose_name_plural = 'تبلیغات'


class Skill(models.Model):
    name = models.CharField(max_length=50, verbose_name='مهارت')

    class Meta:
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت‌ها'

    def __str__(self):
        return self.name


class Notification(models.Model):
    receiver = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, verbose_name='گیرنده')
    message = models.TextField(verbose_name='متن پیام')
    notif_type = models.CharField(max_length=10, default=None, null=True, verbose_name='نوع')
    done = models.BooleanField(default=False, verbose_name='خوانده شده')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام‌ها'


class Cloud(models.Model):
    owner = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, verbose_name='صاحب')
    space = models.CharField(max_length=25, default=25, verbose_name='فضا')
    used_space = models.CharField(max_length=25, default=0, verbose_name='فضای استفاده شده')
    used_percent = models.CharField(max_length=5, default=0, verbose_name='درصد استفاده شده')

    class Meta:
        verbose_name = 'ابر'
        verbose_name_plural = 'ابر‌ها'

    def __str__(self):
        return 'ابر {}'.format(self.owner)


class File(models.Model):
    cloud = models.ForeignKey('Cloud', on_delete=models.CASCADE, null=True, verbose_name='ابر')
    file = models.ImageField(upload_to='images/', blank=True, verbose_name='فایل')


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Person.objects.create(user=instance, username=instance.username)
            person = Person.objects.get(user=instance)
            Cloud.objects.create(owner=person)

        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
