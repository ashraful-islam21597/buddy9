import os
import sys

from cloudinary import CloudinaryImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File

from PIL import Image, ExifTags
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.db import models
from cloudinary.models import CloudinaryField




class Profile(models.Model):
    name=models.CharField(max_length=120)
    contact=models.CharField(max_length=11)
    email=models.EmailField(max_length=120)
    username=models.CharField(max_length=120)
    password=models.CharField(max_length=120)
    confirmpassword = models.CharField(max_length=120)
    present_address=models.TextField(max_length=120,null=True,blank=True)
    permanent_address = models.TextField(max_length=120,null=True,blank=True)
    job = models.CharField(max_length=120,null=True,blank=True)
    birthday = models.DateField()
    school = models.TextField(max_length=120, null=True, blank=True)
    college = models.TextField(max_length=120, null=True, blank=True)
    profilepicture=CloudinaryField('image')
    coverpicture = CloudinaryField('image')
    profilepicture_url=models.CharField(max_length=400)

    def __str__(self):
        return self.username
    def profileimage(self):
        return self.profilepicture

class user_compressed_timeline_image(models.Model):
    idofuser=models.ForeignKey(Profile, on_delete=models.CASCADE)
    timeline_picture=models.ImageField(upload_to="user_image")
    def save(self,*args,**kwargs):
        try:
            super().save(args, kwargs)
            images = Image.open(self.timeline_picture.path)
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(images._getexif().items())

            if exif[orientation] == 3:
                images = images.rotate(180, expand=True)
            elif exif[orientation] == 6:
                images = images.rotate(270, expand=True)
            elif exif[orientation] == 8:
                images = images.rotate(90, expand=True)
            # image.save(filepath)
            # image.close()
            print('1')
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            print('2')
            pass
        if images.height > 600 or images.width > 600:
            print('3')
            output_size = (600, 600)
            images.thumbnail(output_size)
            images.save(self.timeline_picture.path)

class user_timeline_photos(models.Model):
    idtimelineowner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timenine_picture = CloudinaryField('image')

    # def save(self,*args,**kwargs):
    #     try:
    #         super().save(args, kwargs)
    #         images = Image.open(self.timenine_picture.path)
    #         for orientation in ExifTags.TAGS.keys():
    #             if ExifTags.TAGS[orientation] == 'Orientation':
    #                 break
    #         exif = dict(images._getexif().items())
    #
    #         if exif[orientation] == 3:
    #             images = images.rotate(180, expand=True)
    #         elif exif[orientation] == 6:
    #             images = images.rotate(270, expand=True)
    #         elif exif[orientation] == 8:
    #             images = images.rotate(90, expand=True)
    #         # image.save(filepath)
    #         # image.close()
    #         print('1')
    #     except (AttributeError, KeyError, IndexError):
    #         # cases: image don't have getexif
    #         print('2')
    #         pass
    #     if images.height > 600 or images.width > 600:
    #         print('3')
    #         output_size = (600, 600)
    #         images.thumbnail(output_size)
    #         images.save(self.timenine_picture.path)
class user_cover_photos(models.Model):
    idcoverowner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cover_picture = CloudinaryField('image')




    # def save(self,*args,**kwargs):
    #     try:
    #         super().save(args, kwargs)
    #         images = Image.open(self.cover_picture.path)
    #         for orientation in ExifTags.TAGS.keys():
    #             if ExifTags.TAGS[orientation] == 'Orientation':
    #                 break
    #         exif = dict(images._getexif().items())
    #
    #         if exif[orientation] == 3:
    #             images = images.rotate(180, expand=True)
    #         elif exif[orientation] == 6:
    #             images = images.rotate(270, expand=True)
    #         elif exif[orientation] == 8:
    #             images = images.rotate(90, expand=True)
    #         # image.save(filepath)
    #         # image.close()
    #         print('1')
    #     except (AttributeError, KeyError, IndexError):
    #         # cases: image don't have getexif
    #         print('2')
    #         pass
    #     if images.height > 800 or images.width > 800:
    #         print('3')
    #         output_size = (800, 800)
    #         images.thumbnail(output_size)
    #         images.save(self.cover_picture.path)
class user_profile_photos(models.Model):
    idoprofilewner=models.ForeignKey(Profile,on_delete=models.CASCADE)
    pro_picture = CloudinaryField('image')
    # def save(self,*args,**kwargs):
    #     super().save(args, kwargs)
    #     images = Image.open(self.pro_picture.path)
    #     if images.width > 300 or images.height > 300:
    #         print('3')
    #         output_size = (300, 300)
    #         images.thumbnail(output_size)
    #         images.save(self.pro_picture.path)

    # def save(self,*args,**kwargs):
    #
    #
    #     try:
    #         super().save(args, kwargs)
    #         images = Image.open(self.pro_picture.path)
    #         print('try')
    #
    #         for orientation in ExifTags.TAGS.keys():
    #             if ExifTags.TAGS[orientation] == 'Orientation':
    #                 break
    #         exif = dict(images._getexif().items())
    #
    #         if exif[orientation] == 3:
    #             images = images.rotate(180, expand=True)
    #         elif exif[orientation] == 6:
    #             images = images.rotate(270, expand=True)
    #         elif exif[orientation] == 8:
    #             images = images.rotate(90, expand=True)
    #     except (AttributeError, KeyError, IndexError):
    #         pass


class status(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    post=models.TextField(max_length=10000)
    caption=models.TextField(max_length=10000)
    shared_caption=models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sdate = models.DateField(auto_now=True)
    stime = models.TimeField(auto_now=True)
    timeline_pic = CloudinaryField('image')
    profile_pic = CloudinaryField('image')
    cover_pic = CloudinaryField('image')
    video = models.FileField(upload_to='st_videos')

    def cover(self):
        return self.user.coverpicture
    def now(self):
        return self.updated_at.now()
    def img(self):
        return self.user.profilepicture
    def __str__(self):
        return self.user.name
    def np(self):
        return self.user.name
    def u(self):
        return self.user.username
    def time(self):
        date = (str(self.updated_at).split(' ')[0])
        d1 = date.split('-')
        d1_list = [int(i) for i in d1]
        m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        f = (str(str(self.updated_at).split(' ')[1]).split(":")[0])
        g = (str(str(self.updated_at).split(' ')[1]).split(":")[1])
        k = int(f) + 6
        if k>=24:
            k1 = k - 24
            if k1 == 0:
                s = str(12) + (':') + g + " a.m "

            else:
                s = str(k1) + (':') + g + " a.m "

            return  s
        else:
            if k%12==0 :
                s = str(12) + (':') + g+" p.m"

            else:
                if k>12:
                    s = str(k%12) + (':') + g+" p.m "

                else:
                    s = str(k % 12) + (':') + g + " a.m "


            return s
    def date(self):
        date = (str(self.updated_at).split(' ')[0])
        d1 = date.split('-')
        d1_list = [int(i) for i in d1]
        m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
        f = (str(str(self.updated_at).split(' ')[1]).split(":")[0])
        g = (str(str(self.updated_at).split(' ')[1]).split(":")[1])
        k = int(f) + 6
        if k>=24:
            s3=str(d1_list[2]+1)+","+str(m[d1_list[1]-1])+","+str(d1_list[0])
            k1 = k - 24
            if k1 == 0:
                s = str(12) + (':') + g + " a.m "

            else:
                s = str(k1) + (':') + g + " a.m "

                # s="am"

            return s3
        else:
            s3 = str(d1_list[2]) + "," + str(m[d1_list[1] - 1]) + "," + str(d1_list[0])
            if k%12==0 :
                s = str(12) + (':') + g+" p.m"

            else:
                if k>12:
                    s = str(k%12) + (':')+g+"p.m"

                else:
                    s = str(k % 12) + (':') + g + " a.m "


            return s3
    def day(self):
        date = (str(self.updated_at).split(' ')[0])
        d1 = date.split('-')
        d1_list = [int(i) for i in d1]
        day=['Sat','Sun','Mon','Tue','Wed','Thu','Fri']
        m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        f = (str(str(self.updated_at).split(' ')[1]).split(":")[0])
        g = (str(str(self.updated_at).split(' ')[1]).split(":")[1])
        k = int(f) + 6
        year=d1_list[0]
        sub=year-1900
        div=sub//4
        rem=sub%4
        b=[1,4,4,0,2,5,0,3,6,1,4,6] #144025036146

        if k>=24:

            total=(d1_list[2]+1)+sub+div+rem+b[d1_list[1] - 1]
            s4 = day[total % 7]

            return s4
        else:
            total = d1_list[2] + sub + div + rem + b[d1_list[1] - 1]
            s4 = day[total % 7]

            return s4
class friend(models.Model):
    user = models.ManyToManyField(Profile)
    username = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    contact = models.TextField(max_length=11)
    email = models.EmailField(max_length=120)
    def __str__(self):
        return self.name
class coverphotos(models.Model):
    userpic = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, blank=True)
    cover_pic=CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)
class profilephotos(models.Model):
    userpic = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, blank=True)
    profile_pic=CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)
class timelinephotos(models.Model):
    userpic = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, blank=True)
    profile_pic=CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)
class Videos(models.Model):
    uservideo = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #title = models.CharField(max_length=100)
    #video=CloudinaryField('image')
    video = models.FileField(upload_to='videos')

class notification(models.Model):
    ins=models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    message=models.CharField(max_length=120)
    fr=models.ForeignKey(Profile,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fr.name
    def massage(self):
        return self.message
    def time(self):
        return self.updated_at
class friendrequest(models.Model):
    fr = models.ForeignKey(Profile, on_delete=models.CASCADE)
    friensname = models.CharField(max_length=120)
    friensusername = models.CharField(max_length=120)
    message = models.CharField(max_length=120)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Response(models.Model):
    status=models.ForeignKey(status, on_delete=models.CASCADE)
    #liker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like=models.IntegerField(default=0)


    def status_name(self):
        return self.status.user.name
    def status_post(self):
        return self.status.post
class Liker(models.Model):
    status=models.ForeignKey(status, on_delete=models.CASCADE)
    liker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stat=models.IntegerField(default=0)

    def likername(self):
        return self.liker.name
    def likerusername(self):
        return self.liker.username
    def likerimage(self):
        return self.liker.profilepicture
class comments(models.Model):
    status = models.ForeignKey(status, on_delete=models.CASCADE)
    commentator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=1000)
    def com(self):
        return self.commentator.name
    def compro(self):
        return self.commentator.profilepicture
    def ctime(self):
        date = (str(self.updated_at).split(' ')[0])
        d1 = date.split('-')
        d1_list = [int(i) for i in d1]
        m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        f = (str(str(self.updated_at).split(' ')[1]).split(":")[0])
        g = (str(str(self.updated_at).split(' ')[1]).split(":")[1])
        k = int(f) + 6
        if k>=24:
            k1 = k - 24
            if k1 == 0:
                s = str(12) + (':') + g + " a.m "

            else:
                s = str(k1) + (':') + g + " a.m "

            return  s
        else:
            if k%12==0 :
                s = str(12) + (':') + g+" p.m"

            else:
                if k>12:
                    s = str(k%12) + (':') + g+" p.m "

                else:
                    s = str(k % 12) + (':') + g + " a.m "


            return s
    def cdate(self):
        date = (str(self.updated_at).split(' ')[0])
        d1 = date.split('-')
        d1_list = [int(i) for i in d1]
        m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
        f = (str(str(self.updated_at).split(' ')[1]).split(":")[0])
        g = (str(str(self.updated_at).split(' ')[1]).split(":")[1])
        k = int(f) + 6
        if k>=24:
            s3=str(d1_list[2]+1)+","+str(m[d1_list[1]-1])+","+str(d1_list[0])
            k1 = k - 24
            if k1 == 0:
                s = str(12) + (':') + g + " a.m "

            else:
                s = str(k1) + (':') + g + " a.m "

                # s="am"

            return s3
        else:
            s3 = str(d1_list[2]) + "," + str(m[d1_list[1] - 1]) + "," + str(d1_list[0])
            if k%12==0 :
                s = str(12) + (':') + g+" p.m"

            else:
                if k>12:
                    s = str(k%12) + (':')+g+"p.m"

                else:
                    s = str(k % 12) + (':') + g + " a.m "


            return s3
    def cday(self):
        date = (str(self.updated_at).split(' ')[0])
        d1 = date.split('-')
        d1_list = [int(i) for i in d1]
        day=['Sat','Sun','Mon','Tue','Wed','Thu','Fri']
        m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        f = (str(str(self.updated_at).split(' ')[1]).split(":")[0])
        g = (str(str(self.updated_at).split(' ')[1]).split(":")[1])
        k = int(f) + 6
        year=d1_list[0]
        sub=year-1900
        div=sub//4
        rem=sub%4
        b=[1,4,4,0,2,5,0,3,6,1,4,6] #144025036146

        if k>=24:

            total=(d1_list[2]+1)+sub+div+rem+b[d1_list[1] - 1]
            s4 = day[total % 7]

            return s4
        else:
            total = d1_list[2] + sub + div + rem + b[d1_list[1] - 1]
            s4 = day[total % 7]

            return s4
class replies(models.Model):
    reply = models.ForeignKey(comments, on_delete=models.CASCADE)
    replier = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)
    def replier_name(self):
        return self.replier.name
    def replier_username(self):
        return self.replier.username
    def reppro(self):
        return self.replier.profilepicture
    def rtime(self):
        date = (str(self.updated_at).split(' ')[0])
        d1 = date.split('-')
        d1_list = [int(i) for i in d1]
        m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        f = (str(str(self.updated_at).split(' ')[1]).split(":")[0])
        g = (str(str(self.updated_at).split(' ')[1]).split(":")[1])
        k = int(f) + 6
        if k>=24:
            k1 = k - 24
            if k1 == 0:
                s = str(12) + (':') + g + " a.m "

            else:
                s = str(k1) + (':') + g + " a.m "

            return  s
        else:
            if k%12==0 :
                s = str(12) + (':') + g+" p.m"

            else:
                if k>12:
                    s = str(k%12) + (':') + g+" p.m "

                else:
                    s = str(k % 12) + (':') + g + " a.m "


            return s
    def rdate(self):
        date = (str(self.updated_at).split(' ')[0])
        d1 = date.split('-')
        d1_list = [int(i) for i in d1]
        m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
        f = (str(str(self.updated_at).split(' ')[1]).split(":")[0])
        g = (str(str(self.updated_at).split(' ')[1]).split(":")[1])
        k = int(f) + 6
        if k>=24:
            s3=str(d1_list[2]+1)+","+str(m[d1_list[1]-1])+","+str(d1_list[0])
            k1 = k - 24
            if k1 == 0:
                s = str(12) + (':') + g + " a.m "

            else:
                s = str(k1) + (':') + g + " a.m "

                # s="am"

            return s3
        else:
            s3 = str(d1_list[2]) + "," + str(m[d1_list[1] - 1]) + "," + str(d1_list[0])
            if k%12==0 :
                s = str(12) + (':') + g+" p.m"

            else:
                if k>12:
                    s = str(k%12) + (':')+g+"p.m"

                else:
                    s = str(k % 12) + (':') + g + " a.m "


            return s3
    def rday(self):
        date = (str(self.updated_at).split(' ')[0])
        d1 = date.split('-')
        d1_list = [int(i) for i in d1]
        day=['Sat','Sun','Mon','Tue','Wed','Thu','Fri']
        m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        f = (str(str(self.updated_at).split(' ')[1]).split(":")[0])
        g = (str(str(self.updated_at).split(' ')[1]).split(":")[1])
        k = int(f) + 6
        year=d1_list[0]
        sub=year-1900
        div=sub//4
        rem=sub%4
        b=[1,4,4,0,2,5,0,3,6,1,4,6] #144025036146

        if k>=24:

            total=(d1_list[2]+1)+sub+div+rem+b[d1_list[1] - 1]
            s4 = day[total % 7]

            return s4
        else:
            total = d1_list[2] + sub + div + rem + b[d1_list[1] - 1]
            s4 = day[total % 7]

            return s4

class chatroom(models.Model):
    userchat=models.ForeignKey(Profile,on_delete=models.CASCADE)
    chatname=models.CharField(max_length=120)
class allmessages(models.Model):
    usermessage=models.ForeignKey(Profile,on_delete=models.CASCADE)
    chatroom=models.ForeignKey(chatroom,on_delete=models.CASCADE)
    message=models.CharField(max_length=2000)
    messagepic = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def chatter(self):
        return self.usermessage.username
    def chatterpic(self):
        return self.usermessage.profilepicture
class usersociallink(models.Model):
    user_link=models.ForeignKey(Profile,on_delete=models.CASCADE)
    faceebook = models.CharField(max_length=120)
    instragram = models.CharField(max_length=120)
    linkedin = models.CharField(max_length=120)
    snapchat = models.CharField(max_length=120)
    github = models.CharField(max_length=120)
    youtube = models.CharField(max_length=120)
    twitter = models.CharField(max_length=120)
