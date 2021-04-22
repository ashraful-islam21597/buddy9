import cloudinary
from cloudinary import CloudinaryImage
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
import datetime

from .forms import commentForm
from .models import Response, Profile, status, friend, notification, coverphotos, profilephotos, Liker, comments, \
    replies, chatroom, allmessages, user_cover_photos, user_profile_photos, user_timeline_photos, usersociallink, \
    user_compressed_timeline_image, Videos

import PIL
from PIL import Image


def signin(request):
    if 'SignUp' in request.POST:
        name = request.POST['name']
        contact = request.POST['contact']
        username = request.POST['Username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        birthday = request.POST['dd']
        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "usernametaken")
                return render(request, "account.html")
            if User.objects.filter(password=password).exists():
                messages.info(request, "Password not strong")
                return render(request, "account.html")
            if User.objects.filter(email=email).exists():
                messages.info(request, "duplicate email")
                return render(request, "account.html")


            else:

                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();

                u = Profile(name=name, contact=contact,birthday=birthday, username=username, email=email, password=password)
                u.save()
                k=get_object_or_404(Profile,pk=u.id)
                l = usersociallink(user_link_id=k.id)
                l.save()
                f = friend.objects.create(name=name, contact=contact, username=username, email=email)
                f.save()
                q = auth.authenticate(username=username, password=password)
                q1=get_object_or_404(Profile, username=q.username)
                q1.active_status="yes"
                q1.save()
                auth.login(request, q)
                return redirect('/')
        else:
            return render(request, 'account.html')
    if 'Login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        q = auth.authenticate(username=username, password=password)


        if q is not None:
            q1 = get_object_or_404(Profile, username=q.username)
            q1.active_status="yes"
            q1.save()

            auth.login(request, q)

            return redirect('/')
        else:
            messages.info(request, "wrong credential")
            return render(request, "account.html")

    else:
        return render(request, 'account.html')

def profile(request):
    if request.user is not None and request.user.is_authenticated:
        s1 = []
        #p2 = []
        #a2 = []
        f1 = []
        q = get_object_or_404(Profile, username=request.user.username)
        #p = coverphotos.objects.filter(userpic__id=q.id)
        s = Profile.objects.all()
        q1 = get_object_or_404(friend, pk=q.id)
        link = usersociallink.objects.get(user_link_id=q.id)
        x = q1.user.add(q)
        x = q1.user.all()
        stat = status.objects.order_by('-updated_at')
        if x:
            for i in x:
                a = coverphotos.objects.filter(userpic__id=i.id)

                f1.append(i.id)
            s1 = status.objects.filter(user__id__in=f1).order_by('-updated_at')

        if 'editprofile' in request.POST:
            return HttpResponseRedirect(reverse('blog:editprofile', args=(id,)))

        elif 'profile' in request.POST:

            return HttpResponseRedirect(reverse('blog:friendprofile', args=(q.username,)))
            #return HttpResponseRedirect('/' + str(q.username))
            #return render(request, 'new_profile.html', {'q': q, 'x': x, 'link': link})
        elif 'Logout' in request.POST:
            auth.logout(request)
            q.active_status="No"
            q.save()
            return redirect("/signin/")
        elif 'uploadtimelinevideo' in request.POST:
            caption = request.POST['caption']
            timelinevideo = request.FILES['timelinevideo'];
            v = Videos(uservideo_id=q.id, video=timelinevideo)
            v.save()
            pro = status(user_id=q.id, caption=caption, video=v.video)
            pro.save()
            res = Response(status_id=pro.id, like=0)
            res.save()
            return redirect('/')


        elif 'add' in request.POST:
            posts = request.POST['post']
            pro = status(user_id=q.id, post=posts)
            pro.save()
            res = Response(status_id=pro.id, like=0)
            res.save()
            return redirect('/')

        elif 'uploadtimelinephoto' in request.POST:
            caption = request.POST['caption']
            timelinepic = request.FILES['timelineimage'];
            if timelinepic.size < 10485760:
                user_timeline_photo = user_timeline_photos(idtimelineowner_id=q.id, timenine_picture=timelinepic)
                user_timeline_photo.save()
                c=CloudinaryImage(str(timelinepic)).image()

                pro = status(user_id=q.id, caption=caption, timeline_pic=user_timeline_photo.timenine_picture)
                #pro = status(user_id=q.id, caption=caption, timeline_pic=c)
                pro.save()
                res = Response(status_id=pro.id, like=0)
                res.save()
                return redirect('/')
            else:
                return HttpResponse("file size too large. file size should be less than 10mb")
        elif 'friend' in request.POST:
            return HttpResponseRedirect(reverse('blog:addfriend', args=(q.id,)))

        elif 'submit' in request.POST:
            job = request.POST['job']
            present_address = request.POST['presentaddress']
            permanent_address = request.POST['permanentaddress']
            school = request.POST['School']
            college = request.POST['College']
            email = request.POST['email']
            phone = request.POST['phone']
            #birthday = request.POST['dd']
            q.job = job
            q.present_address = present_address
            q.permanent_address = permanent_address
            q.school = school
            q.college = college
            q.email = email
            #q.birthday = birthday
            q.contact = phone
            q.save()
            return redirect('/')

        elif 'search' in request.POST:

            search = request.POST['s']
            s = Profile.objects.filter(username__icontains=search).first()
            if s:
                return HttpResponseRedirect(reverse('blog:friendprofile', args=(s.username,)))
            else:
                return HttpResponse("user not found")

        elif 'coverphoto' in request.POST:
            pic = request.FILES['cover_photo'];

            if pic.size < 10485760 :
                user_cover_photo = user_cover_photos(idcoverowner_id=q.id, cover_picture=pic)
                user_cover_photo.save()


                sta = status(user_id=q.id, cover_pic=user_cover_photo.cover_picture)
                sta.save()
                u = coverphotos(userpic_id=q.id, cover_pic=user_cover_photo.cover_picture)
                q.coverpicture = user_cover_photo.cover_picture
                q.save()
                u.save()
                res = Response(status_id=sta.id, like=0)
                res.save()
                return redirect(request.META['HTTP_REFERER'],{'link': link})
            else:
                return HttpResponse("file size too large. file size should be less than 10mb")

        elif 'upload' in request.POST:
            pic = request.FILES['image'];
            if pic.size <10485760:
                user_profile_photo = user_profile_photos(idoprofilewner_id=q.id, pro_picture=pic)
                user_profile_photo.save()
                sta = status(user_id=q.id, profile_pic=user_profile_photo.pro_picture)
                sta.save()
                u = profilephotos(userpic_id=q.id, profile_pic=user_profile_photo.pro_picture)
                q.profilepicture = user_profile_photo.pro_picture
                q.save()
                u.save()
                res = Response(status_id=sta.id, like=0)
                res.save()
                return redirect('/')
            else:
                return HttpResponse("file size too large. file size should be less than 10mb")

        elif 'i' in request.POST:
            q4 = get_object_or_404(status, pk=request.POST['i'])

            q1 = q4.response_set.get(pk=request.POST['i'])

            try:
                ls = Liker.objects.get(status_id=request.POST['i'], liker_id=q.id)
                q1.like -= 1
                q1.save()
                ls.delete()
                return redirect(request.META['HTTP_REFERER'],{'link': link})
            except:
                ls = q4.liker_set.create(status_id=request.POST['i'], liker_id=q.id)
                ls.save()
                q1.like += 1
                q1.save()
                # return HttpResponseRedirect('/', {'q1': q1})
                return redirect(request.META['HTTP_REFERER'], {'link': link})

        elif 'save_comment' in request.POST:

            ss = get_object_or_404(status, pk=request.POST['i.id'])

            c = comments(status_id=ss.id, commentator_id=q.id, comment=request.POST['p1'])
            c.save()

            return redirect(request.META['HTTP_REFERER'],{'link': link})

        elif "i.id" in request.POST:
            #print(request.POST[i.id])
            #x=request.POST["p{{ i.id }}"]

            print(request.POST['i.id'])
            # print(request.POST['p'])
            ss = get_object_or_404(status, pk=request.POST['i.id'])
            print(ss.post)
            c = comments(status_id=ss.id, commentator_id=q.id, comment=request.POST['p'])
            c.save()
            return redirect(request.META['HTTP_REFERER'],{'link': link})
        elif 'j.id' in request.POST:
            cc = get_object_or_404(comments, pk=request.POST['j.id'])
            rep = replies(reply_id=cc.id, replier_id=q.id, text=request.POST['p'])
            rep.save()
            return redirect(request.META['HTTP_REFERER'],{'link': link})

        elif 'delete' in request.POST:
            print('delete')
            s = status.objects.get(id=request.POST['delete'])
            s.delete()
            return redirect(request.META['HTTP_REFERER'], {'link': link})

        elif 'delete_comment' in request.POST:
            s = comments.objects.get(id=request.POST['delete_comment'])
            s.delete()
            return redirect(request.META['HTTP_REFERER'], {'link': link})

        elif 'delete_reply' in request.POST:
            s = replies.objects.get(id=request.POST['delete_reply'])
            s.delete()
            return redirect(request.META['HTTP_REFERER'], {'link': link})

        elif 'link' in request.POST:
            facebook = request.POST['facebook']
            instragram = request.POST['instragram']
            twitter = request.POST['twitter']
            linkedin = request.POST['linkedin']
            snapchat = request.POST['snapchat']
            youtube = request.POST['youtube']
            github = request.POST['github']
            s = facebook
            link.faceebook = s
            link.instragram = instragram
            link.twitter = twitter
            link.linkedin = linkedin
            link.snapchat = snapchat
            link.youtube = youtube
            link.github = github
            link.save()
            return redirect('/')
        elif 'share' in request.POST:
            j=request.POST['share']
            q1 = status.objects.get(id=j)
            if q1.timeline_pic:
                #user_timeline_photo.save()
                #c=CloudinaryImage(str(timelinepic)).image()
                cap=q.name+ " shared "+q1.user.name+"`s timeline photo"
                pro = status(user_id=q.id,shared_caption=cap, caption=q1.caption,  timeline_pic=q1.timeline_pic)
                #pro = status(user_id=q.id, caption=caption, timeline_pic=c)
                pro.save()
                res = Response(status_id=pro.id, like=0)
                res.save()
                return redirect('/')
            if q1.profile_pic:
                cap=q.name+ " shared "+q1.user.name+"`s profile photo"
                sta = status(user_id=q.id,shared_caption=cap, profile_pic=q1.profile_pic)
                sta.save()
                u = profilephotos(userpic_id=q.id, profile_pic=q1.profile_pic)
                #q.profilepicture = user_profile_photo.pro_picture
                #q.save()
                u.save()
                res = Response(status_id=sta.id, like=0)
                res.save()
                return redirect('/')
            if q1.cover_pic:
                cap=q.name+ " shared "+q1.user.name+"`s cover photo"
                sta = status(user_id=q.id,shared_caption=cap, cover_pic=q1.cover_pic)
                sta.save()
                u = coverphotos(userpic_id=q.id, cover_pic=q1.cover_pic)
                #q.coverpicture = user_cover_photo.cover_picture
                #q.save()
                u.save()
                res = Response(status_id=sta.id, like=0)
                res.save()




                #posts = request.POST['post']
                pro = status(user_id=q.id, post=q1.post)
                pro.save()
                res = Response(status_id=pro.id, like=0)
                res.save()
                #return redirect('/')
                return redirect(request.META['HTTP_REFERER'],{'link': link})


            #return redirect('/')
        elif 'k1' in request.POST:
            k = request.POST['k1']
            q1 = Profile.objects.get(username=request.POST['k1'])
            q2 = get_object_or_404(Profile, pk=q1.id)
            a = get_object_or_404(friend, pk=q.id)
            a.user.add(q2)
            x = a.user.all()

            message = "sent you a friend request"
            q3 = notification(fr_id=q1.id, ins=q.username, message=message)
            q3.save()
            return HttpResponseRedirect('/' + str(q1.username))
        elif 'del' in request.POST:
            # k = request.POST['k1']
            q1 = Profile.objects.get(username=request.POST['del'])
            q2 = get_object_or_404(Profile, pk=q1.id)
            a = get_object_or_404(friend, pk=q.id)
            a.user.remove(q2)
            x = a.user.all()
            print(x)
            message = "sent you a friend request"
            return HttpResponseRedirect('/' + str(q1.username))
        # elif 'i.id' in request.POST:
        #     #print(request.POST[i.id])
        #     ss = get_object_or_404(status, pk=request.POST['i.id'])
        #     data=comments(status_id=ss.id, commentator_id=q.id, comment=request.POST['i.id'])
        #     form = commentForm(request.POST,data)
        #     if form.is_valid():
        #         form.save()
        #         print("H")
        #         return redirect('/')
        #     else:
        #         print('k')
        #         return redirect('/')



        else:

            return render(request, 'home1.html', context={
                'q': q,
                's': s,
                'stat': stat,
                'x': x,
                's1': s1,
                'link': link
            })
    else:
        return HttpResponseRedirect('/signin/')


def friendprofile(request, username):
    if request.user is not None and request.user.is_authenticated:
        q1 = Profile.objects.get(username=request.user.username)
        # q2=q1.friend_set.get(username=username)
        q2 = get_object_or_404(Profile, username=username)
        link = usersociallink.objects.get(user_link_id=q2.id)
        q3 = q1.friend_set.get(username=request.user.username)
        q = Profile.objects.get(username=q2.username)
        # q1 = get_object_or_404(friend, pk=q.id)
        x = q3.user.all()
        #print(q1,q,q2)

        return render(request, 'friendprofile.html', {'q': q, 'x': x, 'q1': q1,'link':link})
    else:
        return HttpResponseRedirect('/signin/')


def home(self):
    return redirect('/')


def logout(request):
    q = Profile.objects.get(username=request.user.username)
    if q is not None and request.user.is_authenticated:
        auth.logout(request)
        return HttpResponseRedirect('/signin/')
    else:
        return HttpResponseRedirect('/signin/')

def delete(request):
    s = status.objects.get(id=request.POST['delete'])
    s.delete()
    return redirect(request.META['HTTP_REFERER'])
def addfriend(request):
    if request.user is not None and request.user.is_authenticated:

        friends = []
        q = Profile.objects.get(username=request.user.username)
        f = q.friend_set.all()
        p = get_object_or_404(friend, pk=q.id)
        x = p.user.all()

        s = Profile.objects.all()

        for i in x:
            friends.append(i)
        for i in s:
            for j in q.friend_set.all():
                if j.username == i.username:
                    if i not in x:
                        friends.append(i)
                else:
                    continue
        z = list(s)
        print(z)
        print(friends)
        print(x)
        k = []
        k = (friends)
        for i in z:

            for j in friends:
                if j in z:
                    z.remove(j)
                else:
                    continue

        for i in friends:
            for j1 in x:
                if j1 in friends:
                    k.remove(j1)
                else:
                    continue
        print(k)
        if 'back' in request.POST:
            return redirect('/')
        elif 'i' in request.POST:
            q1 = Profile.objects.get(username=request.POST['i'])
            q2 = get_object_or_404(Profile, pk=q1.id)
            p.user.add(q2)
            x = p.user.all()

            message = "accepted your friend request"
            q3 = notification(fr_id=q1.id, ins=q.name, message=message)
            q3.save()

            return HttpResponseRedirect('/addfriend/')
            # return redirect('/')

            # return render(request, 'friends.html', context={'s': s,'q':q,'x':x})
        elif 'k' in request.POST:
            k = request.POST['k']
            q1 = Profile.objects.get(username=request.POST['k'])
            q2 = get_object_or_404(Profile, pk=q1.id)
            p.user.add(q2)
            x = p.user.all()

            message = "sent you a friend request"
            q3 = notification(fr_id=q1.id, ins=q.username, message=message)
            q3.save()
            # f=friendrequest(fr_id=q1.id,friensname=q.name,friensusername_id=q.id)
            # f.save()
            return HttpResponseRedirect('/addfriend/')
            # return render(request, 'friends.html', context={'s': s,'k':k ,'q': q,'z':z, 'x': x})

        else:
            return render(request, 'addfriend.html', context={'s': s, 'friends': friends, 'k': k, 'q': q, 'z': z, 'x': x})
    else:
        return redirect('/signin/')


def note(request):
    if request.user is not None and request.user.is_authenticated:
        q = Profile.objects.get(username=request.user.username)
        p = get_object_or_404(friend, pk=q.id)
        x1 = p.user.all()
        j = 0
        for i in x1:
            j += 1
        print(j)
        if request.method == "POST":
            q1 = Profile.objects.get(username=request.POST['i'])
            q2 = get_object_or_404(Profile, pk=q1.id)
            p.user.add(q2)
            x = p.user.all()

            message = "accepted your friend request"
            q3 = notification(fr_id=q1.id, ins=q.name, username=q.username, message=message)
            q3.save()
            j -= 1

            return redirect('/')
        else:
            return render(request, 'notification.html', {'q': q})
    else:

        return redirect('/signin/')


def chats(request, username):
    if request.user is not None and request.user.is_authenticated:
        owner1 = Profile.objects.get(username=request.user.username)
        owner2 = Profile.objects.get(username=username)

        if 'sendpic' in request.POST:
            try:
                userchating1 = chatroom.objects.get(userchat_id=owner1.id, chatname=username)
                userchating2 = chatroom.objects.get(userchat_id=owner2.id, chatname=owner1.username)

                m = allmessages(usermessage_id=owner1.id, chatroom_id=userchating1.id, messagepic=request.FILES['messageimage'])
                m.save()
                m1 = allmessages(usermessage_id=owner1.id, chatroom_id=userchating2.id, messagepic=request.FILES['messageimage'])
                m1.save()

                # return render(request,'chat.html',{'userchating1':userchating1})
                return HttpResponseRedirect('/chat/' + username)
            except:

                con1 = chatroom(userchat_id=owner1.id, chatname=owner2.username)
                con1.save()
                con2 = chatroom(userchat_id=owner2.id, chatname=owner1.username)
                con2.save()
                m = allmessages(usermessage_id=owner1.id, chatroom_id=con1.id, messagepic=request.FILES['messageimage'])
                m.save()
                m1 = allmessages(usermessage_id=owner1.id, chatroom_id=con2.id, messagepic=request.FILES['messageimage'])
                m1.save()

                return HttpResponseRedirect('/chat/' + username)



        elif 'send' in request.POST:
            try:
                userchating1 = chatroom.objects.get(userchat_id=owner1.id, chatname=username)
                userchating2 = chatroom.objects.get(userchat_id=owner2.id, chatname=owner1.username)

                m = allmessages(usermessage_id=owner1.id, chatroom_id=userchating1.id, message=request.POST['message'])
                m.save()
                m1 = allmessages(usermessage_id=owner1.id, chatroom_id=userchating2.id, message=request.POST['message'])
                m1.save()

                # return render(request,'chat.html',{'userchating1':userchating1})
                return HttpResponseRedirect('/chat/' + username)
            except:

                con1 = chatroom(userchat_id=owner1.id, chatname=owner2.username)
                con1.save()
                con2 = chatroom(userchat_id=owner2.id, chatname=owner1.username)
                con2.save()
                m = allmessages(usermessage_id=owner1.id, chatroom_id=con1.id, message=request.POST['message'])
                m.save()
                m1 = allmessages(usermessage_id=owner1.id, chatroom_id=con2.id, message=request.POST['message'])
                m1.save()

                return HttpResponseRedirect('/chat/' + username)
        elif 'back1' in request.POST:
            return HttpResponseRedirect('/')
        else:
            return render(request, 'chat.html', {'owner1': owner1, 'owner2': owner2})

    else:
        return HttpResponseRedirect('/signin/')
def Photos(request, username):
    if request.user is not None and request.user.is_authenticated:
        q1 = Profile.objects.get(username=request.user.username)
        q2 = get_object_or_404(Profile, username=username)
        return render(request, 'photo.html', {'q1': q1, 'q2': q2})
    else:
        return HttpResponseRedirect('/signin/')

