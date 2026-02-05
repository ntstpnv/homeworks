from django.views import generic


class BaseTemplateView(generic.TemplateView):
    title = None
    back = None

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "title": self.title,
            "back": self.back,
        }


class MenuView(generic.ListView):
    template_name = "common/menu.html"

    title = "Выберите задание"
    back = None

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "title": self.title,
            "back_exists": bool(self.back),
            "back": self.back,
        }


class BaseDetailView(generic.DetailView):
    title = None
    back = None

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "title": self.title,
            "back": self.back,
        }
