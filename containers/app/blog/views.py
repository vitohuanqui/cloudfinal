from django.shortcuts import render,  get_object_or_404, redirect
from django.utils import timezone
from django.conf import settings

from .models import Post
from .forms import PostForm

from multiprocessing import Process
import os
import sys
import time
from django.http import HttpResponse

REQUEST_CPUTIME_SEC = 1.0
REQUEST_TIMEOUT_SEC = 5.0


class CpuBurner(object):
    def get_walltime(self):
        return time.time()

    def get_user_cputime(self):
        return os.times()[0]

    def busy_wait(self):
        for _ in xrange(100000):
            pass

    def burn_cpu(self):
        """Consume REQUEST_CPUTIME_SEC core seconds.
        This method consumes REQUEST_CPUTIME_SEC core seconds. If unable to
        complete within REQUEST_TIMEOUT_SEC walltime seconds, it times out and
        terminates the process.
        """
        start_walltime_sec = self.get_walltime()
        start_cputime_sec = self.get_user_cputime()
        while (self.get_user_cputime() <
               start_cputime_sec + REQUEST_CPUTIME_SEC):
            self.busy_wait()
            if (self.get_walltime() >
                    start_walltime_sec + REQUEST_TIMEOUT_SEC):
                sys.exit(1)

    def handle_http_request(self):
        """Process a request to consume CPU and produce an HTTP response."""
        start_time = self.get_walltime()
        p = Process(target=self.burn_cpu)  # Run in a separate process.
        p.start()
        # Force kill after timeout + 1 sec.
        p.join(timeout=REQUEST_TIMEOUT_SEC + 1)
        if p.is_alive():
            p.terminate()
        if p.exitcode != 0:
            return (500, "Request failed\n")
        else:
            end_time = self.get_walltime()
            response = "Request took %.2f walltime seconds\n" % (
                end_time - start_time)
            return (200, response)

def post_list(request):
    """Process a request to consume CPU and produce an HTTP response."""
    a = CpuBurner()
    
    return HttpResponse("%s." % a.handle_http_request()[1])
    return Response({"message": "hola"})
    
    return Response("message")
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts, 'pod_name': settings.MY_POD_NAME})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'pod_name': settings.MY_POD_NAME})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'pod_name': settings.MY_POD_NAME})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'pod_name': settings.MY_POD_NAME})
