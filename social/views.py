from django.shortcuts import render, redirect , get_object_or_404 , get_list_or_404
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from social.models import FollowUser, MyPost, MyProfile, PostComment, PostLike
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http.response import HttpResponseRedirect
from django.db import connection

cursor = connection.cursor()

# Create your views here.
@method_decorator(login_required, name="dispatch")    
class HomeView(TemplateView):
    template_name = "social/home.html"
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        followedList = FollowUser.objects.filter(followed_by = self.request.user.myprofile)
        followedList2 = []
        for e in followedList:
            followedList2.append(e.profile)
        postList = MyPost.objects.filter(uploaded_by__in = followedList2).order_by("-id")
        
        for p1 in postList:
            p1.liked = False
            ob = PostLike.objects.filter(post = p1,liked_by=self.request.user.myprofile)
            if ob:
                p1.liked = True        
            obList = PostLike.objects.filter(post = p1)
            p1.likedno = obList.count()
        context["mypost_list"] = postList
        return context

    




def follow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/myprofile")

def unfollow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/myprofile")

def like(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/home")

def unlike(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/home")


@method_decorator(login_required, name="dispatch")    
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name", "fname","lname","bio","acc_type","branch","societies", "age", "address", "bio", "gender", "phone_no", "pic"]

@method_decorator(login_required, name="dispatch")    
class MyPostCreate(CreateView):
    model = MyPost
    fields = ["subject", "msg", "pic"]
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name="dispatch")    
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        return MyPost.objects.filter(Q(uploaded_by = self.request.user.myprofile)).filter(Q(subject__icontains = si) | Q(msg__icontains = si)).order_by("-id")
 
@method_decorator(login_required, name="dispatch")    
class MyPostDetailView(DetailView):
    model = MyPost

@method_decorator(login_required, name="dispatch")    
class MyPostDeleteView(DeleteView):
    model = MyPost

@method_decorator(login_required, name="dispatch")    
class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        profList = MyProfile.objects.filter((Q(name__icontains = si) | Q(address__icontains = si) | Q(gender__icontains = si)) & ~Q(user=self.request.user)).order_by("-id")
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile = p1) 
            ob1 = FollowUser.objects.filter(followed_by = p1) 
            if ob:
                p1.followed = True
            p1.followno = ob.count()
            p1.followingno = ob1.count()
        return profList

@method_decorator(login_required, name="dispatch")    
class MyProfileDetailView(DetailView):
    model = MyProfile 



class PostCommentCreate(CreateView):
    model = PostComment
    fields =  ['msg']

    def form_valid(self, form, **kwargs):
        form.instance.commented_by = self.request.user.myprofile
        form.instance.post= get_object_or_404(MyPost, pk = self.kwargs['post_id'])
        
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())




def showcomments(request, post_id):
    post = MyPost.objects.get(pk= post_id)
    return render(request, 'social/postcomment_list.html', {'post': post, 'comments': PostComment.objects.raw("select * from social_postcomment where post_id = %s", [post_id])})


def profview(request, pk):
    post= MyPost.objects.filter(uploaded_by_id = pk)
    myprofile = MyProfile.objects.get(pk = pk)
    
    return render(request, 'social/myprofile_detail.html', {'post': post , 'myprofile' : myprofile })




    


   

 

