from django.shortcuts import render, redirect
from django.views import View
from hypernews.settings import NEWS_JSON_PATH
from json import load, dump
from django.http import HttpResponse, Http404
import datetime


# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect("news/")

class MainView(View):
    content = []

    def get(self, request, *args, **kwargs):
        with open(NEWS_JSON_PATH) as f:
            self.content = load(f)

        q = request.GET.get("q", None)
        if q is not None:
            filtered_content = filter(lambda x: q.lower() in x["title"].lower(), self.content)
            self.content = list(filtered_content)
        #     for news in self.content:
        #         news["created"] = news["created"].split()[0]
        #         sorted_news = sorted(self.content, key=lambda i: i['created'], reverse=True)
        #         container = {}
        #         news_4 = {}
        #         for item in sorted_news:
        #             if item["title"] == "News 4":
        #                 news_4 = item
        #             if item['created'] not in container:
        #                 container[item["created"]] = [item]
        #             else:
        #                 container[item['created']].append(item)
        #         context = {"content": container.items(), "news4": news_4}
        #         return render(
        #     request, "list_news/index.html", context=context
        # )


        for news in self.content:
            news["created"] = news["created"].split()[0]
        sorted_news = sorted(self.content, key=lambda i: i['created'], reverse=True)
        container = {}
        news_4 = {}
        for item in sorted_news:
            if item["title"] == "News 4":
                news_4 = item
            if item['created'] not in container:
                container[item["created"]] = [item]
            else:
                container[item['created']].append(item)
        context = {"content": container.items(), "news4": news_4}
        return render(
            request, "news/index.html", context=context
        )


class NewsView(View):
    content = []

    def get(self, request, link, *args, **kwargs):
        with open(NEWS_JSON_PATH) as f:
            self.content = load(f)
        html = ""
        context = {}
        for item in self.content:
            if int(link) == item["link"]:
                context = {"item" : item}
                html = f"""<div>
<h2>{item["title"]}</h2>
<p>{item["created"]}</p>
<p>{item["text"]}</p>
<a target="_blank" href="/news/">News article</a>
</div>"""
        if len(context.values()) == 0:
            raise Http404
        return render(request, "single_news/index.html", context=context)
        return HttpResponse(html)


class CreateNews(View):
    news_list = {}
    content = []

    def get(self, request, *args, **kwargs):
        return render(request, "create_news/index.html")

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        text = request.POST.get("text")
        now = datetime.datetime.now()

        self.news_list["title"] = title
        self.news_list["text"] = text
        self.news_list["created"] = now.strftime("%Y-%m-%d %X")
        self.news_list["link"] = int(now.strftime("%X").replace(":", ""))

        with open(NEWS_JSON_PATH, "r") as f:
            self.content = load(f)
            self.content.append(self.news_list)
        with open(NEWS_JSON_PATH, "w") as w:
            dump(self.content, w)

        return redirect("/news/")

